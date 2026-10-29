---
title: "Pot Odds dan Outs Poker: Kenapa Rule of 2 dan 4 Sering Salah"
date: 2026-10-29T12:05:00+07:00
draft: false
tags: ["Poker", "Matematika", "Strategi"]
---

Kamu punya flush draw di flop, lawan taruh bet sebesar pot, dan kepala langsung bilang "9 outs × 2 = 18%, pot odds 33%, fold". Angka 18% itu taksiran kasar. Yang sebenarnya: **19,15%** kalau cuma satu kartu tersisa, dan **34,97%** kalau dua kartu tersisa — dan dua angka itu memberi jawaban yang **berlawanan** untuk taruhan yang sama. Artikel ini membongkar di mana *rule of 2 dan 4* masih berguna, di mana dia bohong, dan bagaimana menghitung batas call yang benar-benar impas dalam rupiah.

## Dua angka dasar: outs dan pot odds

**Outs** = jumlah kartu sisa yang membuat tanganmu menang. **Pot odds** = harga yang kamu bayar dibanding total pot setelah kamu call.

Rumusnya satu baris:

```
ekuitas yang dibutuhkan = call / (pot + 2 × call)
```

Pot Rp100.000, lawan bet Rp100.000, kamu call Rp100.000 → butuh 100.000 / 300.000 = **33,33%**. Kalau peluangmu lebih besar dari itu, call-nya untung.

| Taruhan lawan | Call | Pot akhir | Ekuitas dibutuhkan |
|---|---|---|---|
| 50.000 (½ pot) | 50.000 | 200.000 | 25,00% |
| 100.000 (1 pot) | 100.000 | 300.000 | 33,33% |
| 150.000 (1,5 pot) | 150.000 | 400.000 | 37,50% |

## Rule of 2 dan 4: cepat, tapi bukan kebenaran

Aturannya: kalikan outs × 2 untuk satu kartu tersisa, × 4 kalau dua kartu tersisa (flop ke river). Ini shortcut yang dipopulerkan Phil Gordon, dan memang berguna — sayangnya arah kesalahannya **tidak konsisten**.

| Outs | Ekuitas exact (2 kartu) | Rule × 4 | Selisih |
|---|---|---|---|
| 4 (gutshot) | 16,47% | 16% | −0,47 |
| 8 (OESD) | 31,45% | 32% | +0,55 |
| 9 (flush draw) | 34,97% | 36% | +1,03 |
| 12 | 44,96% | 48% | +3,04 |
| 15 (OESD + flush) | 54,12% | 60% | **+5,88** |
| 20 | 67,53% | 80% | **+12,47** |

Artinya: untuk draw standar 8–9 outs, rule × 4 cuma lebih tinggi sekitar 1 poin — aman. Tapi begitu outs menumpuk, dia mulai menipu: di 15 outs kamu dikira punya 60%, padahal aslinya 54,12%. Orang yang percaya angka 60% akan call taruhan yang sebenarnya −EV.

## Kesalahan kedua: rule of 2 justru MEREMEHKAN

Ini yang jarang dibahas. Untuk satu kartu tersisa, peluang sebenarnya bukan 2×outs, tapi outs/47 (flop ke turn) atau outs/46 (turn ke river).

| Outs | Flop → turn | Turn → river | Rule × 2 | Selisih |
|---|---|---|---|---|
| 4 | 8,51% | 8,70% | 8% | −0,70 |
| 8 | 17,02% | 17,39% | 16% | −1,39 |
| 9 | 19,15% | 19,57% | 18% | −1,57 |
| 15 | 31,91% | 32,61% | 30% | −2,61 |

Semua selisihnya **negatif**. Rule of 2 bikin kamu terlalu sering fold di spot marginal — dan spot marginal itulah tempat uang menumpuk di meja.

## Jebakan ketiga: menjumlahkan 4/47 + 4/46

Banyak yang menghitung dua kartu dengan menambah peluang turn dan river. Untuk 9 outs:

- Cara naif: 9/47 + 9/46 = **38,71%**
- Exact: 1 − (38 × 37)/(47 × 46) = **34,97%**
- Kelebihan: **+3,75 poin**

Kelebihannya datang dari **double counting** — kombinasi "hit di turn lalu hit lagi di river" dihitung dua kali. Untuk 4 outs kelebihannya +0,74 poin; makin besar outs, makin besar pula bengkaknya.

## Batas call impas — angka yang benar-benar bisa dipakai

