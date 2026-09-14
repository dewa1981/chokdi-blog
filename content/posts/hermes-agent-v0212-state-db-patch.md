---
title: "Hermes Agent v0.21.2: Patch yang Menyelamatkan state.db"
date: 2026-09-14T17:20:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Update"]
---

Kalau kamu pengguna **Hermes Agent** dan sempat kena error aneh setelah update ke v0.21.0 — sesi hilang, `sessions list` error, database diklaim korup padahal sehat — kabar baiknya datang 11 September 2026. Nous Research merilis **v0.21.2 (tag v2026.9.11)**, patch yang secara khusus memburu akar masalah `state.db`.

Ini bukan rilis fitur. Ini rilis penyelamatan.

## 🐷 Apa yang Sebenarnya Rusak di v0.21.0

v0.21.0 menulis ulang cara Hermes menangani koneksi ke session store. Niatnya bagus: performa dan skalabilitas. Tapi ada efek samping yang bikin `state.db` rapuh di banyak instalasi.

Empat penyebab utamanya, semuanya soal **penulis kedua** ke database yang sama:

- Profile gateway menulis state hosted-room ke `state.db` root setiap 5 detik.
- Dashboard membuka handle *writable* saat startup.
- **Lifecycle guard cron** melakukan `open()` mentah ke database yang sedang hidup — ini resep klasik "cara mengorupsi SQLite", karena membatalkan POSIX lock milik gateway.
- `doctor --fix` menjalankan checkpoint di atas holder yang masih hidup.

Empat-empatnya sudah dihilangkan di v0.21.2. Hosted room sekarang tinggal di `shared-state.db` terpisah, dashboard buka read-only dulu, guard lewat connection registry resmi, dan `doctor --fix` menolak checkpoint yang tidak bisa ia buktikan aman.

## 🔧 Yang Berubah Buat Kamu

Skala rilisnya besar untuk ukuran patch: **947 commit non-merge**, **1.869 file berubah** (+182.504 / −15.564), **312 PR** di-merge, **140 kontributor**. Enam PR khusus menutup 44 issue di kampanye `state.db`.

Satu temuan yang penting buat kamu ketahui:

**FTS rusak tidak lagi mematikan percakapan.** Dulu, error yang cuma di indeks full-text-search diklasifikasi sebagai korupsi seluruh file → sesi langsung fail-closed. Sekarang error itu dilabeli `fts_index`: pencarian menurun kualitasnya, indeks di-rebuild belakangan, transcript tetap utuh.

**Satu baris rusak tidak lagi membunuh `sessions list`.** Timestamp bertipe TEXT atau epoch `1e30` dulu bikin seluruh listing crash. Sekarang ada `coerce_epoch()` di setiap reader — baris jelek tampil sebagai `?` dengan WARNING yang menyebut nama sesi.

**Buka `state.db` tidak lagi ngambil write lock kalau tidak ada yang perlu ditulis.** Proses `hermes` satu-kali yang membuka store di belakang gateway sibuk dulu macet 4–20 detik lalu gagal dengan "database is locked". Sekarang 0,01 detik.

Selain itu ada pengamanan isolasi multi-profile (bot profile sekunder tidak lagi mewarisi allow-list atau kredensial profile default), dan **Desktop backend spawn storm** — Bot Mode yang dulu men-spawn backend per profile tiap tick dan per baris roster — sudah berhenti.

## 🚀 Cara Update

```bash
hermes update
```

Fresh install:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Kalau `state.db` kamu sudah terlanjur rusak sejak 0.21.0 atau 0.21.1, urutannya begini:

1. `hermes doctor` — versi baru ini sudah bisa membedakan kerusakan struktural vs kerusakan indeks.
2. Kalau rebuild tidak cukup: `hermes sessions recover --inspect-only` (wajib di-pin ke profile).

Catatan dari kami di sini: rilis ini menutup kelas bug yang juga kami alami — `DeletedWalGenerationError` yang bikin "session history unavailable" berulang, dan masalah writer ganda di staging. Kalau kamu menjalankan **beberapa profile di satu gateway** (multiplex), rilis ini yang kamu tunggu.

## ✨ Bonus yang Ikut Numpang

Bukan cuma perbaikan `state.db`. Rilis ini juga membawa:

- **Password-blind credential vault** — agent bisa sign in, bayar, dan isi alamat dari 1Password, Bitwarden, atau vault lokal tanpa pernah melihat secret-nya.
- **Plugin catalog** — indeks plugin terkurasi, di-pin dengan SHA, lengkap dengan CLI, admission CI, dan halaman dashboard.
- **Nous free tier** — inference dan connector gratis langsung dari satu perintah login, plus `/login` dari dalam chat.

## 🧭 Kesimpulan

v0.21.2 adalah contoh rilis yang jujur: mereka tidak menambal gejalanya, tapi membongkar penyebabnya. Kalau instalasi Hermes kamu sempat kelihatan "korup" sejak awal September, kemungkinan besar database-mu sehat — yang bermasalah adalah siapa saja yang menulis ke situ. Update, lalu jalankan `hermes doctor`.

Kamu pakai Hermes untuk apa? Kalau ada cerita soal bug `state.db` ini, tulis di komentar — kami kumpulkan buat artikel lanjutan.

— Chokdi 🐷 · Content Studio · 2026
