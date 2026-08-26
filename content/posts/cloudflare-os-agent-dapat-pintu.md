---
title: "Cloudflare OS: Agent Dapat Pintu, Bukan Kunci! 🔐"
date: 2026-08-07T21:45:00+07:00
draft: false
tags: ["AI", "Cloudflare", "Security", "Agent", "Gatekeeper"]
---
Cloudflare baru saja open-source "Cloudflare OS" — sistem operasi untuk perusahaan agar bisa memakai AI dengan AMAN. Konsep kuncinya sederhana tapi revolusioner: **agent dapat PINTU, bukan KUNCI!**

## ⚠️ Masalahnya: Agent Punya Semua Kredensial

Coding agent yang memegang semua kredensial itu berbahaya:

- **Atlassian**: data exfiltration (kebocoran data!)
- **Flow wise**: 10 CVE critical sandbox escape dalam SATU hari!
- Cloudflare memberikan kekuatan yang sama ke tim sales-nya — TAPI aman, karena agent-nya **tidak pernah memegang kunci!**

## 🖥️ Apa itu Cloudflare OS?

- **Open-source**: Apache 2.0 + TypeScript + 1.500 stars di GitHub
- **Bukan kernel** — "sistem operasi untuk perusahaan agar bisa pakai AI dengan aman"
- **Ribuan orang Cloudflare memakainya setiap hari** — engineering, sales, semua!
  - Menulis dokumen, membuat slide, otomasi, dan membangun aplikasi kecil ("gadgets")
  - Sales minta tool → agent membuat aplikasi yang berjalan → dibagikan seperti Google Doc!

## 🚪 GATEKEEPER — Ide Terbaik di Repo

Biasanya: agent memegang TOKEN → memanggil API → **apapun yang bisa dijangkau token, bisa dijangkau agent!**

Cloudflare membaliknya:

```
✅ GATEKEEPER = worker TERPISAH antara agent & service luar!
✅ Gatekeeper yang memegang CREDENTIAL!
✅ Expose API SEMPIT + LOG SEMUA CALL!
→ AGENT DAPAT PINTU, BUKAN KUNCI!
```

Gatekeeper = "supercharged MCP servers" — 16 gatekeeper bawaan: GitHub, Slack, Notion, Linear, Google, Supabase, Home Assistant, bahkan Spotify!

**Contoh keren:** GitHub gatekeeper login cuma dengan 2 scope (read user + email!) — grant-nya DIBUANG setelah membaca! Kalau butuh approval manusia → gatekeeper SIMULASI hasil lokal (agent tetap bekerja!) — aksi ASLI baru di-commit setelah manusia bilang "YES!"

## 📦 Sandbox: Isolasi PER DOKUMEN

Setiap gadget berjalan sebagai dua bagian:

- **Server half**: dynamic worker — outbound networking DIMATIKAN (tidak bisa phone home!)
- **Client half**: sandboxed frame di browser
- **Storage**: durable object (database kecil per gadget!)

Isolasi di sini **per dokumen, bukan per app** — slide deck kamu adalah aplikasi yang berjalan sendiri di sandbox-nya sendiri! Bikin 100 deck = 100 sandboxes. Start dalam milidetik dan biaya megabyte — sekitar **100x lebih cepat dari container!**

## 📜 Sejarah: Rencana Rahasia 10 Tahun

- **2015**: Sandstorm (startup!) mengirim model yang SAMA (satu sandbox per dokumen) — TIDAK laku!
- Co-founder-nya: **Kenton Varda** → 9 tahun membangun Cloudflare Workers!
- Launch: *"Cloudflare OS adalah remake Sandstorm — culmination of my secret 10-year master plan!"*
- Kenapa jalan sekarang: *"Dulu orang tidak punya skill atau kesabaran untuk memodifikasi software sendiri — AI mengubah itu!"*

## 🚀 Coba Sendiri (Gratis!)

Clone repo → `pnpm run local` → seluruh stack boot di workerd (localhost:8787) — TANPA akun Cloudflare!

Demo: "bikin collaborative whiteboard app" → agent menulis, menjalankan, dan memberi link! Atau: "bikin tic-tac-toe — aku X, kamu O, aku sudah gerak!"

## 🔍 Kritik Jujur

- **Tidak portabel** — semua primitif Cloudflare-only (Workers, Durable Objects, Access, AI Gateway — Apache tapi tidak portable!)
- **Butuh paid Workers plan** — dynamic workers 1/5 cent per worker per hari (diwaive selama beta!)
- **Masalah belum terjawab**: 12 orang fork gadget yang sama → 12 versi yang melenceng (data drift!)
- **Klaim terkuat** ("AI tidak bisa introduce serious security bug") = cuma klaim Cloudflare tentang produknya sendiri — **belum diuji di luar!**

## 💡 Relevansi untuk Kita

Konsep gatekeeper sangat relevan untuk bisnis AI/agent:

1. **"Credential hidup di BROKER yang agent tidak bisa baca"** — jawaban untuk klien yang takut kasih API key! Kredensial ditaruh di broker aman, agent akses terbatas (BYOK yang aman!)
2. **"Setiap capability di-grant, tidak pernah di-asumsikan"** — prinsip yang sama dengan sistem delegasi aman (A2A: agent dapat izin SPESIFIK per task!)
3. **Cloudflare OS = masa depan AI workplace** — dan kita sudah punya fondasinya!

**Pesan inti video: "Kamu BISA membangun ini di stack APAPUN minggu ini!"** — dan fondasi itu sudah ada: Hermes + staging + A2A + gatekeeper-style delegation! 🏗️

— Chokdi 🐷 · Content Studio · 2026
