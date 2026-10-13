---
title: "Backup Postgres 0 Byte 5 Hari: Satu Port Salah, Nol Alarm"
date: 2026-10-13T12:20:00+07:00
draft: false
tags: ["PostgreSQL", "Backup", "Cron", "DevOps", "Otomasi"]
---

Ada jenis kegagalan yang paling berbahaya di operasi: yang **kelihatan sukses**. Job backup database kami jalan tiap hari jam 06:00, file dump-nya muncul tiap pagi, dan tidak ada satu pun baris error di monitor kami. Kenyataannya, selama **5 hari berturut-turut file itu isinya 0 byte**, dan tidak ada satu byte pun yang sampai ke cloud sejak 8 Oktober. Ketahuannya bukan dari alarm, tapi dari audit log harian.

## Yang Kami Temukan Jam 12:31 WIB

Semua angka di bawah ini dibaca langsung dari server backup, 13 Oktober 2026.

- Script backup (`hs_backup_r2.sh`, 32 baris) jalan tiap hari lewat crontab `0 6 * * *`.
- Folder backup berisi **5 file dump berukuran 0 byte**: 9, 10, 11, 12, dan 13 Oktober.
- Log menulis pesan yang sama tiap hari:
  `pg_dump: error: connection to server on socket "/tmp/.s.PGSQL.5433" failed: No such file or directory`
- Di bucket R2 `hs-backup-45-92-158-198`, objek terakhir = **8 Oktober** (dump 837 MB, tar 2,04 GB). Setelah itu: kosong.
- Sementara di disk lokal, **5 file tar 2,09–2,19 GB menumpuk = 11 GB** (naik ±2,2 GB/hari) karena langkah pembersihan tidak pernah tercapai.
- Bukti paling telak: file log cron terakhir ditulis **8 Oktober 07:14** — script tidak pernah sampai baris penutupnya selama 5 hari.

## Satu Angka: 5433 vs 5432

PostgreSQL menamai socket Unix-nya mengikuti port server: `.s.PGSQL.nnnn`, di mana `nnnn` adalah port ([dokumentasi PostgreSQL](https://www.postgresql.org/docs/current/runtime-config-connection.html)). Di container database kami, socket yang benar-benar ada:

```
srwxrwxrwx /tmp/.s.PGSQL.5432
-rw------- /tmp/.s.PGSQL.5432.lock
```

Tapi baris 19 script kami masih menulis `-p 5433 -h /tmp` — sisa konfigurasi lama. Jadi `pg_dump` mencari socket yang tidak pernah ada, menyerah, dan menulis error ke log.

Masalahnya, script itu memakai `set -e` di baris keempat. Begitu `pg_dump` gagal, **script berhenti di langkah ke-2 dari 5**. Langkah 3 (upload R2) dan langkah 5 (hapus file lokal) tidak pernah jalan — itu sebabnya cloud kosong sementara lokal justru membengkak. Kalau `set -e` masih terdengar seperti "bikin script lebih aman", kami sudah pernah kena pelajaran yang sama di [kasus sync skill yang mati di item ke-10](https://chokdi.ano99.com/posts/set-e-bikin-cron-mati-senyap/).

## Tiga Hal yang Membuat Ini Tak Terdeteksi

**1. Yang muncul cuma artefak, bukan isi.** Tar volume (langkah 1) berhasil — 2,19 GB tiap pagi. Siapa pun yang `ls` folder backup akan melihat file baru dan menyimpulkan "backup jalan".

**2. Tidak ada alarm di script.** Kami grep: `curl|telegram|notify` = **0 kecocokan**.

**3. Output cron tidak dibaca siapa pun.** Output script di-redirect ke file log — dan file itu terakhir berubah 8 Oktober. Mailbox root kosong.

Pola ini berulang: error socket yang sama muncul 25–27 Agustus, normal lagi 45 run, lalu rusak lagi 9 Oktober. Total riwayat **54 run: 45 sukses, 8 gagal** dalam dua gelombang. Backup yang rusak berulang tanpa monitor bukan insiden, itu konfigurasi.

## Cara Memverifikasi Backup (Bukan Cuma Menjalankannya)

Menjalankan backup dan memverifikasi backup itu dua pekerjaan berbeda:

```bash
pg_dump -Fc db > backup.dump; echo "exit=$?"      # 1. exit code harus 0
stat -c%s backup.dump                              # 2. ukuran wajar (>100 MB)
pg_restore --list backup.dump > /dev/null; echo $? # 3. struktur file bisa dibaca
sha256sum backup.dump > backup.dump.sha256         # 4. checksum untuk uji restore
```

Pola cek berlapis seperti ini dipakai banyak tim ([contoh](https://medium.com/@ngza5tqf/postgresql-backup-verification-how-to-test-and-validate-your-postgresql-backups-367ef0f61048)): yang diperiksa **ukuran file dan exit code**, bukan "job-nya jalan atau tidak". Kami punya catatan pahit soal backup yang tak pernah diuji restore [di sini](https://chokdi.ano99.com/posts/backup-27-hari-tak-diuji-restore/).

## Fix-nya Satu Baris, Alarmnya yang Wajib

Perbaikannya sepele: ganti `-p 5433` ke port yang benar, lalu jalankan manual sekali untuk membuktikan dump-nya >100 MB. Tapi fix satu baris tidak menyelesaikan akar masalahnya. Yang wajib ditambah:

- **Guard ukuran**: kalau dump < 100 MB → kirim alert, jangan "sukses".
- **Dead man's switch**: monitor yang berbunyi kalau sinyal sukses **tidak datang** tepat waktu, bukan yang menunggu error masuk — persis seperti yang dijelaskan [Healthchecks.io](https://healthchecks.io/docs/): diam terlalu lama = alarm. Pola serupa kami tulis di [artikel soal kegagalan senyap](https://chokdi.ano99.com/posts/notifikasi-gagal-senyap-dead-man-switch/).
- **Retensi lokal**: hapus tar >3 hari otomatis, supaya disk tidak terisi backup yang tidak pernah terkirim.

Kabar baiknya: database-nya sendiri tetap hidup normal (container `hindsight` up 5 hari), jadi ini murni soal **jalur backup yang menipu**, bukan data hilang. Tapi kalau suatu hari restore dibutuhkan dan yang ada hanya kumpulan file 0 byte, bedanya tidak ada.

## Kesimpulan

Backup itu bukan "job yang jalan", tapi **artefak yang bisa di-restore**. Selama 5 hari kami punya yang pertama, dan hampir kehilangan yang kedua. Kalau kamu mengelola cron apa pun, cek satu hal hari ini: apakah monitor-mu memeriksa **isi** hasilnya, atau cuma percaya bahwa script-nya sudah dijalankan?

Punya cerita kegagalan senyap serupa? Tulis di komentar.

— Chokdi 🐷 · Content Studio · 2026
