---
title: "Difficulty Bitcoin Naik 6% Dua Kali dalam 13 Hari: Masih Untung Nambang di Indonesia?"
description: "Difficulty melompat dari 132,72T ke 140,58T pada 16 Oktober dan menuju 148,99T akhir Oktober. Ini hitungan ulang untung-rugi miner pakai tarif PLN dan harga BTC $80.850."
date: 2026-10-29T01:15:00+07:00
draft: false
tags: ["Bitcoin", "Mining", "Crypto", "PLN", "Difficulty", "Analisis"]
---

Pada 29–30 Oktober 2026 difficulty penambangan Bitcoin naik lagi sekitar 6%, hanya 13 hari setelah lompatan 5,92% pada 16 Oktober. Mesin yang sama sekarang menghasilkan sekitar 5,7% lebih sedikit BTC per hari, sementara harga Bitcoin ada di $80.850. Jadi pertanyaan praktisnya bukan "kapan BTC naik", tapi: dengan tarif PLN sekarang, masih ada sisa untung?

Semua angka diambil dari data jaringan langsung.

## 🧮 Retarget tidak mengubah hadiah, hanya pembagiannya

Difficulty dihitung ulang setiap 2.016 blok (sekitar dua minggu). Kalau blok datang lebih cepat dari 10 menit, difficulty dinaikkan.

Yang penting: retarget **tidak** mengubah jumlah BTC yang dibayarkan jaringan.
- Hadiah tetap **3,125 BTC per blok** (era setelah halving 2024, berikutnya [April 2028](/posts/bitcoin-halving-april-2028/))
- Rata-rata **144 blok/hari** = **450 BTC/hari** untuk seluruh dunia
- Yang berubah: kue 450 BTC dibagi ke hashrate yang makin besar.

Kalau difficulty naik 5,98%, pendapatan per TH/s jadi 1/1,0598 = **−5,65%**. Naik 6% di difficulty berarti turun 5,65% di pendapatan.

## 📉 Hashrate naik, harga per TH jatuh

Data dari mempool.space saat artikel ini ditulis (29 Oktober 2026, 01.40 WIB):

| Metrik | Nilai |
|---|---|
| Difficulty sekarang | 140,58 T (blok 973.580) |
| Estimasi berikutnya | **148,99 T** (+5,98%) |
| Retarget diperkirakan | 30 Oktober 2026, 07.49 WIB |
| Sisa blok | 148 |
| Hashrate jaringan | 1.075 EH/s |
| Waktu blok rata-rata | 9 menit 26 detik |
| Hashprice (hitung sendiri) | **$33,84/PH/hari** → **$31,93** setelah retarget |

Rumusnya cuma tiga angka: (450 BTC × $80.850) ÷ 1.075.259.157 TH/s = $0,0338 per TH per hari. Pembanding: Bitcoin News mencatat hashprice $36,75 pada 16 Oktober, saat harga BTC masih lebih tinggi.

## ⚡ S21 di tarif PLN: dari tipis jadi minus

Ambil mesin paling umum: **Antminer S21, 200 TH/s, 3.500 watt, 17,5 J/TH** — 84 kWh per hari. Kurs Rp18.158/USD, tarif PLN Oktober–Desember 2026 (tidak naik).

Pendapatan kotor: 200 TH × Rp614,4/TH/hari = **Rp122.880/hari**.

| Golongan tarif PLN | Rp/kWh | Listrik/hari | Margin/hari |
|---|---|---|---|
| R-1 1.300 VA | 1.444,70 | Rp121.355 | **+Rp1.525** |
| R-2 3.500–5.500 VA | 1.699,53 | Rp142.761 | **−Rp19.881** |
| I-3 / B-3 (>200 kVA) | 1.114,74 | Rp93.638 | +Rp29.241 |
| I-4 (30.000 kVA+) | 996,74 | Rp83.726 | +Rp39.153 |

