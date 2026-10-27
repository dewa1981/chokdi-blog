---
title: "Format Odds Desimal, Malay, Indo, dan HK: Satu Harga, Empat Wajah Angka"
description: "Odds 1.90, +0.90, -1.11, dan -111 itu taruhan yang SAMA. Ini tabel konversi lengkap, rumus, cara hitung peluang tersirat, dan margin bandar yang jarang dibahas."
date: 2026-10-27T12:10:00+07:00
draft: false
tags: ["Odds", "Sportsbook", "Cara Baca Pasar", "Tutorial", "Bola"]
---

Satu harga taruhan bisa ditulis dengan empat angka yang kelihatan tidak ada hubungannya. Contoh paling gampang: harga **1.90** di situs A, **+0.90** di situs B, **-1.11** di situs C, dan **-111** di situs D — keempatnya taruhan yang persis sama, dengan modal sama, hasil sama. Yang beda cuma cara menuliskan. Kalau tidak tahu konversinya, orang gampang mengira -1.11 itu "minus", artinya peluangnya jelek. Padahal tidak.

## Empat format yang beredar

- **Desimal** (Eropa, paling umum di Indonesia): angka pengali total. Modal Rp100.000 × 1,90 = **Rp190.000** kembali, profit Rp90.000.
- **Hong Kong (HK)**: angka profit per 1 unit. HK 0,90 artinya taruh 1, dapat profit 0,90.
- **Indo**: sama seperti odds Amerika, tapi dibagi 100. Tanda **minus** = favorit (berapa yang harus dipasang untuk menang 1 unit), tanda **plus** = underdog (profit per 1 unit).
- **Malay**: cermin dari Indo. Tanda **plus** = favorit, tanda **minus** = underdog.

## Tabel konversi (modal Rp100.000)

| Desimal | Malay | Indo | HK | US | Peluang tersirat |
|---|---|---|---|---|---|
| 1,50 | +0,50 | -2,00 | 0,50 | -200 | 66,67% |
| 1,85 | +0,85 | -1,18 | 0,85 | -118 | 54,05% |
| 1,90 | +0,90 | -1,11 | 0,90 | -111 | 52,63% |
| 2,00 | 0 (even) | +1,00 | 1,00 | +100 | 50,00% |
| 2,50 | -0,67 | +1,50 | 1,50 | +150 | 40,00% |
| 3,50 | -0,40 | +2,50 | 2,50 | +250 | 28,57% |
| 6,00 | -0,20 | +5,00 | 5,00 | +500 | 16,67% |

Kolom terakhir itu bukan hiasan — di situlah letak semua keputusan.

## Rumusnya, biar tidak perlu hafal tabel

Ambil **D** = odds desimal:

- **HK** = D − 1 (selalu positif)
- **Indo**: kalau D < 2 → −1 ÷ (D − 1); kalau D > 2 → D − 1
- **Malay**: kalau D < 2 → D − 1; kalau D > 2 → −1 ÷ (D − 1)
- **US** = Indo × 100

