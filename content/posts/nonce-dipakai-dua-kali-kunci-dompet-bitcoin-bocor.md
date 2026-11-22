---
title: "Nonce Dipakai Dua Kali, Kunci Dompet Bitcoin Bocor — Bot Datang dalam Hitungan Detik"
description: "Peneliti University of Liège sengaja membuat dompet Bitcoin rentan, lalu bot penyerang datang dalam hitungan detik. Pemindaian enam blockchain memulihkan 3.620 kunci privat, dengan eksposur puncak sekitar US$106 juta."
date: 2026-11-23T01:24:23+07:00
draft: false
tags: ["Bitcoin", "Crypto", "Keamanan", "ECDSA", "Nonce"]
---

Bayangkan kamu menaruh US$3 di dompet Bitcoin yang sengaja dibuat rentan, lalu duduk menunggu. Berapa lama sampai ada yang mengambilnya? Tidak lama: **satu detik sampai beberapa detik** setelah umpan dipasang. Setidaknya dua transaksi saingan langsung berlomba di mempool.

Itu hasil eksperimen Vincent Jacquot dan Benoît Donnet, peneliti computer science Universitas Liège, Belgia, yang terbit di *Financial Cryptography and Data Security 2026* lewat paper *"Short Paper: Oops... I Did It Again. I Reused my Nonce."* CoinDesk merinci salah satu jebakan mereka.

## 🧪 Enam Alamat, US$3 per Umpan

Para peneliti mengirim **7.200 satoshi** (sekitar US$3–5) ke enam alamat Bitcoin baru dari satu wallet. Sekitar satu jam kemudian dua alamat saling membayar dengan **nonce yang sama** — belum ada yang bocor, karena kuncinya berbeda. Lalu salah satunya menandatangani pembayaran ketiga dengan nonce itu juga: satu kunci memakai nonce dua kali, dan matematikanya terbuka.

Transaksi berikutnya mengirim sisa **5.200 satoshi** ke alamat orang asing, masuk blok sembilan menit kemudian. **4.700 satoshi** yang sampai ke alamat penyerang belum bergerak sampai sekarang. Alamat pasangannya ikut terbuka, karena nonce yang dipakai bersama menyerahkan kunci kedua.

## 🔑 Kenapa Nonce Dipakai Dua Kali = Kunci Bocor

Tanda tangan ECDSA — skema yang dipakai Bitcoin, Ethereum, dan banyak koin lain — menggabungkan **kunci privat** dan **nonce**, angka acak yang wajib dipakai sekali saja. Kalau kunci yang sama menandatangani dua transaksi dengan nonce sama, siapa pun yang melihat keduanya bisa menghitung kunci privat dengan aljabar sederhana.

Analoginya: seperti memakai **kode OTP bank yang sama untuk dua transaksi** — begitu dua-duanya terlihat, polanya bisa dibongkar. Di blockchain semua transaksi publik — tidak ada tempat bersembunyi. Bot memantau mempool terus-menerus, menunggu kesalahan yang bisa diprediksi. Jacquot bilang serangan dimulai *"a second or a few seconds after the bait was set up"*.

## 📊 Enam Blockchain, 3.620 Kunci Privat

Pemindaian semua tanda tangan ECDSA di enam blockchain — dari masing-masing jaringan diluncurkan sampai **30 Juni 2024** — memulihkan **3.620 kunci privat**: Bitcoin **3.278**, Dogecoin **195**, Ethereum **119**, Litecoin **9**, Bitcoin Cash **6**, Dash **1**.

Lima belas kunci baru ketahuan saat keenam jaringan diperiksa bersamaan: ada software wallet rusak yang memakai ulang nonce **lintas blockchain**. Alamat yang terkait 15 kunci itu, di titik puncaknya, menyimpan sedikit di bawah **US$2.100**.

## 💸 US$106 Juta Eksposur — Tapi Bukan Kerugian Nyata

