---
title: "MDR QRIS 0% Mulai 1 Oktober 2026: Ongkos Sebenarnya Deposit Rp10 Ribu sampai Rp500 Ribu"
description: "BI memperluas MDR QRIS 0% mulai 1 Oktober 2026. Ini hitungan ongkos nyata per ukuran deposit: batas MDR, limit dompet digital, dan ongkos jaringan USDT."
date: 2026-10-13T00:10:00+07:00
draft: false
tags: ["QRIS", "MDR", "Payment Gateway", "Deposit", "USDT", "Operasional"]
---

# MDR QRIS 0% Mulai 1 Oktober 2026: Ongkos Sebenarnya Deposit Rp10 Ribu sampai Rp500 Ribu

Mulai **1 Oktober 2026**, Bank Indonesia memperluas kebijakan **MDR QRIS 0 persen** ([Siaran Pers BI](https://www.bi.go.id/id/publikasi/ruang-media/news-release/Pages/sp_2815926.aspx)). Kalau bisnismu hidup dari deposit kecil — Rp5.000, Rp10.000, Rp50.000 — ini kabar bagus. Tapi kalau kamu menyimpulkan "biaya deposit sudah nol", ada dua hal yang belum masuk hitungan: **limit di sisi dompet digital** dan **ongkos jaringan** kalau jalurnya crypto. Artikel ini membedah ongkos tiap jalur per ukuran tiket, pakai angka resmi BI, DANA, dan data fee jaringan.

## Apa yang sebenarnya berubah 1 Oktober 2026

Sebelumnya, MDR 0 persen cuma milik merchant **Usaha Mikro (UMI)** dengan plafon transaksi tertentu. Sekarang perluasannya dua lapis:

| Kategori merchant | Nilai transaksi | MDR |
|---|---|---|
| **Semua kategori** (UMI, UKE, UME, UBE) | ≤ Rp100.000 per transaksi | **0%** |
| Usaha Mikro (UMI) | ≤ Rp500.000 per transaksi | **0%** |
| UMI | > Rp500.000 | 0,3% |
| UKE / UME / UBE | > Rp100.000 (di atas plafon baru) | 0,7% |
| Pendidikan / SPBU | — | 0,6% / 0,4% |

Dua catatan yang gampang terlewat. Pertama, **MDR ditanggung merchant dan tidak boleh dibebankan ke konsumen** — itu aturan BI, bukan kebijakan opsional ([penjelasan MDR QRIS BI](https://www.bi.go.id/id/publikasi/ruang-media/cerita-bi/Pages/mdr-qris.aspx)). Kedua, MDR 0 persen **bukan** berarti semua transaksi QRIS bebas biaya: di atas plafon, tarif normal jalan lagi, dan biaya admin dari layanan lain bisa tetap muncul ([detikJatim, 2 Okt 2026](https://www.detik.com/jatim/berita/d-8689705/apa-itu-mdr-qris-ini-aturan-biaya-admin-yang-berlaku-oktober-2026)).

## Hitungan per ukuran tiket

Ini angka yang paling praktis, memakai tarif UKE/UME/UBE (0,7%) sebagai pembanding sebelum perluasan:

| Tiket deposit | MDR sebelum plafon baru | MDR sekarang |
|---|---|---|
| Rp10.000 | Rp70 | **Rp0** |
| Rp50.000 | Rp350 | **Rp0** |
| Rp100.000 | Rp700 | **Rp0** |
| Rp500.000 | Rp3.500 | Rp3.500 (UMI: Rp0) |
| Rp1.000.000 | Rp7.000 | Rp3.000–Rp7.000 |

Artinya: untuk brand yang tiket dominannya **≤Rp100.000**, perluasan ini langsung memangkas biaya per deposit — selisihnya bisa dipakai menambah bonus kecil atau menahan biaya promosi. Untuk tiket Rp500.000 ke atas, biaya MDR masih ada dan wajib dihitung di model bonus, bukan diabaikan.

## Yang lebih sering bikin "deposit gagal": limit dompet, bukan gateway

Di lapangan, kegagalan deposit jarang karena QRIS-nya rusak. Yang lebih sering muncul adalah **limit akun pengirim** di dompet digital. Contoh resmi dari DANA:

- **DANA Basic** (belum verifikasi KYC): limit **Rp2.000.000 per transaksi**, dan uang masuk maksimal **Rp20.000.000 per bulan**.
- **DANA Premium** (KYC + selfie KTP): limit **Rp20.000.000 per transaksi**, uang masuk maksimal **Rp40.000.000 per bulan** ([DANA Blog](https://www.dana.id/blog/simpan-uang-di-dana-maksimal-berapa/)).

Konsekuensinya untuk operasional: pemain yang mau setor Rp5 juta dari akun Basic **tidak akan pernah berhasil**, seberapa mulus pun sistem kita. Edukasi "upgrade ke akun Premium" jauh lebih murah daripada menambah tiket bantuan CS. Di sisi pencatatan, masalah berikutnya bukan uangnya, tapi **mencocokkan uang ke member dan brand yang benar** — mekanisme kode unik dan pemisahan brand per kode pembayar saya bahas di [QRIS Kode Unik: Bikin Depo Terbaca Otomatis Tanpa Ketuker Brand](/posts/qris-kode-unik-depo-otomatis-multibrand/).

## Jalur crypto: ongkosnya di jaringan, bukan di gate

Kalau jalur yang dipakai USDT, tidak ada MDR — tapi ada fee jaringan yang **untuk tiket kecil justru jauh lebih besar dari nilai depositnya**. Angka tipikal 2026 ([Plisio](https://plisio.net/crypto/usdt-transfer-fee), kurs Rp17.900/USD):

| Rail | Fee khas | Waktu | Fee sebagai % dari deposit Rp10.000 |
|---|---|---|---|
| Tron (TRC-20), tanpa energy | $1,44–2,89 (Rp26rb–52rb) | ~3 detik | **258%–517%** |
| BNB Smart Chain (BEP-20) | ~$0,10 (Rp1.790) | ~3 detik | ~18% |
| Solana / Polygon / TON | $0,0002–0,05 | 1–5 detik | ~0% |
| Ethereum (ERC-20) | $0,20–2,00 (bisa >$10 saat padat) | ~12 detik | 4%–>100% |

Perhatikan baris pertama: mengirim USDT TRC-20 untuk setoran **Rp10.000 sama dengan membakar 3–5 kali nilai setorannya**. Kalau jalur ini memang harus dipakai, stake TRX untuk energy atau pilih BEP-20/Solana. Tambahan yang sering lupa dihitung: exchange biasanya menambah **markup penarikan $0,30–$25** di atas fee on-chain itu.

## Aturan praktis yang saya pakai

1. **Tiket ≤ Rp100.000 → QRIS.** MDR-nya 0 persen sekarang, dan jangan sekali-kali membebankan biaya itu ke pemain.
2. **Rp100.000–Rp2.000.000 → QRIS atau e-wallet**, tapi pastikan pengirim sudah akun terverifikasi (limit, bukan gateway, yang jadi penghalang).
3. **Nominal besar atau lintas negara → USDT**, dengan rail yang dipilih sesuai ukuran tiket — bukan default TRC-20. Latar belakang kenapa industri judi bergerak ke jalur on-chain ada di [LP Judol & Blockchain](/posts/lp-judol-blockchain-pembayaran-usdt/).
4. **Catat fee sebagai baris biaya.** Kalau biaya jaringan "hilang" di laporan, kamu tidak akan pernah tahu deposit kecil mana yang sebenarnya merugi. Untuk brand dengan tiket receh, soal margin per deposit saya pernah bedah di [Situs Slot Deposit 5000](/posts/slot-gacor-deposit-5000-2026/).

Perluasan MDR 0 persen ini menutup satu lubang biaya — tapi hanya untuk tiket di bawah Rp100.000 dan hanya kalau jalur pembayarannya dipilih dengan benar. Sisanya tetap kerjaan operasional: mana rail untuk tiket berapa, dan siapa yang menanggung selisihnya.

Kalau kamu mengelola deposit di beberapa brand sekaligus, bagian mana yang paling sering bocor di tempatmu — fee jaringan, limit akun, atau pencocokan uang ke member? Tulis di komentar.

— Chokdi 🐷 · Content Studio · 2026
