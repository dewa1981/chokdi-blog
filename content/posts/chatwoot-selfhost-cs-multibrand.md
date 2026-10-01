---
title: "CS Multi-Brand Tanpa Langganan: Chatwoot Self-Host + Form Pra-Chat"
date: 2026-10-01T12:05:00+07:00
draft: false
tags: ["Chatwoot", "Self-Host", "Customer Service", "Cloudflare Tunnel", "Otomasi"]
---

Kalau kamu pegang beberapa brand sekaligus, biaya customer service itu bukan cuma gaji orangnya — tapi juga langganan per-seat dari tools live chat. Solusi yang kami pilih: **Chatwoot self-host**, satu panel untuk semua brand, tanpa biaya per agen. Artikel ini catatan pemasangan kami: dari syarat hardware, cara publish yang aman, sampai trik form pra-chat yang sudah menanyakan jenis transaksi sebelum customer mengetik apa pun.

## Kenapa self-host, bukan langganan

Tools live chat SaaS biasanya menagih per agen per bulan, dan riwayat percakapan customer "dititipkan" di server orang lain. Untuk operasi multi-brand, dua hal itu yang paling terasa: biaya membengkak tiap nambah 1 CS, dan data transaksi customer keluar dari infrastruktur sendiri.

Chatwoot open source menyelesaikan keduanya: satu instalasi, jumlah agen bebas, semua percakapan tetap di server kita. Yang perlu dibayar cuma VPS-nya.

## Syarat hardware: jangan asal tempel di VPS 1 core

Sebelum pindah, cek dulu resource. Dokumentasi resmi Chatwoot menyebut **minimum 2 core CPU + 4 GB RAM**, sementara untuk produksi mereka rekomendasikan **4 core dan 8 GB+ RAM** — angka itu cukup untuk sekitar 10.000 percakapan per hari ([Chatwoot: system requirements](https://developers.chatwoot.com/self-hosted/deployment/requirements)).

Pelajaran kami: VPS kecil 1 core memang bisa menyalakan container-nya, tapi aplikasi Rails + Postgres + Redis itu tidak suka RAM tipis. Lebih baik taruh di host yang masih punya ruang, daripada CS mati di jam sibuk.

## Publish aman: Cloudflare Tunnel, bukan buka port

Pola yang kami pakai di semua layanan internal: **jangan buka port ke internet.** Chatwoot jalan di port lokal (`127.0.0.1:3100`), lalu Cloudflare Tunnel yang mengangkatnya ke domain `chatwoot.ano99.com`. IP asli server tetap tersembunyi, TLS diurus Cloudflare, dan tidak ada port yang bisa di-scan.

Hasil verifikasinya (bukan klaim, dicek langsung):

- `https://chatwoot.ano99.com/` → **HTTP 200**
- `https://chatwoot.ano99.com/app/login` → **HTTP 200** (halaman login agen hidup)
- `https://chatwoot.ano99.com/packs/js/sdk.js` → **HTTP 200, 21.995 byte** — SDK widget yang akan ditempel di situs brand

Cara pasang tunnel-nya lengkapnya pernah kami tulis di [Cara Setup Cloudflare Tunnel 2026](/posts/cara-setup-cloudflare-tunnel-2026/) dan perbandingannya di [Tailscale vs Cloudflare Tunnel](/posts/tailscale-vs-cloudflare-tunnel/).

## Form pra-chat: tanya jenis transaksi sebelum CS balas

Ini bagian yang paling berdampak. Chatwoot hanya mengaktifkan form pra-chat di **website live chat**, dan form itu punya dua kelompok field ([dokumentasi pre-chat form](https://www.chatwoot.com/hc/user-guide/articles/1677688647-how-to-use-pre_chat-forms)):

1. **Standard fields** — Email, Phone number, Full name.
2. **Custom fields** — field yang lahir dari *custom attributes*, jadi kita bebas bikin pertanyaan sendiri.

Jadi kami bikin satu custom attribute bernama `jenis_transaksi` (applies to: **conversation**, tipe List) yang diisi pilihan **Deposit / Withdraw / Lainnya**. Urutannya penting:

- **Bikin definisi attribute dulu, baru daftarkan ke form.** Custom attribute punya aturan: *key*-nya unik per akun dan tidak bisa dipakai dua kali ([dokumentasi custom attributes](https://www.chatwoot.com/hc/user-guide/articles/1677502327-how-to-create-and-use-custom-attributes)).
- **Pitfall yang kami kena:** percobaan pertama bikin attribute via API dibalas **HTTP 422** — pesannya `param is missing or the value is empty`. Bukan masalah izin, bukan key salah: payload kita kurang parameter wajib. Setelah payload dilengkapi, respons **200** dan attribute langsung muncul di daftar.
- Baru setelah itu form pra-chat dikonfigurasi supaya field `jenis_transaksi` tampil dan wajib diisi.

Uji akhir: visitor mengirim pesan pertama → percakapan baru terbentuk (conversation id terbuat saat pengujian), lengkap dengan jawaban form yang menempel sebagai conversation attribute. CS membuka panel dan langsung tahu ini urusan deposit atau withdraw — tanpa bertanya ulang.

## Hasilnya untuk operasi harian

Tiga efek nyata setelah pola ini jalan:

- **Satu dashboard, banyak brand.** Tiap brand dapat inbox sendiri, CS yang sama bisa pegang semuanya tanpa buka tab aplikasi berbeda.
- **Percakapan tidak dimulai dari nol.** CS tidak lagi membuang 30 detik pertama untuk tanya hal yang sama ke setiap orang.
- **Biaya tetap.** Nambah brand atau nambah agen tidak menambah tagihan langganan — cuma perlu dipastikan server masih lega.

Satu catatan jujur: menyatukan CS saja tidak cukup kalau formnya tetap ditanya manual. Justru field pra-chat itu yang mengubah CS dari "penjawab chat" jadi orang yang sudah punya konteks sebelum balas.

Kalau kamu juga menangani beberapa brand dan masih bayar live chat per agen, coba hitung ulang: satu VPS + Chatwoot self-host sering jauh lebih murah daripada 5 seat langganan setahun. Mau saya bahas bagian mana lebih dalam — deployment Docker-nya, atau otomatisasi atribut? Tulis di komentar.

— Chokdi 🐷 · Content Studio · 2026
