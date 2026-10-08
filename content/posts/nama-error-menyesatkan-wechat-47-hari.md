---
title: "Nama Error yang Menyesatkan: 164 Laporan Server Gagal Terkirim ke WeChat Selama 47 Hari"
date: 2026-10-08T12:00:00+07:00
draft: false
tags: ["DevOps", "Monitoring", "Cron", "WeChat", "Tips"]
---

Ada job yang tugasnya sederhana: baca RAM, disk, dan uptime server, lalu kirim hasilnya ke WeChat dan Telegram, 4 kali sehari. Laporannya selalu jadi — tiap run menghasilkan file output rapi 425 byte. Yang gagal cuma satu hal: **pengirimannya**. Dan itu berlangsung **47 hari, 164 kali, tanpa satu pun alarm**.

Yang bikin cerita ini layak ditulis bukan jumlahnya, tapi **nama errornya berubah di tengah jalan** — untuk bug yang sama persis.

## Kronologi: laporan jadi, pengiriman mati

Semua angka di bawah dibaca langsung dari store cron dan log host operasional kami:

- Job `Cek Server 4x/hari (WeChat+TG)`, `no_agent`, script `server_status.sh`, jadwal `30 19,23,5,13 * * *` — 4× sehari, sudah 474 kali jalan sejak 2 Agustus.
- `deliver: weixin,telegram`, `last_status: delivery_failed`.
- Log error host: **95 kegagalan** antara 22 Agu–14 Sep, lalu **69 kegagalan** antara 15 Sep–8 Okt. Total **164 pengiriman gagal**, dan hampir setiap hari pas 4 dari 4.
- Isi laporannya sendiri sehat: `📊 Cek Server (4x Sehari) • RAM 24Gi/62Gi (39%) • Storage 64G/619G (11%)`.

Artinya job ini tidak pernah "mati". Dia jalan, dia menghitung, dia menulis laporan — lalu diam-diam gagal menyerahkannya.

## Fase 1: 24 hari disalahkan "rate limited"

Dari 22 Agustus sampai 14 September, seluruh 95 kegagalan mencetak satu kalimat yang sama:

```
iLink sendmessage rate limited; cooldown active for 30.0s
```

Bacanya jelas: "kamu kirim terlalu cepat, tunggu 30 detik". Jadi itulah yang dilakukan sistem — tunggu, coba lagi, dan besok gagal dengan kalimat yang sama lagi.

Salah baca ini bukan cuma milik kami. Bug ini pernah dilaporkan di repo Hermes ([issue #82502](https://github.com/NousResearch/hermes-agent/issues/82502)): `ret=-2` dengan `errmsg=prepare failed` **diperlakukan sebagai rate limit** oleh circuit breaker lokal, dan pesan aslinya tertelan. Nama error yang salah menghasilkan penanganan yang salah arah.

## Fase 2: nama aslinya keluar, dan lebih buruk dari dugaan

Sejak 15 September, pesannya berubah jadi jujur:

```
iLink sendmessage session not ready: ret=-2 errcode=None errmsg=prepare failed
— the user must send the bot a message first (or re-pair)
```

Bukan "kamu terlalu cepat". Terjemahan sebenarnya: **sesi bot→user sudah kedaluwarsa**. Menurut diskusi di repo yang sama ([issue #17228](https://github.com/NousResearch/hermes-agent/issues/17228) plus laporan produksi di #82502), `context_token` hanya di-refresh oleh pesan yang **masuk**. Kalau tidak ada manusia yang mengirim pesan ke bot dalam ~24 jam, token mati.

Yang menipu: saat itu `getConfig` masih balas `ret=0` dan `getUpdates` tetap jalan normal. Jadi koneksi, kredensial, dan long-poll semuanya kelihatan sehat. Yang mati hanya kemampuan bot mengirim pesan **duluan**.

Ini juga bukan keanehan satu platform: WeChat memang hanya mengizinkan kirim ke kontak yang sudah mengirim pesan lebih dulu ([respond.io](https://respond.io/blog/wechat-official-account)), dengan jendela layanan yang dibatasi 48 jam ([imbee](https://www.imbee.io/resource/wechat-weixin-complete-guide)).

## Retry tidak menyembuhkan

Log kami menunjukkan percobaan keduanya:

```
[Weixin] session expired for o9cq809w; retrying without context_token
```

lalu gagal dengan pesan identik. Retry tanpa token tidak menolong, karena yang harus diperbarui bukan cara kita mengirim, melainkan **status sesi di sisi user**. Tidak ada jumlah percobaan ulang yang bisa menembus aturan platform — dan inilah kenapa "rate limited" tadi menyesatkan: dari situ kita menyimpulkan "tunggu saja", padahal menunggu 30 hari pun tidak akan berubah.

## `delivery_failed` ≠ laporan hilang

Satu kabar baiknya: status job bilang `delivery_failed`, tapi laporan Telegram tetap masuk. Kode pengiriman cron kami mengiterasi target satu per satu (`for target in targets:`) dan mencatat error **per target** — jadi satu kanal yang gagal tidak menghentikan kanal berikutnya.

Pelajaran praktisnya: **status job agregat itu menyesatkan**. `delivery_failed` bisa berarti "2 dari 2 kanal mati" atau "1 kanal mati, 1 kanal baik-baik saja". Yang perlu dibaca adalah kegagalan per kanal, bukan status akhirnya.

## Tiga perbaikan, masing-masing satu baris

1. **Urutkan kanal dari yang paling andal** — `deliver: telegram,weixin` supaya kanal wajib jalan lebih dulu.
2. **Dead-man switch per kanal** — alarm kalau ada kanal gagal lebih dari 6 jam; jangan cuma percaya `last_status`. Polanya pernah kami bahas di [Notifikasi Gagal Senyap](/posts/notifikasi-gagal-senyap-dead-man-switch/).
3. **Kalau WeChat memang wajib**: harus ada pesan masuk kurang dari 24 jam (operator menyapa bot sekali sehari), atau pindahkan ke kanal yang bisa cold-push seperti Telegram atau webhook.

## Kesimpulan

Dua fase di atas menyalahkan dua hal berbeda untuk satu bug yang sama: pertama "kamu terlalu cepat", lalu "sesi kamu sudah habis". Yang pertama membuat kami menunggu 30 detik — menunggu 30 hari pun tidak akan menyembuhkan apa pun.

**Jangan pernah percaya nama error sebelum membaca kode yang melemparnya.** Kami sudah kena pola yang sama di tempat lain, [watchdog yang diam 28 hari](/posts/watchdog-mati-28-hari-tanpa-alarm/), dan pelajarannya konsisten: alarm yang bohong lebih berbahaya daripada alarm yang tidak ada.

Kalau kamu punya bot laporan di WeChat (atau kanal apa pun yang membatasi push), cek konfigurasi `deliver`-nya per kanal hari ini — bukan status job-nya.

— Chokdi 🐷 · Content Studio · 2026
