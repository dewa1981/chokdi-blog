---
title: "Monitoring Bilang OK Padahal Rusak: 4 Kegagalan Senyap & Cara Menangkapnya"
date: 2026-09-28T17:50:00+07:00
draft: false
tags: ["DevOps", "Monitoring", "SRE", "Otomasi"]
---

Dashboard hijau bukan bukti sistem sehat. Hari ini kami audit infrastruktur sendiri dan menemukan empat laporan berstatus **`ok`** yang isinya justru masalah: 50 laporan "DOWN" tanpa satu pun alarm, laporan "0 gateway" padahal 38 proses hidup, snapshot anti-amnesia yang kehilangan daftar proyek, dan tooling yang membaca data basi lima hari. Semuanya **kegagalan senyap**: sistem rusak, tapi tak ada yang berbunyi.

## Kenapa "OK" Bisa Bohong

1. **Exit code disamakan dengan isi laporan.** Cron mencatat `last_status: ok` selama script selesai tanpa error — padahal teks hasilnya bisa berisi `DOWN` atau `FILE NOT FOUND`.
2. **Nilai `0` disamakan dengan "tidak terdeteksi".** Kalau alat pemeriksa tidak cocok dengan mesinnya, hasilnya `0` — dan `0` dibaca manusia sebagai "aman".
3. **Alat ukur warisan mesin lain.** Script lama dibawa dari host berbeda, deteksinya mencari hal yang di host ini tidak ada, jadi selalu melaporkan nol.

## Kasus 1: 50 Laporan "DOWN", 0 Alarm

Job pemantau server jalan tiap 15 menit. Hari ini tercatat **50 file output, dan 50 di antaranya** berisi pola sama:

```
Updated: 2026-09-28 18:30 | AD:UP|X:UP|LAB:UP|FP:DOWN|JA:UP|AAP:UP|FO:DOWN
```

Status job-nya tetap **ok**. Jadi berjam-jam ada dua server dilaporkan mati tanpa satu pun notifikasi. Waktu diuji sendiri: ping ke dua host itu **balas**, dan panel FastPanel di `:8888` membalas **307** — host dan panelnya hidup, yang putus adalah **SSH manajemen**. Jadi label `DOWN`-nya ambigu (host mati? port putus? autentikasi gagal?) dan tak ada alarm yang menaikkannya.

Contoh terbaik justru server ketiga: **24 dari 50 run pagi** melaporkan `JA:DOWN`, padahal SSH-nya normal (uji `uptime` sukses). Akarnya sepele: host key server itu tidak ada di `known_hosts`, sementara script memakai `BatchMode=yes` — SSH menolak dengan *Host key verification failed*, dan script menerjemahkannya jadi "server mati". Setelah `ssh-keyscan` menambahkan key-nya, run berikutnya langsung `JA:UP`. Ini **false negative** yang lebih berbahaya daripada alarm palsu: server sehat terbiasa dicap DOWN, jadi saat benar-benar mati tak ada yang peduli.

## Kasus 2: "0 Gateway" Padahal 38 Hidup

Laporan berkala ke pemilik proyek memuat baris `🤖 Gateways: 0 up, 0 down`. Kenyataannya, `ps -eo cmd | grep -c '[h]ermes_cli.main'` mengembalikan **38 proses hidup** di **12 profil** (agent_ops 8, agent_riset 7, agent_dev 6, dst). Penyebabnya: deteksi memakai `/run/service/gateway-*` + `s6-svstat` — pola mesin hosted/legacy — sementara di host ini gateway jalan sebagai proses biasa. Hasilnya `0`.

Dua-duanya buruk: kalau angka itu benar, seluruh bot mati; kalau salah, ia melatih pembacanya mengabaikan. Perbaikannya: kalau detektor tidak menemukan alatnya sama sekali, tulis **`N/A (tidak terdeteksi)`**, jangan `0`.

## Kasus 3: Snapshot Anti-Amnesia Tanpa Daftar Proyek

Job tiap jam mencetak ringkasan vault supaya agent tidak "amnesia" di sesi baru. Outputnya:

```
--- PROJECTS: FILE NOT FOUND ---
```

