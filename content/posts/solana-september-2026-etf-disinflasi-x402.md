---
title: "Solana September 2026: ETF $1,47 Miliar, Disinflasi 30%, dan 76% Transaksi Agen AI"
date: 2026-09-25T09:35:00+07:00
draft: false
tags: ["Solana", "Crypto", "AI Agent", "ETF", "On-Chain", "2026"]
---

Solana (SOL) menutup September 2026 dengan tiga perkembangan yang datang hampir bersamaan: ETF spot AS menembus **US$1,47 miliar** akumulasi inflow, validator meloloskan **SGP-0002** yang mempercepat penurunan inflasi SOL, dan jaringan ini menangkap **76%** dari seluruh transaksi pembayaran agen AI lewat protokol x402. Tiga hal ini jarang terjadi dalam satu bulan yang sama — dan masing-masing menyentuh sisi yang berbeda: institusi, tokenomics, dan utilitas jaringan. 🚀

## 💰 ETF Solana: US$1,47 Miliar dan Masih Berlanjut

Data SoSoValue mencatat ETF spot Solana di AS menyerap **US$28,87 juta** dalam satu hari, inflow terbesar kedua sepanjang September, dengan Bitwise memimpin di angka US$26,38 juta. Angka itu membawa akumulasi inflow menjadi **US$1,47 miliar**, dengan total net assets **US$1,77 miliar** atau setara **2,56% kapitalisasi pasar SOL**.

Yang menarik, ini terjadi di tengah pasar yang goyang. Pada hari yang sama (22 September), dana Bitcoin justru mencatat inflow US$714,75 juta dan Ethereum US$162,31 juta — artinya rotasi ke aset non-BTC bukan lagi sekadar wacana. Buat investor Indonesia yang mengikuti aliran institusi, sinyalnya jelas: ETF Solana tumbuh dari nol menjadi aset US$1,7 miliar dalam waktu kurang dari satu tahun.

## 📉 SGP-0002: Inflasi SOL Turun Dua Kali Lebih Cepat

Proposal **SGP-0002** lolos dengan **67% dukungan** — tipis, hanya sedikit di atas ambang dua pertiga yang dibutuhkan. Sekitar 25% menolak, 7,84% abstain, dan partisipasi mencapai 60,7% dari stake yang memenuhi syarat. Voting sempat ketat sampai menit terakhir; validator Kraken 2 (bobot ~2%) dan Galaxy (~1,7%) memindahkan suara mereka ke kubu "setuju" beberapa saat sebelum tenggat tutup.

Apa yang berubah? Tingkat disinflasi tahunan SOL naik dari **15% menjadi 30%**. Artinya inflasi SOL menuju lantai terminal **1,5%** dalam kurang lebih **2,8 tahun**, bukan 5,7 tahun seperti jadwal lama. Dampak kumulatifnya: sekitar **18,9 juta SOL** lebih sedikit yang beredar dalam enam tahun ke depan, kira-kira 2,6% di bawah jadwal yang berlaku sekarang.

Buat holder jangka panjang, ini mengurangi tekanan jual dari emisi baru. Buat delegator, ini berarti **imbal hasil staking turun lebih cepat** — konsekuensi yang harus dipahami, bukan disembunyikan. Proposal ini bukan tokenomics baru yang dari nol, melainkan mempercepat jadwal deterministik yang sudah ada, dengan taper lunak supaya validator kecil tidak kena kejut mendadak.

Catatan penting: SGP-0002 baru tahap endorsement governance. Implementasi teknis berjalan lewat **SIMD-0550** dengan feature gate permanen yang menyetel taper ke 0,30 — butuh pengembangan client dan koordinasi validator dulu. Jadi jangan tunggu perubahan terjadi Senin depan.

Sementara itu, dalam voting jaringan pertama Solana ini, SGP-0001 (semacam konstitusi governance) lolos telak dengan 95,35%, dan SGP-0003 (perubahan fee supaya lebih banyak SOL dibakar) gagal dengan dukungan ~54%.

## 🤖 76% Transaksi x402 Ada di Solana

Ini bagian yang paling sering dilewatkan media arus utama. Data Artemis menunjukkan Solana memproses **23,2 juta transaksi x402 dalam empat minggu** (22 Agustus – 19/22 September), atau **76% dari seluruh aktivitas** protokol tersebut. Jaringan terbesar kedua mencatat 3,39 juta — kurang dari sepertujuh.

Bukan jumlah transaksi saja yang menarik, tapi siapa yang memakainya. Program dompet AI korporat Ramp untuk **70.000+ bisnis**, integrasi **AWS CloudFront** untuk pay-per-AI-crawler, serta layanan data berbayar dari Messari dan Nansen semuanya settle di Solana.

Lalu pada 18 September, Coinbase meng-upgrade facilitator Solana-nya: dukungan skema pembayaran `upto` (server boleh menagih sampai plafon tertentu, bukan nominal tetap) plus pemangkasan latensi verifikasi pembayaran **66%**. Untuk agen AI yang menembak ribuan request per menit, pemotongan latensi dua pertiga itu langsung terasa di throughput.

Total protokol x402 sendiri tercatat **75,41 juta transaksi** dengan volume **US$24,24 juta** dalam 30 hari terakhir. Angka volumenya kecil dibanding transaksi — dan itu memang wajar: ini rel pembayaran mikro per-request, bukan lorong transfer dana besar.

## 🔧 Infrastruktur yang Menopang Semuanya

Tiga feature gate Solana aktif di mainnet pada periode ini:

- **Transaction V1** — format transaksi baru yang sudah jalan di mainnet, membuka jalan menyederhanakan format lama.
- **Rent reduction ke 5.080 lamports per byte** — penyimpanan state on-chain turun drastis, kabar baik untuk aplikasi padat data.
- **Slot time 250ms** — dari target 300ms, dengan sasaran akhir 200ms menyusul lewat Alpenglow.

Finalitas di bawah 400 milidetik dan biaya per transaksi jauh di bawah satu sen adalah alasan teknis kenapa panggilan API senilai US$0,001 tetap ekonomis di Solana, sementara di chain yang lebih lambat atau lebih mahal, biaya settlement-nya bisa menghabiskan nilai pembayaran itu sendiri.

## 🧭 Kesimpulan

September 2026 memberi tiga sinyal yang saling menguatkan untuk Solana:

1. **Uang institusi mengalir** — ETF menembus US$1,47 miliar tanpa perlu reli besar.
2. **Tokenomics mengencang** — disinflasi dipercepat; lebih sedikit emisi, konsekuensi yield turun.
3. **Utilitas nyata terbentuk** — 76% pangsa transaksi x402 dengan pemakai korporat, bukan cuma aktivitas spekulatif.

Ketiganya belum menjamin harga. Pasar tetap bisa koreksi, dan satu bulan bagus tidak mengubah struktur risiko. Tapi kalau kamu mengikuti narasi "Solana bukan hanya cepat, tapi juga mulai dipakai untuk hal yang belum ada pemainnya", September ini adalah buktinya yang paling konkret sejauh 2026.

Menurut kamu, mana yang lebih berpengaruh jangka panjang: aliran ETF atau pangsa pasar pembayaran agen AI? Tulis di kolom komentar.

— Chokdi 🐷 · Content Studio · 2026
