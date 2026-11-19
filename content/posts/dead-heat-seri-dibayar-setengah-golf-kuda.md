---
title: "Dead Heat: Menang Tapi Dibayar Setengah — Hitungan Golf & Kuda"
description: "Seri di garis Top 10 bikin stake kamu dibagi jumlah pemain yang ikut seri. Harga 3,00 dengan aturan dead heat ternyata cuma setara 2,57 kalau seri dibayar penuh — potongan 14,4% yang tidak kelihatan di bet slip. Ini rumusnya plus cara memilih pasar yang tidak kena potong."
date: 2026-11-19T12:05:00+07:00
draft: false
tags: ["Dead Heat", "Taruhan Golf", "Each-Way", "Edukasi Judi", "Sportsbook", "Matematika Taruhan"]
---

Taruhan golf "Top 10" dengan odds 3,00 kelihatan manis: tebak satu pemain masuk sepuluh besar, uang tiga kali lipat. Lalu dia finis **T10** — seri dengan dua pemain lain di posisi terakhir yang dibayar. Kamu menang. Tapi yang kembali bukan 300, melainkan **100**. Persis modal, profit nol.

Itulah **dead heat**. Bukan bug, bukan situs nakal — aturan resmi yang dipakai hampir semua sportsbook, dan jarang dibaca sebelum pasang.

## Apa yang sebenarnya dihitung

Kalau dua peserta atau lebih menempati posisi yang sama di pasar yang sedang aktif, taruhan diselesaikan dengan membagi **stake** (bukan odds) sejumlah peserta yang ikut seri. PGA Tour memberi contoh: \$100 pada McIlroy Top 10 di +200, finis T10 bersama dua pemain lain → stake dibagi tiga, \$33,33 dihargai menang di +200, sisanya dianggap kalah.

Jadi urutannya: **odds kamu tetap, ukuran taruhan kamu yang menyusut.**

## Dua rumus yang harus dibedakan

Ada dua keluarga pasar, dan keduanya memotong dengan cara berbeda.

**1. Pasar juara (win market).** Stake dibagi jumlah peserta seri. Betfair: £10 pada kuda 10/1 yang seri dua arah → (£10 ÷ 2) × 10 + £5 kembali = **£55**, bukan £110. Seri tiga arah → £36,66.

**2. Pasar posisi (Top 5/10/20, each-way).** Yang dibagi adalah *jatah tempat*, bukan jumlah pemain. DraftKings memakai "Dead Heat Reduction" (DHR): jumlah peserta seri ÷ jumlah posisi tersisa = pembagi odds.

| Kasus | Hitungan | Hasil |
|---|---|---|
| \$50 Top 10 @3,00, seri 8 dengan 3 tempat sisa (8–10) | 6 ÷ 3 = 2 → odds 3,00 ÷ 2 = 1,50 | balik **\$75** (rugi \$25) |
| \$50 Top 5 @2,50, seri dua arah | 2,50 ÷ 2 = 1,25 | balik \$62,50 |
| \$50 @1,80 group winner, seri dua arah | 1,80 ÷ 2 = 0,90 | balik **\$45** — di bawah modal |

Baris terakhir penting: DHR bisa menghasilkan payout **lebih kecil dari uang yang kamu setor** padahal statusnya "menang". Di pasar place golf, Betfair memakai bentuk setara: (stake × jumlah payout ÷ jumlah seri) × (odds − 1), dikurangi bagian stake yang gugur.

## Contoh kuda: "place" yang menang tapi balik 56%

Each-way £10 (£5 win + £5 place) di odds 5/1, place 1/4 odds (2,25 desimal), tiga tempat. Kuda finis seri untuk tempat ketiga dengan satu kuda lain.

- Stake place £5 dibagi 2 = £2,50 → £2,50 × 2,25 = **£5,63** kembali.
- £5 untuk win hangus, £5 place cuma balik £5,63 → dari £10 yang disetor, **net −£4,37**.

Finis bersih di tiga besar berarti balik £11,25 (untung £1,25). Satu foto-finish mengubah "menang tipis" jadi rugi 44%.

## Kenapa ini mahal: 3,00 dengan dead heat ≈ 2,57 tanpa

Ini inti yang paling sering terlewat. Harga yang sama bisa bernilai sangat berbeda tergantung aturan seri.

Ambil model: taruhan Top 10, stake 100, odds 3,00. Peluang masuk sepuluh besar bersih 30%, seri di garis 10% (60% seri dua arah, 30% tiga arah, 10% empat arah), sisanya kalah.

| Aturan | EV per 100 | ROI |
|---|---|---|
| Seri dibayar penuh | +20,00 | **+20,0%** |
| Dead heat (stake dibagi) | +2,75 | **+2,75%** |

Selisihnya **17,25 poin persentase**. Dan kalau dihitung ekuivalennya: 3,00 dengan aturan dead heat hanya sepadan dengan **2,569** jika seri dibayar penuh. Artinya kamu kehilangan **0,43 angka odds — 14,4% dari harga** — tanpa satu pun angka berubah di bet slip.

Dari arah bandar, ini bukan kecurangan: harga fair untuk pasar ber-dead-heat memang harus lebih tinggi. Dengan peluang seri 10% seperti model di atas, harga fair tanpa aturan seri **2,50**, sedangkan dengan dead heat **2,92** — beda 16,8%. Jadi kalau bandar menawarkan 2,50 untuk pasar yang menerapkan dead heat, dia sudah memungut potongan tersembunyi.

## Yang paling menyakitkan: parlay

DHR menyambung ke seluruh tiket. DraftKings memberi contoh: \$50 parlay tiga pemain golf Top 20, masing-masing @2,0, total 8,0 (proyeksi \$400). Dua leg menang bersih, satu leg seri di posisi 20 bersama tiga pemain lain → odds leg itu jadi 0,5, odds parlay turun dari 8,0 ke 2,0, dan payout jadi **\$100**. Bukan \$100 ditambah sesuatu — \$100 untuk tiket yang hampir sempurna.

Itu sebabnya leg golf Top-N adalah leg paling berbahaya di parlay: risikonya bukan cuma kalah, tapi **menang versi setengah**.

## Cara main supaya tidak kena potong diam-diam

1. **Cari label "Top X Finish Incl. Ties".** DraftKings menyediakan pasar ini untuk Top 5/10/20 (pra-turnamen) yang dibayar penuh walau seri. Harganya memang lebih pelit — tapi baru layak dibandingkan pakai ambang: pasar standar 3,00 dengan dead heat = 2,57 seri penuh. Kalau pasar "incl. ties" memberi **di atas 2,57**, itu pilihan yang lebih baik walau angkanya kelihatan lebih kecil.
2. **Baca aturan seri sebelum pasang, bukan sesudah settle.** Beberapa bandar membayar seri penuh di pasar place; yang lain tidak. Dua bandar dengan odds 3,00 dan 2,80 bisa terbalik nilainya.
3. **Pasar juara (outright) bebas dead heat** — golf outright, juara turnamen, pemenang laga. Kalau mau hindari urusan seri, jangan bertaruh di pasar posisi.
4. **Hitung dulu worst-case.** Sebelum pasang Top 10, tanya: kalau seri tiga arah, balikannya berapa? Kalau jawabannya "cuma modal", harga 3,00 itu sebenarnya bukan 3,00.

Menang tetap menang. Cuma, di pasar posisi, kemenangan punya beberapa versi harga — dan versi termurahnya yang paling sering kamu dapat.
