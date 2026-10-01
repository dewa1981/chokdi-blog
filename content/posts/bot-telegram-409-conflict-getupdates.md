---
title: "Bot Telegram Diam Setelah Update: 3 Penyebab 409 \"Conflict\""
date: 2026-10-01T17:20:00+07:00
draft: false
tags: ["Telegram", "Hermes Agent", "Bot", "Troubleshooting"]
---

Bot Telegram yang tadinya jawab cepat tiba-tiba diam. Log gateway cuma menampilkan satu baris yang bikin panik: `Conflict: terminated by other getUpdates request`. Kelihatannya seperti token rusak atau server tumbang, padahal artinya jauh lebih sederhana — **ada lebih dari satu proses yang menarik pesan dari bot token yang sama**.

Telegram memang hanya mengizinkan **satu** long-poll `getUpdates` memegang "sewa" per bot token. Begitu ada pemanggil kedua, Telegram memutus salah satunya dan melempar HTTP 409.

Saya kena persis kasus ini saat menyiapkan dua agent baru di server `docker-hermes` pada 30 September 2026. Total waktu yang dipakai untuk menebak penyebabnya jauh lebih lama daripada waktu memperbaikinya.

## 🧭 Kenapa Telegram Cuma Boleh Satu Poller

Model kerja long polling itu sederhana: bot membuka satu koneksi menggantung ke `api.telegram.org`, lalu Telegram mengirim update lewat koneksi itu. Kalau ada dua koneksi yang menahan antrean yang sama, update bisa dikirim dua kali — jadi Telegram memilih satu pemilik dan memutus yang lain dengan status **409**.

Yang penting dipahami: **409 bukan error jaringan, bukan kuota, bukan masalah koneksi server**. Artinya selalu sama — ada pesaing.

## 🔍 Tiga Penyebab, Tiga Tanda

| Penyebab | Tanda khas | Penanganan |
|---|---|---|
| Tumpang-tindih restart | 409 muncul beruntun tepat setelah restart, lalu log diam | Berhenti restart, tunggu 10 menit |
| Poller kedua yang nyata | 409 terus muncul tanpa aktivitas restart | Cari & matikan duplikatnya |
| Loop internal satu instance | 409 datang rapi tiap ~30 detik, proses cuma satu | Bug runtime — cek versi build |

Cara memastikan penyebabnya cuma satu perintah, dan **jangan** pakai `getUpdates` untuk tes. Panggilan itu justru ikut menarik sewa long-poll dan menendang gateway yang sedang jalan — jadi 409 yang Anda cari malah Anda buat sendiri.

Pakai dua panggilan read-only ini:

```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getMe"
curl -s "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
```

- `getMe` → kalau bot-nya balas dengan nama yang benar, token Anda **sehat**. Berhenti menuduh token.
- `getWebhookInfo` → kalau `url` kosong, tidak ada webhook yang mengganggu. Kalau terisi, webhook itulah yang memblokir polling.

Saya jalankan keduanya di instance produksi: `url` kosong dan `pending_update_count: 0`. Artinya tidak ada webhook nyangkut dan tidak ada pesan menumpuk — dua penyebab paling sering langsung tersingkir dalam satu menit.

## 🥇 Penyebab Nomor Satu: Restart Beruntun

Ini yang paling sering terjadi dan paling tidak berbahaya. Sewa long-poll butuh beberapa detik untuk dilepas setelah proses lama dimatikan. Kalau antrean restart terjadi lebih cepat dari itu — misalnya deploy lalu langsung di-restart lagi — dua poller sempat hidup bersamaan.

Gejalanya khas: log Anda menampilkan **satu burst 409** tepat setelah restart, lalu semuanya kembali normal. Kalau log sudah bersih sekitar 10 menit, berarti sudah sembuh sendiri. Jangan buang waktu mengejar duplikat yang tidak ada.

Satu aturan sederhana yang menyelamatkan: beri jeda **sekitar satu menit antar restart** pada bot yang terhubung ke Telegram.

## 🥈 Penyebab Nomor Dua: Salinan Kedua yang Lupa Dimatikan

Ini yang paling sering saya temui di lapangan, dan bentuknya beragam:

- container staging yang masih jalan memakai token yang sama
- proses lama yang belum benar-benar mati setelah crash
- script tes yang Anda jalankan di laptop "cuma buat lihat apakah bot hidup"

Semuanya mengarah ke satu pengecekan:

```bash
ss -tp | grep api.telegram.org
```

Kalau muncul dua proses, itu bukti langsung. Berhenti satu, dan biarkan satu instance polling sendirian.

## 🥉 Penyebab Nomor Tiga: Dua Koneksi dari Satu Proses

Ini yang paling licin: hanya ada satu proses, tapi polanya 409 datang rapi setiap ~30 detik. Artinya runtime Anda membuka dua koneksi ke `api.telegram.org` di dalam proses yang sama — biasanya karena transport yang dipakai bersama tidak di-cache, sehingga probe kesehatan dan poller memakai koneksi berbeda.

Jangan dikira ini cuma masalah satu framework. Keluhan serupa tercatat di issue OpenClaw (#50064, #58951, dilaporkan Maret 2026) dan juga di repo Hermes Agent (#2296) yang melaporkan 409 tunggal membuat polling Telegram berhenti tanpa pemulihan. Kalau Anda memakai **Hermes Agent**, ini alasan kuat untuk tidak tertinggal di versi lama — rilis stabil terakhir **v0.21.5 (v2026.9.24)** memuat ratusan PR perbaikan di jalur panas gateway dan penanganan pesan.

## ✅ Checklist 5 Menit

1. `getWebhookInfo` — pastikan `url` kosong.
2. `ss -tp | grep api.telegram.org` — pastikan cuma satu proses.
3. Cek container staging/zombie yang memakai token yang sama.
4. Sudah restart beruntun? Tunggu 10 menit sebelum menebak lebih jauh.
5. Masih berulang di ~30 detik dengan satu proses? Naikkan versi runtime.

## 🔑 Pelajaran yang Saya Anggap Wajib

Diagnosa 409 itu urusannya **"siapa lagi yang menarik pesan"**, bukan **"kenapa servernya rusak"**. Begitu pertanyaannya digeser, solusinya jadi jelas dan cepat. Yang paling sering saya lihat: orang langsung rotate token, padahal tokennya tidak pernah jadi masalah.

Satu lagi — jangan pernah pakai `getUpdates` untuk tes. Itu tindakan yang membuat Anda mengejar bayangan sendiri.

## 📚 Bacaan Terkait

- [5 Penyebab Website Down](/posts/5-penyebab-website-down/) — urutan diagnosa dari luar ke dalam.
- [Tailscale Webhook Alarm ke Telegram](/posts/tailscale-webhook-alarm-telegram/) — pola notifikasi tanpa polling.
- [2 Bulan, 13 Rilis Hermes Agent](/posts/2-bulan-13-rilis-hermes-agent/) — catatan ritme rilis versi.

Pernah kena bot yang diam padahal server terlihat sehat? Coba cek `ss -tp` dulu, lalu tulis temuan Anda di kolom komentar.

— Chokdi 🐷 · Content Studio · 2026
