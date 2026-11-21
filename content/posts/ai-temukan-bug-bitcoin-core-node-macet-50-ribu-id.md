---
title: "AI Temukan Bug Bitcoin Core: Cukup Ulang 1 ID Transaksi 50.000 Kali, Node Berhenti Kerja"
description: "Bitcoin Core merilis 30.5 dan 31.3 untuk menambal CVE-2026-117348 — bug 'medium' yang ditemukan otomatis oleh Project Loupe milik Spiral/Block. Satu pesan inv berisi wtxid yang sama 50.000 kali bisa membuat node berhenti memproses blok lebih dari belasan detik."
date: 2026-11-21T17:18:00+07:00
draft: false
tags: ["Bitcoin", "Bitcoin Core", "Keamanan", "AI", "Crypto"]
---

Sabtu, 21 November 2026 — Di tengah pasar crypto yang berdarah (BTC sekitar US$57.600, turun 6–7% dalam 24 jam menurut data CoinDesk), ada berita teknis yang jangka panjangnya lebih penting daripada harga: **Bitcoin Core merilis versi 30.5 dan 31.3 pada Jumat, 20 November 2026**, menambal **CVE-2026-117348** — bug yang ditemukan bukan oleh manusia, tapi oleh **pemindaian otomatis LLM** lewat Project Loupe, proyek open-source di bawah Spiral, unit pengembangan milik Block (perusahaan Jack Dorsey).

Severity-nya cuma "medium". Tapi cara kerjanya bikin geli: cukup satu transaksi, diumumkan berulang-ulang.

## 🐛 Satu ID, Diulang 50.000 Kali

Sejak versi 29.0, Bitcoin Core menyimpan transaksi "orphan" — transaksi yang parent-nya belum pernah dilihat node — di orphanage, lalu bertanya ke peer tentang parent yang hilang. Ketika peer mengumumkan transaksi yang ada di orphanage, node menyusun daftar parent yang hilang dan mengecek masing-masing ke mempool dan filter transaksi yang baru dilihat.

Masalahnya: satu pesan `inv` bisa membawa sampai **50.000 entri**, dan Core tidak melewati entri duplikat. Penyerang bisa mengirim satu orphan dengan ribuan parent yang tidak ada, lalu mengirim pesan `inv` berisi wtxid transaksi itu **50.000 kali**. Node mengulang pengecekan mahal yang sama, terus-menerus.

Kutipan advisory resminya: *"Each such message stalls the node for over a dozen seconds"* — setiap pesan seperti itu membuat node berhenti memproses pesan dari peer lain **lebih dari belasan detik**, termasuk blok baru. Kirim pesan tambahan, dan gangguannya bisa diperpanjang sesuka hati.

## ⛔ Bukan Dana Hilang, Tapi Node Berhenti

Ini bukan bug konsensus, bukan bug yang bisa mencetak bitcoin dari udara. Tidak ada dana pengguna yang bisa dicuri. Yang diserang adalah **availability**.

Konsekuensi praktisnya tetap nyata:

- **Exchange** yang mengandalkan node terpengaruh bisa terlambat mengkredit deposit.
- **Miner** bisa membuang komputasi untuk pandangan blockchain yang sudah basi.
- Node publik yang jadi pintu masuk pengguna bisa "diam" tanpa error yang jelas.

## 🩹 Versi: Siapa yang Wajib Update

Advisory Bitcoin Core menyebut:

- **Diperbaiki di:** 32.1, 30.5 dan 31.3.
- **Terpengaruh:** 29.0–29.5, 30.0–30.4, dan 31.0–31.2.
- **29.x sudah end-of-life** — tidak akan menerima perbaikan sama sekali. Kalau node kamu masih di 29.x, tidak ada patch yang akan datang; harus pindah major.

Perbaikannya sederhana dan elegan: setiap transaksi yang diumumkan dalam satu pesan `inv` diproses **hanya sekali**.

## 🤖 Kenapa AI yang Menemukan, Bukan Manusia

Timeline lengkapnya menarik:

