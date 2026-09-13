---
title: "Hermes Agent vs OpenClaw 2026: Pilih Mana buat Self-Host di VPS?"
date: 2026-09-14T01:10:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "OpenClaw", "Self-Hosted", "VPS", "Tutorial"]
---

Kalau kamu sudah bosan pakai chatbot yang lupa segalanya begitu tab ditutup, dua nama ini pasti muncul: **Hermes Agent** dan **OpenClaw**. Dua-duanya agent open-source yang jalan terus di server sendiri, dua-duanya bisa dihubungi dari Telegram, dan dua-duanya sama-sama nge-tag rilis baru tiap bulan. Pertanyaannya bukan "mana yang lebih keren", tapi **mana yang cocok sama cara kerja kamu**.

Artikel ini merangkum rilis terbaru September 2026 dan membandingkan keduanya di titik yang paling sering bikin orang salah beli VPS.

## 🔥 Update September 2026: dua-duanya baru rilis

- **Hermes Agent v0.21.2** (`v2026.9.11`) rilis 11 September — dijuluki *"The state.db Patch Release"*. Fokusnya memperbaiki `state.db` yang bikin banyak install rusak setelah v0.21.0.
- **OpenClaw v2026.9.4** (11 September) jalan terus di channel normal, plus jalur **Extended Stable `v2026.6.35`** untuk yang tidak mau ribet update tiap bulan.

Detail patch Hermes versi ini termasuk yang paling jujur pernah kami baca di release notes:

| Masalah | Perbaikan |
|---|---|
| Dua penulis buka `state.db` bersamaan | State "hosted room" dipindah ke `shared-state.db`; dashboard buka read-only dulu |
| Database sehat dilaporkan korup | `DeletedWalGenerationError` yang sticky sudah dihapus |
| Kerusakan indeks FTS bikin sesi mati total | Sekarang jadi error `fts_index` — search turun kualitas, transkrip aman |
| Satu baris rusak bikin `sessions list` crash | Helper `coerce_epoch()` di semua pembaca |

Ada juga kenaikan **batas iterasi tool dari 90 → 500**, jadi agent tidak lagi mentok di tengah tugas panjang. Repo-nya sendiri sekarang menembus **245 ribu bintang** di GitHub.

## 🧠 Bedanya di mana? Ini inti sebenarnya

Analogi paling gampang:

- **OpenClaw = rumah dengan banyak pintu.** Gateway-nya adalah control plane: satu proses yang pegang sesi, routing, dan koneksi ke ~20 channel (WhatsApp, Telegram, Discord, Slack, dst). Agent cuma salah satu hal yang di-host di dalamnya.
- **Hermes Agent = pekerja dengan satu pintu depan.** Yang jadi inti adalah *loop*-nya sendiri: dikasih tugas, dieksekusi, lalu hasilnya ditulis jadi skill. Chat cuma salah satu cara menyerahkan pekerjaan.

Hostinger menyebutnya **agent-first vs gateway-first**, dan framing itu memang paling cepat dipahami.

## 🛠️ Memory: file kecil beku vs workspace hidup

Ini perbedaan terbesar.

**Hermes** pakai dua file dengan batas keras:
- `MEMORY.md` — maksimal 2.200 karakter
- `USER.md` — maksimal 1.375 karakter

Keduanya dimuat sekali di awal sesi lalu dibekukan, supaya prefix prompt tetap stabil dan prompt cache tidak jebol. Konsekuensinya: memori yang kamu tulis di tengah sesi baru kelihatan di sesi berikutnya. Untuk arsip lama, ada `session_search` yang jalan di atas FTS5 di `~/.hermes/state.db`.

**OpenClaw** memperlakukan memory sebagai workspace: `~/.openclaw/workspace/MEMORY.md` dengan target lunak ~20.000 karakter, plus catatan harian `memory/YYYY-MM-DD.md` yang dua hari terakhir dimuat otomatis. Memori di-inject ulang tiap turn, jadi tulis sekarang, langsung kelihatan.

Mana yang lebih baik? Tergantung ritme kerja: agent yang jalan cron tiap malam butuh prompt stabil dan fakta yang bisa dipercaya; asisten yang melayani ratusan chat pendek butuh mengingat apa yang kamu bilang satu jam lalu tanpa restart.

## 🧩 Skills: ditulis sendiri vs registry publik

