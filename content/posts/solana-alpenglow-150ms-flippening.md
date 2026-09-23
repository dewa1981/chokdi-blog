---
title: "Solana Alpenglow Masuk Testnet: Finality 13 Detik Jadi 0,15 Detik, Lanjut Tantang Ethereum"
date: 2026-09-24T00:50:00+07:00
draft: false
tags: ["Crypto", "Solana", "Alpenglow", "Ethereum", "DeFi", "On-Chain"]
---

Dua berita besar soal **Solana (SOL)** datang barengan minggu ini: upgrade konsensus **Alpenglow** resmi masuk public testnet, dan co-founder Multicoin Capital, Kyle Samani, terang-terangan bilang **Solana bakal menyalip Ethereum di siklus ini**. Buat kamu yang ngikutin on-chain, ini dua hal yang wajib dicatat — satu soal teknologi, satu soal arah modal.

## ⚡ Alpenglow: Finality dari 12,8 Detik ke 150 Milidetik

Angka paling gila dari upgrade ini: waktu transaksi jadi **tidak bisa dibatalkan (finality)** dipangkas dari sekitar **12,8 detik** jadi **0,15 detik** — hampir **85x lebih cepat**.

Kenapa finality penting? Karena itu momen penentu buat semua orang:

- **Exchange** nunggu finality sebelum kredit deposit kamu
- **Bridge** nunggu sebelum melepas dana di chain lain
- **Merchant** butuh itu buat memastikan pembayaran gak bisa ditarik balik

Kalau finality cuma 150 milidetik, setoran dan pembayaran bisa dianggap **final hampir instan**. Ini yang bikin Solana makin masuk akal buat pembayaran sehari-hari, bukan cuma buat trading.

### Yang berubah di dapur: TowerBFT → Votor

Solana sekarang pakai **TowerBFT** buat konsensus — validator nyatet vote mereka on-chain dan harus numpuk vote di 32 slot sebelum satu blok jadi final. Itu sumber utama kelambatan.

Alpenglow ganti sistem itu dengan **Votor**: validator kirim vote **langsung antar validator**, dan blok bisa final setelah cuma **satu atau dua ronde**. Gak ada lagi rantai vote on-chain yang panjang.

Yang penting buat pengguna: **gak perlu ganti wallet atau cara kirim dana**. Aplikasi tetap jalan seperti biasa — yang berubah cuma bagian belakangnya.

## 📅 Tanggal Penting: 21 dan 28 September

Ini bagian yang paling sering salah dikutip di media. Urutan resminya begini (dari jadwal rilis **Agave 4.3** yang di-maintain Anza):

- **8 September** — panggilan volunteer buat pindah 10% stake ke v4.3
- **14 September** — panggilan yang sama buat 25% stake
- **21 September** — rekomendasi umum ke semua validator mainnet buat pindah ke v4.3
- **28 September** — **start feature activation** di mainnet-beta

Catatan krusial: **28 September itu "mulai menyalakan", bukan "Alpenglow resmi live hari itu"**. Aktivasi Solana lewat **feature gate** yang baru aktif kalau cukup banyak stake sudah mendukung, dan eksekusinya nunggu **batas epoch** (1 epoch = 432.000 slot, sekitar 38 jam). Jadi prosesnya bertahap, bukan saklar on/off.

Satu lagi: validator yang ikut testnet **wajib pakai Agave 4.3**, dan **Firedancer serta Frankendancer belum support** uji Alpenglow. Artinya migrasi pertama ini 100% lewat Agave — sesuatu yang sebaiknya diwaspadai dari sisi ketahanan klien.

## 🧑💻 Buat Kamu yang Punya SOL: Gak Perlu Panik

Ini bagian praktisnya:

- **SOL kamu di exchange atau di wallet sendiri (unstaked)** → gak ada yang perlu dilakukan. Nol aksi.
- **Kamu delegate sendiri ke validator** → cek validator kamu sudah pakai Agave 4.3 atau belum. Ini yang jadi tugasmu.
- **Cara ngecek**: lihat **versi klien** yang dilaporkan, **status**, dan **skip rate** validator. Data itu jauh lebih berguna daripada angka APY di landing page mana pun.
- **Pencatatan pajak:** upgrade konsensus gak mengubah perlakuan pajak reward staking. Tetap dihitung saat masuk, tetap pakai harga saat itu.

Kalau validator kamu masih di Agave 4.2, gak berarti langsung rugi — tapi kamu bakal tertinggal dari sisi performa begitu activation jalan.

## 🐂 Sisi Lain: "Solana Bakal Salip Ethereum"

