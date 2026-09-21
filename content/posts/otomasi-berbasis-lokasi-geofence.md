---
title: "Otomasi Berbasis Lokasi: Bikin Bot, Rumah & HP Nyala Sendiri Begitu Kamu Sampai"
date: 2026-09-21T12:10:00+07:00
draft: false
tags: ["Otomasi", "Geofencing", "Cron", "Smart Home"]
---

Kebanyakan orang bikin jadwal otomatis pakai jam: "tiap hari jam 9, kirim reminder ini". Masalahnya, hidup nggak jalan pakai jam — hidup jalan pakai **lokasi**. Kamu nggak butuh reminder saat jam 9, kamu butuh reminder saat **sudah sampai** di suatu tempat. Di sinilah **otomasi berbasis lokasi (location-triggered automation / geofencing)** masuk: pemicunya bukan waktu, tapi "masuk" atau "keluar" dari sebuah area di peta.

Artikel ini membahas cara kerjanya di 3 level: HP kamu, smart home, dan bot/server (yang kami pakai sendiri di Chokdi).

## Apa Itu Trigger Lokasi & Geofence?

**Geofence** = pagar virtual: satu titik koordinat + radius (misal 200 meter). Sistem akan memberi tahu kamu saat sebuah perangkat **masuk (enter)** atau **keluar (leave)** dari pagar itu. Yang menjadi pemicu bukan GPS presisi tinggi, tapi layanan lokasi hemat daya dari OS (Google Fuse Location di Android, region monitoring di iOS).

Konsekuensinya penting: trigger lokasi itu **tidak instan**. Ada jeda beberapa detik sampai puluhan detik, dan akurasinya tergantung sinyal sekitar — WiFi, menara seluler, baru GPS. Jadi jangan pakai trigger lokasi untuk hal yang butuh ketepatan detik.

## Tiga Cara yang Terbukti Jalan

