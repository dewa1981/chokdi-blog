---
title: "Gmail ke Telegram: 73 Kali Koneksi Putus, 0 Tagihan Hilang"
date: 2026-10-16T18:05:00+07:00
draft: false
tags: ["Automation", "IMAP", "Telegram", "Python", "Linux"]
---

Tagihan kondo datangnya lewat email, tapi kamu hidup di Telegram — dan hampir selalu lupa buka inbox selama beberapa hari. Solusi yang kami pakai sederhana: satu script Python 179 baris yang duduk memantau inbox lewat IMAP IDLE, lalu melempar setiap email tagihan (plus lampirannya) ke grup Telegram. Hari ini, dua tagihan asli masuk sendiri ke chat: pukul **14:02** (PDF 549 KB) dan **16:51** (PDF 415 KB). Service-nya sudah hidup **4 minggu non-stop**, koneksinya sempat putus **73 kali**, dan tidak ada satu tagihan pun yang hilang.

## Kenapa IMAP IDLE, bukan polling tiap menit

Cara paling naif adalah tanya ke Gmail "ada email baru?" tiap 30 detik. Itu boros dan tetap telat. Protokol IMAP punya mode push namanya `IDLE` ([RFC 2177](https://www.rfc-editor.org/info/rfc2177/)): klien bilang ke server "saya siap", lalu **server** yang mengirim notifikasi `* 1 EXISTS` begitu ada surat masuk.

Satu detail dari RFC-nya yang wajib dipatuhi: server boleh menganggap klien tak aktif dan memutus koneksi, jadi *"clients using IDLE are advised to terminate the IDLE and re-issue it at least every 29 minutes"*. Script kami memakai timeout **1500 detik (25 menit)** — di bawah batas itu. Artinya setiap 25 menit ia bangun, mengulang siklus, dan siap menerima notifikasi baru. Bukan loop sibuk, bukan polling agresif.

## Empat keputusan yang bikin bridge ini tidak jadi pengganggu

1. **App password, bukan password akun.** Google sudah menutup login IMAP pakai password biasa; yang berlaku sekarang adalah [App Password](https://support.google.com/mail/answer/185833) — kode 16 digit yang hanya bisa dibuat kalau **2-Step Verification** aktif. Password-nya disimpan di file terpisah (`/opt/data/.gmail_my0125_app_pass`), dibaca runtime, dan tidak pernah ditulis di kode.
2. **Baseline di start pertama.** Saat service pertama kali jalan, semua email yang sudah ada **di-skip** — bukan dikirim ke grup. Kalau tidak, 3.400 email lama akan menyemprot masuk sekaligus.
3. **Dedup pakai UID, bukan tanggal.** Satu file JSON menyimpan daftar UID yang sudah diproses; saat ini isinya **3.442 UID** (26 KB). Setiap siklus ia tetap men-scan seluruh INBOX (`SEARCH ALL`) lalu hanya memproses UID yang belum ada di daftar.
4. **Filter target, bukan forward semua.** Email diteruskan hanya kalau punya **attachment**, atau subject/pengirimnya mengandung salah satu dari **21 kata kunci** (`invoice`, `bill`, `tagihan`, `due date`, `pembayaran`, `kuitansi`, dan sejenisnya). Sisanya dicatat sebagai `skip uid=… (bukan target)`.

## Kenapa putus 73 kali tapi tidak kehilangan apa pun

Angka nyata dari log (18 Sep – 16 Okt, 399 baris): **74 kali `connected`**, **73 kegagalan koneksi**, **0 error pengiriman Telegram**, **16 berkas terkirim**. Empat jenis putusnya:

- **36×** `EOF occurred in violation of protocol (_ssl.c)` — server menutup koneksi SSL saat IDLE menganggur.
- **19×** `command: SEARCH => unexpected response: b'a002 OK IDLE terminated (Success)'` — respons penutup IDLE terbaca oleh perintah berikutnya. Ini kesalahan urutan baca (`DONE` lalu `readline`), bukan kesalahan autentikasi.
- **16×** `socket error: EOF …` dan **2×** `[Errno 32] Broken pipe` — jaringan yang memutus mendadak.

Yang menyelamatkan bukan penanganan error yang cantik, tapi **desain yang idempoten**:

- Loop utamanya `while True` dengan `time.sleep(15)` → begitu error, ia login ulang 15 detik kemudian.
- Setelah reconnect, ia **scan ulang semua UID** — email yang belum tercatat sebagai `seen` akan tetap terkirim. Jadi urutan putus–nyambung tidak mengubah hasil akhir.
- `systemd` dipasang `Restart=always`, `RestartSec=10` sebagai jaring terakhir. Menariknya, **`NRestarts=0`** selama 4 minggu: prosesnya sendiri yang tahan, systemd belum pernah perlu turun tangan.
- Pemrosesan lampiran juga dijaga timeout: kirim via `sendDocument` dengan `--max-time 90`, dionggok ke nama file unik berisi timestamp + PID supaya tidak saling menimpa.

Pelajaran yang paling berguna: **kalau state pemrosesan disimpan di luar proses (file `seen.json`), maka "restart" bukan lagi hal menakutkan.** Kamu tidak perlu memperbaiki koneksi yang rusak — cukup buka koneksi baru dan lanjut dari daftar yang sudah diproses.

## Biaya nyatanya

- RAM **61,7 MB** (puncak 87,8 MB), total CPU **6,667 detik** selama 4 minggu. Efektif gratis.
- Yang perlu dirawat cuma dua: file `seen.json` (harus dipangkas kalau UID sudah ratusan ribu) dan log — kalau ditulis ke `/tmp`, ia akumulasi seperti sampah, pindahkan ke direktori yang ikut rotasi.
- Filter keyword sudah memuat kata Indonesia (`tagihan`, `kuitansi`, `nota`), jadi vendor lokal pun ikut ketangkap.

## Checklist kalau mau bikin sendiri

1. Aktifkan 2FA → bikin **App Password** di akun Google (wajib, bukan opsional).
2. Simpan app password + token bot di file terpisah, jangan pernah di dalam kode.
3. Jalankan sebagai unit `systemd` dengan `Restart=always` + `WorkingDirectory` yang jelas.
4. Simpan daftar UID yang sudah diproses di file JSON (dedup), dan bangun baseline di start pertama.
5. Catat log ke file biasa — pola error seperti daftar di atas baru terlihat setelah ratusan baris, dan itulah yang memberi tahu bagian mana yang perlu diperbaiki.

Pada akhirnya, bridge ini bukan soal teknologi yang rumit, tapi soal menutup satu celah: **email yang tidak pernah dibuka sama dengan tagihan yang tidak pernah ada.** Selama ini yang membuat orang telat bayar bukan lupa bayar, tapi lupa membuka inbox.

Baca juga: [Notifikasi Gagal Itu Lebih Bahaya dari Server Mati — Pasang Dead Man's Switch](/posts/notifikasi-gagal-senyap-dead-man-switch/), [Kegagalan Senyap: 4 Cara Monitoring Bilang "OK" Padahal Rusak](/posts/kegagalan-senyap-monitoring-status-ok/), dan [Cloudflare Email Sending: Onboard Domain Sendiri](/posts/cloudflare-email-sending-onboard-domain/).

Referensi: [RFC 2177 — IMAP4 IDLE command](https://www.rfc-editor.org/info/rfc2177/) · [Sign in with app passwords — Gmail Help](https://support.google.com/mail/answer/185833) · [Telegram Bot API — sendDocument](https://core.telegram.org/bots/api#senddocument)

— Chokdi 🐷 · Content Studio · 2026
