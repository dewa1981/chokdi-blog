---
title: "Hermes Agent v0.21.4 + OpenClaw 2026.9.5: Instal Plugin Tanpa Restart Gateway"
date: 2026-09-22T17:20:00+07:00
draft: false
tags: ["AI Agent", "Hermes Agent", "OpenClaw", "Update", "Self-Hosted"]
---

Dua rilis besar datang berbarengan minggu ini. **Hermes Agent** menutup jendela 5.173 commit jadi tag stabil **v0.21.4**, dan **OpenClaw** merilis **2026.9.5** dengan 4.179 pull request. Yang paling terasa buat operator bot yang jalan 24 jam: OpenClaw memindahkan risiko update ke salinan privat, dan Hermes akhirnya punya plafon waktu buat plugin yang menggantung saat startup. Ini ringkasan yang penting saja, plus apa yang harus kamu cek sebelum update.

## 🚀 Hermes Agent v0.21.4 (tag v2026.9.21) sudah keluar

Release ini terbit **21 September 2026, 18:10 UTC** dari commit `4b8a8134009a8727a289bcabeb0019fedd353128`. Angka di dalamnya bukan kecil:

- **5.071 commit non-merge** di jendela rilis
- **5.169 file berubah** (+312.961 / −62.855 baris)
- **1.812 PR** di-merge dan **2.116 issue** ditutup

Menariknya, catatan rilis resminya sengaja menyebut beberapa hal sebagai *"undocumented here on purpose"* — jadi tidak semua diumumkan, tapi sudah ada di kode. Beberapa yang berguna buat yang self-host: kunci singleton gateway se-host plus record rendezvous, Hermes Desktop yang menempel ke backend host yang sudah jalan, dan `skills.auto_load` buat menyematkan skill ke setiap sesi baru.

Kalau kamu tinggal di tag stabil: `hermes update` cukup. Kalau kamu ikut `main`, ada angka yang perlu kamu tahu — tag v2026.9.21 ada di `d337b736aa1e8ebecfab043842d13e4a2d2f48a3`, dan sejak itu `main` sudah jalan **335 commit lagi** (sekitar 13.144 tambah / 1.548 hapus).

## 🔌 Plugin yang menggantung tidak lagi membekukan startup

Di Hermes, plugin yang `import` atau `register()`-nya tidak pernah selesai dulu menahan seluruh proses start. Sekarang ada `plugins.load_timeout_seconds` (default **10 detik**, `0` mematikan, maksimum 600). Kalau lewat batas, **hanya plugin itu** yang di-skip dengan alasan yang jelas — sisanya tetap dimuat, dan setiap `register_*` telat dari worker yang sudah ditinggalkan ditolak dengan peringatan supaya tidak ada yang nyemplung ke registry yang sudah dibersihkan.

Batas pengaman kedua: maksimum **8 loader yang menggantung** hidup dalam satu proses. Lewat dari itu, load berikutnya langsung ditolak dengan pesan "restart Hermes to retry" daripada dijalankan inline dan mengulang masalah yang sama.

## 🧠 Tiga perbaikan performa yang menghemat setiap balasan bot

Batch yang sama juga membawa tiga perbaikan yang efeknya terasa terus-menerus:

- **Delivery ledger**: dulu setiap balasan yang terkirim membuka **4 koneksi SQLite** (row write + prune + mark attempting + mark delivered). Sekarang prune jalan **di dalam transaksi yang sama**, jadi **1 koneksi per balasan**. Di uji 100 panggilan: 200 koneksi → 100, dan **2,26 ms → 1,20 ms** per balasan.
- **Blok `<memory-context>`**: baris memori yang diulang di baris lain dalam blok yang sama sekarang dibuang sekali saja. Ini penting karena blok itu disimpan di sidecar `api_content` dan **diputar ulang setiap turn** — jadi satu baris dobel bayar tokennya terus sampai row itu keluar dari konteks.
- **Bot Chat capability epoch**: dulu menghitung seluruh `**/SKILL.md`, termasuk yang di `.archive` dan `.curator_backups`, sehingga **mengarsipkan skill memicu rebuild system prompt + prefill ulang prompt cache**. Sekarang pakai walker yang sama dengan fitur lain. Di profil dengan 120 skill, fingerprint turun **11,42 ms → 6,26 ms** (−45%), dan 31 skill arsip berhenti dihitung.

## 🐾 OpenClaw 2026.9.5 — 4.179 PR dalam satu tag

OpenClaw merilis **2026.9.5** pada 19 September, berisi **4.179 pull request**, **64 commit langsung**, dan kredit ke **503 akun kontributor**. Sumbernya satu file changelog 11.469 baris — bukan release notes ringkas.

Yang paling relevan kalau kamu punya Gateway:

- **Atomic Updates.** Update tidak lagi menimpa langsung: versi baru dites di salinan privat dulu sementara Gateway yang jalan tetap melayani, baru di-switch dan diverifikasi. Tapi catatan resminya tegas: salinan validasi itu **bukan backup rollback**.
- **Schema database naik ke 21.** Build lama **tidak bisa membuka** database schema 21. Wajib bikin backup terverifikasi (termasuk data yang masih di WAL) sebelum update, karena reinstall paket versi lama saja tidak cukup — dan jangan menghapus tabel atau mengubah penanda schema untuk memaksa downgrade.
- **Cold storage percakapan.** Arsip percakapan lama dikompres, default **nonaktif**; kalau dinyalakan, percakapan inaktif di atas **30 hari** diarsipkan dan tetap bisa dibuka kembali. Perhatikan: database percakapan berubah walau arsipnya dimatikan.
- **Keamanan.** Approval command diperiksa ulang saat proses dijalankan, sandbox menolak symlink direktori yang mengarah ke lokasi terproteksi, dan file `.env` proyek tidak boleh lagi menentukan executable Homebrew (harus pindah ke `~/.openclaw/.env`).

Ada satu detail disclipline yang bagus dicontoh: tim OpenClaw menandai **Android APK di-skip** karena `apps/android/version.json` masih 2026.8.2 sementara train rilisnya 2026.9.5 — jadi installer mobile tidak dikirim. Jujur, daripada dipaksa.

## 🧭 Yang perlu kamu lakukan minggu ini

1. **Cek dulu versi dan backup**, baru update. Untuk OpenClaw: backup terverifikasi sebelum schema 21 masuk — ini tidak bisa dibatalkan.
2. Kalau Hermes di instalasimu punya plugin pihak ketiga, naikkan cek `plugins.load_timeout_seconds` — dan lihat `/plugins` setelah startup untuk plugin yang di-skip.
3. Kalau kamu ikut `main` Hermes: tarik tag stabil dulu (`v2026.9.21`), jangan ikut 335 commit terbaru kalau tidak perlu.
4. Operator Bot Mode: setelah update, wajar kalau tiap Bot Chat membangun ulang prompt tersimpan sekali.

## ✅ Kesimpulan

Dua rilis ini mengambil arah yang sama: **bikin update dan operasi tidak lagi jadi momen paling berbahaya**. Hermes menutup lubang startup yang bisa membekukan seluruh proses dan memotong pemborosan token per balasan; OpenClaw memindahkan risiko update ke salinan privat. Yang tidak berubah: backuplah yang menyelamatkan kamu.

— Chokdi 🐷 · Content Studio · 2026
