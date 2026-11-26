---
title: "Hashrate Hijacking: 1.051 Situs Mining Dibajak dalam Satu Detik Lewat Rute BGP Palsu"
description: "Laporan forensik Braiins: rute BGP more-specific mengalihkan miner Stratum V1 ke pool palsu — sampai 1,9 EH/s, tanpa menyentuh ASIC atau pool."
date: 2026-11-26T18:10:00+07:00
draft: false
tags: ["Bitcoin", "Mining", "Keamanan", "Stratum", "BGP", "Infrastruktur"]
---

Pada **20 November 2026**, lebih dari seribu situs mining kehilangan koneksi ke pool mereka **dalam detik yang sama**. Mesin tetap berputar penuh, panel miner bilang pool hidup — tapi dashboard pool mencatat hashrate nol. Tidak ada ASIC yang diretas maupun pool yang ditembus. Yang dipalsukan cuma **rute internetnya**.

## 📉 Tiga gelombang, dua benua

Braiins merilis laporan forensik pada **25 November 2026**. Polanya:

- **7–12 November** — Amerika Latin, terutama Brasil dan Argentina. 19 episode, 120–400 situs, 36–174 PH/s, durasi 1,5 menit sampai 3 jam.
- **20 November** — mayoritas Eropa. 4 episode, **1.050–1.600 situs**, 0,6–1,9 EH/s, 6–49 menit.

Dalam dua minggu, hashrate yang dibajak naik dari di bawah **175 PH/s** ke **1,9 EH/s** — sekitar 1 dari 550 tebakan seluruh jaringan Bitcoin. Attacker berganti metode dan pindah benua. Braiins menyebutnya *testing the waters*.

## 🛣️ BGP: rambu jalan yang bisa dicat siapa saja

Internet adalah kumpulan jaringan yang saling memberi tahu alamat IP mana yang bisa dijangkau lewat **BGP**. Masalahnya, BGP berjalan di atas kepercayaan: siapa pun di jalur bisa memasang rambu, dan router mengikuti rambu yang **paling spesifik**.

Alamat Stratum pool berada di blok **/20 berisi 4.096 alamat**. Penyerang mengumumkan blok lebih kecil, **/24 berisi 256 alamat**, dan di dalamnya ada alamat pool. Blok lebih spesifik menang, jadi trafik miner dialihkan ke server penyerang.

Jaringan yang memvalidasi lewat **RPKI** menolak rute palsu itu — tapi banyak yang tidak. Dan pengumuman palsu mencantumkan **pemilik asli sebagai origin**, jadi pemantau yang cuma memeriksa origin tidak menyalakan alarm.

## 🎭 Yang dilihat miner: semuanya normal

Urutannya konsisten di 12 merek firmware berbeda:

1. Koneksi pool di-reset serentak pada detik yang sama. Pool asli tidak menerima apa pun; sesinya baru timeout dua menit kemudian.
2. Miner menyambung ulang ke **hostname dan IP yang sama**. DNS tidak disentuh — ini bukan DNS spoofing.
3. Server lain yang menjawab: dari Brasil handshake-nya 30 ms, padahal pool asli 280 ms. Ia menerima username dan password apa saja.
4. Server itu mengirim **job mining asli** dari pool publik besar lain, dengan tag dan payout pool itu, lalu menyetor share ke akun penyerang. Difficulty naik sampai **536.870.912** — Braiins Pool tidak pernah menyetel di atas 16.777.216.

Miner melaporkan hashrate normal, suhu normal, pool hidup. Hanya dashboard pool yang jujur. Satu miner sempat failover ke pool cadangan, lalu balik ke pool palsu dua menit kemudian karena terlihat stabil.

## 💰 Uangnya kecil, pesannya bukan soal uang

CoinDesk memperkirakan pendapatan terdampak **di bawah US$17.000**. Untuk 1,9 EH/s itu remeh — episodenya pendek dan payout lewat ambang pool. Justru itu intinya: ini bukan perampokan, tapi uji mekanisme — apakah ribuan mesin bisa dibelokkan sekaligus tanpa ketahuan.

