---
title: "Hermes Agent v0.20.6 Rilis: ~525 PR Baru, Ledakan MCP Catalog + Browsing Profil Asli"
date: 2026-09-07T17:20:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "MCP", "Automation"]
---

Kabar buat lo yang self-host AI agent: **Hermes Agent** (punya Nous Research) baru saja menyematkan tag stable terbarunya, **v0.20.6 (v2026.8.27)**. Rilis ini memang patch release, tapi jangan salah—di baliknya ada kerja keras **~525 pull request** yang di-merge sejak v0.20.5, alias sekitar **1.313 commit** di lebih dari 1.500 file.

Yang lebih menarik: rilis ini jadi "jembatan" menuju v0.21.0 yang sedang digodok Nous sebagai rilis besar dengan catatan lengkap dari semua yang terjadi sejak v0.20.0. Penasaran apa saja yang berubah? Ini rangkumannya untuk developer & power user Indonesia.

## 🧩 Ledakan Katalog MCP: 50+ Server Vendor Baru

Salah satu tambahan paling gede di jendela rilis ini adalah ekspansi besar **katalog MCP remote**. Hermes sekarang punya **50+ server vendor yang sudah live-verified** siap pakai—termasuk dari:

- **Cloudflare**
- **Grafana Cloud**
- **Better Stack**
- **Railway**

Buat lo yang mau nyambungin agent ke tool favorit tanpa repot setup manual dari nol, ini penghemat waktu gede. Image "browser AI bisa utak-atik AWS/Cloudflare lo" jadi makin nyata.

## 🌐 Real-Profile Browsing (Dengan Persetujuan)

Hermes mulai mendukung **consent-gated real-profile browsing**: agent bisa pakai profil Chromium *default* lo untuk aktivitas lokal, plus alur close-with-approval khusus Windows. Artinya browser agent nggak lagi "kotak kosong"—ia bisa kerja di profil yang udah lo pakai, tapi tetap di bawah kontrol persetujuan lo. Keamanan tetap dijaga.

## ⚡ Kinerja & Kenyamanan yang Bikin Sehari-hari Makin Enak

Jendela v0.20.5 → v0.20.6 membawa banyak penyempurnaan yang berasa pas dipakai tiap hari:

- **TTL result caching** untuk `web_search` / `web_extract` — hasil pencarian yang sama nggak di-fetch ulang terus.
- **Lean-tail compression jadi default** — konteks panjang dipadatkan lebih efisien, hemat token.
- **Multi-query `tool_search` dengan stemming** — nyari tool lebih oke dari query sejenis.
- **OS-keychain encryption opsional** untuk secret tersimpan — nggak ada lagi prompt macOS Keychain tiap buka app.
- **Desktop Browser dapat OS window sendiri** + remote-update engine + fleet profile rail.

## 🛠️ Untuk Operator: Update Lebih Aman

Buat siapa yang kelola banyak instance (fleet), ini lega banget:

- **Updater pause gateway lewat control socket**, bukan tree-kill yang brutal—jadi nggak ada sesi kepotong mendadak.
- Image/package-managed install menolak update in-place yang nggak aman.
- Ada model-model baru di picker (GLM-5.3-Flash, MiniMax M3 free, MiniMax H3 Max video generasi).

## 🔜 Yang Perlu Lo Tunggu: v0.21.0

Semua ini cuma "pemanasan." Nous sudah ngasih sinyal terang bahwa **v0.21.0 akan membawa curated release notes lengkap**—men-dokumentasikan semua highlight, area fitur, dan kredit kontributor sejak v0.20.0. Kalau v0.20.6 aja segini gede, v0.21.0 (yang rilis besar beneran) pantas dinanti.

## 💡 Poin Praktis Buat Lo

- **Self-host di VPS?** Jalankan `hermes update` — prosesnya kini pause gateway lewat control socket, jadi sesi aktif nggak ke-tree-kill.
- **Sering riset?** Aktifkan TTL caching buat `web_search`/`web_extract` biar hasil yang sama nggak di-fetch ulang & hemat token.
- **Banyak tool pihak ketiga?** Manfaatin 50+ MCP server vendor yang udah live-verified (Cloudflare, Grafana Cloud, Railway)—nyambungin agent ke tool lo tinggal beberapa langkah.
- **Perhatiin secret?** Aktifkan OS-keychain encryption supaya kredensial nggak minta prompt ulang tiap kali buka aplikasi.

## Kesimpulan

Ritme rilis Hermes Agent nggak main-main: patch stable rutin dengan ratusan PR tiap jendela, plus katalog MCP yang melebar ke 50+ vendor. Buat lo yang self-host agent—buat otomasi kerja, bikin bot, atau kelola fleet—ini update yang layak `hermes update` sekarang juga.

Lo udah coba MCP server baru di Hermes? Share pengalaman lo di kolom komentar!

— Chokdi 🐷 · Content Studio · 2026
