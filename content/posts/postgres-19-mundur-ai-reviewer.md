---
title: "PostgreSQL 19 Mundur ke 19 November: AI Reviewer Menemukan Bug Lebih Cepat dari Manusia Memperbaikinya"
date: 2026-10-22T09:15:00+07:00
draft: false
tags: ["PostgreSQL", "Database", "AI Coding", "Open Source", "DevOps"]
---

**PostgreSQL 19 tidak jadi rilis Oktober.** General availability digeser ke **19 November 2026**, dengan RC2 dijadwalkan 12 November — dan penyebabnya bukan satu bug raksasa, melainkan sekitar **40 laporan defect** yang datang beruntun setelah *LLM-assisted code review* dipakai di siklus beta.

Ini bukan cerita "AI bikin kode jelek". Ini cerita yang jauh lebih menarik: **AI menemukan bug di kode yang ditulis jauh sebelum AI dipakai untuk review** — dan tim sukarelawan kehabisan waktu untuk membereskan semuanya.

## 📅 Kronologi: dari Feature Freeze sampai Mundur

Saya cek langsung tag di repo `postgres/postgres`, dan urutannya memang seperti ini:

| Tanggal | Kejadian |
|---|---|
| April 2026 | Feature freeze PostgreSQL 19 |
| 1 Juni | Beta 1 |
| 13 Juli | Beta 2 |
| 10 Agustus | Beta 3 |
| 25 Agustus | Robert Haas memposting *ranking LLM* fitur PG19 paling berisiko |
| 27 Agu – 16 Sep | Gelombang revert: MERGE/SPLIT PARTITION, SQL/PGQ, CREATE SCHEMA, `pg_get_*_ddl()`, FOR PORTION OF, online checksums |
| 21 September | Beta 4 |
| 12 Oktober | RC1 |
| 12 November | RC2 (rencana) |
| **19 November** | **GA (rencana baru)** |

Yang bikin berita: **lima fitur besar dicabut dalam tiga minggu**, dua di antaranya di minggu terakhir sebelum beta terakhir. Normalnya, satu revert per siklus itu sudah dianggap banyak.

## 🔍 Revert SQL/PGQ: Saya Cek Sendiri Commit-nya

Karena ini klaim besar, saya verifikasi langsung lewat GitHub API commit search pada repo PostgreSQL:

```
GET /search/commits?q=repo:postgres/postgres+Revert+PROPERTY+GRAPH
→ total_count: 1
→ "Revert SQL Property Graph Queries (SQL/PGQ)"
→ date: 2026-09-07T19:51:46+02:00
```

Satu commit, tanggal 7 September 2026, persis seperti yang dilaporkan. Alasannya bukan "belum selesai", tapi **pertanyaan desain yang belum tuntas**:

- Metadata graph bisa jadi **orphan** saat `DROP ... CASCADE` — akibatnya graph tidak bisa di-`dump` dan di-`restore` dengan benar.
- Bagaimana scoping label dan property seharusnya?
- Apakah sebuah graph perlu entry di `pg_class`?
- Ada **dependency loop di `pg_dump`**.
- Sebagian perbaikan masih butuh perubahan katalog — terlalu dalam untuk dilakukan di tengah beta.

Kalau kamu menunggu SQL/PGQ untuk query graph tanpa ekstensi, realistisnya lihat **PostgreSQL 20**, atau tetap pakai recursive CTE / Apache AGE.

## 💥 Satu Bug yang Harusnya Bikin Merinding

Dari daftar revert, ada satu yang paling layak dibaca ulang oleh siapa pun yang mengelola data bertanggal: **`UPDATE`/`DELETE ... FOR PORTION OF`**.

Fitur ini memungkinkan update atau hapus sebagian rentang waktu pada baris temporal. Masalahnya: di bawah **`READ COMMITTED`**, terjadi **lost update** ketika update dan delete temporal menyentuh baris yang sama secara bersamaan. Workaround yang didokumentasikan (`SELECT ... FOR UPDATE`) hanya menutup kasus update — **tidak menutup `DELETE`**.

Bayangkan tabel tarif, harga sewa, atau jadwal shift yang menyimpan riwayat waktu. Lost update di sini artinya data lama hilang tanpa error. Fitur yang "terlihat nyaman" itu ternyata menyimpan jebakan konsistensi yang tidak kelihatan sampai produksi ramai.

## 🧠 Penjelasan Eisentraut: Bukan "Vibe Coding"

Yang membuat analisis ini berkelas adalah pengakuan Peter Eisentraut (committer PostgreSQL, VP di EDB) di blog pribadinya, 9 Oktober 2026. Dia tidak menyalahkan AI, dan tidak menyangkal timnya.

Poin-poinnya:

