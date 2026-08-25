---
title: "Hermes Agent Rilis 2 Versi dalam Sepekan: Bot Mode Ubah Agent Jadi Tim AI Multi-Agent"
date: 2026-08-25T01:30:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Multi-Agent", "Open Source", "Bot Mode"]
---

Pekan ini jadi pekan sibuk buat Hermes Agent, framework AI agent open-source dari Nous Research. Dalam 9 hari, tim rilis **4 versi patch** — puncaknya **v0.20.5 (21 Agustus)** yang menggabungkan ~323 PR dan ~746 commit, plus **Bot Mode** yang kini jadi fitur bawaan. Kalau kamu penasaran dengan tren AI agent 2026, ini update yang layak disimak.

## 🤖 Apa yang Baru di v0.20.4 dan v0.20.5?

Rilis patch berturut-turut dalam sepekan membawa perbaikan yang terasa langsung:

- **Keyless web search** — pencarian web tanpa API key, dengan rotasi gratis 5 vendor dan ring failover. Di install baru, web search langsung jalan tanpa konfigurasi tambahan.
- **Bot Mode group-room threads** — diskusi antar-bot dalam satu ruang, plus ringkasan percakapan yang bisa dilipat.
- **Drag & drop attachment** PDF/file langsung ke chat di Hermes Desktop.
- **Fuzzy `/model` picker + Ctrl+P command palette** di CLI — ganti model jadi lebih cepat.
- **Runtime stall guards** — hasil temuan evaluasi Composio yang mencegah agent "macet" diam-diam.
- **Perbaikan cron memory** dan `hermes update` receipts + `worktree list/prune`.

Sebelumnya, v0.20.4 (18 Agustus, ~74 PR) menghadirkan desktop glass/translucency, sidebar tabbed **SESSIONS | BOTS** dengan hide/unhide per bot, pemindaian keamanan NVIDIA SkillEvaluator di instalasi skill, dan notifikasi native kanban.

## 👥 Bot Mode: Tim AI yang Saling Kirim Tugas

Fitur paling menarik minggu ini adalah **Bot Mode** — mengubah profil agent menjadi daftar bot bernama, masing-masing punya `memory`, skills, dan model sendiri yang terisolasi. Bot-bot ini saling berkirim pesan lewat **Agent Inbox** yang persisten, dan bisa handoff kerja via **@mention**: misalnya bot *scout* menemukan bahan → *reviewer* menilai → *publisher* menerbitkan. Alur kerja ini persis seperti tim manusia, tapi dijalankan agent.

Menariknya, Bot Mode awalnya cuma plugin beta satu hari dari Teknium (co-founder Nous Research). Sekarang sudah **bundled dan default-on** di Hermes Desktop sejak v0.20.3. Di YouTube sudah muncul demo nyata: satu game dibangun tim 5 agent (1 orchestrator + 4 worker specialist) yang berkomunikasi lewat agent inbox.

## ⚡ 3 Hal Praktis yang Bisa Kamu Coba Hari Ini

1. **Update ke versi terbaru** — jalankan `hermes update` dan cek rilis di GitHub (tag `v2026.8.19`). Keyless web search langsung aktif tanpa setup API key.
2. **Coba Bot Mode di Hermes Desktop** — buat 2-3 bot dengan peran berbeda (riset → tulis → review), lalu kirim tugas via @mention. Mulai dari proyek kecil, misalnya riset topik sampai draft artikel.
3. **Eksplorasi command palette** — tekan Ctrl+P di CLI untuk berpindah model atau menjalankan perintah cepat; fitur ini baru dan sering jadi pintasan paling efisien.

## 🚀 Kenapa Ini Penting untuk Indonesia

Hermes Agent diklaim jadi proyek AI agent open-source dengan pertumbuhan tercepat 2026 — **0 ke 223.000+ GitHub stars dalam 5 bulan**, dengan ritme rilis 2-3 hari per patch. Buat developer dan builder di Indonesia, ini berarti framework serius dengan komunitas aktif, tanpa biaya lisensi, dan bisa dijalankan di laptop atau VPS sendiri. Dibanding Claude Code atau Codex yang proprietary, Hermes Agent memberi kendali penuh atas data dan konfigurasi — nilai plus besar buat yang peduli privasi dan biaya.

## Kesimpulan

Sepekan terakhir membuktikan Hermes Agent bergerak cepat: 4 rilis dalam 9 hari, Bot Mode jadi fitur utama, dan pengalaman pengguna makin mulus. Kalau kamu belum pernah mencoba AI agent open-source, sekarang waktu yang tepat — mulai dari web search tanpa API key, lalu eksperimen dengan tim bot-mu sendiri. Selamat mencoba, dan bagikan pengalamanmu di kolom komentar!

— Chokdi 🐷 · Content Studio · 2026