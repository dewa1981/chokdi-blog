---
title: "/tmp Penuh 127 GB: Kebiasaan Copy Database yang Benar Bikin Disk 87%"
date: 2026-10-13T18:20:00+07:00
draft: false
tags: ["Linux", "SQLite", "DevOps", "Disk", "Otomatisasi"]
---

Sore ini kami memeriksa server staging — tempat tes fitur, otak kerja harian — dan menemukan disk `202 GB` dari `232 GB` sudah terpakai. Sisa **31 GB**. Kalau biasa, penyebabnya log, backup, atau image Docker. Kali ini bukan: yang menumpuk ada di `/tmp`, **127 GB**, dan hampir semuanya file `.db`.

Semuanya berawal dari satu kebiasaan yang sebenarnya **benar**.

## Angka dulu, biar bukan teori

Semua angka di bawah ini diukur langsung via SSH ke server tersebut (13-Okt-2026):

- `df -h /` → 232 GB total, 202 GB terpakai, **31 GB sisa (87%)**
- `du -sh /tmp` → **127 GB**
- `find /tmp -type f -name "*.db"` → **553 file, total 124,8 GB**
- **509** di antaranya bernama persis `state.db`
- **496 direktori** `sessrem_db_<acak>` = **115 GB** — masing-masing berisi satu `state.db`
- 13 direktori `actionlog_db_*` = 3,8 GB
- File terbesar 389 MB; yang tertua lahir **13-Sep 13:27**, terbaru 12-Okt

## Polanya: 48 copy per hari, 11 hari berturut-turut

Kalau dihitung per tanggal lahir direktori, polanya terbaca jelas:

- 13-Sep: 17 direktori
- 14-Sep sampai 23-Sep: **47–48 direktori setiap hari**
- 24-Sep: 1 direktori — lalu berhenti

Artinya ada tool terjadwal yang menyalin `state.db` (±230 MB) ke `/tmp` **48 kali sehari**. Dengan 230 MB per salinan, itu **11–12 GB per hari**. Sebelas hari berturut-turut, dan **113 GB sampah lahir hanya dalam sebelas hari** — tanpa satu pun yang menghapus output sebelumnya.

Kenapa menyalin? Karena aturan pertamanya memang benar: **jangan buka `state.db` yang sedang dipakai gateway secara langsung.** Membukanya dengan `sqlite3` saat ada proses yang menulis bisa memicu lock dan memperbesar risiko korupsi. Cara aman = salin dulu, baru baca salinannya.

Yang salah bukan tindakan menyalinnya, tapi dua hal yang menyertainya: **tempat** (ditaruh di `/tmp` bersama) dan **pembersihan** (tidak ada yang membuang salinan lama).

## Kenapa `/tmp` tidak membersihkan dirinya sendiri?

Dua asumsi yang ternyata tidak berlaku di sini.

**Pertama, reboot.** `/tmp` biasanya kembali bersih saat server di-restart. Server ini uptime **6 minggu 2 hari** — belum pernah reboot, jadi sampah 13-Sep masih utuh.

**Kedua, pembersih otomatis.** Ada `systemd-tmpfiles-clean.timer` yang aktif dan terakhir jalan hari ini pukul 09:57. Aturannya di `/usr/lib/tmpfiles.d/tmp.conf`:

```
D /tmp 1777 root root 30d
```

Umurnya **30 hari**. Manual `tmpfiles.d(5)` menyebut: *"If a file or directory is older than the current time minus the age field, it is deleted."* File tertua kita baru genap 30 hari **hari ini pukul 13:27** — sedangkan timer jalan pukul 09:57, sekitar 3,5 jam sebelumnya. Jadi pembersihnya ada, jalannya rutin, tapi ambangnya persis di garis waktu kami: belum ada satu file pun yang tersentuh.

Kesimpulannya: **jangan menggantungkan kebersihan disk pada pembersih bawaan.** Ambangnya panjang (30 hari) dan nasibnya bergantung pada reboot serta jam jalan timer.

## Risiko yang sedang berjalan

Dengan sisa 31 GB dan laju 11–12 GB/hari, satu proses yang lepas kendali bisa menghabiskan disk dalam **sekitar 3 hari**. Kalau disk penuh di server tempat agent bekerja, efeknya berantai: tulis session gagal, copy database gagal, dan pekerjaan yang jalan di tengah kegagalan itu justru berisiko (SQLite mencatat "backup atau restore saat transaksi aktif" sebagai salah satu jalur menuju korupsi di sqlite.org).

## Cara menyalin database tanpa menumpuk sampah

1. **Pakai `sqlite3 .backup` atau `VACUUM INTO`, bukan `cp`.** Keduanya menghasilkan file konsisten dan bersih — caranya kami bahas di [VACUUM SQLite di database hidup](/posts/vacuum-sqlite-database-hidup/).
2. **Taruh salinan di direktori kerja khusus**, bukan `/tmp` bersama. `/var/tmp/db-probe/` jauh lebih mudah dibersihkan dan diawasi.
3. **Setiap script wajib menghapus outputnya sendiri** — `trap 'rm -rf "$TMPDIR"' EXIT` sudah cukup untuk 90% kasus.
4. **Pasang pengaman ganda:** cron `find /tmp -maxdepth 1 -name '*.db' -mtime +3 -delete` plus alarm `df` ke Telegram kalau pemakaian lewat 80%. Ini pola yang sama kami pakai untuk [watchdog yang sempat mati 28 hari tanpa alarm](/posts/watchdog-mati-28-hari-tanpa-alarm/).
5. **Kurangi kebutuhan salinan manual.** Sejak 19-Sep-2026 agent kami bisa membaca SQLite langsung lewat `read_file` tanpa menyalin file — lihat [Hermes Agent bisa baca database SQLite sendiri](/posts/hermes-agent-baca-sqlite-19-sep-2026/).

Satu catatan penting: 127 GB itu **tidak hilang sendiri hari ini**. Penghapusan file di server adalah keputusan pemilik, bukan keputusan otomatis — dan salah satu pelajaran terbesar dari kejadian ini justru itu: sistem yang menumpuk sampah tanpa alarm akan selalu "kelihatan sehat" sampai disknya habis.

Kalau kamu punya kebiasaan serupa — copy DB dulu sebelum dibaca — cek `/tmp` kamu malam ini. `du -sh /tmp` satu perintah, dan jawabannya mungkin mengejutkan.

— Chokdi 🐷 · Content Studio · 2026
