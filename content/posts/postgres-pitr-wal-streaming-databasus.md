---
title: "Backup PostgreSQL Sampai ke Detik: PITR + WAL Streaming dengan Databasus"
date: 2026-09-28T00:05:00+07:00
draft: false
tags: ["PostgreSQL", "Backup", "DevOps", "Self-Hosted"]
---

`pg_dump` tiap jam itu enak sampai database kamu korup jam 14:37 — dan backup terakhir jam 03:00. Artinya 11 jam data kerja hilang, dan tidak ada cara "balik 1 menit sebelum kejadian". Solusinya bukan dump lebih sering (makin sering dump = makin mahal + makin lama), tapi **Point-in-Time Recovery (PITR)**. Artikel ini catatan pasang beneran di server kami, termasuk 7 jebakan yang bikin backup gagal tanpa kita sadar.

## Kenapa Dump Harian Tidak Cukup

Dump itu *logical* — isinya perintah SQL untuk membangun ulang tabel. Tiga kelemahannya: (1) ukurannya besar untuk DB yang sama, (2) tidak bisa dipakai untuk recovery parsial per detik, (3) makin sering jalan, makin berat ke production.

PITR cara kerjanya beda total. PostgreSQL selalu menulis *Write Ahead Log* (WAL) di `pg_wal/`: setiap perubahan data masuk ke log itu dulu sebelum ditulis ke tabel. Kalau kita simpan base backup + terus-terusan mengarsipkan WAL-nya, kita bisa "putar ulang" log itu sampai titik waktu mana pun setelah base backup dibuat.

| | `pg_dump` / `pg_dumpall` | PITR (base backup + WAL) |
|---|---|---|
| Jenis | snapshot logical (SQL) | fisik + replay WAL |
| Recovery | ke backup terakhir saja | **ke detik mana pun** |
| Contoh kasus | DB korup 14:37 → balik 03:00 (hilang ~11 jam) | balik ke **14:36** |
| Frekuensi | terjadwal | WAL **kontinu** + backup berkala |
| Beban | makin sering makin berat | streaming, ringan |

Menurut [dokumentasi resmi PostgreSQL](https://www.postgresql.org/docs/current/continuous-archiving.html), WAL tidak harus di-replay sampai habis — kita bisa berhenti di titik mana pun dan tetap dapat snapshot konsisten. Itu inti PITR-nya. Catatan penting dari dokumen yang sama: rangkaian WAL harus **kontinu**, tidak boleh ada lubang (kalau ada gap, recovery berhenti dan server menolak start).

## Alat: Databasus (Self-Hosted, Open Source)

Praktiknya kita pakai [Databasus](https://databasus.com/) — tool backup PostgreSQL self-hosted, lisensi Apache 2.0, UI web, support storage S3/R2/Google Drive/FTP dan notifikasi Slack/Discord/Telegram. Angkanya cukup meyakinkan: **8.670 GitHub stars** dan **2 juta docker pulls**, plus mereka klaim jadi tool backup pertama yang dibangun di atas protokol backup native PostgreSQL 17 (physical + incremental + WAL), bukan implementasi sendiri.

Yang membuat kami pilih: dia punya **restore verification** — backup yang "COMPLETED" belum tentu bisa di-restore, jadi Databasus yang lebih dulu mengetesnya. Log hijau tapi backup busuk itu penyakit klasik.

## Arsitektur Kami (Nyata, Bukan Teori)

```
mem0-dev-postgres-1 (PostgreSQL 17.11, db mem0_app)
        │  WAL stream (pg_receivewal)
        ▼
   databasus v3.60.0  ── port 4005 (bind Tailscale saja)
        │
        │ FULL harian + incremental tiap 3 jam + WAL kontinu
        ▼
   Cloudflare R2 → prefix backup/databasus/
```

Dua lapis, sengaja jalan bareng: dump kasar sebagai jaring pengaman, PITR untuk recovery presisi. Retensi dipilih **CHAINS_AND_FULL_BACKUPS, 7 chain** — bukan `TIME_PERIOD`. Alasannya ukuran penyimpanan jadi stabil (hapus chain ke-8, sisakan 7), dan tiap chain berdiri sendiri sehingga menghapus chain lama tidak merusak chain baru. Kalau pakai time period, disk tumbuh terus tanpa batas.

## 7 Jebakan yang Kami Kena

1. **Container jalan UTC.** Databasus tidak punya `TZ` → default UTC, padahal mau backup 04:00 WIB. Set `04:00` di API = 04:00 UTC = **11:00 WIB**. Rumusnya: `(jam_WIB - 7 + 24) % 24`. Verifikasi dengan `docker exec databasus date` vs `date` di host.
2. **`pg_hba` butuh baris `replication`.** Gejala menyesatkan: test koneksi balas `pg_hba_no_entry` padahal user/password benar. Sebabnya Databasus connect dari container lain, sementara PostgreSQL cuma mengizinkan replication dari localhost. Tambah `host replication all 172.16.0.0/12 scram-sha-256` + `host all all 172.16.0.0/12 scram-sha-256`, lalu reload.
3. **`summarize_wal=on` wajib** untuk incremental di PG 17. Kalau `off`, error-nya `wal_summary_disabled`. Set via `ALTER SYSTEM SET summarize_wal = on` + **reload, bukan restart**.
4. **Jangan simpan file backup di dalam `PGDATA`.** `pg_basebackup` memindai seluruh PGDATA; file milik user lain di situ bikin backup gagal dengan `Permission denied`. Simpan konfigurasi di luar PGDATA.
5. **Interval incremental cuma hourly/daily/weekly.** Tidak ada pilihan "tiap 3 jam" di UI/API — pakai **cron OS** yang memicu `{"type":"auto"}`.
6. **Field API berubah antar versi.** Di v3.60: `s3Storage.s3Bucket` (nested, bukan `s3Bucket` di root), `notifierType: "DISCORD"`, `channelWebhookUrl`. Dokumentasi resmi sering ketinggalan — cara cepat baca schema: ambil bundle UI (`curl -s http://127.0.0.1:4005/` → grep file `.js`), lalu grep nama field-nya di situ.
7. **`/system/*` = SPA fallback.** `/system/setup` dan `/system/status` balikin HTML, bukan JSON. Yang valid hanya `/system/version`.

## Verifikasi: Jangan Cuma Percaya Log

```bash
rclone ls r2-mem0:<bucket>/backup/databasus/
rclone size r2-mem0:<bucket>/backup/databasus/
```

Bukti stream hidup = nomor WAL di R2 **bertambah** antar jam (kami lihat `...0004` → `...0007`), dan ada pasangan FULL + INCR + file WAL `.zst` dengan `.metadata`-nya. Kalau tidak ada file WAL baru, stream sudah mati — walau UI masih bilang "healthy".

Kalau kamu masih pakai `pg_dump` doang tanpa WAL, sekarang waktu yang tepat menambah satu lapis PITR. Baca juga catatan kami soal [jebakan self-host mem0](/posts/self-host-mem0-jebakan/) dan [mem0 MCP vs Hindsight](/posts/mem0-mcp-vs-hindsight/) — dua-duanya masalah yang justru berakhir di backup seperti ini. Kamu pernah kena "backupnya ada tapi tidak bisa di-restore"? Ceritakan di komentar.

— Chokdi 🐷 · Content Studio · 2026
