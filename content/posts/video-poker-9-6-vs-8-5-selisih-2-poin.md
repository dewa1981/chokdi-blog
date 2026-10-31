---
title: "Video Poker 9/6 vs 8/5: Dua Baris Tabel Bayaran, Selisih Rp269 Ribu per 4 Jam"
date: 2026-11-01T00:10:00+07:00
draft: false
tags: ["Kasino", "Video Poker", "House Edge", "Probabilitas"]
---

Video poker kelihatan seperti slot yang kebetulan pakai kartu. Padahal di sini ada satu keputusan yang benar-benar bisa dihitung: **pegang kartu mana**. Tapi sebelum sampai ke situ, ada hal yang lebih menentukan dan sering dilewati pemain — dua baris di tabel bayaran. Mesin 9/6 dan 8/5 menarik kartu dari dek yang sama, lima kartu yang sama, dan strategi optimal yang sama. Bedanya cuma *full house* dibayar 9 atau 8, *flush* dibayar 6 atau 5. Selisihnya: **99,54% vs 97,30%** — 2,25 poin.

Artikel ini menghitung ulang angkanya dari kombinasi kartu, bukan mengutip brosur.

## Kenapa RTP-nya bisa dihitung persis

Satu tangan video poker = 5 kartu dibagi, lalu sisanya boleh ditukar. Total kemungkinan jalur per tangan: C(52,5) = **2.598.960** cara membagi, dikali C(47,5) = **1.533.939** cara menarik ulang — 3,99 triliun kombinasi. Dengan strategi optimal, distribusi hasil akhirnya begini (tabel 9/6):

| Hasil akhir | Bayar | Peluang | 1 di antara | Kontribusi RTP |
|---|---|---|---|---|
| Royal flush | 800 | 0,00248% | 40.388 | 1,98 pp |
| Straight flush | 50 | 0,01093% | 9.148 | 0,55 pp |
| Four of a kind | 25 | 0,23625% | 423 | 5,91 pp |
| Full house | 9 | 1,15122% | 87 | 10,36 pp |
| Flush | 6 | 1,10145% | 91 | 6,61 pp |
| Straight | 4 | 1,12294% | 89 | 4,49 pp |
| Three of a kind | 3 | 7,44487% | 13 | 22,34 pp |
| Two pair | 2 | 12,92789% | 8 | 25,86 pp |
| Jacks or better | 1 | 21,45850% | 5 | 21,46 pp |
| **Total** | | | | **99,54%** |

Peluang dapat tangan yang membayar: **45,457%**. House edge 9/6 = **0,456%** — paling tipis di seluruh lantai kasino, lebih rendah dari [baccarat banker](/posts/baccarat-banker-vs-player-house-edge/) (1,06%) dan jauh di bawah Big/Small [sicbo](/posts/sicbo-216-kombinasi-house-edge/) (2,78%).

## Selisih 2,25 poin itu datang dari dua baris saja

Karena peluang tiap hasil hampir tidak berubah ketika tabel bayaran diturunkan, selisih RTP bisa dipotong per baris:

| Perubahan | Peluang kena | Biaya |
|---|---|---|
| Full house 9 → 8 | 1,15122% | −1,1512 pp |
| Flush 6 → 5 | 1,10145% | −1,1015 pp |
| **Jumlah** | | **−2,2527 pp** |

Hitung sendiri: 99,5439 − 2,2527 = **97,2912%**. Angka resmi mesin 8/5 = **97,2984%** — beda 0,0072 poin, yang muncul karena strategi optimal di tabel 8/5 sedikit bergeser (lebih jarang mengejar flush). Artinya: **strategi hampir tidak menyelamatkan tabel bayaran yang jelek.**

Tangga lengkapnya, semua dihitung dari tabel 9/6 dengan mengganti baris full house/flush:

| Tabel | RTP | House edge |
|---|---|---|
| 9/6 | 99,54% | 0,46% |
| 8/6 | 98,39% | 1,61% |
| 9/5 | 98,44% | 1,56% |
| 8/5 | 97,30% | 2,70% |
| 7/5 | 96,14% | 3,86% |
| 6/5 | 94,99% | 5,01% |

