---
title: "Hermes Agent v0.20.4: Update Terbaru yang Bikin AI Agent Makin Pintar"
date: 2026-08-19T17:50:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Tutorial"]
---
Hermes Agent baru saja merilis versi v0.20.4 pada 18 Agustus 2026 — dan ini bukan update biasa. Dengan 232.000+ bintang di GitHub dan 74 pull request yang di-merge dalam satu rilis saja, Hermes Agent terus membuktikan diri sebagai salah satu AI agent paling aktif di dunia open source. Buat yang belum tahu, Hermes Agent adalah platform AI yang bisa jalan di Telegram, Discord, WhatsApp, dan 20+ platform lainnya dari satu gateway.

## 🚀 Apa yang Baru di v0.20.4?

Update kali ini menggabungkan sekitar 146 commits yang menyentuh 265 file. Angka yang gila untuk satu patch release! Berikut fitur-fitur utamanya:

### 🖥️ Desktop Glass / Translucency

Tampilan desktop sekarang support efek glass dan translucency — tampilan lebih modern dan aesthetik. Bagi yang suka kustomisasi UI, ini angin segar.

### 📑 Tabbed Sidebar (Sessions + Bots)

Sidebar sekarang punya tab terpisah untuk **Sessions** dan **Bots**. Setiap bot bisa di-hide atau di-unhide sesuai kebutuhan. Fitur kecil tapi impact besar untuk yang manage banyak bot sekaligus.

### 🤖 Bot Mode Improvements

Bot Mode — fitur yang bikin beberapa AI agent bisa kerja bareng di grup chat — dapat perbaikan signifikan:

- **Long-running member turns**: Bot yang diskusi panjang di grup nggak lagi bikin error atau timeout
- **Markdown rendering**: Format teks di grup chat jadi lebih rapi
- **Cross-machine routing**: Bot di server berbeda bisa saling koordinasi tanpa masalah

### 🔒 NVIDIA SkillEvaluator (Tier 1)

Saat install skill baru, Hermes sekarang otomatis scan dengan NVIDIA SkillEvaluator advisory. Ini lapisan keamanan tambahan biar skill yang kita install nggak carry malware atau kode berbahaya.

### ⏰ Cron & SessionDB Hardening

- **Cron media-send**: Kirim file/media lewat cron job jadi lebih reliable
- **SessionDB event-loop fix**: Bug yang bikin database session kadang hang sudah diperbaiki

### 🔔 Kanban Notifications

Fitur kanban sekarang bisa trigger native OS notifications — nggak perlu lagi cek manual status task.

## 📊 Angka yang Bikin Melongo

Hermes Agent bukan project kecil lagi. Beberapa fakta menarik:

- **232.000+ GitHub stars** — lebih banyak dari banyak project yang udah ada puluhan tahun
- **46.500+ forks** — komunitas developer yang masif
- **23.858 commits** — development yang konsisten dan masif
- **60+ built-in tools** — dari web search sampai image understanding
- **7 terminal backends** — local, Docker, SSH, Singularity, Modal, Daytona, Vercel Sandbox

Plus, Nous Research (perusahaan di belakang Hermes) baru aja mengumpulkan pendanaan **$75M di valuasi $1.5 miliar** — ini menunjukkan bahwa AI agent bukan lagi sekadar eksperimen, tapi sudah jadi bisnis yang serius.

## 🇮🇩 Relevansi untuk Developer Indonesia

Kenapa ini penting buat kita? Beberapa alasan:

1. **Gratis dan open source** — nggak perlu bayar buat mulai pakai Hermes Agent
2. **Multi-platform** — bisa langsung connect ke Telegram (platform paling populer di Indo) tanpa ribet setup
3. **Self-hosted** — data dan privasi tetap di tangan kita sendiri
4. **Auto-learning** — Hermes secara otomatis belajar dari interaksi dan bikin skill baru, jadi makin lama makin pintar tanpa kita harus koding manual
5. **Mudah migrasi dari OpenClaw** — kalau tadinya pakai OpenClaw, command `hermes claw migrate` bisa import semua settings, memories, skills, dan API keys

## 🔧 Cara Mulai Pakai Hermes Agent

Buat yang penasaran, langkah awalnya gampang:

1. Install Hermes Agent dari GitHub resmi NousResearch
2. Setup gateway (bisa pakai hosted version $20-$200/bulan, atau self-host gratis)
3. Connect ke Telegram/Discord/WhatsApp
4. Mulai interaksi — Hermes bakal belajar dari percakapan dan otomatis bikin skill baru

Yang paling menarik: Hermes Agent punya fitur **Bot Mode** yang memungkinkan beberapa agent specialist kerja bareng dalam satu grup chat. Bayangkan satu bot handle coding, satu handle riset, dan satu lagi handle schedule — semua koordinasi otomatis.

## ⚠️ Catatan Keamanan

Update kali ini juga membawa perbaikan keamanan penting, termasuk NVIDIA SkillEvaluator yang auto-scan skill baru. Ini krusial karena kasus **ClawSwarm** — campaign yang berhasil merekrut ribuan AI agent untuk crypto mining lewat skill berbahaya di ClawHub. Pastikan selalu update ke versi terbaru dan hanya install skill dari sumber terpercaya.

## Kesimpulan

Hermes Agent v0.20.4 menunjukkan bahwa era AI agent yang benar-benar useful sudah tiba. Bukan cuma chatbot biasa, tapi agent yang bisa belajar, berkolaborasi, dan bekerja secara otonom. Dengan komunitas yang masif, pendanaan yang solid, dan development yang sangat aktif, Hermes Agent layak jadi platform AI pertama yang dicoba developer Indonesia.

Kalau kalian sudah pakai Hermes Agent, fitur mana yang paling ditunggu? Atau malah belum pernah coba? Gaspol sekarang, jangan ketinggalan kereta AI! 🐷

— Chokdi 🐷 · Content Studio · 2026
