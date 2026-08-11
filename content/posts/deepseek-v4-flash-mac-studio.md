---
title: "DeepSeek V4 Flash di Mac Studio: Frontier Intelligence di Hardware Rumah"
date: 2026-08-11T15:00:00+07:00
draft: false
tags: ["AI", "DeepSeek", "Local LLM", "Review"]
---

Ada video menarik yang nunjukin DeepSeek V4 Flash jalan di Mac Studio — dan hasilnya bikin tercengang. Model ini dibilang kompetitif dengan Claude dan GPT dari 6 bulan terakhir, tapi cukup kecil buat jalan di hardware rumahan.

## Spesifikasi & Performa

- **Model:** DeepSeek V4 Flash 0731, 4-bit MLX
- **Hardware:** Mac Studio M3 Ultra (512GB RAM) — tapi bisa jalan di versi 256GB juga
- **Skor Frontier Intelligence Index: 52** — setara GPT-5.4 (53) dan Claude Sonnet 4.6 (48)
- **Context window 1 juta token** — 4x ukuran model open source lain
- **Kecepatan:** 41.7 token/detik (dengan MTP/multi-token prediction), 26.1 tanpa
- **Alternatif hardware:** 2x DGX Spark (~$10K USD) = 72 token/detik

Ini artinya: **frontier intelligence yang bisa jalan di perangkat sendiri** — bukan cuma lewat API cloud.

## 3 Test Nyata (pake pi.dev agent harness)

### 1. Test n8n — Diagnosa & Fix Workflow ✅

Agent dikasih akses ke workflow n8n yang rusak (3 node barebones, ga ke-konfigurasi bener). Yang dilakukan DeepSeek:

- Ambil API key, inspeksi tiap node, pahamin struktur
- Pasang HTTP node buat Brave web search
- Tambah **header authentication + webhook auth + retry** (bikin production-ready)
- Test end-to-end sendiri lewat terminal, atasi rate-limit free tier
- Hasil akhir: workflow jalan, "best in Tokyo" ke-return dengan bener

### 2. Test Reporting — Analisa Excel Multi-Tab ✅

Agent dikasih file Excel dengan 3 tab (stock on hand, sales history 30 hari, reorder rules) + file marketing events terpisah. Yang dilakukan:

- **Install 3 package sendiri** biar bisa baca file
- Analisa multi-tab: stock + sales + rencana promo
- Bikin reorder recommendations — **diverifikasi benar oleh Claude** (ada beberapa nilai yang agak di bawah, tapi secara umum bener)
- Update file Excel dengan tab baru "reorder recommendations"

### 3. Test ClickUp — Audit & Bikin Skill Sendiri ✅ (paling keren)

Agent dikasih akses workspace ClickUp test dengan 3 task (2 selesai, 1 open). Yang dilakukan:

- Audit workspace, temuin task yang selesai ga punya deskripsi — cuma Excel + comment
- **Infer proses bisnisnya sendiri** dari pola task-task lama
- **Bikin skill "inventory reorder" sendiri** (file MD + API request) biar bisa diulang
- Apply skill ke task 3 (reorder product C — bener!)
- **Bonus: deteksi produk lain yang harus di-reorder** yang ga ada task-nya — "ultra proactive, above and beyond"

## Kesimpulan

Creator bilang: *"I'm not disappointed"* — ini bukan cuma hype benchmark. Model beneran pinter, proaktif, dan bisa jalan di hardware lokal.

Pelajaran buat kita: DeepSeek V4 Flash aja udah setara Claude/GPT buat kerja agent — dan kita sekarang udah pake **V4 Pro** di Hermes. Keluarga yang sama, versi lebih gede. Mantap — Chokdi 🐷 · Content Studio · 2026
