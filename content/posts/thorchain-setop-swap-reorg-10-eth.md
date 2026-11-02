---
title: "Reorg 1 Blok Ethereum Bikin THORChain Setop Swap 10 Jaringan — 10 ETH Cukup Lumpuhkan Protokol"
date: 2026-11-02T16:00:00+07:00
draft: false
description: "Sabtu 31 Oktober 2026 satu blok Ethereum di-reorg, setoran 10 ETH yang sudah dikonfirmasi hilang, refund tetap dibayar, dan swap di 10 dari 13 jaringan THORChain langsung dihentikan. RUNE -18,4%."
tags: ["Crypto", "THORChain", "DeFi", "Ethereum", "On-Chain", "RUNE"]
---

Swap lintas-chain di THORChain berhenti sejak Sabtu, 31 Oktober 2026 — bukan karena FBI, bukan karena hack, tapi gara-gara bug refund yang dipicu reorg satu blok di Ethereum. Dampaknya: swap di 10 dari 13 jaringan yang tersambung dipause, termasuk Bitcoin, Ethereum, Solana, dan Tron. Token RUNE ikut tergelincir 18,4% dalam 24 jam.

Intinya: transaksi yang "sudah terkonfirmasi" belum tentu final.

## 🧩 Kronologi: dari satu blok sampai sepuluh jaringan mati

Urutannya (catatan THORChain via TechFlow, dirangkum CryptoTicker 2 November):

1. Sebuah blok Ethereum diganti (reorg) setelah terbit. Setoran 10 ETH yang sudah dikonfirmasi THORChain ikut lenyap.
2. Swap pasangan itu gagal karena kena batas harga, jadi protokol mengembalikan dananya — ini prosedur normal.
3. Masalahnya: setelah reorg, setoran yang sedang dikembalikan tadi sudah tidak ada. Hasilnya **10 ETH keluar dari vault tanpa pemasukan yang cocok**.
4. Pemeriksa solvabilitas otomatis menangkap selisihnya dan langsung menghentikan perdagangan ETH.
5. Operator node (THORNode) menyusul mempause swap di jaringan lain. Data node yang dianalisis The Block: 10 dari 13 chain berhenti.

Per Senin pagi, 2 November, sebagian sudah dibuka lagi: Avalanche, Base, XRP Ledger, dan jaringan RUNE sendiri. Bitcoin, Ethereum, dan Solana masih ditutup. Dana 10 ETH sudah dikembalikan penerimanya dan vault dinyatakan sehat — tapi jaringan tetap ditutup sampai akar masalahnya diperbaiki, karena skenario yang sama bisa diulang.

## ⛓️ Reorg itu apa, dan kenapa "confirmed" bukan "final"

Reorg (reorganisasi) adalah kondisi ketika blockchain mengganti satu atau beberapa blok yang sudah terbit dengan versi lain. Transaksi di blok lama dianggap tidak pernah terjadi sampai dimasukkan lagi ke blok baru.

Di Ethereum, reorg satu blok jarang tapi mungkin. Protokol yang mengkredit setoran setelah menunggu sebentar menanggung risiko itu sendiri — THORChain mendesain konfirmasi inbound lebih cepat daripada finalitas absolut supaya swap terasa instan.

Analogi kasir: uang kembalian sudah diserahkan, lalu struknya dibatalkan dari pusat. Uangnya sudah keluar, transaksinya tidak ada.

## 💸 10 ETH nominal receh, mekanismenya yang besar

Nilainya sekitar **$23.000** di harga ETH ±$2.307. Dibanding kerugian hack Binance yang sekitar $6,3 miliar, itu nol koma sekian persen. Lihat [kronologi hack Binance di artikel kami sebelumnya](/posts/binance-hack-6-3-miliar-terbesar-sejarah/).

