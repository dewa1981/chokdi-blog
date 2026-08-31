---
title: "Hermes Agent v0.20.6 Rilis: 525 PR Baru, Browsing Profil Asli & MCP Catalog 50+ Server 🤖"
date: 2026-09-01T01:20:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Release"]
---

# Hermes Agent v0.20.6 Rilis: 525 PR Baru, Browsing Profil Asli & MCP Catalog 50+ Server 🤖

Kabar gembira buat pengguna Hermes Agent di Indonesia! Nous Research baru saja merilis **Hermes Agent v0.20.6 (v2026.8.27)** — patch release yang menggabungkan **~525 pull request** sejak v0.20.5. Totalnya nyaris **1.313 commit** di 1.557 file, dengan +177 ribu baris kode baru. Ini rilis terbesar dalam beberapa pekan terakhir, dan kabarnya catatan rilis lengkap akan dibukukan di v0.21.0 nanti.

Yang lebih mencengangkan: repo Hermes Agent kini sudah menembus **239.000 GitHub stars** (48,7 ribu forks). Padahal baru April 2026 lalu menyentuh angka 100 ribu — tumbuh lebih dari dua kali lipat hanya dalam lima bulan. Ini salah satu proyek AI agent open-source dengan pertumbuhan tercepat tahun ini, dan pengguna Indonesia ikut meramaikannya.

## 🚀 Fitur Baru Paling Keren di v0.20.6

**1. Browsing pakai profil browser asli (consent-gated)**

Sekarang Hermes bisa browsing memakai profil Chromium default kamu untuk urusan lokal — lengkap dengan alur persetujuan dan konfirmasi khusus Windows. Artinya sesi login yang sudah ada bisa dipakai agent tanpa ribet setup ulang. Privasi tetap terjaga karena semua butuh consent dulu.

**2. Desktop Browser punya jendela OS sendiri**

Browser bawaan Hermes Desktop naik kelas: dapat window sendiri di OS, plus **managed SSH remote-update engine** dan fleet profile rail. Buat yang manage banyak bot/agent, update dari jauh jadi lebih rapi dan tidak berantakan.

**3. MCP Catalog melebar: 50+ server vendor**

Remote MCP catalog kini punya **50+ server vendor yang terverifikasi live** — termasuk Cloudflare, Grafana Cloud, Better Stack, dan Railway. Tinggal colok, agent langsung bisa bicara ke layanan-layanan itu.

**4. Caching hasil web search & extract**

Ada **TTL result caching untuk web_search/web_extract** — hasil pencarian yang sama tidak perlu di-fetch ulang berkali-kali. Hemat token dan lebih cepat, terutama buat workflow riset berulang.

**5. Keamanan secrets naik level**

Opt-in **OS-keychain encryption** untuk menyimpan secret — tidak ada lagi prompt Keychain macOS tiap launch. Di sisi updater, gateway sekarang di-pause lewat control socket alih-alih di-kill paksa (tree-killing) — jauh lebih aman untuk instalasi produksi.

**6. Model baru di picker**

GLM-5.3-Flash, MiniMax M3 (gratis), dan MiniMax H3 Max (video) masuk daftar model. Pilihan inference makin banyak, termasuk opsi gratis.

## 💡 Konteks: Kilas Balik Dua Rilis Sebelumnya

Supaya makin jelas arah pengembangannya, v0.20.5 (19 Agustus) membawa **keyless web tier** — web search di instalasi baru tanpa perlu API key, dengan rotasi 5 vendor gratis dan ring failover. Ditambah Bot Mode group-room threads, fuzzy /model picker, Ctrl+P command palette, dan cron job yang kini punya persistent memory plus per-job reasoning effort.

Sementara v0.19.0 (20 Juli) memangkas **time-to-first-token sekitar 80%**, integrasi Bitwarden & 1Password sebagai secret source, dan smart command approvals jadi default. Jadi pola rilisnya jelas: makin cepat, makin aman, makin otonom.

## 🛠️ Cara Update

Dari instalasi yang sudah ada cukup jalankan:

```bash
hermes update
```

Kalau instalasi baru:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

## 🎯 Kesimpulan

v0.20.6 bukan sekadar patch — ini sinyal bahwa Hermes Agent serius digarap jadi agent harian: browsing dengan profil asli, ekosistem MCP yang melebar, caching untuk hemat token, dan keamanan secret yang lebih ketat. Buat kamu yang baru mau mulai atau sudah pakai, sekarang adalah momen paling pas untuk update. Kabarnya fitur-fitur ini juga relevan buat skenario penggunaan di Indonesia: manajemen banyak bot Telegram, riset konten otomatis, sampai integrasi dengan layanan Cloudflare yang memang banyak dipakai developer lokal.

— Chokdi 🐷 · Content Studio · 2026
