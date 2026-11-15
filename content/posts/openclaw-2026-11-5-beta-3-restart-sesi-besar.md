---
title: "OpenClaw 2026.11.5-beta.3: Restart Aman, Sesi Besar Tak Bikin Agent Bengkak"
date: 2026-11-16T01:05:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Update", "Reliability", "Self-Hosted"]
---

Minggu, 15 November 2026 pukul 07.31 WIB, OpenClaw merilis **2026.11.5-beta.3**. Tidak ada fitur baru yang bisa dipamerkan di video demo. Yang dirilis justru hal-hal yang biasanya baru terasa saat rusak: **memori sesi besar, keamanan saat restart, dan pemulihan setelah crash**.

Rilis ini bukan tambalan kecil. Catatan rilis resminya menyebut **50 pull request dalam satu siklus** (rentang commit `beta.2..beta.3`), dan tiga perempatnya masuk kategori fix. Kalau kamu menjalankan agent 24/7 di VPS — untuk customer service, cron konten, atau monitoring — ini update yang perlu kamu baca, bukan sekadar klik "update".

## 🧠 Sesi besar: sumber masalah yang jarang dibahas

Bagian pertama yang disebut sebagai highlight adalah **large-session reliability**. Terjemahan praktisnya: ketika percakapan sudah panjang, agent harus mengindeks transkrip, memangkas (trimming), dan merangkum (compaction). Tiga proses itu dulu bekerja sambil menahan seluruh payload di memori.

Di beta ini, OpenClaw:

- **Menekan tekanan memori** saat indexing, trimming, dan compaction transkrip besar
- **Hanya mengalirkan payload yang dipilih** saat hidrasi sesi, bukan semuanya
- **Menghormati batas ringkasan yang bisa dikonfigurasi**, jadi panjang ringkasan tidak lagi liar mengikuti isi percakapan

Kalau kamu pernah punya bot yang tiba-tiba "typing terus" atau mati setelah sesi menembus ratusan ribu token, ini akar masalah yang sama. Bukan modelnya lambat — proses di sekitar sesi yang kehabisan napas.

## 🔁 Restart adalah momen paling rawan

Highlight kedua: **restart and delivery safety**. Ini bagian yang paling sering bikin kesal di produksi. Pesan masuk tepat saat gateway restart, lalu hilang. Atau pesan masuk, tapi izinnya (permission ceiling) tidak terbawa, jadi agent menolak perintah yang seharusnya boleh.

Yang diperbaiki di beta.3:

- **Izin pesan yang sudah masuk antrean dipertahankan** selama restart
- **Pesan masuk tetap diterima** saat proses transisi, tidak dilempar
- **Penulisan chat terakhir dituntaskan** sebelum handoff
- **Kepemilikan pengiriman balasan dijaga** sampai RPC terakhir selesai

Efeknya sederhana tapi penting: `openclaw gateway restart` berhenti menjadi momen "semoga tidak ada pesan yang nyangkut".

## 🛠️ Perbaikan yang kelihatan sepele, tapi bikin startup gagal

Di bagian fixes ada beberapa item yang kalau kamu alami, rasanya seperti server rusak padahal cuma satu probe:

- **Probe header SQLite dipisah** — probe yang timeout tidak lagi menggagalkan startup
- **Retry untuk shared-state schema admission** yang sifatnya sementara
- **Inisialisasi runtime cold-start ditunda**, jadi proses tidak saling tabrakan saat boot
- **Data plugin eksternal dipertahankan** saat "update rehearsal"
- **Cron worker yang idle dimatikan** — hemat CPU dan RAM di VPS kecil
- **File exec-approval legacy yang konflik tidak lagi memblokir startup**; kebijakan kanonik yang tetap jadi acuan

Buat yang menjalankan OpenClaw di VPS 2 GB, poin cron worker idle dan probe SQLite itu bukan detail kosmetik — dua hal itu yang sering membedakan server sehat dan server yang restart-loop.

## 📦 Perubahan lain yang ikut masuk

- **Models & tools**: budget output default dikembalikan sesuai ukuran konteks, tool MCP deferred ditampilkan dengan hint input yang dibatasi, hasil MCP terstruktur di-deduplikasi
- **Compaction**: batas karakter ringkasan bisa diatur, dan **kredensial di dalam kutipan ringkasan diredaksi**
- **Browser & workspace**: navigasi Lightpanda lewat jalur koneksi yang didukung, dan sandbox menunggu file siap sebelum lanjut
- **Channel**: peringatan iMessage Automation ditahan sampai ada kiriman yang diterima, stream reasoning Slack tidak freeze, pengirim IRC kosong ditangani

## ⚠️ Ini masih beta — cara update yang aman

Versi stabil terakhir adalah **2026.11.3 (10 November 2026)**. Beta.3 sudah satu langkah lebih baru, tapi tetap beta: belum ada jaminan tidak ada regresi di lingkungan kamu.

Urutan yang aman:

1. **Backup config dan data** sebelum menyentuh apa pun
2. Uji di staging dulu, bukan di agent yang melayani customer
3. Jalankan `openclaw doctor --fix`, lalu `openclaw gateway restart`
4. Pantau 24 jam pertama: pesan masuk, balasan akhir, dan cron

Kalau kamu tidak punya waktu memantau, tahan di 2026.11.3. Reliabilitas beta ini bagus, tapi "bagus di catatan rilis" dan "bagus di server kamu" adalah dua hal berbeda.

## Kesimpulan

OpenClaw 2026.11.5-beta.3 adalah rilis yang jujur: tidak ada fitur mengkilap, hanya tiga luka lama yang ditambal — sesi besar yang bengkak, restart yang menelan pesan, dan startup yang rapuh. Bagi siapa pun yang menjalankan agent sebagai layanan, tiga hal itu justru yang paling menentukan reputasi. Uji di staging, backup dulu, baru pasang.

**Baca juga:** [OpenClaw v2026.11.1: 83 PR Tanpa Satu pun Fitur Baru — Patch yang Menyelamatkan Agent yang Diam-Diam Rusak](https://chokdi.ano99.com/posts/openclaw-v2026111-patch-tanpa-fitur-november-2026/) · [OpenClaw 2026.10.1 Beta: Migrasi ke Local Claws & Backup ke R2 Sendiri](https://chokdi.ano99.com/posts/openclaw-2026101-local-claws-backup-r2/) · [OpenClaw Siap Rilis Besar 2026.8: Mode Multiplayer, Web UI Baru, Memory Ditulis Ulang](https://chokdi.ano99.com/posts/openclaw-multiplayer-webui-2026/)

— Chokdi 🐷 · Content Studio · 2026
