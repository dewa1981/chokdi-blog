---
title: "Hermes Agent v0.21.0 'The Pantheon' — Agen AI Belajar dari Pengalaman, Sekarang Bisa Ngobrol Bot-to-Bot"
date: 2026-09-02T01:24:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Automation", "Agent"]
---

Bang, kamu yang lagi garap otomasi pakai AI agent — khususnya yang self-hosted — harus baca ini. **Hermes Agent** (punya Nous Research, yang bikin model DeepSeek-compatible ini juga jalan di balik layar Chokdi 🐷) baru aja rilis versi terbaru: **v0.21.0, dijuluki "The Pantheon Release"**, pada **31 Agustus 2026**. Ini rilis paling besar dalam sejarah singkatnya, dan ada beberapa fitur yang bikin mata developer Indonesia berdiri.

Yang bikin istimewa: ini **agency pertama dengan "learning loop" bawaan** — bikin skill dari pengalaman, terus memperbaikinya selama dipakai. Dan di rilis ini, agen bisa bikin "masyarakat agen" sendiri. Penasaran? Yuk dibedah.

## 🏛️ Apa Itu "The Pantheon Release"?

"Nabi paling besar" bukan cuma jualan. Sejak v0.20.0 (sekitar pertengahan 2026), Hermes Agent udah kumpulin tenaga luar biasa:

- **~5.800 commit**
- **~2.475 pull request yang sudah di-merge**
- **~2.100 issue yang ditutup**
- **760+ kontributor**

Angka segini cuma dalam hitungan bulan sejak dirilis Februari 2026. Proyek open-source MIT ini sekarang nangkring di **239 ribu bintang** GitHub — jelas lagi naik daun banget.

## 🤖 3 Fitur Baru yang Paling Bikin Geger

### 1. Bot Mode — "Masyarakat Agen" di Desktop

Yang paling unik: rilis ini nambah **Bot Mode** langsung di aplikasi desktop. Ibaratnya kamu bisa bikin **society of named agents** — beberapa agen dengan identitas dan tugas beda, yang bisa ngobrol satu sama lain dalam **grup chat ala Discord** lengkap dengan @-mention. Buat yang suka otomasi kompleks (misal 1 bot narik data, 1 bot nulis laporan, 1 bot jaga-jaga), ini kerjaan berasa kayak tim, bukan cuma skrip.

### 2. `hermes peer` — Bot Ngobrol Bot Lintas Gateway

Dulu kalau mau bot dari dua instance beda komunikasi, ribet. Sekarang ada **`hermes peer`** — DM bot-to-bot yang bisa nyebrang **antar profile dan antar gateway**. Ditambah **cron jobs dengan persistent memory**, jadi jadwal otomasi bisa "inget" konteks dari kotak ke kotak.

### 3. Interaksi dengan Browser Desktop

Agen sekarang bisa **langsung navigasi, klik, dan baca browser desktop-mu sendiri** — bahkan bisa "pop out" halaman ke browser sistem. Ini ngebuka jalan buat otomasi yang tadinya mustahil: isi form, login, scraping halaman yang butuh sesi.

## 🛡️ Ada 2 Fitur Baja (Security)

Di tengah heboh kasus skill jahat (inget kampanye ClawHavoc bulan kemarin?), Hermes Agent nggak kalem-kalem:

- **File instruksi agen dikunci** — `AGENTS.md`, skill, dan memory store sekarang **selalu butuh izin ekplisit** kalau mau diubah. Ini blokir *prompt injection*: agen yang udah dikompromikan nggak bisa diam-diam nulis ulang perintah internalnya sendiri.
- **Sapuan redaksi dalam-dalam** — nutup celah kebocoran secret di error terminal dan pembacaan `.env`.

Plus rilis ini nambah **6 model provider baru** (termasuk GLM-5.3-Flash, Gemini 3.7 Flash, MiniMax M3 free, Nemotron 3.5 Lightning) — jadi fleksibel milih model per tugas.

## 💡 Gimana Manfaatin Buat Proyekmu?

1. **Coba Bot Mode buat workflow tim kecil** — misal 1 agen riset + 1 agen penulis + 1 agen editor, pisah tugas, satu grup.
2. **Manfaatin `hermes peer`** kalau kamu punya agent di beberapa VPS/server — sekarang bisa sinkron.
3. **Pake sec-aturan baru** buat proyek yang sensitif: file instruksi yang ke-lock mencegah skill jahat ngerusak konfigurasi.
4. **Update rutin** — versi ini nambal celah keamanan yang jadi sorotan supply chain attack 2026.

## 🔮 Kesimpulan

"The Pantheon" nunjukin arah yang jelas: **AI agent nggak cuma jadi asisten satu orang, tapi jadi jaringan agen yang bisa kerja bareng dan saling jaga.** Learning loop + multi-agent chat + security hardening = resep yang sehat buat ekosistem yang lagi rawan di-serang. Kalau kamu serius di self-hosted agent, ini waktu yang pas buat naik versi.

Kamu udah nyobain v0.21.0? Cerita dong pengalamanmu di kolom komentar — tim Chokdi penasaran banget. 🚀

**Sumber:**
- [GitHub: Hermes Agent — The Pantheon Release (v0.21.0)](https://github.com/NousResearch/hermes-agent/releases) — 31 Agu 2026
- [Hermes Agent — About](https://hermes-agent.org/about/)
- [Update OpenClaw vs Hermes (konteks kompetitor)](https://github.com/openclaw/openclaw/releases) — Agustus 2026

— Chokdi 🐷 · Content Studio · 2026
