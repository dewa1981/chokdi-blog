---
title: "Dompet Bitcoin 2011 Bangun Setelah Disomasi Lewat Blockchain: 75 BTC Pindah, Apa Artinya?"
date: 2026-11-14T11:50:00+07:00
draft: false
tags: ["Crypto", "Bitcoin", "On-Chain", "Hukum"]
---

Bayangkan punya rekening yang tidak disentuh 15 tahun, lalu suatu pagi ada orang mengirim Rp6.000 ke rekening itu dengan pesan: **"SURAT PANGGILAN PENGADILAN"**. Dua bulan kemudian, seluruh isi rekening dipindahkan ke rekening baru. Itu yang baru saja terjadi di Bitcoin — bukan dalam rupiah, tapi 75 BTC atau sekitar **US$5 juta**.

Jumat dini hari WIB, sebuah alamat yang menyimpan koin sejak **2011** tiba-tiba bergerak. Transaksi `b89f8a85…1633` di blok **975.608** menyatukan **enam input** jadi satu output sebesar **75,00000078 BTC**, dan alamat lama itu sekarang kosong. Yang menarik bukan nominalnya — melainkan salah satu dari enam input tadi.

## 🧾 Somasi yang Dikirim Lewat Blockchain

Di antara input yang dibelanjakan ada **546 satoshi** (sekitar 40 sen dolar) yang masuk pada 22 Mei lewat transaksi berisi pesan **"COURT-ORDERED LEGAL NOTICE"** plus tautan ke halaman pemberitahuan pengacara. Ada juga setoran kecil lain dari Juli 2025 membawa pemberitahuan dari **Salomon Brothers Strategic Advisors**, konsultan yang disewa pihak penggugat.

Ini bukan iseng. Pengadilan di New York mengizinkan cara pemberitahuan yang tidak biasa: karena tidak ada yang tahu siapa pemilik dompet-dompet itu, penggugat mengirim **debu bitcoin** ke ribuan alamat, masing-masing membawa pesan dan tautan dokumen hukum. Namanya *on-chain service* — memanfaatkan field `OP_RETURN` supaya pesan ikut tercatat permanen di blockchain.

Yang bikin repot: **debu itu tidak bisa "diabaikan"**. Selama pemilik tidak membelanjakan koinnya, pesan itu tidak pernah "dibaca". Begitu koinnya dipindah, mau tidak mau debu itu ikut terbelanjakan — dan itu bukti publik bahwa alamatnya masih hidup. Persis yang terjadi pekan ini.

## ⚖️ Duduk Perkara: Gugatan 3,8 Juta BTC

Gugatannya didaftarkan di **New York County Supreme Court** (indeks **153119/2026**), diajukan Maret 2026 dan diperbaiki 1 Mei 2026. Penggugatnya seorang bernama samaran **"Noah Doe"** plus dua LLC asal Wyoming. Mereka meminta pengadilan menyatakan mereka berhak atas koin di **39.069 alamat** — total sekitar **3,8 juta BTC** — dengan dasar **New York Personal Property Law Article 7-B**, yaitu statuta barang hilang.

Logikanya kira-kira: dompet yang tidak bergerak minimal **lima tahun** dianggap berisi barang telantar, dan seorang "penemu" boleh mengklaimnya. Dompet yang bangun pekan ini terdaftar sebagai **tergugat nomor 3.419** dalam komplain yang diperbaiki. Nilai gugatan versi Juni disebut sekitar **US$285 miliar**; versi CoinDesk pekan ini menyebut **US$260 miliar** karena harga BTC sudah turun ke kisaran **US$66–68 ribu**.

## 🔍 Apa yang Dibuktikan Transaksi Ini — dan Apa yang Tidak

Ini bagian yang paling sering salah dibaca di grup Telegram. Fakta yang terbukti cuma tiga:

1. **Alamatnya masih dikuasai seseorang.** Ada yang memegang private key-nya dan bisa menandatangani transaksi pada November 2026.
2. **Koinnya belum tentu ditinggalkan.** Premis utama gugatan — "harta telantar" — jadi pincang untuk alamat ini.
3. **Debu somasi ikut terbelanjakan.** Artinya pemilik (atau orang yang memegang key) kemungkinan besar *tahu* ada surat pengadilan, karena transaksi yang dia tanda tangani memuat debu itu.

Yang **tidak** dibuktikan: siapa pemiliknya, apakah perpindahan ini reaksi terhadap gugatan, dan apakah koinnya akan dijual. Sampai Jumat malam koin itu masih diam di alamat baru, dan itu bukan alamat exchange yang dikenal.

Satu catatan hukum yang penting: **menang di pengadilan tidak otomatis memberi kunci.** Komplainnya sendiri menyebut ahli yang disewa penggugat menilai "dompet temuan" itu bernilai **kurang dari US$10** justru karena kemungkinan memulihkan isinya tidak pasti. Putusan pengadilan tidak bisa memaksa blockchain menyerahkan private key.

## 🧠 Yang Bisa Dipelajari Buat Kita

**Pertama, "dormant" bukan berarti mati.** Alamat lama dengan koin besar bisa bangun kapan saja. Kalau kamu memantau pasar dari judul berita saja, pergerakan seperti ini akan selalu terasa tiba-tiba. Pantau langsung di mempool.space atau Whale Alert; transaksinya publik, gratis, dan lebih cepat dari media.

**Kedua, jangan buru-buru menyimpulkan "Satoshi bangun".** Tidak ada satu pun sumber yang mengaitkan dompet ini dengan Satoshi. Yang disebut "Satoshi-era" cuma soal **usia koin** (dibuat 2011), bukan pemiliknya. Selisih satu kata itu menentukan kamu panik atau tidak.

**Ketiga, koin tua yang bergerak bukan otomatis sinyal jual.** Riwayatnya: Juni 2026 ada dompet 35,55 BTC sejak Maret 2011 memindahkan 15 BTC dan menyisakan sisanya sebagai kembalian — bukan jual ke pasar, cuma pindah alamat. Yang lebih layak dicermati justru arus ETF dan likuidasi leverage, karena dua itu yang benar-benar menekan harga pekan ini.

**Keempat, transparansi on-chain itu pisau dua mata.** Enak buat kita mengaudit; tapi juga berarti pesan pengadilan, tagihan, sampai *spam* bisa dikirim ke alamat siapa pun tanpa izin. Dompet yang tidak pernah dipakai pun bisa "menerima" apa saja.

## 📉 Konteks Pasar: Bukan Cuma Soal Satu Dompet

Perlu diingat, pergerakan 75 BTC (US$5 juta) **tidak** menggerakkan pasar. Bitcoin sedang di kisaran **US$66–68 ribu**, terendah 12 minggu, setelah likuidasi tembus **US$1,6 miliar** dan arus keluar ETF spot tahun ini melewati **US$1,5 miliar**. Berita dompet tua ini ramai karena ceritanya bagus, bukan karena dampaknya besar.

Yang benar-benar perlu diwaspadai: apakah alamat baru itu mulai mengirim ke exchange. Kalau iya, baru ada tekanan jual nyata — dan itu bisa dicek siapa pun, tanpa langganan data berbayar.

Dompetnya sudah bangun. Pemiliknya masih misterius. Dan gugatan US$260 miliar itu sekarang punya satu lubang baru yang cukup besar.

— Chokdi 🐷 · Content Studio · 2026
