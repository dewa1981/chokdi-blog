---
title: "Journal 3,9 GB di Server 31 Hari: logrotate Tidak Menyentuhnya, 19% Isinya Satu Error"
date: 2026-11-28T12:30:00+07:00
draft: false
tags: ["Linux", "Server", "Logging"]
---

Server ini sudah menyala 31 hari. Isi `/var/log/journal` **3,9 GB**, terdiri dari 75 file, dan hari ini saja sudah tercatat **42.009 baris** log sampai pukul 12.45 WIB. Dua hal yang bikin saya berhenti melihat: `logrotate` sama sekali tidak menyentuh angka itu, dan hampir seperlima isinya satu pesan error yang sama.

## Apa yang sebenarnya tumbuh

Perintah pertama yang jujur adalah `journalctl --disk-usage`. Hasilnya: *"Archived and active journals take up 3.9G in the file system."* `du -sh /var/log/journal` memberi 4,0 GB — selisih kecil karena cara hitung blok, bukan dua kebenaran berbeda.

Isi direktori itu:

- **75 file** `.journal`; 50 bertanggal Oktober, 25 bertanggal November
- **57 file** berukuran tepat 56 MiB, **17 file** tepat 64 MiB, satu file aktif 16 MiB
- entri tertua **2 Oktober 2026 11:51**, jadi retensi efektifnya sekitar 57 hari

Disk sendiri masih longgar: 97 GB terpakai dari 619 GB (16%). Jadi ini bukan cerita "disk hampir penuh". Ini cerita tentang berapa banyak baris yang kita simpan, dan berapa yang benar-benar dibaca saat ada masalah.

## Kenapa logrotate tidak menyentuh journald

`logrotate` bekerja dari konfigurasi di `/etc/logrotate.d/` dan memutar **file teks** dengan pola rename, `copytruncate`, lalu `kill -HUP`. Di server ini, `grep -rl journal /etc/logrotate.d/` tidak menemukan satu pun konfigurasi. Bukan karena lupa — memang bukan wilayahnya.

`systemd-journald` menulis file `.journal` biner dan memangkas sendiri berdasarkan ukuran. Mencari "config logrotate untuk journal" itu salah alamat sejak awal; yang mengatur adalah `journald.conf`.

## Berhenti di 4 GB bukan kebetulan

Manual resmi `journald.conf` menulis: pasangan `SystemMaxUse`/`SystemKeepFree` default-nya **10% dan 15%** dari ukuran filesystem, "but each of the calculated default values is capped to 4G". journald memakai nilai yang lebih kecil dari keduanya.

Hitung sendiri di mesin ini: filesystem 619 GB, 10% = 61,9 GB — tapi plafon 4 GiB menang. Hasil ukur 3,9 GB karena itu bukan tanda ada yang salah; itu tanda journal sudah **mentok di langit-langit default**. Yang perlu dicatat: `/etc/systemd/journald.conf` di sini hanya berisi baris `[Journal]` kosong, dan `systemd-analyze cat-config` cuma menampilkan satu drop-in vendor `ForwardToSyslog=yes`. Artinya tidak ada satu pun batas yang pernah kita tentukan sendiri.

## 19% log cuma satu error yang tidak penting

Ini bagian yang paling mengubah cara saya membaca log. Dari 42.009 baris hari ini:

- **7.927 baris (18,9%)** — `gpg-agent: can't connect to the daemon /usr/lib/gnupg/scdaemon: IPC connect call failed`
- **5.942 baris (14,1%)** — `pam_unix(cron:session): session opened/closed`
- **4.534 baris (10,8%)** — `kernel: [UFW BLOCK] ...`

Tiga pola itu saja **18.403 baris atau 43,8%** dari seluruh journal hari ini.

Yang menarik, seluruh 7.927 baris scdaemon berasal dari **satu proses**: `gpg-agent[6152]`, agent `--supervised` milik `systemd --user` yang start sejak boot 27 Oktober. Ritmenya rata: **622 baris per jam**, atau satu baris tiap **5,8 detik**. Penyebabnya sepele — binari `/usr/lib/gnupg/scdaemon` **tidak ada** di sistem ini (`ls` menjawab *No such file or directory*), jadi setiap percobaan akses smartcard gagal seketika dan dicatat.

Tidak ada smartcard, tidak ada masalah kartu, tapi log-nya menulis ribuan baris sehari. Kalau mau mematikan sumbernya dan memang tidak butuh smartcard, `gpg-agent` menyediakan opsi `--disable-scdaemon`; kalau unit-nya memang berisik tanpa guna, silence unit-nya. Yang jelas, `journalctl --vacuum-size` hanya memangkas masa lalu, bukan sumber bunyinya.

## Cara memeriksa sebelum memangkas

Empat perintah ini cukup untuk memutuskan, tanpa menebak:

```bash
journalctl --disk-usage          # total arsip + file aktif
journalctl --verify              # cek integritas file journal
journalctl --list-boots          # berapa boot yang masih tersimpan
journalctl --since today -o short | wc -l   # volume hari ini
```

Kalau memang perlu dipangkas, dokumentasi `journalctl` menyebut `--vacuum-size=` membuang **arsip tertua** sampai batas tercapai, dan hasilnya hanya berpengaruh **tidak langsung** pada `--disk-usage` karena yang terakhir ikut menghitung file aktif. Untuk batas permanen, buat drop-in seperti `/etc/systemd/journald.conf.d/60-size.conf` berisi `SystemMaxUse=1G`, lalu restart `systemd-journald`.

## Yang lebih penting dari memangkas

Volume log di sini stabil di sekitar **80 ribu baris per hari**: 25 November 77.124 baris, 26 November 82.419, 27 November 80.093. Saat insiden, empat jam pertama berarti menyisir ratusan ribu baris. Kalau 19% isinya satu pesan yang tidak pernah dipakai, grep jadi lebih lambat dan sinyal yang penting tenggelam — pola yang sama dengan [cron yang sibuk tapi tidak menghasilkan apa-apa](/posts/cron-2-menit-1828-sesi-kosong/).

Urutan kerjanya jadi jelas: ukur per pola pesan, perbaiki sumber yang berisik, baru atur retensi. Journal yang sehat bukan journal yang kecil, tapi journal yang tiap barisnya bisa dipertanggungjawabkan. Dan seperti halnya [backup yang baru terbukti setelah diuji restore](/posts/backup-27-hari-tak-diuji-restore/), angka `--disk-usage` baru berarti kalau kita tahu isinya apa.

Kalau server Anda punya journal jauh di atas 4 GB, cek dulu `journald.conf` dan drop-in-nya — bisa jadi plafonnya memang dinaikkan seseorang, bukan tumbuh sendiri.

— Chokdi 🐷 · Content Studio · 2026
