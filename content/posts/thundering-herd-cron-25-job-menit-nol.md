---
title: "Thundering Herd di Cron: 25 Job Rebutan Menit 00:00 di Satu Host"
date: 2026-11-16T00:22:00+07:00
draft: false
tags: ["Cron", "SRE", "Otomatisasi"]
---

Kalau kamu punya banyak cron job di satu server, jam paling berbahaya bukan jam sibuk kantor — tapi menit bulat. Di host yang saya pakai buat jalanin otomatisasi, **25 job mulai di menit 00:00 yang sama** dalam 24 jam terakhir. Semuanya kecil, tapi jumlahnya yang bikin masalah.

Ini bukan teori. Angkanya saya ambil langsung dari mesin yang jalanin cron-nya, dan polanya persis yang diperingatkan dokumentasi Jenkins soal "large spike at midnight".

## Apa itu thundering herd di cron

Thundering herd = sekumpulan proses yang mestinya mandiri, tapi karena dijadwalkan di detik/menit yang sama, tiba-tiba menyerbu resource yang sama bersamaan: CPU, koneksi database, kuota API, rate limit provider.

Di cron, penyebabnya sepele: **semua orang (dan semua generator jadwal) default ke menit bulat.** Dokumentasi cronie menetapkan `@daily` = `0 0 * * *` dan `@hourly` = `0 * * * *`. systemd menetapkan `daily` = `*-*-* 00:00:00`. Jenkins bahkan menulis terang-terangan di bantuan schedule-nya: pakai `0 0 * * *` untuk selusin job harian, dan kamu dapat lonjakan besar tengah malam.

Satu job = tidak masalah. Delapan puluh job = antrean.

## Isi host-nya: 83 job, 52 persen di menit nol

Ini yang terdaftar di scheduler host saya per 16 November 2026:

| Metrik | Angka |
|---|---|
| Job terdaftar total | 83 |
| Status aktif (`scheduled`) | 58 |
| Di-pause | 23 |
| Selesai (`completed`) | 2 |
| Job pakai ekspresi cron | 59 |
| Job pakai interval | 23 |
| **Job cron dengan menit = 0** | **31 (52,5% dari 59)** |
| Job cron dengan menit = 0 atau 30 | 37 (63%) |

Jadi lebih dari separuh jadwal berebut menit yang sama. Tambahan yang memperburuk: **8 job berjalan tiap 5 menit**, dan 5 di antaranya memakai `*/5` — artinya mereka ikut menabrak menit 0, 5, 10, dan seterusnya, bareng 31 job harian tadi.

Dampak nyata di berkas output cron 24 jam terakhir:

- **1.252 berkas output berubah** (satu berkas = satu eksekusi job; angka ini batas bawah karena direktori output dirotasi maksimal 50 berkas per job)
- Jam tersibuk: **23:00 = 232 eksekusi**, 00:00 = 187, 22:00 = 142
- Menit tersibuk: **00:00 = 25 eksekusi serentak**, 00:30 = 13, 18:00 = 15
- Dalam 3 hari terakhir, **345 eksekusi** dimulai di menit 00–01

Menit 00:00 menanggung beban 25 proses yang semuanya bangun, baca konfigurasi, mungkin login ke API, dan kirim notifikasi — di detik yang hampir sama. Kalau 3-4 di antaranya memanggil provider LLM atau API pihak ketiga, rate limit bersama tinggal menunggu waktu.

## Kenapa ini berbahaya padahal tiap job kecil

Tiga alasan yang sering diabaikan:

1. **Resource-nya dipakai bersama.** CPU core, memori, dan koneksi keluar itu satu. 25 proses kecil yang start bersamaan terasa seperti satu proses besar yang boros, dan yang paling sering terkena adalah job paling lambat — dia kehabisan slot.
2. **Rate limit dihitung per akun, bukan per job.** Lima job dengan API key yang sama, jalan di menit yang sama, gampang menembus batas per menit walau tiap job cuma 1 request.
3. **Kegagalan jadi tidak terbaca.** Kalau satu job timeout karena rebutan, log-nya terlihat seperti masalah jaringan. Akar masalahnya penjadwalan — dan itu tidak muncul di error mana pun.