| Platform | Pemicu | Catatan |
|---|---|---|
| Home Assistant | `trigger: zone` / `zone.entered` | Bisa YAML, jalan di server sendiri |
| Android (Tasker + AutoLocation) | Geofence monitor | Hemat baterai, butuh WiFi nyala |
| iPhone (Shortcuts) | Travel trigger *Arrive*/*Leave* | Perlu ditekan "Run" (lihat jebakan di bawah) |

### 1. Home Assistant — zone trigger

Home Assistant punya trigger bawaan khusus lokasi. Contohnya cukup pendek:

```yaml
triggers:
  - trigger: zone.entered
    target:
      entity_id: person.nina
    options:
      zone: zone.work
```

Selain `zone.entered`, ada juga `zone.occupancy_cleared` — pemicu yang jalan **saat orang terakhir keluar** dari sebuah zona. Ini pakai-nya banyak: matikan kipas kantor, kunci pintu, atau nyalakan mode "rumah kosong".

### 2. Android — Tasker + AutoLocation

Di Android, geofence biasanya dipegang Google Play Services. Menurut FAQ resmi AutoLocation, ada tiga mode monitor yang beda tujuan: **Geofence Monitor** (hemat daya, nggak pakai GPS), **Location Monitor** (cari koordinat, bisa pakai GPS), dan kondisi lokasi bawaan Tasker (algoritma sendiri). Untuk pemicu "sampai di tempat X", Geofence Monitor sudah cukup.

### 3. iPhone — Travel trigger di Shortcuts

Apple menyediakan trigger **Arrive** dan **Leave**: pilih lokasi, lalu bisa dipersempit lagi dengan **Time Range** (misal hanya jalan kalau kamu tiba antara jam 17:00–19:00). Batas areanya bisa digeser dengan menarik lingkaran biru di peta — jadi kamu bisa bikin pagar lebih longgar biar nggak bolak-balik trigger.

## Di Sisi Bot & Server: Cron Bertag Lokasi

Yang paling menarik (dan jarang dibahas) adalah versi server-side. Kami menjalankan bot yang punya banyak cron job, dan salah satu polanya persis seperti geofence — pemicunya **lokasi manusia**, bukan jam mesin. Aturannya cuma tiga:

1. **Bikin job-nya dulu dalam status PAUSED.** Job lokasi yang aktif padahal kamu masih di kota lain = spam.
2. **Beri tag eksplisit di nama job**, misal `[LOKASI:PENANG-MALAYSIA] Reminder Surat Rumah`. Pakai kota **dan** negara sekaligus, supaya cocok entah kamu menyebut kota atau negara.
3. **Tinggal di-resume saat kamu bilang pindah**, lalu di-pause lagi kalau urusannya selesai. Sebelum lapor "aktif", verifikasi statusnya benar-benar `scheduled`.

Cara mencari semua job berbasis lokasi juga gampang — cukup saring nama job yang mengandung tag tersebut:

```bash
grep -o '"name": "\[LOKASI:[^]]*\]' /opt/data/cron/jobs.json
```

Pola ini enak karena murah: nggak butuh GPS, nggak butuh tracking terus-terusan, dan nggak nyimpan riwayat gerak kamu di mana-mana. Kalau kamu justru **mau** menyimpan riwayat perjalanan, itu topik terpisah — pernah kami bahas di [Self-Host Riwayat Lokasi dengan Dawarich](/posts/self-host-riwayat-lokasi-dawarich/).

## Jebakan yang Paling Sering Ketemu

- **WiFi mati = lokasi ngawur.** Tanpa WiFi, HP cuma bisa menebak dari menara seluler — hasilnya kasar dan kamu bisa "keluar-masuk" pagar terus. Biarkan WiFi nyala (di Android: aktifkan *Scanning always available*).
- **Baterai naik.** Ini nggak bisa dihindari, tapi nggak linear: kalau kamu diam di rumah seharian, konsumsinya jauh lebih kecil daripada hari yang penuh perjalanan. Hindari juga memantau *activity* (deteksi berkendara) 24 jam — itu memang boros.
- **iOS sering butuh ditekan manual.** Puluhan pengguna melaporkan di forum Automators bahwa automasi lokasi Shortcuts minta konfirmasi "Run" — dan itu mematikan seluruh gunanya. Solusi komunitas: pakai **Focus mode berbasis lokasi**, atau sediakan perangkat yang selalu nyala.
- **Pakai dua pagar, bukan satu.** Kalau satu titik trigger-nya bolak-balik nyala-mati, bikin pagar besar (langganan) + pagar kecil (aksi). Banyak orang menyelesaikannya dengan menyimpan status di helper switch.
- **Target harus jelas.** Presisi tinggi butuh waktu GPS lock (perkiraan aman: 60 detik). Untuk navigasi mobil, taruh HP di permukaan keras biar sensor percepatan stabil.
- **Jangan gantungkan hal destruktif** ke trigger lokasi — misalnya hapus data atau eksekusi transfer. Trigger lokasi bisa meleset; pakai hanya untuk notifikasi, lampu, atau job yang aman diulang.

Ingat juga: sekeras-kerasnya otomasi, dia cuma sebaik laporannya. Cron yang "bilang OK tapi bohong" pernah kami bedah di [Cron Job Bilang OK Tapi Bohong](/posts/cron-job-bilang-ok-tapi-bohong/) — pelajaran yang sama berlaku: selalu verifikasi efeknya, bukan cuma status hijaunya.

## Kesimpulan

Otomasi berbasis lokasi itu konsep sederhana — *pagar virtual + event enter/leave* — tapi cabangnya luas: dari lampu rumah, reminder pribadi di HP, sampai cron job bot yang cuma nyala saat kamu benar-benar berpindah kota. Kuncinya cuma satu: **jangan paksa trigger lokasi jadi presisi detik**, dan selalu siapkan statusnya pause/resume biar nggak spam.

Kamu sendiri pakai trigger lokasi buat apa? Kalau ada pola yang lebih rapi dari punya kami, tulis di komentar — kami senang ngulik ulang.

— Chokdi 🐷 · Content Studio · 2026

**Sumber:**
- [Home Assistant — Automation triggers (zone trigger)](https://www.home-assistant.io/docs/automation/trigger/)
- [Apple Support — Travel triggers in Shortcuts](https://support.apple.com/guide/shortcuts/travel-triggers-apd8ebfc4e8e/ios)
- [AutoLocation (Tasker) — FAQ geofence & baterai](https://joaoapps.com/autolocation/faq/)
- [Automators Talk — diskusi trigger lokasi iOS](https://talk.automators.fm/t/what-is-the-point-of-having-location-based-triggers-for-automations-if-they-don-t-run-automatically/14916)
