---
title: "Liquid Network Lumpuh: 4.000 BTC (US$320 Juta) Ditarik Peretas yang Ngaku White-Hat"
date: 2026-09-08T18:15:00+07:00
draft: false
tags: ["Bitcoin", "Kripto", "Keamanan", "Liquid Network"]
---

Sidechain Bitcoin milik Blockstream, **Liquid Network**, tiba-tiba menghentikan seluruh transaksinya pada 7 September 2026. Penyebabnya bukan bug kecil: hampir **4.000 BTC (sekitar US$320 juta)** ditarik dari federation wallet yang menjadi cadangan token L-BTC. Yang bikin heboh, pelakunya mengaku *white-hat hacker* dan bilang dananya bakal dikembalikan — asal bug-nya diperbaiki dulu.

## Yang Terjadi: Cadangan L-BTC Dikuras 95%

Liquid Network adalah sidechain Bitcoin yang diluncurkan Blockstream pada 2018, dipakai banyak exchange untuk transaksi cepat dan aset tokenisasi. Untuk setiap L-BTC yang beredar di Liquid, harus ada 1 BTC asli yang disimpan di federation wallet — dompet multisig yang dijaga puluhan federation member.

Nah, pada 7 September, pelaku menarik **±4.000 BTC** dari dompet cadangan itu. Jumlahnya gila: sekitar **95% dari total saldo ±4.200 BTC** yang mendukung L-BTC di seluruh jaringan. Begitu ketahuan, tim Liquid langsung menghentikan jaringan — bridge nodes dimatikan dan semua transaksi di-pause.

## "Kami White-Hat, Dana Akan Dikembalikan"

Bagian paling dramatis: pelaku tidak kabur. Mereka justru ninggalin pesan on-chain bertanda tangan yang isinya klaim sebagai *white-hat hacker* — istilah untuk peretas "baik" yang mengeksploitasi celah demi keamanan, bukan keuntungan pribadi. Mereka berjanji mengembalikan sebagian besar BTC setelah bug di **Elements** (software dasar Liquid) di-patch di semua node federation.

Penarikan ini diduga terjadi lewat layanan peg-out **SideSwap** memakai Peg-out Authorization Key (PAK). Menariknya, SideSwap sendiri menegaskan kunci itu **tidak diretas** — ini sinyal bahwa celahnya mungkin bukan di kunci, tapi di logika atau proses lain yang belum dipublikasikan detailnya.

Kronologi negosiasi ini dirakit oleh **Samson Mow** (CEO Jan3, mantan CSO Blockstream) dari pesan-pesan publik yang disematkan pelaku di transaksi Bitcoin. Timeline-nya panjang: negosiasi mulai sekitar 11:30 pagi waktu Pasifik, dan sampai malam (±9:12 PM PT) dana ±3.998,5 BTC belum bergerak kembali.

## Dampaknya ke Pengguna

- **Exchange menghentikan deposit & penarikan L-BTC** — kalau kamu punya L-BTC di exchange, dana aman tapi layanan jalan di tempat sampai jaringan pulih.
- **Aset Liquid lain tidak terdampak** — USDT, DePix, dan token RWA di Liquid tetap aman; yang bermasalah khusus L-BTC karena cadangan on-chain-nya yang ditarik.
- **Jaringan berhenti total** — semua transaksi di-pause, ini bukan cuma L-BTC, tapi seluruh aktivitas sidechain sampai situasi terkendali.

## Pelajaran Buat Pengguna Kripto

1. **Sidechain punya risiko sendiri.** "Pegged" asset seperti L-BTC bergantung pada keamanan federation wallet — kalau lapisan itu jebol, cadangannya bisa digoyang walau Bitcoin mainnet-nya aman.
2. **Klaim white-hat bukan jaminan.** Banyak peretas pakai istilah ini buat meringankan hukuman atau negosiasi. Sampai dana benar-benar kembali ke federation wallet, statusnya tetap "hilang".
3. **Diversifikasi, jangan taruh semua di satu sidechain.** Ini kasus kedua besar di ekosistem Bitcoin dalam waktu singkat — sebelumnya industri juga diguncang kasus serupa di platform lain.

Hingga artikel ini ditulis, dana 4.000 BTC itu belum kembali dan tidak ada pesan lanjutan dari pelaku. Komunitas Bitcoin menunggu apakah janji "white-hat" itu ditepati — atau ini jadi salah satu penarikan terbesar dalam sejarah sidechain Bitcoin. Yang jelas, insiden ini bakal jadi bahan diskusi panjang soal keamanan federation dan desain sidechain ke depan.

Menurutmu, apakah dana 4.000 BTC itu bakal kembali? Tulis pendapatmu di komentar ya!

— Chokdi 🐷 · Content Studio · 2026
