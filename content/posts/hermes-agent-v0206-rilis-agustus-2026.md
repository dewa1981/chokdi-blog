---
title: "Hermes Agent v0.20.6 Rilis: 525 PR Baru, Bot Mode Makin Matang"
date: 2026-08-29T09:30:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Tutorial"]
---

Hermes Agent dari Nous Research baru saja merilis versi terbaru **v0.20.6 (v2026.8.27)** — cuma dua hari lalu. Ini patch release yang merangkum **~525 pull request** dalam satu minggu terakhir, dan buat kamu yang sudah pakai Hermes atau baru kepo soal AI agent open-source, update ini layak banget dilirik. Artikel ini ngasih kamu ringkasan fitur paling penting + cara update-nya, singkat dan praktis.

## 🚀 Apa Saja yang Baru di v0.20.6?

Release kali ini besar banget: **~1.313 commit** di **~1.557 file** (+177 ribu baris kode baru) sejak v0.20.5. Buat konteks, repo-nya sekarang sudah mengumpulkan **238 ribu bintang GitHub** dengan 48 ribu fork — salah satu proyek AI open-source paling ramai saat ini.

Fitur unggulan di rilis ini:

- **Consent-gated real-profile browsing** — Hermes Desktop sekarang bisa pakai profil Chromium bawaan kamu buat browsing, dengan alur approval saat tutup browser di Windows.
- **Desktop Browser punya jendela OS sendiri** + mesin update SSH remote dan "fleet profile rail" buat yang kelola banyak mesin.
- **Katalog MCP melebar: 50+ server vendor live** — termasuk Cloudflare, Grafana Cloud, Better Stack, dan Railway. Artinya integrasi ke tool eksternal makin gampang, tinggal colok.
- **TTL result caching** untuk `web_search`/`web_extract` — hasil pencarian di-cache sementara, hemat token dan makin cepat.
- **Lean-tail compression jadi default** — percakapan panjang dipadatkan lebih efisien.
- **Enkripsi secret via OS keychain** (opsional) — tidak ada lagi prompt Keychain tiap kali buka app di macOS.
- **Updater pause gateway via control socket** — tidak lagi "tree-kill" proses secara brutal; update lebih mulus.
- **Model baru**: GLM-5.3-Flash, MiniMax M3 (gratis!), dan MiniMax H3 Max buat video.

## 🤖 Bot Mode: Satu Profil = Satu "Tim"

Yang paling ramai dibicarakan bukan dari rilis ini, tapi fitur **Bot Mode** yang resmi jadi bawaan (default-on) di Hermes Desktop sejak v0.20.3. Konsepnya sederhana tapi kuat: **satu bot = satu Hermes profile**, lengkap dengan chat, memori, skill, dan model pin-nya sendiri.

- Bot saling kirim pesan lewat **Agent Inbox** yang persisten, dan oper pekerjaan pakai `@mention` — misal `@researcher have a look at this`.
- Bisa bikin **group chat 2–6 bot** dalam satu room, tiap pesan memicu sampai 3 ronde respons bergiliran.
- Avatar kustom: bentuk geometris 7 macam, 10 warna, upload gambar sendiri, atau "pixel pet" yang matanya ikut scan saat bot bekerja.
- Semua berbasis profil Hermes biasa — jadi transparan, bisa di-edit, dan **MIT license, gratis**.

Pola pemakaian yang kepake banget: bot research yang di-pin ke model reasoning + bot writer di model murah, lalu handoff berantai scout → reviewer → publisher. Cocok buat solo developer atau tim kecil yang mau "asisten virtual ber-rombongan".

## 🧠 Kenapa Hermes Berbeda? "Agent That Grows With You"

Dalam talk-nya di **Arize Observe 2026** (YouTube), Sam Herring dari Nous Research cerita kalau Hermes Agent lahir dari kebutuhan internal: agent CLI-first yang bisa dipakai dalam sesi jangka panjang, dengan **memori bertingkat (tiered memory)** supaya tidak lupa konteks pekerjaan yang sudah dilakukan. Dia juga blak-blakan: Hermes dibuat sebagai "OpenClaw competitor" — bedanya, fokus ke stabilitas memori dan kontrol penuh di tangan user. Karena itu tagline-nya "the agent that grows with you".

Buat kamu yang baru mulai: Hermes menang di **transparansi** — semua profil, memori, dan skill adalah file lokal yang bisa kamu pegang dan edit langsung.

## ⚡ Cara Update

```bash
hermes update
```

Atau instalasi baru dari nol:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

## ✅ Kesimpulan

Hermes Agent v0.20.6 adalah update "pemantapan": ratusan PR digulung jadi satu rilis stabil, fitur Bot Mode makin matang, katalog MCP melebar, dan banyak perbaikan kualitas hidup (caching, enkripsi, update yang lebih aman). Buat pengguna di Indonesia — baik yang pakai model gratis seperti MiniMax M3, atau yang mau eksperimen multi-agent — sekarang adalah waktu yang pas buat update dan coba Bot Mode.

Punya pengalaman pakai Hermes Agent? Tulis di kolom komentar ya!

— Chokdi 🐷 · Content Studio · 2026
