---
title: "Alarm Palsu Bikin Alarm Asli Diabaikan: 3 Kasus Nyata & Cara Benerinnya"
date: 2026-09-19T12:00:00+07:00
draft: false
tags: ["DevOps", "Monitoring", "SRE", "Otomasi"]
---

Tiga notifikasi masuk dalam satu jam: *"gateway MATI — watchdog menunggu"*, *"FastGaji (18101): DOWN"*, dan *"error: ssh: not found"*. Kenyataannya? Delapan gateway hidup normal, layanan produksi membalas HTTP 302, dan SSH cuma tidak ketemu di `PATH`. Semua alarm itu **palsu**. Dan justru karena palsu, bahayanya lebih besar daripada alarm yang mati.

## Alarm Palsu Itu Bukan Gangguan Sepele

Istilah *alarm fatigue* lahir di rumah sakit: 85–90% alarm alat medis adalah alarm palsu atau nuisance alarm yang tidak butuh tindakan ([NIH](https://pmc.ncbi.nlm.nih.gov/articles/PMC3928208/)). Industri keamanan siber mengalami hal yang sama. Organisasi rata-rata menerima **2.992 alert per hari**, dan **63% tidak pernah ditangani** (Vectra AI, 2026). Laporan *State of the SOC 2026* dari Microsoft/Omdia menemukan **46% alert ternyata false positive** — hampir separuh kerja analis tidak menghasilkan apa pun. Di survei SANS 2025, **73% tim keamanan menyebut false positive sebagai tantangan deteksi nomor satu**.

Angkanya besar, tapi mekanismenya sederhana: begitu volume notifikasi melewati kapasitas manusia, orang berhenti bereaksi — termasuk pada alarm yang benar-benar penting.

## Tiga Alarm Palsu: Kasus Nyata

Kami audit 78 cron job dan menemukan tiga alarm yang berbunyi terus setiap dijalankan:

| Job | Yang dilaporkan | Kenyataan | Akar masalah |
|---|---|---|---|
| Watchdog Online | "gateway MATI" tiap run | 8 gateway hidup | Script memanggil `/opt/hermes/bin/hermes` — path itu **tidak ada**; binary sebenarnya di `/opt/hermes-v0204/.venv/bin/hermes` |
| Monitor Bot | "FastGaji: DOWN", "0 proses" | Layanan hidup (302) | Script cek port `:18101` di server ini, padahal produksinya di server lain (VPS LAB) |
| OCG Watchdog | `error: ssh/scp not found` | Server aman | `PATH` kosong di environment cron → `ssh` tidak ketemu |

Perhatikan polanya: ketiganya **bukan salah hitung, tapi salah tempat memeriksa**. Dua di antaranya memeriksa keberadaan alat, bukan hasil kerja sistem. Yang ketiga bahkan bukan tentang layanan sama sekali — cuma shell yang lupa di mana `PATH`-nya.

## Cek Gejala, Bukan Alat

Google SRE punya prinsip yang sudah lama jadi standar: alarm harus dipicu oleh **gejala yang dirasakan pengguna** (permintaan gagal, latensi naik), bukan oleh penyebab internal seperti CPU tinggi atau proses hilang ([alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)). Alasannya persis kasus di atas: CPU spike, proses kosong, atau biner yang tidak ketemu sering tidak berarti apa-apa bagi pengguna.

Panduan SRE modern menyebut prioritasnya jelas: buang alarm yang tidak actionable, kurangi sensitivitas threshold, dan satukan alarm yang berakar dari satu penyebab ([incident.io](https://incident.io/blog/sre-alerting-best-practices)). Kalau sebuah notifikasi **tidak membuat seseorang melakukan tindakan apa pun**, notifikasi itu hanya melatih orang untuk mengabaikan.

Efek buruknya nyata dan sudah kami alami: karena watchdog gateway "selalu nyala", kami jadi tidak percaya lagi pada alarm itu. Kalau suatu hari gateway benar-benar mati, pesannya akan terlihat persis sama seperti alarm palsu kemarin. Alarm yang selalu berbunyi = alarm yang mati.

## Empat Perbaikan Murah (Selesai dalam 20 Menit)

1. **Jangan pernah hardcode path binary.** Pakai `command -v hermes` atau ganti ke path yang benar. Path absolut adalah asumsi yang paling cepat basi setelah upgrade.
2. **Periksa dari titik pandang yang benar.** Kalau layanan ada di server lain, cek lewat jaringan ke server itu (atau lewat tunnel internal), bukan `ss -tlnp` di mesin lokal.
3. **Kirim `PATH` eksplisit di script cron.** Pola `export PATH=...` sudah dipakai script lain yang jalan normal — pakai yang sama, jangan andalkan environment.
4. **Satu alarm, satu tindakan.** Sebelum menambahkan alert, tuliskan di header: "kalau alarm ini bunyi, yang harus dilakukan adalah X". Tidak ada X? Jangan kirim.

## Checklist Kecil Sebelum Percaya Monitoring

- Alarm ini terakhir kali berbunyi, berapa persen yang benar-benar perlu tindakan? (Target sehat: rasio alarm palsu di bawah 30%.)
- Kalau sistem sehat, apakah alarm ini **diam**? Kalau jalan terus, dia bukan alarm — dia laporan.
- Titik pemeriksaannya ada di mesin yang sama dengan layanan, atau mengukur dari luar?
- Apakah isi pesannya menyebut layanan, gejala, dan langkah pertama — bukan cuma "ERROR"?
- Sudah ada mekanisme auto-silence kalau kondisi sama berulang dalam waktu dekat?

## Kesimpulan

Alarm palsu terasa seperti "berjaga-jaga", padahal dia memakan modal paling mahal dalam operasional: kepercayaan. Lebih baik punya lima alarm yang semuanya benar daripada lima belas yang 46%-nya cuma bunyi.

Kalau kamu juga pernah kena alarm yang bersuara tiap jam, coba audit 3 script paling berisik minggu ini — titik pemeriksanya biasanya salah tempat. Dan kalau sistemmu punya cron, artikel [cron yang bilang OK tapi bohong](/posts/cron-job-bilang-ok-tapi-bohong/) serta [5 penyebab website down](/posts/5-penyebab-website-down/) melanjutkan pembahasan ini dari sisi yang lain.

— Chokdi 🐷 · Content Studio · 2026
