---
title: "Andar Bahar: 51,5% Peluang Menang, Tapi Tetap Rugi 2,15%"
date: 2026-11-06T00:35:00+07:00
draft: false
tags: ["Casino", "Matematika", "Andar Bahar", "House Edge"]
---

Andar Bahar kelihatan paling gampang di antara semua permainan kartu kasino: satu kartu dibuka, taruhan pilih kiri atau kanan, tunggu kartu kembar muncul. Dua pilihan, tanpa strategi, tanpa keputusan rumit. Tapi di situlah jebakannya — "gampang" bukan berarti "adil". Angka aslinya: sisi **Andar menang 51,5006%**, Bahar 48,4994%, dan meski begitu pemain tetap rugi rata-rata **2,15% dari setiap taruhan** kalau bayarannya 0,9 banding 1.

Artikel ini membedah matematikanya sampai ke akar, bukan cuma bilang "rumah selalu menang".

## Aturan main dalam 30 detik

Satu set 52 kartu. Dealer membuka satu kartu di tengah — sebut saja kartu tengah (orang sering salah menyebutnya "joker", padahal dia bukan kartu liar). Setelah itu pemain bertaruh: **Andar** (dalam/kiri) atau **Bahar** (luar/kanan). Dealer lalu membagi kartu bergantian ke dua tumpukan sampai muncul kartu yang **rank-nya sama** dengan kartu tengah. Tumpukan yang dapat kartu kembar itu menang. Permainan ini berasal dari Bengaluru, India selatan, dan di Tamil dikenal sebagai *Mangatha* atau *Ullae Veliyae*.

Karena kartu pertama selalu jatuh ke sisi Andar, jumlah kartu setelah kartu tengah menentukan pemenang:

- jumlah kartu **ganjil** → Andar menang
- jumlah kartu **genap** → Bahar menang

Tidak ada seri. Tidak ada push. Tidak ada cara "main aman".

## Kenapa Andar menang 51,5%, bukan 50%

Kartu pertama setelah kartu tengah pasti milik Andar. Artinya untuk menang, Andar butuh permainan selesai di kartu ke-1, ke-3, ke-5, dan seterusnya. Peluangnya dijumlah dari distribusi panjang permainan:

| Total kartu | Peluang tepat | Peluang ≤ |
| --- | --- | --- |
| 1 | 5,88% | 5,88% |
| 3 | 5,42% | 16,95% |
| 5 | 4,97% | 27,11% |
| 10 | 3,94% | 48,81% |
| 11 | 3,75% | 52,56% |
| 20 | 2,23% | 78,42% |

Total peluang jumlah kartu ganjil = **51,5006%**. Selisih 3 poin persen dari Bahar itu bukan keberuntungan, itu struktur mekanik: Andar dapat "start duluan".

Masalahnya, 51,5% tidak cukup untuk menutup bayaran yang dipotong.

## Payout membalik semuanya

Untuk impas dengan bayaran 0,9 banding 1, pemain butuh menang `1 / 1,9 = 52,63%`. Kenyataannya cuma 51,50%. Di situlah 2,15% hilang.

| Taruhan | Bayaran | Peluang menang | House edge |
| --- | --- | --- | --- |
| Andar | 0,85 : 1 | 51,50% | **4,72%** |
| Andar | 0,90 : 1 | 51,50% | **2,15%** |
| Bahar | 0,95 : 1 | 48,50% | **5,43%** |
| Bahar | 1,00 : 1 | 48,50% | **3,00%** |

Lihat pola yang sering dilewatkan orang: **taruhan dengan peluang menang lebih besar justru dibayar lebih kecil**, dan versi bayaran yang "kelihatan murah" pun tetap lebih baik daripada versi bayaran yang lebih besar. Menawar "yang penting bayarannya tinggi" di meja ini justru bikin rugi dua kali lipat.

Contoh konkret: taruhan Rp100.000 per putaran, 100 putaran per jam di Andar 0,9:1 → ekspektasi rugi **Rp215.000 per jam**. Pindah ke Bahar 0,95:1 → rugi **Rp543.000 per jam**. Permainan yang sama, selisihnya 2,5 kali lipat, cuma karena pilihan sisi dan versi bayaran.

## Side bet: makin besar bayaran, makin dalam lubangnya

Meja Andar Bahar modern menawarkan taruhan sampingan yang jauh lebih menggoda: tebak warna kartu tengah, tebak total kartu, tebak "20 kartu atau lebih". Semuanya punya satu kesamaan — tepi rumah lebih buruk daripada taruhan utama.

| Side bet | Bayaran | Peluang | EV |
| --- | --- | --- | --- |
| Warna kartu tengah | 0,9 : 1 | 50% | −5,00% |
| Jenis (suit) kartu tengah | 2,8 : 1 | 25% | −5,00% |
| Tepat angka 8 | 11 : 1 | 7,69% | −7,69% |
| Total 20+ kartu | 2,9 : 1 | 23,82% | −7,11% |
| Total 6–10 kartu | 3,5 : 1 | 21,70% | −2,33% |
| Total 16–25 kartu | 3,5 : 1 | 21,80% | **−1,90%** |

Yang menarik: taruhan sampingan **16–25 kartu** dengan bayaran 3,5:1 punya EV −1,90% — lebih baik daripada taruhan utama Andar (−2,15%). Bukan karena kasino baik hati, tapi karena pemain menanggung varians jauh lebih besar: satu taruhan seperti itu bisa menang sekali tiap lima putaran, dan kekalahan beruntun 20 kali berturut-turut adalah hal normal, bukan anomali.

Dan taruhan "20+ kartu" yang paling ramai dipasang? EV −7,11%, nyaris tiga kali lebih buruk dari taruhan utama. Rata-rata permainan selesai di **kartu ke-13** (median 11), jadi "main panjang" memang lebih sering terjadi — tapi tidak cukup sering untuk membayar 2,9:1.

## Yang bisa disimpulkan

Andar Bahar adalah contoh bersih bagaimana kasino membangun keunggulan tanpa mengubah peluang: peluang menang pemain tetap 51,5%, yang diubah cuma **harga** dari kemenangan itu. Jadi tiga hal yang benar-benar bisa dikontrol:

1. **Pilih versi bayaran terbaik yang tersedia** — Andar 0,9:1 (−2,15%) selalu lebih baik daripada 0,85:1 (−4,72%).
2. **Hindari side bet bernomor besar** — semua yang bayarannya dua digit punya EV terburuk di meja.
3. **Ukur dalam ratusan putaran, bukan satu putaran.** Satu kemenangan 0,9:1 terasa seperti "strategi bekerja"; 1.000 putaran adalah satu-satunya ukuran yang jujur.

Kalau mau membandingkan permainan lain yang mekanismenya mirip, baca juga [Dragon Tiger: satu kartu, tiga aturan](/posts/dragon-tiger-satu-kartu-tiga-aturan/) dan [Bandar Ceme: seri melawan bandar](/posts/bandar-ceme-seri-bandar-house-edge/). Untuk yang lebih suka angka RTP mesin, ada [cara membaca RTP dan volatilitas slot](/posts/rtp-slot-volatilitas-cara-baca-2026/).

Sumber angka: analisis Michael Shackleford di [Wizard of Odds](https://wizardofodds.com/games/andar-bahar/) dan aturan historis dari [Pagat](https://www.pagat.com/banking/andar_bahar.html).

— Chokdi 🐷 · Content Studio · 2026
