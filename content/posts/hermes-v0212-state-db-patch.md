---
title: "Hermes Agent v0.21.2: Patch Penyelamat state.db yang Sempat Bikin Chat Gagal Dibuka"
date: 2026-09-15T08:00:00+07:00
draft: false
tags: ["hermes-agent", "ai-agent", "database", "sqlite", "open-source"]
---

Kalau kamu pengguna Hermes Agent dan sempat panik karena chat tiba-tiba tidak bisa dibuka setelah update ke v0.21.0, kamu tidak sendirian. Banyak pengguna melaporkan hal yang sama: database `state.db` yang tadinya sehat tiba-tiba dituduh korup, `sessions list` gagal jalan, dan percakapan hilang dari tampilan. Kabar baiknya, Nous Research merilis **Hermes Agent v0.21.2 (v2026.9.11)** pada 11 September 2026 — dan ini murni *patch release* yang fokus menutup seluruh kelas bug tersebut.

## 🐞 Apa yang Sebenarnya Terjadi di v0.21.0?

v0.21.0 membawa penulisan ulang besar-besaran pada cara session store menangani koneksi database. Niatnya bagus, tapi efek sampingnya kasar untuk sebagian instalasi:

- **Dua penulis saling membatalkan lock.** Gateway profil menulis state ke `state.db` root setiap 5 detik, sementara dashboard membuka handle writable saat startup.
- **Database sehat dilaporkan korup.** Muncul `DeletedWalGenerationError` di store yang sebenarnya masih bagus.
- **Satu baris rusak mematikan seluruh daftar.** Satu timestamp bertipe TEXT atau epoch `1e30` cukup untuk membuat `sessions list` crash total.

Ada satu temuan yang menarik: cron lifecycle guard ternyata melakukan `open()` mentah ke database yang sedang hidup. Itu resep klasik cara mengorupsi SQLite — persis masalah yang kami alami sendiri di server produksi Chokdi beberapa waktu lalu, dan solusinya sama: **jangan pernah buka `state.db` yang sedang dipakai penulis aktif**, salin dulu ke lokasi lain kalau mau dibaca.

## 🔧 Enam PR yang Menutup Akar Masalahnya

Yang membuat rilis ini layak diapresiasi: mereka tidak menambal gejala, tapi membongkar akarnya.

| Masalah | Perbaikan di v0.21.2 |
|---|---|
| Penulis kedua di state.db | Hosted room pindah ke `shared-state.db` terpisah |
| Dashboard buka handle writable | Dashboard buka read-only lebih dulu |
| Cron guard `open()` mentah | Lewat connection registry yang ter-track |
| `doctor --fix` checkpoint saat DB hidup | Menolak checkpoint yang tidak bisa dibuktikan aman |
| FTS rusak dianggap korup total | Klasifikasi baru `fts_index` — search turun, transcript aman |
| Buka DB tanpa perlu nulis | Dari 4–20 detik + error "database is locked" jadi 0,01 detik |

Satu detail kecil yang penting: `.recover` tidak lagi gagal startup hanya karena ada tabel shadow FTS5 yang yatim, dan database dengan header zeroed sekarang bisa dipulihkan, bukan langsung ditolak.

## 🛡️ Isolasi Multi-Profile Ikut Dikencangkan

Kalau kamu menjalankan beberapa profil di satu gateway — seperti kami yang menjalankan Chokdi utama plus staging dan bot staf — bagian ini relevan. Sebelumnya, bot profil sekunder bisa mewarisi allow-list profil default, adapter bisa mengirim kredensial ke host profil default, dan server MCP stdio bisa menerima secret vault profil default.

Sekarang semuanya dipisah: pengiriman `MEDIA:` tidak bisa lagi menyertakan `.env`, `auth.json`, atau `state.db` milik profil lain. Ini penting kalau kamu memisahkan bot kerja dan bot pribadi di satu mesin.

## 💡 Poin Praktis Kalau Kamu Kena Masalah Serupa

Beberapa pelajaran yang berlaku umum, bukan cuma untuk Hermes:

1. **Jangan panik dan langsung repair.** Kalau chat gagal dibuka sekali, refresh dulu. Satu `disk I/O error` transien di WSL2 bukan tanda kerusakan permanen.
2. **Selalu copy sebelum baca.** Kalau mau inspeksi database yang sedang dipakai, `cp state.db state.db-wal /tmp/` dulu. Koneksi terakhir yang close bisa menghapus `-wal`/`-shm` dan mematikan penulis yang sedang jalan.
3. **Pastikan satu penulis saja.** Dua proses yang menulis ke database yang sama adalah sumber utama korupsi, bukan bug library.
4. **Cek versi Node kamu.** SQLite bisa memotong teks di build Node lama — ini juga disorot di catatan rilis OpenClaw terbaru.
5. **Update ke v0.21.2 kalau kamu di v0.21.0 atau v0.21.1.** Jendela rilisnya mencakup 947 commit non-merge dan 312 PR yang sudah di-merge.

## 🌍 Konteks Lebih Besar: Lomba Agen AI Makin Ketat

Rilis ini datang di tengah persaingan yang menghangat. OpenClaw baru saja meluncurkan v2026.9.4 dengan 1.558 PR, dan di YouTube sudah banyak perbandingan langsung antara keduanya — salah satunya mengklaim Hermes menyalip OpenClaw dengan 224 miliar token per hari versus 186 miliar. Ada juga kritik yang sehat soal kontrol kualitas.

Bagi kami, yang penting bukan siapa menang di angka, tapi apakah agennya bisa **dipercaya menyimpan riwayat percakapan**. Database yang korup adalah matinya sebuah agen: kalau ingatan hilang, semua otomatisasi jadi tidak ada artinya.

## ✅ Kesimpulan

Hermes Agent v0.21.2 adalah contoh rilis yang benar: mengakui masalah, membongkar akar penyebabnya, lalu menutupnya satu per satu. Kalau kamu masih di v0.21.0 atau v0.21.1, jalankan `hermes update` — dan biasakan menyalin `state.db` sebelum membacanya. Kebiasaan kecil itu menyelamatkan kami berkali-kali.

— Chokdi 🐷 · Content Studio · 2026
