---
title: "WordPress 7.0 Armstrong: AI Masuk ke Core, Situs Kecil Jangan Asal Klik Update"
date: 2026-11-23T00:10:00+07:00
draft: false
tags: ["WordPress", "AI Agent", "MCP", "Keamanan"]
---

# WordPress 7.0 Armstrong: AI Masuk ke Core, Situs Kecil Jangan Asal Klik Update

WordPress 7.0 **"Armstrong"** rilis 20 Mei 2026. Ini bukan update biasa: pertama kalinya WordPress Core membawa infrastruktur AI sendiri — bukan plugin, bukan tempelan SaaS.

Kalau kamu cuma punya satu-dua situs kecil — blog niche, landing page afiliasi, situs judi buat promosi — berita "AI masuk core" kedengarannya bukan urusan kita. Salah. Yang berubah bukan tampilan, tapi **permukaan serangan**: kredensial AI disimpan terpusat, dan ada lapisan baru yang bikin agent AI bisa memanggil aksi di WordPress lewat MCP.

## 📦 Apa yang benar-benar dikirim 7.0

Rilisnya sempat mundur: jadwal awal 9 April 2026 di WordCamp Asia Mumbai, tapi arsitektur database Real-Time Collaboration (RTC) bermasalah. 8 Mei RTC dicabut dari 7.0 dan ditunda ke 7.1; 20 Mei sisanya keluar.

Yang mendarat:

- **AI Connectors** — menu Settings › Connectors. Tiga provider resmi: OpenAI, Anthropic, Google; plus komunitas: OpenRouter, Ollama, Mistral. Satu API key dipakai semua plugin yang dibangun di atas WP AI Client.
- **Empat komponen** — WP AI Client (PHP core, `wp_ai_client_prompt()`), Abilities API, JS Abilities API (`@wordpress/abilities` + `@wordpress/core-abilities`), Connectors API.
- **Opt-in** — tidak ada fitur AI nyala sendiri; core cuma pipa, plugin isinya.

| Aspek | Sebelum 7.0 | Setelah 7.0 |
|---|---|---|
| API key AI | Tersebar di tiap plugin | Satu layar Connectors |
| Integrasi provider | Kode ulang per plugin | Ganti provider = ganti config |
| Kemampuan AI | Tidak ada standar | Abilities API (schema + permission) |
| Otomasi agent | Plugin custom | MCP Adapter → tool |

## 🔌 Bagian yang bikin saya baca ulang: Abilities + MCP

Abilities API versi PHP sudah ada di 6.9; 7.0 dapat pasangan JavaScript-nya. Plugin bisa mendaftarkan kemampuannya — "buat post", "ambil draft" — lengkap dengan schema dan *permission callback*.

Lalu **MCP Adapter** mengubah ability itu jadi *tool* yang bisa ditemukan dan dijalankan agent seperti Claude Desktop atau Cursor. WordPress bukan cuma "dibantu AI", tapi bisa **dikendalikan AI**: publish, ambil draft, ubah metadata — tanpa kode integrasi.

Buat pipeline konten otomatis ini yang kita tunggu, tapi pintunya lebih lebar. Buktinya WordPress Playground sudah punya MCP server resmi sebelum 7.0 keluar:

```bash
claude mcp add --transport stdio --scope user wordpress-playground -- npx -y @wp-playground/mcp
```

## ⚠️ Risikonya bukan teori, sudah ada angkanya

Cloud Security Alliance lewat *Agentic MCP Security Best Practices Guide* (draft 27 Maret 2026) mencatat lebih dari **30 CVE** menyasar MCP server, client, dan infra sepanjang Januari–Februari 2026. Paling berat **CVE-2025-6514**, CVSS **9.6**, kena paket `mcp-remote` di **437.000+ environment**.

Awal 2026 peneliti mengatalogkan **hampir 7.000 MCP server** terbuka di internet — sekitar **separuhnya tanpa autentikasi**. Dua vektor paling aktif: *tool poisoning* (deskripsi tool palsu) dan *indirect prompt injection*.

Kalau kamu pasang MCP Adapter tapi Application Password longgar, "tool WordPress-mu" itu pintu, bukan fitur.

## ✅ 5 hal yang dicek sebelum klik Update

1. **PHP minimal 7.4.** 7.2 dan 7.3 tidak didukung lagi. Cek hosting dulu.
2. **Kredensial terpusat.** Satu key bocor = semua plugin AI kena. Pakai key per situs, limit budget, rotate rutin.
3. **Jangan pasang MCP Adapter kalau tak butuh.** Kalau butuh: Application Password terpisah, read-only kalau bisa, `permission_callback` ketat, jangan akun administrator.
4. **Audit plugin "AI-ready".** 7.0 mengirim infrastruktur, bukan fitur. Plugin tetap penentu apa yang terjadi.
5. **Backup + staging.** Dan jangan janjikan editing bareng ke klien — RTC tidak ada di 7.0, tunggu 7.1.

## 🎁 Yang benar-benar berguna buat situs kecil

Nilai terbesar 7.0 buat situs kecil justru bukan AI-nya:

- **Visual revisions** — perubahan tampil seperti aslinya, dengan penanda kuning (ubah), merah (hapus), hijau (tambah).
- **Command Palette** `⌘K` / `Ctrl+K`, dan **empat blok baru** — Gallery lightbox, Heading variations, Breadcrumbs schema-ready, Icons. Minimal 2-3 plugin bisa di-uninstall; permukaan plugin mengecil = lebih aman.
- **Responsive block controls** — sembunyikan blok per viewport tanpa CSS hack.

## 🎯 Kesimpulan

WordPress 7.0 Armstrong lebih penting dari kelihatannya, tapi bukan karena AI-nya. Buat situs kecil, untung nyatanya datang dari pengurangan plugin dan revisi visual yang akhirnya masuk akal. AI Connectors dan MCP Adapter itu bonus — pasang kalau perlu, dan pasang dengan sadar: satu key, satu pintu, satu tanggung jawab.

Kalau situsmu sering jadi sasaran abuse: [batasi apa yang boleh dipanggil, jangan percaya default](https://chokdi.ano99.com/posts/cctv-abuse-wp-alarm-membungkam-diri/). Kalau mau agent yang melihat isi situs, [mulai dari MCP yang sempit, bukan yang lebar](https://chokdi.ano99.com/posts/chrome-devtools-mcp-agent-buta-jadi-bisa-lihat/). Dan [situs tetap harus kebal DDoS](https://chokdi.ano99.com/posts/cara-bikin-website-kebal-ddos/) — AI tidak menambal itu.

Sumber: [WordPress.org 7.0](https://wordpress.org/download/releases/7-0/) · [WP Dev Blog April 2026](https://developer.wordpress.org/news/2026/04/whats-new-for-developers-april-2026/) · [onPoint Armstrong](https://onpoint.to/wordpress-7-0-armstrong/) · [CSA MCP Security](https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/)

— Chokdi 🐷 · Content Studio · 2026
