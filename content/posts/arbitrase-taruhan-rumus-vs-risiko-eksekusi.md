---
title: "Arbitrase Taruhan: Untung 1,56% Dikunci — Sampai Satu Leg Di-Void dan Rugi 750 Kali Lipat 🔁"
date: 2026-11-14T00:15:00+07:00
draft: false
tags: ["Sportsbook", "Matematika Taruhan", "Arbitrase", "Manajemen Risiko"]
---

# Arbitrase Taruhan: Untung 1,56% Dikunci — Sampai Satu Leg Di-Void dan Rugi 750 Kali Lipat 🔁

Arbitrase taruhan kelihatan seperti celah ajaib: pasang semua kemungkinan hasil di bandar berbeda, lalu untung apa pun yang menang. Matematikanya **memang** benar — dan itu bagian yang paling menipu. Sebab 1,56% yang "terkunci" di kertas bisa lenyap total karena satu hal yang tidak ada di rumus: **eksekusi**.

Artikel ini nunjukin cara hitung sendiri (10 detik, tanpa kalkulator online), berapa laba realistis, dan kenapa satu leg yang di-void bisa menghapus ratusan siklus keuntungan.

## 🧮 Syarat mutlak: total peluang di bawah 100%

Satu bandar tidak pernah memberi arbitrase ke kamu — dia justru menambah margin. Ubah odds desimal jadi peluang dengan `1 / odds`, lalu jumlahkan:

- Bandar A: 1.30 (76,92%) + 3.70 (27,03%) = **103,95%**
- Bandar B: 1.40 (71,43%) + 2.98 (33,56%) = **104,99%**

Dua-duanya di atas 100% = tidak ada arb di dalam satu bandar. Arb baru muncul kalau kamu **silang** odds terbaik dari dua bandar berbeda: ambil 1.40 dari B dan 3.70 dari A → 71,43% + 27,03% = **98,46%**.

Selisih dari 100% itulah margin kamu: `(1 / 0,984556 − 1) × 100` = **+1,57%**.

## 💰 Cara bagi stake biar hasilnya rata

Jangan bagi dua sama rata — odds besar butuh stake lebih kecil. Rumusnya:

`stake_leg = total_stake × (1/odds_leg) ÷ total_semua_(1/odds)`

Untuk modal Rp1.000.000 di contoh di atas: **Rp725.494** di odds 1.40 dan **Rp274.506** di odds 3.70. Cek hasilnya:

- Kandidat 1 menang → Rp1.015.691 (laba Rp15.691)
- Kandidat 2 menang → Rp1.015.691 (laba Rp15.691)

Rata persis. Itu sebabnya disebut "risk-free" — **di atas kertas**.

## ⚠️ Bagian yang tidak ada di rumus: satu leg di-void

Ini yang membunuh pemula. Bandar berhak membatalkan taruhan karena *palpable error* (odds salah tulis), atau pasar ditutup lebih awal. Kalau leg **3.70** di-void, yang tersisa cuma taruhan tunggal Rp725.494 di odds 1.40:

- Menang → laba **Rp15.691** (sama seperti rencana)
- Kalah → **minus Rp1.000.000**

Sekarang hitung rasio yang sebenarnya. Laba per siklus = 1,57% × Rp1.000.000 ≈ **Rp15.700**. Kerugian satu kali skenario itu = **Rp1.000.000**. Artinya satu kegagalan eksekusi menghapus sekitar **64 siklus** laba bersih — dan itu baru satu leg, belum hitungan modal yang nyangkut.

Kalau modalnya Rp1.500.000 dengan stake besar 75% (Rp1.125.000), eksposur itu setara **750 siklus** laba Rp1.500. Bandar tidak perlu nakal; cukup satu *palpable error* untuk menutup semua kerja tiga bulan.

## 📉 Odds bergerak: arb 1,57% bisa jadi nol dalam 30 detik

Arb hidup dari selisih waktu update antar bandar — detik, bukan menit. Simulasi pergeseran pada leg 3.70:

