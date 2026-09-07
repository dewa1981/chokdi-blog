---
title: "Coldcard Hacker Mulai Cuci BTC Curian: 97 Bitcoin Dipindah via THORChain dan CoinJoin"
date: 2026-09-07T18:15:00+07:00
draft: false
tags:
  - bitcoin
  - crypto
  - keamanan
  - coldcard
  - self-custody
---

Hacker di balik peretasan hardware wallet Coldcard akhirnya mulai bergerak. Setelah sebulan lebih mendiamkan hasil curian, **97,09 BTC (sekitar $7,7 juta) baru saja dipindah** lewat THORChain dan CoinJoin untuk mengaburkan jejak — dan ini sinyal fase baru dari salah satu eksploit terbesar 2026. Berikut analisis lengkap dari Galaxy Research.

## 🕵️ 97 BTC Pindah dalam Tiga Putaran

Galaxy Research melacak pergerakan dana hasil **gelombang ketiga** pencurian Coldcard. Strateginya jelas: pecah dana besar, cuci lewat jalur yang sulit dilacak, dalam beberapa tahap:

| Tanggal | Jumlah | Metode |
|---|---|---|
| 2 September | 20,5 BTC | THORChain (DEX cross-chain) → landing di Ethereum |
| 5 September | 15,48 BTC | CoinJoin (dicampur transaksi banyak user) |
| 6 September | 61,12 BTC | Dari 10 vault berbeda |

CoinJoin menggabungkan transaksi bitcoin dari banyak pengguna sekaligus, sehingga sangat sulit menghubungkan input dengan output akhirnya. Sementara THORChain dipakai buat memindahkan dana lintas blockchain — dari Bitcoin ke Ethereum — biar jejak on-chain-nya makin putus.

Total yang sudah "dicuci" dari gelombang ketiga: **97,09 BTC atau sekitar 45% dari total yang dicuri di gelombang itu**.

## 🔓 11 Vault Terbesar Sudah Kosong

Yang lebih menarik: vault-vault ini **bukan dompet korban**. Galaxy Research menemukan sang penyerang membuat vault khusus — satu untuk setiap korban — dengan format **multisig 2-of-2** yang butuh dua kunci untuk memindahkan bitcoin.

Hacker bekerja sistematis: menguras **293 vault dari yang terbesar ke terkecil**, dan kini **11 vault terbesar sudah habis total**. Sisa tebusannya:

- 10 vault berikutnya: masih ada 30,81 BTC
- Vault peringkat 61–293: total 33,77 BTC

Galaxy juga menemukan satu vault tambahan yang didanai 58 alamat dengan format sama — kemungkinan korban Coldcard lain. Kalau dihitung, total eksploit ini mendekati **1.806 BTC atau sekitar $143,9 juta**.

## 📊 82% BTC Curian Masih "Diam"

Kabar baiknya: dari seluruh BTC yang dicuri di semua gelombang, **82% masih berada di alamat milik penyerang** dan belum dipindah. Hanya 18% yang sudah bergerak lewat transaksi yang dirancang mengaburkan jejak.

Ini beda dengan hacker profesional seperti TraderTraitor dari Korea Utara yang biasanya langsung agresif mencuci dana dalam hitungan jam. Pola Coldcard ini terkesan lebih hati-hati — atau mungkin masih belajar cara memindahkan dana sebesar itu tanpa ketahuan.

## 🧬 Akar Masalah: Bug Firmware 2021

Buat yang baru dengar: pencurian ini mulai 30 Juli 2026, mengeksploitasi **bug firmware Coldcard versi Maret 2021** yang melemahkan keacakan (randomness) saat generate seed wallet. Efektifnya, kekuatan kunci anjlok drastis:

- Seharusnya: 128 bit (tidak mungkin di-brute-force)
- Kenyataannya: bisa turun sampai **40 bit** di perangkat lama — cukup lemah buat ditebak komputer modern

Update firmware yang sudah dirilis Coinkite **tidak bisa memperbaiki wallet yang seed-nya sudah terlanjur lemah**. Satu-satunya jalan: bikin seed baru dan pindahkan semua dana.

## 💡 Pelajaran Buat Pemegang BTC

Kasus ini pengingat keras: **self-custody memindahkan risiko, bukan menghilangkannya**. Hardware wallet cuma setangguh proses yang bikin kunci-nya. Beberapa hal yang wajib kamu cek:

- Kalau kamu generate seed Coldcard antara **Maret 2021 sampai patch terbaru** — anggap dompetmu sudah kompromi, pindah sekarang
- Firmware update itu wajib, tapi tidak menyelamatkan seed lama
- Beli hardware wallet dari **distributor resmi**, hindari pasar loak
- Simpan seed di tempat fisik yang aman, jangan pernah di foto atau cloud

Masih penasaran dengan rentetan kasus keamanan bitcoin tahun ini? Baca juga cerita [hack Coldcard gelombang awal senilai $116 juta](https://chokdi.ano99.com/posts/bitcoin-agustus-2026-etf-outflow-coldcard-hack/) dan [eksploit Liquid Network $320 juta yang bikin bursa panik](https://chokdi.ano99.com/posts/liquid-network-exploit-4000-btc/).

Menurutmu bakal ada gelombang pencucian lebih besar lagi, atau hacker-nya keburu ketahuan dulu? Tulis pendapatmu di kolom komentar! 🐷

— Chokdi 🐷 · Content Studio · 2026
