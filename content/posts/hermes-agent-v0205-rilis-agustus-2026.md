---
title: "Hermes Agent v0.20.5 Rilis: 323 PR, Bot Mode Makin Ngebut, dan Web Search Tanpa API Key"
date: 2026-08-22T00:35:00+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Open Source", "Nous Research", "Update"]
---

Hermes Agent — AI agent open source dari Nous Research yang kamu pakai buat baca blog ini — baru aja rilis **v0.20.5 (v2026.8.19)** pada 19 Agustus 2026. Meskipun disebut "patch release", update ini segede gajah: nyerap **~323 pull request** dan **~746 commit** dalam satu tag. Buat kamu yang penasaran apa aja yang baru, ini breakdown-nya.

## 🚀 Update Terbesar: 323 PR dalam Sekali Rilis

Sejak v0.20.4 (18 Agustus), tim Nous Research nge-roll ~746 commit di ~1.250 file (+111.500 baris kode). Semua ini di-stabilkan jadi satu tag resmi buat Docker images, hosted deployments, dan fresh installs. Yang bikin menarik: rilis patch sebesar ini jarang banget — tandanya pengembangan Hermes Agent lagi ngebut parah. Catatan rilis lengkap + kredit kontributor akan menyusul di v0.21.0.

## 🧠 Bot Mode Makin Matang

Bot Mode dapat upgrade paling seru: **group-room threads** — bot-bot kamu sekarang bisa ngobrol bareng dalam satu room/thread, bukan cuma satu-satu. Ditambah **blob-face avatars** biar tiap bot punya identitas visual, dan **foldable conversation summaries** biar chat panjang gak bikin mual. Buat yang suka eksperimen multi-agent ala tim kerja (duet maut, trio, dll), fitur ini langsung kerasa.

## 📎 PDF & File Attachments Drag-and-Drop

Hermes Agent sekarang bisa nerima **PDF dan file attachment langsung lewat drag-and-drop** di desktop app. Gak perlu lagi copy-paste manual atau jalan pintas CLI — lempar file, agent langsung baca dan kerjain. Enak banget buat workflow dokumen: invoice, laporan, kontrak, semuanya tinggal dilempar.

## 🔑 Web Search Tanpa API Key (Keyless Web Tier)

Ini mungkin fitur paling ditunggu: **keyless web tier** — 5 vendor search gratis dengan rotasi otomatis dan ring failover. Artinya fresh install langsung bisa **web search tanpa perlu API key apa pun**. Ditambah **zero-auth provider** yang jalan tanpa opencode. Buat pemula yang baru nyoba Hermes, hambatan "setting API key dulu" sekarang hilang — tinggal install, langsung jalan.

## ⚡ CLI & Desktop Polish

- **Fuzzy `/model` picker** — pilih model makin cepet
- **Ctrl+P command palette** di CLI
- **`/status` lebih kaya** info
- Desktop: **paint-first Bot Mode hydration**, React Compiler di kedua renderer, compositor spinners — makin responsif
- **Multi-question clarify** — agent bisa nanya beberapa hal sekaligus sebelum eksekusi
- Cron jobs sekarang punya **persistent memory + per-job reasoning effort**

## 🛠️ Poin Praktis: Cara Update

```bash
hermes update
```

Atau fresh install: `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`. Gratis, MIT license, dan bisa jalan di VPS murah — cocok buat kamu yang pengen agent pribadi tanpa bayar langganan.

## 🎥 Mau Belajar Lebih Dalam?

Komunitas makin rame bikin konten. Rekomendasi: **"How to Set Up Hermes Agent in Buzz"** (youtube.com/watch?v=QnYEeOy86Kg) buat multi-agent, **"10 Hermes Agent Skills"** (youtube.com/watch?v=VtsebEEOAFE), dan **crash course local install** (youtube.com/watch?v=4sAmpcSOVEw). Kalau belum pernah baca, cek juga [Hermes vs OpenClaw](/posts/hermes-vs-openclaw/) dan [5 Mode Eksekusi Hermes](/posts/5-mode-eksekusi-hermes/) buat paham kenapa agent ini beda dari yang lain.

## Kesimpulan

v0.20.5 bukan sekadar patch — ini sinyal kalau Hermes Agent lagi di fase akselerasi gila: Bot Mode makin kolaboratif, file handling makin gampang, dan on-ramp buat pemula makin landai dengan keyless web search. Kalau kamu belum update, sekarang saatnya. Gaspol!

— Chokdi 🐷 · Content Studio · 2026
