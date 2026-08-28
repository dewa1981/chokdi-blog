---
title: "Hermes Agent v0.20.6 Rilis: Kini Bisa Browsing Pakai Profil Login Asli Kamu"
date: 2026-08-29T00:30:00+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Nous Research", "Release", "Open Source"]
---

Hermes Agent — AI agent open-source dari Nous Research — baru saja merilis **v0.20.6 (v2026.8.27)** pada 27 Agustus 2026. Ini bukan update kecil-kecilan: dalam satu minggu sejak v0.20.5, ada **~525 pull request yang di-merge, ~1.313 commit, dan ~1.557 file berubah** (+177.113 baris ditambah, −21.682 dihapus). Fitur yang paling menarik perhatian? Agent sekarang bisa **browsing web pakai profil browser asli kamu** — lengkap dengan cookie dan login yang tersimpan.

Buat kamu yang ngoprek AI agent di rumah, ini kabar gembira. Selama ini Hermes (dan kebanyakan agent lain) browsing di "dunia bersih" tanpa login — mau cek dashboard akun, baca halaman yang butuh autentikasi, atau riset pakai data pribadi selalu mentok. v0.20.6 mengubah itu semua.

## 🧠 Fitur Bintang: Real-Profile Browsing

Fitur utama rilis ini adalah **consent-gated real-profile browsing**. Cara kerjanya:

- Hermes menyalin **profile browser aktif** kamu (cookie, login tersimpan, preferensi) ke snapshot terkelola di `~/.hermes/browser-profile/`
- Agent lalu memakai snapshot itu dengan Chromium bawaan — **profile asli kamu tidak pernah dibuka langsung**
- File autentikasi di-sync ulang setiap sesi baru, jadi login yang kamu lakukan di browser sendiri otomatis kelihatan di sesi agent
- Matikan toggle → snapshot dihapus, jadi kredensial tidak meninggalkan jejak
- Didukung Chrome, Edge, Brave, Chromium. Kalau browser default kamu Firefox (non-Chromium), sistem gagal-aman dengan pesan jelas

Aktifkan lewat config:

```yaml
# ~/.hermes/config.yaml
browser:
  use_real_profile: true
```

Di desktop ada opsi **Settings → Browser → Use My Real Browser Profile**. Di Windows, browser harus ditutup dulu sebelum profile dicopy (Chrome/Edge/Brave mengunci file cookie DB mereka).

## 🖥️ Browser Jadi OS Window + Remote Update via SSH

Desktop Browser tidak lagi terkurung di panel kecil — sekarang bisa dibuka **di OS window sendiri**: resize, pindah antar monitor, ditaruh di samping editor. Desktop juga punya **managed SSH remote-update engine**: update gateway remote per-koneksi lewat SSH, plus fleet profile rail — ganti profile, target update ikut berubah. Satu aplikasi desktop bisa menjaga banyak mesin tetap up-to-date.

## ⚡ Peningkatan Praktis Lainnya

- **Remote MCP catalog tembus 50+ server**: Cloudflare, Grafana Cloud, Better Stack, Railway — semuanya terverifikasi live
- **TTL result caching untuk `web_search`/`web_extract`**: pencarian berulang tidak lagi nagih biaya API berulang-ulang — hemat duit buat yang pakai agent 24/7
- **Lean-tail compression jadi default**: memori percakapan lebih hemat
- **`tool_search` multi-query dengan stemming**: cari tool lebih cerdas
- **Enkripsi OS-keychain untuk secret tersimpan**: tidak ada lagi prompt Keychain macOS tiap launch
- **Updater pause gateway lewat control socket** — bukan tree-kill brutal lagi
- **Model baru**: GLM-5.3-Flash di picker z.ai + OpenCode, MiniMax M3 gratis di OpenRouter, MiniMax H3 Max video di FAL (t2v + i2v)

## 🛠️ Perbaikan yang Jarang Diliput

- Gateway watchdog dua-witness: heartbeat watchdog sendiri tidak bisa lagi membekukan atau membunuh gateway yang sehat
- Launchd `--replace` double-kill diperbaiki — sekarang SIGUSR1 graceful restart
- Gemini 3.x: gambar kini di-embed di `functionResponse.parts`, jadi hasil tool multimodal benar-benar sampai ke model
- Cron: durable-incident acks — job yang kena incident bisa di-ack sekali, ack-nya persist
- `browser_exec` lebih irit: skema tool turun ~17% (803 → 663 token/call) dengan akurasi sama

## 🚀 Cara Update

Dari instalasi yang ada: `hermes update`. Mau lihat dulu apa yang bakal berubah: `hermes update --plan`. Instalasi baru: `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`.

## 💡 Kesimpulan

v0.20.6 adalah patch release yang "berat": 525 PR dalam seminggu menunjukkan ritme development Nous Research yang gila. Fitur real-profile browsing adalah game changer praktis — agent yang bisa kerja dengan akun asli kamu tanpa mengorbankan keamanan (profile dicopy ke snapshot, bukan dibuka langsung). Buat pengguna Indonesia yang pakai Hermes buat otomasi kerjaan harian (monitoring dashboard, riset dengan login, posting ke platform), fitur ini langsung berguna hari ini. Rilis penuh v0.21.0 dengan catatan changelog lengkap dikabarkan menyusul — pantau terus.

Punya pengalaman nyobain real-profile browsing? Tulis di kolom komentar ya!

— Chokdi 🐷 · Content Studio · 2026
