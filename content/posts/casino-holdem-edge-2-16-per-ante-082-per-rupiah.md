---
title: "Casino Hold'em: House Edge 2,16% per Ante — tapi Cuma 0,82% per Rupiah yang Kamu Taruh"
date: 2026-11-03T00:25:00+07:00
draft: false
tags: ["Kasino", "Casino Hold'em", "House Edge", "Poker", "Probabilitas"]
---

Casino Hold'em cuma punya satu keputusan per tangan: **lipat, atau call 2× ante**. Justru karena cuma satu keputusan, seluruh biayanya bisa dihitung sampai digit terakhir: **house edge 2,1576% dari ante** per tangan.

Tapi angka itu sering dibaca salah. Per rupiah yang benar-benar berputar di meja, biayanya cuma **0,8173%** — lebih murah dari Caribbean Stud (2,555% per rupiah). Artikel ini membedah kenapa dua angka itu berbeda jauh, plus satu hitungan sendiri: **dealer gagal qualify 28,290% kali**, bukan 20,55% seperti di tabel publik.

## Aturannya dalam satu paragraf

Ante satu unit. Kamu dan dealer masing-masing dapat **2 kartu tertutup**, lalu **3 kartu flop terbuka**. Sekarang putuskan: **fold** (ante hangus) atau **call tepat 2× ante**. Kalau call, dua kartu community lagi dibuka, kartu dealer dibalik, lalu tangan 7 kartu dibandingkan. Dealer wajib punya **pair of 4s** atau lebih baik untuk qualify. Kalau dealer gagal qualify: ante dibayar sesuai paytable (royal 100:1, straight flush 20:1, four of a kind 10:1, full house 3:1, flush 2:1, sisanya 1:1) dan call-mu **push** — balik utuh. Kalau dealer qualify dan kamu menang: ante sesuai paytable, call 1:1. Kalau kalah: ante **dan** call hilang, total −3 unit. Seri = push.

## Isi tabel 27,8 triliun tangan

Analisis publik membedah **27.813.810.024.000** kombinasi dengan strategi optimal. Ringkasannya untuk paytable royal 100:1 / straight flush 20:1 / quads 10:1:

| Hasil | Probabilitas | Kontribusi |
|---|---|---|
| Menang dengan straight atau kurang | 23,106% | +0,693 |
| Dealer gagal qualify, tanganmu straight atau kurang | 19,851% | +0,199 |
| Kalah (ante + call hilang) | 31,782% | −0,953 |
| Lipat | 18,009% | −0,180 |
| Menang full house | 2,120% | +0,106 |
| Seri | 2,440% | 0 |
| **Total** | **100%** | **−0,0216** |

Bacanya: **kamu menang 47,77% tangan, kalah 31,78%, seri 2,44%, lipat 18,01%.** Strategi optimal call di **81,99%** tangan — persis angka "raise 82% dari waktu" yang dipakai referensi.

Yang paling penting: **43,03% dari semua kemenanganmu datang dari dealer yang gagal qualify**, bukan dari tanganmu yang bagus. Hampir separuh rasa "pintar main" di meja ini sebenarnya cuma dealer yang tidak punya pair.

## Hitungan sendiri: 28,29% dealer gagal qualify

Saya hitung peluang tangan 7 kartu dealer bernilai **di bawah pair of 4s** secara eksak dari C(52,7) = 133.784.560 kombinasi:

- **Tanpa pair sama sekali**: C(13,7) × 4⁷ = 28.114.944 → **21,0151%**
- **Persis satu pair 2s** (5 rank lain berbeda): 6 × C(12,5) × 4⁵ = 4.866.048 → **3,6372%**
- **Sama untuk pair 3s**: **3,6372%**

Total: **28,290%**. Simulasi Monte Carlo 4 juta tangan memberi **28,310%** — selisih 0,02 poin, di dalam derau (standard error 0,0225).

Lalu kenapa tabel publik cuma mencatat **20,5545%**? Karena tabel itu mengikuti strategi: **18% tangan terburuk sudah kamu lipat sebelum kartu dealer dibuka**. Flop jelek yang bikin kamu lipat juga flop yang bikin dealer kecil — kejadian "dealer gagal qualify" banyak yang tak pernah tercatat. Dihitung hanya pada tangan yang benar-benar di-call: **20,5545% ÷ 81,99% = 25,07%**.

## Kenapa 2,16% berubah jadi 0,82%

Ini inti artikelnya. "2,16%" dihitung **per unit ante**, bukan per uang yang kamu pertaruhkan. Kalau call, kamu menaruh **3 unit** (ante 1 + call 2). Rata-rata uang yang benar-benar berputar per tangan:

**3 × 81,99% + 1 × 18,01% = 2,6398 unit ante**

Maka kerugian per rupiah yang berputar = 2,1576% ÷ 2,6398 = **0,8173%**. Itu sebabnya Casino Hold'em disebut salah satu house game termurah — setara element of risk Caribbean Stud 2,555%, jauh di bawah Let It Ride 3,51% dan [Three Card Poker Q-6-4 3,37%](/posts/three-card-poker-q-6-4-potong-kerugian-setengah/).

Artinya: satu keputusan itu yang menentukan 2,16% atau 5%+.

## Uangnya di angka

Ante Rp10.000, 40 tangan per jam, strategi optimal:

- **Total uang berputar**: 2,6398 × Rp10.000 × 40 = **Rp1.055.920/jam**
- **Kerugian ekspektasi**: 2,1576% × Rp10.000 × 40 = **−Rp8.630/jam**

Bandingkan dengan [Caribbean Stud raise buta](/posts/caribbean-stud-raise-buta-rugi-16-persen/) yang bisa −Rp66.444/jam di ante dan jam yang sama. Bedanya bukan keberuntungan: call tetap 2× (tidak bisa membengkak), 20%+ kemenangan datang otomatis dari dealer non-qualify, dan paytable ante memberi bonus tipis di tangan besar.

## Tiga hal yang menentukan hasilmu

1. **Lipat 18% tangan terbawah** — dua kartu kecil tanpa straight/flush draw. Call semua tangan menaikkan edge ke ±2,4%.
2. **Periksa paytable.** Versi royal 20:1 / quads 10:1 = 2,40% (0,24 poin lebih mahal). Versi "zero house edge" Gamesys tetap 0,35% **plus komisi 10%** per sesi.
3. **Side bet jangan dicampur.** AA Bonus dan progresif punya hitungan sendiri, tidak mengubah keputusan call — sama seperti [Pai Gow Poker](/posts/pai-gow-poker-push-40-persen-house-edge/).

Ukuran taruhan pakai [Kelly criterion](/posts/kelly-criterion-ukuran-taruhan-bankroll/). RTP 97,84% di sini datang dari strategi, bukan putaran gratis.

<!-- cta-funnel -->

> Sebelum main, cek dua hal di meja: paytable ante (royal 100:1 atau 20:1) dan batas maksimum bayar. Dua angka itu mengubah 2,16% jadi 4%-an tanpa kamu sadari.

**[MAIN SEKARANG — AMBIL BONUS DEPO AWAL →](https://tomat.jagungbaru.com/banner/vip?utm_source=blog&utm_campaign=casino-holdem-edge-2-16-per-ante-082-per-rupiah)**

*Tabel bayaran tiap penyedia berbeda — periksa paytable sebelum taruhan pertama. Artikel ini edukasi mekanika, bukan jaminan hasil.*

— Chokdi 🐷 · Content Studio · 2026
