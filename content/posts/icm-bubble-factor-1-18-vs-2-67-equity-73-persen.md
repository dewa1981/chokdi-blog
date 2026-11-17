---
title: "ICM Bubble Factor: 1,18 di Hand Pertama, 2,67 di Gelembung — Kok Bisa Butuh 73% Equity Buat Call?"
date: 2026-11-17T18:05:00+07:00
draft: false
tags: ["Poker", "Turnamen", "ICM", "Matematika", "Strategi"]
---

Kalau kamu main turnamen poker dan masih memakai pot odds gaya cash game, kamu sedang membakar uang tanpa sadar. Di cash game, 500 chip ya 500 chip. Di turnamen, 500 chip yang sama bisa bernilai jauh berbeda tergantung **posisi kamu di klasemen dan struktur hadiah**. Alat ukur paling praktis untuk itu namanya **bubble factor**.

Bubble factor (BF) adalah angka yang memberi tahu berapa besar kerugian equity turnamen kalau kamu kalah all-in, dibandingkan berapa besar keuntungan equity kalau kamu menang. Angkanya selalu di atas 1 — karena di turnamen, kehilangan chip selalu lebih sakit daripada enaknya menambah chip.

## 🎯 Rumusnya Cuma Dua Baris

Bubble factor didefinisikan sebagai rasio antara equity yang hilang saat kalah dan equity yang didapat saat menang:

**BF = (EV sekarang − EV kalah) ÷ (EV menang − EV sekarang)**

Dari situ, equity minimum yang kamu butuhkan untuk call all-in bisa didekati dengan:

**Equity dibutuhkan = BF ÷ (BF + 1) × 100%**

Jadi kalau BF = 1, kamu butuh tepat 50% — inilah dunia cash game. Kalau BF = 2, kamu butuh 66,7%. Kalau BF = 3, kamu butuh 75%. Semakin besar tekanannya, semakin sempit tangan yang layak kamu pertahankan.

Konsep ini dipopulerkan Lee Nelson, Steven Heston, dan Tysen Streib lewat buku *Kill Everyone* (2009), lalu hidup lagi di era solver karena GTO Wizard dan ICMIZER menampilkannya langsung sebagai matriks antar pemain.

## 🧮 Contoh Pertama: SNG $100, 10 Pemain, BF = 1,18

Ambil contoh mainan dari GTO Wizard: turnamen 10 pemain, buy-in $100, tumpukan 1.000 chip, hadiah $500/$300/$200. Sebelum kartu dibagi, equity semua orang persis $100.

Sekarang SB dan BB all-in di hand pertama, dan SB kalah. Yang menang tidak mendapat $100 penuh — equity-nya naik ke **$184,44**, artinya cuma **+$84,44**. Yang kalah kehilangan **$100**.

BF = 100 ÷ 84,44 = **1,18**. Equity yang dibutuhkan untuk call = 1,18 ÷ 2,18 = **54,1%**.

Perhatikan: ini baru **hand pertama**, belum ada uang hadiah yang dibagikan, tapi kamu sudah butuh 54% equity — bukan 50%. Selisih 4,1 poin persen itu disebut **risk premium**, dan itu sebabnya orang bilang "ICM berlaku sejak hand pertama". Banyak pemain mengira ICM cuma soal gelembung. Salah.

## 📊 Contoh Kedua: BB 4.000 Chip, BF = 2,67 → Butuh 73%

Contoh dokumentasi ICMIZER lebih tajam. Sebuah SNG 9-max di fase gelembung (3 hadiah). BB punya 4.000 chip, equity awalnya **29,23%** dari prize pool.

- Kalau kalah all-in lawan UTG yang menutupi tumpukannya: equity jadi **0%**.
- Kalau menang: tumpukan baru hanya bernilai **40,16%** — dan itu pun belum menjamin masuk uang.

BF = (29,23 − 0) ÷ (40,16 − 29,23) = 29,23 ÷ 10,93 = **2,67**.

Equity call minimum = 2,67 ÷ 3,67 = **72,75%**. Solver kemudian menjawab: calling range-nya **99+**, dan 99 sendiri punya sekitar 72% equity lawan range push CO yang sangat lebar. Cocok.

Artinya: menang 4.000 chip cuma menambah 10,93 poin prize pool, tapi kalah 4.000 chip menghapus 29,23 poin. Chip-nya sama, harganya tidak.

## 📈 Tabel Cepat: BF vs Equity yang Dibutuhkan

| Bubble Factor | Equity minimum call | Konteks khas |
|---|---|---|
| 1,00 | 50,0% | Cash game / Spin & Go 1 hadiah |
| 1,18 | 54,1% | Hand pertama MTT, stack rata |
| 1,50 | 60,0% | Fase menengah, stack menengah |
| 1,60 | 61,5% | Rata-rata saat gelembung uang |
| 2,00 | 66,7% | Short stack hadapi big stack |
| 2,67 | 72,8% | BB 4.000 chip di gelembung SNG |
| 3,00 | 75,0% | Satelit / ladder hadiah tajam |

Pola pentingnya: BF naik pelan dari hand pertama, memuncak sekitar **1,6 di gelembung uang**, lalu turun setelah semua orang masuk uang.

## 🗡️ Sisi Sebaliknya: Bubble Factor Itu Senjata

BF bukan cuma angka pertahanan. Di meja yang sama, GTO Wizard menunjukkan BTN punya BF paling kecil dan boleh call **9,4%** range lawan push lebar; SB hanya **3,5%**; sementara BB dengan tumpukan terbesar punya BF **2,7** dan cuma bisa call **2,7% tangan teratas**.

Baca ulang: pemain dengan tumpukan paling besar justru paling takut, karena equity-nya yang besar paling mahal untuk dipertaruhkan. Itu celah agresinya. Menekan big stack di gelembung sering lebih menguntungkan daripada menekan short stack yang sudah nyaris mati — modalnya bukan kartu bagus, tapi kesabaran membaca siapa yang punya sesuatu untuk dijaga.

## ⚠️ Tiga Kesalahan yang Mahal

1. **Pakai pot odds cash game di turnamen.** Calling 2:1 karena "odds-nya bagus" mengabaikan fakta bahwa losing cost > winning gain.
2. **Hitung bubble factor di meja.** Tidak realistis. Pakai di luar meja untuk melatih heuristik, lalu bawa pola: short stack = longgar, mid stack = ketat, big stack lawan mid stack = tekanan.
3. **Anggap ICM cuma soal gelembung.** Lihat contoh pertama: hand pertama pun BF sudah 1,18.

Kalau kamu mau memperdalam dasar matematikanya, mulai dari [Kelly Criterion untuk ukuran taruhan](/posts/kelly-criterion-ukuran-taruhan-bankroll/) dan [rule 2-4 untuk hitung outs](/posts/pot-odds-outs-poker-rule-2-4/). Untuk perbandingan game meja yang house edge-nya sudah dipatok kasino, lihat [Caribbean Stud dan raise 2x yang cuma dibayar 15%](/posts/caribbean-stud-poker-raise-2x-dibayar-15-persen/).

## 🎯 Kesimpulan

Bubble factor mengubah satu pertanyaan sederhana — "berapa equity saya?" — jadi pertanyaan yang benar: **"berapa equity yang saya pertaruhkan dibanding yang saya bisa menangkan?"** Di hand pertama jawabannya 1,18. Di gelembung bisa 2,67. Di satelit bisa lebih dari 3.

Angka itu bukan teori akademis. Itu selisih antara call yang benar dan call yang menghapus tiga jam kerja kamu di meja.

— Chokdi 🐷 · Content Studio · 2026
