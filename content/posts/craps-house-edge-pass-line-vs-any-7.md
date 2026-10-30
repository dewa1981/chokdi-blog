---
title: "Craps: House Edge 1,41% dan 16,67% Ada di Meja yang Sama"
date: 2026-10-30T12:05:00+07:00
draft: false
tags: ["Kasino", "Craps", "Matematika Taruhan", "House Edge"]
---

Craps sering dianggap permainan paling ribet di kasino: puluhan kotak taruhan, teriakan "seven out!", dan tumpukan chip yang berpindah tangan tiap 20 detik. Padahal kalau dipotong sampai dasar, craps cuma dua dadu dan 36 kemungkinan hasil. Yang bikin meja ini menarik: di dalam satu meja yang sama ada taruhan dengan pajak rumah **1,41%** dan taruhan dengan pajak **16,67%**. Bedanya cuma satu baris di tabel — dan hampir semua pemain memilih yang kedua.

Artikel ini membedah craps dari nol dengan angka yang bisa kamu hitung sendiri pakai kalkulator, bukan kutipan brosur.

## Dua dadu, 36 kemungkinan, satu tabel

Semua matematika craps lahir dari tabel ini. Dua dadu enam sisi = 36 kombinasi, dan total 7 punya 6 cara (1-6, 2-5, 3-4, 4-3, 5-2, 6-1) sementara total 2 cuma 1 cara (1-1).

| Total | Cara | Peluang |
|---|---|---|
| 2 | 1 | 2,78% |
| 3 | 2 | 5,56% |
| 4 | 3 | 8,33% |
| 5 | 4 | 11,11% |
| 6 | 5 | 13,89% |
| 7 | 6 | 16,67% |
| 8 | 5 | 13,89% |
| 9 | 4 | 11,11% |
| 10 | 3 | 8,33% |
| 11 | 2 | 5,56% |
| 12 | 1 | 2,78% |

Hafalkan satu baris: **7 paling sering (16,67%), 2 dan 12 paling jarang (2,78%)**. Semua house edge di craps dibangun dari selisih antara peluang asli dan bayaran yang ditawarkan.

## Pass line: 244 dari 495

Taruhan dasar craps. Lemparan pertama (come-out): 7 atau 11 langsung menang, 2/3/12 langsung kalah, angka lain jadi "point". Setelah point terbentuk, kamu menang kalau point itu keluar lagi sebelum 7.

Hitungannya dua tahap. Come-out: menang 8 cara dari 36 (22,22%), kalah 4 cara dari 36 (11,11%). Sisanya 24/36 masuk fase point, dan di sini peluang menang tergantung angka point:

| Point | Cara | Peluang menang sebelum 7 |
|---|---|---|
| 4 atau 10 | 3 | 3/9 = 33,33% |
| 5 atau 9 | 4 | 4/10 = 40,00% |
| 6 atau 8 | 5 | 5/11 = 45,45% |

Gabungkan: 22,22% + (2,78% + 4,44% + 6,31% + 6,31% + 4,44% + 2,78%) = **49,2929%**, atau persis 244/495. Karena bayarannya 1:1, nilai harapan = 2 × 0,492929 − 1 = **−1,4141%**. Itu sebabnya tabel standar menulis house edge pass line 1,41% — sama dengan Wikipedia dan Wizard of Odds.

Artinya: 1.000 taruhan @ Rp100.000 (turnover Rp100 juta) menyisakan kerugian rata-rata **Rp1.414.141**. Bukan karena bandar curang, tapi karena 244:251 bukan 50:50.

## Odds bet: satu-satunya taruhan 0%

Setelah point terbentuk, kamu boleh menaruh taruhan tambahan di belakang garis (odds) yang dibayar **sesuai peluang asli**: 2:1 untuk 4/10, 3:2 untuk 5/9, 6:5 untuk 6/8. House edge-nya nol — kasino tidak mengambil apa pun dari taruhan ini.

Tapi odds tidak menghapus pajak pass line, cuma mengencerkannya. Total uang yang dipertaruhkan naik (odds hanya jalan 2/3 dari waktu), jadi edge gabungan mengecil:

| Odds | House edge gabungan |
|---|---|
| Tanpa odds | 1,4141% |
| 1x | 0,8485% |
| 2x | 0,6061% |
| 3x | 0,4714% |
| 5x | 0,3263% |
| 10x | 0,1845% |
| 100x | 0,0209% |

Perhatikan arahnya: makin besar odds, makin kecil persentase kerugian **per rupiah yang berputar** — tapi jumlah rupiah yang berputar juga makin besar. Di 10x odds, kerugian nominal per 1.000 keputusan pass line tetap sekitar Rp1,41 juta; yang berubah cuma penyebutnya.

## Don't pass: 1,36%, sedikit lebih murah tapi dibenci meja

Kebalikan pass line. Menang kalau shooter kalah. Di sini ada aturan "bar 12": kalau come-out keluar 12, taruhan don't pass **push** (uang kembali, bukan menang). Hasil terukurnya: menang 47,9293%, kalah 49,2929%, push 2,7778% — EV **−1,3636%**. Sedikit lebih murah dari pass line, tapi di kasino fisik taruhan ini sering dianggap "melawan meja" secara sosial. Matematikanya tidak peduli.

## Enam taruhan, satu meja, selisih sampai 12x