- **8 Juli 2026** — Project Loupe melaporkan isu ini (hasil scan LLM otomatis, dipimpin Elias Rohrer di Spiral).
- **4 Agustus 2026** — peneliti independen "Stutxo" melaporkan hal yang sama.
- **6 Agustus 2026** — PR #35878 dari Gregory Sanders (yang memvalidasi temuan Loupe) di-merge ke master.
- **27 Oktober 2026** — Bitcoin Core 32.1 rilis dengan perbaikan.
- **17 November 2026** — perbaikan di-backport ke cabang 31.x dan 30.x.
- **20 November 2026** — 30.5 dan 31.3 rilis, plus **pengungkapan publik di hari yang sama**.

Yang terakhir itu bukan kebetulan. Pada 22 Oktober 2026 Bitcoin Core mengubah kebijakan keamanannya: bug yang dinilai **"easily discoverable"** — dalam praktiknya, bisa ditemukan dengan satu prompt ke LLM — langsung diperbaiki di semua versi yang masih didukung dan diumumkan secepat mungkin, tanpa embargo berbulan-bulan.

Alasannya jujur. Antoine Poinsot dari Chaincode Labs menulis: *"We recently experienced an increase in the number of reports for security vulnerabilities that can be easily (re-)discovered"* — dan penyebab utamanya, *"LLMs drastically reducing the bar to find certain classes of issues."*

Skalanya sudah kelihatan sejak musim panas: kelompok relawan **Bitcoin Red Team** (16 developer) menjalankan model AI ke **390 proyek bitcoin** dalam sekitar satu hari pada akhir Juli 2026 dan mencatat **4.962 temuan, 85 di antaranya kritis**. Beberapa hari kemudian, celah BTCPay Server yang dilaporkan secara privat sudah dieksploitasi di server merchant sungguhan. Bug Coldcard yang tidur sejak 2021 menguras **594 BTC dalam 25 menit**.

Konsekuensi kebijakan baru ini juga ada harganya: Poinsot mengakui perbaikan cepat "tidak punya waktu bake time yang sama" dalam pengujian sebelum sampai ke pengguna.

## ✅ Yang Perlu Kamu Lakukan

1. **Cek versi node:** `bitcoind --version` atau `bitcoin-cli getnetworkinfo`.
2. **Upgrade:** ke 30.5, 31.3, atau 32.1 — pilih sesuai major yang sedang dipakai, jangan lompat major tanpa alasan.
3. **Kalau masih 29.x:** wajib pindah major. Tidak ada patch untuk seri itu.
4. **Exchange, pool, dan miner:** prioritaskan. Delay kredit deposit dan kerja di chain view basi = kerugian nyata.
5. **Anggap detailnya sudah publik.** Advisory lengkap sudah terbit; siapa pun bisa membaca mekanismenya sekarang.

## 💭 Penutup

Selama ini keamanan open-source bertumpu pada satu asumsi: bug aman selama belum ada yang menemukannya, dan menemukan bug itu mahal. AI mematahkan asumsi kedua. Bitcoin Core memilih beradaptasi — ungkap lebih cepat, patch lebih cepat, terima risiko testing yang lebih tipis. Untuk operator node, pelajarannya sederhana dan tidak nyaman: **versi yang kamu jalankan kemarin bisa jadi versi yang rapuh hari ini**.

**Sumber:** CoinDesk (21 Nov 2026) · Advisory Bitcoin Core CVE-2026-117348 (20 Nov 2026) · Project Loupe (GitHub) · YouTube: "Project Loupe — AI powered security scanning for Bitcoin OSS", Elias Rohrer, bitcoin++ Berlin, 2 Okt 2026.

**Baca juga:** [Bitcoin Jebol US$58 Ribu: Cuma 2% dari Low 2026, US$1,5 Miliar Posisi Likuidasi, Pasar Lari ke Cash](https://chokdi.ano99.com/posts/bitcoin-58-ribu-dua-persen-dari-low-2026/) · [Bitcoin Jebol US$75.000: Support yang Disebut Minggu Lalu Akhirnya Ambruk, Sempat Sentuh US$73.750](https://chokdi.ano99.com/posts/btc-jebol-support-75-ribu-november-2026/) · [Bitcoin Jebol di Bawah US$70.000: Terendah 12 Minggu, Enam Pekan Merah Berturut-turut](https://chokdi.ano99.com/posts/bitcoin-bawah-70-ribu-terendah-12-minggu-november-2026/)

— Chokdi 🐷 · Content Studio · 2026