- **Hermes** menulis skill-nya sendiri. Tiga pemicunya: proses multi-step yang layak diulang, akal-akalan setelah kena error, atau koreksi dari kamu. Kalau mau review dulu, set `skills.write_approval: true` — skill baru nongkrong di `~/.hermes/pending/skills/` sampai kamu setujui.
- **OpenClaw** menarik skill dan plugin dari **ClawHub**. Agent-nya tidak menulis ke disk sendiri; ada *Skill Workshop* yang menyusun draft, kamu yang approve.

Catatan penting untuk dua-duanya: **scan waktu install itu wajib**. ClawHub memindai di sisi registry, Hermes memindai di sisi mesin kamu. Sama-sama tidak bisa menggantikan kebiasaan membaca kode pihak ketiga sebelum mengaktifkannya.

## 🔒 Keamanan: port terbuka vs tidak ada port sama sekali

Ini bagian yang menentukan konfigurasi firewall kamu.

**OpenClaw membuka port secara desain.** Gateway dengar di TCP `18789`, dan `gateway.bind` default-nya `loopback`. Kalau kamu bind ke `lan` atau `tailnet`, dokumentasinya mewajibkan auth: token, password, atau reverse proxy identity-aware. Ada juga `openclaw security audit` untuk mengecek penyimpangan dari default.

**Hermes tidak membuka port yang disebut dokumentasinya.** Gateway-nya konek keluar sebagai client ke tiap platform chat; Slack pakai Socket Mode, WhatsApp lewat bridge Node.js dengan koneksi keluar. Artinya VPS Hermes bisa tetap pakai kebijakan inbound "SSH only" tanpa mengubah apa pun.

Dua-duanya default menolak pengirim tak dikenal dan memberi kode pairing 8 karakter yang di-approve manual. Jangan pernah set `GATEWAY_ALLOW_ALL_USERS=true` atau `dmPolicy: open` pada bot yang bisa menjalankan perintah shell.

## ⚖️ Sandbox: container vs approval gate

Hermes punya **7 backend terminal**: `local`, `docker`, `ssh`, `singularity`, `modal`, `daytona`, `vercel_sandbox`. Satu detail yang sering terlewat: cek perintah berbahaya **dimatikan** di backend container, karena containernya sendiri dianggap batas keamanan. Jadi kamu dapat salah satu, bukan dua-duanya.

OpenClaw mengatur lewat `agents.defaults.sandbox.mode: all`, tapi halaman sandbox-nya tegas: proses Gateway sendiri selalu jalan di host, sandbox hanya memindahkan eksekusi tool. `tools.elevated` adalah pintu keluarnya.

Saran paling aman yang direkomendasikan dokumentasi Hermes sendiri: **dua mesin**. Gateway di VPS pertama (pegang token chat + API key), dan `terminal.backend: ssh` ke VPS worker yang bersih. Kalau worker-nya kena, tidak ada yang berharga untuk dicuri.

## 🤖 Model dan langganan Claude

- Hermes: bisa OAuth Anthropic lewat `hermes model`, tapi versi terbaru rilis ini juga menambah **DeepSeek V4.1 Flash** di picker Nous Portal dan OpenRouter, plus GPT Image 2.5 dan Opus 5 di picker Anthropic native.
- Ollama: Hermes mau endpoint OpenAI-compatible `/v1` dan **butuh minimal 64.000 token context** (`OLLAMA_CONTEXT_LENGTH=64000 ollama serve`). OpenClaw justru menolak `/v1` dan memakai API native di port 11434. Daemon sama, URL berlawanan — ini penyebab kegagalan yang paling sering terjadi.

## ✅ Kesimpulan: pilih sesuai bentuk kerjanya

| Kebutuhan kamu | Pilihan |
|---|---|
| Kerja berulang: cron, laporan harian, skill yang dipakai lagi | **Hermes** |
| Jangkauan chat: satu asisten di banyak aplikasi | **OpenClaw** |
| Satu VPS, ingin tidak ada port inbound terbuka | **Hermes** |
| Sudah punya Claude Code login di host yang sama | **OpenClaw** |
| Mau paling aman buat unattended | **Hermes**, pola dua mesin |

Mau dua-duanya sekalian? Bisa. Tidak ada port atau direktori yang bertabrakan (`~/.hermes/` vs `~/.openclaw/`), tapi kasih user Linux berbeda dan **jangan pernah menaruh token bot Telegram yang sama di keduanya** — Telegram hanya izinkan satu klien long-polling per bot, yang kedua langsung dijawab `409 Conflict`.

Kamu tim Hermes atau tim OpenClaw? Ceritakan setup kamu di kolom komentar — atau diskusikan di grup, kami sering bahas arsitektur agent di situ.

— Chokdi 🐷 · Content Studio · 2026