| Odds leg kedua | Total peluang | Status |
|---|---|---|
| 3.70 (kutipan awal) | 98,46% | Arb +1,57% |
| 3.65 | 98,83% | Arb +1,19% |
| 3.60 | 99,21% | Arb +0,80% |
| 3.50 | 100,00% | **Bukan arb** (nol) |

Turun 0,20 poin saja = seluruh keuntungan hilang. Kalau leg kedua terlanjur dipasang lebih dulu dan leg pertama sudah berubah, kamu bukan lagi arbitraser — kamu pemegang satu taruhan tunggal.

## 🧱 Tiga tembok nyata di lapangan

1. **Limit stake.** Arb selalu lahir di harga "aneh" yang justru paling ketat limitnya. Kalau leg mahal cuma boleh Rp200.000, seluruh posisi harus dipotong — laba 1,57% dari Rp1.500.000 (Rp23.500) jadi tinggal separuh atau kurang.
2. **Pola taruhan terdeteksi.** Bertaruh dua sisi pasar yang sama berulang-ulang adalah tanda tangan arbitrase. Bandar membatasi atau menutup akun yang konsisten begitu pola terlihat — bukan karena legal, tapi karena mereka tidak mau jadi sisi yang kalah harga.
3. **Modal terkunci di banyak akun.** Untuk menangkap peluang, dana harus sudah parkir di 5–10 bandar. Uang itu tidak produktif, dan satu akun bermasalah = satu kaki hilang dari strategi.

## 🔍 Arb vs taruhan +EV: beda filsafat

| Aspek | Arbitrase | +EV / value bet |
|---|---|---|
| Sumber untung | Selisih harga antar bandar | Harga lebih tinggi dari peluang sebenarnya |
| Laba per transaksi | 1–3% | 2–10% edge per taruhan |
| Risiko | Nol *kalau* semua leg jadi di harga kutipan | Bisa kalah per taruhan |
| Kebutuhan modal | Tinggi (dua sisi + banyak akun) | Rendah (satu sisi) |
| Frekuensi | Jendela detik, makin langka | Lebih sering, lebih tahan lama |

## ✅ Cara pakai yang waras

- **Anggap ini latihan harga, bukan mesin uang.** Sebelum pasang apa pun, jumlahkan `1/odds` semua leg; kalau ≥ 1,00 jangan disentuh.
- **Cek limit dulu, hitung stake belakangan.** Arb yang tidak bisa dieksekusi penuh bukan arb.
- **Ukur dalam siklus, bukan persen.** Laba Rp15.700 terasa manis sampai eksposur Rp1.000.000 ada di meja.

Arbitrase bukan tipuan — rumusnya jujur. Yang menipu adalah perasaan "pasti untung" yang membuat orang melewatkan bahwa **1,57% di kertas butuh eksekusi 100% sempurna** untuk jadi uang nyata. Hitung dulu, baru pasang.

Kalau mau memperdalam sisi hitungannya, baca [overround: margin bandar 1X2](/posts/overround-margin-bandar-1x2-persen/) dan [cash-out yang memotong equity 9%](/posts/cash-out-taruhan-potong-equity-9-persen/). Untuk ukuran taruhan yang proporsional, lihat [Kelly Criterion dan bankroll](/posts/kelly-criterion-ukuran-taruhan-bankroll/).

— Chokdi 🐷 · Content Studio · 2026

**Sumber:** [Smarkets Help — How to calculate arbitrage betting](https://help.smarkets.com/hc/en-gb/articles/115001175531-How-to-calculate-arbitrage-betting) (contoh cross-match 1.40/3.70, margin gabungan dan rumus pembagian stake), [SharpAPI — Sports Betting Arbitrage Explained](https://sharpapi.io/learn/sports-betting-arbitrage-explained) (syarat ∑ peluang < 100%, profit%, risiko limit akun dan jendela peluang 30 detik–5 menit), [TheRundown — Arbitrage betting math](https://therundown.io/blog/arbitrage-betting) (rumus stake proporsional, risiko void dan *palpable error*), [Oddsshopper — Arbitrage Betting Mistakes](https://www.oddsshopper.com/articles/betting-101/arbitrage-betting-mistakes) (limit pada harga outlier), perhitungan mandiri atas semua angka di tabel dan simulasi pergeseran odds.
