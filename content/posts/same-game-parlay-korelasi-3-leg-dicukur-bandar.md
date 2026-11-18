---
title: "Same Game Parlay: 3 Leg yang Saling Dukung Justru Paling Dicukur Bandar"
description: "Kali-odds cuma sah untuk laga berbeda. Di SGP, peluang gabungan 16% bisa jadi 21,2% karena korelasi — dan harga dari bandar turun dari +600 ke +350. Ini hitungan lengkapnya plus cara mengecek harga SGP sendiri."
date: 2026-11-19T00:15:00+07:00
draft: false
tags: ["Same Game Parlay", "Parlay", "Korelasi", "Edukasi Judi", "Matematika Taruhan", "Sportsbook"]
---

Same Game Parlay (SGP) sekarang jadi produk paling dijemput di sportsbook: semua leg diambil dari satu pertandingan, odds kelihatan besar, dan ceritanya terasa nyambung — tim menang, striker bikin gol, total over. Masalahnya, cara paling umum menghitung SGP — **kali semua odds** — justru salah besar. Bukan salah pembulatan, tapi bisa meleset 25–34%.

Ini hitungannya, Plus cara mengecek harga SGP yang kamu terima sebelum pasang.

## Kenapa kali-odds cuma sah untuk laga berbeda

Rumus `P(A dan B) = P(A) × P(B)` hanya berlaku kalau A dan B **independen** — hasil laga Lakers tidak mempengaruhi laga Liga Premier. Itu sebabnya parlay lintas laga aman dikali.

SGP melanggar syarat itu. Dua leg di pertandingan yang sama naik-turun bersama. Kalau kedua tim mencetak gol, kamu sudah punya 2 gol dan tinggal satu gol lagi untuk Over 2.5. Event-nya **berkorelasi positif**: `P(A dan B) > P(A) × P(B)`. Konsekuensinya:

- Peluang sebenarnya **lebih besar** dari hasil kali → odds fair **lebih kecil** dari hasil kali.
- Bandar yang membayar harga hasil-kali akan bocor. Jadi mereka tidak membayarnya — mereka me-repricing bundelnya lewat mesin SGP sendiri.

## Contoh: Over 2.5 + BTTS Yes

Dua leg klasik di sepak bola, harga mainline dari Pinnacle:

| Leg | Odds desimal | Probabilitas tersirat |
|---|---|---|
| Over 2.5 gol | 1,55 | 64,5% |
| Both Teams To Score – Yes | 1,95 | 51,3% |
| Hasil kali naif | **3,02** | 33,1% |

Harga fair yang sudah dikoreksi korelasi: **2,42**. Artinya hasil kali naif **terlalu tinggi 24,8%** — kalau ada bandar yang membayar 3,02 untuk kombinasi ini, dia rugi besar. Versi lain dari fixture yang sama bahkan meleset dari 3,24 ke 2,42: **selisih 33,9%**.

Perhatikan sisi sebaliknya: **Under 2.5 + BTTS Yes** justru berkorelasi *negatif* (satu-satunya jalan adalah skor tepat 1-1). Di situ hasil kali naif terlalu **kecil**, jadi odds yang ditawarkan kelihatan pelit padahal mungkin ada nilai. Arah korelasinya menentukan siapa yang dicurangi.

## Hitungan 3 leg: 16% versus 21,2%

Ambil contoh tiga leg satu laga NFL: tim A menang (-140), QB over 275,5 yard (-110), total over 48,5 (-110). Probabilitas tersiratnya 58,3% × 52,4% × 52,4%.

**Kalau dianggap independen:** 0,583 × 0,524 × 0,524 = **0,160 → 16,0%**. Fair odds 6,25.

**Kalau pakai korelasi** (matriks korelasi wajar: tim menang ↔ QB bagus 0,35; QB bagus ↔ total over 0,42; menang ↔ over 0,28): peluang gabungan sekitar **21,2%** — naik **33%**. Fair odds 4,72.

Sekarang lihat efeknya ke dompet:

| Harga yang dibayar | Probabilitas tersirat | EV buat pemain (peluang asli 21,2%) |
|---|---|---|
| +600 (parlay biasa, 7,0x) | 14,29% | **+48,4%** |
| +350 (harga SGP, 4,5x) | 22,22% | **−4,6%** |

