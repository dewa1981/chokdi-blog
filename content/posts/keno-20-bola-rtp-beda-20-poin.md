---
title: "Keno: 20 Bola dari 80, tapi RTP-nya Beda 20 Poin di Mesin Sebelah"
date: 2026-10-31T18:05:00+07:00
draft: false
tags: ["Kasino", "Keno", "Matematika"]
---

Keno kelihatan seperti permainan paling polos di lantai kasino: papan 80 angka, kamu pilih beberapa, mesin menarik 20 bola. Tidak ada keputusan yang bisa salah, tidak ada strategi yang bisa dihitung. Tapi justru di sini ada satu hal yang jarang disadari pemain — **dua mesin keno yang menarik bola dengan cara sama sekali identik bisa mengembalikan uangmu beda hampir 20 poin persen**, dan satu-satunya penyebabnya adalah tabel bayaran yang ditempel di mesinnya. Artikel ini menghitung ulang semuanya dari kombinatorik, lalu mencocokkan hasilnya dengan paytable yang dipublikasikan, bukan mengutip brosur bandar.

## Aturannya cuma tiga baris

Satu papan berisi 80 angka. Kamu memilih 1 sampai 10 angka (disebut *spot*). Kasino menarik **20 bola tanpa pengembalian**, dan setiap angka pilihanmu yang keluar dihitung satu *catch*. Bayaran tergantung dua hal: berapa angka yang kamu pilih, dan berapa yang tertangkap.

Karena bola tidak dikembalikan, peluangnya mengikuti distribusi hipergeometrik, bukan perkalian 25% per bola:

**P(catch k) = C(p, k) × C(80−p, 20−k) ÷ C(80, 20)**

dengan p = jumlah angka yang kamu pilih. Untuk pick 10, penyebutnya C(80,10) = **1.646.492.110.120** susunan — angka inilah yang membuat keno terasa "hampir kena".

## Peluangnya tidak seindah yang terlihat

Hasil hitung untuk dua pilihan populer:

| Catch | Pick 6 | Pick 10 |
|---|---|---|
| 0 | 16,66% | 4,58% |
| 1 | 36,35% | 17,96% |
| 2 | 30,83% | 29,53% |
| 3 | 12,98% | 26,74% |
| 4 | 2,85% | 14,73% |
| 5 | 0,31% | 5,14% |
| 6 | 0,0129% (1 in 7.753) | 1,15% |
| 7 | — | 0,161% (1 in 621) |
| 8 | — | 0,0135% (1 in 7.384) |
| 9 | — | 0,000612% (1 in 163.381) |
| 10 | — | 0,0000112% (1 in 8.911.711) |

Rata-rata tangkapan untuk pick 10 tetap **2,50** dari 10 angka, dengan simpangan baku hanya **1,29**. Artinya hasilmu hampir selalu menumpuk di sekitar 2–3 tangkapan: peluang dapat 2 atau 3 angka = **56,27%**, sementara peluang dapat 5 ke atas (satu-satunya zona yang benar-benar untung di tabel umum) cuma **6,47%**. Papan yang terasa "sayang sekali, kurang satu" itu memang distribusi normal, bukan sial.

## Dari peluang ke RTP: satu rumus, dua baris hitungan

RTP = Σ [P(catch k) × total bayaran untuk catch itu]. Coba paytable yang memuat 3x, 4x, 75x, dan 1.660x untuk pick 6:

| Catch | Peluang | Bayar | Sumbangan ke RTP |
|---|---|---|---|
| 3 | 12,981955% | 3x | 38,95 pp |
| 4 | 2,853792% | 4x | 11,42 pp |
| 5 | 0,309564% | 75x | 23,22 pp |
| 6 | 0,012898% | 1.660x | 21,41 pp |
| **Total** | | | **94,99%** |

Angka 94,99% itu bukan tebakan — sama persis dengan return yang dipublikasikan untuk paytable tersebut, dan seluruh tabel pick 1–10 di artikel ini juga cocok dengan hitungan pihak ketiga. Artinya tidak ada yang disembunyikan di mekanika bolanya; yang berbeda cuma harga yang dibayar.

## Jackpot 10.000x cuma menyumbang 0,11 poin

Ini bagian yang paling sering salah dibaca pemain. Ambil paytable populer untuk pick 10: catch 0 dibayar 1x, catch 5 dibayar 5x, 6 → 25x, 7 → 120x, 8 → 500x, 9 → 2.000x, dan 10 dari 10 → 10.000x. Total RTP-nya **86,43%** — house edge 13,57%, tiga kali lebih mahal daripada [Plinko 16 baris](/posts/plinko-16-baris-rtp-99-persen/) atau [Mines](/posts/mines-kotak-aman-bikin-makin-berbahaya/). Pecahannya:

| Catch | Bayar | Peluang | Sumbangan |
|---|---|---|---|
| 0 | 1x (uang kembali) | 4,58% | 4,58 pp |
| 5 | 5x | 5,14% | 25,71 pp |
| 6 | 25x | 1,15% | **28,70 pp** |
| 7 | 120x | 0,161% | 19,33 pp |
| 8 | 500x | 0,0135% | 6,77 pp |
| 9 | 2.000x | 0,000612% | 1,22 pp |
| 10 | 10.000x | 0,0000112% | **0,11 pp** |

