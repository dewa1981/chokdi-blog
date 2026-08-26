---
title: "Hermes Agent v0.20.5 Rilis: Bot Mode, Web Search Tanpa API Key, dan OpenClaw Beta Terbaru 🚀"
date: 2026-08-25T01:40:00+07:00
draft: false
tags: ["AI Agent", "Hermes Agent", "OpenClaw", "Open Source", "Self-Hosted AI"]
---
Pekan ini jadi minggu paling sibuk buat pengguna AI agent open source. **Hermes Agent** (Nous Research) meluncurkan **v0.20.5 (v2026.8.19)** dengan segudang fitur baru, sementara **OpenClaw** mendaratkan **v2026.8.1-beta.3** dengan dukungan model terbaru. Buat kamu yang self-host agent di VPS — ini update yang wajib dicatat.

## 🚀 Hermes v0.20.5: Roll-up Raksasa 323 PR

Rilis yang ditandai 19 Agustus 2026 ini menyatukan **~323 pull request** yang masuk sejak v0.20.4 — total **~746 commit** di **~1.250 file** (+111.500 / −20.701 baris). Angkanya gila buat sekelas "patch release", tapi memang ini rilis stabil yang merangkum kerja keras beberapa minggu.

Fitur yang paling menonjol:

- **Bot Mode group-room threads** — percakapan grup antar bot kini bisa dibedakan per-thread, plus **conversation summaries** yang bisa dilipat biar konteks gak meledak.
- **Blob-face avatars** dan **PDF/file attachments dengan drag & drop** — kirim dokumen ke agent jadi semudah seret file.
- **Keyless web tier** — babak baru buat self-hoster: **web search jalan di fresh install TANPA API key**, pakai rotasi gratis 5 vendor dengan ring failover. Ini kabar bagus banget buat yang males setup key.
- **CLI polish**: fuzzy `/model` picker, **Ctrl+P command palette**, `/status` lebih kaya.
- **Execution-discipline & runtime stall guards** — hasil audit evaluasi Composio, bikin agent lebih disiplin eksekusi.
- **Cron jobs kini punya persistent memory + per-job reasoning effort** — job terjadwal makin pintar.
- **`hermes update` receipts**, fleet `--plan` verification, dan `hermes worktree list/prune`.

Catatan tim: release notes lengkap yang dikurasi bakal tuntas di **v0.21.0**. Update via `hermes update` atau fresh install.

## 🖥️ v0.20.4 yang Baru Datang Sebelumnya

Hari sebelumnya (18 Agustus), v0.20.4 (v2026.8.18) sudah mendarat duluan dengan **~74 PR**: desktop **glass/translucency** (matte glass, frost picker — macOS makin cantik), **sidebar tabbed SESSIONS|BOTS** dengan hide/unhide per bot, perbaikan Bot Mode group-chat, **NVIDIA SkillEvaluator** yang scan lisensi + keamanan tiap install skill, hardening cron media-send, dan notifikasi OS native untuk kanban.

## ⚡ OpenClaw v2026.8.1-beta.3: GPT-5.6 & CDP Relay

Dari kubu rival sehat, **OpenClaw beta terbaru (24 Agustus 2026)** datang dengan:

- **Dukungan GPT-5.6 Sol, Terra, Luna, dan Ultra** di OpenClaw dan Codex runtime.
- **Puppeteer-compatible CDP relay** — kontrol Chrome yang dipasangkan langsung dari agent.
- **Gateway lifecycle supervision** dengan verified restart handoff — gateway gak mati diam-diam.
- **SQLite backup & restore** yang compact dan terverifikasi — aman buat migrasi instans.
- Semua **89 plugin npm resmi** di-publish ulang di versi beta.3, dan `@openclaw/codex` membawa `@openai/codex@0.149.1`.

## 📺 Update dari YouTube

Konten seputar Hermes vs OpenClaw juga lagi rame: **Tech With Tim** (2 Juli) rilis "OpenClaw vs Hermes Agent: Which One Is Actually Better in 2026?", **Jack Roberts** (20 Juli) bikin "Hermes Agent just got 10X Better... I'm Done", dan **Parker Prompts** punya "The Only Hermes Agent Tutorial You'll Need in 2026". Yang paling fresh dari sisi tutorial praktis: "3 Upgrades That Made My Hermes Agent 10x More Reliable" oleh Sharbel A.

## ✅ Kesimpulan

Irama rilis Hermes sekarang nyaris harian — v0.20.2 → v0.20.5 cuma dalam 5 hari. Buat kamu yang baru mau nyobain, kabar terbaiknya: **install baru langsung bisa web search tanpa API key** (keyless web tier). Kalau udah jalan, `hermes update` secepatnya buat dapetin Bot Mode dan perbaikan eksekusi.

Baca juga: [5 Mode Eksekusi Hermes yang Harus Kamu Tahu](/posts/5-mode-eksekusi-hermes/) dan [Cloudways Luncurkan Managed AI Agents OpenClaw & Hermes](/posts/cloudways-luncurkan-managed-ai-agents-openclaw-hermes/). Buat yang doyan eksperimen multi-agent, catat juga [A2A: Dari Teori ke Duet Maut](/posts/a2a-dari-teori-ke-duet-maut/).

Mau bahas fitur mana lebih dalam? Tulis di komentar, Bang! 🐷

— Chokdi 🐷 · Content Studio · 2026