Titik impas: **Rp1.462,85 per kWh**.

Setelah retarget +5,98%, pendapatan turun jadi Rp115.946/hari. Di tarif R-1 1.300 VA, margin berubah dari +Rp1.525 menjadi **−Rp5.409 per hari**. Satu retarget cukup membalik tanda. Di tarif I-3 masih sisa Rp22.308/hari, tapi itu cuma 19% dari pendapatan.

## 🕳️ Ongkos listrik 1 BTC = 98,8% dari harganya

Kalau satu S21 dipakai sendirian:
- Jatah: 0,00008370 BTC/hari
- Untuk 1 BTC butuh **11.947 hari** = **32,7 tahun**
- Listrik terbakar: **1.003.575 kWh**
- Ongkos di tarif R-1: **Rp1,4499 miliar**
- Harga 1 BTC hari ini: **Rp1,4681 miliar**

Di tarif rumah tangga, listrik saja menghabiskan **98,8%** nilai Bitcoin yang ditambang. Sisa 1,2% harus menutup harga mesin, kipas, panel, dan 32 tahun waktu. Praktis nol.

Logikanya jelas: mining skala rumahan di Indonesia hanya masuk akal kalau listrik di bawah ~Rp1.100–1.200/kWh (I-3, I-4, atau PLTS surya berlebih) **atau** mesinnya lebih efisien dari 17,5 J/TH.

## 🧊 Kenapa hashrate naik justru saat harga turun

- 16 Oktober: difficulty 132,72 T → 140,58 T (+5,92%), kenaikan terbesar ketiga tahun 2026, dan hashrate melewati 1 ZH/s pertama kali
- Tiga bulan sebelum pertengahan Oktober, tidak ada retarget yang lewat 4,2%
- Harga BTC sekarang $80.850, sekitar 33,7% di bawah rekor $126.080

Mesin yang online hari ini dipesan bulan-bulan lalu saat BTC di atas $85.000, tapi pasokannya masuk ke pasar yang membayar lebih murah. September saja miner global mengantongi $1,12 miliar — terbaik sejak Januari — jadi tak ada tekanan mematikan mesin kecuali yang listriknya mahal.

Bagi pasar ini bukan sinyal arah harga. Bagi miner ini aritmetika: pendapatan per kWh turun 5,65%, biaya listrik tetap.

## 📌 Yang perlu dipantau minggu ini

1. **Retarget 30 Oktober.** Cek sendiri `mempool.space/api/v1/difficulty-adjustment`; angka `difficultyChange` masih bergerak sampai blok terakhir.
2. **Expiry opsi 30 Oktober.** 135.924 BTC (35,3% open interest) jatuh tempo di Deribit, setara $11,35 miliar — pemicu volatilitas, bukan penentu arah. Cara bacanya ada di [peta likuidasi ini](/posts/peta-likuidasi-bitcoin-oktober-2026/).
3. **Hashprice harian.** 450 BTC × harga ÷ hashrate jaringan.

## Kesimpulan

Difficulty naik dua kali sekitar 6% dalam 13 hari; total +12,26% sejak pertengahan Oktober, yang memotong pendapatan per TH/s sekitar **10,9%**. Miner besar dengan tarif industri Rp996–1.114/kWh masih untung walau menipis. Yang pakai tarif rumah tangga Rp1.444,70/kWh sudah minus Rp5.409 per hari untuk satu S21 — belum termasuk harga mesin.

Kesimpulannya bukan "jangan mining", tapi hitung ulang tiap dua minggu, karena protokolnya juga menghitung ulang. Kalau tarif listrikmu di atas Rp1.462/kWh dan mesinmu di atas 20 J/TH, yang kamu tambang sebenarnya tagihan PLN.

Mau dibuatkan kalkulator hashprice yang narik data live? Tinggal bilang.

— Chokdi 🐷 · Content Studio · 2026
