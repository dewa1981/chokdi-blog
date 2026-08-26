---
title: "Upgrade Ethereum Glamsterdam Pensiunkan Aturan Gas 21.000 — Wallet Bisa Salah Hitung 🔥"
date: 2026-08-25T09:31:00+07:00
draft: false
tags: ["Crypto", "Ethereum", "Glamsterdam", "Blockchain", "EIP"]
---
Ethereum lagi bersiap buat upgrade terbesarnya di 2026: **Glamsterdam**. Dan salah satu dampaknya nyentuh aturan paling tua yang selama ini diandalkan semua wallet: **transfer ETH = flat 21.000 gas**. Mulai upgrade ini, kirim ETH ke alamat baru harganya bakal beda sama kirim ke alamat lama — dan software yang kakunya nempel sama angka 21.000 berpotensi salah hitung biaya. Buat kamu yang pegang ETH atau develop di ekosistem Ethereum, ini wajib dipantau, Bang!

## 🧱 Dulu: Kenapa Selalu 21.000 Gas?

Gas itu satuan "upah" kerja jaringan Ethereum. Tiap transaksi minta jaringan ngitung sesuatu, dan user bayar dalam ETH. Selama bertahun-tahun, transfer ETH dasar selalu dihitung **21.000 gas** — mau kirim ke alamat yang udah sering dipake atau ke alamat baru yang belum pernah muncul di record blockchain. Angka ini jadi patokan universal: wallet pakai buat nentuin gas yang ditempel, block explorer pakai buat sorting transaksi.

## 💥 Sekarang: Alamat Baru vs Alamat Lama Bakal Beda Tarif

Di upgrade **Glamsterdam**, aturan itu berubah. Kirim ETH ke akun yang udah exist tetap 21.000 gas. Tapi kirim ke alamat yang **belum pernah ada** di record Ethereum bakal lebih mahal — karena jaringan harus bikin akun baru dan nyimpen datanya permanen.

Biaya ekstranya: **183.600 unit "state gas"** (kategori gas baru, dirancang di EIP-8037/8038). Alasannya masuk akal: bayar ke alamat lama Cuma ngubah saldo yang udah ditracking, sedangkan bayar ke alamat baru nambah record yang harus disimpen selamanya. Dua pekerjaan beda yang selama ini dihargai sama — sekarang dibedain.

Efeknya: aplikasi yang menganggap 21.000 sebagai **harga tetap** (bukan cuma batas bawah) bakal nolak transaksi valid atau ngasih estimasi fee yang kurang. Wallet, tracker blockchain, sampai kalkulator gas kena imbasnya.

## 🧪 Platåberget: Testnet Baru yang "Sengaja Dibikin Rusak"

Ethereum Foundation udah ngasih warning resmi lewat [blog post 17 Agustus](https://blog.ethereum.org/2026/08/17/plataberget-testnet) ke para developer wallet: update software kalian sekarang. Glamsterdam mulai dinyalakan **Kamis, 20 Agustus** di **Platåberget** — testnet publik yang pakai token tanpa nilai, biar developer bebas ngerusak-ngrusak tanpa risiko. Habis itu lanjut ke **Sepolia** dan **Hoodi**, baru ke Ethereum mainnet (target **Q4 2026**).

Glamsterdam sendiri bukan cuma soal gas — ini paket besar: **ePBS (EIP-7732)**, pemisahan proposer-builder yang ngerombak cara block dibangun, plus **Block-Level Access Lists** dan kenaikan **gas limit dari 60 juta ke ~200 juta**. Jadi ini upgrade fundamental, bukan sekadar penyesuaian tarif.

## 📺 Video Fresh yang Worth Watching

Buat yang lebih suka nonton: video **"Ethereum's 21,000 Gas Rule Dies: Why Wallets May Break in Glamsterdam"** (FatheryFinds) dan **"What Is the Ethereum Glamsterdam Upgrade?"** (SuperEx) udah rilis minggu ini, plus analisis FXEmpire soal potensi Glamsterdam memantik bull run ETH berikutnya. Konteksnya juga makin seru karena ETH minggu ini **naik ~33%** (dari ~$1.893 ke ~$2.526) di tengah rally crypto global bareng Bitcoin yang udah ke $80K.

## 🧑‍💻 Yang Perlu Kamu Lakukan (Poin Praktis)

1. **User biasa: gak perlu panik minggu ini.** Kirim ETH biasa masih jalan normal — warning ini ditujukan ke pembuat software.
2. **Update wallet & app kamu** ke versi terbaru — dev wallet udah mulai nyesuaiin estimator gas.
3. **Kalau transaksi tiba-tiba gagal/underpriced** setelah mainnet Glamsterdam, cek dulu apakah ini soal "kirim ke alamat baru" sebelum nyalahin jaringan.
4. **Developer**: jangan hardcode 21.000 — pakai estimasi dinamis (eth_estimateGas) dan handle kasus `to` = alamat kosong.
5. Pantau jadwal resmi di blog.ethereum.org biar gak ketinggalan momen switch ke mainnet.

## 🎯 Kesimpulan

Glamsterdam adalah pengingat bagus bahwa blockchain itu bergerak — bahkan aturan "paling pasti" kayak gas 21.000 bisa berubah. Bagi pengguna Indonesia yang pegang ETH, kabar ini gak perlu bikin takut: justru ini sinyal ekosistem Ethereum makin dewasa. Yang penting: jangan pake wallet usang, dan selalu siapin gas ekstra kalau kirim ke alamat baru setelah upgrade mendarat di mainnet. Update terus info cryptonya di sini, biar gak ketinggalan! 🚀

— Chokdi 🐷 · Content Studio · 2026
