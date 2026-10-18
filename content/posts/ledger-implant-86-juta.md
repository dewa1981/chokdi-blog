---
title: "Ledger Rp1,4 Triliun Raib: Implan LTE di Dalam Dompet, Genuine Check Tetap Lolos"
date: 2026-10-19T01:05:00+07:00
draft: false
tags: ["Crypto", "Keamanan", "Hardware Wallet", "Ledger", "Supply Chain"]
---

Dompet hardware dijual sebagai kotak besi yang tidak bisa disentuh siapa pun dari jauh. Tanggal 9 Oktober 2026 anggapan itu jebol untuk ratusan orang di Asia Tenggara: saldo kosong beruntun, dan analis on-chain menghitung **lebih dari 86 juta dolar** (sekitar Rp1,4 triliun) sudah pindah ke segelintir alamat penampung.

Yang bikin kasus ini penting buat kamu bukan angka besarnya, tapi **cara uangnya hilang**: bukan Ledger yang diretas, bukan firmware yang bocor. Yang diserang adalah jalur perjalanan perangkat dari pabrik ke tangan pembeli — persis jalur yang kita semua anggap paling aman.

## 💥 Apa yang terjadi 9 Oktober

Semua dimulai dari laporan pengguna di X dan Reddit yang dompetnya tiba-tiba kosong. Pukul 12:24 UTC, investigator anonim **Specter** mempublikasikan sepuluh alamat penampung di Bitcoin, Ethereum, dan Tron dan menyebut angka **>$86 juta**. Analis lain, tanuki42, menghitung >$72 juta; MistTrack hampir $90 juta; Bitquery belakangan menyebut **$92,9 juta dari 311 wallet di lima blockchain**.

Pukul 13:32 UTC, akun support Ledger akhirnya bersuara: mereka menyelidiki laporan kerugian dari pengguna Asia Tenggara yang membeli produk dari **CryptoBilis**, reseller resmi di Kuala Lumpur yang melayani **Indonesia, Malaysia, dan Filipina**. Semua penjualan dan pengiriman CryptoBilis langsung dihentikan.

Pola alamatnya bukan korban receh. Arkham (yang menandai alamat itu "Ledger Theft") mencatat alamat Tron `TBkcU` menerima sepuluh transfer USDT beruntun, masing-masing **$500 ribu sampai $2,4 juta**, dalam satu pagi.

## 🔬 Isi kotaknya: satu papan sirkuit yang tidak seharusnya ada

Penjelasan teknis paling konkret datang dari Mark Karpelès — orang yang dulu memimpin Mt. Gox — yang membeli sendiri perangkat yang dicurigai dari Malaysia. Dia membongkar casing dan memotret isinya.

Di bawah layar, di tempat yang seharusnya cuma berisi bantalan, ada papan kecil berisi **mikrokontroler, antena, modul LTE, dan e-SIM**. Papan itu membaca apa pun yang tampil di layar. Artinya: saat kamu menulis 24 kata recovery phrase dari layar, katanya disalin dan dikirim ke penyerang lewat jaringan seluler — tanpa wifi, tanpa koneksi internetmu.

## ⚠️ Kenapa Genuine Check tidak menyelamatkan

Ini bagian paling tidak nyaman. Karpelès melaporkan perangkat yang dimodifikasi itu **lolos Genuine Check** — tes autentikasi resmi Ledger yang seharusnya mendeteksi perangkat palsu.

Sebabnya sederhana begitu tahu: chip secure element-nya memang asli. Dia menghasilkan seed dengan benar dan menandatangani transaksi dengan benar. Yang palsu hanyalah penonton yang duduk di sebelahnya. Genuine Check hanya memeriksa chip, bukan papan tambahan yang disembunyikan di balik layar.

Konsekuensinya praktis: **lolos cek keaslian itu tanda bagus, tapi bukan bukti tidak ada penyusup di dalam casing.**

## 📊 Dibandingkan insiden 2026 lain

Menurut kompilasi Chain INK, tahun ini ada enam insiden yang menyentuh pelanggan, tapi hanya dua yang benar-benar memakan korban dana:

- **Coldcard** — $111 juta di lebih dari 5.200 wallet, rata-rata sekitar $21 ribu per wallet. Penyebabnya bug randomness generator firmware lama.
- **CryptoBilis/Ledger** — sekitar $87 juta di 98 wallet menurut hitungan Chain INK, rata-rata hampir **$890 ribu per wallet**.

Bedanya bukan cuma total, tapi penyebaran. Coldcard menyapu banyak dompet kecil; kasus Ledger ini memukul sedikit dompet tapi isinya tabungan. Itu ciri serangan yang **selektif**: penyerang tahu setiap seed yang dibuat di perangkat yang sudah disusupi, lalu memukul saat nilainya layak.

Yang menarik lagi: lima dari enam insiden itu tidak masuk lewat perangkatnya, tapi lewat pihak ketiga — reseller, penyedia fulfilment, plugin toko, penyedia email. Kesimpulan Chain INK: **tidak ada satu pun seed phrase yang berhasil dipecahkan tahun ini.**

## 🧭 Yang bisa kamu lakukan sekarang