Baca baris terakhir pelan-pelan: hadiah yang paling diperjuangkan orang — 10 dari 10, bayaran 10.000x — menyumbang **0,11 poin** dari total 86,43%, alias **0,13% dari seluruh nilai pengembalian**. Sementara "uang kembali" saat tidak dapat satu angka pun menyumbang 4,58 poin, sekitar **41 kali lebih besar** dari jackpot itu. Pemenang sesungguhnya di tabel ini adalah tangkapan 6 angka (25x) dengan 28,70 poin. Kemenangan yang membuatmu bertahan bukan yang membuatmu kaya.

Dan soal 1 banding 8.911.711 itu: kalau satu putaran berjalan tiap menit tanpa henti, rata-rata kamu butuh **16,94 tahun** untuk sekali menang penuh. Dalam 10.000 putaran, peluang tidak pernah menyentuhnya masih **99,89%**.

## Satu mesin, sepuluh pilihan, selisih 20 poin

Sekarang bagian yang paling praktis. Pada paytable yang memuat baris pick 1 sampai 10, angka pilihanmu menentukan RTP secara langsung:

| Pick | RTP |
|---|---|
| 1 | 75,00% |
| 2 | 90,19% |
| 3 | 94,35% |
| 4 | 94,78% |
| 5 | 94,95% |
| 6 | **94,99%** |
| 7 | 94,92% |
| 8 | 94,90% |
| 9 | 93,60% |
| 10 | 93,20% |

Pilih 1 angka: 25% peluang menang, dibayar 3x → 0,25 × 3 = **75%**. Di mesin yang sama, pilih 6 angka → **94,99%**. Selisih **19,99 poin** tanpa satu pun bola berubah, hanya karena tabel bayarannya berbeda per jumlah pick. Puncaknya di pick 6; menambah ke 10 angka justru menurunkan RTP ke 93,20% walau hadiahnya tampak lebih besar.

Sebagai pembanding di lapangan, survei langsung keno Las Vegas 2001 menemukan return **65%–80%**, Laughlin 2012 hanya **50%–74%**, sedangkan video keno San Diego 2008 di **84%–95%**. Keno live termasuk taruhan termahal yang bisa kamu temukan — lebih mahal daripada kebanyakan slot.

## Dalam rupiah

Modal Rp10.000 per putaran, 100 putaran (turnover Rp1.000.000):

| Pilihan | RTP | Rata-rata sisa |
|---|---|---|
| Pick 1, bayaran 3x | 75,00% | rugi **Rp250.000** |
| Pick 10, tabel biasa | 86,43% | rugi **Rp135.700** |
| Pick 6, tabel bagus | 94,99% | rugi **Rp50.100** |

Selisih Rp85.600 dari Rp1 juta turnover — untuk permainan yang sama, di malam yang sama.

## Empat jebakan yang mahal

1. **"Angka langganan"**. Tiap undian independen; 20 bola ditarik dari himpunan yang sama tiap putaran. Angka yang kamu pakai 10 tahun tidak punya peluang lebih baik daripada pilihan acak detik ini.
2. **Mengejar 10.000x**. Kontribusinya 0,11 poin dari RTP, dan butuh rata-rata 16,94 tahun pada laju satu putaran per menit.
3. **Main 1 angka karena "25% itu besar"**. Hit ratenya memang tertinggi di papan, tapi bayaran 3x membuat RTP-nya 75% — pilihan terburuk di tabel yang sama.
4. **Mengira pilih lebih banyak = lebih baik**. Dari pick 6 (94,99%) ke pick 10 (93,20%), return turun hampir 1,8 poin meski hadiah maksimalnya terlihat jauh lebih menarik.

## Checklist sebelum duduk

- Cari **tabel bayaran** dulu, bukan tampilan papan: hitung RTP untuk jumlah pick yang kamu mau (Σ peluang × bayaran). Pilih jumlah pick dengan RTP tertinggi **di mesin itu** — untuk banyak paytable, itu pick 4–6, bukan pick 10.
- Jangan pakai uang yang kamu butuhkan: house edge keno 5%–25% bukan gangguan kecil.
- Bandingkan dengan meja lain sebelum bertahan — di [Craps](/posts/craps-house-edge-pass-line-vs-any-7/) taruhan terbaik cuma 1,41%, di [Baccarat](/posts/baccarat-banker-vs-player-house-edge/) 1,06%, di [Roulette Eropa](/posts/roulette-house-edge-martingale/) 2,70%. Kalau tujuannya hiburan, sadari ongkosnya.
- Ingat hasil [Kelly Criterion](/posts/kelly-criterion-ukuran-taruhan-bankroll/): pada permainan ber-EV negatif, ukuran taruhan optimalnya nol. Sisanya cuma soal seberapa besar kamu rela membayar untuk hiburan itu.

## Kesimpulan

Keno tidak curang. Bolanya adil, 20 dari 80, dan peluangnya bisa dihitung sampai digit terakhir. Yang tidak adil adalah **harga**: tabel bayaran bisa memotong 5% atau 25% dari uangmu, dan pemain tidak pernah diajak melihat tabelnya — hanya papannya. Antara pick 1 dan pick 6 di mesin yang sama ada 20 poin RTP; antara dua mesin di kota yang sama bisa 30 poin lebih. Kalau tetap bermain, biaya sesungguhnya bukan keberuntungan, tapi tabel yang kamu lupakan.

<!-- cta-funnel -->
> Mau lihat sendiri bagaimana papan 80 angka ini bergerak? Coba meja kasino langsung dan bandingkan angka RTP di artikel ini dengan tabel bayaran yang muncul di layar.
>
> **[MAIN SEKARANG — MEJA KASINO VIP →](https://tomat.jagungbaru.com/banner/vip?utm_source=blog&utm_campaign=keno-20-bola-rtp-beda-20-poin)**

— Chokdi 🐷 · Content Studio · 2026