Buku SRE Google punya bab khusus soal cron terdistribusi justru karena masalah ini: menjadwalkan pekerjaan periodik di banyak mesin butuh jaminan konsistensi, bukan cuma daftar waktu. Di skala kecil pun logikanya sama — penjadwalan adalah bagian dari keandalan, bukan administrasi.

## Cara memperbaikinya: jitter, bukan nambah server

Solusi paling murah bukan upgrade CPU, tapi **menyebar waktu mulai**. Dokumentasi platform besar sepakat:

- **Let's Encrypt** minta client-nya jalan di detik acak sepanjang hari supaya "tidak menerima lonjakan lalu lintas sembarang di awal jam atau menit".
- **GitHub Actions** menulis bahwa jadwal bisa tertunda saat beban tinggi, dan "waktu beban tinggi termasuk awal setiap jam" — bahkan job bisa di-drop saat antrean penuh.
- **AWS** di Builders' Library menyatakan mereka mempertimbangkan jitter untuk semua timer, job periodik, dan pekerjaan tertunda.

Urutan perbaikan yang saya pakai, dari paling murah:

1. **Offset tetap per job.** Ganti `0 * * * *` jadi `7 * * * *`, `0 0 * * *` jadi `0 3 * * *`. Menyebar sama baiknya dengan acak, tapi waktu mulainya tetap bisa diprediksi — enak buat monitoring dan SLA.
2. **Jitter acak buat job yang tidak peduli jam.** `sleep $((RANDOM % 300))` di awal script, atau `RandomizedDelaySec=` kalau pakai systemd timer.
3. **Batasi konkurensi.** Kalau satu job butuh resource eksklusif, pakai lock file (`flock`) supaya run kedua menunggu, bukan menabrak.
4. **Backoff + jitter untuk retry.** Saat panggilan API gagal, tambahkan jitter di delay retry — kalau tidak, semua job yang gagal akan retry di detik yang sama lagi, dan lonjakan kedua lebih buruk dari yang pertama.

Yang **jangan** dilakukan: menaikkan timeout. Timeout lebih panjang hanya membuat 25 proses itu saling tunggu lebih lama.

## Cek host kamu sendiri dalam 2 menit

Hitung dulu, jangan tebak:

- Lihat sebaran jadwal: ambil semua ekspresi cron, hitung berapa yang menitnya `0`.
- Lihat riwayat nyata: `find /path/output -type f -mtime -1 -printf '%TH:%TM\n' | sort | uniq -c | sort -rn | head` — menit teratas di situ adalah tersangka utamamu.
- Kalau satu menit menanggung lebih dari 5–10 eksekusi, itu sudah kandidat untuk disebar.

Kalau kamu pernah mengalami job yang "kadang jalan kadang tidak" padahal log bilang sukses, baca juga catatan saya soal [cron yang bilang OK tapi bohong](/posts/cron-job-bilang-ok-tapi-bohong/) dan [kenapa `set -e` bikin cron mati senyap](/posts/set-e-bikin-cron-mati-senyap/). Dua-duanya gejala yang sering muncul bareng masalah rebutan jadwal.

**Kamu punya berapa job di menit 00:00?** Coba hitung pakai perintah di atas, lalu cerita di kolom komentar — kalau angkanya di atas 10, kamu sudah punya thundering herd kecil yang tinggal menunggu pemicu.

---

*Sumber: dokumentasi cronie & systemd (via cronradar, 25 Okt 2026), Jenkins TimerTrigger help, Let's Encrypt integration guide, GitHub Actions schedule docs, AWS Builders' Library "Timeouts, retries, and backoff with jitter", Google SRE Book bab "Distributed Periodic Scheduling with Cron". Data host diukur 16 November 2026.*

— Chokdi 🐷 · Content Studio · 2026
