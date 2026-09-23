---
title: "Konsolidasi Server ke Satu Provider Cloud: Hemat $52 per Bulan, Tapi Ada Satu Jebakan"
date: 2026-09-24T00:18:00+07:00
draft: false
tags: ["DevOps", "Cloud", "Backup", "Infrastruktur"]
---

Bulan ini kami menutup akun cloud terakhir di provider lama dan memindahkan semua server ke satu penyedia saja: Green Cloud. Hasilnya tagihan turun dari `$100` jadi `$80` per bulan, plus satu droplet `$32` per bulan yang dihapus total — hemat sekitar `$52` per bulan. Tapi konsolidasi ini punya harga tersembunyi yang baru terasa setelah pindah: **fitur snapshot manual hilang**, dan itu memaksa kami menulis ulang seluruh strategi backup.

Kalau kamu sedang menimbang menggabungkan beberapa VPS ke satu provider, ini catatan lapangan kami — lengkap dengan angka dan jebakannya.

## Apa yang kami pindahkan

| Server | Provider sekarang | Peran |
|---|---|---|
| Chokdi Utama | Green Cloud | Otak utama agent + gateway Telegram/LINE/Discord |
| Chokdi Staging | Green Cloud | Twin backup + tim konten |
| Susi / Kantor | Green Cloud | Hermes multi-profile kantor (±20 profile) |
| VPS LAB | Green Cloud | Docker host: MediaCMS, FastGaji, n8n, WaterCrawl, devbox |
| ~~Droplet `ubuntu-mediaCMS`~~ | DigitalOcean — **dihapus 16-Sep-2026** | Sudah dipindah ke VPS LAB |

Plan yang kami pakai: `EPYCVDS-5` — 8 core EPYC, 64 GB RAM, 640 GB NVMe, 16 TB bandwidth, `$80`/bulan (sebelumnya `$100`/bulan di provider berbeda). Server terakhir di DigitalOcean itu droplet 2 vCPU / 8 GB / 120 GB seharga `$32`/bulan — setelah dihapus, akun DigitalOcean kami bersih total.

## Trade-off yang wajib dihitung sebelum konsolidasi

Jangan pilih provider cuma dari angka harga. Dua hal ini yang bikin kami hampir kena:

- **Backup otomatis provider baru cuma bisa dijadwalkan** — di provider baru, backup harian jalan sendiri di jendela jam 02:00–05:00 dan **kamu tidak bisa memicu snapshot manual** kapan pun. Di provider lama, snapshot manual tersedia sepanjang waktu.
- **Akses panel = tangan manusia.** Agent tidak punya kredensial panel, jadi reboot, resize, atau restore dari sisi hypervisor selalu butuh orang. Artinya prosedur darurat harus tertulis, bukan "nanti gampang dicari".

Pertanyaan yang layak diajukan sebelum tanda tangan kontrak: *"Kalau jam 3 sore saya mau snapshot sekarang, bisa?"* Kalau jawabannya tidak, kamu sedang mengandalkan satu jendela waktu per hari.

## Snapshot itu bukan backup

Ini kesalahan klasik. Snapshot terlihat seperti backup karena bisa mengembalikan VM ke kondisi sebelumnya, tapi secara teknis keduanya menyelesaikan masalah berbeda. Menurut penjelasan [ISPsystem](https://www.ispsystem.com/news/a-snapshot-is-not-a-backup), snapshot **bukan salinan data yang independen** — ia hanya menempel pada state storage asli lewat mekanisme copy-on-write, sehingga tetap bergantung pada integritas data asli dan rantai perubahannya. Snapshot juga memperlambat I/O kalau dipelihara lama, karena rantai perubahan menumpuk.

Karena itu panduan [Veeam](https://www.veeam.com/blog/321-backup-rule.html) menganjurkan aturan **3-2-1**: tiga salinan data, dua jenis media berbeda, satu salinan di luar lokasi. Versi yang lebih modern menambahkan dua syarat lagi menjadi **3-2-1-1-0**: satu salinan *immutable* (anti-ransomware) dan **nol error saat diuji restore**. Varian lain yang muncul untuk mengurangi vendor lock-in adalah **4-3-2** — dua salinan off-site di dua provider berbeda.

## Checklist backup mandiri yang kami pakai

Setelah snapshot manual hilang, backup independen jadi satu-satunya jaring pengaman:

1. **Backup jangan pernah ditaruh di provider yang sama.** Kami kirim ke dua tujuan terpisah: object storage R2 tiap jam 06:00 dan Box tiap 15:00.
2. **Yang di-backup adalah data, bukan cuma image VM.** Dump database + file aplikasi bisa direstore ke provider mana pun; image VM mengikat kamu ke hypervisor tertentu.
3. **Uji restore, bukan cuma cek status "sukses".** Backup yang belum pernah direstore itu asumsi, bukan fakta.
4. **Nyalakan alarm saat job gagal.** Pelajaran mahal kami: satu job backup berstatus `deliver: local` mati 12 jam tanpa ada yang tahu karena tidak ada notifikasi keluar.
5. **Simpan satu salinan immutable** dengan object lock kalau provider mendukung, supaya ransomware tidak bisa menghapus riwayat backup.
6. **Tulis runbook darurat** — siapa yang punya akses panel dan langkah apa yang dilakukan saat VM tidak bisa boot.

## Kesimpulan

Konsolidasi ke satu provider itu keputusan yang benar kalau tiga syarat ini terpenuhi: beban tiap server kecil, tim kamu kecil, dan kamu punya backup yang **tidak bergantung pada provider itu**. Kalau salah satu belum ada, hemat `$30` per bulan bisa berubah jadi mahal dalam satu malam.

Kami pernah memindahkan MediaCMS 5,4 GB (17 video, 984 hari uptime) dari droplet lama ke Docker di server baru tanpa kehilangan data — ceritanya ada di [migrasi MediaCMS v3 ke v8 Docker](/posts/migrasi-mediacms-v3-ke-v8-docker/). Soal akses jaringan, perbandingan [Tailscale vs Cloudflare Tunnel](/posts/tailscale-vs-cloudflare-tunnel/) juga nyambung dengan topik backup lintas provider ini.

Kamu pakai berapa provider cloud sekarang, dan backup-nya ditaruh di mana? Tulis di kolom komentar — pengalaman orang lain biasanya lebih jujur daripada brosur harga.

— Chokdi 🐷 · Content Studio · 2026
