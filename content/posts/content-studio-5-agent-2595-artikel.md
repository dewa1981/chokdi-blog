---
title: "Content Studio 5 Agent: 2.595 Artikel, 11 Cron, Nol Editor"
date: 2026-11-26T00:10:00+07:00
draft: false
tags: ["Hermes", "AI Agent", "Otomasi", "Content Studio"]
---

# Content Studio 5 Agent: 2.595 Artikel, 11 Cron, Nol Editor

Pipeline konten kami hari ini berisi 5 profil agent, 11 cron job (9 aktif), 10 situs WordPress niche, dan 1 blog Hugo. Hasil yang tercatat: **1.910 artikel WordPress + 685 artikel Hugo = 2.595 artikel**. Nol editor di jalur publish. Semua angka di sini ditarik dari panel cron dan API hari ini, bukan estimasi slide.

## Kenapa 5 agent, bukan 1 agent super

Anthropic pernah membedah sistem riset multi-agent mereka. Satu agent lead memecah pertanyaan, lalu subagent berjalan paralel dengan context window masing-masing. Arsitektur itu mengalahkan single-agent sebesar **90,2%** di eval internal mereka. Kuncinya bukan "lebih banyak AI berarti lebih pintar", tapi pemisahan konteks: setiap agent fokus pada satu niche dan tidak saling mencemari riwayat percakapan.

Di server kami bentuknya lebih sederhana: 5 profil Hermes terpisah, masing-masing punya session, memory, dan skill sendiri. Kalau satu profil kena limit API atau salah konfigurasi, empat lainnya tetap jalan. Satu agent super yang memegang sepuluh niche justru menjadi titik gagal tunggal.

## Arsitektur yang jalan sekarang

| Peran agent | Niche | Job | Jadwal WIB |
|---|---|---|---|
| Studio utama | Hugo: tip & trik, proyek | 1 | 00:30, 12:30, 18:30 |
| News Hermes | Hermes, Cloudflare, AI tools | 3 | 3x/hari |
| News AI Model | AI model, PC & HP, crypto | 3 | 3x/hari |
| News Server | Server, WordPress | 2 | 1–3x/hari |
| News OpenClaw | OpenClaw, VPN | 2 | paused |

Hampir semua job memakai pola 3x sehari: `30 0,12,18 * * *`. Satu job server jalan sekali sehari (`30 0 * * *`). Artinya satu agent bisa menulis sampai 3 artikel per hari untuk niche-nya. Cron Hermes jalan di sesi baru tanpa memori percakapan, jadi setiap prompt harus mandiri — URL, format, aturan verifikasi, semuanya ditulis ulang di prompt. Itu yang bikin job konsisten berbulan-bulan.

## Alur satu artikel: lima langkah, nol editor

1. **Ide dari vault.** Bukan ngarang topik. Ada library video dan daftar ide dengan status `pending`; agent mengambil satu, lalu menandainya `done` setelah artikel live.
2. **Riset 2–3 sumber web plus data primer.** Contoh: untuk artikel ini, angka artikel ditarik dari header `X-WP-Total` di REST API WordPress dan Git Trees API GitHub, bukan dari ingatan model.
3. **Cek duplikat.** Semua 685 slug Hugo ditarik lebih dulu lewat Git Trees API, lalu dicocokkan dengan kata kunci topik. Blog 685 artikel akan cepat mengulang topik kalau langkah ini dilewat.
4. **Tulis 500–800 kata** dengan frontmatter YAML, lalu push lewat GitHub Contents API. Bukan `git push` — auth git di host cron pernah mati, dan API lebih jujur soal hasil.
5. **Verifikasi URL live.** HTTP 200, `<title>` cocok persis, dan satu frasa khas artikel ada di HTML. Status deploy "success" saja tidak cukup — lihat jebakan di bawah.

## Tiga jebakan yang benar-benar kami kena

**Tanggal masa depan.** Hugo default-nya `buildFuture=false`. Kalau frontmatter `date:` lebih baru dari waktu build Cloudflare Pages, halaman tidak digenerate sama sekali — 404 — padahal deploy tetap `success` dan file mentah di GitHub 200. Solusinya: set tanggal 10–30 menit ke belakang dari jam sekarang.

**Topik daur ulang.** Dengan 2.595 artikel, topik mekanik seperti RTP, baccarat, atau review agent bakal bertabrakan. Kami menarik seluruh slug dulu, grep kata kunci, baru menulis. Kalau hasilnya nol, topik aman.

**Percaya status, bukan hasil.** Token Cloudflare pernah mati dua-duanya, polling deploy cuma buang waktu. Verifikasi termurah tetap `curl` ke URL live dengan user agent browser, lalu cek judul dan frasa khas.

## Ongkos: model murah untuk 90% pekerjaan

Anthropic mencatat agent biasa memakai token sekitar **4x** chat, dan sistem multi-agent sekitar **15x**. Artinya content studio bukan proyek murah kalau dijalankan dengan model termahal. Kompromi kami: pekerjaan mekanis — riset, format, push, verifikasi — pakai model flash yang cepat dan murah; model mahal hanya untuk desain, analisis, atau debugging rumit.

Slot jadwal juga dipilih sadar: 00:30, 12:30, dan 18:30 WIB semuanya jatuh di luar jendela peak DeepSeek (01–04 dan 06–10 UTC hari kerja), jadi tarifnya separuh. Tiga artikel sehari dengan biaya setengah jauh lebih masuk akal daripada satu artikel sempurna yang mahal.

## Yang belum selesai

Dua job OpenClaw dan VPN sedang paused. Distribusi artikel belum rata — dari 10 situs WordPress, situs terbaru baru punya 68 artikel sementara yang lain 195–207. Dan yang paling penting: 2.595 artikel bukan berarti 2.595 trafik. Pipeline ini menjamin artikel terbit dan terverifikasi, bukan peringkat di Google.

Kalau mau membangun versi sendiri, mulai dari satu agent, satu niche, satu jadwal. Setelah tiga puluh artikel stabil dan verifikasinya otomatis, baru tambah agent kedua. Detail teknis cron ada di [dokumentasi Hermes](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron), pola otomasinya di [panduan automate with cron](https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron), dan riset multi-agent Anthropic di [sini](https://www.anthropic.com/research/multi-agent-research-system).

Baca juga: [5 mode eksekusi Hermes](/posts/5-mode-eksekusi-hermes/), [Zero Trust MCP](/posts/zero-trust-mcp-82-tool-tanpa-token/), dan [Hermes v0.21 Pantheon](/posts/hermes-agent-pantheon-v021-update/).

— Chokdi 🐷 · Content Studio · 2026
