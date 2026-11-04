---
title: "Arbitrum Bekukan $30 Juta Dana Hack Binance Tanpa Private Key — Kok Bisa?"
date: 2026-11-05T01:20:42+07:00
draft: false
tags: ["Crypto", "Arbitrum", "Keamanan", "On-Chain", "Binance"]
---

# Arbitrum Bekukan $30 Juta Dana Hack Binance Tanpa Private Key — Kok Bisa?

Di crypto kita diajari satu hukum besi: dana cuma bisa pindah kalau **private key** menandatangani transaksi. Tanpa key, tidak ada yang bisa disentuh. Tapi Jumat, 30 Oktober 2026 pukul 08:08 HKT, **Arbitrum memindahkan 8.425 ETH dan 74.559.805,2 ARB** — sekitar **$30 juta** — dari alamat yang dikaitkan dengan [hack Binance $6,3 miliar](/posts/binance-hack-63-miliar-terbesar-sejarah/). Tanpa tanda tangan si hacker. Tanpa retas. Tanpa bug. Ini fitur, bukan kecelakaan.

## 🧊 Kronologi: satu transaksi, tiga langkah

Security Council Arbitrum adalah **12 orang yang dipilih pemegang token ARB**, dengan kuasa darurat untuk meng-upgrade kontrak inti kalau **9 dari 12 anggota** setuju. Kuasa itu dipakai dengan cara yang cukup elegan:

- Satu transaksi di Ethereum (**0xb69c…35d6**, block 26301886) memanggil L1 UpgradeExecutor lewat Safe 9-dari-12: mengarahkan proxy kontrak **Inbox** ke implementasi baru, mengirim pesan, lalu mengembalikannya.
- Implementasi baru menambahkan fungsi `sendUnsignedTransactionOverride` — pembuat transaksi lintas-chain yang bisa "mengaku" sebagai pengirim alamat lain, **tanpa alias**.
- Sekitar **10 menit** kemudian di Arbitrum One: dua transaksi tipe **0x65 (ArbitrumUnsignedTx)** dengan nilai r, s, v semuanya nol. Nonce 2 memindahkan ARB, nonce 3 mengirim **8.425,998 ETH** ke alamat `0x000…0DA0`. Keduanya memakai penghitung transaksi milik alamat si penyerang.
- Kode Inbox dikembalikan ke implementasi asli **di transaksi yang sama** — semuanya atomik.

Pengumuman resmi di forum governance menegaskan: "Tidak ada dana atau aplikasi pengguna lain yang terpengaruh." Dana beku itu hanya bisa keluar lewat **voting governance ArbitrumDAO**.

## 🔑 Kenapa bisa tanpa private key?

Analoginya begini: private key itu kunci pintu rumah kamu. Tapi di jaringan L2, ada **kunci master** untuk mengganti kunci pintu seluruh gedung — namanya *upgrade path*. Selama mayoritas council setuju, kontrak inti bisa diganti sementara, dan pesan dari Ethereum bisa dipaksa terlihat berasal dari alamat siapa pun.

Firma keamanan Zealynx yang menelusuri transaksi ini menyimpulkan: asumsi bahwa "alamat hanya bergerak kalau key-nya menandatangani" berlaku **"tergantung siapa yang mengontrol jalur upgrade"**. Kalimat itu bukan teori konspirasi — itu konsekuensi desain.

Yang juga perlu dicatat: council memakai kuasa yang memang diberikan DAO, dan mempublikasikan kedua aksi dalam **1,5 jam**. Transparan. Tapi tetap menunjukkan di mana batas "desentralisasi" sebuah L2.

## ⚖️ Ini kedua kalinya — dan yang pertama ribet

April 2026, council melakukan hal serupa: membekukan **30.765 ETH** (waktu itu sekitar **$71 juta**) dari exploiter KelpDAO. Bedanya, mencairkan dana itu butuh **berminggu-minggu**: keluarga pemegang putusan terorisme terhadap Korea Utara mencoba mengklaim, dan hakim federal Manhattan harus mengubah *restraining notice* sebelum DAO bisa voting mengirim dana ke Aave.

Jadi rumusnya jelas: **freeze itu cepat, unfreeze itu politik dan hukum.** Untuk konteks, FBI mengatribusikan hack Binance ke kelompok **TraderTraitor** (Korea Utara) pada 31 Oktober.

## 📉 Pasar sudah lupa? Hampir

Menariknya, pasar pulih cepat. Data CoinDesk 4 November: Bitcoin rebound dari sekitar **$75.600** ke **$80.500** (+3,9%), Ethereum **$2.435** (+6,1%), dan indeks DeFi memimpin dengan kenaikan sekitar 5%. Tapi skeptisisme belum hilang — **Fear & Greed Index 37** dan **altcoin season index 51** menunjukkan sentimen masih hati-hati. Sorotan berikutnya: laporan tenaga kerja AS hari Jumat.

Di YouTube, cerita ini juga ramai dibahas — Andrei Jikh mengangkatnya lewat video **"The Biggest Crypto Theft In History"**, sementara Al Jazeera English membahasnya dari sisi risiko platform di **"How vulnerable are cryptocurrency platforms?"**.

## 🧠 5 poin praktis buat kamu

1. **Self-custody ≠ kebal governance.** Di L2, kunci upgrade dipegang council. Simpan dana besar di tempat yang trust model-nya kamu pahami.
2. **Cek pemegang upgrade key sebelum masuk.** Setiap L2 punya komposisi security council berbeda. Baca dokumentasinya, bukan cuma halaman "decentralized".
3. **Sebar risiko.** Jangan 100% dana di satu L2 atau satu bridge. L1, CEX, dan L2 punya jenis risiko yang berbeda.
4. **"Dana disita" bukan "dana kembali".** Butuh voting DAO, dan bisa nyangkut sengketa hukum berbulan-bulan seperti kasus April.
5. **Jangan panik jual.** Fundamental tidak berubah dalam semalam. Yang berubah adalah pemahaman kamu soal siapa yang sebenarnya bisa menggerakkan dana.

## 🎯 Kesimpulan

Kejadian $30 juta ini bukan bukti Arbitrum "tidak aman". Justru sebaliknya — mekanisme daruratnya bekerja cepat, sesuai mandate, dan transparan. Tapi ia mengingatkan satu hal yang sering terlewat: di L2, private key kamu adalah **lapisan terakhir**, bukan satu-satunya. Selama ada jalur upgrade, selalu ada pihak yang bisa mengganti aturan main. Baca trust model-nya, jangan cuma lihat APY-nya.

**Sumber:** CoinDesk (3–4 Nov 2026), Arbitrum Governance Forum — *Security Council Emergency Action 30/10/2026*, Zealynx di Ethereum Magicians (2 Nov), Etherscan tx `0xb69c…35d6`. Video: Andrei Jikh — *"The Biggest Crypto Theft In History"*; Al Jazeera English — *"How vulnerable are cryptocurrency platforms? | Inside Story"*.

— Chokdi 🐷 · Content Studio · 2026
