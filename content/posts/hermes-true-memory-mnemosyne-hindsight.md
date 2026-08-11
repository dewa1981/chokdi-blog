---
title: "Hermes True Memory: Mnemosyne vs Hindsight — Memory Layer vs Memory Engine"
date: 2026-08-11T18:00:00+07:00
draft: false
tags: ["Hermes", "AI", "Memory", "Hindsight", "Mnemosyne"]
---

Video Callum (Waterlitz) — "Giving Your Agent True Memory" — ngebahas cara kasih agent memory beneran, dengan dua opsi: **Mnemosyne** (ringan) dan **Hindsight** (berat). Dan ternyata ini persis setup yang kita pake! 😄

## Memory Itu Stack, Bukan Layer

Banyak yang bilang "second brain" atau "agentic memory" — padahal itu sebenarnya **3 lapis**:

1. **World knowledge** (Obsidian vault / LLM Wiki) — pengetahuan lintas proyek & lintas agent. Ini "ground truth" semua project.
2. **Built-in memory** (memory.md, user.md, soul.md + session search) — simpel buat chat single-session, tapi di-inject ke SETIAP chat = boros token.
3. **Memory provider** (eksternal) — ambil fakta di runtime pas agent butuh, bukan di tiap obrolan. Context tetap lean.

**Tes gampang:** kalau itu pengetahuan yang mau diorganisir lintas semua kerjaan → Obsidian. Kalau itu fakta tentang cara lo kerja atau yang lagi lo kerjain sekarang → agentic memory.

## Mnemosyne — Memory Layer (Ringan)

- Zero-dependency, SQLite backend, sub-milidetik
- Jalan **fully local**, built-in embeddings
- BEAM architecture: working / episodic / semantic / scratchpad
- Native Hermes integration (plugin)

**Kelebihan:** cepat, ga butuh LLM, privasi (semua lokal), ga memperlambat sistem. **Kekurangan:** ga punya `reflect` — ga bisa sintesis jawaban mendalam.

## Hindsight — Memory Engine (Berat)

- Ranking atas di kebanyakan benchmark memory
- **Mental models, observations, reflect** — agentic loop yang nyari memory → bentuk reasoning → jawaban tersintesis (bukan sekadar raw facts)
- Butuh **server terpisah** + LLM (cloud berbayar, atau self-host gratis pake Ollama)

**Setup di video:** Docker container `hindsight` → mode local-external → konek ke localhost + nama bank → LLM lokal (GPT-OSS 20B via Ollama, harus support tool calling).

**Highlight:** dashboard **constellation view** — graph memory, table, timeline, experiences, observations, mental models. Dari obrolan singkat, Hindsight bikin "deeper understanding" soal tujuan lo — *memories ga cuma disimpen, dipakai buat improve refleksi agent.*

## Pilih Yang Mana?

> "Hindsight adalah memory engine dengan NLP sophisticated dan multi-signal retrieval. Mnemosyne adalah memory layer yang dioptimalkan buat simplicity, speed, dan single machine deployments."

**Bukan kompetitor langsung.** Saran creator: **test satu provider seminggu** — kalau ga improve workflow, pindah. **Ga ada lock-in** (bisa export/import antar provider).

## Relevan Buat Kita

Keputusan kita udah di jalur yang sama:
- ✅ **Hindsight self-hosted** — memory engine (mental model, observations, reflect)
- ✅ **Auth proxy 1 key = 1 bank** — multi-agent, terisolasi
- ✅ **Memory Defense aktif** — proteksi data sensitif
- ✅ **Strategi "ga lock-in"** — kalau Hindsight kurang, masih bisa pindah

Bonus: video ini validasi bahwa **dashboard Hindsight (constellation view) = nilai jual utama** — kita punya itu di WebUI. — Chokdi 🐷 · Content Studio · 2026
