---
title: "VACUUM SQLite di Database Hidup: Kenapa Selalu Ditolak & Cara Benar Pakai VACUUM INTO"
date: 2026-10-02T18:20:00+07:00
draft: false
tags: ["SQLite", "Database", "DevOps", "Cron", "Monitoring"]
---

Job maintenance yang paling menipu bukan yang merah — tapi yang **hijau padahal tidak mengerjakan apa pun**. Itu yang kami temukan hari ini di server produksi: sebuah cron `optimize` SQLite yang jalan 14 kali, ditolak 114 kali, dan tetap keluar dengan exit code `0`. Tulisan ini membedah kenapa SQLite (dan Hermes) menolak men-VACUUM database yang sedang dipakai, lalu cara benar melakukannya tanpa mematikan aplikasi.

## Gejala: 38 Database, 14 Run, Nol Pekerjaan

Script `optimize-state-weekly.sh` dijadwalkan `0 4 * * 1,3,5` (Senin/Rabu/Jumat 04:00) dan menggilir **37 database profil + 1 database utama**. Log-nya bicara sendiri:

| Metrik | Angka |
|---|---|
| Baris `=== <tanggal> ===` (jumlah run) | 14 |
| Baris `Refusing ... another process is using` | 114 |
| Baris sukses optimize | 0 |
| Exit code wrapper terakhir | **0** |

Jadi selama berbulan-bulan, tidak sekali pun FTS-optimize atau VACUUM benar-benar jalan — tapi dashboard job-nya bersih. Pelajaran pertamanya bukan soal SQLite, tapi soal **sinyal**: script yang tidak pernah mengembalikan status gagal akan selalu terlihat sehat.

## Kenapa SQLite Menolak: Lock, Bukan Bug

Menurut dokumentasi resmi [VACUUM](https://sqlite.org/lang_vacuum.html), perintah ini **menulis** ke database: dia membangun ulang file, merapatkan halaman, dan membuang ruang kosong. Karena itu: *"VACUUM (but not VACUUM INTO) is a write operation and so if another database connection is holding a lock that prevents writes, then the VACUUM will fail."*

Di server kami, yang memegang lock itu bukan pengguna nakal — tapi gateway Hermes sendiri. Setiap profile punya proses `gateway run` yang memegang `state.db`, `state.db-shm`, dan `state.db-wal`. Selama 38 gateway hidup, tidak ada jendela lock untuk VACUUM klasik.

## Kalau Dipaksa `--force`, Ini Taruhannya

Hermes sendiri memberi jalur pintas `hermes sessions optimize --force`, lengkap dengan peringatan yang jujur:

> "Run even while another Hermes process (gateway, Desktop, dashboard, cron) holds state.db — rewriting the store under a live writer can leave **every agent refusing turns** until all writers are stopped."

Tool yang dipakai lintas-agent tidak boleh mengorbankan dirinya sendiri demi hemat disk. Rewrite file di bawah writer aktif = jalan pintas menuju `state.db-wal` yang rusak, dan itu pernah terjadi di sini. Makanya guard-nya sengaja ketat.

## Cara Benar #1: `VACUUM INTO` (Aman di Database Hidup)

Dokumen SQLite menyebut opsi yang jarang dipakai orang: **`VACUUM INTO 'file-baru.db'`**. Bedanya besar:

- Database asli **tidak disentuh** — hasilnya file baru yang sudah ter-vacuum.
- Aman dijalankan pada **database yang hidup**; dokumentasi menyebutnya *"an alternative to the backup API for generating backup copies of a live database"*.
- Hasilnya paling kecil karena semua halaman kosong dibuang, plus **menghapus jejak data yang sudah dihapus** (berguna kalau isi DB pernah memuat kredensial).
- Syaratnya satu: file target **belum ada atau kosong** — kalau tidak, perintahnya gagal.

Untuk database utama kami yang 767 MiB dengan WAL sekitar 5,8 MB, pola ininya: `VACUUM INTO` ke file baru → cek ukuran + `PRAGMA integrity_check` → baru tukar nama file di jendela sepi. Tidak ada lock panjang, tidak ada downtime.

## Cara Benar #2: Cek Dulu, Apakah Perlu VACUUM?

VACUUM itu operasi mahal. Ukur dulu, jangan tebak — dan ukur dari **salinan**, bukan dari file hidup:

```sql
PRAGMA journal_mode;    -- wal
PRAGMA page_size;       -- 4096
PRAGMA page_count;      -- total halaman
PRAGMA freelist_count;  -- halaman kosong
```

Rasio `freelist_count / page_count` itulah "sampah" database. Contoh nyata: satu `state.db` profile di sini cuma 87 halaman dengan `freelist_count = 0` — VACUUM di situ murni buang waktu. Sebaliknya, store besar yang tiap hari append + hapus sesi pasti punya banyak halaman bebas.

## Tiga Aturan Sebelum Menjadwalkan Maintenance DB Hidup

1. **Bedakan operasi tulis dan baca.** VACUUM butuh lock tulis; `VACUUM INTO`, online backup API, dan `sqlite3 .backup` dirancang untuk DB hidup. Pilih sesuai apakah kamu boleh memblokir penulis.
2. **Jangan jadwalkan di jam gateway hidup lalu berharap keajaiban.** Pindahkan ke jendela sepi (stop → optimize → start per profile), atau pakai pola copy-swap.
3. **Perbaiki sinyalnya, bukan hanya jadwalnya.** Kalau script menggilir 38 database, dia harus gagal kalau 38-nya ditolak — bukan menutup dengan `--- done ---`. Silent failure seperti ini sudah pernah kami bahas di [Cron Job Bilang OK Tapi Bohong](/posts/cron-job-bilang-ok-tapi-bohong/) dan polanya berulang: job hijau, kerjaan nol.

## Kesimpulan

Menolak VACUUM di database hidup itu **fitur**, bukan bug — dan SQLite sudah menyediakan jalan keluarnya lewat `VACUUM INTO`. Yang perlu dibenahi cuma dua: pindahkan maintenance ke pola copy-swap, dan buat job-nya berani bilang gagal. Baca juga dasar kenapa database file tunggal ini layak dipercaya di [SQLite: Kenapa yang "Lite" Justru Menang](/posts/sqlite-kenapa-lite-justru-menang/).

Database-mu terakhir di-VACUUM kapan? Kalau kamu cuma tahu dari dashboard hijau, mungkin jawabannya sama dengan kami: belum pernah. 🐷

— Chokdi 🐷 · Content Studio · 2026
