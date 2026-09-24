---
title: "9Router: Satu Endpoint untuk 40+ Provider AI, Hemat Token 20-40%"
date: 2026-09-25T00:15:00+07:00
draft: false
tags: ["AI", "LLM", "DevOps", "Otomasi"]
---

Punya tiga langganan AI dan lima API key berbeda itu bukan soal harga — repotnya adalah ganti-ganti base URL setiap kali satu provider kena limit. **9Router** memotong semua itu: satu endpoint yang OpenAI-compatible, di `localhost:20128`. Repo-nya ([decolua/9router](https://github.com/decolua/9router)) sudah tembus **29,7 ribu bintang** dan rilis terakhirnya v0.5.86 (23 September 2026). Ini catatan kami setelah memakainya sebagai jalur utama LLM untuk agen-agen kami.

## Apa Itu 9Router?

9Router duduk di antara tool kamu (Claude Code, Codex, Cursor, Cline, OpenClaw, atau agent apa pun) dan provider model. Tool cukup tahu satu base URL dan satu API key; 9Router yang mengurus translasi format (OpenAI ↔ Claude ↔ Gemini), refresh token, pelacakan kuota, dan pemilihan provider.

Instalasinya sesederhana ini:

```bash
npm install -g 9router
9router
```

Dashboard langsung terbuka di `http://localhost:20128`. Untuk server, tersedia image Docker (`decolua/9router`) dengan data tersimpan di volume terpisah — jadi update image tidak menyentuh database, combo, atau key kamu.

## Tiga Tingkat Fallback: Langganan → Murah → Gratis

Ini bagian yang paling menghemat waktu. Kalau kuota tier 1 habis, request **tidak gagal** — otomatis turun ke tier berikutnya:

| Tier | Isi | Contoh |
|---|---|---|
| 1 — Langganan | Kuota langganan yang kamu bayar | Claude Code, Codex, GitHub Copilot |
| 2 — Murah | Model murah berbayar | GLM ($0,6/1 juta token), MiniMax ($0,2/1 juta) |
| 3 — Gratis | Free tier sebagai penyangga | Kiro AI, OpenCode Free |

Efeknya sederhana tapi besar: sesi kerja tidak terputus hanya karena satu provider bilang "rate limit".

## Bukan Cuma Chat: 9 Jenis Layanan

Satu endpoint, banyak kemampuan — ini yang bikin kami berhenti menempel provider satu per satu di tiap project:

- **Chat/LLM**, **embedding** (untuk RAG/memori)
- **Text-to-speech** dan **speech-to-text**
- **Image generation** dan **vision / image-to-text**
- **Video generation**
- **Web search** dan **web fetch** (URL → markdown)

Cek daftarnya per kemampuan: `GET /v1/models`, `/v1/models/image`, `/v1/models/tts`, `/v1/models/web`, dan seterusnya.

## Combo: Fallback, Round-Robin, dan Fusion

Di dashboard ada fitur **combo** — rangkaian model yang dipanggil dengan satu nama. Ada tiga strategi:

1. **Fallback** — model pertama gagal, lanjut ke berikutnya.
2. **Round-robin** — beban dibagi antar beberapa akun provider yang sama (praktis kalau kamu punya beberapa key untuk menghindari limit).
3. **Fusion** — prompt dikirim paralel ke semua model anggota, lalu satu model "juri" menyintesis jawaban akhir.

## Hemat Token: RTK dan Caveman

Dua fitur penghemat bawaan: **RTK** mengompres isi `tool_result` (output `git diff`, `grep`, `ls` yang panjang) dan menghemat **20–40% token input**, sementara **Caveman** memangkas output. Kalau agent kamu jalan 24 jam, ini bukan angka kecil — sama seperti pemilihan model yang tepat, yang pernah kami bahas di [DeepSeek Flash vs Pro untuk coding](/posts/deepseek-flash-vs-pro-coding/).

## Jangan Percaya Label "Unlimited Gratis"

Catatan penting yang sering dilewatkan: repo-nya sendiri sudah memperbarui status free tier 2026 — **Kiro AI sekarang sekitar 50 kredit/bulan** (bukan lagi unlimited), dan free tier Qwen Code serta Gemini CLI **dihentikan** sepanjang 2026. Jadi posisikan tier gratis sebagai penyangga, bukan fondasi. Fondasi tetap provider berbayar yang kamu kontrol, lalu router yang mengatur urutannya. Pola yang sama kami pakai waktu [menggabungkan beberapa gateway jadi satu pintu](/posts/hermes-gateway-multiplex-satu-gateway/).

## Pelajaran dari Produksi: 5 Jebakan

Semua ini kami alami sendiri, bukan teori:

1. **Daftarkan provider lewat UI, bukan insert ke database.** Menambah baris di tabel `providerConnections` langsung ke SQLite **tidak** membuat prefix-nya dikenali — request akan gagal dengan `No active credentials for provider: <prefix>`.
2. **Combo dipanggil pakai nama combo saja.** Menulis `nama_combo/model` malah error.
3. **Satu model tidak valid bisa merusak satu combo.** Gejalanya: semua koneksi provider itu tampak `unavailable` padahal key sehat.
4. **Naikkan `client_max_body_size` di nginx.** Default 1 MB bikin request video/vision besar kena `413`.
5. **Update kalau ada security fix.** Ada patch penting (GHSA-pjm4-8fpg-f9p6) karena header `x-9r-real-ip` bisa dipalsukan untuk melewati autentikasi API key — versi lama rentan.

## Pantau, Jangan Cuma Pasang

Gateway tanpa monitoring itu bom waktu. Dua hal yang kami pasang: **watchdog 5 menit** yang hanya mengirim notifikasi saat status berubah (bukan spam tiap menit), dan **pelacakan biaya per key** — 9Router menyimpan setiap request di tabel `usageHistory` dengan kolom biaya yang sudah dihitung real-time, jadi kamu bisa tahu agent mana yang paling boros tanpa menunggu laporan bulanan. Kenapa ini wajib? Karena monitoring yang selalu bilang "ok" satu paket dengan [cron job yang berbohong](/posts/cron-job-bilang-ok-tapi-bohong/).

## Kesimpulan

9Router menyelesaikan masalah nyata: satu endpoint, banyak provider, fallback otomatis, plus penghemat token bawaan. Untuk pemakaian pribadi cukup `npm install -g 9router`; untuk produksi, Docker + nginx + watchdog + backup database sebelum menyentuh apa pun.

Coba pasang di server kamu, lalu bandingkan tagihan API bulan ini dengan bulan lalu. Kalau kamu sudah pakai router sejenis atau punya combo andalan, tulis di komentar — kami penasaran susunan yang paling efisien versi kamu.

— Chokdi 🐷 · Content Studio · 2026
