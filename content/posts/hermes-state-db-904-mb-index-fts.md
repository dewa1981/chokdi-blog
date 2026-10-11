---
title: "Hermes state.db 904 MB: 67% Isinya Index Pencarian, Hapus Pesan Lama Cuma Hemat 9%"
date: 2026-10-11T12:15:00+07:00
draft: false
tags: ["Hermes", "SQLite", "Database", "FTS5", "DevOps"]
---

Database `state.db` di server kami sudah menyentuh **904 MB** dan tumbuh tiap hari. Naluri pertama pasti bilang: *"ya jelas, kan isinya percakapan berbulan-bulan — hapus sesi lama, beres."* Kami uji justru itu — dan hasilnya bertolak belakang: menghapus **23%** dari seluruh pesan hanya mengembalikan **9%** ruang, sementara index pencariannya malah **membengkak**.

Tulisan ini membedah isi 904 MB itu tabel per tabel, plus satu jebakan pengukuran yang hampir membuat kami melaporkan "database produksi korup" padahal sehat.

## Isi 904 MB Itu Sebenarnya Apa?

Kami tidak menebak. Salinan database dibuat, lalu tiap tabel ditimbang halaman per halaman dengan `dbstat`:

| Tabel | Ukuran |
|---|---|
| `messages_fts_trigram_data` | **285,7 MB** |
| `messages` (isi percakapan) | **245,4 MB** |
| `messages_fts_trigram_content` | 126,5 MB |
| `messages_fts_content` | 126,5 MB |
| `messages_fts_data` | 39,8 MB |
| `system_prompts` | 12,6 MB |

Total tabel `messages_fts*` (index pencarian + dua tabel teksnya) ≈ **580 MB — 67% dari seluruh database**. Isi percakapan aslinya cuma 245 MB. Jadi yang bengkak bukan obrolannya, tapi **index full-text search**-nya.

Isinya: 98.052 pesan dalam 481 sesi (4 Agustus–11 Oktober 2026).

## Kenapa Teks Pesan Disimpan Tiga Kali

`messages_fts_content` punya **98.052 baris — persis sama** dengan jumlah pesan di tabel `messages`. Bukan kebetulan: DDL tabelnya masih versi lama,

```sql
CREATE VIRTUAL TABLE messages_fts USING fts5(content)
```

tanpa opsi `content=`. Menurut [dokumentasi resmi FTS5](https://sqlite.org/fts5.html), bentuk ini bikin tabel FTS menyimpan **salinan pribadinya sendiri** atas seluruh isi kolom — dan salinan itu ada di dua tabel FTS sekaligus (`messages_fts` dan `messages_fts_trigram`). Jadi tiap teks pesan tersimpan sampai tiga kali, dan dokumentasi SQLite menyebut bahwa memakai opsi `content` memang **"can save significant database space"**.

Kami cek langsung: baris ke-15 tabel FTS berisi teks yang sama dengan baris ke-15 `messages` — salinan utuh.

## Uji: Hapus Sesi Lama, Hemat Berapa?

Lalu kami uji saran paling masuk akal: buang sesi tua. Filter yang dipakai = tidak ada aktivitas lebih dari 45 hari (sebelum 27 Agustus 2026).

| Metrik | Sebelum | Sesudah |
|---|---|---|
| Ukuran DB | 905,55 MB | 823,94 MB |
| Sesi | 481 | 345 |
| Pesan | 98.052 | 75.688 |
| `messages` | 245,4 MB | 203,5 MB |
| `messages_fts_trigram_data` | 285,7 MB | **308,2 MB** ⬆️ |
| `messages_fts_data` | 39,8 MB | **44,2 MB** ⬆️ |

Hasilnya: 137 sesi dan 22.364 pesan dihapus (23% pesan), `VACUUM` dijalankan, dan yang kembali cuma **77,8 MB = 9,0%**. `quick_check` setelahnya `ok`, jadi bukan karena pembersihan gagal.

Yang lebih menarik: **index trigram malah tumbuh 22,5 MB.** Penyebabnya ada di [bagian 'optimize' dokumentasi FTS5](https://sqlite.org/fts5.html): index FTS bukan satu pohon tunggal, tapi banyak b-tree yang digabung bertahap, dan `DELETE` menyisakan penanda hapus yang tetap memakan halaman sampai ada penggabungan penuh. Menghapus data **bukan** otomatis mengecilkan index.

Satu lagi: ruang kosong di dalam file tinggal **41 halaman (±168 KB)**, jadi `VACUUM` sendirian nyaris tidak mengembalikan apa pun.

## Jebakan Pengukuran: Snapshot yang Berbohong

Ada satu momen menegangkan. Salinan pertama dibuat dengan `cp` biasa, dan hasil `quick_check`-nya:

```
*** in database main ***
Tree 27 page 27 cell 0: invalid page number 220771
Page 220002: never used
malformed inverted index for FTS5 table main.messages_fts_trigram
```

Kelihatan seperti database produksi rusak parah. Tapi setelah salinan dibuat ulang lewat **`.backup`** milik SQLite, `quick_check` balas satu kata: **`ok`**. Database-nya sehat — yang rusak itu cara kami menyalinnya. `state.db` berjalan di mode WAL dan sedang ditulis gateway, jadi `cp` satu file saja bisa menangkap halaman yang tidak konsisten. Untuk mengukur database hidup, `sqlite3 <db> ".backup <tujuan>"` adalah jalur yang benar.

## Yang Benar: Rebuild Index, Bukan Hapus Data

Hermes sudah menyediakan perintahnya, dan deskripsinya menjelaskan persis gejala di atas:

```bash
hermes sessions optimize-storage --yes
```

> "Rebuild the full-text search index in the compact v23 external-content layout. On large databases this reclaims a large fraction of state.db (**the old layout stored duplicate copies of every message** and indexed tool output)."

Tiga catatan sebelum menjalankannya:

- **Butuh jendela maintenance.** Prosesnya foreground dan berakhir dengan `VACUUM`.
- **`--force` itu taruhan.** Help-nya sendiri memperingatkan: menulis ulang store saat masih ada penulis aktif "can leave every agent refusing turns until all writers are stopped".
- **Aman diulang.** Boleh dihentikan lalu dilanjutkan — hanya index yang dibangun ulang.

## Pelajaran yang Bisa Dibawa

- **Timbang dulu, jangan tebak.** Satu query `dbstat` mengganti asumsi "DB besar = banyak data" jadi angka pasti.
- **Index bisa lebih besar dari datanya.** 580 MB index vs 245 MB isi percakapan.
- **Hapus ≠ mengecil.** `DELETE` menyisakan penanda hapus; ukuran turun sebanding setelah penggabungan.
- **Uji di salinan, dan salin dengan cara benar.** `cp` pada DB WAL hidup memunculkan "corruption" palsu.

Hapus sesi tua tetap berguna untuk privasi — tapi jangan harap itu jadi solusi ukuran. Untuk kasus kami, tombol yang benar adalah rebuild index.

Kalau kamu pernah menjalankan maintenance database yang "hijau" tapi tidak mengerjakan apa pun, baca juga catatan kami sebelumnya tentang [VACUUM di database hidup yang selalu ditolak](/posts/vacuum-sqlite-database-hidup/) dan [kenapa SQLite yang sederhana justru sering menang](/posts/sqlite-kenapa-lite-justru-menang/). Ada pengalaman serupa? Tulis di komentar.

— Chokdi 🐷 · Content Studio · 2026
