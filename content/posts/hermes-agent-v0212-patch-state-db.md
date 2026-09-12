---
title: "Hermes Agent v0.21.2: Patch state.db, Akar Korupsi Database Akhirnya Dibasmi"
date: 2026-09-12T12:10:00+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Update", "Self-Hosted"]
---

Kalau kamu pernah lihat `state.db` rusak setelah update ke Hermes Agent v0.21.0, kamu tidak sendirian — dan rilis **v0.21.2** (tag `v2026.9.11`, dirilis 11 September 2026) memang dibuat khusus untuk menutup masalah itu. Ini bukan rilis fitur besar, melainkan **patch release**: tim Nous Research membongkar akar penyebab database sesi jadi rapuh, bukan menambal gejalanya.

## Kenapa state.db bisa rusak setelah v0.21.0

v0.21.0 menulis ulang cara session store membuka koneksi. Efeknya, beberapa instalasi jadi punya **penulis kedua** (second writer) ke file yang sama — dan di SQLite itu resep klasik korupsi data. Yang ditemukan di release notes resminya:

- Gateway per profil menulis state "hosted room" ke `state.db` **root setiap 5 detik**.
- Dashboard membuka handle *writable* begitu aplikasi start.
- Lifecycle guard milik cron melakukan `open()` mentah ke database yang sedang hidup — ini membatalkan POSIX lock milik gateway.
- `doctor --fix` menjalankan checkpoint di atas database yang masih dipegang proses lain.

Semuanya sudah dihapus di rilis ini. Hosted room sekarang hidup di `shared-state.db` yang terpisah, dashboard membuka koneksi **read-only dulu**, guard lewat connection registry yang terlacak, dan `doctor --fix` menolak checkpoint yang tidak bisa dibuktikan aman.

## Enam PR, 44 issue ditutup sekaligus

Kampanye perbaikan state.db ini menutup 44 issue. Beberapa yang paling terasa buat pengguna:

- **Database WAL yang sehat berhenti macet.** `DeletedWalGenerationError` palsu (dipicu dentry `(deleted)` OpenZFS dan race `close()` melawan `append_message`), error `disk I/O` transien di WSL2, sampai banner "database is locked" yang muncul padahal lock-nya sudah hilang — semua dibereskan.
- **Kerusakan indeks FTS tidak lagi mematikan percakapan.** Error yang cuma soal full-text search dulu diklasifikasi sebagai "korupsi seluruh file" lalu menutup turn. Sekarang diklasifikasi `fts_index`: pencarian turun kualitas sementara, indeks dibangun ulang, transkrip tetap utuh.
- **Satu baris rusak tidak lagi membunuh `sessions list`.** Timestamp TEXT atau epoch `1e30` dulu membuat seluruh listing, export, dan insights crash. Sekarang baris buruk ditampilkan `?` plus WARNING yang menyebut nama sesinya.
- **Sesi tidak lagi nyasar ke database profil lain.** Desktop launch backend bisa terkunci ke `state.db` profil yang salah saat race `HERMES_HOME`, dan `session_search` dengan ID polos diam-diam memindai semua profil lalu mengembalikan transkrip milik profil lain.
- **Buka state.db tidak lagi mengambil write lock kalau tidak ada yang perlu ditulis.** Proses `hermes` sekali jalan di belakang gateway yang sibuk dulu nyangkut **4–20 detik** lalu gagal dengan "database is locked". Sekarang **0,01 detik**.

## Angka rilisnya

Jendela perubahan sejak v0.21.1 tercatat: **947 commit non-merge**, **1.869 file berubah** (+182.504 / −15.564 baris), **312 PR merged**, dan **140 kontributor**. Repo `NousResearch/hermes-agent` kini menyentuh **245 ribu bintang** dan 50,7 ribu fork.

## Selain state.db

- **Password-blind credential vault.** Agent bisa login, membayar, dan mengisi alamat dari 1Password, Bitwarden, atau vault lokal Hermes **tanpa pernah melihat secret-nya**. Kode 2FA diambil dari authenticator key tersimpan atau diminta lewat UI kamu.
- **Plugin catalog.** Indeks plugin terkurasi dengan SHA pinning — lengkap dengan CLI, admission CI, dokumentasi, dan satu halaman "Plugins" di Desktop untuk instalasi serta pin per-commit.
- **Nous free tier + guided first launch.** Inference gratis dan `/login` langsung dari chat, plus onboarding awal di balik env `HERMES_GUEST_ONBOARDING=1`.
- **Picker model bertambah.** DeepSeek V4.1 Flash masuk di pilihan Nous Portal dan OpenRouter, GPT Image 2.5 via OpenAI/FAL, serta Opus 5 dan Fable 5.1 di picker Anthropic native.

## Yang perlu kamu lakukan kalau self-host multi-profil

1. **Update** dengan `hermes update`. Kalau `state.db` kamu sudah terlanjur rusak, jalankan `hermes doctor --fix` setelah upgrade — perbaikan `.recover`, database ber-header nol, dan orphan FTS5 sudah ikut di rilis ini.
2. **Pastikan hanya ada SATU penulis per state.db.** Ini pelajaran mahal di server kami sendiri: dua proses yang menulis ke `state.db` yang sama (UI web + gateway) pernah membuat file korup berulang dan harus di-repair berkali-kali. Aturan yang akhirnya kami pakai: satu writer saja, sisanya read-only.
3. **Backup sebelum upgrade.** Copy `state.db` beserta `state.db-wal` selagi prosesnya berhenti, jangan saat gateway sedang sibuk.
4. **Cek isolasi profil kamu.** Perbaikan multi-profile di rilis ini berarti bot profil sekunder tidak lagi mewarisi allow-list, credential, atau secret vault milik profil default.

Kalau kamu baru mulai dan belum pernah menyentuh jalur v0.21.x, lihat dulu catatan rilis [v0.21.1](/posts/hermes-agent-v0211-september-2026/) dan deadline kompatibilitas plugin [14 September](/posts/hermes-plugin-compat-14-september/). Untuk yang menjalankan banyak agent, [peta memory Hindsight dan Mnemosyne](/posts/hermes-true-memory-mnemosyne-hindsight/) juga relevan dibaca sebelum menata ulang state.

Sumber resmi: [release notes v0.21.2 (v2026.9.11)](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.9.11).

Pernah kena "database is locked" atau state.db corrupt setelah update? Tulis di komentar — saya penasaran seberapa luas kasus ini di instalasi self-host.

— Chokdi 🐷 · Content Studio · 2026
