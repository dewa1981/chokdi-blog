---
title: "Sicbo: 216 Kombinasi, Satu Papan — Cuma Satu Kotak yang Harganya Wajar"
date: 2026-10-28T18:05:00+07:00
draft: false
tags: ["Kasino", "Sicbo", "House Edge", "Matematika Taruhan"]
---

Tiga dadu, satu lemparan, dan papan taruhan dengan belasan kotak. Sicbo kelihatan seperti permainan keberuntungan murni — padahal seluruh harganya bisa dihitung dengan kertas dan pulpen, karena jumlah kemungkinannya cuma **216**. Artikel ini membedah papan Sicbo kotak per kotak: mana yang dibayar hampir adil, mana yang memakan seperempat sampai setengah uangmu, dan kenapa angka 180:1 bukan tawaran menarik.

Sicbo (骰寶, disebut juga *dai siu* — "besar kecil") adalah permainan dadu Tionghoa kuno yang jadi permainan kasino terpopuler kedua di Macau setelah baccarat. Aturannya sederhana: tiga dadu dikocok, pemain bertaruh pada kondisi hasil lemparan. Yang rumit bukan aturannya, tapi **selisih antara peluang sebenarnya dan bayaran yang ditawarkan**.

## 216 kombinasi, semuanya bisa didaftar

Setiap dadu punya 6 muka, jadi total susunan = 6 × 6 × 6 = **216**, dan semuanya peluangnya sama. Kalau kita daftar satu per satu, distribusi totalnya seperti ini:

| Total | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cara | 1 | 3 | 6 | 10 | 15 | 21 | 25 | 27 | 27 | 25 | 21 | 15 | 10 | 6 | 3 | 1 |

Dari tabel ini semua angka lain lahir. Contoh: total 4–10 (kategori **Kecil**) punya 3+6+10+15+21+25+27 = 107 cara. Tapi Kecil **kalah kalau keluar triple**, dan di rentang itu ada 2 triple (222 dan 333) — jadi kemenangan efektifnya 105 cara. Sisa 111 cara kalah.

Peluang menang = 105/216 = **48,61%**. Bayaran 1:1. Kerugian harapan = (105 − 111)/216 = **−2,78%**.

## Kenapa Big/Small jadi satu-satunya kotak yang wajar

Angka −2,78% itu bukan kebetulan; dia lahir dari 6 kombinasi triple yang "dibuang" dari kemenangan. Itu sebabnya Big, Small, Ganjil, dan Genap semuanya mendarat di angka yang sama. Bandingkan dengan tetangga seri ini:

- **Baccarat Banker** (komisi 5%): −1,06%
- **Roulette Eropa** taruhan 1:1: −2,70%
- **Sicbo** Big/Small: −2,78%

Ketiganya masuk kategori "harga wajar". Sisanya di papan Sicbo jauh lebih mahal.

## Papan lengkap: edge dari 2,78% sampai 47,22%

Kolom "fair" adalah bayaran yang seharusnya diberikan kalau tidak ada margin sama sekali (216 ÷ jumlah cara menang − 1). Selisih antara kolom fair dan kolom bayar **itulah** ongkos bermainnya.

| Taruhan | Cara menang | Peluang | Fair | Dibayar | Edge |
|---|---|---|---|---|---|
| Big / Small / Ganjil / Genap | 105 | 48,61% | 1,06:1 | 1:1 | **−2,78%** |
| Total 10 / 11 | 27 | 12,50% | 7,00:1 | 6:1 | −12,50% |
| Total 9 / 12 | 25 | 11,57% | 7,64:1 | 6:1 | **−18,98%** |
| Total 8 / 13 | 21 | 9,72% | 9,29:1 | 8:1 | −12,50% |
| Total 7 / 14 | 15 | 6,94% | 13,40:1 | 12:1 | −9,72% |
| Total 6 / 15 | 10 | 4,63% | 20,60:1 | 17:1 | −16,67% |
| Total 5 / 16 | 6 | 2,78% | 35,00:1 | 30:1 | −13,89% |
| Total 4 / 17 | 3 | 1,39% | 71,00:1 | 60:1 | −15,28% |
| Any triple | 6 | 2,78% | 35,00:1 | 30:1 | −13,89% |
| Triple spesifik | 1 | 0,46% | 215,00:1 | 180:1 | −16,20% |
| Dobel spesifik | 16 | 7,41% | 12,50:1 | 10:1 | −18,52% |
| Angka tunggal (1/2/3 kali) | 91 | 42,13% | — | 1:1 / 2:1 / 3:1 | −7,87% |
| Domino 2 muka berbeda (5:1) | 30 | 13,89% | 6,20:1 | 5:1 | −16,67% |

Semua angka di tabel itu hasil hitung ulang 216 kombinasi, bukan kutipan brosur — dan cocok dengan tabel referensi Wizard of Odds untuk aturan Atlantic City.

## Dua kotak "6:1" yang harganya beda 6 poin persen

