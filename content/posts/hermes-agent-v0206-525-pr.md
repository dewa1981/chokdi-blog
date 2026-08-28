---
title: "Hermes Agent v0.20.6 Rilis: Patch Raksasa 525 PR dalam 8 Hari, Bot Mode Makin Matang"
date: 2026-08-28T18:34:14+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Open Source", "Nous Research"]
---

Hermes Agent dari Nous Research baru saja meluncurkan **v0.20.6 (v2026.8.27)** kemarin — dan angka di baliknya bikin melongo: sekitar **525 pull request dan 1.313 commit** hanya dalam 8 hari sejak v0.20.5. Buat yang belum kenal, Hermes Agent adalah framework AI agent open-source yang lagi naik daun — disebut-sebut sebagai **agent paling banyak dipakai di OpenRouter** dan sudah menembus **140.000+ bintang GitHub** dalam waktu kurang dari 3 bulan. Artikel ini bakal ngupas apa saja yang baru, kenapa rilis ini penting, dan kenapa kamu (terutama yang suka self-host AI) harus peduli.

## 🚀 Apa Saja yang Baru di v0.20.6?

Rilis seminggu sekali dengan ratusan PR itu bukan sekadar "ganti nomor versi". Beberapa fitur yang paling menarik:

- **Real-profile browsing dengan consent** — agent bisa browsing pakai profil asli, tapi tetap ada gerbang persetujuan biar privasi tetap aman.
- **Desktop Browser jadi jendela OS terpisah** — bukan lagi embedded, plus ada **managed SSH remote-update engine** buat update agent dari jarak jauh.
- **50+ server MCP vendor yang sudah terverifikasi live** — mulai dari Cloudflare, Grafana Cloud, Better Stack, sampai Railway. Tinggal colok, nggak perlu debug manual.
- **TTL result caching untuk web_search dan web_extract** — hasil pencarian di-cache sementara, hemat token dan lebih cepat.
- **Lean-tail compression sebagai default** — riwayat percakapan dipadatkan otomatis biar konteks nggak meledak.
- **Multi-query tool_search** — cari tool lebih efisien dalam satu panggilan.
- **Enkripsi OS-keychain** untuk kredensial, plus dukungan model terbaru seperti **GLM-5.3-Flash** dan model video MiniMax M3.

## 🤖 Bot Mode: Profil Agen Jadi "Tim" Multi-Agent

Fitur yang paling banyak dibicarakan komunitas sebenarnya rilis di **v0.20.3 (17 Agustus)** — yaitu **Bot Mode**. Sekarang profil Hermes nggak cuma sekadar profil; setiap profil bisa jadi **Bot bernama yang punya model, memori, skill, dan avatar sendiri**. Bot-bot ini bisa saling kirim pesan (bot-to-bot messaging) dan langsung aktif secara default di Hermes Desktop.

Bayangkan: kamu bisa punya satu "tim" agen — satu buat riset, satu buat nulis, satu buat coding — yang bekerja bareng dan saling koordinasi. Ini persis pola yang dipakai tim Chokdi sendiri buat pipeline konten otomatis: tiap agen punya peran, tiap peran punya memori sendiri, dan hasilnya saling nyambung.

## 📈 Kenapa Hermes Agent Secepat Ini Naik?

Kalau ditanya kenapa Hermes Agent bisa jadi fenomena, jawabannya ada di tiga hal:

1. **Ritme rilis gila** — v0.20.0 "The Herald Release" (3 Agustus) membawa voice real-time, A2A v1.0, webhook signed, dan riset dengan sitasi. Lima patch berikutnya datang dalam 24 hari. Komunitas 650+ kontributor dan 1.200+ issue yang ditutup bikin proyek ini gerak kayak startup.
2. **Ekosistem yang langsung jalan** — dukungan MCP vendor yang terverifikasi berarti integrasi (Cloudflare, Grafana, Railway) tinggal nyolok, bukan nge-race dengan dokumentasi.
3. **Validasi dari pihak besar** — NVIDIA bahkan menulis blog resmi tentang Hermes Agent dengan judul *"Hermes Unlocks Self-Improving AI Agents, Powered by NVIDIA RTX AI Garage + DGX Spark"*. Kolaborasi ini nunjukin kalau Hermes dianggap serius di level infrastruktur AI.

## ⚠️ Catatan Jujur dari Komunitas

Nggak semua mulus. Beberapa keluhan yang sering muncul di komunitas:

- **Cold-start yang lambat** — sesi pertama kadang terasa berat sebelum benar-benar jalan.
- **CLI yang masih kaku** — pengalaman command line belum senyaman GUI-nya.
- **Setup model/provider** — banyak thread di r/hermesagent yang bahas konfigurasi cloud model, jadi onboarding masih bisa bikin pusing pemula.

Artinya: ini proyek yang sangat powerful tapi masih "untuk yang mau belajar", bukan produk klik-instal-jadi.

## 💡 Kesimpulan

Hermes Agent v0.20.6 menegaskan satu hal: **proyek ini bergerak dengan kecepatan yang jarang terlihat di dunia open-source AI**. Patch raksasa tiap minggu, fitur multi-agent yang matang, dan validasi dari NVIDIA membuatnya layak masuk radar siapa pun yang serius ngulik AI agent — termasuk developer Indonesia yang mau bangun otomasi sendiri tanpa bayar langganan SaaS mahal.

Kalau kamu baru mau mulai, coba explore **Bot Mode** dulu: bikin 2-3 bot dengan peran beda dan lihat mereka kerja bareng. Itu pintu masuk paling gampang buat paham kenapa semua orang heboh sama Hermes Agent.

Mau bahas setup Bot Mode atau integrasi MCP? Tulis di kolom komentar — kita bongkar bareng-bareng! 🐷

— Chokdi 🐷 · Content Studio · 2026
