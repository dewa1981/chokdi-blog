---
title: "OpenClaw 2026.9.4: Ubah Obrolan Lama Jadi Skill, Cari Plugin & Skill dalam Satu Kotak"
date: 2026-09-17T01:21:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Tutorial", "Self-Host", "Update"]
---

OpenClaw baru saja merilis versi **2026.9.4** pada 11 September 2026 — dan ini bukan rilis kecil. Ada **1.558 pull request** plus 20 commit langsung dari **294 kontributor** di dalamnya. Tiga hal yang paling terasa buat kamu yang menjalankan agent sendiri di VPS: skill sekarang bisa lahir dari obrolan lama, plugin dan skill dicari dari satu tempat, dan cloud session jauh lebih bisa dikendalikan.

Kalau kamu self-host agent AI (OpenClaw, Hermes, atau sejenisnya), rilis ini layak kamu pasang — bukan karena fitur mahal, tapi karena kerjanya jadi lebih hemat waktu.

## 🧠 Fitur Utama: Belajar dari Obrolan Lama

Ini yang paling menarik. Di changelog resmi OpenClaw menulis: *"lets you turn past conversations into reusable skills through a chat you can steer"* — obrolan lama kamu bisa **disulap jadi skill yang bisa dipakai ulang**, dan prosesnya lewat chat yang bisa kamu setir (steer).

Kenapa ini penting? Selama ini masalah terbesar agent AI bukan "tidak bisa", tapi **lupa**. Kamu mengajari sesuatu lewat percakapan panjang hari Senin, minggu depan harus ngulang dari nol. Sekarang pola yang sudah pernah berhasil bisa dikunci jadi skill.

Implementasinya di PR #142909 ("Learn from past conversations in a steerable chat"). Halaman Skills juga berubah: **pencarian kini menyatu** antara skill yang sudah terpasang dan katalog ClawHub. Card-nya menunjukkan mana yang siap dipakai dan mana yang masih butuh setup, plus ganti agent langsung menampilkan skill milik agent itu saja.

### Tips praktis bagi pemula

- Sebelum mulai, pastikan sudah ada beberapa percakapan berkualitas. Skill lahir dari pola — bukan dari satu percakapan sekali lewat.
- Pakai mode steer: perbaiki arah di tengah proses, jangan tunggu selesai baru bilang "salah".
- Verifikasi skill hasilnya sebelum dipakai serius di produksi. Skill yang salah itu lebih berbahaya daripada tidak punya skill, karena dijalankan otomatis.

## 🔍 Plugin & Skill Kini dalam Satu Kotak

Browsing plugin di web UI sekarang menampilkan **bundled plugin dan ClawHub** secara terpadu (PR #138755), lengkap dengan filter dan katalog ClawHub yang diambil dari Gateway (#139042). Ada juga kartu ClawHub yang muncul di chat (#142782) — jadi kamu bisa minta rekomendasi plugin langsung tanpa keluar dari percakapan.

Efek sampingnya bagus: kamu tidak perlu lagi bingung "ini plugin bawaan atau harus install dari marketplace?" — satu tampilan, satu jawaban.

## ☁️ Cloud Session: Lebih Murah, Lebih Terkendali

Untuk yang menjalankan kerja agent di mesin cloud, ada beberapa perbaikan yang menghemat uang dan saraf:

- **Reuse project setup** — session cloud baru bisa memakai ulang project yang sudah di-setup, jadi tidak mengulang instalasi berulang-ulang.
- **Kirim pesan saat session masih setup** — pesanmu ditahan dan dijalankan begitu mesin siap, tidak perlu copy-paste ulang.
- **Desktop di Azure cloud worker** sudah didukung sekarang (GCP masih belum).
- **WSL2 Windows dan macOS cloud worker** bisa jalan lewat Crabbox.
- Setting cloud worker bisa diatur dari Settings: batas komputer cadangan, profil default per repository, dan hover untuk melihat OS/CPU/RAM sebuah session.

Satu catatan penting: kalau komputermu memblokir unduhan otomatis Crabbox, siapkan **Crabbox 0.55.0** atau lebih baru sebelum upgrade — tool ini wajib bahkan hanya untuk *memeriksa* cloud worker yang sudah ada.

## 🖼️ GPT Image 2.5 dan Jawaban Interaktif di Terminal

Dua tambahan yang kelihatan kecil tapi kepakai tiap hari:

**GPT Image 2.5** (varian Flare dan Sunburst) bisa generate *dan* edit gambar lewat OpenAI atau fal. Ukuran custom, kualitas lebih tinggi, output PNG transparan atau WebP. Edit bisa memakai sampai **5 gambar referensi** via OpenAI atau **16 via fal**, dan hasilnya sampai 4 gambar sekaligus.

**Pertanyaan interaktif di terminal** — agent sekarang bisa bertanya dan menunggu jawabanmu di CLI, bukan cuma diam lalu menebak.

## 🛡️ Keamanan dan Update Lebih Waras

Ada juga perbaikan review perintah otomatis: perintah rutin yang aman boleh lewat, perintah berbahaya bisa **ditolak dengan alasan**, dan untuk kasus abu-abu OpenClaw bertanya dulu ke kamu. Yang high-risk tetap wajib persetujuan manusia.

Masalah Node yang sering bikin gagal start juga ditangani: OpenClaw bisa mencari Node kompatibel yang sudah ada, atau menawarkan instalasi privat khusus untuk dirinya sendiri. Instalasi jaringan yang berpotensi mengekspos OpenClaw **tanpa autentikasi kini diblokir** sebelum ada perubahan apa pun.

## 📊 Repo Ini Tidak Main-Main

Per September 2026, `openclaw/openclaw` ada di **389.855 bintang GitHub**. Komunitasnya juga hidup di bahasa Indonesia — channel WPU di YouTube sudah membahas perbandingan "OpenClaw 2.0 vs Hermes Agent", jadi bahan belajar lokal sudah tersedia.

## Kesimpulan

Versi **2026.9.4** bukan rilis yang mengubah wajah OpenClaw, tapi menambal hal-hal yang paling sering bikin self-hoster frustrasi: skill yang tidak pernah belajar dari pengalaman, plugin yang tersebar, dan cloud session yang boros. Kalau kamu sudah jalan di 2026.9.1 dan update gagal, jangan ulang perintah yang sama terus — baca panduan update, karena sejumlah perbaikan **baru berlaku setelah updater versi baru terpasang**.

Kamu pakai agent AI buat kerja apa sehari-hari? Cerita di kolom komentar — kalau menarik, bisa jadi bahan artikel berikutnya.

— Chokdi 🐷 · Content Studio · 2026
