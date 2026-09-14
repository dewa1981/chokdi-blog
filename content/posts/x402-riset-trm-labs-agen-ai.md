---
title: "Riset TRM Labs: Belanja Agen AI On-Chain Cuma 0,6–7,5% dari Volume x402"
date: 2026-09-14T12:20:00+07:00
draft: false
tags: ["AI", "Crypto", "Riset"]
---

Narasi "agen AI mulai belanja sendiri pakai kripto" terdengar keren — tapi riset TRM Labs yang terbit 9 September 2026 bilang realitasnya jauh lebih kecil dari hype. Dari US$52,7 juta yang mengalir lewat x402, hanya **0,6% sampai 7,5%** yang benar-benar terlihat seperti dibayar agen AI.

## Apa Itu x402 dan Kenapa Ramai Dibahas

x402 adalah protokol yang menghidupkan lagi status code HTTP `402 Payment Required` sebagai langkah pembayaran sungguhan. Alurnya sederhana:

1. Pembeli (bisa agen, bisa script biasa) minta sebuah resource ke server.
2. Server balas `402` beserta harga.
3. Pembeli mengirim ulang request dengan otorisasi yang ditandatangani.
4. Sebuah *facilitator* memverifikasi, menyiarkan settlement on-chain, dan menanggung gas.

Karena pembayaran jadi bagian dari request software — bukan checkout yang dilihat manusia — x402 sering diangkat sebagai "rel" ekonomi agen AI. TRM Labs mencatat ada empat standar yang bersaing di ruang ini: **AP2** dari Google, **ACP** dari OpenAI + Stripe, **MPP** dari Stripe + Tempo, dan **x402** sendiri.

## Angka Besarnya: US$52,7 Juta dari 198,9 Juta Transaksi

Menelusuri Base, Solana, dan Polygon sejak Mei 2025, TRM menemukan sekitar **US$52,7 juta** dana tersettle melalui facilitator x402 yang dikenal — tapi tersebar di **198,9 juta transaksi settlement**. Artinya nilai rata-rata per transaksi jauh di bawah satu dolar. Ini bukan aliran uang besar; ini aliran mikro yang jumlahnya luar biasa banyak.

## Setelah Difilter, Setengahnya Hilang

TRM tidak langsung percaya angka itu. Mereka menyaring tiga hal:

- pembayaran ke alamat sendiri (*self-payment*),
- aliran besar dari satu atau dua pembayar saja,
- penjual yang punya kurang dari sepuluh pembeli berbeda.

Hasilnya: sekitar **separuh volume langsung rontok**, menyisakan **US$25,62 juta** yang layak disebut "commerce". Dua saringan terakhir itu sengaja dibuat sebagai penanda anomali — menghapus arus yang terlalu terkonsentrasi atau terlalu sepi.

## Yang Benar-Benar dari Agen: 0,6%–7,5%

Pertanyaan berikutnya lebih pelik: dari commerce yang tersisa, berapa yang benar-benar dari agen? Masalahnya, on-chain tidak bisa membedakan agen dengan script terjadwal — jejaknya identik. Jadi TRM tidak menetapkan satu angka, melainkan memberi batas atas dan bawah:

- **Tes permisif**: hitung semua pembayar yang "mungkin" agen — dibayarkan via facilitator, nominal rata-rata sub-dolar, dan harga bervariasi, bukan berulang di angka yang sama.
- **Tes ketat**: hanya yang polanya bertahan berbulan-bulan *dan* terdaftar di registry agen publik (ERC-8004) *atau* membayar lebih dari satu penjual.

Hasilnya: **0,6% hingga 7,5%**. TRM mengakui tes ini bisa meremehkan — banyak agen hari ini mungkin memang single-purpose dan membayar satu layanan secara berulang, sehingga terbaca seperti script.

## Hampir Semua Bayar Pakai USDC

Satu temuan yang paling tegas justru soal asetnya:

| Metrik | Angka |
|---|---|
| Total nilai x402 | US$52,68 juta |
| Yang settled dalam USDC | US$52,47 juta (**99,6%**) |
| Nilai setelah difilter | US$25,62 juta |
| Perkiraan porsi agenik | 0,6% – 7,5% |
| Volume bulanan agen (2026) | ±US$5.000 – 11.000 |

Selain itu, komposisi merchant-nya berubah drastis sepanjang 2025–2026: akhir 2025 didominasi spekulasi dan mint meme-token, paruh pertama 2026 menumpuk di satu kontrak pembayaran, lalu pertengahan 2026 layanan AI kembali — kali ini lewat *agent-payment router*, bukan satu toko tunggal.

## Kenapa Sulit Membuktikan "Itu Agen"

Menurut TRM, ada tiga hal yang bikin atribusi pembayaran agen rusak:

- **Klaim kepemilikan tidak diverifikasi.** Registry agen on-chain bersifat sukarela dan mayoritas peserta belum memakainya.
- **Tidak ada manusia yang menyetujui.** Agen menandatangani, facilitator menyiarkan, tidak ada jeda review. Kontrol yang mengasumsikan keputusan manusia tidak punya tempat untuk duduk.
- **Nilai dan jumlah terpisah.** Transaksi ini ada di bawah hampir semua ambang nilai *dan* di atas hampir semua ambang jumlah — kontrol yang dikalibrasi untuk manusia melewatkannya dari dua arah sekaligus.

## Apa Artinya untuk Kita

Kalau Anda developer yang sedang membangun monetisasi API berbayar, kesimpulannya praktis: traffic agen bukan traffic pelanggan biasa. Endpoint harus machine-readable, harga per panggilan, dan bisa ditemukan tanpa manusia melihat halaman. Untuk yang menekuni sisi kripto, lihat juga catatan kami soal [agen AI yang mulai jadi pengguna stablecoin](https://chokdi.ano99.com/posts/ai-agent-pengguna-crypto-stablecoin/) dan [analisis wallet pakai AI](https://chokdi.ano99.com/posts/5-ai-analisis-wallet-kripto/).

Kalau Anda ingin memeriksa sendiri data on-chain-nya, pola yang kami tulis di [Alchemy CLI: 12 hal on-chain cukup satu perintah](https://chokdi.ano99.com/posts/alchemy-cli-12-hal-on-chain-satu-perintah/) bisa dipakai untuk mulai menelusuri alamat facilitator.

## Kesimpulan

Rel-nya sudah jalan — x402, AP2, ACP, MPP semua sudah hidup. Yang belum ada adalah infrastruktur yang bisa membuktikan siapa yang sebenarnya membayar. TRM Labs menutup laporannya dengan kalimat yang layak ditempel di dinding: *"Agentic commerce will need agentic compliance."* Angka US$52,7 juta boleh terlihat besar di headline, tapi setelah difilter, ekonominya masih kecil dan didominasi USDC — sekitar US$5.000 sampai 11.000 per bulan.

Kalau menurut Anda porsi 0,6% itu realistis atau justru terlalu pesimis, tulis di kolom komentar. Data on-chain selalu bisa dibantah dengan data on-chain juga — dan itu justru bagian yang menarik.

— Chokdi 🐷 · Content Studio · 2026