Di hari yang hampir sama, **Kyle Samani** (co-founder Multicoin Capital) bilang ke Cointelegraph kalau **Solana akan flip Ethereum di siklus pasar ini**. Argumennya tajam dan sengaja provokatif:

> "Hari ini, hampir gak ada yang benar-benar pakai Ethereum."

Samani bilang Ethereum cuma masih memimpin karena **stablecoin**, dan karena stablecoin yang dijaminkan pakai ETH. Soal value accrual, dia menyebut Ethereum sebagai aset **$300–400 miliar dengan akumulasi nilai yang dipertanyakan, "kalau ada"** — dan menurut dia gak tumbuh sama sekali.

Yang bikin klaim ini menarik: **angka on-chain sebagian mendukungnya**.

- Solana menghasilkan sekitar **$23 juta fee dalam 30 hari terakhir**, sementara Ethereum sekitar **$12,6 juta** — Solana menang di weekly dan monthly fees.
- Solana juga sudah **memimpin di fee 30 hari** meski market cap-nya kurang dari seperlima Ethereum.

Tapi ada catatan penting yang sering dilewatkan:

- SOL perlu naik sekitar **5x** dari kapitalisasi ~$58 miliar buat ngalahin market cap ETH yang ~$293 miliar. Itu bukan jarak dekat.
- Selama sebulan terakhir **ETH naik 30%, SOL naik 34%** — beda tipis, dan SOL naik dari basis yang lebih rendah.
- Dalam setahun terakhir SOL turun **59%** vs ETH **45%** (TradingView).
- SOL masih **underperform** secara relatif: SOL vs BTC **-25,3%**, SOL vs ETH **-16,4%**.

Jadi menang di fee itu nyata, tapi "flippening" tetap proyeksi, bukan fakta.

## 📊 Yang Bikin Bull Case Makin Kuat

Selain Alpenglow, ada beberapa pijakan yang sudah kelihatan:

- **Block time turun ke 250ms** lewat SIMD-0525 (tahap ketiga, target akhir 200ms) — blok diproduksi ~17% lebih sering.
- **Transaction V1** live 15 September: ukuran transaksi maksimum naik dari 1.232 byte ke **4.096 byte** (3,3x) — bisa bungkus operasi kompleks seperti multi-sig atau ZK proof dalam satu transaksi.
- **Rent reduction bertahap**: dari 6.960 jadi 696 lamports per byte, potong **90%**. Ini nurunin modal buat developer yang ngelola banyak akun user (gaming, sosial).
- **Disinflasi dipercepat** (SGP-0002, Agustus): laju disinflasi tahunan naik dari 15% ke 30%, bikin inflasi terminal 1,5% datang lebih cepat — dari 2032 ke paruh pertama 2029.

Kombinasi "makin cepat + makin murah + makin langka" itu paket yang jarang muncul bersamaan.

## 🎯 Kesimpulan

Alpenglow bukan sekadar angka marketing. Finality 150 milidetik mengubah posisi Solana dari "chain cepat buat trading" jadi kandidat serius buat **pembayaran dan settlement** — dan itu justru wilayah yang selama ini jadi alasan orang bertahan di Ethereum.

Tapi jangan terjebak narasi "flippening" tanpa lihat angka. Menang di fee bulanan itu fakta; menyalip market cap butuh SOL naik 5x, dan relative performance-nya masih negatif terhadap BTC maupun ETH. Yang paling aman dilakukan sekarang: **cek validator kamu** (kalau delegasi sendiri), dan pantau tanggal **28 September** — bukan sebagai hari peluncuran, tapi sebagai hari mulai menyalanya.

Kalau kamu staking SOL sendiri, kamu udah cek versi Agave validator kamu belum? Tulis di komentar — pengalaman lapangan lebih berguna daripada rilis berita.

Sumber: [CoinDesk](https://www.coindesk.com/tech/2026/09/23/solana-starts-testing-upgrade-that-could-cut-finality-from-12-8-seconds-to-150-milliseconds), [Cointelegraph via TradingView](https://www.tradingview.com/news/cointelegraph:58ec9c1ba094b:0-kyle-samani-predicts-sol-flippening-claims-no-one-uses-eth/), [CryptoTicker](https://cryptoticker.io/en/solana-alpenglow-activation-date-validator-check/), [CoinMarketCap AI](https://coinmarketcap.com/cmc-ai/solana/latest-updates/)

Baca juga: [Solana ETF Tembus $1 Miliar](/posts/solana-etf-tembus-1-miliar-2026/) dan [EIP-8361: Ethereum Bakar Reward Validator](/posts/ethereum-eip-8361-bakar-reward-validator/)

— Chokdi 🐷 · Content Studio · 2026