## Dua jebakan yang lebih mahal dari paytable

**1. Main kurang dari 5 koin.** Royal flush membayar 250 per koin untuk taruhan 1–4 koin, dan 800 per koin hanya kalau kamu pasang 5 koin. Ganti bayaran royal jadi 250 di tabel 9/6: RTP jatuh ke **98,18%** (edge 1,82%) — kerugian 1,36 poin hanya karena satu koin yang tidak dipasang. Pinnacle mencatat angka yang sama: 98,181% untuk taruhan 1–4 kredit.

**2. Memilih mesin karena tampilannya.** 6/5 punya edge 5,01% — lebih dari sepuluh kali lipat 9/6. Pemain yang hafal seluruh [strategi blackjack](/posts/blackjack-basic-strategy-ev-per-kartu/) pun tidak bisa menutup selisih itu dengan akurasi *hold*.

## Terjemahan ke rupiah

Asumsi wajar main cepat: 600 tangan per jam, taruhan Rp5.000 per tangan → turnover **Rp3 juta per jam**.

| Tabel | EV per jam | EV 4 jam |
|---|---|---|
| 9/6 | −Rp13.683 | −Rp54.731 |
| 8/5 | −Rp81.047 | −Rp324.188 |
| 4 koin (royal 250) | −Rp54.575 | −Rp218.300 |
| 6/5 | −Rp150.336 | −Rp601.345 |

Selisih 9/6 vs 8/5 = **Rp67.364 per jam**, atau **Rp269.456 per 4 jam**. Itu uang yang hilang bukan karena kartu sial, tapi karena satu angka di layar.

## Tapi jangan salah baca: varians tetap raja

Standar deviasi Jacks or Better = **4,42 taruhan per tangan**. Untuk 600 tangan: 108,3 taruhan ≈ **Rp541.337** — sekitar 40 kali lipat EV per jam. Akibatnya:

- Peluang sesi 600 tangan berakhir profit di 9/6: **49,0%**
- Di 8/5: **44,0%** · di 6/5: **39,1%**

Dan selisih paytable 2,25 poin baru "mengalahkan" noise setelah sekitar **38.700 tangan** (~65 jam main). Artinya: pemain 8/5 bisa menang besar malam ini dan tetap rugi secara matematis, sebaliknya pemain 9/6 bisa kalah tiga sesi berturut-turut tanpa strateginya salah.

## Kesimpulan

Urutan keputusan yang benar: **cek tabel bayaran dulu, pasang 5 koin, baru hafal urutan hold.** Bukan sebaliknya. Video poker satu-satunya permainan di mana pemain bisa menyentuh 99% secara matematis — tapi hanya kalau mesinnya 9/6 dan taruhannya 5 koin. Di mesin 6/5, akurasi setinggi apa pun cuma memperlambat kerugian.

Angka RTP di artikel ini dihitung dari tabel kombinasi Wizard of Odds (9/6 dan 8/5, 19,9 triliun kombinasi *deal+draw*), dicocokkan dengan tabel house edge Pinnacle dan frekuensi tangan New Game Network; semua aritmetika dihitung ulang sendiri, bukan dikutip mentah.

<!-- cta-funnel -->

> Kalau kamu mau main video poker atau meja lain, cek tabel bayarannya dulu — dan pasang taruhan maksimum yang mesinnya minta. Bukan karena itu bikin menang, tapi karena itu satu-satunya bagian yang benar-benar bisa kamu kontrol.

**[MAIN SEKARANG — AMBIL BONUS DEPO AWAL →](https://tomat.jagungbaru.com/banner/vip?utm_source=blog&utm_campaign=video-poker-9-6-vs-8-5-selisih-2-poin)**

*Tabel bayaran penyedia bisa berubah dan beberapa mesin memakai aturan royal berbeda — hitung ulang sebelum bertaruh. Artikel ini edukasi mekanika, bukan jaminan hasil.*

— Chokdi 🐷 · Content Studio · 2026
