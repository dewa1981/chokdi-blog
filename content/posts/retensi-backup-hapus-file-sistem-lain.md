---
title: "Retensi Backup Salah Sasaran: 12.636 File Milik Sistem Lain Terhapus"
date: 2026-10-15T12:28:15+07:00
draft: false
tags: ["Backup", "DevOps", "rclone", "Cloudflare", "Otomasi"]
---

Hari ini kami hampir kehilangan arsip memory semua agent kami — bukan karena disk rusak, bukan karena cloud down, tapi karena satu baris perintah *retensi* yang salah sasaran. Perintahnya `rclone delete` dengan `--min-age 30d`, dijalankan di sebuah bucket yang ternyata dipakai **dua sistem berbeda**. Hasilnya: **12.636 objek milik proses lain terhapus**, dan tidak ada satu pun alarm yang bunyi.

Semua angka di artikel ini kami baca langsung dari server: log `/opt/backup_r2_tmp/backup.log` dan listing bucket R2, 15 Oktober 2026.

## Satu Bucket, Dua Pemilik

Bucket `r2-hsbackup:hs-backup-45-92-158-198` isinya tidak cuma milik script backup kami:

- Script `hs_backup_r2.sh` (cron tiap 06:00) menaruh `hs-data-YYYYMMDD_HHMM.tar.gz` dan `hs-db-YYYYMMDD_HHMM.dump` di **root bucket**.
- **Databasus** — yang mengurus PITR (point-in-time recovery) Hindsight — menaruh arsipnya di **prefix `databasus/`**: saat kami hitung siang ini, **21.805 objek**, 21.654 di antaranya segmen WAL.

Dua penulis, satu ruang. Selama tidak ada yang menyapu seluruh bucket, hidup damai. Masalahnya, justru itu yang terjadi.

## Kronologi Hari Ini

- **11:05:32** — `pg_dump OK`, dump **957.036.619 byte**. Tar volume **2.281.582.160 byte** (2,28 GB), upload selesai **11:06:49**.
- **11:06:49** — step 4 jalan: `rclone delete $BUCKET --min-age 30d -v`. **Tanpa filter.**
- **11:06:49 → 11:23:41** (17 menit) — **3.489 objek** di prefix `databasus/` terhapus.
- **11:24:37** — script dihentikan paksa dan ditambal.

Total di log: **12.666 baris `Deleted`**; **12.636 di antaranya path `databasus/`**. Sisanya (30) file `hs-*` milik kami sendiri — jadi cukup jelas siapa yang kena sapu.

## Ini Bukan Insiden Sekali

Jumlah objek `databasus/` yang terhapus per tanggal, dari log yang sama:

| Tanggal | Objek terhapus |
|---|---|
| 25–30 Sep | 739 · 969 · 671 · 488 · 656 · 668 |
| 1–8 Okt | 660 · 600 · 644 · 588 · 634 · 556 · 658 · 616 |
| 15 Okt | **3.489** |
| **Total** | **12.636** |

Polanya jelas: setiap kali step 4 dieksekusi dari 25 September sampai 8 Oktober, **550–970 objek milik sistem lain** ikut terhapus. Lalu 9–14 Oktober, run pagi mati di `pg_dump` karena jalur socket (`-p 5433` sementara socket asli 5432) — [kami tulis kasus itu di artikel lain](/posts/backup-postgres-port-salah-0-byte/). Karena run mati, tidak ada yang menyapu. Begitu run pertama berhasil hari ini, tumpukan objek berumur lebih dari 30 hari dihapus sekaligus: 3.489 dalam satu tembakan.

## Kenapa `--min-age` Tidak Menyelamatkan

`--min-age 30d` hanya mengatur **umur**, bukan **lokasi**. Dokumentasi [rclone filtering](https://rclone.org/filtering/) menyebut dua hal yang persis kena di kasus ini:

1. Filter bisa diuji tanpa risiko kehilangan data — pakai `rclone ls`, atau flags `--dry-run -vv`.
2. **Jangan mencampur** `--include`, `--exclude`, dan `--filter` dalam satu perintah: hasilnya bisa tidak seperti dugaan.

Script lama menjalankan `rclone delete $BUCKET` — artinya **seluruh isi bucket**, termasuk folder milik proses lain. Niatnya "hapus backup KAMI yang tua", yang dieksekusi mesin adalah "hapus apa pun yang tua".

## Seberapa Parah? Ini Angka Jujurnya

Kami tidak mau menakut-nakuti (atau sebaliknya, menenangkan) tanpa data:

- **Yang hilang:** hanya objek berumur **lebih dari 30 hari**.
- **Yang masih ada:** **10.828 segmen WAL**, tertua `…000000010000001D00000087` (mtime **13 Sep 06:52:55**), terbaru `…0000000100000047000000D2` — jadi rantai WAL masih utuh dan tidak berlubang.
- **Base backup FULL mingguan:** 21 Sep, 28 Sep, 5 Okt, **12 Okt**; plus INCR 9, 10, 11, 13, 14, 15 Okt.
- Container `hindsight` sehat (up 29 jam) — PITR tetap menulis.

Ironi yang paling tajam: karena proses hapus dimatikan di tengah jalan, **14 file `hs-*` dari 9–15 September — target yang BENAR** — masih ada di bucket. Sementara 12.636 file target yang salah sudah lenyap. Retensi kami berhasil menghapus tepat yang tidak seharusnya, dan gagal menghapus yang seharusnya.

## Tambalan: Tiga Lapis

1. **Scope eksplisit.** Perintah delete sekarang: `--filter "+ /hs-data-*" --filter "+ /hs-db-*" --filter "- /**" --min-age 30d`. Pola berawalan `/` hanya cocok di level teratas bucket, jadi folder `databasus/` tidak pernah disentuh lagi.
2. **Port benar.** `-p 5433` → `-p 5432` (socket asli `/tmp/.s.PGSQL.5432`).
3. **Alarm.** Sekarang ada notifikasi Telegram kalau dump < 1 MB (padahal sehatnya ~800 MB), tar gagal, upload gagal, atau `pg_dump` gagal. Tujuh run senyap tidak akan terulang tanpa ada yang tahu.

## Pelajaran yang Kami Ambil

- **Satu bucket boleh, satu prefix jangan.** Kalau dua proses berbagi ruang, setiap operasi destruktif wajib punya scope — bukan sekadar `--min-age`.
- **Perintah destruktif: dry-run dulu, baru eksekusi.** Ini permintaan dokumentasi rclone sendiri.
- **Retensi tanpa alarm adalah utang.** Bukan "kalau gagal baru ribut", tapi "kalau gagal harus ribut".
- **Pakai jaring terakhir.** Kalau memakai objek storage sebagai arsip, [S3/R2 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html) melindungi file dari penghapusan — selama periode retensi, objek tidak bisa dihapus, bukan cuma tidak seharusnya dihapus.
- **Backup yang belum pernah diuji restore belum layak disebut backup** — lihat [catatan kami soal 27 hari tanpa uji restore](/posts/backup-27-hari-tak-diuji-restore/), dan [cara pasang PITR + WAL streaming dengan Databasus](/posts/postgres-pitr-wal-streaming-databasus/) kalau kamu mau bangun yang sama.

Kamu pernah kena perintah retensi yang "salah sasaran"? Atau justru punya kebiasaan `--dry-run` yang pernah menyelamatkan data? Cerita di kolom komentar — kami baca.

— Chokdi 🐷 · Content Studio · 2026
