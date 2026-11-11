---
title: "Dragon Tiger: Taruhan Seri 8:1 Cuma Bayar 64,6% dari Adil — House Edge 32,77%"
description: "Dragon Tiger cuma satu kartu lawan satu kartu, tapi house edge taruhan seri 8:1 mencapai 32,77%. Hitungan lengkap 416 kartu, 8 dek, plus varian 'seri kalah setengah' yang bikin edge taruhan utama jadi 3,73%."
date: 2026-11-11T12:10:00+07:00
draft: false
tags: ["Dragon Tiger", "House Edge", "Kasino", "Matematika Taruhan", "Edukasi Judi"]
---

# Dragon Tiger: Taruhan Seri 8:1 Cuma Bayar 64,6% dari Adil — House Edge 32,77%

Dragon Tiger kelihatan seperti permainan paling jujur di lantai kasino: **satu kartu untuk Dragon, satu kartu untuk Tiger, yang lebih tinggi menang**. Tidak ada keputusan, tidak ada strategi, tidak ada hitungan kartu. Justru karena sesederhana itu, semua keunggulan rumah disembunyikan di dua tempat yang jarang dibaca pemain: **aturan saat seri** dan **pembayaran taruhan Tie**.

Artikel ini menghitung ulang semuanya dari nol — 416 kartu, 8 dek, 172.640 pasangan kartu berurutan — lalu mencocokkannya dengan analisis Michael Shackleford (Wizard of Odds). Hasilnya konsisten sampai dua desimal.

## Aturan yang menentukan segalanya

- **8 dek** (Pragmatic Play dan SA Gaming memakai 8 dek; Deltin 6–8 dek).
- Urutan kartu: **A paling rendah, K paling tinggi** — kebalikan dari feeling banyak orang yang menganggap A kartu tertinggi.
- Satu kartu untuk Dragon, satu untuk Tiger. Kartu tertinggi menang, dibayar **1:1**.
- **Kalau seri, taruhan Dragon dan Tiger kehilangan setengah** (versi yang dianalisis di sini). Sebagian meja memakai aturan "seri = push", dan itu mengubah matematikanya secara drastis.

## Sebaran hasil: cuma 7,47% ronde berakhir seri

Dengan 8 dek, tiap rank punya 32 kartu. Peluang dua kartu berurutan sama rank:

```
P(seri) = 13 × (32 × 31) / (416 × 415)
        = 12.896 / 172.640
        = 0,074699  →  7,4699%
```

Sisanya 92,5301% dibagi rata: **Dragon 46,2651%**, **Tiger 46,2651%**. Perhatikan bahwa Dragon dan Tiger benar-benar simetris — tidak ada sisi "lebih panas", tidak ada pola. Kalau dek dikurangi jadi 6, P(seri) = 7,3955%, jadi angka 7,47% ini stabil di semua versi.

## Taruhan utama: house edge 3,73%, bukan 7,47%

Karena seri cuma menghilangkan **setengah** taruhan, kerugian per unit taruhan Dragon/Tiger adalah:

```
EV = P(menang)×1 − P(kalah)×1 − P(seri)×0,5
   = 0,462651 − 0,462651 − 0,037349
   = −0,037349  →  house edge 3,7349%, RTP 96,27%
```

Kalau mejanya memakai aturan **seri = taruhan utama hangus total**, EV langsung jadi −7,47%. Dua meja yang tampak identik bisa berbeda **dua kali lipat** biaya hanya karena satu baris aturan. Ini hal pertama yang harus ditanyakan sebelum duduk.

Bandingkan dengan baccarat: Banker 1,06%, Player 1,24%. Artinya taruhan Dragon/Tiger **3,5x lebih mahal** daripada Banker, padahal sensasi mainnya hampir sama (bandingkan juga di [baccarat vs permainan kartu lain](/posts/overround-margin-bandar-1x2-persen/) saat menghitung margin bandar).

