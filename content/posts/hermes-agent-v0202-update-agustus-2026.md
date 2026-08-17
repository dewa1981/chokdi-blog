---
title: "Hermes Agent v0.20.2 Resmi Rilis: Update Agustus 2026 untuk AI Agent Lokal"
date: 2026-08-17T09:40:00+07:00
draft: false
tags: ["AI Agent", "Hermes Agent", "Open Source", "Update"]
---

Hermes Agent, AI agent open-source dari Nous Research yang kini punya lebih dari 230.000 bintang di GitHub, baru saja merilis **v0.20.2 (v2026.8.16)** pada 16 Agustus 2026. Patch release ini merangkum sekitar **397 pull request** yang digabung sejak v0.20.1 — dan kabar baiknya, semua perbaikan itu bisa langsung dinikmati dengan satu perintah: `hermes update`.

Buat kamu yang belum kenal: Hermes Agent itu AI agent yang hidup di komputermu sendiri (bukan cloud orang lain), lisensi MIT, gratis, dan bisa nyambung ke Telegram, WhatsApp, Discord, sampai 21+ platform messaging. Update kemarin bikin dia makin matang.

## 🚀 Apa Saja yang Baru di v0.20.2?

Jendela rilis ini mencatat **~967 commit di ~1.279 file** (+128.522/−7.622 baris). Terlalu banyak buat disebut satu-satu, tapi ini highlight-nya:

- **Desktop app**: multi-gateway Connections registry, refresh per-profil, MCP health checks + deep links.
- **CLI**: Windows update probes, dukungan Kitty keyboard protocol, hardening untuk chat `-c`.
- **Gateway**: model routes yang tersimpan permanen, `/loop` completion, Telegram DM topics.
- **Prompt caching** untuk LiteLLM Claude di OpenAI wire — hemat token!
- **Cron hardening** + auth resolution lewat profile scopes.
- **Installer lebih robust** di Linux maupun Windows.

Catatan: release notes lengkap yang dikurasi bakal dibawa **v0.21.0** (dokumentasi lengkap dari v0.20.0 ke atas). Jadi v0.20.2 ini "stabil dulu, cerita lengkapnya menyusul".

## 🧠 Kenapa Hermes Berbeda dari AI Agent Lain?

Banyak tutorial sekarang sudah basi karena Hermes berkembang cepat. Yang bikin dia unik:

1. **Reflective Phase** — setelah tugas selesai, Hermes menulis "manual" untuk dirinya sendiri (file skill). Tugas serupa berikutnya langsung lebih cepat. Agent yang makin pintar sendiri setiap dipakai.
2. **A2A Protocol** — agent-to-agent: Hermes bisa menemukan agent lain, kirim pesan, dan orkestrasi kerja lintas mesin dengan access token + audit log.
3. **Memory sederhana tapi efektif** — dua file markdown kecil (memory + profil user) yang di-edit sendiri oleh agent, plus pencarian total riwayat percakapan di database lokal.

## ⚡ 3 Hal Praktis yang Langsung Dicoba

- **Mulai gateway-nya!** Setup hanya mengonfigurasi, TIDAK menjalankan. Bot diam = lupa menjalankan `hermes gateway` (atau `hermes gateway install` biar hidup terus).
- **Hemat token pakai `!`** — ketik `!` sebelum perintah shell = eksekusi instan tanpa memanggil model. Gratis token. Jaga `/context` seperti fuel gauge.
- **Pin model murah ke cron jobs** — pekerjaan semalam (monitor, briefing pagi) jangan bakar token flagship. Satu baris konfigurasi: model murah untuk pekerja, model pintar untuk perencana.

## 🔒 Soal Keamanan, Jangan Main-main

Agent ini bisa eksekusi perintah di mesinmu — perlakukan seperti itu. Empat aturan emas: (1) biarkan gateway default-deny dengan pairing code, jangan pernah ALLOW_ALL + akses terminal; (2) command approvals tetap di smart mode; (3) jalankan eksekusi di dalam Docker + egress proxy biar API key-mu tidak pernah bocor ke sandbox; (4) jangan pernah port-forward dashboard ke internet.

## ✅ Kesimpulan

v0.20.2 adalah patch release yang solid — bukan fitur gila, tapi ratusan perbaikan yang bikin Hermes makin nyaman dipakai harian. Kalau kamu sudah install: `hermes update`. Kalau belum: `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`. Komunitas Indonesia yang mau mulai serius dengan AI agent lokal, sekarang saatnya.

Sudah coba v0.20.2? Cerita di kolom komentar, yuk! 🐷

— Chokdi 🐷 · Content Studio · 2026
