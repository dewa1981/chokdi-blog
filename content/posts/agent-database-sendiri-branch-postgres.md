---
title: "Setiap Agent Punya Database Sendiri: Pelajaran dari 7 Produk Postgres dalam 30 Hari"
date: 2026-10-02T07:30:00+07:00
draft: false
tags: ["PostgreSQL", "AI Agent", "DevOps", "Database", "Open Source"]
---

Satu orang meluncurkan **7 produk PostgreSQL open-source dalam 30 hari** dan mengumpulkan 2.000+ bintang GitHub. Namanya Alex Shapalov, dan tweet-nya diakhiri dengan satu kalimat jujur: *"I might have a Postgres problem."* 🐘

Tapi di balik lelucon itu ada satu produk yang serius: **pgrun** — yang menjawab masalah yang hampir semua tim AI agent hadapi hari ini, dan sering tidak disadari sampai terlambat.

## Masalahnya: Satu Staging untuk 20 Agent

Kalau kamu punya agent AI yang bisa nulis kode, jalankan migrasi, dan test sendiri, kamu akan cepat ketemu tembok ini:

```
agent-1 ─┐
agent-2 ─┼→ staging   ← semua rebutan satu DB
agent-3 ─┘
```

Akibatnya bisa ditebak: migrasi tabrakan, test saling mengotori state, dan cleanup jadi pekerjaan baru yang tidak ada yang mau memiliki. Kalau satu agent lagi nge-test sambil agent lain ngubah skema, hasilnya bukan bug di kode — tapi **pengaruh silang** yang susah dilacak.

Yang lebih menakutkan: sering kali "satu staging" itu ternyata **produksi yang disamarkan**. Agent jalan migrasi langsung ke database yang dipakai user.

## Jawabannya: Branch, Bukan Salinan

pgrun mengambil pendekatan yang mirip `git branch`, tapi untuk database:

```
agent-1 → branch-1
agent-2 → branch-2
agent-3 → branch-3
```

Setiap agent, setiap pull request, dan setiap job CI dapat **Postgres-nya sendiri** — isolated dan *disposable*. Selesai kerja, hapus. Tidak ada state nyangkut, tidak ada job cleanup.

Yang membuat ini menarik secara teknis: **pgrun tidak menyalin datanya.**

Pertanyaan yang sering muncul: *"Bagaimana bisa 100 GB Postgres disalin dalam hitungan detik?"* Jawabannya: **tidak disalin.** pgrun memakai **Copy-on-Write (CoW)** — branch baru berbagi blok disk yang sama dengan sumbernya, dan hanya menyimpan bagian yang berubah. Kalau agent cuma menyentuh 200 MB dari 100 GB, yang disimpan cuma 200 MB itu.

### Angka di balik layar

Versi 2.0 dari pgrun memecah prosesnya jadi beberapa tahap, dan tiap tahap diukur:

| Tahap | Waktu (p50) |
|---|---|
| Snapshot filesystem | **22 ms** |
| Clone snapshot | **31 ms** |
| Postgres startup | **80 ms** |
| `DATABASE_URL` siap dipakai | **1,36 detik** |

Sebelum optimasi, `DATABASE_URL` butuh 4,88 detik. Sekarang **1,36 detik** — tiga kali lebih cepat. Dan yang paling penting: **tidak ada proses copy database** di jalur kritisnya.

## Tiga Jaminan yang Bikin Ini Layak Dipakai di Produksi

Yang membedakan pgrun dari "sekadar bikin DB baru" adalah tiga jaminan ini:

**1. Kredensial produksi tidak pernah sampai ke agent.**
Kamu connect database produksi **sekali** saja. Setelah itu agent hanya menerima `DATABASE_URL` milik branch-nya sendiri. Kredensial asli tetap di tempatnya.

**2. Data sensitif bisa di-mask sebelum masuk branch.**
Kolom yang terdeteksi sensitif bisa disamarkan sebelum branch dibuat. Artinya kamu bisa kasih agent data "berbentuk seperti asli" tanpa membocorkan isi sebenarnya.

**3. Branch itu sekali pakai.**
Setiap branch terisolasi dan menghapusnya gratis — tidak ada biaya, tidak ada sisa state.

## Yang Paling Sederhana Justru yang Paling Penting

pgrun tidak menciptakan API database baru. Tidak ada query language khusus, tidak ada ORM wajib.

Yang dikembalikan ke kamu cuma satu hal: **connection string Postgres biasa.**

```
DATABASE_URL=postgres://…
```

Artinya Rails, Django, Prisma, Drizzle, pgx, `psql` — semua yang sudah kamu pakai **tidak perlu tahu apa-apa**. Tidak ada perubahan kode. Itu keputusan desain yang bagus: tool yang memaksa kamu ganti cara kerja akan ditinggalkan, tool yang menyisipkan diri tanpa terasa akan dipakai terus.

## Enam Produk Lainnya (Bonus)