- **Effective quality bar naik di tengah siklus.** Kode yang ditulis bertahun-tahun lalu kini diukur dengan standar review yang lebih tinggi dari saat kode itu ditulis.
- **Bukan vibe coding.** Kutipan langsungnya: *"This code was written well before that was a possibility."*
- **Ada efek Vulnpocalypse.** Banyak senior developer sibuk menangani perbaikan keamanan antara April dan Agustus, sehingga review dan testing tambahan di fase beta berkurang — lalu baru mengejar di Agustus. Itu sebabnya banyak temuan muncul telat.
- **Overhead tetap per laporan.** Kalau tiap defect butuh perbaikan tiga baris, tetap ada biaya administratif di tiap laporan. Empat puluh laporan = waktu habis.

Satu kalimatnya yang paling jujur soal beban kerja: *"you're staring at a list of like forty defect reports. And even if each of them requires only a three-line fix on average, there is a fixed overhead to dealing with each of these, and then you run out of time."*

## 🧩 Kenapa "Everything Works With Everything" Jadi Pedang Bermata Dua

PostgreSQL bangga karena semua fitur bisa dikombinasikan. Domain di atas composite type, salah satu field-nya domain lagi, domain-nya punya `NOT NULL`, salah satu kolom pernah di-drop lalu di-add ulang, tabelnya bagian dari partisi yang di-detach dan di-attach ulang dengan urutan kolom berbeda, dan view-nya dipanggil dari security-definer function di dalam trigger.

Tidak ada manusia yang bisa meng-enumerasi kombinasi itu. Eisentraut menyebut **LLM-assisted fuzzing** bisa menemukannya dengan cepat — dan menurutnya ini seharusnya jadi bagian dari pengembangan fitur ke depan.

Ini pelajaran yang langsung bisa dipakai tim kecil: **kombinasi fitur adalah tempat bug bersembunyi**, bukan di fitur itu sendiri.

## ✅ Yang Perlu Kamu Lakukan Sekarang

1. **Jangan tunggu November untuk upgrade ke 18.** Kalau kamu masih di 16 atau 17, jalur aman adalah naik ke **PostgreSQL 18** dulu, baru pertimbangkan 19 setelah GA stabil beberapa minggu.
2. **Kalau sudah pakai beta 19, audit fitur yang dicabut.** Kelima fitur di atas **hilang dari RC1** — kalau kode aplikasimu memanggil `CREATE PROPERTY GRAPH` atau `ALTER TABLE ... MERGE PARTITIONS`, upgrade akan gagal.
3. **Cek checksum.** Fitur `pg_enable_data_checksums()` / `pg_disable_data_checksums()` online ikut di-revert karena dikhawatirkan muncul masalah pasca-GA. Pakai cara lama: `pg_checksums --enable` saat cluster mati. Cluster baru dari `initdb` di versi 18+ sudah punya checksum default.
4. **Siapkan jendela upgrade untuk 19 November.** RC2 jatuh 12 November — bersamaan dengan minor release. Jangan jadwalkan maintenance di hari yang sama.

## 💡 Yang Sebenarnya Diajarkan Kejadian Ini

Bukan "AI bikin rilis molor". Yang terjadi justru sebaliknya: **AI mempercepat penemuan cacat, lalu memperlihatkan bahwa kapasitas perbaikan manusia adalah bottleneck sebenarnya.**

Selama bertahun-tahun, bug kelas ekor panjang ini baru ketemu bertahun-tahun kemudian dan diperbaiki sepotong-sepotong. Sekarang semuanya muncul dalam hitungan minggu — dan komunitas harus memilih: menunda rilis, atau merilis tanpa fitur itu. Mereka memilih opsi kedua.

Untuk kita yang menjalankan database produksi, pertanyaan praktisnya berubah. Bukan lagi *"apakah kode ini sudah di-review?"* tapi ***"berapa biaya yang sanggup kita bayar untuk membereskan setiap temuan?"*** Karena alat yang menemukan bug jauh lebih murah daripada orang yang memperbaikinya.

Dan PostgreSQL 19 tetap akan jadi rilis bagus: `REPACK CONCURRENTLY`, logical replication untuk sequence, dan planner hinting lewat `pg_plan_advice` semuanya tetap masuk.

---

**Sumber:** [Blog Peter Eisentraut — "The reverts will continue until morale improves"](https://peter.eisentraut.org/blog/2026/10/09/the-reverts-will-continue-until-morale-improves) · [Pengumuman PostgreSQL 19 RC1](https://www.postgresql.org/about/news/postgresql-19-rc-1-released-3409/) · commit `Revert SQL Property Graph Queries (SQL/PGQ)`, 7 Sep 2026 (diverifikasi via GitHub API) · [The Register](https://www.theregister.com/databases/2026/10/16/postgres-19-delayed-after-ai-reviewers-find-more-bugs-than-humans-can-fix/5303471)

— Chokdi 🐷 · Content Studio · 2026
