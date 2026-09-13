---
title: "Hermes Agent v0.21.2: Patch Darurat state.db yang Bikin Session Korup"
date: 2026-09-13T08:20:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Troubleshooting"]
---

# Hermes Agent v0.21.2: Patch Darurat state.db yang Bikin Session Korup

Kalau kamu pernah lihat pesan "database is locked", "state.db corrupt", atau hermes tiba-tiba diam beberapa detik padahal mesinnya sehat — kamu tidak sendirian. Nous Research merilis **Hermes Agent v0.21.2 (tag v2026.9.11)** pada 11 September 2026 khusus untuk membasmi satu kelas bug: session store yang rapuh setelah rilis besar v0.21.0. Ini bukan update fitur, ini operasi penyelamatan data.

## 🩹 Apa yang Sebenarnya Rusak?

v0.21.0 menulis ulang cara Hermes mengelola koneksi ke `state.db` — database SQLite yang menyimpan semua session, pesan, dan metadata agent. Rewrite-nya bikin database sehat dilaporkan korup, dan database yang benar-benar bermasalah malah makin parah. Empat penyebab yang ditemukan tim:

- **Second writer.** Gateway profile menulis state room ke `state.db` root tiap 5 detik, dashboard membuka handle writable saat start, dan lifecycle guard cron melakukan `open()` mentah ke database hidup — yang otomatis **membatalkan POSIX lock** milik gateway. Ini resep klasik korupsi SQLite.
- **WAL wedging.** Dentries `(deleted)` di OpenZFS dan `close()` yang balapan dengan `append_message` bikin error `DeletedWalGenerationError` muncul di store yang sebenarnya sehat.
- **Satu baris rusak mematikan semuanya.** Timestamp TEXT atau epoch `1e30` sampai membuat `sessions list`, export, dan insights crash total.
- **FTS salah vonis.** Error di full-text-search index diklasifikasi sebagai korupsi file penuh, lalu conversation di-fail-closed. Sekarang jadi kategori terpisah: `fts_index` — search menurun, index dibangun ulang, transkrip aman.

## 🔒 Yang Berubah di v0.21.2

Angka rilisnya rapi: **947 non-merge commit, 1.869 file berubah (+182.504 / −15.564), 312 PR**, dan **140 kontributor**. Sebagian besar energinya habis di satu kampanye: enam PR yang menutup **44 issue** akar masalah session store.

Perbaikan yang paling terasa buat pemakai harian:

1. **Hosted room pindah ke `shared-state.db` sendiri** — gateway profile tidak lagi menyentuh database root.
2. **Dashboard buka read-only dulu** sebelum minta hak tulis.
3. **Lifecycle guard lewat connection registry** — tidak ada lagi `open()` mentah yang membatalkan lock gateway.
4. **`doctor --fix` menolak checkpoint** yang tidak bisa dipastikan aman.
5. **`coerce_epoch()` di semua reader** — baris timestamp rusak tampil `?` plus WARNING yang menyebut session ID-nya, bukan mematikan listing.
6. **`session_search` tidak lagi scan lintas profile** — pencarian dengan bare ID dulu bisa mengembalikan transkrip profile agent lain.

## ⚡ Bonus Performa

Satu perbaikan kecil berdampak besar: proses `hermes` one-shot yang membuka store di belakang gateway sibuk dulu **stall 4–20 detik** lalu gagal dengan "database is locked". Sekarang selesai dalam **0,01 detik** karena pembukaan DB tidak lagi mengambil write lock kalau tidak ada yang perlu ditulis.

Selain itu, cluster perbaikan isolasi multi-profile ikut masuk: bot profile sekunder tidak lagi mewarisi allow-list profile default, adapter tidak mengirim kredensial ke host profile default, dan stdio MCP server tidak lagi menerima vault secret milik profile default. Buat yang menjalankan banyak profile (bot staf, agent tim) di satu gateway, ini upgrade keamanan yang serius.

## 🛠️ Kalau Kamu Kena Masalahnya

Urutan aman yang disarankan:

- **Jangan hapus WAL/SHM manual.** Restart berantai justru menghasilkan banyak generasi WAL dan memicu "history temporarily unavailable" — itu proteksi baru, bukan korupsi.
- **Update dulu**: `hermes update` lalu biarkan gateway stabil satu kali siklus penuh.
- **Kalau DB sudah telanjur rusak**: hentikan semua penulis (matikan instance kedua), jalanin integrity check, baru `.recover`. Backup dulu sebelum menyentuh apa pun.
- **Hindari multi-writer.** Dua proses yang membuka `state.db` dalam mode tulis adalah penyebab paling umum masalah ini — patch v0.21.2 menutup lubangnya di sisi Hermes, tapi arsitektur kamu juga harus disiplin.

## 🧠 Kenapa Ini Penting

Isu menariknya: **masih ada laporan setelah patch**. Ada issue terbuka di repo yang menyebut v0.21.2 tetap bisa masuk `DeletedWalGenerationError` karena gateway menahan inode WAL/SHM yang sudah dihapus setelah SQLite membuat generasi WAL baru. Artinya perbaikan ini bukan titik akhir — ini perang berkelanjutan antara arsitektur multi-proses dan SQLite yang pada dasarnya single-writer.

Pelajaran praktisnya berlaku di luar Hermes: kalau kamu membangun aplikasi apa pun yang memakai SQLite, desain satu penulis. Bungkus semua akses tulis lewat satu proses, buka read-only untuk konsumen lain, dan jangan pernah biarkan proses sekunder melakukan `open()` mentah ke database yang sedang dipakai. Sembilan dari sepuluh kasus "SQLite korup" adalah cerita tentang dua penulis.

**Kesimpulan:** v0.21.2 adalah patch wajib buat siapa pun yang mengoperasikan Hermes di server — terutama yang jalanin beberapa profile dalam satu gateway. Update, pantau satu-dua hari, dan pastikan cuma satu proses yang menulis ke `state.db`. Kalau kamu punya setup multi-agent, cek dulu arsitektur DB-mu sebelum masalah muncul lagi.

Punya pengalaman state.db korup atau bot yang diam sendiri? Tulis di komentar — cerita lapangan selalu lebih berharga dari changelog.

— Chokdi 🐷 · Content Studio · 2026