Pgrun bukan satu-satunya. Dari 7 produk itu, beberapa layak dicatat:

| Produk | Isi |
|---|---|
| **pgbot.dev** | "Postgres intelligence for AI agents." Tanya pakai bahasa manusia, dapat diagnosa — bukan dashboard. Binary-nya **5,9 MB**, **read-only by construction** (agent tidak bisa merusak apa pun). Punya **MCP stdio**, jadi bisa langsung dipasang sebagai tool agent |
| **pgterm.dev** | Terminal Postgres (GUI) ditulis pakai **Rust** 🦀. Monitoring & stats — sengaja **tidak** membaca isi tabel |
| **pglogs.dev** | Stream & filter log database. Setiap query, warning, dan error diketik saat terjadi — format terbaca manusia **dan** AI agent |
| **pggo.dev** | Driver Postgres untuk Go. **1,7 MB, zero dependencies** — dioptimalkan untuk agent, CLI, dan binary kecil |
| **pgbook.dev** | Belajar Postgres |
| **pg???** | "Postgres in seconds" (masih WIP) |

Ada satu pola yang konsisten di semua produk ini: **ukuran kecil, dependensi minimal, output yang bisa dibaca mesin.** Itu bukan kebetulan — itu desain yang sengaja dibuat untuk dikonsumsi agent, bukan cuma manusia.

## Hubungannya dengan Cara Kami Menjaga Database

Kami sendiri sudah lebih dulu serius di sisi *backup*: PostgreSQL kami jalankan **PITR + WAL streaming dengan Databasus**, supaya kalau database korup jam 14:37, kami bisa balik ke 14:36 — bukan ke dump terakhir jam 03:00. Itu sisi **keselamatan data**. Baca: [Backup PostgreSQL Sampai ke Detik](/posts/postgres-pitr-wal-streaming-databasus/).

Tapi ada satu lubang yang PITR tidak menutup: **kalau kamu butuh database untuk berbuat kesalahan.** Test migrasi, uji skema baru, jalanin agent yang belum terbukti — semua itu butuh database, dan biasanya yang dipakai adalah staging bersama (atau lebih buruk: produksi).

Pgrun dan PITR itu dua hal yang berbeda dan saling melengkapi:

| | PITR (yang kami pakai) | Branch CoW (pola pgrun) |
|---|---|---|
| Tujuan | Memulihkan setelah bencana | Memberi ruang untuk mencoba |
| Arah | Mundur ke masa lalu | Bercabang dari sekarang |
| Jumlah | Satu riwayat | 1000+ branch paralel |
| Biaya | Streaming WAL terus-menerus | ~1,4 detik per branch |

PITR melindungi database dari **kecelakaan**. Branch melindungi database dari **eksperimen**. Kalau kamu punya agent AI yang jalan sendiri, kamu butuh keduanya.

## Pelajaran yang Bisa Dipakai Hari Ini

Kalau kamu tidak bisa langsung pasang pgrun (misalnya karena database-mu MariaDB, bukan Postgres — seperti punya kami), tiga prinsip ini tetap bisa dipakai:

**1. Jangan pernah beri agent kredensial produksi.**
Ini bukan soal paranoid. Ini soal membatasi kerusakan maksimum kalau agent salah. Pola "connect sekali, agent cuma dapat credential cabang" itu bisa ditiru manual.

**2. Eksperimen harus punya tempat pembuangan sendiri.**
Aturan sederhana: kalau sebuah perubahan belum terbukti, dia tidak boleh menyentuh database yang dipakai orang. Sediakan jalur khusus untuk "berbuat salah".

**3. Ukur jalur kritisnya, jangan cuma totalnya.**
Pgrun memecah 1,36 detik jadi 22 ms + 31 ms + 80 ms + sisanya. Itu yang membuat mereka tahu bagian mana yang harus dipercepat. Kalau sistemmu cuma punya satu angka "lambat", kamu tidak akan tahu apa yang harus diperbaiki.

## Penutup

Yang menarik dari gelombang produk ini bukan teknologinya — snapshot filesystem itu sudah ada sejak lama. Yang baru adalah **asumsinya**: alat-alat ini dibangun dengan asumsi bahwa *agent akan membuat database lebih banyak dalam sehari daripada yang dibuat manusia dalam setahun*.

Kalau asumsi itu benar untukmu, maka satu staging bersama bukan lagi solusi. Itu bottleneck.

Kalau kamu penasaran: pgrun ada di [pgrun.dev](https://pgrun.dev), pgbot di [pgbot.dev](https://pgbot.dev), dan semua produknya open source.

Kalau kami di Chokdi mau nyoba pola ini untuk FastGaji (MariaDB), tantangan pertamanya bukan software-nya — tapi **filesystem-nya**: CoW seperti ini butuh ZFS atau LVM, dan itu harus dicek dulu sebelum dijanjikan. Tapi itu cerita lain.

— Chokdi 🐷 · Content Studio · 2026
