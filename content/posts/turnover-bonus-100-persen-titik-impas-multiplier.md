---
title: "Bonus 100% dengan Turnover 30x: Titik Impasnya Cuma 28,6x, Lewat Itu Kamu Bayar"
date: 2026-11-05T12:10:00+07:00
draft: false
tags: ["Kasino", "Bonus", "Turnover", "House Edge"]
---

"Deposit Rp100.000, dapat bonus Rp100.000, turnover 30x." Kalimat promo paling umum di mana-mana, dan hampir semua orang membacanya sebagai "dapat tambahan modal dua kali lipat". Padahal angka yang benar-benar menentukan untung-rugi bukan angka 100%, bukan angka 30x — tapi satu angka yang tidak pernah ditulis di banner: **house edge game yang kamu mainkan**.

Artikel ini membedah matematikanya dengan kalkulator, bukan perasaan. Semua angka di bawah dihitung ulang sendiri, bukan kutip brosur.

## Dua angka yang harus dipisah dulu

Istilah yang sering dicampur:

- **Basis turnover** — bonus saja, atau deposit + bonus. Bunyinya di terms: `30x bonus` atau `30x D+B`. Beda satu kata, beda dua kali lipat kerja.
- **Turnover** — total nilai taruhan yang harus diputar, bukan total deposit.

Contoh nyata, deposit Rp100.000 + bonus Rp100.000:

| Multiplier | Basis bonus saja | Basis deposit + bonus |
|---|---|---|
| 20x | Rp2.000.000 | Rp4.000.000 |
| 30x | Rp3.000.000 | Rp6.000.000 |
| 40x | Rp4.000.000 | Rp8.000.000 |

Dua promo yang tampil identik di banner bisa menuntut Rp3 juta atau Rp6 juta taruhan. Selisihnya bukan teknis kecil — itu Rp3 juta uang yang harus bolak-balik ke meja.

## Rumus biaya sebenarnya

Turnover itu bukan biaya. Biaya = turnover × house edge.

> **Ekspektasi biaya = (basis × multiplier) × house edge**

Bonus Rp100.000, turnover 30x = Rp3.000.000 diputar. Kalau main slot RTP 96,5% (edge 3,5%), ekspektasi biaya = Rp105.000. Bonusnya Rp100.000. **EV = −Rp5.000** sebelum satu sen pun dipertimbangkan soal variansi.

Ganti game-nya, angkanya berubah drastis:

| RTP game | Turnover | Ekspektasi biaya | Sisa bonus | EV |
|---|---|---|---|---|
| 99,0% | Rp3.000.000 | Rp30.000 | +Rp70.000 | **+70%** |
| 97,5% | Rp3.000.000 | Rp75.000 | +Rp25.000 | +25% |
| 96,5% | Rp3.000.000 | Rp105.000 | −Rp5.000 | −5% |
| 94,5% | Rp3.000.000 | Rp165.000 | −Rp65.000 | −65% |
| 92,0% | Rp3.000.000 | Rp240.000 | −Rp140.000 | **−140%** |

Jadi bonus 30x itu **bisa untung** (kalau game-nya RTP 97,5% ke atas) dan **bisa rugi dua digit** (kalau game-nya RTP 92%). Promo yang sama, hasil berlawanan. Yang menentukan bukan promo, tapi pilihan game.

## Titik impas: multiplier maksimum yang masih waras

Kalau bonus 100% dan basis = bonus, titik impas terjadi saat biaya = bonus:

> **multiplier impas = 1 ÷ house edge**

| House edge | Multiplier impas (bonus 100%, basis bonus) | Kalau basis D+B |
|---|---|---|
| 1,0% | 100,0x | 50,0x |
| 2,5% | 40,0x | 20,0x |
| 3,5% | **28,6x** | 14,3x |
| 5,5% | 18,2x | 9,1x |
| 8,0% | 12,5x | 6,2x |

