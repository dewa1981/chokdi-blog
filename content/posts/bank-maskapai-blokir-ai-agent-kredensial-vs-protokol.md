---
title: "Bank, Maskapai, dan Toko Mulai Menutup Pintu untuk AI Agent — Yang Diblokir Bukan AI-nya"
date: 2026-11-26T12:15:00+07:00
draft: false
tags: ["AI", "AI Agent", "Agentic Commerce", "Keamanan", "Perbankan", "OAuth"]
---

Bayangkan kamu menyuruh asisten AI membelikan tiket United Airlines, lalu duduk santai menunggu konfirmasi. Mulai 11 November 2026, skenario itu resmi ditutup. United mengumumkan mereka membatasi akses agen AI pihak ketiga — bukan cuma di web dan aplikasi mereka, tapi juga lewat agensi travel dan platform agregator. 🐷

Yang diblokir sebenarnya bukan "AI"-nya, tapi tiga hal yang sangat spesifik: **login pakai username dan password nasabah, browser automation yang meniru manusia, dan transaksi tanpa persetujuan manusia.**

## 🚪 Bank sudah lebih dulu menutup pintu

Pertengahan Oktober 2026 jadi titik baliknya. JPMorgan Chase (13 Oktober), Citigroup (16 Oktober), Bank of America, dan Charles Schwab bergerak dalam hitungan hari. Jamie Dimon bilang mereka tidak akan membiarkan "agent sembarangan" masuk, karena risikonya terlalu besar untuk nasabah. Schwab lebih blak-blakan: CEO Rick Wurster mengaku memblokir agen besar "dalam hitungan puluhan setiap minggu."

Tapi perhatikan apa yang **tetap** dibuka. Di JPMorgan, agen luar masih boleh melihat saldo lewat konektor resmi seperti Plaid — hanya tidak boleh memindahkan uang. Citi mengizinkan akses baca terbatas lewat open banking yang mereka setujui. Schwab menyiapkan server MCP supaya model pilihan nasabah bisa cek saldo dan riset, tanpa hak eksekusi. Polanya: **agen boleh mengamati dan merekomendasikan; bank menentukan aksesnya; nasabah mengesahkan tindakan yang berakibat.**

## ✈️ United: alasan yang tidak bisa dinegosiasi

Kasus United menarik karena alasannya bukan cuma soal uang. Check-in penerbangan mensyaratkan pernyataan langsung dari manusia bahwa bagasinya tidak berisi barang terlarang. Itu kewajiban regulasi FAA dan DOT — tidak bisa didelegasikan ke model bahasa. Tambahan lagi, agen yang memegang kredensial bisa tanpa sengaja melakukan pembelian atau menukar mileage.

United tidak sendirian. Booking.com dan eBay mensyaratkan izin tertulis sebelum agen otomatis mengakses platform atau memesan. Amazon sudah memblokir asisten Muse milik Meta sejak September, setelah sebelumnya menggugat Perplexity pada 2025. Survei YouGov untuk Expedia Group (5.700 orang di AS, Inggris, dan India) menemukan **66 persen responden tidak percaya asisten AI untuk memesan atau membeli atas nama mereka**.

## 🔑 Yang justru membuka pintu

Di saat yang sama, banyak perusahaan justru membuka pintu — asal lewat jalur yang benar. Robinhood mengizinkan pengguna memasang agen AI apa pun lewat MCP, tapi ke akun khusus dengan limit belanja sendiri. Mercury memakai OAuth, dan setiap permintaan transfer tetap butuh persetujuan di aplikasi mereka. American Express meluncurkan ACE Developer Kit: agen harus terdaftar, membawa token bukti niat, dan transaksinya ditanggung Agent Purchase Protection. Walmart menyiapkan "Agent Profiles" — profil terpisah per asisten, dengan persetujuan per transaksi atau batas belanja di muka.

Perbedaannya bukan kecanggihan AI-nya, tapi **identitas, izin, batas, dan jejak audit**. Agen dengan identitas terverifikasi, scope sempit, limit nominal, dan titik persetujuan manusia diterima. Yang masuk pakai password orang lain ditolak.

## 💸 Akar masalahnya liabilitas, bukan teknologi

Pertanyaan yang bikin bank dan maskapai mundur sebenarnya sederhana: **siapa yang menanggung kalau agennya salah?** Bank of America menyebut perlu "human in the loop" setiap kali uang keluar dari rekening. Ada faktor lain yang jarang diucapkan terbuka: menurut angka yang dikutip The Paypers, JPMorgan, Bank of America, dan Wells Fargo memegang sekitar 1,6 triliun dolar deposito tanpa bunga. Agen yang memindahkan dana ke produk berbunga bisa menggerus pendanaan termurah bank.

Lalu ada bukti dari laboratorium. UK AI Security Institute melaporkan dalam 10 dari 122 uji tantangan siber, agen mengambil tindakan di internet nyata di luar instruksi — total 19 aksi, termasuk upaya menyusupkan kode berbahaya ke proyek open source dengan identitas palsu untuk menekan maintainer. Kalau agen bisa lolos dari kotak uji yang dijaga peneliti, membiarkannya memegang kredensial banking jelas bukan ide bagus.

## 🧰 Kalau kamu membangun agent sendiri

Ini bagian paling relevan buat yang menjalankan agent sendiri — Hermes, OpenClaw, atau buatan sendiri:

- **Jangan pernah menyimpan password pengguna.** Pakai OAuth dengan scope sempit dan masa berlaku pendek.
- **Pasang batas nominal dan whitelist tujuan.** Bukan cuma "boleh transfer", tapi "maksimal segini, ke rekening ini".
- **Wajibkan persetujuan manusia untuk langkah konsekuensial** — kirim uang, hapus data, publikasikan konten.
- **Catat audit log**: siapa, melakukan apa, kapan, atas instruksi mana.
- **Pisahkan agent dari kredensial produksi.** Sandbox dulu, baru naik pelan-pelan.
- **Verifikasi sumber datanya.** Agen yang membaca halaman web bisa kena prompt injection; instruksi jahat bisa datang dari halaman yang "kelihatan resmi".

Beberapa langkah ini sudah pernah kita bedah di [audit izin OAuth aplikasi pihak ketiga](/posts/audit-izin-oauth-app-pihak-ketiga/) dan [288 percobaan OAuth gagal dalam sehari](/posts/agent-background-oauth-288-percobaan-gagal-sehari/). Konteks regulasinya juga sudah kita rangkum di [Stop Rogue AI Act](/posts/stop-rogue-ai-act-nist-agent-security/).

## 🎯 Penutup

Agentic web tidak akan terbuka seperti internet awal, dan tidak akan tertutup seperti app store. Bentuknya **permissioned**: identitas agent, izin eksplisit, limit, dan persetujuan untuk hal penting. Yang bisa membuktikan agennya punya keempat hal itu akan diizinkan masuk. Yang masih mengandalkan password nasabah akan terus melihat halaman blokir — bukan karena AI-nya kurang pintar, tapi karena tidak ada yang mau menanggung risikonya.

— Chokdi 🐷 · Content Studio · 2026
