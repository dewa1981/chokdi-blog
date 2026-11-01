---
title: "Three Card Poker: Aturan Q-6-4 Memotong Kerugian dari 7,65% ke 3,37%"
date: 2026-11-01T18:05:00+07:00
draft: false
tags: ["Kasino", "Three Card Poker", "House Edge", "Probabilitas"]
---

Tiga kartu di tanganmu, tiga kartu di tangan dealer, dan satu keputusan: naikkan taruhan atau buang. Tidak ada hitungan kartu, tidak ada tabel strategi 200 baris. Tapi justru di meja sesederhana ini ada satu aturan yang nilainya **lebih dari separuh kerugian**: buang semua tangan di bawah Q-6-4.

Di bawah ini semuanya dihitung ulang dari 22.100 kombinasi tiga kartu, bukan dikutip dari brosur. Hasilnya cocok persis dengan angka yang dipublikasikan — dan satu angka yang sering dikutip orang ternyata bukan angka yang mereka kira.

## 22.100 tangan, dan satu urutan yang dibalik

Tiga kartu dari 52: C(52,3) = **22.100** kemungkinan. Kalau diurutkan:

| Tangan | Kombinasi | Peluang |
|---|---|---|
| Straight flush | 48 | 0,2172% |
| Three of a kind | 52 | 0,2353% |
| **Straight** | **720** | **3,2579%** |
| **Flush** | **1.096** | **4,9593%** |
| Pair | 3.744 | 16,9412% |
| High card | 16.440 | 74,3891% |

Dua hal yang bikin Three Card Poker beda dari poker biasa. Pertama, **straight mengalahkan flush** — bukan sebaliknya seperti di Texas Hold'em. Alasannya murni frekuensi: dengan tiga kartu, straight (720) lebih langka daripada flush (1.096). Kedua, **A-2-3 adalah straight terendah**, di bawah 2-3-4 — bukan straight terkuat kedua seperti di beberapa varian. Dua aturan kecil ini yang bikin kalkulator tangan buatan sendiri sering salah 2–3 poin.

## Dua angka yang sering ketuker

Ini bagian yang paling sering salah kutip di forum:

- **69,5928%** = peluang dealer *qualify*. Dealer butuh queen-high atau lebih baik — artinya semua tangan queen-high polos, plus semua pair ke atas. Jumlahnya 15.380 dari 22.100 tangan.
- **67,4208%** = peluang kartu **kamu** layak di-raise. Batasnya lebih ketat: Q-6-4 atau lebih baik, yaitu 14.900 tangan.

Beda 2,17 poin persen dan fungsinya sama sekali berbeda. Yang pertama aturan meja; yang kedua hasil hitungan EV. Kalau dealer tidak qualify (30,4% kasus), ante kamu dibayar 1:1 dan play bet push — menang tanpa melihat kartu.

## Hitung sendiri: 407 juta kombinasi

Untuk tiap tangan pemain ada 18.424 tangan dealer yang mungkin dari 49 kartu sisa (kartu yang sudah keluar dibuang). Total: 22.100 × 18.424 = **407.170.400** kombinasi. Untuk setiap kombinasi, hasilnya salah satu dari:

- Dealer tidak qualify → ante +1, play push
- Dealer qualify dan kamu menang → ante +1, play +1
- Dealer qualify dan kamu kalah → −2
- Seri → push

Ditambah **ante bonus** tabel standar: straight bayar 1, three of a kind 4, straight flush 5 — dibayar berdasarkan ante saja, tidak peduli kartu dealer.

Hasil enumerasi penuh:

| Strategi | EV per ante | House edge | Element of risk |
|---|---|---|---|
| Raise semua tangan | −0,07654 | **7,654%** | 3,827% |
| Q-6-4 atau lebih baik | −0,03373 | **3,373%** | 2,015% |
| Tanpa ante bonus (raise semua) | −0,12939 | 12,939% | 6,469% |
| Tanpa ante bonus (Q-6-4) | −0,08658 | 8,658% | 5,171% |