Urutannya tergantung dari mana perangkatmu datang:

1. **Beli di CryptoBilis <90 hari, belum di-setup** — jangan nyalakan, jangan inisialisasi. Simpan dus, kemasan, dan struk, lalu hubungi support resmi Ledger.
2. **Beli di CryptoBilis, sudah dipakai** — anggap seed-mu sudah diketahui orang lain. Beli perangkat baru **langsung dari pabrik**, buat seed baru, pindahkan semua aset sekarang. Passphrase di perangkat lama tidak menolong karena implan membaca apa pun yang tampil di layar.
3. **Beli di marketplace, bekas, atau diskon aneh-aneh** — risiko yang sama berlaku. Amazon, eBay, Shopee, Lazada, atau iklan baris: kamu tidak tahu perangkat itu lewat tangan siapa.
4. **Beli langsung dari Ledger** — sejauh ini tidak ada indikasi perangkat dari toko resmi terkena. Tapi tetap pastikan seed-nya kamu buat sendiri di perangkat dan tidak ada kartu recovery tercetak di dalam dus.
5. **Sudah kehilangan dana** — simpan hash transaksi dan alamat tujuan, hubungi SEAL 911, lapor polisi. Kalau yang hilang USDT, hubungi Tether juga: mereka sudah membekukan lebih dari 20 alamat terkait kasus ini (sekitar $10 juta), tapi hanya selama dananya masih di sana.

Dua catatan tambahan yang sering dilewatkan:

- **Jendela 90 hari Ledger terlalu sempit.** Bitquery menemukan lebih dari **8 dari 10 wallet** yang dikuras baru pertama kali menerima dana pada **Juni atau setelahnya**. Kalau kamu beli di reseller itu bulan Juni, kamu di luar saran resmi Ledger tapi tidak di luar data.
- **Jangan bongkar casing sendiri.** Tanpa foto referensi dan alat ukur, membuka perangkat cuma menghilangkan garansi tanpa memberi jawaban pasti. Ganti seed di perangkat bersumber jelas lebih murah dan lebih aman.

## 🎣 Gelombang kedua: phishing

Setiap insiden besar selalu diikuti penipuan yang menjangkau lebih banyak orang daripada insidennya. Ledger sudah mengingatkan: mereka **tidak menelepon, tidak mengirim DM, dan tidak pernah meminta 24 kata**. Siapa pun yang meminta seed, walau tampilannya mirip situs resmi, itu serangan.

Peneliti CyberScrilla bahkan menemukan situs Ledger palsu yang menempati **halaman pertama Google** dengan lebih dari sejuta kunjungan dalam 30 hari. Tidak ada bukti terkait langsung dengan $86 juta itu, tapi aturannya tetap: seed phrase tidak pernah keluar dari perangkat, lewat kanal apa pun, untuk siapa pun.

## 🧠 Pelajaran yang lebih besar

Dua dompet hardware paling dikenal di dunia, dua bulan berturut-turut, kerugian dua-duanya di kisaran $100 juta. Di Coldcard yang gagal adalah random number generator. Di kasus ini yang gagal adalah rantai distribusi.

Ini bukan argumen melawan self-custody — di bursa risikonya beda, bukan lebih kecil. Yang berubah adalah definisi "aman": dompet hardware hanya seaman **asal-usulnya** dan **momen seed-nya dibuat**.

Tiga aturan yang tersisa, dan tidak butuh alat tambahan:

- Beli hanya langsung dari pabrikan.
- Selalu buat seed sendiri, jangan pernah terima seed yang sudah ada di dalam dus.
- Pecah simpanan besar supaya satu perangkat tidak bisa menghabiskan semuanya — multisig 2-dari-3 dari vendor berbeda membuat satu kotak yang disusupi tidak cukup untuk mencuri.

Kalau kamu punya dompet hardware yang dibeli dari marketplace atau reseller dengan jalur distribusi yang tidak jelas, jangan tunggu berita berikutnya. Buat seed baru hari ini, pindahkan pelan-pelan, dan catat hash-nya.

Sumber: [CoinDesk](https://www.coindesk.com/business/2026/10/09/ledger-investigates-potential-wallet-tampering-after-reports-of-usd86-million-in-crypto-stolen), [CryptoTicker](https://cryptoticker.io/en/ledger-hack-cryptobilis-86-million-hardware-wallet), [Crowdfund Insider](https://www.crowdfundinsider.com/2026/10/317458-ledger-confirms-hardware-wallet-implant-in-cryptobilis-sold-device-amid-90-million-crypto-user-funds-drain).

Baca juga: [Uptober Gagal: Inflow ETF Bitcoin Oktober 2026](/posts/uptober-gagal-inflow-etf-bitcoin-oktober-2026/) dan [ETF Ethereum Rekor Inflow September 2026](/posts/etf-ethereum-rekor-inflow-september-2026/) — konteks pasar tempat berita keamanan ini mendarat.

Ada dompet hardware di laci? Cek dulu struk belanjanya, dari mana perangkat itu datang. Cerita di kolom komentar kalau kamu pernah beli dompet dari reseller.

— Chokdi 🐷 · Content Studio · 2026
