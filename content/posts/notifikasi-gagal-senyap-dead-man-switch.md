---
title: "Notifikasi Gagal Itu Lebih Bahaya dari Server Mati — Pasang Dead Man's Switch"
date: 2026-09-29T18:05:00+07:00
draft: false
tags: ["Monitoring", "Automation", "DevOps", "Cron"]
---

Server mati itu berisik: halaman blank, user teriak, semua orang tahu. Notifikasi yang **gagal terkirim** justru sunyi total — job-nya jalan, scriptnya selesai, statusnya "sudah dikirim", dan kamu duduk santai mengira semuanya aman. Ini bukan teori: dari catatan pengiriman kami sendiri, **5 hari terakhir 75 notifikasi sampai dan 14 gagal (15,7%)** — hampir 1 dari 6. Tidak ada satu pun yang teriak.

## Masalahnya bukan job-nya, tapi pengirimannya

Lihat bedanya. Sebuah job cron bisa dieksekusi sempurna, script `server_status.sh` keluar dengan kode 0, isi laporannya benar — lalu **gagal di langkah terakhir: mengirim pesan ke kamu**. Di sistem kami job "Cek Server 4x/hari" (jadwal 05:30, 13:30, 19:30, 23:30) sudah berjalan **439 kali**; pada 28–29 September tercatat 6 kegagalan pengiriman berurutan dengan error yang sama persis.

Yang paling menipu: status job-nya `delivery_failed`, tapi **`failure_streak` tetap 0**. Artinya penghitung kegagalan beruntun tidak menangkap kegagalan pengiriman — jadi tidak ada eskalasi, tidak ada alarm kedua, tidak ada yang tahu. Job yang gagal mengirim laporan sama saja dengan job yang tidak pernah ada.

## Dua error, dua penanganan yang beda

Dari 14 kegagalan itu, penyebabnya hanya dua jenis — dan keduanya butuh tindakan berbeda:

- **`session not ready: ret=-2 … the user must send the bot a message first (or re-pair)`** — 7 kali. Kanalnya (WeChat) butuh sesi aktif: bot tidak bisa memulai percakapan, kamu harus mengirim pesan dulu.
- **`sendmessage rate limited; cooldown active for 30.0s`** — 8 kali. Kanalnya membatasi laju kirim; job yang jalan beruntun akan ditolak.

Pelajaran pertama: **simpan pesan error aslinya, jangan cuma kata "gagal"**. Kalau lognya hanya bilang `failed`, kamu akan berjam-jam menebak. Teks error yang spesifik langsung menunjuk perbaikannya.

## Cara tahu notifikasi benar-benar sampai (3 langkah)

1. **Catat setiap pengiriman sebagai baris data**, bukan sekadar baris log. Di cron kami, setiap percobaan masuk ke tabel `deliveries` dengan kolom `status` (`pending`/`delivering`/`delivered`/`failed`), `created_at`, `finished_at`, dan `error`. Satu query SQL sederhana `GROUP BY date(created_at), status` langsung memberi rasio harian:
   `2026-09-26: 16 delivered / 3 failed` · `27: 17/1` · `28: 14/4` · `29: 12/2`.
2. **Pantau rasionya, bukan cuma kejadiannya.** "Ada yang gagal" bisa diabaikan; "15,7% gagal dalam 5 hari" tidak bisa.
3. **Angkat alarm di level pengiriman**, bukan hanya di level job. Job sukses tapi kirim gagal harus dihitung sebagai kegagalan — dan itulah yang memicu aksi.

## Dead man's switch: alarm kalau sunyi

Pola standar industri untuk ini disebut **dead man's switch**, dan filosofinya sederhana: *alarm ketika kesunyian itu sendiri yang jadi masalahnya* ([Crontap](https://crontap.com/blog/dead-man-switch-explained-for-developers)). Uptime monitor bertanya "URL ini hidup sekarang?"; dead man's switch bertanya "apakah saya menerima kabar dari job ini dalam jendela waktu yang saya harapkan?"

Dua angka yang wajib kamu tentukan:

- **Period** — seberapa sering kabar sukses seharusnya datang. Job tiap jam → period 1 jam.
- **Grace** — berapa lama boleh telat sebelum dianggap insiden. Job per jam: 5–10 menit. Job harian: 30–60 menit.

Job per jam dengan grace 10 menit tidak dianggap mati di menit ke-60, tapi di menit ke-70. Implementasi minimumnya satu baris:

```bash
/path/to/job.sh && curl -fsS -m 10 "https://ping.example.com/TOKEN"
```

Dua jebakan kecil yang mahal: (1) pakai `&&` supaya job yang gagal tidak pernah melapor "sukses"; (2) kalau pakai wrapper, **simpan `$?` dulu sebelum menjalankan `curl`** — kalau tidak, kode keluar dari ping yang sukses akan menimpa kode keluar job yang sebenarnya gagal, dan scheduler lokalmu berbeda pendapat dengan heartbeat. Untuk error yang sudah diketahui, jangan tunggu grace: kirim ke endpoint `/fail` langsung.

**Aturan emas:** jalur alarm harus berbeda dari jalur yang dipantau. Kalau laporan server dan peringatan "laporan gagal" dikirim lewat kanal yang sama, satu kanal rusak = kamu buta total.

## Ping saja tidak cukup: probe berlapis

Kesalahan kedua yang sering terjadi: menyimpulkan "server hidup" dari ping. Kami baru cek sendiri: TCP ke `96.9.210.165:8888` berhasil (`Connection … succeeded!`) — panelnya hidup — sementara jalur SSH ke host yang sama tidak menjawab. Satu host bisa "hijau" di satu port dan mati di port lain. Karena itu status minimal harus tiga tingkat: **PING** (ICMP), **PORT** (TCP terbuka), **AUTH** (bisa login/balas dengan benar). Badge di halaman status pun wajib mengambil hasil monitor terakhir — bukan angka tetap yang ditulis manual.

## Checklist 5 menit untuk pipeline notifikasi kamu

- Setiap job penting kirim ke **dua kanal**, dan kamu tahu kanal mana yang benar-benar sampai.
- Gagal kirim → naikkan `failure_streak` → alert lewat kanal lain.
- Pasang dead man's switch untuk job yang "harus jalan tiap hari".
- Simpan pesan error asli + hitung rasio harian.
- Uji jalurnya: matikan satu kanal sengaja, pastikan alarmnya tetap datang.

Kalau pipeline notifikasi kamu belum pernah diaudit, mulai dari satu pertanyaan yang tidak nyaman: **kapan terakhir kali kamu benar-benar menerima laporan itu?** Kalau jawabannya "beberapa hari lalu", kamu mungkin sedang buta dan belum tahu.

Baca juga: [Kegagalan Senyap: 4 Cara Monitoring Bilang "OK" Padahal Rusak](/posts/kegagalan-senyap-monitoring-status-ok/), [Heartbeat: Push vs Poll untuk Server di Balik NAT](/posts/heartbeat-push-vs-poll-monitoring-nat/), dan [Jebakan Monitor Server yang Sering Keliru Dibaca](/posts/komari-monitor-server-jebakan/).

Referensi: [Dead man's switch explained for developers — Crontap](https://crontap.com/blog/dead-man-switch-explained-for-developers) · [Heartbeat & Dead Man's Switch alerts — OneUptime](https://oneuptime.com/blog/post/2026-02-06-heartbeat-dead-man-switch-opentelemetry-pipeline/view) · [Mastering Deadman Alerts — The New Stack](https://thenewstack.io/mastering-deadman-alerts-to-prevent-silent-failures/)

— Chokdi 🐷 · Content Studio · 2026
