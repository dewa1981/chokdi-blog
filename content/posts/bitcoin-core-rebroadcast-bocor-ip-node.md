---
title: "Celah Bitcoin Core: Bayar Rp3.300–6.200, Alamat Wallet Bisa Nyambung ke IP Node-mu"
description: "Kontributor Bitcoin Core Abubakar Sadiq Ismail menunjukkan pembayaran debu di bawah Rp6.500 bisa menghubungkan alamat wallet ke IP node yang memantaunya. Simulasi 30/30 berhasil, tambalan PR #36482 belum rilis."
date: 2026-11-27T17:20:00+07:00
draft: false
tags: ["Bitcoin", "Privasi", "Bitcoin Core", "Keamanan", "Node"]
---

Tanggal 25 November 2026, kontributor Bitcoin Core **Abubakar Sadiq Ismail** memposting temuan di forum Delving Bitcoin. Judulnya kering — *Exploiting Wallet Rebroadcast to Link Addresses to Node IPs and More* — tapi isinya sederhana dan tidak nyaman: sebuah pembayaran senilai **US$0,18–0,34** cukup untuk menghubungkan alamat Bitcoin ke IP komputer yang memantaunya.

Ini bukan soal dana hilang. Ini soal privasi yang kita sangka sudah aman justru karena menjalankan node sendiri.

## 🧩 Celahnya ada di fitur yang tak pernah kita pikirkan

Bitcoin Core punya kebiasaan: transaksi yang belum dikonfirmasi akan **diumumkan ulang** ke jaringan setelah 12–36 jam. Fitur ini masuk akal — kalau transaksi mandek, wallet membantu menyiarkannya lagi.

Masalahnya, pengumuman ulang itu **sinyal deterministik**. Berbeda dari serangan LinkingLion yang sifatnya probabilistik dan berisik, rebroadcast selalu terjadi dengan pola yang sama.

Ismail menulis: *"The rebroadcast is a deterministic signal, and in a simulation, I was able to link the address to the node whose wallet tracks it 100% of the time."*

Cara kerjanya:

1. Penyerang tahu satu alamat yang pernah dipakai.
2. Dia mengirim pembayaran kecil di ambang *dust* dengan fee minimum ke alamat itu. Karena fee-nya terlalu kecil, transaksi tidak cepat dikonfirmasi.
3. Wallet target menyimpan transaksi itu, lalu mengumumkan ulang setelah timer 12–36 jam habis.
4. Penyerang menyambungkan peer pengintai baru ke tiap kandidat node. Node yang mengumumkan transaksi itu adalah node yang wallet-nya memantau alamat tersebut — berikut IP-nya.

## 💸 Hitungan biayanya

Biaya satu pembayaran uji, tergantung jenis output:

- **P2WPKH**: 309 satoshi ≈ **US$0,18**
- **P2TR**: 346 satoshi ≈ **US$0,20**
- **P2PKH**: 569 satoshi ≈ **US$0,34**

Dengan BTC sekitar US$59.000 saat riset (25 November) dan kurs Rp18.350 per dolar, satu percobaan setara **Rp3.300–Rp6.250**. Artinya penyerang bisa mencoba ke banyak alamat sekaligus tanpa memikirkan biaya.

## 🎯 Siapa yang kena

Yang paling terpapar adalah wallet bawaan Bitcoin Core, termasuk **watch-only wallet** — wallet yang cuma memantau alamat tanpa memegang kunci. Software lain yang menitipkan alamatnya ke wallet Core ikut kena: Sparrow (mode Core), Specter Desktop, Liana (backend bitcoind), Fully Noded, Gordian Wallet, JoinMarket/Jam, Lily Wallet v1.0.7, Electrum Personal Server, Caravan, bwt, dan Eclair.

Nuansa penting: karena watch-only ikut kena, node yang teridentifikasi belum tentu pemilik dananya. Bisa saja itu server exchange, layanan pemantau, atau node milik pihak lain. Tapi untuk analisis rantai, asosiasi alamat ke node tetap berharga.

## 🧪 Simulasi 30 dari 30, bukan uji mainnet

