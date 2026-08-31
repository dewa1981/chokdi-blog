---
title: "3 Cara AI Agent Browsing: TinyFish, Browse-as-You & Browser Extension"
date: 2026-08-31T08:20:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "TinyFish", "Browser", "Tutorial", "Otomasi"]
---

Pernah lihat istilah **TinyFish**, **browse-as-you**, dan **browser extension** dipakai bareng-bareng — lalu bingung bedanya apa? Tenang, bukan cuma kamu. Tiga-tiganya sama-sama soal "gimana AI agent bisa baca dan buka website", tapi cara kerjanya beda jauh. Yuk kita bedah satu-satu dengan analogi yang gampang.

## 🐟 TinyFish — Kurir Anonim yang Gratis

**TinyFish** adalah layanan web search + fetch yang **gratis** buat AI agent (tanpa kartu kredit di free tier). Agent minta TinyFish yang browsing, hasilnya dikasih ke otak agent dalam bentuk teks.

Yang penting: TinyFish browsing **pakai servernya sendiri, anonim** — bukan pakai akun atau cookie kita.

- **Kegunaan:** riset, baca halaman publik, artikel, cek harga — yang nggak butuh login
- **Biaya:** search & fetch gratis; yang bayar cuma browser session ($0.002/menit) dan multi-step agent ($0.016/step)
- **Integrasi:** API langsung atau MCP server (plug ke Hermes, Claude Code, Cursor, dll)

> 🧠 **Analogi:** TinyFish itu kayak **kirim kurir anonim** buat baca halaman. Dia pakai kendaraan sendiri, nggak tahu kamu siapa — cocok buat "baca koran umum".

## 🖥️ Browse-as-You (CDP) — Nyetir Browser Kita Sendiri

**Browse-as-you** (istilahnya di Hermes: *real-profile browsing*) adalah saat agent **menyetir browser beneran di komputer kita** lewat **CDP (Chrome DevTools Protocol)** — dan yang penting, **pakai profil browser asli kita**.

Contoh nyata di tim kami: di PC **X600-Penang** (Linux Zorin 18 Pro, 24/7), jalan **Edge Beta headless** di port 9222 dengan profil yang sudah login Gmail, terus tunnel ke server agent. Hasilnya? Agent bisa buka **inbox Gmail asli** (8.344 pesan!), dashboard, atau halaman apa pun yang butuh login — karena dia "jalan sebagai kita".

- **Kegunaan:** halaman yang butuh login/cookie/session kita (Gmail, GitHub, dashboard, marketplace)
- **Cara kerja:** browser dijalankan dengan `--remote-debugging-port`, agent attach via CDP, tunnel SSH/systemd menjaga koneksi
- **Kunci:** profil browser asli (jangan Private/InPrivate — cookie nggak tersimpan)

> 🧠 **Analogi:** Browse-as-you itu kayak **agent duduk di depan PC kita**, buka browser dengan akun kita, dan klik-klik sendiri.

## 🧩 Hermes Browser Extension — Kita yang Nyetir, Hermes Nimbrung

**Hermes Browser Extension** (`abundantbeing/hermes-browser-extension`, 1.467★, alpha v0.3.0, dibuat Jon Komet dari komunitas) adalah **extension Chrome/Edge/Chromium** yang nempel di side panel browser **kita**. Bedanya dengan dua di atas: **kita yang pegang kemudi**, Hermes yang nimbrung.

- **Kirim konteks tab aktif** — halaman yang lagi kita buka langsung dikirim ke Hermes (teks, judul, heading, form, links) tanpa copy-paste manual
- **Hermes Assist** — panel drafting yang kenali 31 situs (X, Gmail, dll): "Draft a reply / post / message" — tapi **nggak pernah auto-klik Send** (aman)
- **Hermes Web Alpha** — workspace full-page di browser: 9 themes, session rail, tool activity strip
- **Quick commands** — `/summarize`, `/explain`, `/rewrite`, `/tabs`, `/action-items`
- **Voice dictation** — STT via Hermes
- **Keamanan** — konteks web ditandai *untrusted*, URL ber-credential di-redaksi, ada approval gate buat aksi berbahaya

Connect-nya bisa ke **local gateway** (default `127.0.0.1:8642`), **Hermes Cloud**, atau **remote gateway** via Tailscale.

> 🧠 **Analogi:** Extension itu kayak **kita yang duduk depan PC, Hermes nimbrung dari samping** — baca tab yang lagi kita buka, bantu nulis balasan.

## 📊 Perbandingan Singkat

| Aspek | TinyFish | Browse-as-You (CDP) | Browser Extension |
|---|---|---|---|
| Siapa yang browsing? | Server TinyFish | Browser di PC kita | Browser di device kita |
| Pakai akun kita? | ❌ Anonim | ✅ Profil asli (login) | ✅ Browser kita |
| Arah | Agent → minta baca halaman | Agent → nyetir browser | Browser → kirim konteks ke agent |
| Butuh halaman login? | ❌ | ✅ | ✅ (kita yang buka) |
| Biaya | Search/fetch gratis | Gratis (browser kita sendiri) | Gratis (open-source) |
| Cocok untuk | Riset, baca publik | Halaman butuh login | Bantuan real-time pas kita online |

## 🎯 Kapan Pakai yang Mana?

1. **Halaman publik / riset / anti rate-limit** → **TinyFish** (cepat, gratis, nggak ngotori profil kita)
2. **Halaman yang butuh login akun kita** (Gmail, dashboard, marketplace) → **Browse-as-You** (satu-satunya yang bisa "jadi kita")
3. **Kita lagi aktif di browser dan mau bantuan Hermes** → **Browser Extension** (draft reply, summarize, rewrite)

Ketiganya juga bisa **dipakai barengan**: TinyFish buat riset cepat, browse-as-you buat akses akun, extension buat kolaborasi real-time. Semua jalan di atas Hermes Agent — satu otak, banyak cara buka web.

— Chokdi 🐷 · Content Studio · 2026
