---
title: "US$247 Juta dari Hack Binance Sudah Dicuci Lewat Coinjoin — US$2,35 Miliar Masih Numpang di Dompet"
description: "Elliptic melacak 90.000 transaksi di 16 blockchain: US$247 juta dana hack Binance masuk coinjoin yang dikoordinasi satu pihak bernama Kruw, US$2,85 miliar sudah dibekukan, US$2,35 miliar masih bergerak. Plus kasus Chainflip: vault kering sembilan menit ke Tornado Cash."
date: 2026-11-24T01:00:00+07:00
draft: false
tags: ["Crypto", "Bitcoin", "Binance", "On-Chain", "Keamanan"]
---

Hack Binance US$6,3 miliar bukan lagi soal "bagaimana bisa masuk" — itu sudah dijawab FBI: kelompok TraderTraitor, satu wawancara kerja palsu, lalu berbulan-bulan menanam diri di sistem. Pertanyaan yang sekarang jauh lebih penting: **ke mana uangnya pergi, dan seberapa cepat bisa diuangkan?**

Senin, 23 November 2026, Elliptic memberi jawaban sebagian. Pendiri Elliptic, Tom Robinson, menyebut **sedikitnya US$247 juta** dana curian sudah melewati transaksi bitcoin yang menggabungkan dana banyak pengguna sekaligus — **coinjoin** — supaya asal-usulnya kabur.

## 🧩 Coinjoin: cuci uang yang tidak lewat bursa

Coinjoin itu sederhana konsepnya: banyak orang menaruh bitcoin di satu transaksi besar, keluar ke alamat baru, sehingga rantai kepemilikan putus. Tidak ada bursa, tidak ada KYC, tidak ada pintu yang bisa ditutup otoritas.

Yang bikin temuan Elliptic menarik: hampir semua transaksi pencampuran itu **dikoordinasi oleh satu pihak yang dikenal sebagai "Kruw"**, dan aktivitasnya makin mengumpul di **jam-jam yang sama setiap hari**. Pola itu, kata Robinson, bisa berarti dana sudah diserahterimakan ke pencuci uang berbasis Tiongkok — pola yang sama dengan pencurian Korea Utara sebelumnya. Tapi ia sendiri menegaskan waktunya belum cukup untuk jadi kesimpulan final.

Semua ini terlacak di **lebih dari 27.000 dompet, minimal 16 blockchain, dan sekitar 90.000 transaksi**. Bukan pekerjaan satu orang; ini industri.

## ❄️ Yang sudah beku dan yang masih jalan

Angka per 20 November 2026:

- **US$2,85 miliar** sudah dibekukan atau disita.
- **US$2,35 miliar** masih berada di dompet yang terhubung ke pencurian.
- Elliptic menyebut **hampir tidak ada bukti** dana diubah jadi uang tunai — artinya bursa dan perantara keuangan masih punya peluang mencegat.

Di meja hukum, Binance mengantongi perintah pembekuan global dari pengadilan Abu Dhabi pada 19 November. Tapi ini penting dipahami: perintah itu **mengikat aset yang ada di bursa**, bukan dompet yang kuncinya dipegang peretas. Transfer antar-dompet pribadi tetap tidak bisa dihentikan siapa pun. Sidang lanjutan 1 Desember akan menentukan apakah 18 perusahaan wajib menyerahkan aset yang sudah mereka bekukan.

Binance sendiri menyebut pengacaranya sudah mengidentifikasi **26.000 alamat dompet** berisi aset curian, dan daftarnya diperbarui mengikuti pergerakan dana.

## ⚡ Chainflip: vault kering dalam satu transaksi, Tornado Cash sembilan menit

Kasus kedua pekan ini lebih kecil nominalnya, tapi lebih bikin merinding dari sisi teknis. Chainflip, protokol swap lintas-chain, kehilangan sekitar **US$4,86 juta** dari vault Ethereum-nya: **520,22 ETH, 3,25 juta USDC, dan 758.000 USDT** keluar dalam **satu transaksi**.

Yang bikin aneh: transaksi itu membawa **tanda tangan yang valid**. Pelacak on-chain seperti Onchain Lens menilai ini mengarah ke kompromi kunci bersama yang dipakai validator untuk menyetujui pembayaran dari vault. Bukan private key satu orang — kunci yang seharusnya butuh kesepakatan banyak pihak.

Stablecoin langsung ditukar ke ether, dan **hampir seluruh dana masuk Tornado Cash dalam sembilan menit**. Sembilan menit. Tidak ada ruang untuk negosiasi, tidak ada waktu untuk bursa membekukan apa pun.

Protokol masuk safe mode penuh: deposit, penarikan, swap, dan quote berhenti. Liquidity provider tidak bisa menarik dana sampai safe mode dicabut. Token FLIP jatuh lebih dari 30%, dengan TVL sekitar US$13,3 juta. Ini bukan exploit pertama — September lalu vault Tron-nya juga kehilangan sekitar 736.000 USDT dan diganti dari dana surplus.

## 🔍 Empat hal praktis yang bisa dipetik

1. **Coinjoin meninggalkan pola.** Kalau koordinasinya jalan di jam yang sama tiap hari dengan volume serupa, itu sidik jari. Analisis on-chain hari ini bukan soal mengikuti alamat satu per satu, tapi membaca ritme.
2. **Pembekuan pengadilan berhenti di pintu bursa.** Dompet self-custody tidak tunduk pada perintah apa pun. Satu-satunya pertahanan adalah kecepatan bursa menandai alamat — karena itu daftar 26.000 alamat Binance itu berharga.
3. **Vault lintas-chain adalah titik konsentrasi.** Satu kunci bersama bocor, satu transaksi, habis. Kalau kamu menaruh likuiditas di bridge atau vault, tanyakan dulu: berapa pihak yang harus setuju, dan apa yang terjadi kalau salah satunya disusupi?
4. **Safe mode bukan cuma soal keamanan, tapi soal likuiditasmu.** Saat protokol membeku, LP ikut terkunci. Chainflip punya sejarah mengganti rugi dari surplus — protokol lain belum tentu punya.

## 📌 Catatan yang sering kelewat

Pasar tidak runtuh karena berita ini. Bitcoin justru sedang memantul dari low dua tahun, dan yang menggerakkan harga pekan ini adalah saham AI serta ekspektasi The Fed — bukan pelacakan dana curian. Jadi jangan campur aduk: **berita hack memengaruhi kepercayaan pada bursa dan protokol tertentu, bukan otomatis harga seluruh pasar.**

Yang perlu diingat dari pekan ini cuma enam angka: **247 juta** dicuci, **2,35 miliar** masih jalan, **2,85 miliar** beku, **27.000 dompet**, **16 blockchain**, dan **9 menit** sampai dana hilang di mixer.

Sisanya cerita hukum — dan itu baru mulai 1 Desember.

**Baca juga:** [Binance Kena Hack $6,3 Miliar: Cerita Terbesar dalam Sejarah Crypto, dan Apa Artinya Buat Kita](https://chokdi.ano99.com/posts/binance-hack-63-miliar-terbesar-sejarah/) · [Patch Sudah Ada Tapi Belum Dirilis: Pelajaran dari Hack US$319 Juta Liquid Network](https://chokdi.ano99.com/posts/patch-tertinggal-hack-liquid-network-319-juta/) · [AI Dipakai Menyerang, AI Dipakai Bertahan: Pelajaran dari Hack Binance $6,3 Miliar](https://chokdi.ano99.com/posts/ai-serangan-crypto-aliansi-keamanan/)

— Chokdi 🐷 · Content Studio · 2026
