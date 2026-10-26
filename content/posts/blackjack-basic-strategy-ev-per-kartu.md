---
title: "Blackjack: Kenapa 16 Lawan Kartu 10 Wajib Hit, Tapi Lawan Kartu 6 Wajib Stand"
description: "House edge blackjack 0,43% sampai 2,18% cuma ditentukan 4 aturan meja. Ini angka EV per kartu, kenapa 16 lawan 10 wajib hit, dan kenapa strategi dasar bukan saran tapi matematika."
date: 2026-10-26T02:10:00+00:00
draft: false
tags: ["Casino", "Blackjack", "Basic Strategy", "House Edge", "Tutorial"]
---

Blackjack kelihatan sederhana: jumlahkan kartu, jangan lewat 21. Tapi keputusan yang sama — misalnya "16 lawan kartu 10, tambah atau stop?" — punya ongkos yang berbeda jauh tergantung kartu atas dealer. Dan seluruh selisih antara permainan yang hampir adil (house edge 0,43%) dengan permainan yang menyedot 5 kali lebih cepat (2,18%) datang dari **empat baris aturan meja**, bukan dari keberuntungan.

Artikel ini membongkar angkanya. Bukan trik, bukan pola, tapi expected value (EV) per kartu yang sudah dihitung orang sampai ke digit keempat, plus cara membaca aturan meja sebelum duduk.

## 🎯 Kenapa blackjack beda dari baccarat dan roulette

Di baccarat dan roulette, kamu tidak punya keputusan. Uang ditaruh, kartu/bola bergerak, selesai. House edge-nya mati: 1,06% untuk Banker baccarat, 5,26% untuk roulette Amerika, 14,36% untuk Tie.

Di blackjack, ada **keputusan di setiap tangan** dan itu mengubah angka. Ini sebabnya blackjack satu-satunya permainan meja di mana pemain bisa mengubah ongkosnya sendiri — mau lebih murah atau lebih mahal.

Dasar hitungannya tabel Michael Shackleford (Wizard of Odds) untuk kondisi acuan: **dealer stand di soft 17, blackjack bayar 3:2, double setelah split boleh, continuous shuffler**. House edge menurut jumlah dek:

| Dek | House edge |
|---|---|
| 1 | 0,014% |
| 2 | 0,341% |
| 4 | 0,499% |
| 6 | 0,551% |
| 8 | 0,577% |

Selisih 8 dek vs 1 dek = **0,563 poin persen**. Semua aturan lain sama. Jumlah dek saja sudah hampir setara dengan seluruh house edge permainan.

## 📊 Empat aturan yang menentukan ongkosmu

Ambil basis 8 dek dengan house edge sekitar **0,430%**. Lalu ubah satu aturan demi satu aturan. Angka-angka ini efek terhadap return pemain (tanda minus = pemain rugi):

| Perubahan aturan | Efek |
|---|---|
| Blackjack bayar 6:5 (bukan 3:2) | **−1,39%** |
| Dealer hit soft 17 (H17) | −0,22% |
| Tidak boleh double setelah split | −0,14% |
| Dealer tidak boleh split aces | −0,18% |
| Player tidak boleh double sama sekali | −1,48% |

Kalau ketiganya digabung (6:5 + H17 + tanpa double-setelah-split), house edge naik dari 0,430% ke **2,180%**. Artinya modal kamu habis **5 kali lebih cepat** di meja yang sama, dengan strategi yang sama.

Hitungan langsung untuk modal Rp100.000 per tangan, 100 tangan per jam:

| Meja | House edge | Rata-rata rugi per jam |
|---|---|---|
| Rules bagus (3:2, S17, DAS) | 0,43% | Rp43.000 |
| Rules payah (6:5, H17, tanpa DAS) | 2,18% | Rp218.000 |

Selisih **Rp175.000 per jam**. Itu bukan detail kecil — itu gaji harian orang.

## 🃏 Kartu 16: kenapa lawan 10 wajib hit, lawan 6 wajib stand

Ini pertanyaan blackjack paling sering, dan jawabnya bukan soal keberanian. Ini EV dua kartu awal terhadap kartu atas dealer (tabel infinite deck, basic strategy):

| Kartu atas dealer | EV hard 16 |
|---|---|
| 2 | −0,2928 |
| 3 | −0,2523 |
| 4 | −0,2111 |
| 5 | −0,1672 |
| 6 | −0,1537 |
| 7 | −0,4148 |
| 8 | −0,4584 |
| 9 | −0,5093 |
| 10 | −0,5398 |
| A | −0,5171 |

Baca tiga hal dari tabel ini:

- **Lawan 6 adalah titik terbaik hard 16** (−0,1537). Kamu tetap rugi, tapi paling sedikit ruginya. Kuncinya: dealer dengan kartu 6 punya peluang bust paling besar, jadi kamu cukup diam dan biarkan dia yang meledak.
- **Lawan 10 adalah titik terburuk** (−0,5398). Diam di sini artinya menyerahkan 54 sen per rupiah. Hit memberi peluang memperbaiki tangan, dan memang masih lebih baik daripada diam.
- **Lawan 7 sudah memburuk drastis** (−0,4148) — hampir 3 kali lebih buruk daripada lawan 6. Batas "zona aman" hard 16 ketat: hanya 2 sampai 6.

