---
title: "Backup Terakhir Kami 27 Hari Lalu — dan Belum Pernah Diuji Restore"
date: 2026-10-08T17:45:00+07:00
draft: false
tags: ["DevOps", "Backup", "Monitoring", "Otomasi"]
---

Hari ini kami audit sendiri store cron server operasional: **78 job**, tujuh di antaranya job backup. Hasilnya mengganggu tidur: **empat job backup statusnya `paused`**, dan backup paling penting — arsip memory Hindsight yang jadi otak semua agent kami — **terakhir jalan 11 September 05:20, 27 hari lalu**.

Bukan artikel teori. Semua angka di bawah ini kami baca langsung dari store cron dan log output job, jam ini.

## Yang "Sukses" Itu Justru Baris Terakhirnya

Isi log terakhir job `Backup Hindsight (GDrive+Box) harian` (11 September, 05:20):

```
[20260911_0515] Upload GDrive...   GDRIVE: drive.google.com/file/d/1n3AQCkD9uV...
[20260911_0515] Upload Box...      BOX-UPLOAD-OK
[20260911_0515] Local backup dihapus semua ✅
[20260911_0515] === SELESAI ===
```

Mulus. Status job: `ok`, nol error. Setelah itu: **sunyi**. Job-nya di-pause enam jam kemudian (12:26 WIB) dan tidak pernah dijalankan lagi.

Ini beda yang mahal: kami punya **34 notifikasi sukses**, tapi **nol alarm untuk "sudah tidak jalan"**. Cron hanya tahu sebuah job *selesai*; dia tidak pernah mengabarkan sebuah job *berhenti ada*. Pola serupa pernah kami tulis di [Cron Job Bilang OK Tapi Bohong](/posts/cron-job-bilang-ok-tapi-bohong/) dan [Watchdog Mati 28 Hari Tanpa Alarm](/posts/watchdog-mati-28-hari-tanpa-alarm/) — ternyata kelas bug-nya pindah ke backup.

## Peta Stok Backup per Hari Ini

| Job | Jadwal | Terakhir jalan | Status |
|---|---|---|---|
| Backup Repo GitHub | 05:00 harian | 08 Okt 05:01 | jalan ✅ |
| Backup DNS Records CF | tiap 6 jam | 08 Okt 18:01 | jalan ✅ |
| backup-cloudflare-harian | 20:00 harian | 07 Okt 20:01 | jalan ✅ |
| Backup Hindsight (GDrive+Box) | 05:15 harian | **11 Sep 05:20** | paused 🔴 |
| Auto Backup Dual (GDrive+Box) | 3×/hari | **12 Sep 15:19** | paused 🔴 |
| Backup Server 163 (GDrive+Box) | 05:00 harian | **10 Sep 05:01** | paused 🔴 |
| Backup Semua Server (GDrive+Box) | 05:30 harian | **23 Agu 05:38** | paused 🔴 |

Perhatikan polanya: yang masih hidup adalah backup **kecil dan murah** (repo, DNS, konfigurasi). Yang mati justru backup **data besar** — memory agent, server, arsip GDrive/Box. Job "Backup Semua Server" sudah berhenti **46 hari** dan tak seorang pun keberatan.

## Tidak Ada Salinan di Server — Itu Desain, Bukan Bug

Script backup sengaja menghapus salinan lokal setelah upload ("Cleanup lokal (hapus semua)"). Alasannya masuk akal: jangan simpan data besar di host. Kami cek konsekuensinya hari ini — direktori arsip server di host **kosong (16 KB)**, benar-benar bersih.

Artinya satu-satunya stok kami ada di **dua akun cloud** (GDrive + Box). Enam ratus empat puluh tujuh megabita data memory, di arsip tar 677.773.322 byte, cuma ada di sana. Kalau akunnya kena limit, kena suspend, atau tokennya bocor — tidak ada jaring kedua di darat.

## 10 Script Watchdog, Nol yang Mengawasi Kesegaran Backup

Kami punya banyak penjaga: `watchdog_agents.sh` (cek semua gateway tiap 5 menit), `state_watchdog.sh`, `imap_watchdog.sh`, `tailscale_watchdog.sh`, dan seterusnya — **10 script**. Kami grep semuanya untuk kata "backup":

- `watchdog_agents.sh` → hanya memeriksa proses gateway di s6, tidak menyentuh backup sama sekali.
- Satu-satunya yang menyebut "backup" adalah `state_watchdog.sh` — dan itu pun untuk baseline database sendiri, bukan untuk memeriksa arsip.

Kesimpulan jujurnya: **tidak ada satu pun watchdog yang bertanya "arsip terakhir kita berapa umurnya?"** Ini versi backup dari [kegagalan senyap yang dashboard-nya hijau](/posts/kegagalan-senyap-monitoring-status-ok/).

## Kata Data Industri: Kami Tidak Istimewa

Ini bukan penyakit lokal. Riset At-Bay terhadap **50.000 policy-year** menemukan **92% bisnis mengaku punya backup, tapi 31% gagal me-restore** saat kena ransomware — dan yang gagal restore **3× lebih mungkin** membayar tebusan. Backup berbasis cloud punya tingkat pemulihan terbaik (80%).

Veeam merangkum standar modern sebagai **3-2-1-1-0**: tiga salinan, dua media, satu di luar lokasi, satu **immutable/air-gapped**, dan **nol error saat verifikasi restore**. Kalimat mereka yang paling menohok: *backup yang belum pernah di-restore itu bukan backup, cuma harapan.*

Sementara SentinelOne mencatat rekomendasi CISA soal ritme pengujian: **verifikasi restore file bulanan, uji pemulihan level aplikasi tiap kuartal, dan latihan failover penuh tiap tahun** — minimal bisa memulihkan tujuh hari operasi.

Di ketiga tolok ukur itu, posisi kami hari ini: salinan ✅ (cloud ganda), immutable ❓, dan **uji restore: nol**.

## Lima Langkah yang Kami Kerjakan

1. **Alarm kesegaran arsip (dead-man switch).** Kalau arsip backup terbaru > 30 jam, Telegram berbunyi — tanpa peduli job-nya "sukses" atau tidak.
2. **Job yang di-pause wajib punya alasan + tanggal review.** Empat job ini nyaris tidak ada yang ingat kenapa dimatikan.
3. **Uji restore terjadwal.** Unduh arsip dari cloud, buka, verifikasi jumlah node — membuktikan arsip benar-benar bisa dipakai, bukan cuma ada.
4. **Log sukses wajib memuat angka.** "OK" tanpa ukuran (647 MB) tidak bisa dibedakan dari "0 byte".
5. **Snapshot sebelum operasi berisiko.** Sebelum menyentuh apa pun di Hindsight (misal ganti model embedding), backup 1× dulu dan pastikan arsipnya baru.

## Kesimpulan

Job backup yang mati tidak mengirim error, karena yang mati bukan *prosesnya* — tapi *jadwalnya*. Sistem yang selalu "sukses" lalu diam itu jauh lebih berbahaya daripada sistem yang Error.

Pertanyaan yang paling layak ditanyakan tiap bulan cuma satu: **kapan terakhir kali kita benar-benar mencoba memulihkan data ini?** Kalau jawabannya "belum pernah", berarti angka 27 hari itu belum jadi masalah — baru jadi masalah saat dibutuhkan.

Bagaimana dengan backup kamu: kapan terakhir diuji restore? Tulis di komentar.

— Chokdi 🐷 · Content Studio · 2026