Ismail menguji di jaringan **regtest** dengan node Bitcoin Core standar dalam Docker. Lima target, enam percobaan, total 30 atribusi: pengintai menautkan alamat ke node yang benar **30 dari 30 kali**.

Dua catatan jujur yang dia tulis sendiri: ini simulasi di jaringan terisolasi, bukan pengukuran di mainnet, dan sampai riset terbit belum ada laporan eksploitasi liar. Angka 100% berlaku untuk skenario yang dia tentukan, bukan semua konfigurasi.

## 🧅 Tor saja tidak menutup semuanya

Banyak yang mengira cukup menjalankan node di belakang Tor. Tidak selalu.

- Kalau transaksi dikirim dengan `-privatebroadcast` lalu mandek, pengumuman ulang jatuh kembali ke jalur normal dan bocor ke semua peer.
- Node yang jalan di Tor **tapi masih punya peer clearnet** akan mengumumkan ulang lewat clearnet juga, dan IP clearnet-nya ikut terlihat.
- Yang aman dari sisi clearnet: `-onlynet=onion` atau `-onlynet=i2p`. Konsekuensinya, alamat tetap terhubung ke identitas onion node — bukan anonim sempurna.

## 🛠️ Yang bisa dilakukan sekarang

1. **`-walletbroadcast=0`** mematikan seluruh broadcast dari wallet. Efek sampingnya, transaksi keluar juga tidak diumumkan otomatis — kamu harus menyiarkannya manual dengan `sendrawtransaction`.
2. **`-onlynet=onion`** kalau node memang didedikasikan untuk privasi.
3. **Pisahkan node pemantau dari wallet panas.** Jangan impor semua alamat ke Core kalau tidak perlu.
4. **Jangan panik.** Ini kebocoran privasi, bukan pencurian dana. IP bukan identitas.
5. **Tunggu tambalan resmi.** PR **#36482** (hanya mengumumkan ulang transaksi yang baru masuk mempool) belum dirilis. Kontributor Martin Zumsande menilai PR itu cuma menaikkan biaya serangan sedikit, dan mengusulkan rebroadcast untuk transaksi masuk dibuat *opt-in* lewat #36398 dan #36481. Ismail setuju dengan catatan itu.

## 🇮🇩 Kenapa ini relevan buat yang self-custody di Indonesia

Kalau node-mu jalan di VPS dengan IP publik statis — pola yang umum di sini karena rumah pakai NAT — maka asosiasi alamat ke IP ikut menunjuk penyedia dan kota. Untuk dompet dengan saldo besar, itu informasi yang cukup untuk phishing yang meyakinkan atau penargetan.

Kabar baiknya: pengguna exchange dan aplikasi kustodian tidak terkena langsung, karena mereka tidak menjalankan wallet Core. Yang perlu waspada adalah yang benar-benar menyimpan sendiri dan mengoperasikan node.

## Kesimpulan

Bitcoin Core 32.1 (27 Oktober 2026) sudah menambal masalah privasi lain di fitur `-privatebroadcast` eksperimental. Temuan Ismail menunjukkan masih ada jalur yang terbuka, dan jalurnya murah: di bawah satu dolar per percobaan.

Sampai PR #36482 masuk rilis stabil, pilihannya cuma dua — matikan wallet broadcast dan siarkan transaksi manual, atau jalankan node hanya lewat onion/I2P. Pelan itu aman, bukan lambat.

**Baca juga:** [AI Temukan Bug Bitcoin Core: Cukup Ulang 1 ID Transaksi 50.000 Kali, Node Berhenti Kerja](https://chokdi.ano99.com/posts/ai-temukan-bug-bitcoin-core-node-macet-50-ribu-id/) · [Nonce Dipakai Dua Kali, Kunci Dompet Bitcoin Bocor — Bot Datang dalam Hitungan Detik](https://chokdi.ano99.com/posts/nonce-dipakai-dua-kali-kunci-dompet-bitcoin-bocor/) · [Sejarah Baru Bitcoin: Transaksi Quantum-Resistant Pertama Sukses di Mainnet!](https://chokdi.ano99.com/posts/bitcoin-transaksi-quantum-resistant-pertama/)

— Chokdi 🐷 · Content Studio · 2026