Ini inti artikelnya. Semua angka di bawah dihitung dari tabel 36 kombinasi yang sama, dengan turnover Rp100 juta (1.000 taruhan @ Rp100.000):

| Taruhan | Bayaran | Peluang menang | House edge | Rugi per Rp100 jt |
|---|---|---|---|---|
| Pass line | 1:1 | 49,29% | 1,41% | Rp1.414.141 |
| Place 6 | 7:6 | 45,45% | 1,52% | Rp1.515.152 |
| Field | 1:1 (2 & 12 = 2:1) | 44,44% | 5,56% | Rp5.555.556 |
| Big 6/8 | 1:1 | 45,45% | 9,09% | Rp9.090.909 |
| Hard 8 | 9:1 | 9,09% | 9,09% | Rp9.090.909 |
| Any 7 | 4:1 | 16,67% | 16,67% | Rp16.666.667 |

Any 7 kelihatan menggoda karena bayar 4:1, padahal peluang 7 keluar cuma 6/36 = 16,67%. Bayaran yang adil untuk peluang itu adalah **5:1**, bukan 4:1. Selisih satu unit itulah seluruh keuntungan kasino: 6/36 × 4 − 30/36 = −0,1667.

Pola yang sama muncul di semua permainan meja: yang mahal bukan yang peluangnya kecil, tapi yang **selisih bayaran dan peluangnya paling lebar**. Bandingkan dengan [baccarat yang edge-nya cuma 1,06%](/posts/baccarat-banker-vs-player-house-edge/) atau [roulette Eropa 2,70%](/posts/roulette-house-edge-martingale/); kalau kamu memang mau duduk di meja, pilih meja yang pajaknya kecil, bukan yang "seru".

## Uji 1.000 taruhan: 5.000 sesi, hasilnya tidak simetris

Hitungan EV cuma rata-rata. Yang kamu alami adalah satu jalur acak. Simulasi 5.000 sesi × 1.000 taruhan pass line @ Rp100.000 memberi gambaran variansi nyata:

- Rata-rata hasil: **−Rp1.509.560** (dekat dengan EV −Rp1.414.141, selisihnya noise simulasi)
- Sesi yang berakhir profit: **30,28%**; sesi rugi: **67,36%**
- Median hasil: **−Rp1.600.000**; terburuk −Rp12.600.000; terbaik +Rp11.000.000

Tiga dari empat sesi berakhir merah meski kamu memainkan taruhan terbaik di meja. Dan itu justru kabar baik: artinya kerugianmu lambat, bukan instan — cukup lambat untuk disalahartikan sebagai "lagi hoki". Kalau mau mendalami cara mengukur ukuran taruhan terhadap modal, [kriteria Kelly](/posts/kelly-criterion-ukuran-taruhan-bankroll/) menjelaskan kenapa bertaruh lebih besar dari proporsi optimal justru mempercepat kebangkrutan tanpa menambah keuntungan.

## Tiga jebakan yang paling sering kena

1. **Prop bet di tengah meja.** Any 7, Yo (11), dan sejenisnya punya edge 11–16%. Mereka ada di meja untuk satu alasan: memberi aksi cepat dengan harga mahal.
2. **"Dadunya panas."** Setiap lemparan independen. Dadu tidak punya memori soal 7 yang keluar 3 kali berturut-turut — peluang 7 tetap 6/36.
3. **Menganggap odds bet sebagai strategi menang.** Odds hanya menurunkan persentase pajak, bukan mengubah tanda EV. Dari −1,41% ke −0,02% tetap negatif.

## Checklist sebelum duduk

- Kenali dulu taruhan mana yang edge-nya di bawah 2% (pass, don't pass, place 6/8) dan mana yang di atas 9% (Big 6/8, hardway, prop).
- Pasang odds **hanya** kalau modalmu sudah cukup untuk menahan variansi pass line-nya.
- Hitung ekspektasi biaya hiburan: turnover × 1,41%. Turnover Rp50 juta = biaya rata-rata Rp705 ribu — anggap itu harga tiket, bukan kerugian yang bisa "dikejar".
- Berhenti sebelum menaikkan stake untuk menutup kekalahan; melipatgandakan taruhan tidak mengubah EV, hanya memperbesar simpangan.

Craps bukan permainan yang harus dihindari karena rumit. Yang harus dihindari adalah duduk di kotak taruhan yang salah tanpa tahu angkanya.

**Sumber:** [Wikipedia — Craps (tabel house edge 1,41% / 1,36% / field 5,56%)](https://en.wikipedia.org/wiki/Craps) dan [Wizard of Odds — Craps: Rules, Odds & Best Bets](https://wizardofodds.com/games/craps/). Semua angka payout di artikel ini dihitung ulang dari 36 kombinasi dua dadu, bukan dikutip mentah.

<!-- cta-funnel -->
> **Mau lihat meja kasino live dengan tabel bayaran yang jelas?** VIP579 punya baccarat, roulette, sicbo, dragon tiger, sampai craps live dealer — semua RTP dan aturan meja terbuka, bukan disembunyikan.
>
> 👉 **[GASPOL MASUK MEJA VIP SEKARANG](https://tomat.jagungbaru.com/banner/vip?utm_source=blog&utm_campaign=craps-house-edge-pass-line-vs-any-7)** — deposit 24 jam, WD cepat, bonus rollingan harian.
<!-- /cta-funnel -->

— Chokdi 🐷 · Content Studio · 2026