Bandingkan dengan modal bukti dari tabel EV dua kartu awal: hard 16 = **−0,4174**, hard 14 = **−0,3725**, hard 20 = **+0,5796**, blackjack = **+1,4290**. Jadi hard 16 itu 12% lebih buruk daripada hard 14, dan hampir 0,6 kali lebih buruk daripada tangan 20. Tidak ada cara "main cantik" untuk menyulap 16 jadi tangan bagus — yang bisa dilakukan cuma memilih kerugian terkecil.

## 🎲 Kartu 10: kekuatan terbesar ada di tangan jelek

Kartu pertama adalah prediktor terkuat hasil tangan:

| Kartu pertama | EV |
|---|---|
| A | **+0,5017** |
| 10 | +0,1435 |
| 9 | −0,0107 |
| 8 | −0,0871 |
| 7 | −0,1821 |
| 6 | −0,2111 |

As memberi EV lebih dari setengah taruhan sebelum kartu kedua dibagi. Itu sebabnya split As wajib, dan As tidak boleh dianggap "angka 1 yang payah".

Lihat juga hard 10 terhadap kartu atas dealer: lawan 5 = **+0,5125**, lawan 6 = **+0,5756**, lawan 7 = **+0,3924**, lawan 10 = **+0,0253**. Satu kartu 10 melawan 6 jauh lebih berharga daripada melawan 10 — selisihnya 0,55 taruhan, padahal kartu yang kamu pegang sama persis.

Ini inti basic strategy: **nilai tanganmu tidak berdiri sendiri.** Selalu dibaca berpasangan dengan kartu atas dealer.

## ⚠️ Tiga jebakan yang bikin angka di atas tidak berlaku

1. **Bayaran 6:5 di meja "single deck".** Banyak kasino memasarkan single deck (0,014%) tapi memasang blackjack 6:5 (−1,39%). Hasilnya jauh lebih buruk daripada 8 deck 3:2 (0,577%). Baca papan aturan, jangan percaya kata "single deck".
2. **Asuransi.** Dealer menunjukkan As, ditawari asuransi bayar 2:1. Itu taruhan sampingan dengan house edge besar dan tidak ada hubungannya dengan strategi dasar. Wizard of Odds memberi judul videonya singkat: *Insurance in Blackjack — Just Say No*. Statistik emosional ("dia sudah 4 kali blackjack, pasti kali ini tidak") tidak mengubah kartu yang tersisa di shoe.
3. **Pola dan feeling.** Shoe dengan continuous shuffler mengacak tiap tangan. Tidak ada "panas" atau "dingin" — yang ada cuma aturan meja yang sudah kamu pilih sebelum duduk.

Yang paling sering dilupakan: **basic strategy mengasumsikan aturan meja tertentu**. Strategi untuk H17 beda tipis dengan S17, dan strategi 1 dek beda dari 4–8 dek. Kalau kamu hafal satu tabel lalu duduk di meja beda aturan, kamu bermain sedikit lebih buruk daripada yang kamu kira. Saran praktis dari Wizard: kalau cuma mau hafal satu, hafal versi S17 — biaya salah pakai strategi S17 di meja H17 lebih kecil daripada sebaliknya.

## 🧾 Kesimpulan

Blackjack bukan permainan di mana kamu bisa menang terus. House edge tetap positif, dan di meja terbaik pun tetap 0,43%. Yang bisa kamu kendalikan cuma dua hal:

- **Pilih mejanya.** 3:2 bukan 6:5, S17 bukan H17, double setelah split boleh. Satu baris aturan bisa mengubah ongkos dari Rp43.000 jadi Rp218.000 per jam.
- **Ikuti EV, bukan feeling.** Hard 16 lawan 6 = stand, lawan 10 = hit. Bukan karena berani, tapi karena −0,15 lebih baik daripada −0,54.

Strateginya bisa dihafal dalam 15 menit. Yang mahal biasanya bukan keputusan di meja, tapi meja yang salah dipilih.

Kalau kamu mau seri ini dilanjut — roulette (selisih 2,70% vs 5,26% karena satu angka nol) atau cara baca odds desimal vs Malay — bilang saja di komentar.

Baca juga seri "cara baca meja kasino" sebelumnya: [baccarat: kenapa Banker lebih murah 0,18% dari Player](/posts/baccarat-banker-vs-player-house-edge/) dan panduan [mix parlay: cara hitung odds](/posts/apa-itu-mix-parlay-cara-hitung-odds-2026/).

Sumber angka: [Wizard of Odds — Why the Number of Decks Matters](https://wizardofodds.com/games/blackjack/why-number-of-decks-matter/), [Blackjack Rule Variations](https://wizardofodds.com/games/blackjack/rule-variations/), dan [Expected Returns with Infinite Decks](https://wizardofodds.com/games/blackjack/player-expected-return/).

— Chokdi 🐷 · Content Studio · 2026
