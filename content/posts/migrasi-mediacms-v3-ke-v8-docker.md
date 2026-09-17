---
title: "Migrasi MediaCMS v3 ke v8: 6 Jebakan Upgrade Lintas 2,5 Tahun"
date: 2026-09-17T12:15:00+07:00
draft: false
tags: ["DevOps", "Docker", "Self-Hosted", "Migrasi"]
---

Ada satu server video kami yang jalan **984 hari tanpa pernah di-upgrade**. Waktu dibongkar, isinya MediaCMS rilis November 2023, PostgreSQL 14, dan tiga patch keamanan yang sudah ketinggalan belasan versi. Proyek minggu ini: pindahkan semuanya ke Docker dengan MediaCMS **v8.4.0** + PostgreSQL 17.2, tanpa kehilangan satu file pun. Yang menarik bukan MediaCMS-nya — tapi **kenapa cutover bisa terlihat sukses padahal servernya belum benar-benar pindah**.

## Kenapa Baru Sekarang Dipindah

Alasan bertahan selama ini masuk akal: server lama bisa **snapshot manual kapan saja**, sedangkan server baru backup-nya otomatis cuma sekali sehari. Setelah ditimbang, ternyata backup mandiri (dump database + media ke object storage) lebih penting daripada snapshot VM. Ditambah tiga hal ini:

- **1 vCPU / 1 GB RAM seharga $32 per bulan** — mahal untuk ukuran 2026.
- **Versi app ketinggalan ±2,5 tahun** — v3.1.0 vs upstream v8.4.0.
- **Patch keamanan yang kelewat**: path traversal di nginx (v8.3.2), akses media/playlist privat (v8.3.3), dan subtitle (v8.3.5).

## Hasil Akhir (angka nyata, bukan proyeksi)

| Item | Server lama | Server baru |
|---|---|---|
| Versi MediaCMS | v3.1.0 (2023) | **v8.4.0** |
| Database | PostgreSQL 14 | **PostgreSQL 17.2** |
| Migrations | 35 | **72** |
| Tabel | 38 | **60** |
| Video / User | 17 / 7 | **17 / 7** |
| Media | 5,4 GB | **5,4 GB (4.175 file)** |
| Container | systemd (5 service) | **6 Docker container** |
| Uptime server | 984 hari | 31 hari |

Domain tetap sama, SSL tetap di belakang Cloudflare, dan **jumlah baris datanya identik** — itu bukti yang kami pakai untuk bilang migrasi ini bersih.

## Alur 7 Fase

1. **Inventaris read-only** — versi, ukuran media, jumlah user/video, daftar service.
2. **Backup di server lama** — `pg_dump -Fc` + SQL gzip + `media_files.tar.gz` + checksum SHA256.
3. **Transfer ditarik dari sisi tujuan** (`rsync -avP --partial --inplace`), bukan didorong dari server lama — lalu diverifikasi `sha256sum -c`.
4. **Deploy Docker fresh SEBELUM import** — port app digeser, data dir database dikeluarkan dari folder repo, env DB/Redis dipasang ke semua service.
5. **Import data lama** — `pg_restore --no-owner --no-privileges`, lanjut `manage.py migrate` sebagai jembatan skema v3 → v8.
6. **Cutover domain** — hostname ditambah ke tunnel, DNS A diganti CNAME.
7. **Watchdog 24 jam** — cek tiap 4 jam, lapor otomatis.

## 6 Jebakan yang Bikin Migrasi Kelihatan Sukses Padahal Belum

### 1. DNS masih menunjuk server lama

Ini yang paling menipu. Web balas **HTTP 200**, halaman tampil normal, semua orang senang — padahal request-nya masih dilayani server lama. Cutover belum terjadi. Bukti yang sah cuma satu: **log container di server baru** menunjukkan request masuk, bukan angka 200 dari luar.

### 2. `migrate` exit 0 walau semua query gagal

Container selesai dengan status sukses, `docker compose ps` hijau, tapi database-nya kosong karena query-nya gagal semua. **Exit code bukan bukti.** Verifikasinya harus query nyata ke database: hitung barisnya, bandingkan dengan sumber.

### 3. Healthcheck PostgreSQL false positive

`pg_isready` cuma mengecek socket, bukan apakah klaster benar-benar melayani. Kalau kepemilikan folder data salah, Postgres bisa mati sementara statusnya tetap `healthy`. Healthcheck yang tidak menyentuh data = hiasan.

### 4. Image mendeklarasikan `VOLUME` → chown ditimpa

Image aplikasi mendeklarasikan `VOLUME` di Dockerfile. Akibatnya **setiap kali container start, Docker membuat ulang direktori mount** dengan uid 33 dan menimpa `chown` yang sudah kita set. Solusinya: folder data database **wajib di luar folder repo**. Detail perilaku ini memang dokumentasi resmi Docker, tapi efeknya baru terasa saat produksi.

### 5. `role "postgres" does not exist` — ini normal

Muncul di log, kelihatan seram, padahal cuma artinya klaster memakai user yang kita set di environment sebagai superuser. Jangan panik dan jangan "perbaiki" dengan membuat role baru.

### 6. URL media yang benar bukan yang kelihatan logis

Path media yang benar punya segmen `original` di tengahnya. Menebak URL dari struktur folder = 404 yang bikin kita mengira data media tidak ikut tercopy.

## Yang Bisa Dipakai Siapa Saja

Naik lintas major version (Postgres 14 → 17) itu **selalu lewat dump + restore ke folder data baru**, bukan upgrade di tempat pada folder lama. Dan yang lebih penting: **jangan pernah percaya satu sinyal saja**. Exit code boleh bohong, status container boleh hijau, healthcheck boleh salah — pola ini kami bahas juga di artikel [Cron Job Bilang OK Tapi Bohong](/posts/cron-job-bilang-ok-tapi-bohong/). Verifikasi harus dari sisi yang benar-benar melayani request.

Kalau setup-nya melibatkan tunnel dan domain, langkah cutover-nya mirip dengan panduan [Cloudflare Tunnel](/posts/cara-setup-cloudflare-tunnel-2026/). Intinya sama: yang menentukan berhasil atau tidak adalah **apa yang melayani request**, bukan apa yang tertulis di dashboard.

Kami masih menunggu watchdog 24 jam dan baru menghapus server lama setelah semua cek hijau. Ada pengalaman serupa soal migrasi lintas versi? Ceritakan di komentar.

Sumber: [MediaCMS](https://github.com/mediacms-io/mediacms) · [Dokumentasi VOLUME Docker](https://docs.docker.com/reference/dockerfile/#volume)

— Chokdi 🐷 · Content Studio · 2026
