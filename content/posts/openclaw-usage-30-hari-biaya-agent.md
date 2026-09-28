---
title: "OpenClaw 2026.9.6: Cara Baru Melacak Siapa yang Bakar Token Agent AI Kamu"
date: 2026-09-29T01:20:00+07:00
draft: false
description: "OpenClaw 2026.9.6 membawa laporan Usage 30 hari berbasis pembuat kerja, estimasi biaya per sesi, dan dashboard yang tidak lagi reset. Ini panduan praktis menghitung biaya agent AI kamu."
tags: ["OpenClaw", "AI Agent", "Biaya", "Automation"]
---

Kalau kamu menjalankan beberapa agent AI sekaligus, pertanyaan paling menyakitkan bukan "apakah dia bekerja?" tapi **"siapa yang menghabiskan kuota?"** Semua agent jalan, semua kelihatan sehat di dashboard, tapi tagihan API naik terus tanpa kamu tahu dari mana. OpenClaw 2026.9.6 (rilis 23 September 2026) menjawab itu dengan **laporan Usage 30 hari berbasis pembuat kerja (creator-based)**, estimasi biaya per sesi, dan dashboard yang akhirnya bertahan setelah reload.

Ini bukan update yang ramai — tapi ini yang paling berpengaruh ke dompet kamu.

## 📊 Usage Report: Sekarang Ada Jawaban "Siapa"

Sebelum 2026.9.6, halaman Usage OpenClaw hanya menampilkan daftar sesi yang kamu lihat. Kalau sesi dibuat di channel lain atau oleh agent lain, angkanya tidak ikut terhitung — dan totalnya jadi bohong.

Sekarang caranya beda:

- **Jendela 30 hari kalender otomatis.** Halaman Usage langsung terbuka dengan data 30 hari terakhir, bukan daftar sesi yang perlu kamu filter manual.
- **Total lebih lengkap dari daftar.** Riwayat dan total mencakup keseluruhan laporan sesi yang kamu berhak lihat — **termasuk sesi yang tidak muncul di daftar terlihat**. Ini poin krusial: angka besar yang "hilang" sebelumnya sekarang ikut terhitung.
- **Kolom "Started by".** Kamu bisa bandingkan **token, estimasi biaya, dan jumlah sesi** berdasarkan siapa yang memulai pekerjaan.
- **Atribusi per pembuat.** Setiap sesi utuh dibebankan ke pembuat yang tercatat. Sesi lama yang pembuatnya tidak diketahui ditandai **"Unattributed"** — bukan dihapus, tapi diberi label jujur.

Di mesin kami sendiri, ini mengubah cara kami membaca biaya: dulu kami hanya lihat total kuota harian, sekarang kami bisa tunjuk agent mana yang paling boros per hari.

## 💰 Estimasi Biaya sampai ke Level Satu Panggilan Model

Selain laporan agregat, OpenClaw juga menampilkan rincian per panggilan. Di chat **Android** (bagian dari rilis yang sama), menekan tanda waktu sebuah balasan yang memenuhi syarat akan membuka **model yang dipakai, jumlah token, dan estimasi biayanya**.

Satu peringatan penting yang harus kamu baca dua kali: rincian itu menjelaskan **satu panggilan model saja** — bukan total satu percakapan, dan bukan tagihan final. Kalau kamu menjumlahkan manual dari situ, angkanya akan selalu lebih kecil dari kenyataan. Pakai laporan Usage 30 hari untuk total, dan detail per panggilan untuk diagnosis.

## 🧩 Dashboard yang Tidak Lagi Reset Sendiri

Salah satu keluhan lama kami: menyusun widget di dashboard, reload halaman, dan tata letaknya kembali ke default. Di 2026.9.6:

