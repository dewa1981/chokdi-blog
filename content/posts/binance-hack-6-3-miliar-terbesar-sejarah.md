---
title: "Binance Kena Hack $6,3 Miliar: Rekor Perampokan Kripto Terbesar dalam Sejarah"
date: 2026-10-31T17:30:00+07:00
draft: false
tags: ["Crypto", "Binance", "Keamanan", "Korea Utara", "Bitcoin"]
---

Malam 29 Oktober 2026, mulai pukul 20:05 UTC (03:05 WIB), sesuatu yang belum pernah terjadi dalam sejarah kripto berjalan. Dalam hitungan menit, dompet-dompet Binance di **sepuluh blockchain** mengirim saldo keluar ke alamat yang dikendalikan satu pihak. Binance menyebut dampaknya sekitar **$6,3 miliar**; TRM Labs menghitung **$6,36 miliar** — kasar **Rp 105 triliun**.

Sebagai pembanding, ini sekitar **empat kali lipat** hack Bybit ($1,5 miliar) Februari 2025. Chainalysis dan TRM Labs sepakat: pencurian kripto terbesar yang pernah tercatat. BBC menyebutnya pencurian tunggal terbesar sepanjang sejarah.

## 🧨 Apa yang Sebenarnya Terjadi

Intinya ada di satu hot wallet bernama **Binance 14**. Sekitar pukul 20:24 UTC, dompet itu mengirim **167.464 ETH**, lebih dari **1,6 miliar USDT**, dan puluhan token lain dalam satu tarikan transaksi.

Mekanismenya:

- Di Ethereum, penyerang memakai **delegasi EIP-7702** untuk mengubah hot wallet Binance jadi *sweeper* yang dia kendalikan — dengan **50 otorisasi yang sudah ditandatangani lebih dulu**.
- Di sembilan chain lain (XRP Ledger, Bitcoin, Tron, Solana, dan lainnya), dompet Binance mengirim dana lewat transfer bertanda tangan biasa.
- Ada **gelombang kedua sekitar 23:05 UTC** yang menyapu dompet Binance di Avalanche dan Polygon.

Binance bilang tidak ada private key yang bocor. Dugaan awal: **laptop seorang engineer DevOps** diambil alih penyerang, lalu dipakai masuk ke sistem internal.

## 💸 Angka-angkanya

Per blockchain menurut TRM Labs:

- **Ethereum ~$3,79 miliar** — 200.630 ETH plus 185 token lain, termasuk 1,875 miliar USDT dan 823 juta USDC
- **Bitcoin 18.270 BTC** — sekitar $1,47 miliar
- **Tron** — 612,7 juta USDT (~$628 juta)
- **XRP Ledger** — 233,46 juta XRP (~$296 juta), **Solana** 970.500 SOL (~$96 juta)
- Sisanya tersebar di Arbitrum, Optimism, Base, Avalanche, Polygon (~$77 juta)

Yang paling penting bukan besarannya, tapi **kecepatannya**: sekitar 20 menit untuk 10 chain.

## 🧊 Yang Berhasil Dibekukan (dan Yang Lolos)

Tether membekukan ~$1,57 miliar, Circle lebih dari $800 juta, Ripple ~$200 juta, World Liberty Financial lewat BitGo ~$29 juta, dan Arbitrum Security Council 8.426 ETH plus 74,6 juta ARB. Totalnya sekitar **$2,7 miliar** — sekitar 43% dari yang dicuri.

Tapi penyerang balapan: menjual USDT ke market maker dan meminjam ETH dengan jaminan USDT di Aave. Sekarang dia memegang **lebih dari 420.000 ETH dan 18.270 BTC** — sekitar **$2,4 miliar** yang sudah di luar jangkauan penerbit stablecoin mana pun.

## 🇰🇵 Kenapa Semua Mata ke Korea Utara

TRM Labs menuding **TraderTraitor**, unit hacker elite Korea Utara, dengan keyakinan tinggi. Polanya mirip serangan sebelumnya: penarikan kecil lewat Tornado Cash untuk mendanai dompet operator, staging yang jalan jauh sebelum eksekusi, lalu tanda tangan dikumpulkan dulu dan dieksekusi sekali gebrak — persis Bybit 2025 dan KelpDAO April 2026. Menurut rangkuman CoinGabbar, Korea Utara kini menanggung sekitar **89% kerugian hack kripto 2026**. Uangnya, kata narasumber BBC, antara lain untuk membiayai program militer dan misil.

## 🇮🇩 Efeknya ke Kita di Indonesia

- **Indodax**, exchange kripto terbesar RI yang diawasi OJK, **menghentikan sementara deposit dan penarikan** rupiah maupun kripto sejak 29 Oktober, setelah mendeteksi "peningkatan upaya serangan siber". CEO William Sutanto mengumumkan langsung. Jadi risikonya bukan cuma di exchange global.
- **Bitcoin jatuh lebih dari 3% ke $76.368** — terendah enam minggu. Ethereum ke $2.178, BNB turun 5% ke ~$709. Hari ini BTC di kisaran **$77.200–$77.400**, dan **Fear & Greed Index 30 (Fear)**, turun dari 51 minggu lalu dan 74 bulan lalu.

Tim Sun, peneliti senior HashKey Group, menyebut insiden ini bisa "semakin menekan selera risiko dan memaksa investor menilai ulang keamanan aset di exchange terpusat". Bernardo Brites (Trace Finance) lebih blak-blakan: *"Semakin sulit menahan hack karena AI bisa menemukan celah lebih cepat daripada kemampuan kita memperbaikinya."*

Dari sisi Binance: co-founder Yi He bilang perusahaan menanggung "semua kerugian hacking" lewat **SAFU** dan dana perusahaan, withdrawal dibuka bertahap, dan **Proof of Reserves** baru dipublikasikan setelah remediasi.

## ✅ 5 Poin Praktis

1. **Jangan panic sell, jangan panic buy.** Tunggu withdrawal dibuka dan PoR baru keluar.
- **Baca Proof of Reserves**, bukan iklan "aman".
3. **Pisahkan fungsi.** Exchange buat trading, hardware wallet buat simpanan panjang. 420.000 ETH yang lolos itu buktinya.
4. **Waspada musim scam.** Tiap hack besar diikuti phising "refund Binance" dan grup Telegram "pemulihan dana". Semua penipuan.
5. **Untuk exchange lokal, pantau kanal resmi.** Status Indodax cuma sah dari akun dan situs resmi mereka — bukan screenshot yang diteruskan di WhatsApp.

## Kesimpulan

Hack Binance ini tiga pelajaran sekaligus: kustodi terpusat tetap punya titik lemah manusia (satu laptop engineer), eksekusi sekarang dihitung dalam menit bukan hari, dan pembekuan aset oleh penerbit stablecoin memang bekerja — tapi cuma untuk sebagian, karena penyerang makin paham cara menghindarinya.

Buat kita di Indonesia, sinyal paling praktis bukan harga Bitcoin hari ini, tapi pengumuman Indodax dan wajah baru industri kustodi setelah kejadian ini. Kalau exchange sebesar Binance — 335 juta pengguna terdaftar, $162,8 miliar aset kustodian — bisa kehilangan $6,3 miliar dalam 20 menit, asumsi "exchange besar pasti aman" perlu diuji ulang.

— Chokdi 🐷 · Content Studio · 2026
