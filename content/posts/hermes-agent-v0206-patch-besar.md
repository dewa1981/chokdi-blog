---
title: "Hermes Agent v0.20.6: Patch Release yang Justru Paling Padat Fitur, Ada Browsing Proses Asli"
date: 2026-08-29T12:35:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Update"]
---

Nous Research merilis **Hermes Agent v0.20.6 (v2026.8.27)** pada 27 Agustus 2026. Dibilang "patch release" kecil, tapi begitu dicek isinya — jangan salah kaprah. Versi ini menggulung sekitar **525 PR** dan merangkum hampir **1.313 commit** sejak v0.20.5. Buat pengguna Indonesia yang pakai Hermes Agent buat otomasi, ini rilis yang paling banyak bawa fitur praktis dalam sebulan terakhir.

## 🎭 Browsing Profil Asli Butuh Persetujuan

Highlight terbesar: **consent-gated real-profile browsing**. Sekarang Hermes Agent bisa pakai profil Chromium default kamu untuk browsing lokal — lengkap dengan sesi login, cookie, dan ekstensi yang sudah terpasang. Artinya agent bisa buka akun yang sudah login tanpa ribet captcha ulang. Di Windows jadi lebih menarik lagi: ada alur **close-with-approval**, jadi browser ditutup hanya setelah kamu setujui. Privasi tetap dipegang: semua browsing pakai persetujuan dulu.

## 🖥️ Browser Desktop Punya Jendela Sendiri

Browser bawaan Hermes Agent kini dapat **OS window sendiri** — tidak lagi tersembunyi sebagai tab internal. Ini memudahkan kamu memantau apa yang sedang dikerjakan agent secara visual. Ada juga **managed SSH remote-update engine** dan **fleet profile rail**, cocok buat kamu yang kelola banyak server Hermes sekaligus.

## 🔌 Katalog MCP Remote Membesar

Tersedia **50+ server MCP vendor yang sudah diverifikasi**, termasuk **Cloudflare, Grafana Cloud, Better Stack, dan Railway**. Buat developer Indonesia yang kerja dengan layanan-layanan ini, sekarang tinggal pasang MCP langsung tanpa konfigurasi manual panjang.

## 🔐 Keamanan & Performa

- **OS-keychain encryption** opsional untuk menyimpan secret — tidak ada lagi prompt Keychain macOS di tiap launch.
- **Updater pause gateway** lewat control socket alih-alih membunuh proses (tree-kill) — upgrade jadi tidak memutus sesi yang sedang jalan.
- **TTL result caching** untuk `web_search` dan `web_extract` — hasil pencarian di-cache, lebih hemat token dan lebih cepat.
- **Lean-tail compression** jadi default — konteks ringkas, hemat quota.
- **Multi-query tool_search** dengan stemming — pencarian tool lebih cerdas.

## 🧠 Model Baru Bermunculan

Ada **GLM-5.3-Flash**, **MiniMax M3 (gratis)**, dan **MiniMax H3 Max (video)**. Buat yang suka eksperimen model murah-murah, MiniMax M3 gratis layak dicoba buat tugas ringan.

## 🚀 Cara Update

Buat pengguna yang sudah terpasang, cukup:

```bash
hermes update
```

Atau instalasi baru:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

## 🛠️ Kualitas Hidup Lainnya

Beberapa peningkatan kecil yang bikin kerja sehari-hari makin nyaman:

- **Cron durable-incident acks** — pekerjaan terjadwal (cron job) yang gagal kini mencatat pengakuan insiden secara tahan banting, tidak hilang saat proses restart.
- **Slack link-unfurl controls** — kontrol tampilan pratinjau link di Slack.
- **Shared Docker container identities** — container Docker bisa berbagi identitas, memudahkan setup multi-service.
- **Pluggable terminal environment backends** — terminal agent bisa di-swap backend-nya sesuai lingkungan.
- **Update yang lebih aman** — instalasi via image atau package manager menolak update in-place yang tidak aman, melindungi dari kerusakan konfigurasi.

## 🐷 Kesimpulan

Meski berlabel patch, v0.20.6 ini menandai arah besar Hermes Agent: **browsing asli dengan persetujuan, desktop browser mandiri, katalog MCP luas, dan manajemen secret lebih aman**. Ini bukan sekadar perbaikan bug — ini pematangan fondasi buat rilis besar v0.21.0 yang akan datang. Kalau kamu belum update sejak Agustus, sekarang saatnya.

— Chokdi 🐷 · Content Studio · 2026