Perhatikan pola Malay dan Indo: keduanya tukar tempat. Itu sebabnya Malay disebut kebalikan odds Amerika — favorit yang di Indo ditulis -2,00 justru ditulis +0,50 di Malay. Rumus konversi desimal ke Malay dan Amerika ini sama dengan yang dipakai [The Odds API](https://the-odds-api.com/sports-odds-data/odds-format.html), jadi bisa dipakai untuk cek angka dari situs mana pun.

## 1,90 bukan berarti peluangnya 90%

Ini salah paham paling mahal. Odds desimal **bukan** persentase peluang; peluang tersirat = **1 ÷ D**. Jadi 1,90 = 52,63% — bukan 90%. Odds 6,00 = 16,67%, bukan 60%. Rumus `P = 1/D` ini standar dalam [matematika bookmaking](https://en.wikipedia.org/wiki/Mathematics_of_bookmaking).

Konsekuensinya penting: dua angka "kelihatan dekat" bisa jauh beda hasilnya. 1,90 dan 2,00 cuma selisih 0,10 di layar, tapi dengan modal Rp100.000 profitnya Rp90.000 vs Rp100.000 — beda **Rp10.000, atau 11,11%** dari profit. Nol koma satu itu bukan nol koma satu.

## Margin bandar kelihatan dari sini

Jumlahkan peluang tersirat semua pilihan di satu pasar. Pasar yang adil berjumlah 100%. Kenyataannya selalu lebih:

- Dua arah 1,90 vs 1,90 → 52,63% + 52,63% = **105,26%**, margin **5,26%**.
- Tiga arah 2,10 / 3,40 / 3,60 → **104,81%**, margin **4,81%**.

Kelebihan di atas 100% itu namanya *overround* atau vig — jatah bandar, bukan keberuntungan. Kalau marginnya dibuang, harga yang "seharusnya" untuk pasar 1,90/1,90 adalah **2,00** di dua sisi; untuk 2,10/3,40/3,60 menjadi **2,20 / 3,56 / 3,77**. Selisih itulah yang bikin menang-kalah bergantian tetap berujung rugi pelan-pelan.

Dan margin ini **berlipat** di parlay. Rumusnya `B1 × B2 × 100 − 100`: dua leg dari pasar bermargin 5,26% menghasilkan overround gabungan **10,80%**. Sebab itu satu leg kalah sudah menghanguskan seluruh tiket — peluangnya sudah dipotong dua kali.

## Contoh kerja: modal Rp100.000, satu harga, tiga tampilan

Misal kamu ambil sisi favorit dengan harga desimal 1,90:

- **Desimal 1,90** → kembali Rp190.000, profit Rp90.000.
- **Malay +0,90** → taruh 100.000, profit 100.000 × 0,90 = Rp90.000. Sama.
- **Indo -1,11** → 100.000 ÷ 1,1111 = Rp90.001 profit. Beda Rp1 cuma karena pembulatan. Sama.

Tiga situs, tiga angka, satu matematika. Yang berubah cuma bahasa.

## Empat jebakan yang paling sering kena

1. **Mengira tanda minus = peluang jelek.** Di Indo, -2,00 itu favorit kuat (peluang 66,67%). Yang "jelek" justru +5,00.
2. **Pakai harga yang sudah lewat.** Odds bergerak sampai kick-off. Yang mengikat adalah angka saat tiket dipasang, bukan saat kamu melihat layar 20 menit sebelumnya.
3. **Lupa koma di menang setengah.** Di garis seperempat, odds hanya berlaku untuk separuh modal — mekanismenya dibahas di [handicap Asia dan menang setengah](/posts/handicap-asia-voor-menang-setengah/).
4. **Mengalikan odds tanpa sadar mengalikan margin.** Untuk perkalian multi-leg dan kasus push, rumusnya ada di [panduan hitung odds mix parlay](/posts/apa-itu-mix-parlay-cara-hitung-odds-2026/).

Kalau pasar yang dibaca bukan bola tapi meja kasino, logikanya sebangun: yang menentukan bukan keberuntungan semalam, tapi selisih kecil yang berulang — lihat [edge banker vs player di baccarat](/posts/baccarat-banker-vs-player-house-edge/) dan [cara baca RTP serta volatilitas](/posts/rtp-slot-volatilitas-cara-baca-2026/).

## Cek cepat sebelum pasang

- Format apa yang dipakai situs ini? Kalau minus/plus tanpa koma, itu Indo atau US — bagi 100 dulu.
- Hitung peluang tersiratnya: 1 ÷ desimal. Bandingkan dengan feelingmu, bukan dengan angka di layar.
- Jumlahkan semua sisi pasar. Di atas 105% berarti harganya lumayan mahal.

Odds itu bahasa, bukan takdir. Begitu bisa menerjemahkan empat format ini bolak-balik dalam kepala, tiket yang dulu terasa "aneh" saat settle jadi biasa saja — dan keputusan taruhan berhenti jadi tebak-tebakan — Chokdi 🐷 · Content Studio · 2026
