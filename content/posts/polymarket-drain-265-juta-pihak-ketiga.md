---
title: "Polymarket Bocor Rp 42 Miliar dalam Hitungan Menit — yang Jebol Bukan Smart Contract, tapi Vendor Pihak Ketiga"
date: 2026-11-01T01:40:00+07:00
draft: false
tags: ["Crypto", "Keamanan", "DeFi", "Prediction Market", "Berita"]
---

Kamis, 29 Oktober 2026, bursa prediksi **Polymarket** menghentikan perdagangan di platform internasionalnya (Polymarket.com). Bukan karena pasar sepi, tapi karena ada saldo pengguna yang mengalir keluar dalam hitungan menit. Estimasi dari data on-chain Arkham yang dikutip sejumlah media: **2,2 sampai 2,65 juta dolar** — sekitar Rp 36–42 miliar.

Yang bikin cerita ini penting buat siapa pun yang menyimpan uang di platform crypto: **yang bocor bukan smart contract-nya**. Menurut pengakuan Polymarket sendiri, sumber masalahnya ada di **pihak ketiga** — vendor di luar protokol inti mereka. Artinya, kode yang sudah diaudit pun tidak menolong kalau pintu sampingnya lupa dikunci.

## ⏱️ Kronologi: dari cancel-only sampai normal lagi dalam satu jam

Timeline ini penting, karena kecepatan respons adalah satu-satunya hal yang bisa dinilai saat insiden begini terjadi. Semua waktu ET (WIB +11 jam) dari status page resmi dan unggahan akun X Polymarket, dirangkum Unchained:

- **14:05 ET (01:05 WIB)** — platform masuk mode **cancel-only**: order lama masih bisa dibatalkan, tapi order dan trade baru tidak diproses. Aksi *relayer* dihentikan sementara.
- **14:33 ET** — Polymarket menyebut sudah menemukan dan memperbaiki masalahnya, menyatakan "salah satu penyedia pihak ketiga kami terkompromi", dan melaporkan kejadian itu ke aparat hukum.
- **14:54 ET** — pengumuman perdagangan akan dibuka lagi sekitar pukul 15:00.
- **15:05 ET** — status page menandai insiden **resolved**. Perdagangan kembali normal, dan Polymarket menyatakan akan **mengganti penuh** dana pedagang yang terdampak.

Yang tidak diberitahukan sampai berita ini ditulis: berapa total kerugian resmi, berapa akun yang kena, dan vendor mana yang jebol. Polymarket hanya menyebut angka di luar (dari Arkham) sebagai estimasi pihak ketiga.

## 🔍 Pelajaran utama: risiko rantai pasok, bukan risiko "kode protokol"

Pola ini bukan pertama kali. Unchained mencatat insiden Polymarket kali ini adalah **yang ketiga sejak Mei 2026**, dan semuanya masuk lewat "titik akses di sekitar platform" — login, frontend, relayer — bukan lewat kontrak perdagangannya.

Ini pergeseran yang layak dicatat. Selama bertahun-tahun orang belajar menilai platform crypto dari satu pertanyaan: *"smart contract-nya sudah diaudit belum?"* Insiden-insiden terakhir menunjukkan pertanyaan yang lebih relevan: **berapa banyak vendor luar yang ikut memegang akses ke akun dan dana saya?**

Satu vendor login yang jebol bisa menembus semua audit kontrak di belakangnya. Kasus Binance akhir Oktober lalu juga meletus di periode yang sama — dan itu bukan kebetulan soal model ancaman yang sedang berubah, melainkan soal permukaan serang yang makin lebar: makin banyak integrasi, makin banyak pintu.

## 🛡️ 5 langkah praktis kalau bursa tempat kamu simpan dana kena insiden

Ini bukan teori — ini urutan yang masuk akal dilakukan dalam 30 menit pertama, saat informasi masih simpang siur.

**1. Jangan klik apa pun dari DM atau grup.** Setelah insiden besar, gelombang pesan "verifikasi wallet", "klaim refund", dan tautan restore selalu muncul. Itu bukan bantuan, itu panen korban kedua. Satu-satunya sumber status adalah status page resmi dan akun X resmi platform.

**2. Pahami arti "cancel-only".** Mode ini berarti order bisa dibatalkan tapi trade baru tidak jalan, dan penarikan sering ikut dibekukan. Jangan memaksa membuat order baru di platform lain sebagai "ganti" sebelum situasinya jelas — sering kali itu justru memindahkan dana ke tempat yang belum tentu lebih aman.

**3. Hitung eksposur dalam 2 menit, bukan 2 jam.** Tuliskan: berapa saldo di platform (custodial, kunci di tangan mereka), berapa di wallet sendiri (kunci di tangan kamu). Yang di platform = risiko pihak ketiga. Yang di wallet sendiri = risiko seed phrase kamu.

**4. Kalau kamu terdampak, siapkan bukti dari awal.** TX hash, screenshot posisi, riwayat order, dan email akun. Janji "reimburse penuh" biasanya dieksekusi berdasarkan bukti kepemilikan, bukan berdasarkan siapa yang paling cepat melapor di media sosial.

**5. Setelah pulih, ubah kebiasaan simpan dana.** Saldo kerja di platform secukupnya untuk trading sepekan; sisanya ke wallet yang kamu pegang sendiri. Dan perlakukan vendor login sebagai bagian dari penilaian keamanan platform, sama seriusnya seperti audit kontrak.

## 📉 Kenapa ini terjadi sekarang

Konteksnya tidak bisa dilepas: pasar sedang tidak ramah. Bitcoin bergerak di kisaran **76–77 ribu dolar** saat insiden terjadi, jauh di bawah puncak Oktober 2025 di sekitar 126 ribu. Di kondisi seperti ini platform memangkas biaya, mempercepat rilis, dan menambah integrasi untuk mengejar volume — tiga hal yang semuanya memperlebar permukaan serang.

Untuk pembaca di Indonesia, kesimpulannya sederhana dan tidak nyaman: **platform yang "kembali normal dalam satu jam" belum tentu platform yang aman** — itu hanya berarti mereka punya prosedur darurat yang jalan. Yang menentukan apakah uangmu selamat adalah seberapa kecil dana yang kamu tinggalkan di sana, dan seberapa jelas kamu tahu siapa yang memegang kuncinya.

Kalau mau melihat pola serupa dari kasus lain, dua catatan lama di blog ini masih relevan: [Binance dan rekor perampokan kripto terbesar](/posts/binance-hack-6-3-miliar-terbesar-sejarah/) dan [patch tertinggal yang menghabiskan 319 juta dolar](/posts/patch-tertinggal-hack-liquid-network-319-juta/).

**Sumber:** The Block (29 Okt 2026), Unchained (29 Okt 2026), NBC News, CNBC, Forbes, status page Polymarket, data Arkham.

— Chokdi 🐷 · Content Studio · 2026
