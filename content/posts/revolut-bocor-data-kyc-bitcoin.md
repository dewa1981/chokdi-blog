---
title: "Revolut Bocor Data KYC ke Penipu: Paspor, Selfie, dan Riwayat Bitcoin Pelanggan Ikut Terbongkar"
date: 2026-09-13T00:18:00+07:00
draft: false
tags: ["Crypto", "Keamanan", "Privasi"]
---

Revolut, bank digital asal London dengan lebih dari 80 juta pelanggan, mengakui telah menyerahkan data pribadi sejumlah nasabah ke pihak tak berwenang. Pemicunya sederhana tapi mengerikan: sebuah permintaan data yang datang dari **domain email resmi instansi pemerintah**, lengkap dengan kredensial yang lolos pemeriksaan internal. Yang bocor bukan cuma nama dan alamat — paspor, selfie verifikasi, sampai riwayat transaksi bitcoin ikut diserahkan.

Perusahaan bilang dana nasabah aman. Tapi kasus ini membuka titik lemah yang jarang dibahas industri kripto: data KYC (know your customer) yang kita serahkan ke bursa dan bank digital.

## Apa yang Sebenarnya Terjadi

Menurut notifikasi yang dikirim ke pelanggan terdampak (dibaca TechCrunch), permintaan itu **tampak berasal dari instansi pemerintah yang sah** dan membawa kredensial yang berhasil melewati sistem pemeriksaan Revolut. Karena permintaan itu lolos sebagai permintaan hukum yang valid, data pun diserahkan.

Belakangan Revolut menghubungi instansi terkait secara terpisah, dan di situ baru ketahuan bahwa permintaan tersebut palsu. Perusahaan sudah memblokir alamat email sumber permintaan, mengabari instansi yang namanya dicatut, memberi tahu penegak hukum, regulator keuangan, dan otoritas perlindungan data.

Yang masih tertutup sampai sekarang: **berapa banyak pelanggan yang terdampak**. Juru bicara Revolut hanya menyebut jumlahnya "terbatas" dan menolak menyebut instansi mana yang dicatut, dengan alasan investigasi masih berjalan. Dana dan sistem Revolut dinyatakan tidak terpengaruh.

## Data Apa Saja yang Bocor

Kalau digabung, paket data ini lengkap sekali untuk kejahatan lanjutan:

| Kategori | Isi |
|---|---|
| Identitas | Paspor atau SIM, selfie verifikasi wajah, nama, tanggal lahir, pekerjaan |
| Kontak & domisili | Alamat rumah, alamat email, nomor telepon |
| Keuangan | IBAN, mutasi rekening, catatan penarikan, riwayat transaksi penuh — termasuk seluruh aktivitas bitcoin |

Perhatikan poin terakhir. Riwayat transaksi berarti si penyerang tahu **kapan** seseorang pindah dana, ke mana, dan seberapa besar. Itu bukan sekadar pelanggaran privasi, itu profil risiko.

## Kenapa Ini Serius buat Pemegang Bitcoin

Blockchain itu publik — semua transaksi bisa dilihat siapa saja. Yang tidak publik adalah keterkaitan antara alamat on-chain dan orang di baliknya. Nah, database KYC-lah yang menyambungkan dua dunia itu: nama, alamat rumah, kepemilikan bitcoin, semuanya di satu tempat.

Penyidik on-chain ZachXBT, yang pertama menyoroti insiden ini lewat siaran Telegram, menduga kebocoran ini **terarah ke nasabah bernilai tinggi**. Untuk pemegang bitcoin besar, alamat rumah yang bocor bukan cuma masalah spam — ini bahan untuk perampokan fisik, skenario yang sudah berkali-kali terjadi di dunia kripto.

Ini nyambung dengan pelajaran dari [kasus Coldcard Agustus 2026](https://chokdi.ano99.com/posts/bitcoin-agustus-2026-etf-outflow-coldcard-hack/): aset kripto paling rapuh di titik di mana identitas manusia bertemu kunci pribadi.

## Titik Lemahnya Otorisasi, Bukan Firewall

Yang dilanggar di sini bukan tembok pertahanan servernya, tapi **sistem otorisasi** — mekanisme yang memutuskan "permintaan ini datang dari pihak sah". Di internet yang penuh AI, dokumen dan surat-menyurat birokrasi yang meyakinkan makin murah diproduksi dalam skala besar. CoinDesk menyebut pergeseran pertanyaan kuncinya: bukan lagi "seberapa kuat institusi melindungi data", tapi **"seberapa banyak data sensitif yang perlu dikumpulkan, disimpan, dan diungkap"**.

Di situ masuk zero-knowledge proof (ZK). Dengan ZK, institusi bisa membuktikan bahwa verifikasi identitas sudah selesai, atau pelanggan memenuhi syarat tertentu, tanpa melihat paspor dan alamat aslinya. Teknologi ini lama dibahas di komunitas [privacy coin seperti Zcash dan Monero](https://chokdi.ano99.com/posts/zcash-monero-rally-privacy-coin-september-2026/), tapi insiden Revolut memberi ZK use case yang lebih mendesak: kepatuhan tanpa menyimpan data mentah.

## Yang Bisa Kamu Lakukan Sekarang

Kalau kamu pengguna bursa kripto atau bank digital — di mana pun, termasuk yang di Indonesia — anggap data KTP dan selfie kamu sudah pernah berisiko bocor. Praktik yang masuk akal:

- **Pisahkan identitas digital.** Jangan pakai alamat email dan nomor HP yang sama untuk exchange, email utama, dan media sosial.
- **Pakai aplikasi authenticator, bukan SMS.** Penyerang yang sudah punya nomor telepon kamu bisa menyerang OTP lewat SIM swap.
- **Waspadai pesan yang menyebut detail pribadi.** Kalau ada email atau telepon yang tahu nama, nomor rekening, dan riwayat transaksimu, anggap data itu sudah di tangan penipu. Verifikasi lewat aplikasi resmi, bukan tautan yang dikirim.
- **Pindahkan holding jangka panjang.** Untuk jumlah besar, hardware wallet tetap pilihan paling masuk akal; hot wallet di bursa sebaiknya hanya untuk dana yang siap dipakai.
- **Jangan publikasikan kaitan identitas dan dompet.** Tidak ada gunanya memamerkan alamat dompet yang bisa dikaitkan ke namamu.

## Kesimpulan

Revolut tidak dibobol lewat bug eksploitasi, tapi lewat permintaan yang kelihatan resmi. Pertahanan yang mengandalkan "dokumen terlihat sah" makin rapuh ketika AI bisa memalsukan dokumen dengan biaya nyaris nol.

Sampai industri memakai verifikasi yang tidak perlu menimbun data sensitif, asumsi teraman: **database KYC adalah target, bukan brankas.**

Kamu masih nyaman menyimpan semuanya di bursa, atau sudah pindah ke hardware wallet? Tulis di kolom komentar.

— Chokdi 🐷 · Content Studio · 2026

**Sumber:** [TechCrunch — Revolut confirms customer data breach through fake government requests](https://techcrunch.com/2026/09/12/revolut-confirms-customer-data-breach-through-fake-government-requests/) · [CoinDesk — Bitcoin activity, passports exposed after Revolut falls for fake government request](https://www.coindesk.com/tech/2026/09/12/bitcoin-activity-passports-exposed-after-revolut-falls-for-fake-government-request) · [CryptoTicker — Revolut Data Breach: Am I Affected and What To Do?](https://cryptoticker.io/en/revolut-data-breach-am-i-affected/)
