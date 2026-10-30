---
title: "DCA Bitcoin Mulai dari Hari Puncak: −0,53% vs Beli Sekali −38%"
date: 2026-10-31T01:10:00+07:00
draft: false
tags: ["Crypto", "Bitcoin", "Investasi", "Data"]
---

Jumat, 30 Oktober 2026, bitcoin ditutup di US$77.028 — anjlok 4,79% dalam 24 jam dan 5,13% dalam sepekan, sementara kapitalisasi pasar kripto global turun 5,05% ke US$2,58 triliun (CoinMarketCap via Liputan6). Setiap koreksi seperti ini selalu memunculkan dua pertanyaan yang sama: masih boleh masuk, dan seburuk apa kalau saya kebetulan beli di puncak?

Alih-alih menebak, saya unduh 730 hari data BTCUSDT dari API publik Binance lalu menghitung empat cara masuk pasar dengan uang yang sama. Hasilnya lebih ekstrem dari yang saya duga.

## 📉 Posisi harga: bukan turun 5%, tapi 38% dari puncak

Berita hari ini cuma bagian paling kecil dari cerita. Dalam dua tahun terakhir:

- Puncak harga penutupan: **US$124.658,54** pada 6 Oktober 2025.
- Penutupan 30 Oktober 2026: **US$76.878,23** — berarti **−38,33%** dari puncak.
- Penurunan terdalam dari puncak berjalan ke titik terendah berikutnya: **−53,63%**.
- **695 dari 729 hari (95,3%)** harga bergerak di bawah puncak sementara saat itu.

Poin terakhir itu yang paling penting: "sedang di bawah puncak" bukan kondisi darurat, itu kondisi normal bitcoin. Yang luar biasa justru hari-hari ketika harga mencetak puncak baru.

## 🧮 Empat cara masuk pasar, modal sama, hasil beda 30 poin

Semua angka di bawah ini dihitung dari candle harian Binance, penutupan 30 Oktober 2026.

| Cara masuk | Modal | Nilai sekarang | Hasil |
|---|---|---|---|
| Beli sekali di puncak (US$110.540,68) | US$3.650 | US$2.538,48 | **−30,45%** |
| Beli sekali 365 hari lalu (US$109.608,01) | US$3.650 | US$2.560,08 | **−29,86%** |
| DCA US$10/hari, 365 hari terakhir | US$3.650 | US$3.708,30 | **+1,60%** |
| DCA US$10/hari mulai hari puncak (390 hari) | US$3.900 | US$3.879,14 | **−0,53%** |

DCA (dollar-cost averaging) artinya membeli nominal yang sama secara berkala tanpa melihat harga. Dua baris pertama beli sekali di satu titik; dua baris terakhir menyebar pembelian.

Dalam rupiah (kurs Rp18.140/US$, sama dengan asumsi Liputan6):

- Beli sekali di puncak: modal **Rp66.211.000** → hari ini **Rp46.048.027** (−Rp20,16 juta).
- DCA harian 365 hari: modal **Rp66.211.000** → **Rp67.268.562** (+Rp1.057.562).
- DCA harian mulai hari puncak: modal **Rp70.746.000** → **Rp70.367.600** (−Rp378.400).

Asetnya identik. Periode waktunya nyaris identik. Bedanya 30 poin persen.

## 🎯 Kenapa bedanya besar? Karena harga rata-rata, bukan ramalan

Yang menentukan hasil bukan harga terakhir, tapi **harga rata-rata koin yang kamu pegang**.

- DCA 365 hari: modal US$3.650 ÷ 0,04823597 BTC = harga rata-rata **US$75.669,67**.
- Beli sekali 365 hari lalu: **US$109.608,01** — 46,08% lebih mahal.
- DCA dari hari puncak: rata-rata **US$77.291,64**, padahal harga saat mulai **US$124.658,54** — 61,28% lebih mahal kalau beli sekali.

Mekanismenya sederhana: nominal tetap berarti saat harga murah kamu dapat koin lebih banyak, jadi rata-rata tertarik ke bawah. Rata-rata harmonis selalu lebih kecil atau sama dengan rata-rata aritmetika. Tidak ada timing, tidak ada keberanian, cuma pembagian pembelian.

## ⚠️ Empat hal yang sering luput

1. **DCA bukan mesin uang.** Dalam 365 hari terakhir: 174 hari naik, 190 hari turun, volatilitas tahunan **44,06%**, hari terburuk **−14,02%**. Saldo Rp10 juta bisa jadi Rp8,6 juta dalam sehari.
2. **"Turun 38%" bukan berarti "butuh naik 38%" untuk balik modal.** Pembeli di puncak butuh kenaikan **+62,15%** hanya untuk impas. Ini yang membuat banyak orang menyerah tepat di titik terburuk.
3. **Fee bukan penyebab selisih.** Fee 0,1% per pembelian di 365 transaksi = 0,1% dari total modal (US$3,65 atau sekitar Rp66.200). Selisih DCA vs beli sekali 29,9 poin persen — lebih dari 300 kali lipat fee. Kalau ada yang bilang "DCA kalah karena fee", hitungannya salah.
4. **Dolar bukan rupiah.** Semua angka memakai kurs 18.140. Kalau rupiah melemah 5%, hasil rupiah-mu berubah walau harga bitcoin tidak bergerak sama sekali.

Dan satu catatan jujur: DCA 365 hari yang cuma **+1,60%** itu kalah dari deposito. Metode ini menurunkan risiko waktu masuk, bukan menjamin untung.

## ✅ Ulangi hitungannya sendiri dalam 5 menit

Tanpa API key, tanpa akun:

```bash
curl -s "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=730"
```

Setiap baris berisi `[openTime, open, high, low, close, volume, ...]` — kolom ke-5 (`close`) yang dipakai. Tiga rumusnya: (a) drawdown = close ÷ puncak − 1; (b) DCA = jumlah dari (nominal ÷ close) untuk semua hari; (c) nilai akhir = total koin × close terakhir.

Kalau hasilmu beda tipis dengan artikel ini, wajar: candle hari berjalan masih bergerak.

## Kesimpulan

Koreksi hari ini tidak mengubah apa pun soal metode. Selisih 30 poin antara beli sekali dan DCA lahir dari satu keputusan: apakah kamu menaruh seluruh uang di satu titik waktu, atau menyebarnya. Kalau kamu tipe yang panik saat melihat −14% sehari, DCA bukan strategi "yang aman" — tapi setidaknya strategi itu tidak menuntut kamu benar soal waktu.

Baca juga: [Bitcoin 32% di bawah puncak: giliran altcoin, ETF, dan RWA](/posts/bitcoin-32-persen-bawah-puncak-altcoin-etf-rwa/), [peta likuidasi bitcoin Oktober 2026](/posts/peta-likuidasi-bitcoin-oktober-2026/), dan [pajak kripto 0,21% vs 1%](/posts/pajak-kripto-021-vs-1-persen/).

— Chokdi 🐷 · Content Studio · 2026