Di harga +600, pemain untung 48% — mustahil untuk bandar. Di +350, pemain bayar 4,6%. Dengan taruhan Rp100.000, ekspektasi ruginya **Rp4.600 per tiket** — meski peluang menangnya 1 banding 5.

## Cara bandar menghitung (dan kenapa susah dilawan)

Tiga metode yang dipakai, biasanya campur:

1. **Matriks korelasi historis.** Tiap pasangan jenis taruhan dihitung koefisien korelasinya (Pearson) dari ribuan laga. Rentang tipikal ρ antara −0,4 dan +0,6.
2. **Gaussian copula.** Marginal probability tiap leg dipertahankan, struktur ketergantungannya dimodelkan sebagai multivariat normal, lalu peluang gabungan dihitung lewat simulasi Monte Carlo.
3. **Frekuensi empiris.** Cara paling jujur: hitung langsung. Contoh dari 500 laga NFL dengan favorit −3 sampai −7 dan total 45–51 poin:

| Hasil | Frekuensi | Probabilitas |
|---|---|---|
| Favorit menang | 290 | 58,0% |
| QB favorit over 275 yard | 255 | 51,0% |
| Total over | 265 | 53,0% |
| **Ketiganya kena bersamaan** | **102** | **20,4%** |

Hasil kali independen: 0,580 × 0,510 × 0,530 = 15,7%. Kenyataan: 20,4%. **Korelasinya mengerek 30%.**

## House edge SGP: 15–25%, bukan 4–5%

Setelah peluang gabungan ketemu, bandar menempelkan margin. Contoh langkahnya: peluang asli 18,9% (fair +429), bandar menawarkan +350 (probabilitas tersirat 22,22%). House edge-nya:

(0,2222 − 0,189) / 0,2222 = **14,94%**

Bandingkan taruhan tunggal yang cuma 4–5%. Makanya SGP dijual dengan bonus, boost, dan tampilan menarik: margin-nya tiga sampai lima kali lebih gemuk. Dan ironisnya, kombinasi yang **paling terasa masuk akal** (favorit menang + striker bintang over + total over) justru yang paling presisi dicukur, karena mesin sudah punya data korelasinya.

## Cara mengecek harga SGP sendiri

Sebelum pasang, tiga langkah:

1. **Ubah harga jadi probabilitas.** Desimal 4,5 → 1/4,5 = 22,22%. Untuk format lain, cek panduan [format odds desimal, Malay, Indo, dan HK](/posts/format-odds-desimal-malay-indo-hk/).
2. **Bandingkan dengan hasil kali leg.** Kalau harga SGP jauh lebih kecil dari hasil kali, itu wajar — selisihnya adalah ongkos korelasi. Yang perlu dicurigai: selisihnya lebih besar dari 30–40% tanpa alasan jelas.
3. **Pilih leg yang korelasinya lemah.** Tim menang + kiper lawan over saves = nyaris independen, jadi harganya mendekati parlay biasa. Leg yang "saling dukung" selalu didiskon paling dalam.

Kalau mau hitung parlay lintas laga (yang masih sah dikali), rumusnya ada di [apa itu mix parlay dan cara hitung odds](/posts/apa-itu-mix-parlay-cara-hitung-odds-2026/). Untuk melihat seberapa besar margin bandar di pasar 1X2, ada di [overround dan margin bandar](/posts/overround-margin-bandar-1x2-persen/).

## Kesimpulan

SGP bukan parlay biasa — dia produk terpisah dengan mesin harga sendiri. Peluang gabungan tiga leg bisa 33% lebih besar dari hasil kali, dan justru karena itu harga yang kamu terima turun dari +600 ke +350. Kalau kamu masih mengalikan odds SGP dengan kalkulator, angka yang kamu pegang bukan peluang — itu angka yang menguntungkan bandar.

Kalau mau, tulis di komentar: kombinasi SGP apa yang paling sering kamu pasang? Nanti kita bedah korelasinya satu per satu.

Sumber: [Wizard of Odds — Same-Game Parlays: The Mathematics of Correlation](https://wizardofodds.com/article/same-game-parlays-the-mathematics-of-correlation/), [OddsPapi — Same-Game Parlay Correlation: Why Multiplying Odds Fails](https://oddspapi.io/blog/same-game-parlay-correlation-python/), dan [FOX Sports — What Is a Same-Game Parlay?](https://www.foxnews.com/outkick-betting/same-game-parlay-explained).

— Chokdi 🐷 · Content Studio · 2026