Ini jebakan yang paling sering lolos: **Total 9 atau 12** dan **Total 10 atau 11** sama-sama membayar 6:1. Tapi 9/12 cuma punya 25 cara menang, sementara 10/11 punya 27. Hasilnya: edge 18,98% vs 12,50%. Kotak yang kelihatan identik, ongkosnya beda hampir separuh.

Pola ini berulang di mana-mana: dua kotak bertetangga dengan bayaran sama tidak berarti peluangnya sama. Distribusi total di tabel pertama menjelaskan semuanya — 10 dan 11 memang titik puncak kurva.

## Triple 180:1 — fair-nya 215:1

Ini kotak yang paling sering difoto orang karena angka bayarannya besar. Faktanya: triple spesifik cuma punya **1 dari 216** cara (0,46%), jadi bayaran yang adil adalah **215:1**. Kasino membayar 180:1. Selisih 35 unit itu = edge **−16,20%**, lebih buruk daripada taruhan angka tunggal yang bayarannya cuma 1:1.

Aturan Macau malah lebih tajam lagi: triple spesifik dibayar 150:1 (−30,09%) dan total 5/16 dibayar 18:1 — padahal fair-nya 35:1, sehingga edge-nya **−47,22%**. Kotak yang sama di meja berbeda bisa berharga dua kali lipat lebih mahal. Selalu baca paytable sebelum duduk.

## Versi rupiah: 100 taruhan Rp100.000

Teori edge terasa abstrak sampai dijadikan uang. Modal kerja: 100 taruhan × Rp100.000 = turnover Rp10 juta, stake sama tiap taruhan.

| Taruhan | Edge | Rugi harapan |
|---|---|---|
| Big / Small | 2,78% | Rp277.780 |
| Angka tunggal | 7,87% | Rp787.040 |
| Total 7 / 14 | 9,72% | Rp972.220 |
| Total 10 / 11 | 12,50% | Rp1.250.000 |
| Any triple | 13,89% | Rp1.388.890 |
| Triple spesifik | 16,20% | Rp1.620.369 |
| Dobel spesifik | 18,52% | Rp1.851.850 |
| Total 9 / 12 | 18,98% | Rp1.898.150 |
| Total 5/16 (Macau) | 47,22% | Rp4.722.220 |

Turnover Rp1 miliar di Big/Small = ongkos harapan **Rp27,8 juta**, hampir seluruhnya tanpa terasa karena datang sepotong-sepotong.

## Empat jebakan yang mahal

1. **Mengejar pola di Big/Small.** Peluang kalah 10 kali beruntun = (111/216)^10 ≈ **0,13%**, atau 1 dari 779. Dalam 1.000 lemparan, kejadian "mustahil" itu bukan tamu langka.
2. **Menganggap taruhan kecil lebih aman.** Angka tunggal dibayar 1:1/2:1/3:1 dan terasa ramah, tapi edge-nya **−7,87%**, hampir 3× Big/Small.
3. **Menganggap semua meja sama.** Paytable Macau vs Atlantic City berbeda di 6 kotak; selisihnya bisa 30 poin persen.
4. **Menambah taruhan untuk menutup kerugian.** Cara memperkecil kerugian bukan menambah kotak, tapi memperkecil ukuran taruhan — logikanya sama seperti [Kelly criterion](/posts/kelly-criterion-ukuran-taruhan-bankroll/) untuk bankroll.

## Checklist sebelum pasang

- Cari paytable dulu: berapa bayaran triple, 5/16, dan 4/17 di meja itu?
- Kalau harus bermain, kotak dengan edge terendah adalah Big/Small/Ganjil/Genap (2,78%) — sama seperti [roulette Eropa taruhan luar](/posts/roulette-house-edge-martingale/).
- Bandingkan dengan meja lain: [baccarat Banker](/posts/baccarat-banker-vs-player-house-edge/) masih lebih murah di 1,06%.
- Hitung ongkos dalam rupiah per 100 taruhan, bukan per lemparan.
- Ingat konversi bayaran: 6:1 berarti profit 6 unit, bukan peluang 6 kali — dasar yang sama dengan [membaca format odds](/posts/format-odds-desimal-malay-indo-hk/).

Sicbo bukan permainan yang bisa dikalahkan; yang bisa dilakukan cuma memilih harga yang paling murah, dan tahu kapan berhenti. Papan itu cuma 216 kemungkinan — semuanya sudah dihitung sebelum dadu pertama dikocok.

<!-- cta-funnel -->
> Sudah paham harganya, sekarang pilih mejanya. Meja kasino live dengan paytable transparan ada di **[VIP579 — masuk lewat sini](https://tomat.jagungbaru.com/banner/vip?utm_source=blog&utm_campaign=sicbo-216-kombinasi-house-edge)**. Main dengan ukuran taruhan yang sudah dihitung, bukan karena emosi.

Sumber: [Wizard of Odds — Sic Bo](https://wizardofodds.com/games/sic-bo/) (tabel paytable Atlantic City & Macau) dan [Wikipedia — Sic bo](https://en.wikipedia.org/wiki/Sic_bo) (216 kombinasi, konvensi bayaran).

— Chokdi 🐷 · Content Studio · 2026
