---
title: "Glamsterdam Sepolia 6 Oktober 2026 — Gas Transfer ETH Turun 71%"
date: 2026-09-24T09:15:00+07:00
draft: false
tags: ["Crypto", "Ethereum", "Glamsterdam", "ePBS", "Layer 1"]
---

Kalau kamu pernah merasa biaya kirim ETH itu mahal padahal cuma mindahin saldo, angka barunya bakal bikin kamu senyum. Ethereum sudah menetapkan jadwal uji coba Glamsterdam ke testnet Sepolia pada **6 Oktober 2026** — dan di dalam paket upgrade itu ada proposal EIP-2780 yang memangkas biaya dasar transfer ETH biasa sampai **71% lebih murah**.

Ini bukan janji marketing. Ini angka dari halaman roadmap resmi ethereum.org, dan tanggalnya sudah diputuskan dalam rapat All Core Developers Consensus pada 17 September 2026.

## 🎯 Apa Itu Glamsterdam Sebenarnya?

Glamsterdam adalah gabungan dua nama: **Amsterdam** (komponen execution layer, diambil dari kota tuan rumah Devconnect) dan **Gloas** (komponen consensus layer, diambil dari nama bintang). Jadi satu upgrade, dua lapisan sekaligus.

Posisinya jelas: lanjutan dari Fusaka yang sudah live Desember 2025, dan dia mengejar dua target besar di roadmap Ethereum — **"Scale L1"** dan **"Scale Blobs"**.

Tiga pilar utamanya:

- **Parallelization** — transaksi diproses bersamaan, bukan satu-satu
- **Kapasitas lebih besar** — blok bisa membawa data jauh lebih banyak
- **Anti-bloat database** — biaya storage dibikin jujur sesuai beban nyata

## 🚀 Fitur Utama #1: ePBS (EIP-7732)

Ini headliner-nya. Enshrined Proposer-Builder Separation memindahkan serah-terima antara *proposer* (yang memilih blok konsensus) dan *builder* (yang merakit payload eksekusi) langsung ke dalam protokol.

Kenapa ini penting buat kamu yang cuma pakai ETH buat transaksi?

- Relay pihak ketiga seperti MEV-Boost **tidak lagi jadi jalur wajib** — trust assumption-nya hilang dari persamaan
- **Jendela propagasi data melebar dari ~2 detik jadi ~9 detik** — ini yang membuka pintu ke throughput jauh lebih tinggi
- Ada **Payload Timeliness Committee (PTC)** plus logika dual-deadline, jadi validator bisa meng-attest blok konsensus dan payload eksekusi secara terpisah

Analoginya: dulu kopi harus selesai di-racik dalam 2 detik sebelum kurir datang. Sekarang kurirnya sabar nunggu 9 detik — jadi barista bisa bikin pesanan lebih banyak tanpa ngos-ngosan.

## 📋 Fitur Utama #2: Block-Level Access Lists (EIP-7928)

BALs memberi validator **peta di depan** tentang transaksi mana menyentuh data mana. Efeknya berantai:

- Validator bisa baca disk secara paralel, bukan antre satu-satu
- Node bisa sync dengan lebih cepat — bahkan lewat *executionless sync*, baca hasil akhirnya saja tanpa replay semua transaksi
- Data yang dibutuhkan sudah ter-*pre-load*, jadi tidak ada lagi tebak-tebakan saat validasi

Ada juga **eth/71 (EIP-8159)** alias Block Access List Exchange — jalur networking supaya node benar-benar bisa saling bertukar daftar akses itu.

## 💸 Fitur Utama #3: Transfer ETH Jadi Jauh Lebih Murah (EIP-2780)

Ini bagian yang paling terasa buat pengguna biasa.

Hari ini, **semua transaksi Ethereum bayar gas dasar yang flat** — entah itu cuma kirim ETH, entah itu deploy kontrak ribet. EIP-2780 memecah biaya itu supaya hanya mencerminkan kerja nyata: verifikasi tanda tangan digital dan update saldo.

Hasilnya? **Transfer ETH antar akun yang sudah ada bisa sampai 71% lebih murah.** Buat yang pakai Ethereum buat pembayaran harian, ini perubahan besar — bukan sekadar penghematan receh.

## 🗄️ Soal Database: EIP-8037 & EIP-8038

Ethereum terus tumbuh, dan setiap akun, token, atau NFT baru = data permanen yang harus disimpan semua node selamanya. Dua EIP ini merapikan itu:

| EIP | Yang Diubah | Target |
|---|---|---|
| EIP-8037 | Biaya pembuatan state naik & dipisah ke *reservoir* | Pertumbuhan DB ~120 GiB/tahun |
| EIP-8038 | Biaya akses state naik sesuai beban compute nyata | Anti-DoS + dorong app efisien |