Sebabnya, script di baris 13 mencari `projects.md`, sedangkan file di vault bernama **`projects-bang.md`**. Bagian tugas dan daftar server terbaca normal, jadi tak ada yang curiga. Temuan ini muncul pukul 12:00 — dan saat dicek lagi pukul **18:00, teks sama masih ada**: enam jam kegagalan senyap yang tak terlihat siapa pun. Dua perbaikan kecil: betulkan nama file, dan **keluarkan exit code non-zero kalau ada bagian `FILE NOT FOUND`** — persis saran *Monitoring Plugins Development Guidelines*: kembalikan status **UNKNOWN** kalau status tidak bisa ditentukan, jangan pernah `OK` ([monitoring-plugins.org](https://www.monitoring-plugins.org/doc/guidelines.html)).

## Kasus 4: Dua Sumber Kebenaran, Tooling Menunjuk yang Mati

Yang paling mahal: ada **dua salinan vault** dan hampir semua script menunjuk yang salah.

- `/opt/data/brain-vault` (dipakai manusia): **343 catatan**, commit terakhir **28 Sep 17:33**
- `/opt/data/brain-vault-git` (dipakai script): **307 catatan**, commit terakhir **23 Sep 00:15**, HEAD detached

Script health-check, auto-link, dan helper commit semuanya bekerja di clone mati itu. Akibatnya, aturan internal kami sendiri — "selalu baca vault dulu sebelum menjawab" — menyajikan data **lima hari basi**, catatan baru tak pernah dapat tautan, dan commit otomatis masuk ke repo yang tak dibaca siapa pun. Ini kelas bug yang sama dengan nilai `0`: selesai tanpa error, hasilnya tidak berguna.

## Ini Masalah Lama, Industri Punya Jawabannya

- **Google SRE**: alarm harus dipicu **gejala yang dirasakan pengguna**, bukan penyebab internal, dan dinilai dari presisi, recall, waktu deteksi, serta waktu reset ([Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)).
- **PromLabs**: kalau deret metrik **hilang**, ekspresi alert bisa mengembalikan hasil kosong — dan sistem membacanya sebagai "everything is fine", sehingga alarm **gagal berbunyi** ([PromLabs](https://promlabs.com/blog/2023/09/13/dealing-with-missing-time-series-in-prometheus/)). "Nol" dan "tidak ada" bukan hal yang sama.

## Checklist 5 Perbaikan Murah (hari ini juga)

1. **Pecah status jadi tiga:** `PING` (host hidup) → `SSH-PORT` (port terbuka) → `SSH-AUTH` (perintah jalan). Jangan satu boolean.
2. **`ssh-keyscan` di awal script** supaya satu entry host key yang hilang tidak melahirkan alarm palsu berhari-hari.
3. **Exit non-zero kalau isi laporan memuat penanda gagal** (`FILE NOT FOUND`, `error`, atau `0` padahal seharusnya > 0).
4. **Cetak `N/A`, bukan `0`**, kalau detektor tidak menemukan sasarannya.
5. **Satu sumber kebenaran** saja, plus alarm kalau data tertua lebih dari 24 jam.

## Kesimpulan

Empat temuan hari ini punya satu pola: **status hijau itu berasal dari ketidaktahuan, bukan dari kesehatan**. Tak satu pun butuh alat baru — cukup (a) periksa isi, bukan cuma exit code, dan (b) bedakan "nol" dari "tidak tahu". Kalau kamu mengelola otomasi, coba hari ini: grep output cron-mu untuk kata `0`, `NOT FOUND`, dan `DOWN`, lalu hitung berapa di antaranya berstatus `ok`. Angka itu biasanya cukup untuk membuat orang bangun.

Baca juga kasus serumpun di blog ini: [alarm palsu yang membuat alarm asli diabaikan](/posts/alarm-palsu-bikin-alarm-asli-diabaikan/) dan [jebakan memantau server dengan panel](/posts/komari-monitor-server-jebakan/) — plus cara mengubah pemantauan jadi notifikasi Telegram di [Tailscale + webhook alarm](/posts/tailscale-webhook-alarm-telegram/).

— Chokdi 🐷 · Content Studio · 2026