## 🛡️ Checklist yang harus dikerjakan sekarang

Untuk miner:

- Tidak boleh ada entri pool berawalan **`stratum+tcp://`** — termasuk pool cadangan.
- Pakai **Stratum V2**: URL-nya membawa public key pool, dan miner menolak server yang tidak bisa membuktikan punya private key pasangannya.
- Kalau belum bisa V2, pakai **Stratum V1 over TLS** — tapi hanya jika firmware benar-benar **memverifikasi sertifikat**. Braiins menguji 7 firmware: dua punya opsi TLS tapi menerima sertifikat tidak valid. TLS tanpa verifikasi sama saja koneksi terenkripsi ke pencuri.
- Firmware tanpa TLS dan V2 bisa lewat **proxy SV2** di LAN: miner bicara V1 ke proxy, proxy bicara V2 ke pool.
- Deteksi: cari reset koneksi yang diikuti difficulty ratusan juta, dan periode miner ber-hash tapi dashboard pool kosong.

Untuk pool: sediakan port TLS-only dengan sertifikat otoritas publik, periksa alamat sendiri di **RIPE RIS** atau **RouteViews** sejak 1 November, dan minta provider mengumumkan **/24** berisi endpoint Stratum dengan ROA RPKI terbatas pada prefix itu.

## 🧠 Ini bukan masalah mining

Stratum V1 lahir 2012, mengirim data sebagai teks polos, dan miner tidak bisa memastikan lawan bicaranya. Pada 2014 SecureWorks sudah mendokumentasikan trik routing yang sama (US$83.000); pada 2020 Braiins menulis peringatannya. Industri menganggapnya langka — sampai minggu lalu.

Polanya akrab: protokol teks polos yang membawa uang, ditambah routing yang percaya pada pengumuman siapa pun. Kita sudah menulis soal serupa di [Zero Trust untuk MCP](/posts/zero-trust-mcp-82-tool-tanpa-token/) dan [Chainflip: US$12 juta dari satu signature](/posts/chainflip-12-juta-satu-signature-sah/). Bedanya, di sini yang dipalsukan bukan kredensial atau signature, melainkan **alamat tujuan** itu sendiri.

## 🐷 Kesimpulan

Braiins tidak kehilangan ASIC dan tidak ditembus. Yang bocor adalah asumsi: bahwa koneksi ke "pool.example.com" benar-benar sampai ke pool.example.com. Selama jalurnya teks polos dan identitas server tidak diverifikasi, asumsi itu tak punya dasar teknis.

Kalau kamu menjalankan miner — atau sistem apa pun yang bicara ke server tanpa autentikasi — pertanyaannya: **kalau server di ujung sana diganti orang lain, apa yang membuat sistemmu menolak?** Kalau jawabannya "tidak ada", konfigurasi itu belum selesai.

**Sumber:** [Braiins — Security Alert Stratum V1](https://braiins.com/blog/bitcoin-hashrate-hijacking-unencrypted-stratum-v1), [CoinDesk](https://www.coindesk.com/markets/2026/11/26/hackers-hijacked-1-000-plus-bitcoin-mines-in-one-second-by-faking-internet-routes), [The Block](https://www.theblock.co/news/ecosystems/2026-11-25-bitcoin-miners-hit-hashrate-hijacking-attack-exploiting-unencrypted-connections-446723).

**Baca juga:** [Difficulty Bitcoin Naik, Ongkos Listrik Miner Ikut Naik](/posts/difficulty-bitcoin-naik-ongkos-listrik-miner/) · [Bitcoin di Bawah Biaya Mining: Hashrate Rekor November 2026](/posts/bitcoin-bawah-biaya-mining-hashrate-rekor-november-2026/)

— Chokdi 🐷 · Content Studio · 2026
