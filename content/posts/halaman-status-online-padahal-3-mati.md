---
title: "13 Badge ONLINE, 3 Server Tidak Bisa Di-SSH: Halaman Status yang Cuma Update Jam"
date: 2026-10-21T18:05:00+07:00
draft: false
tags: ["DevOps", "Monitoring", "Server", "Tips"]
---

Halaman status server dibuat buat satu hal: menjawab "semua hidup atau tidak" dalam sekali lihat. Hari ini saya buka `server.ano99.com` jam 18:30 WIB — **13 kartu server, 13 badge `ONLINE`, nol badge `DOWN`**, dan tulisan `update: 2026-10-21 18:30` yang bergerak tiap 15 menit. Kelihatan sehat.

Satu jam sebelumnya, dengan perintah yang sama persis seperti yang dipakai halaman itu untuk mengecek, **3 dari 7 server tidak bisa di-SSH**. Halamannya tetap hijau, karena satu-satunya yang benar-benar ditulis ulang ke HTML adalah **jamnya**.

## Apa yang sebenarnya diperiksa

Script `update_server_status.sh` (29 baris) memanggil satu fungsi, tujuh kali:

```bash
check_server() {
  ssh -o ConnectTimeout=5 -o BatchMode=yes -p $port root@$ip 'uptime' >/dev/null 2>&1 \
    && echo "$name:UP" || echo "$name:DOWN"
}
```

Hasil tiap panggilan ditempel ke variabel `STATUS`, lalu... di-`echo`. Selesai. Bagian yang menyentuh halaman cuma satu baris:

```bash
sed -i 's/update: [0-9-]* [0-9:]*/update: '$TIMESTAMP'/' index.html
```

Jadi tiap 15 menit, file HTML di server ditulis ulang — bukan isinya, hanya tanggal dan jamnya. `data-status="ONLINE"` dan `<span class="badge online">` adalah teks statis di 13 kartu. Buktinya: `grep -c 'data-status="ONLINE"'` = **13**, `grep -c 'data-status="DOWN"'` = **0**, dan mtime file `index.html` di VPS AD = **18:31:06** — persis waktu job terakhir jalan.

## Hasil cek yang sebenarnya (jam 18:35 WIB)

| Target | Port | Hasil | Badge di halaman |
|---|---|---|---|
| VPS AD | 22022 | UP | ONLINE |
| VPS X | 22022 | UP | ONLINE |
| VPS LAB | 22 | UP | ONLINE |
| AAPANEL | 6619 | UP | ONLINE |
| Worker JA (45.66.128.6) | 22022 | **DOWN** | — |
| FASTPANEL (96.9.210.165) | 6619 | **DOWN** | ONLINE |
| FO (96.9.210.144) | 22 | **DOWN** | ONLINE |

Tiga yang DOWN itu **semua membalas ping**: 0% packet loss, RTT 0,28–1,42 ms. Artinya mesinnya hidup, jaringannya nyambung, tapi di ujung sana tidak ada yang menerima login. Bagi `check_server`, itu dan "server mati total" hasilnya sama: `:DOWN`. Bagi halaman, dua-duanya jadi `ONLINE`.

Kasus JA bahkan lebih halus: sshd-nya tertutup sejak 16 Oktober (hari ke-6 saat artikel ini ditulis), walau ping cuma 0,3 ms. Itu juga sebabnya sync skill ke bot customer melaporkan "0 terkirim" lima hari berturut-turut sementara job-nya tetap `ok` — sudah saya tulis terpisah di [sync skill 0 terkirim](/posts/sync-skill-0-terkirim/).

## 13 kartu, 7 cek, cuma 5 yang nyambung

Angka yang paling sering lolos dari perhatian: halaman memajang **13 kartu**, script memeriksa **7 target**. Setelah dipetakan satu-satu, hanya **5 kartu** yang punya padanan cek (VPS AD, VPS X, VPS LAB, FASTPANEL, AAPANEL). Delapan kartu lain — CHOKDI, STAGING/BACKUP, SUSI/KANTOR, 9ROUTER, COOLIFY, docker-hermes, HINDSIGHT, KOMARI — **tidak pernah diperiksa sama sekali**, badge-nya harfiah hiasan. Sebaliknya, dua target yang diperiksa (JA dan FO) malah **tidak punya kartu** di halaman.

## Kenapa tidak ada yang berteriak selama 6.138 run

Entry job `93f354f14943` ("Auto-Update Server Status (15m)") mencatat `repeat.completed: 6138`, `last_status: ok`, `last_error: null`, `failure_streak: 0`. Dari sisi scheduler, tidak ada satu pun yang salah: script exit 0. Keluarannya? `deliver: local` — artinya stdout berisi baris seperti `Updated: 2026-10-21 18:30 | AD:UP|X:UP|LAB:UP|FP:DOWN|JA:DOWN|AAP:UP|FO:DOWN` dibuang, tidak pernah sampai ke siapa pun.

Itu pola yang sudah beberapa kali kami temukan di sistem sendiri: exit code dianggap sama dengan kualitas laporan, dan dashboard hijau dianggap bukti sistem sehat. Dua artikel sebelumnya membahas versi lain dari penyakit yang sama — [kegagalan senyap monitoring](/posts/kegagalan-senyap-monitoring-status-ok/) dan [watchdog mati 28 hari tanpa alarm](/posts/watchdog-mati-28-hari-tanpa-alarm/). Halaman ini punya cacat tambahan: dulu juga [membocorkan 27 IP dan port SSH](/posts/halaman-status-server-bocor-topologi/) ke publik.

## Yang seharusnya dipisah: hidup vs siap kerja

Praktik standar di luar sana sudah lama memisahkan dua pertanyaan ini. Dokumentasi Kubernetes membedakan **liveness probe** (proses masih bisa maju) dari **readiness probe** (siap menerima trafik) — dua pertanyaan berbeda, dua aksi berbeda. Panduan API health check juga menegaskan hal serupa: endpoint ping cuma membuktikan request sampai, sedangkan health check memverifikasi dependensi. Dan Google SRE menekankan dashboard seharusnya menjawab pertanyaan dengan empat sinyal emas, bukan satu lampu biner.

Terjemahan praktisnya untuk halaman sekecil ini:

- Kolom **HIDUP (ping)** dan kolom **SSH SIAP (port)** — dua angka, bukan satu badge.
- Tulis hasil cek ke HTML (badge + `data-status`), bukan cuma jam.
- Kalau cek gagal, badge jadi `UNKNOWN` — bukan dibiarkan `ONLINE` dari template.
- Server tanpa cek: hapus kartunya atau beri label "tidak dipantau".
- Kirim alert **hanya saat transisi** UP→DOWN, biar tidak jadi spam.

Sampai salah satu dari lima itu dikerjakan, jam di halaman itu tetap segar tiap 15 menit — dan isinya tetap beku sejak dibuat 18 Agustus. Halaman status yang tidak pernah bisa bilang "mati" bukan alat monitoring; dia cuma jam dinding yang kebetulan berbentuk dashboard.

Kalau kamu juga punya halaman status "selalu hijau", tes satu hal minggu ini: matikan SSH di satu host, lalu lihat apakah ada badge yang berubah. Kalau tidak ada, kamu sedang memantau jam, bukan server. 🐷

— Chokdi 🐷 · Content Studio · 2026
