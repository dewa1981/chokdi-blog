---
title: "Chainflip Kehilangan US$12 Juta dengan Signature yang Sah: Kuncinya Bocor, Bukan Kodenya"
date: 2026-11-26T09:14:47+07:00
draft: false
tags: ["Crypto", "Keamanan", "DeFi", "On-Chain", "Chainflip", "Bridge"]
---

Pada 21 November 2026 pukul 07:10:59 UTC, satu transaksi mengosongkan seluruh Ethereum Vault milik Chainflip — **520,2 ETH, 3,25 juta USDC, dan 758.141 USDT**, sekitar **US$4,86 juta** saat itu. Yang membuat kasus ini layak dibaca ulang bukan angka kerugiannya, tapi satu detail: transaksi itu membawa **signature yang sah** dari kunci bersama para validator. Kontraknya tidak salah. Kuncinya yang bermasalah.

Total kerugian seluruh vault akhirnya membengkak ke sekitar **US$12 juta** setelah Chainflip merinci 122,86137042 BTC, 520,2243399 ETH, 3.249.631,41 USDC, dan 758.141,33 USDT.

## 🔑 Apa yang sebenarnya terjadi

Investigasi on-chain [Bitquery](https://bitquery.io/investigations/chainflip-hack) merekonstruksi urutannya hampir per menit:

- **07:09** — dompet penyerang menerima ETH pertamanya, dikirim dari Tornado Cash. Dompet itu belum punya riwayat transaksi lain.
- **07:10:59** — transaksi masuk ke `Vault.transferBatch` membawa **aggregate Schnorr signature** yang diterima kontrak. Vault membayar.
- **07:14** — stablecoin ditukar ke ETH lewat Uniswap.
- **07:19** — **2.909 ETH** sudah masuk Tornado Cash dalam **38 deposit selama 48 detik**.
- **08:53** — Chainflip mengganti kunci signing Ethereum, 1 jam 42 menit setelah drain, dan 13 jam lebih awal dari jadwal rotasi tiga hariannya.
- Setelah itu: **nol signature**. Padahal sehari sebelumnya vault menerima sekitar 46 signature per jam.

## ❓ Kalau signature-nya sah, salahnya di mana

Desain Chainflip sebenarnya rapi di atas kertas: hingga **150 validator**, dan sebuah pembayaran butuh **100 dari 150** tanda tangan. Tidak ada satu pihak yang bisa memindahkan dana sendirian. Tapi skema ambang seperti ini hanya kuat selama *mesin di sekitar kuncinya* juga kuat.

Bitquery menemukan satu anomali yang menentukan: dari **299.677 signature** yang diterima vault sejak 2023, hanya satu yang **memutus urutan nonce** — yaitu signature drain ini. Nonce di Chainflip dibagikan dari hitungan berjalan, jadi signature lama tidak bisa diputar ulang. Kalau urutannya putus, artinya signature itu dibuat **di luar proses normal jaringan**, bukan lewat jalur yang seharusnya.

Sampai sekarang Chainflip **belum mengumumkan penyebabnya**. Tidak ada bukti kontraknya bocor. Yang mengeras justru kecurigaan ke sisi kunci: share kunci yang dicuri, server signing yang diambil alih, atau jalur lain.

## 🕵️ Jejak persiapan 10 hari sebelumnya

Yang paling mengganggu dari kasus ini adalah betapa panjang persiapannya:

- **11 November** — dana penyerang lewat Tornado Cash.
- **20 November** — membeli token asli protokol, **FLIP**, lalu mendaftarkan akun validator pada server tertentu.
- **21 November** — drain.

Artinya penyerang tidak menebak. Dia masuk ke dalam sistem, menjadi bagian dari himpunan penandatangan, lalu menunggu momen. Chainflip menyebut sudah mengidentifikasi mekanisme bocornya kunci dan sudah memasang pengaman, serta mengumpulkan metadata layanan yang dipakai penyerang untuk membantu penegak hukum.

Tawaran mereka: penyerang boleh menyimpan **10%** kalau **90%** dikembalikan sebelum 23 November 18:38 UTC. Lewat tenggat itu, jalurnya hukum. Harga FLIP sendiri jatuh sekitar **30%** (CoinDesk) hingga **42,9%** menurut agregator, dan protokol masuk *safe mode* penuh: deposit, penarikan, swap, dan quoting dimatikan.

## 🛡️ Tiga hal yang bisa dicek di sistem pembayaran sendiri

Saya menjalankan sistem pembayaran otomatis berbasis USDT, dan kasus ini menampar di tempat yang sama: **valid bukan berarti benar**.

1. **Batas per signature, bukan cuma batas harian.** Skema 100-dari-150 terdengar aman sampai satu signature bisa memindahkan seluruh isi vault. Kalau satu tanda tangan maksimal hanya bisa membawa 5% saldo, kerugian terburuk sudah dibatasi desain, bukan dideteksi setelah kejadian.
2. **Alarm untuk dompet yang "baru lahir".** Dompet penyerang berumur satu menit dan dananya dari mixer, lalu langsung memicu pembayaran besar. Aturan sederhana — tolak atau tahan pembayaran ke alamat dengan riwayat < 1 jam atau sumber dana mixer — akan menghentikan langkah terakhirnya.
3. **Pantau urutan nonce, bukan cuma nominal.** Yang membongkar kasus ini adalah hitungan yang putus, bukan jumlah transfer. Sistem pembayaran yang menyimpan nonce berurutan bisa memicu alarm saat ada nomor yang melompat atau dipakai dua kali — ini juga akar insiden "WD dobel" yang sering kita bahas.

## ⚠️ Angka yang masih bertengkar

Jangan menelan satu angka saja. Kerugian Ethereum vault **US$4,86 juta**, tapi rincian resmi Chainflip memasukkan 122,86 BTC sehingga total mendekati **US$12 juta** — dan kedua angka ini belum direkonsiliasi publik. Penurunan FLIP dilaporkan 30% sampai 42,9% tergantung sumber. Yang belum ada: sebab pasti bocornya kunci, identitas penyerang, dan rencana pengembalian dana pengguna.

## 🎯 Kesimpulan

Chainflip bukan korban kode yang salah tulis. Ini kasus **kunci yang sah dipakai pihak yang salah**, dengan persiapan sepuluh hari dan pelarian dana dalam sembilan menit. Audit kontrak tidak akan menangkap kelas kegagalan ini, karena yang gagal adalah lapisan di atas kontrak: proses signing, rotasi kunci, dan batas nilai yang boleh dibawa satu tanda tangan.

Kalau kamu memegang vault, bridge, atau sistem pembayaran otomatis: batasi nilai per signature, alarm untuk dompet baru, dan anggap setiap kunci yang dipakai bersama sebagai titik tunggal kegagalan sampai terbukti sebaliknya.

Menurut kamu, mana yang lebih mendesak dipasang dulu di protokol kecil: batas per transaksi atau rotasi kunci lebih sering? Tulis di komentar.

**Baca juga:** [Reorg 1 Blok Ethereum Bikin THORChain Setop Swap 10 Jaringan — 10 ETH Cukup Lumpuhkan Protokol](https://chokdi.ano99.com/posts/thorchain-setop-swap-reorg-10-eth/) · [Rotasi ETF Crypto 11 September: Bitcoin Keluar $13 Juta, Ethereum Masuk $216 Juta](https://chokdi.ano99.com/posts/etf-crypto-rotasi-bitcoin-ke-ethereum-11-september-2026/) · [Arbitrum Bekukan $30 Juta Dana Hack Binance Tanpa Private Key — Kok Bisa?](https://chokdi.ano99.com/posts/arbitrum-bekukan-30-juta-dana-hack-binance-tanpa-private-key/)

— Chokdi 🐷 · Content Studio · 2026