Daripada mengira-ngira, balik rumusnya. Untuk pot Rp100.000, ini call maksimum yang masih impas (EV = 0):

| Draw | Outs | Ekuitas 2 kartu | Call maksimum |
|---|---|---|---|
| Gutshot | 4 | 16,47% | Rp24.552 |
| OESD | 8 | 31,45% | Rp84.788 |
| Flush draw | 9 | 34,97% | Rp116.308 |
| OESD + flush draw | 15 | 54,12% | tanpa batas |

Baris terakhir penting: karena 54,12% sudah di atas 50%, **berapa pun** taruhannya tetap +EV selama tidak ada taruhan lagi di turn. Cek: lawan bet Rp10 juta ke pot Rp100.000 → ekuitas yang dibutuhkan cuma 49,75%, masih di bawah 54,12%.

## Tiga keputusan nyata dengan modal Rp100.000

Pakai ekuitas exact, pot awal selalu Rp100.000:

| Skenario | Call | EV |
|---|---|---|
| Flush draw vs bet 1 pot | 100.000 | **+4.903** |
| Flush draw vs bet ½ pot | 50.000 | **+19.935** |
| Gutshot vs bet 1 pot | 100.000 | **−50.601** |
| Gutshot vs bet ½ pot | 50.000 | **−17.068** |
| OESD + flush vs bet 1 pot | 100.000 | **+62.350** |

Flush draw vs pot bet cuma untung tipis Rp4.903 — dan di sinilah rake masuk.

## Rake Rp15.000 yang membalik segalanya

Meja kasino memotong rake, umumnya 5% dari pot dengan cap tertentu. Pot Rp300.000 × 5% = **Rp15.000**. Yang dibayar ke pemenang tinggal Rp285.000, jadi EV call pertama tadi berubah:

- Tanpa rake: 0,3497 × 300.000 − 100.000 = **+4.903**
- Setelah rake: 0,3497 × 285.000 − 100.000 = **−342**

Keputusan yang "benar secara matematis" jadi rugi setelah potongan meja. Ini alasan pemain pro menghitung rake sebagai bagian dari pot odds, bukan biaya terpisah — sama seperti [house edge di baccarat](/posts/baccarat-banker-vs-player-house-edge/) dan [roulette](/posts/roulette-house-edge-martingale/) yang tidak pernah hilang dari meja.

## Empat jebakan yang paling mahal

1. **Hitung outs kotor, bukan outs bersih.** Flush draw 9 outs — tapi kalau lawan bisa punya full house lebih besar, dua di antaranya bukan outs menang.
2. **Pakai rule × 4 padahal masih ada taruhan di turn.** × 4 hanya sah kalau lawan all-in di flop; kalau tidak, kamu bayar dua kali untuk satu peluang.
3. **Lupa kartu di tangan lawan.** 47 kartu tak terlihat di flop, bukan 52 — angka 47/46 itu sudah memperhitungkan kartu mati, tapi tidak memperhitungkan blocker lawan.
4. **Berhenti di hit rate, tidak menghitung ukuran taruhan.** Menghitung EV satu keputusan beda dengan menghitung [ukuran taruhan optimal untuk bankroll](/posts/kelly-criterion-ukuran-taruhan-bankroll/) — yang kedua menjaga kamu tetap duduk.

## Kesimpulan

Rule of 2 dan 4 tetap alat yang bagus untuk meja cepat: akurasinya dalam 1 poin untuk draw 8–9 outs. Tapi untuk keputusan bernilai besar — terutama saat menghadapi all-in atau taruhan besar — pakai angka exact: satu kartu = outs/47 atau outs/46, dua kartu = 1 − (47−outs)(46−outs)/(47 × 46). Lalu bandingkan dengan call ÷ (pot + 2 × call), dan jangan lupa potong rake.

Kalau mau latihan dengan uang nyata, mulai dari taruhan kecil sampai batas call ini jadi refleks — bukan hafalan.

<!-- cta-funnel -->
> **Mau langsung praktik di meja?** Meja kartu dan live casino VIP ada di sini — daftar dulu, main setelah batas call-nya kamu hafal.
> **[GASPOL DAFTAR SEKARANG →](https://tomat.jagungbaru.com/banner/vip?utm_source=blog&utm_campaign=pot-odds-outs-poker-rule-2-4)** · modal kecil, hitungan dulu, baru gas.

---

— Chokdi 🐷 · Content Studio · 2026
