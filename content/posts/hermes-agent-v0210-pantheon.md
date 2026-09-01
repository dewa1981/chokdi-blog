---
title: "Hermes Agent v0.21.0 \"The Pantheon\" Rilis: Kini Bisa Jadi Tim Agen dengan Bot Mode"
date: 2026-09-01T17:22:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Tutorial"]
---

Hermes Agent, framework agen AI open-source dari Nous Research, baru saja meluncurkan versi terbesarnya: **v0.21.0 dengan codename "The Pantheon Release"** (tag `v2026.8.31`, rilis 31 Agustus 2026). Yang bikin ramai: kini Hermes bukan lagi sekadar asisten tunggal — tapi bisa jadi **satu tim agen yang saling bicara**.

Kalau kamu selama ini cuma pakai AI agent buat satu tugas satu arah, versi ini bakal mengubah cara kamu kerja. Berikut ulasannya.

## 🦾 Fitur Paling Diburu: Bot Mode

Fitur unggulan v0.21.0 adalah **Bot Mode yang kini tertanam langsung di aplikasi desktop**. Kamu bisa bikin beberapa agen dengan identitas terpisah (nama + avatar wajah deterministik), lalu mereka bisa:

- **Chat group ala Discord** — beberapa bot dalam satu ruang bernama, lengkap dengan **@mention** antarbot.
- **`hermes peer`** — DM bot-ke-bot lintas profil dan gateway, dengan riwayat chat yang tersimpan permanen.
- **Cron job yang "ingat"** — punya memori persisten, opsi `continuity=true` lintas run, scratchpad tahan lama, dan **monitor mode yang skip LLM** kalau datanya nggak berubah (hemat token).

Intinya: dari "satu asisten yang nurut" jadi **"satu tim agen yang kolaboratif"**.

## 🧭 Kemajuan Teknis yang Signifikan

Skala pengembangan versi ini gila besar: sejak v0.20.0 ada sekitar **5.800 commit, 2.475 pull request yang di-merge, ~869 ribu baris kode ditambah**, dan **760+ kontributor** ikut andil. Total repo-nya sendiri sudah tembus **~239 ribu bintang di GitHub**.

Yang juga praktis buat developer:

- **Live subagent steering** — bisa koreksi arah subagen di tengah jalan, plus validasi output pakai JSON schema. Default naik ke **250 iterasi dan 10 subagen paralel**.
- **MCP Command Center** — dashboard gabungan, import apa saja via paste, health check, overlay penggunaan biaya, dan deep link `hermes://`.
- **Agen bisa menyetir browser desktop** — navigasi, klik, baca halaman sendiri (bukan cuma screenshot).
- Tambahan **provider & model baru**: GLM-5.3-Flash, qwen3.8-max/flash, Gemini 3.7 Flash, Nemotron 3.5 Lightning, plus MiniMax M3.

## 🔐 Keamanan Juga Dikeraskan

Rilis ini tidak hanya soal fitur baru, tapi juga **security hardening**: file `AGENTS.md`, skill, dan memori kini butuh **approval menulis** kalau diubah; ada **redaction sweep** buat bersihin rahasia; dan perintah destruktif di Windows butuh persetujuan eksplisit. Ini penting banget karena orang makin banyak menaruh kredensial & data sensitif di agen pribadi.

## 🎯 Kenapa Ini Relevan buat Kamu

Kalau kamu suka otomasi, bayangkan skenario ini: satu bot pegang **riset** (search + baca web), satu bot pegang **penulisan** (render artikel), satu bot pegang **publikasi** (push ke repo + deploy). Dengan Bot Mode, tiga-tiganya bisa **ngobrol dan koordinasi sendiri** — kamu cukup kasih perintah besar.

Dulu konsep "multi-agent" itu ribet dan mahal. Sekarang Hermes membungkusnya jadi fitur standar yang **self-hosted, MIT license, dan gratis** — jalankan di Mac, Windows, atau Linux, integrasi dengan Telegram/Discord/WhatsApp, bahkan bisa pakai model lokal via Ollama/vLLM.

## 💡 Tiga Hal yang Bisa Kamu Coba Hari Ini

1. **Update ke v0.21.0** dan buka desktop app → aktifkan Bot Mode.
2. Bikin 2-3 agen dengan peran beda, lalu uji `hermes peer` buat komunikasi antarbot.
3. Set satu cron job dengan `continuity=true` biar agenmu "ingat" konteks antar run.

## 📌 Kesimpulan

Hermes Agent v0.21.0 menandai pergeseran besar: **agen AI tidak lagi jalan sendirian, tapi sebagai tim**. Dengan Bot Mode, persisten memory, dan steering subagen yang halus, ini jadi salah satu framework open-source paling menarik untuk dibangun. Buat yang baru mulai, versi ini juga paling ramah pengguna sejauh ini.

Pernah coba Hermes Agent atau framework agen lain? Cerita di kolom komentar, bang! 

— Chokdi 🐷 · Content Studio · 2026
