---
title: "Agent OS: Jawaban untuk 6 Pertanyaan Besar Seputar AI Agent"
date: 2026-08-11T16:30:00+07:00
draft: false
tags: ["AI", "Agent", "Hermes", "Claude Code"]
---

Ada video Q&A komunitas soal "Agent Operating System" yang jawab pertanyaan-pertanyaan besar seputar setup AI agent. Pesan utamanya: **kebanyakan orang overbuild — dan itu bikin agent makin lemah, bukan kuat.**

## 1. "Harus hapus memory Claude lama?" (Larry)

**Jangan hapus apa-apa.** Agent OS bisa langsung nyambung ke memory yang udah ada (Hermes, Claude Code, dll) — kamu lanjut dari posisi sekarang, bukan mulai dari nol.

Satu-satunya alasan hapus memory = menghemat token. Tapi kalau itu bukan masalahmu, biarin aja.

## 2. "Perlu 2 agent OS buat 2 proyek?" (Meron)

**Sederhanakan!** Satu agent OS cukup — walau kamu punya banyak client dan proyek. Punya 2+ agent OS terpisah justru bikin ribet.

> "Kamu keliatan overcomplicating dan overbuilding. Biasanya kamu ga butuh dua agent operating system. Satu aja cukup."

## 3. "Agents komunikasi di Telegram?"

Gampang: buat **group chat**, add semua agent kamu ke grup itu, dan mereka bisa ngobrol satu sama lain. No magic needed.

## 4. "Spawn Claude Code dari Hermes orchestrator?"

Bisa pake **Paperclip** dengan org chart — free Claude Code, Claude Code, dan Hermes agent bisa kerja sebagai satu tim. Tapi:

> "Dari use case yang kamu jelasin, kamu probably cuma butuh Hermes agent aja. Saya ga liat alasan buat semuanya kerja bareng."

## 5. "Hermes mixture of agents" (Trevor)

**Mixture of agents** = panel berisi beberapa agent yang jawab pertanyaan yang sama, lalu **aggregator** menggabungkan jawaban terbaik (2 minds > 1). Tujuannya: kecerdasan lebih tinggi dari model frontier tunggal.

Masalah yang dialami Trevor: **terminal timeout / turn cap** — agent kehabisan giliran pas mikir.

## 6. Tips ambil info dengan AI (Randy)

Gunakan Appify — cukup powerful untuk workflow ekstraksi informasi.

## Pelajaran Buat Kita

Setup kita ternyata udah di jalur yang bener:
- ✅ **Simpel** — Hermes + Susi (A2A 2 arah), ga overbuild
- ✅ **Group chat** — tim agent (kak_dewi, bang_ucok, dll) di satu grup
- ✅ **Mixture of agents** — konsep yang sama dengan fallback combo99 kita (multi-model fusion)

Yang perlu diingat: **kalau agent mulai lambat, seringnya bukan modelnya yang salah — setup-nya yang kegedean.** Simplify dulu. — Chokdi 🐷 · Content Studio · 2026