Tapi yang bikin operator menutup 10 jaringan bukan nominalnya, melainkan polanya: kalau setoran terkonfirmasi bisa menguap setelah fakta, pola itu bisa diulang siapa pun yang tahu celahnya. Tim THORChain sendiri menyebut risikonya terbuka — setiap ada reorg di chain eksternal, aktor jahat bisa mengirim transaksi dengan nonce yang sama dan dibayar oleh vault.

## 🕵️ Efek samping: cucian Binance ikut macet

Ini bagian paling ironis. Pause-nya murni bug, bukan kepatuhan — tapi justru mengganggu aliran dana hasil hack.

- Analis SomaXBT mencatat sekitar **$242 juta** dicuci lewat Tron dalam dua hari; **$194 juta** keluar lewat bridge dan swap service.
- Rinciannya: Relay $48 juta, THORChain $44 juta, Chainflip $32,1 juta, Symbiosis $16 juta.
- Sebelum pause, THORChain sempat membayar **17.019 ETH ke 170 alamat** dan **53,25 BTC ke 20 alamat**.
- Chainalysis menyebut pause ini ikut menahan pelaku karena rute BTC/ETH mereka tertutup, sama seperti "[koin yang tidak bisa ditarik dari kustodi](/posts/bitcoin-tak-bisa-ditarik-kustodi-exchange/)".

FBI bersama Secret Service dan IRS-CI menerbitkan 608 alamat Ethereum, 19 Bitcoin, dan 1 Solana yang diatribusikan ke kelompok TraderTraitor (Korea Utara). Elliptic menghitung $6,43 miliar dicuri, **$2,85 miliar (44%)** sudah dibekukan atau disita — dan 94% dari yang dibekukan adalah stablecoin yang bisa dibekukan penerbitnya. Di Bitcoin tidak ada yang bisa membekukan: **18.270 BTC** masih diam di 19 alamat itu.

## 📉 RUNE: harga yang dibayar untuk lubang mekanisme

Senin pagi RUNE diperdagangkan ±**$0,507**, turun **18,4%** dalam 24 jam (rentang $0,498–$0,649) dan sekitar 32% dalam 30 hari. Di Pintu, RUNE memimpin daftar loser harian dengan -18,73% ke Rp9.206. Dari all-time high $20,87 (Mei 2021), harganya kini lebih dari 97% di bawah.

Wajar: selama jaringan besar ditutup, fee swap yang membiayai pool dan operator ikut berhenti.

## 🧰 Yang perlu dicek sebelum swap lintas-chain

- **Cek rute di dompet.** Banyak wallet memakai THORChain di belakang layar tanpa menyebut namanya. Kalau rutenya lewat jaringan yang ditutup, swap-nya nyangkut.
- **Jangan kirim besar-besaran ke jaringan berstatus paused.** Tunggu pengumuman resmi THORChain, jangan mengandalkan screencap grup.
- **Pahami asumsi finalitas.** Exchange besar menunggu lebih banyak konfirmasi daripada DEX. Itu bukan lambat, itu murah hati.
- **Bedakan bug sekali jalan vs cacat desain.** Koreksi harga token protokol baru jadi peluang kalau akar masalahnya benar-benar ditutup.

## ✅ Kesimpulan

Yang menjatuhkan swap di sepuluh jaringan bukan hack dan bukan regulator, tapi 10 ETH yang dikembalikan ke setoran yang sudah tidak ada. Satu reorg blok di Ethereum cukup membuktikan bahwa di jembatan lintas-chain, asumsi "sudah masuk" adalah risiko — bukan jaminan.

Kalau kamu rutin pindah aset antar-chain, cek dulu rutenya. Dan jangan panik lihat RUNE merah: yang sedang rusak mekanismenya, bukan cuma harganya.

*Sumber: Pintu News (2 Nov 2026), CryptoTicker (2 Nov 2026), crypto.news (2 Nov 2026), The Block via CryptoTicker.*

— Chokdi 🐷 · Content Studio · 2026
