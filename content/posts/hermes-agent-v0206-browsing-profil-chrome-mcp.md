---
title: "Hermes Agent v0.20.6 Rilis: Browsing Pakai Profil Chrome Asli, 50+ MCP Server, dan Cache Hasil Pencarian"
date: 2026-08-28T00:32:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Agentic AI"]
---

Nous Research kembali merilis versi baru Hermes Agent: **v0.20.6 (v2026.8.27)** — dirilis 27 Agustus 2026, hanya seminggu setelah v0.20.5. Patch release ini menggulung **~525 PR** dengan **~1.313 commit** dalam satu minggu. Bukan sekadar perbaikan bug kecil — ada fitur-fitur yang bikin Hermes makin nyaman dipakai buat kerja harian, terutama buat kamu yang sering minta agent browsing atau nyari informasi.

## 🌐 Browsing Pakai Profil Chrome Asli

Fitur paling menarik di rilis ini adalah **consent-gated real-profile browsing**. Sekarang Hermes bisa pakai profil Chromium default kamu untuk browsing lokal — jadi login, cookie, dan sesi website yang sudah kamu buka ikut terpakai oleh agent. Ada alur close-with-approval khusus di Windows: setiap kali agent mau akses profil kamu, dia minta persetujuan dulu.

Artinya: agent kamu bisa buka dashboard, ambil data dari website yang butuh login, tanpa kamu harus setup credential ulang. Buat yang sering pakai Hermes untuk automasi — ini penghemat waktu besar.

## 🧩 Katalog MCP Server Makin Gede: 50+ Server

Kabar bagus buat pengguna MCP: katalog remote MCP sekarang diperluas dengan **50+ vendor-hosted server** yang sudah terverifikasi live. Termasuk server resmi dari **Cloudflare, Grafana Cloud, Better Stack, dan Railway**. Jadi kalau kamu mau agent memantau status website Cloudflare, baca log Grafana, atau deploy ke Railway — tinggal pilih dari katalog, tanpa setup manual yang ribet.

## ⚡ Cache Hasil Pencarian + Kompresi Lean-Tail

Dua fitur performa yang langsung kerasa:

- **TTL result caching untuk web_search dan web_extract** — hasil pencarian yang sama tidak di-fetch ulang dalam periode tertentu. Hemat waktu dan token, apalagi kalau agent kamu sering riset topik yang sama.
- **Lean-tail compression sebagai default** — konteks percakapan yang panjang otomatis diringkas lebih agresif, jadi sesi lama tidak cepat bengkak.

Tambahan lain: **multi-query tool_search dengan stemming** — cari tool lebih cerdas, bisa beberapa query sekaligus.

## 🔐 Keamanan: Enkripsi Keychain OS + Updater yang Lebih Sopan

- **Opt-in OS-keychain encryption untuk stored secrets** — di macOS, tidak ada lagi prompt Keychain setiap kali launch. Sekali set, secret tersimpan terenkripsi.
- **Updater sekarang menunda gateway via control socket** — bukan tree-kill lagi. Proses agent tidak dibunuh paksa saat update; gateway di-pause dulu, update, lalu lanjut. Buat yang menjalankan Hermes 24/7 (kayak bot di server), ini artinya downtime lebih halus.
- **Install lewat image/package manager menolak update in-place yang tidak aman** (#91277 Phase 3).

## 🚀 Model Baru di Picker

Hermes v0.20.6 menambahkan beberapa model baru: **GLM-5.3-Flash**, **MiniMax M3 free**, dan **MiniMax H3 Max** untuk video. Makin banyak pilihan murah/gratis buat kamu yang mau hemat biaya API.

## 📝 Cara Update

Update sangat gampang, tinggal jalankan:

```bash
hermes update
```

Atau buat install baru: `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`

Catatan: rilis ini adalah patch — changelog lengkap yang terkurasi (dari v0.20.0) akan dibahas detail di **v0.21.0** yang akan datang.

## 🎯 Kesimpulan

v0.20.6 membuktikan ritme rilis Hermes Agent yang sangat cepat — seminggu sekali, ratusan PR, dan fitur-fitur yang langsung relevan buat pengguna harian: browsing dengan profil asli, katalog MCP 50+ server, cache pencarian, dan update yang tidak bikin service mati mendadak. Kalau kamu pakai Hermes, langsung update — dan coba fitur real-profile browsing-nya. Siapa tahu, automasi kerjaanmu makin mulus.

— Chokdi 🐷 · Content Studio · 2026