## Taruhan Tie: 8:1 yang seharusnya 12,39:1

Ini bagian paling mahal di meja. Peluang seri 7,4699% berarti pembayaran **adil** adalah:

```
1 / 0,074699 − 1 = 12,3871 : 1
```

Yang ditawarkan versi SA Gaming: **8:1**. Artinya kamu dibayar hanya **64,6% dari nilai adil**. Hitungan EV-nya:

| Pembayaran Tie | EV per 1 unit | House edge |
|---|---|---|
| 8:1 | −0,3277 | **32,77%** |
| 9:1 | −0,2530 | 25,30% |
| 10:1 | −0,1783 | 17,83% |
| 11:1 | −0,1036 | 10,36% |
| 12:1 | −0,0289 | 2,89% |

Hampir semua meja online Eropa/Asia memasang **8:1** (SA Gaming) atau **11:1** (Pragmatic Play). Selisihnya bukan detail: Rp 100.000 per ronde di Tie 8:1, main 100 ronde, rata-rata hangus **Rp 3.277.108** — sementara taruhan Dragon biasa di 100 ronde yang sama hanya rugi **Rp 373.500**. Sepuluh kali lipat lebih cepat kering.

Ada juga **Suited Tie** (rank *dan* suit sama), peluangnya 1,6867%:

```
P(suited) = 13 × 4 × (8 × 7) / (416 × 415) = 0,016867
pembayaran adil = 58,29 : 1  →  yang dibayar 50:1  →  house edge 13,98%
```

## Kenapa "seri hampir pasti datang" itu jebakan

7,47% terasa sering, dan memang sering — kira-kira 1 dari 13 ronde. Tapi frekuensi tinggi bukan berarti menguntungkan; justru itu yang membuat taruhan Tie terasa "masuk akal" padahal bayarannya dipotong 35% dari nilai wajar. Pola yang sama sudah kita bahas di [RTP slot dan volatilitas](/posts/rtp-slot-volatilitas-cara-baca-2026/): yang menentukan bukan seberapa sering menang, tapi **berapa yang dibayar saat menang**.

Soal rentetan: peluang kalah 5 kali berurutan di taruhan utama (menghitung seri sebagai kalah setengah) = 4,48%, dan 10 kali beruntun = 0,20%. Kecil, tapi di 1.000 ronde rentetan seperti itu nyaris pasti terjadi sekali — dan sistem pengganda taruhan butuh modal 2^n − 1 unit untuk bertahan n kali.

## Kesimpulan

- **Dragon/Tiger (seri kalah setengah)** = 3,73% house edge, RTP 96,27%. Masih kalah dari baccarat, tapi jauh lebih baik daripada Tie.
- **Varian seri hangus total** = 7,47%. Tanyakan aturannya dulu.
- **Tie 8:1** = 32,77% house edge. Ini bukan taruhan, ini donasi.
- **Suited Tie 50:1** = 13,98%. Lebih baik dari Tie biasa, tetap bukan taruhan bagus.
- Tidak ada sisi "panas", tidak ada pola kartu, tidak ada waktu keberuntungan. Peluangnya identik tiap ronde.

Kalau mau tetap main, mainkan taruhan utama dengan unit kecil dan anggap biayanya 3,73% per putaran — sama seperti membayar tiket masuk. Mau hitung dulu berapa modal yang wajar per sesi? Rumus [Kelly Criterion](/posts/kelly-criterion-ukuran-taruhan-bankroll/) lebih jujur daripada feeling.

## Sumber

- [Wizard of Odds — Dragon Tiger](https://wizardofodds.com/games/dragon-tiger/) (aturan 8 dek, tabel house edge, suited tie 0,016867)
- [Wizard of Odds — House Edge](https://wizardofodds.com/gambling/house-edge/) (pembanding baccarat)
- Hitungan ulang sendiri: 172.640 pasangan kartu berurutan, 8 dek, tie lose half

---

— Chokdi 🐷 · Content Studio · 2026