Menariknya, EIP-8037 memakai **model reservoir** — biaya komputasi dan biaya penyimpanan permanen dipisah. Artinya developer bisa deploy kontrak yang jauh lebih besar dan kompleks, asal dananya cukup buat "mengisi reservoir" data. Sebelumnya, ukuran data aplikasi bisa mentok-menghabiskan gas limit.

Kenapa developer sendiri yang diuntungkan? Karena pengembang sekarang **calibrating di reference block gas limit 150 juta** untuk menghitung harga state yang akurat — menuju lantai **200 juta gas limit** yang akan dibuka Glamsterdam.

## 🛡️ Ketahanan Jaringan & Tools Baru untuk Developer

Glamsterdam juga merapikan hal-hal yang jarang dibahas tapi penting:

- **EIP-8045** — validator yang sudah di-slash tidak bisa dipilih lagi jadi proposer, jadi tidak ada missed slot saat kejadian mass slashing
- **EIP-7954** — batas ukuran kontrak naik dari ~24 KiB jadi **64 KiB**
- **EIP-7997** — factory predeploy universal, jadi smart contract wallet bisa punya alamat yang sama persis di semua EVM chain
- **EIP-7708** — transfer dan burn ETH sekarang memancarkan log, lebih simpel untuk accounting
- **EIP-7975 (eth/70)** — block receipt list bisa diminta bertahap, mencegah crash node saat sync

## ⚠️ Yang WAJIB Kamu Tahu: Ini Testnet, Bukan Mainnet

Ini bagian yang paling sering bikin orang salah paham, dan aku mau jujur di sini.

**6 Oktober 2026 itu fork Sepolia — testnet. Bukan tanggal launch mainnet.**

Roadmap resmi Ethereum masih menulis mainnet di **Q4 2026**, dengan catatan tegas: *"Date not yet confirmed."* Meta-EIP yang mendefinisikan isi upgrade pun masih berstatus draft, dan scope masih bisa berubah sebelum mainnet.

Jadi baca ini sebagai kerangka kerja, bukan hitungan mundur. Devnet memunculkan bug → proposal naik ke testnet publik → baru menyentuh ETH sungguhan. Untuk trader yang mencari katalis jangka pendek, kesimpulan praktisnya: ritmenya nyata dan bergerak, tapi Q4 2026 tetap *window*, bukan janji.

**Dan yang paling penting:** tidak ada yang perlu kamu lakukan untuk ETH kamu. Tidak perlu convert, tidak perlu upgrade. **Siapa pun yang menyuruhmu "upgrade" ETH sedang mencoba menipumu.**

## 🧭 Apa yang Perlu Dilakukan Sekarang?

- **Kalau kamu cuma pengguna:** tidak ada. Simpan ETH kamu, waspada scam bertema upgrade.
- **Kalau kamu node operator:** siapkan update client execution *dan* consensus. ePBS mengubah cara blok dibangun, divalidasi, dan di-attest — mau tidak mau harus update.
- **Kalau kamu staker:** ikuti mailing list dan Protocol Announcements EF Blog, lalu uji di testnet sebelum mainnet aktif.
- **Kalau kamu developer:** review pemakaian gas kamu sekarang. Harga deployment kontrak dan storage bakal berubah karena EIP-8037 dan EIP-8038.

Harga ETH sendiri saat artikel ini ditulis ada di kisaran **$2.679** (turun ~2,9% dalam 24 jam), sementara BTC di **$84.154**. Pasar sedang tidak ramai, dan justru di momen seperti ini update fundamental biasanya lebih layak diperhatikan daripada grafik.

Baca juga pembahasan kami soal [harga gas Ethereum yang bisa dibayar tanpa ETH](/posts/gas-ethereum-bisa-dibayar-tanpa-eth/) dan [dampak EIP-8361 pada reward validator](/posts/ethereum-eip-8361-bakar-reward-validator/).

Kalau menurutmu EIP-2780 bakal benar-benar bikin Ethereum dipakai buat bayar sehari-hari, atau justru tetap kalah dari Solana yang lebih dulu kencang — tulis di kolom komentar. Aku penasaran.

---

*Sumber: [ethereum.org — Glamsterdam](https://ethereum.org/roadmap/glamsterdam/), [The Defiant](https://thedefiant.io/news/blockchains/ethereum-glamsterdam-final-devnet-200m-gas-limit-target), [99Bitcoins via Yahoo Tech](https://tech.yahoo.com/science/articles/sepolia-sets-stage-ethereum-glamsterdam-154810992.html), harga live Binance.*

— Chokdi 🐷 · Content Studio · 2026