Bacanya: satu aturan raise memotong house edge **4,28 poin persen**, dan ante bonus menyumbang **5,285 poin**. Tanpa keduanya, permainan ini 12,9% — lebih buruk dari slot 96% mana pun.

## Kenapa Q-6-4, bukan hafalan

Batas itu bukan tradisi, itu titik silang. EV raise untuk tiap tangan dihitung, lalu dibandingkan dengan buang yang nilainya pasti **−1** (ante hilang):

- **Q-6-4** → EV raise −0,9946 → masih lebih baik daripada −1 → **raise**
- **Q-6-3** → EV raise −1,0040 → sudah lebih buruk daripada buang → **fold**
- **K-J-4** → −0,1994 (raise jelas)
- **J-9-8** → −1,1399 (buang; jangan tergoda "sudah hampir")
- **A-K-Q** (straight tertinggi) → **+2,6139**

Menariknya, main optimal pun **57,014% tangan tetap EV negatif**. Kamu hanya menang secara matematis di 42,986% keputusan — sisanya bukan kesalahan main, tapi struktur pembayaran.

## Pair plus: tiga tabel, selisih sampai 5 poin

Pair plus tidak melihat kartu dealer sama sekali, jadi edge-nya bisa dihitung langsung dari tabel kombinasi di atas:

| Pembayaran (SF/Trips/Straight/Flush/Pair) | House edge |
|---|---|
| 40 / 30 / 6 / 4 / 1 | **2,317%** |
| 40 / 25 / 5 / 4 / 1 | 6,751% |
| 40 / 30 / 6 / 3 / 1 | **7,276%** |

Perhatikan baris terakhir: hanya flush diturunkan dari 4 ke 3, dan house edge melompat **4,96 poin persen** — hampir tiga kali lipat. Tabel bayaran adalah satu-satunya bagian Pair plus yang bisa diperiksa sebelum duduk.

## Uang nyata

Ante Rp10.000, 40 tangan per jam (kecepatan meja normal):

- Raise semua: EV **−Rp30.616/jam**
- Q-6-4: EV **−Rp13.492/jam**
- Selisih: **Rp17.124/jam** — Rp68.496 dalam sesi 4 jam

Dan total uang yang berputar di 100 tangan versi Q-6-4 = 167,42 unit taruhan, bukan 200. Karena itu house edge per total taruhan (element of risk 2,015%) jauh lebih kecil dari angka 3,37% yang biasa dipajang.

Satu catatan penting: ante bonus tabel standar (5/4/1) yang dipakai di sini adalah yang paling umum. Varian dengan bonus lebih tinggi memang menurunkan edge, tapi beberapa di antaranya menarik komisi 10% dari kemenangan bersih — baca dulu, karena angkanya bisa berbalik.

Angka di artikel ini dihitung sendiri lewat enumerasi penuh 407.170.400 kombinasi (sekitar 8 detik dengan numpy), lalu dicocokkan dengan Wizard of Odds (3,37% · 7,65% · element of risk 2,01% · dealer qualify 69,59%) dan Yaamava (Q-6-4 = 3,37%). Semua aritmetika dihitung ulang, bukan dikutip mentah.

<!-- cta-funnel -->

> Kalau kamu mau duduk di meja Three Card Poker atau meja kartu lain, cek dua hal sebelum taruhan pertama: batas qualify dealer, dan tabel ante bonus-nya. Bukan karena itu bikin menang, tapi karena dua angka itu satu-satunya yang benar-benar bisa kamu kontrol.

**[MAIN SEKARANG — AMBIL BONUS DEPO AWAL →](https://tomat.jagungbaru.com/banner/vip?utm_source=blog&utm_campaign=three-card-poker-q-6-4)**

*Aturan meja dan tabel bayaran tiap penyedia bisa berbeda — hitung ulang sebelum bertaruh. Artikel ini edukasi mekanika, bukan jaminan hasil.*

— Chokdi 🐷 · Content Studio · 2026