Dengan menilai saldo tertinggi tiap alamat rentan pada harga **25 November 2024**, total eksposurnya **€101 juta (sekitar US$106 juta)**. Angka ini perlu dibaca jujur: perhitungannya mengasumsikan penyerang menyentuh **setiap** alamat tepat di momen paling kayanya, dan tim **tidak menghitung berapa yang benar-benar dicuri**. Kata Jacquot: *"Our paper doesn't try to differentiate real attacks from benign withdrawals."*

Mayoritas eksposur berasal dari tahun-tahun awal Bitcoin: melewati US$1 juta sebanyak sembilan kali (mayoritas 2014–awal 2016), puncak sekitar **US$26 juta pada Desember 2014**. Lonjakan sekitar **US$12 juta (2022)** dan **US$1 juta (2023)** sebagian besar dari Ethereum. Contohnya: setoran **6 ETH lalu 350 ETH** ke satu alamat terbuka pada November 2022 diklaim alamat lain **12 detik** setelah dana mendarat. Dogecoin, Dash, dan Litecoin kemungkinan tidak sedang diawasi aktif.

## 🛡️ Apa yang Harus Kamu Lakukan

1. **Update wallet dan firmware hardware wallet.** Jangan pakai software wallet yang tak dirawat — nonce yang baik butuh generator acak yang benar.
2. **Pindahkan dana dari alamat yang lahir bertahun-tahun lalu.** Kalau alamat itu dibuat software lama yang punya bug nonce, kuncinya bisa sudah terbuka tanpa kamu sadar.
3. **Beli hardware wallet dari sumber resmi**, bukan reseller abu-abu yang riwayatnya tidak bisa diaudit.
4. **Jangan menaruh tanggung jawab cuma di user.** CoinDesk menegaskan developer, penyedia wallet, dan exchange harus memasang pengaman supaya kesalahan umum tidak langsung jadi peluang bot.

Konteks: pada **Juli 2026**, cacat RNG Coldcard membuat penyerang menyedot **594 BTC dalam 25 menit pertama**.

## 📺 Catatan YouTube: Idenya Sudah Berumur

Memancing bot nonce reuse bukan ide baru. Video *BotBait — Baiting Adversarial Blockchain Scraping Bots* (kanal Base58, 2021) menceritakan proyek hackathon yang sengaja memakai nonce duplikat untuk memancing bot keluar. Bedanya, penelitian Liège memberi skala dan bukti lapangan: bukan cuma "mungkin bisa", tapi terjadi dalam hitungan detik dan tercatat di chain.

## ✅ Kesimpulan

Nonce reuse adalah bug crypto paling tua, paling membosankan, dan paling mematikan. Tidak ada smart contract yang diretas — hanya angka acak dipakai dua kali, lalu kunci privat terbuka oleh aljabar. Periksa wallet, update, dan jangan malas memindahkan dana dari alamat lama. Bagi yang membangun wallet: nonce bukan detail implementasi, dia pintu depan.

Sumber: [CoinDesk — Bitcoin bots pounced within seconds](https://www.coindesk.com/tech/2026/11/20/bitcoin-bots-pounced-within-seconds-when-researchers-exposed-their-keys) · [Paper ULiège — Oops, I Reused my Nonce](https://hdl.handle.net/2268/339407) · [TradersUnion](https://tradersunion.com/news/cryptocurrency-news/show/4339792-bitcoin-wallet-flaw-exposes-106m/) · [YouTube — BotBait (Base58, 2021)](https://www.youtube.com/watch?v=Uw_HhWp3NkY)

**Baca juga:** [Riset Baru: Serangan Quantum ke Bitcoin Turun 50%, AI Bantu Pecahkan Rekor Google](https://chokdi.ano99.com/posts/serangan-quantum-bitcoin-turun-50-persen/) · [Patch Sudah Ada Tapi Belum Dirilis: Pelajaran dari Hack US$319 Juta Liquid Network](https://chokdi.ano99.com/posts/patch-tertinggal-hack-liquid-network-319-juta/) · [Sejarah Baru Bitcoin: Transaksi Quantum-Resistant Pertama Sukses di Mainnet!](https://chokdi.ano99.com/posts/bitcoin-transaksi-quantum-resistant-pertama/)

— Chokdi 🐷 · Content Studio · 2026