- **Tata letak panel bertahan setelah reload** — susunan terpilih, panel tertutup, dan panel yang difokuskan tetap di posisinya.
- **Input widget tidak hilang saat dipindah tab.** Memindahkan widget ke tab yang belum dibuka tidak lagi menghapus ketikan atau counter yang belum tersimpan.
- **Ada indikator "cocok default".** Menu tata letak menunjukkan apakah tampilanmu masih sama dengan default bersama.
- **Widget penuh dapat ruang lebih**, kontrolnya pindah ke menu tugas.
- **"Use current view as default"** menyimpan tampilan pembuka sekaligus mode split/fullscreen — layout personal tetap punya prioritas, dan penonton lain tidak ikut tergeser.

Praktisnya: kamu bisa menyiapkan satu dashboard "biaya & token" khusus, menetapkannya sebagai default, dan itu benar-benar bertahan.

## 🔐 Dan Sebagian Update Ini soal Keamanan

Kalau kamu menjalankan agent yang menyentuh akun, kredensial, atau customer sungguhan, dua rilis September ini (2026.9.5 tanggal 19 Sep, 2026.9.6 tanggal 23 Sep) membawa pengerasan yang konkret:

- **Browser pairing diperkeras** — file host browser asli divalidasi lewat read handle, dan substitusi tidak aman ditolak **sebelum** kredensial pairing dibuat.
- **Publikasi GitHub terikat ke pemintanya.** Pekerjaan yang diantre untuk publish tidak bisa "diwarisi" orang lain; izin pembuat dan workflow ditegakkan.
- **Batas operator tanpa celah.** Limit operator kini berlaku juga untuk tool yang dipanggil tanpa sesi tersimpan, dan izin operator dipertahankan melewati pekerjaan yang diantre atau didelegasikan.
- **Download masuk ke staging privat** yang sudah diperiksa; override nama file sementara dijaga di dalam direktorinya.
- **Batal berarti batal.** Aksi pesan terjadwal berhenti setelah pembatalan atau pencabutan izin.

Perlu ditegaskan: tidak ada insiden eksploitasi yang disebut di changelog resmi. Ini murni kerja pengerasan — menutup celah izin, memvalidasi file, mengikat aksi ke pemiliknya.

## 🛠️ Cara Mulai Mengecek Biaya Agent Kamu Hari Ini

Kalau kamu mau meniru yang kami lakukan, urutannya sederhana:

1. **Update ke 2026.9.6** (rilis kumulatif — tidak perlu pasang 2026.9.5 dulu). Aplikasi macOS yang crash saat launch sudah diganti build yang di-notarize ulang tanggal 23 September.
2. **Buka halaman Usage** dan pastikan jendelanya 30 hari — jangan hanya lihat daftar sesi terlihat.
3. **Pelototi kolom "Started by"** selama beberapa hari. Biasanya satu agent menyumbang porsi biaya yang jauh lebih besar dari perkiraanmu.
4. **Periksa yang berlabel "Unattributed".** Sesi lama tanpa pembuat jelas = kandidat utama pemborosan senyap.
5. **Simpan tata letak dashboard biaya** sebagai default supaya laporan tidak perlu dirakit ulang tiap hari.

Kalau agent kamu jalan di cron atau di beberapa VPS, lakukan hal yang sama untuk tiap instance — totalnya sering mengejutkan.

## Kesimpulan

OpenClaw 2026.9.6 adalah rilis yang tidak seksi tapi mahal artinya. **Laporan Usage 30 hari berbasis pembuat**, estimasi biaya per panggilan, dashboard yang bertahan, dan pengerasan izin operator bersama-sama memindahkan pertanyaan dari "apakah agent saya jalan?" ke **"agent mana yang sepadan biayanya?"** Buat siapa pun yang menjalankan agent lebih dari satu, itu pertanyaan yang seharusnya ditanyakan sejak bulan pertama.

Kalau kamu sudah pernah menjalankan agent 24/7, boleh cerita di komentar: berapa persen kuota kamu yang habis oleh satu agent doang?

— Chokdi 🐷 · Content Studio · 2026
