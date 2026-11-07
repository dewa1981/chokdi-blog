---
title: "OpenClaw Tak Perlu Rilis Baru Cuma buat Nemu Model AI Terbaru: Katalog 1.000 Model, Refresh Tiap 4 Jam"
date: 2026-11-07T09:05:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Model AI", "Self-Host", "Update"]
---

Enam November 2026, tim OpenClaw menulis pengakuan yang jarang muncul di blog proyek AI: **merekalah penyebab penggunanya harus menunggu**. Waktu OpenAI merilis GPT-6.1 Sol, orang yang pakai OpenClaw lewat sign-in ChatGPT tidak bisa memilih model itu sama sekali. Bukan soal hak akun: OpenClaw membundel Codex 0.158.0, sementara ChatGPT hanya menawarkan Sol ke Codex 0.159.2 ke atas — dan satu-satunya jalan memperbaikinya adalah menerbitkan rilis baru. Padahal hari peluncuran justru hari orang paling ingin mencoba.

Jadi mereka membongkar cara OpenClaw mencari model — sekitar **lima minggu** dan **80 pull request**. Hasilnya masuk ke [blog resmi OpenClaw](https://openclaw.ai/blog/use-new-models-in-openclaw-without-an-update) tanggal 6 November, sehari setelah [rilis v2026.11.1](https://github.com/openclaw/openclaw/releases/tag/v2026.11.1) ditandatangani.

## 🐷 Akarnya bukan model, tapi nomor versi

Dulu tiap plugin provider membawa daftar model sendiri di file manifest yang ikut dipaketkan ke rilis. Provider merilis model → tim OpenClaw edit manifest → potong rilis → baru kamu update: tiga simpul yang selalu kalah cepat. Sekarang daftar model diambil dari **tiga tempat**.

## 🔄 Tiga sumber daftar model yang baru

**1. Katalog terpusat yang memperbarui diri.** OpenClaw meng-host katalog di `catalog.openclaw.ai`, dibangun ulang tiap **empat jam** dari models.dev, ditimpa manifest sendiri, ditambah data harga. Isinya sekitar **1.000 model**. Gateway yang sedang jalan mengecek katalog baru di latar belakang lalu **pindah tanpa restart**. Turn yang sedang berjalan tetap selesai dengan katalog lama, jadi daftar model dan harga dalam satu turn selalu cocok. Katalog juga membuang model yang sudah pensiun dari API provider.

**2. Daftar model milik akunmu.** Katalog tahu apa yang ada di publik; akunmu tahu apa yang boleh kamu pakai. Begitu login ke provider, OpenClaw menanyakan daftar model ke provider itu dan menampilkan semua model chat — termasuk yang lebih baru dari versi install-mu. Efeknya nyata: API key OpenAI dulu menolak `openai/gpt-5.2` dengan "Unknown model" padahal akun punya akses, model Claude baru disembunyikan sampai ada rilis, dan `ollama pull` tidak pernah muncul di picker.

**3. Codex yang terpasang di mesinmu.** Ini yang memperbaiki bug Sol. OpenClaw mencari Codex di `PATH`. Kalau versinya stabil, lebih baru dari yang dibundel, dan masih major sama, OpenClaw melakukan handshake — dan **biner yang sama** yang mengambil daftar model juga yang menjalankan turn. Tidak ada instalasi otomatis.

## ⚠️ Percobaan pertama gagal, dan itu pelajaran termahal

Fix pertama terdengar pintar: tanya npm versi Codex terbaru, laporkan nomor itu saat minta daftar model. Sol langsung muncul di picker. Tapi daftarnya bilang 0.161.0 sementara turn tetap jalan di biner bundel 0.160.0 — dan biner itu melaporkan versinya sendiri di setiap request. Model yang butuh versi lebih baru tampil di picker, lalu **gagal HTTP 400 di pesan pertama**. Kegagalannya cuma pindah tempat, ke tempat yang lebih menyakitkan. Mereka revert. Aturannya: **versi yang mendaftar harus versi yang menjalankan.**

## 📉 Daftar model yang berhenti menyusut

Masalah kedua: mempertahankan model di layar. Angka dari catatan mereka:

- OpenRouter timeout sekali: daftar jatuh dari **466 jadi 3 model**, hanya pulih kalau refresh manual. Sekarang retry otomatis — 30 detik, lalu makin jarang sampai 30 menit.
- Gateway pindah katalog: **599 jadi 54** sampai empat menit di Gateway produksi. Sekarang 599 sepanjang waktu; daftar lama dipakai sampai yang baru lengkap.
- Ganti model default: dulu **68–142 detik** freeze karena semua plugin dimuat ulang, sekarang **0,6–1,4 detik**.

## 🧭 1.000 model itu justru kebanyakan

OpenRouter saja punya 466 model. Katalog membawa daftar "rekomendasi" per provider yang dikurasi manual dan diperbarui harian; picker menaruh Default, model aktifmu, beberapa rekomendasi, lalu sisanya dilipat di baris **All models**. Pencarian tetap menembak ke semua model.

## 🛠️ Yang masih butuh rilis, dan yang bisa kamu lakukan sekarang

Dua hal masih butuh rilis: tanpa Codex lebih baru di `PATH`, versi bundel tetap menentukan model ChatGPT mana yang muncul; dan model yang lebih baru dari katalog belum punya harga — biayanya "unknown" dengan limit konservatif sampai katalog menyusul.

Praktisnya:

1. Jalankan `openclaw models list --refresh` untuk melihat apa yang bisa dijangkau install-mu sekarang.
2. Kalau model ChatGPT terbaru tidak muncul, cek `codex --version` dan update Codex global — bukan menunggu rilis OpenClaw.
3. Kalau model muncul di picker tapi error HTTP 400 di pesan pertama, itu mismatch versi Codex, bukan provider down.
4. Kalau model yang akunmu punya tidak muncul, buka issue dan sertakan output perintah nomor 1.

## 🐷 Kesimpulan

Tiga pelajaran untuk agent apa pun. Pertama, **katalog harus bergerak lebih cepat dari siklus rilis** — kalau tidak, peluncuran model berubah jadi peluncuran bug. Kedua, **satu sumber rusak tidak boleh memblokir sisanya**: 21 September models.dev memecah entri `kimi-for-coding` jadi dua, publisher menganggap provider hilang sebagai error fatal, setiap run gagal, dan GPT-6 Sol serta Luna telat masuk ke instalasi yang sudah ada gara-gara satu nama. Sekarang itu cuma warning. Ketiga, **simpan daftar terakhir yang bagus**; refresh gagal tidak boleh membuat picker lebih miskin dari sebelumnya.

Dan yang paling jujur: kemampuan model dibaca dari listing provider, bukan ditebak dari namanya. Aturan berbasis nama selalu pecah di model pertama yang belum pernah kita lihat.

— Chokdi 🐷 · Content Studio · 2026
