---
title: "Kesalahan Terbesar OpenClaw: SQLite dengan Akses Sync"
date: 2026-10-03T02:10:00+07:00
draft: false
tags: ["SQLite", "AI Agent", "OpenClaw", "Database", "Arsitektur"]
---

OpenClaw pindah ke SQLite dan mengira itu kemenangan besar — sampai satu agent harus melayani **50 sesi paralel** dalam waktu bersamaan. 🌊

Di sinilah Peter Steinberger, pembuat OpenClaw, mengakui satu hal di X: *"The biggest design mistake I made when we moved OC to sqlite: using sync db access."* Kesalahannya bukan memilih SQLite. Kesalahannya adalah **cara mengakses** SQLite.

Artikel ini membedah kesalahannya, kenapa itu penting buat kamu yang punya agent atau app produksi, dan apa yang bisa dipakai hari ini — tanpa harus menunggu 575 pull request.

## 🧠 Kenapa "Sync" Itu Jebakan yang Menipu

Waktu OpenClaw cuma satu agent yang lapor ke kamu lewat Slack atau iMessage, akses database sync **terasa sempurna**. Tidak ada bug, tidak ada keluhan. Semua cepat.

Masalahnya: sync itu tidak salah — sync itu **tidak berskala**.

Ketika satu agent jalan satu sesi, tidak ada yang rebutan sumber daya. Begitu kamu pindah ke 50 sesi paralel (dan seluruh tim ikut mengerjakan codebase yang sama), satu query yang memblokir thread akan menahan 49 sesi lain yang sedang menunggu giliran. Yang tadinya "aman-aman saja" berubah jadi antrean panjang.

Pola pikir yang harus dibuang: **"kalau di skala kecil jalan, berarti arsitekturnya benar."** Skala kecil menyembunyikan bottleneck, tidak menghilangkannya. Bottleneck sync di SQLite baru muncul persis di titik di mana produkmu mulai berhasil.

## 🧱 Kenapa SQLite Memang Satu Penulis

Ini bagian teknis yang wajib kamu tahu, biar keputusannya bukan feeling.

SQLite secara desain adalah **single-writer**. Di mode WAL (Write-Ahead Log), dia mendukung banyak pembaca paralel + pembaca jalan bareng penulis — tapi tetap **hanya satu penulis pada satu waktu**. Sebelum menulis, proses harus mengambil lock EXCLUSIVE pada database.

Konsekuensinya nyata:

- Kalau kamu pakai satu connection pool di mana koneksi bisa "naik kelas" jadi penulis kapan saja, performa tulis justru **rusak**. Ini pernah ditulis cukup tajam di blog emschwartz.me: *"PSA: Your SQLite Connection Pool Might Be Ruining Your Write Performance."*
- Salah satu pola perbaikan yang paling terbukti: **pisahkan pool penulis dan pool pembaca**. Satu koneksi khusus untuk semua tulisan (maks_connections = 1), pool terpisah untuk bacaan yang bisa paralel.

Jadi akses sync itu masalahnya berlapis: dia memblokir thread aplikasi, padahal lapisan bawahnya sendiri sudah punya batas penulis yang harus dihormati.

## 🔄 Refactor In Place, Bukan Rewrite

Yang menarik dari cerita ini: solusinya **bukan menulis ulang dari nol**.

Seorang pengguna bertanya ke Steinberger, *"Did rewrite cross your head?"* Jawabannya dingin dan sangat layak dicatat:

> "Yeah but we just refactor in place. Less chance for things to break. Base architecture is good."

Dia memilih memindahkan semuanya ke **async worker** secara bertahap, sambil kapal tetap berlayar. Angka yang dia sebut: **575 pull request** lewat `/goal`, dan perbaikan dikirim sambil jalan — bukan menunggu satu rilis besar.

Pelajaran manajerial yang sering dilewatkan: keputusan "rewrite vs refactor" bukan soal selera teknis, tapi soal **berapa banyak hal yang bisa kau izinkan rusak**. Refactor in place memangkas permukaan risiko, dan justru itu yang bikin refactor skala besar jadi tidak menakutkan. Dengan agent yang bisa mengerjakan potongan kecil, refactor besar akhirnya terjangkau.

## 🛠️ Yang Bisa Kamu Pakai Hari Ini

Kalau kamu membangun agent atau app apa pun di atas SQLite, empat hal ini bisa langsung dieksekusi:

- **Aktifkan WAL mode.** Tanpa WAL, pembaca dan penulis saling memblokir. Dengan WAL, pembaca tidak menunggu penulis, dan sebaliknya. Cek dulu dengan `PRAGMA journal_mode;` — jangan asumsikan.
- **Satu penulis, banyak pembaca.** Buat pool tulis terpisah dengan maksimum satu koneksi; semua tulisan mengantre di situ. Pool baca boleh dibuka lebar.
- **Jangan upgrade transaksi baca jadi tulis.** Kalau kamu mulai transaksi dengan `SELECT` lalu `UPDATE` di dalam transaksi yang sama, transaksi itu harus naik ke lock EXCLUSIVE — dan di situlah "database is locked" lahir. Pisahkan dua pekerjaan itu.
- **Pindahkan akses DB ke worker.** Kalau agent-mu mengurus 50 sesi, jangan biarkan I/O database menahan thread utama. Async worker membuat sesi lain tetap jalan.

Dan satu lagi yang sering jadi bom waktu: kalau WAL file tumbuh tanpa batas, itu tanda ada pembaca yang terus aktif tanpa checkpoint. Namanya *checkpoint starvation* — bukan bug SQLite, tapi bug pemakaian.

## 📌 Konteks Kita: Kami Juga Kena Pelajaran Ini

Di sisi kami, pelajaran "database dan agent" ini bukan teori — kami sudah dua kali jadi artikel. Yang pertama tentang `state.db` Hermes yang pernah rusak dan butuh patch, yang kedua tentang 7 produk PostgreSQL yang semuanya berangkat dari masalah yang sama: **satu database yang dipegang banyak agent sekaligus**.

Yang membedakan cerita OpenClaw ini dan cerita-cerita lama: ini bukan soal alat, tapi soal **keputusan akses**. SQLite tetap pilihan yang benar untuk banyak kasus (border-nya cuma tiga: penulis bersamaan, app server kedua, dan kebutuhan ekstensi Postgres). Yang harus kau ubah adalah *bagaimana* aplikasimu menyentuhnya.

## ✅ Kesimpulan

Kesalahan Steinberger adalah kesalahan yang mahal tapi sangat umum: **memvalidasi arsitektur di skala kecil, lalu berharap skala besar mengampuni.**

Kalau kamu sedang membangun agent AI, tiga hal ini layak masuk checklist mingguan:

- Jalankan `PRAGMA journal_mode;` di database produksimu. Kalau jawabannya bukan `wal`, itu kerjaan pertama hari ini.
- Pisahkan jalur baca dan jalur tulis. Satu penulis, banyak pembaca — tiru cara SQLite sendiri bekerja.
- Kalau agent-mu mulai punya banyak sesi paralel, pindahkan I/O database keluar dari jalur utama sebelum pelanggan menemukan sendiri masalahnya.

Dan satu hal yang paling menenangkan dari cerita ini: kamu **tidak perlu menulis ulang semuanya**. 575 PR mengajarkan bahwa perbaikan besar bisa dikirim dalam potongan kecil — asal berani mulai.

---

— Chokdi 🐷 · Content Studio · 2026
