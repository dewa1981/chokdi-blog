---
title: "2 Bulan, 13 Rilis Hermes Agent: Kenapa Agent AI Sekarang Butuh Tim, bukan Robot Pintar"
date: 2026-09-29T16:05:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Multi-Agent", "Agent AI"]
---

Selama dua bulan terakhir, Hermes Agent merilis **13 versi** — dan angka itu bikin bingung: kok bisa secepat itu? Yang lebih menarik, hampir semua perubahan besar di periode ini mengarah ke satu hal yang sama: **agent AI berhenti jadi robot pintar tunggal, dan mulai jadi tim**.

Kalau kamu cuma pakai agent AI buat kerjaan harian di Indonesia, ada tiga hal dari periode ini yang benar-benar mengubah cara kerja kamu.

## 📊 Dulu vs Sekarang: Angka yang Bicara

Data per 18 September 2026 dari laporan komunitas Hermes Atlas, ditambah pengecekan langsung ke repo GitHub:

- **Bintang GitHub: 216.354 → 249.932** (cek langsung 29 Sep 2026)
- **Fork: 40.502 → 53.285**
- **Rilis baru dalam 2 bulan: 13 tag** (dari v0.19.0 sampai v0.21.3, lalu lanjut ke v0.21.5)
- **Ekosistem sekitar repo: 203 → 250 proyek** yang dilacak komunitas

Yang penting bukan angka bintangnya. Perhatikan ini: **bintang naik ~14%, tapi fork naik ~28%** — dua kali lebih cepat.

Artinya sederhana. Orang berhenti cuma "melihat" dan mulai **memasang, mengubah, dan menyambung** agent ini ke sistem mereka sendiri. Buat kamu yang usaha di Indonesia, sinyalnya jelas: ini bukan mainan demo, ini alat kerja yang dipakai beneran.

Yang paling tumbuh justru bagian yang bikin agent bisa dipakai berulang — **skill, memori, dan workspace** menyumbang sekitar **70% dari seluruh pertumbuhan ekosistemnya**.

## 🚀 Rekapan 4 Babak: 13 Rilis dalam 2 Bulan

Kecepatan rilis ini sebenarnya punya alur yang rapi, bukan asal tembak:

- **v0.19 "Quicksilver" — lambat itu mahal.** Waktu tunggu dari perintah dikirim sampai agent mulai kerja dipangkas dari ~4,3 detik jadi ~0,9 detik (turun ~80%). Buat dipakai puluhan kali sehari, ini bedanya antara "enak dipakai" dan "malesin".
- **v0.20 "Herald" — agent dapat suara dan protokol.** Voice real-time, bisa dipotong di tengah bicara, wake word, plus **A2A** (komunikasi antar agent) dan webhook bertanda tangan.
- **v0.21 "Pantheon" — multi-agent jadi gampang dibaca.** Bot Mode jadi fitur bawaan, tiap profile punya nama dan identitas, dan kamu bisa bikin **group chat berisi beberapa agent** — mention satu-satu, lihat siapa bilang apa. Ada juga perintah `hermes peer` buat nyambung antar gateway.
- **Babak penguatan — tagihan kecepatan.** v0.21.0 menulis ulang cara sesi menyimpan data. Hasilnya beberapa instalasi kena masalah: penulis kedua saling membatalkan lock, database sehat dilaporkan korup. Ditutup di v0.21.2 dengan **44 issue** diselesaikan.

Babak keempat inilah pelajaran paling mahal — dan paling penting buat kamu yang mau serius pakai agent AI.

## 🧠 Pelajaran Terbesar: Simpan Data Itu Titik Paling Rawan

Semua fitur keren (voice, group chat, delegasi) bergantung pada satu hal yang kelihatan sepele: **file penyimpanan sesi**.

Kalau bagian ini rusak, yang terjadi bukan error keren — tapi **kegagalan senyap**:

- Agent "lupa" percakapan sebelumnya, padahal catatannya masih ada
- Dashboard bilang sehat, tapi session list kosong
- Dua proses nulis bersamaan → satu mencatat, satunya batal

Pelajaran praktis buat kamu yang jalanin agent di kantor atau usaha sendiri:

- **Kalau jalanin agent, batasi satu penulis.** Jangan buka panel, cron, dan CLI yang semuanya menulis ke database yang sama tanpa aturan.
- **Backup database sesi sebelum update** — bukan sesudah masaalah muncul.
- **Jangan percaya "hijau"** — metrik sehat itu bukan bukti data utuh. Tes: cari satu percakapan lama, pastikan masih bisa dibuka.

## 🗓️ Cron yang Punya Ingatan: Kenapa Ini Penting buat Bisnis

Fitur yang paling sering diabaikan padahal paling berguna buat pemilik usaha adalah perubahan di **cron job**.

Dulu tugas terjadwal cuma jalan dan selesai — hasilnya lewat begitu saja. Sekarang jadwal bisa:

- **Memuat dan memperbarui memori** antar run (jadi tidak mulai dari nol tiap pagi)
- **Membawa hasil run sebelumnya** ke run berikutnya, dengan `continuity=true`
- **Punya scratchpad permanen** sendiri
- **Diam total** kalau sumbernya belum berubah (mode monitor) — hemat biaya token

Bayangkan laporan harian bisnis yang mengingat apa yang sudah dilaporkan kemarin, jadi tidak mengulang hal sama. Kamu tinggal baca yang berubah. Itu bedanya tugas otomatis yang melelahkan dengan yang benar-benar meringankan.

## 🎯 Cara Belajar dari Kecepatan Rilis Semacam Ini

13 rilis dalam 2 bulan terdengar mengerikan bagi yang takut ketinggalan. Sebenarnya tidak perlu dikejar semua. Pakai saringan ini:

1. **Baru pasang kalau patch-nya soal data atau keamanan.** Fitur baru bisa ditunggu; perbaikan integritas data tidak.
2. **Pilih 1 versi tiap bulan, jangan tiap tag.** Loncat 2-3 versi sekaligus lebih hemat waktu daripada update setiap minggu.
3. **Baca bagian "patch release" saja.** Catatan rilis telaknya sengaja ditahan untuk versi besar berikutnya, jadi tidak ada gunanya panik tiap tag keluar.
4. **Tulis perubahan penting ke catatanmu sendiri.** Update secepat ini membuat dokumentasi pihak ketiga selalu tertinggal.

## ✨ Kesimpulan

Bulan Juli, pertanyaan besarnya adalah *"apakah agent AI bisa dipercaya?"*. Bulan September, pertanyaannya sudah berubah jadi *"bagaimana mengatur banyak agent supaya bisa dikoordinasi dan diperiksa?"*.

Itu pergeseran yang bagus untuk kita. Artinya alat ini sedang jadi lebih mudah dipakai siapa saja yang punya pekerjaan berulang — bukan cuma buat yang jago ngoding.

Kamu sendiri sudah pakai agent AI buat kerjaan apa? Tulis di komentar, siapa tahu jadi ide artikel berikutnya.

— Chokdi 🐷 · Content Studio · 2026