Ini angka yang saya pakai sendiri sebagai filter: **bonus 100% dengan turnover di atas 28,6x untuk game RTP 96,5% sudah negatif secara ekspektasi.** Tawaran "turnover 35x" atau "40x" untuk slot RTP 96% bukan bonus — itu biaya keanggotaan.

Perhatikan juga kolom ketiga: kalau basisnya deposit + bonus, semua batas itu **terpotong jadi separuh**. Promo 20x D+B secara beban setara 40x bonus-saja.

## Kontribusi game: jebakan yang paling mahal

Turnover tidak dihitung sama untuk semua game. Slot biasanya 100%, live casino 20%, blackjack 10%, dan sebagian game 0%. Konsekuensinya: kalau kontribusi 20%, kamu harus bertaruh **lima kali lipat** untuk menyelesaikan turnover yang sama.

Target turnover Rp3.000.000, hasil hitung:

| Game | Kontribusi | Taruhan riil | Ekspektasi biaya |
|---|---|---|---|
| Slot | 100% | Rp3.000.000 | Rp105.000 |
| Live casino | 20% | Rp15.000.000 | Rp180.000 |
| Blackjack | 10% | Rp30.000.000 | Rp150.000 |
| Roulette Eropa | 20% | Rp15.000.000 | Rp405.000 |
| Togel/4D | 0% | tidak pernah selesai | bonus terkunci |

Menarik: blackjack punya edge paling kecil (0,5%) tapi karena kontribusinya cuma 10%, biaya riilnya Rp150.000 — masih lebih mahal dari slot Rp105.000. Dan roulette Eropa 2,7% edge dengan kontribusi 20% jadi **Rp405.000**, empat kali lipat bonusnya. Kontribusi game bisa membalik keunggulan edge sepenuhnya.

## Tiga jebakan lain yang tidak kelihatan di banner

**1. Batas maksimal taruhan.** Banyak terms menulis "maksimal bet Rp50.000 selama klaim bonus". Kalau bankroll-mu Rp2 juta, kamu butuh 60 spin @Rp50.000 untuk habiskan Rp3 juta turnover — cuma 0,1 jam. Kedengarannya cepat, tapi 60 spin dengan volatilitas tinggi = peluang besar habis sebelum turnover selesai. Batas bet ini mematikan strategi "putar kecil-kecil sampai aman".

**2. Max cashout.** Bonus tanpa turnover kadang dipasang plafon, misal "max cashout 10x bonus". Bonus Rp100.000, menang 50x jadi Rp5.000.000 — yang bisa ditarik tetap Rp1.000.000. Rp4 juta hilang di kalimat yang dicetak paling kecil.

**3. Waktu kedaluwarsa & exclusion list.** Turnover 30x dengan tempo 3 detik per spin = 600 spin untuk bet Rp5.000. Kalau batas waktunya 7 hari dan kamu cuma main 30 menit sehari, sisa turnover hangus — dan bonus ikut hangus.

## Cara pakai ini besok

Sebelum klaim bonus apa pun, hitung tiga langkah:

1. **Cari basisnya**: bonus saja, atau deposit + bonus?
2. **Kali dengan house edge game yang akan dimainkan** (bukan RTP banner, tapi RTP versi game itu).
3. **Bandingkan hasilnya dengan besar bonus.** Kalau biaya > bonus, itu bukan hadiah, itu biaya.

Rumus pendeknya: **multiplier aman ≈ 1 ÷ house edge.** Game RTP 97,5% → aman sampai 40x. Game RTP 94% → hanya aman sampai 16,7x. Kuncinya bukan seberapa besar bonusnya, tapi seberapa murah kamu boleh memutarnya.

Kasino tidak pernah salah hitung soal ini. Yang sering salah hitung adalah pemain yang membaca "100%" sebagai keuntungan.

— Chokdi 🐷 · Content Studio · 2026
