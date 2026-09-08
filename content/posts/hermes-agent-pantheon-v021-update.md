---
title: "Hermes Agent Update: Rilis Pantheon v0.21.0 dan Patch v0.21.1, AI Agent Berubah Jadi Tim Lengkap"
date: 2026-09-08T07:00:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Nous Research", "Open Source"]
---

Hermes Agent, AI agent open-source self-hosted besutan Nous Research, baru saja mengunci dua rilis besar dalam sepekan. Versi **v0.21.0 "Pantheon"** (31 Agustus 2026) membawa perubahan paling radikal sepanjang sejarahnya — agen tak lagi satu alat, tapi jadi "tim AI" yang bot-nya bisa saling kirim pesan. Disusul **v0.21.1 (patchnya, rilis 7 September 2026)** yang merangkum 632 pull request perbaikan. Ini kabar penting buat lo yang main AI agent di server sendiri maupun desktop.

## 🏛️ Panjang Umur "Pantheon": Agent jadi Masyarakat, Bukan Toolbox

Judul rilisnya pantas banget. Kalau sebelumnya Hermes adalah "utusan" yang ngomong satu arah, sekarang di v0.21.0 "the gods assemble" — para dewa berkumpul. Skalanya gede: sejak v0.20.0 ada **lebih dari 5.800 commit, sekitar 2.475 PR digabung, 2.100 isu ditutup, dan 760+ kontributor**.

Fitur utamanya yang bikin heboh:

* **Bot Mode kini built-in di desktop app** — tiap profil agent dapat nama, wajah avatar deterministik (bisa di-randomize/lock), dan tempat di roster bersama.
* **Group chat ala Discord** — bikin room berisi beberapa bot + lo sendiri, saling @-mention, kasih nama dan foto grup. Multi-agent yang tadinya ribet di-setup jadi kelihatan kayak aplikasi chat penuh rekan kerja.
* **`hermes peer` — DM bot-ke-bot** — agent bisa kirim pesan ke agent lain antar profil/gateway, dan jawabannya mendarat di Bot Chat masing-masing biar terekam dan bisa diperiksa, bukan cuma fire-and-forget.

## 🤖 Cron Job yang Ingatan, Subagent yang Bisa Dikendalikan

Dua hal yang paling terasa "hidup":

* **Cron jobs yang ingat** — job terjadwal nggak lagi "goldfish". Sekarang bisa `continuity=true` biar hasil run kemarin dibawa ke run besok (buat monitor yang dedupe laporan), dapat notepad scratchpad permanen, dan mode monitor pinter yang skip LLM kalau nggak ada yang berubah.
* **Subagent bisa di-steer live** — tool `delegate_task` naik kelas: bisa list anak yang lagi jalan, koreksi arah di tengah jalan, atau stop lebih awal dan simpan hasil parsial. Plus validasi output pakai JSON-schema, dan defaultnya naik ke 250 iterasi / 10 anak paralel.

## 🛠️ MCP Command Center, CLI Lebih Galak, dan Browser

* **MCP Command Center** — kelola 20-an MCP server dari satu dashboard: health check otomatis yang ngingetin lo re-auth sebelum tool gagal, overlay cost/usage per server, dan deep link `hermes://` buat install MCP server sekali konfirmasi.
* **CLI power wave** — Ctrl+P buka command palette fuzzy, `/model` bisa difilter sambil ketik, `/status` nunjukin reasoning mode + pending approval + context usage. Ada juga statistik cache-hit % dan token/detik. Malah ada **terminal pets**, biar si agent punya teman.
* **Agent nyetir browser desktop** — browser in-app yang tadinya cuma bisa dilihat, sekarang bisa dinavigasi, diklik, dan dibaca langsung oleh agent.

## 🔐 Keamanan Kian Ketat

Sebulan terakhir Hermes gencar numpuk pengamanan: file instruksi penting (AGENTS.md, skills, memory) sekarang **selalu butuh approval sebelum ditulis** — biar agent yang kena prompt injection nggak bisa diam-diam nulis ulang perintahnya sendiri. Ada juga sweep redaksi deep yang nutup kebocoran secret di terminal errors, `.env` reads, checkpoint, dan log ACP.

## 📦 v0.21.1: Patch Rillis 7 September

Terbaru, **Hermes Agent v0.21.1 (v2026.9.7)** rilis tanggal 7 September kemarin sebagai *patch release* yang merangkum kondisi `main` terkini sejak v0.21.0 — **632 PR sudah digabung** pada jendela rilis. Buat yang butuh versi stabil (Docker, hosted deployment, install baru), patch rollup kayak gini jadi andalan biar nggak ambil commit `main` yang masih mungkin mentah.

## Kesimpulan

Kalau lo masih pakai Hermes versi lama dan penasaran sama yang namanya "multi-agent tanpa pusing setup", rilis Pantheon ini momen yang pas buat upgrade — bot yang saling ngobrol, cron job yang ingat, dan subagent yang bisa diarahkan di tengah jalan adalah tiga fitur yang langsung ngubah cara kerja. Dan kabar baiknya, update tinggal `hermes update` dari terminal. Ada yang udah nyobain Bot Mode atau `hermes peer`? Cerita di kolom komentar, ya!

— Chokdi 🐷 · Content Studio · 2026
