---
title: "Hermes Agent v0.21.3: Fix Refresh Burst & Bocor Handle state.db — Panduan Aman Update"
date: 2026-09-17T09:30:00+07:00
draft: false
tags: ["Hermes Agent", "AI", "Nous Research", "Update", "Self-Hosted", "state.db", "Docker"]
---

Nous Research menandai rilis **Hermes Agent v0.21.3 (v2026.9.14)** pada 14 September 2026. Sekilas ini cuma patch release — tapi isinya persis jenis masalah yang bikin agent produksi mati diam-diam: **sesi remote yang expire sendiri** dan **handle database yang bocor**. Kalau kamu jalankan Hermes di VPS, Docker, atau Hermes Cloud, rilis ini penting.

## Masalah Pertama: Sesi Remote Expire saat Refresh Barengan

Kasusnya seperti ini. Desktop atau dashboard melakukan **refresh token berputar** (rotating refresh token). Saat aplikasi bangun dari sleep, dia bisa menembakkan **beberapa request refresh sekaligus** — "refresh burst". Problemnya: request kedua membawa token yang **sudah dipakai** request pertama. Portal melihat token lama dipakai ulang, menganggapnya sebagai **token reuse attack**, lalu **mencabut seluruh sesi**.

Hasilnya kamu merasa "login terus tapi selalu logout sendiri". Yang diperbaiki di v0.21.3:

- **Cookie gate dan bearer route** di gateway sekarang **menggabungkan (coalesce) request bersamaan** yang membawa rotating token yang sama — jadi burst tidak lagi mereplay token yang sudah dirotasi.
- Refresh **dijalankan di luar event loop**, jadi identity provider yang lambat tidak lagi membekukan endpoint `/api/status`.
- Dipasangkan dengan perubahan sisi Portal (`hermes-portal#1209`): **idle horizon 30 hari** dan **grace 5 menit** untuk token yang sudah dirotasi.

Analogi gampangnya: dulu lima orang antre di pintu dengan **tiket yang sama**, satpam panik dan menutup gedung. Sekarang satpam cuma mengizinkan satu yang memproses, sisanya menunggu hasilnya — dan gedung tetap terbuka.

## Masalah Kedua: Handle state.db Bocor di Proses Panjang Umur

Ini yang lebih senyap. Setiap proses yang hidup lama — **gateway, backend dashboard/Desktop, ACP, dan CLI** — menempelkan **handle penulis (writer handle) duplikat** ke `state.db`. Dari luar agent kelihatan sehat, tapi di log muncul precursor `N live SessionDB handles` yang naik terus. Ujungnya: kontensi SQLite, WAL numpuk, dan database berisiko terkunci.

Perbaikan di v0.21.3: proses pembaca **attach secara read-only** dan penulis dalam satu proses **berbagi satu handle** dari registry. Jadi jumlah handle berhenti bertambah pada topologi yang sehat.

Ini menyambung kerja v0.21.2 (v2026.9.11) — rilis yang memang dikhususkan untuk **kampanye keandalan state.db**: enam PR, puluhan issue ditutup, memisahkan state room hosted ke `shared-state.db` dan memaksa handle dashboard menjadi read-only.

## Skala Rilisnya Tidak Kecil

Angka yang dilaporkan di catatan rilis, diukur pada commit `9b419a2`:

- **1.036 non-merge commit**
- **2.642 file berubah** (+131.690 / −37.096 baris)
- **338 pull request** digabung sejak v0.21.2

Yang juga ikut masuk tapi sengaja tidak dibahas panjang: permintaan JSON-RPC server→client plus **registry wire-contract Pydantic** dengan generate TypeScript/OpenRPC untuk gateway TUI/Desktop, pilihan **reasoning effort** di setiap model picker, login **OpenRouter OAuth PKCE**, decoding gambar **HEIF/HEIC/AVIF**, refresh token MCP OAuth yang diikat ke issuer-nya, katalog FAL baru (Wan 3.0, Kling 3.0, MiniMax H3 Max Turbo, Gemini Omni Flash 1.1, Meta Muse), dan **penolakan state.db WAL pada filesystem lintas-VM**.

Catatan rilis lengkap dan terkurasi versi baru akan menyusul di **v0.22.0**, yang mendokumentasikan semuanya dari v0.21.0 ke atas.

## Poin Praktis: Cara Update yang Aman

Update-nya sebenarnya membosankan — dan itu pujian:

1. **Backup dulu.** Memory, skill, dan config disimpan sebagai file terpisah dari software, jadi update tidak menghapusnya. Tapi export 30 detik itu murah.
2. **Jalankan `hermes update`** (instalasi git), atau ulangi installer satu baris untuk instalasi bersih.
3. **Docker / Hermes Cloud** tinggal pakai image yang dibangun dari tag ini: `nousresearch/hermes-agent:v2026.9.14`. Cloud auto-update ke tag rilis terbaru — dan justru karena itu fix login di atas penting.
4. **Restart semua yang jalan.** Gateway, dashboard, Desktop, sesi CLI yang terbuka masih memakai build lama sampai di-restart.
5. **Cek versinya.** Kalau CLI masih menunjukkan v0.21.0, berarti proses lamanya belum benar-benar mati.
6. **Perhatikan filesystem.** Karena rilis ini menyertakan penolakan WAL pada filesystem lintas-VM, jangan taruh `state.db` di mount jaringan atau folder share Docker Desktop. Ini juga jawaban untuk keluhan "database korup setelah update".

## Kesimpulan

v0.21.3 bukan rilis yang bikin heboh di media sosial — tidak ada fitur besar di dalamnya. Tapi dua perbaikannya menyasar titik paling menyakitkan untuk operator: **sesi yang tiba-tiba dicabut** dan **database yang bocor handle**. Bagi siapa pun yang menjalankan agent 24/7, rilis tipe ini justru yang paling layak dipasang cepat.

Pola yang kelihatan jelas dari tiga patch terakhir — v0.21.1 (modularisasi besar), v0.21.2 (kampanye state.db), v0.21.3 (sesi remote + handle) — adalah satu hal: Nous sedang **mengeraskan fondasi**. Fitur-fitur besar ditahan sampai v0.22.0. Jadi kalau kamu menunggu headline feature, sabar sebentar; kalau kamu menunggu stabilitas, ini saatnya update.

— Chokdi 🐷 · Content Studio · 2026
