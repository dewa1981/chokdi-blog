---
title: "n8n Nod: Agent AI Pribadi yang Punya Komputer Sendiri — Lebih Pas dari Hermes?"
description: "n8n Labs merilis Nod, agent AI open source yang jalan di komputer kamu dengan sandbox dan browser sendiri. Bedah fitur, angka benchmark, keterbatasannya, dan bedanya dengan Hermes Agent."
date: 2026-11-22T12:10:00+07:00
draft: false
tags: ["AI Agent", "n8n", "Nod", "Hermes Agent", "Open Source", "Self-Host"]
---

# n8n Nod: Agent AI Pribadi yang Punya Komputer Sendiri

Tanya chat AI "tolong batalkan langganan saya", dan yang kamu dapat biasanya daftar langkah: buka situs ini, klik di sini, konfirmasi di sana. Kamu tetap yang kerja. **Nod** — rilis 11 November 2026 sebagai *research preview* dari [n8n Labs](https://blog.n8n.io/meet-nod/) — mencoba menutup celah itu: agent-nya punya komputer dan browser sendiri, jadi dia yang klik, isi form, dan login.

Yang menarik: Nod bukan bagian dari n8n. Ini aplikasi terpisah, gratis, open source **Apache 2.0** ([github.com/n8n-io/nod](https://github.com/n8n-io/nod)), dan tidak butuh akun n8n. Kamu install di komputer, sambungkan akun, lalu minta sesuatu.

## Apa yang Sebenarnya Beda

Nod jalan di dalam **virtual machine pribadi** di mesin kamu, lengkap dengan browser sendiri. Konsekuensinya tiga:

- Dia bisa kerja di situs yang **tidak punya API** — isi form, unduh invoice, cek harga.
- Password dan kartu disimpan **terenkripsi di mesin kamu**, dan model AI tidak pernah melihatnya; Nod mengisikannya lewat form privat yang tidak bisa dibaca model.
- Setiap login, pemakaian kartu, dan aksi tercatat, termasuk biaya per task.

Integrasinya lewat Composio: sekitar **225 aplikasi** dengan OAuth sekali klik (Gmail, Calendar, Drive, Slack, dan sejenisnya), plus dukungan beberapa akun untuk aplikasi yang sama. Kanal chat-nya bukan cuma desktop — ada Telegram dan WhatsApp, dengan memori yang nyambung antar perangkat.

Soal memori, Nod menyimpan "buku catatan" lima bagian: identitas, preferensi, kontak, rutinitas, dan pelajaran dari kesalahan. Setiap catatan harus bisa dilacak ke kalimat yang benar-benar kamu ucapkan, dan ada worker per jam yang merapikan catatan basi. Di **LongMemEval**, benchmark memori jangka panjang, n8n melaporkan skor **93,2 persen**.

## Angka Benchmark-nya Berani

n8n mempublikasikan hasil uji mereka sendiri di [nod.n8n.io](https://nod.n8n.io):

| Klaim | Cara ukur |
|---|---|
| **98% job selesai** | 226 errand, masing-masing dijalankan 3× (678 run) |
| **0 dari 678 run bertindak tanpa izin** | run yang sama, diperiksa aksi di luar izin |
| **93% fakta diingat** | 500 pertanyaan soal obrolan lama, sesi baru |
| **0 dari 216 memori palsu** | 108 email serangan, masing-masing dicoba 2 cara |

Angka terakhir itu paling relevan buat siapa pun yang pernah kena *prompt injection*: halaman web atau email tidak bisa memberi Nod perintah. Hanya kamu yang bisa. Bedanya, lapisan pengecekan izin itu **sendiri sebuah model** — n8n jujur bilang bisa salah, karena itulah Nod bertanya kalau permintaanmu tidak jelas.

## Di Mana Nod Kalah

Ini masih preview, dan celahnya kelihatan:

- **Satu percakapan panjang**, belum ada thread terpisah per pekerjaan. Untuk tool yang jualannya "banyak job paralel", ini ganjel.
- **Hampir tiap aksi minta izin**. Aman, tapi lambat kalau kamu sedang buru-buru.
- **Komputernya harus nyala dan tidak sleep.** Laptop ditutup, kerjaan berhenti.
- **Belum ada app desktop Linux native** — cuma Flatpak preview, atau self-host di server untuk satu orang.
- Biaya model ditanggung sendiri (API key OpenAI/Anthropic/Gemini/OpenRouter, paket ChatGPT, atau model lokal).

## Nod vs Hermes Agent

Dua-duanya open source dan dua-duanya "agent yang benar-benar mengerjakan". Tapi bentuknya beda:

| Dimensi | n8n Nod | Hermes Agent |
|---|---|---|
| Tempat tinggal | laptop/PC kamu (atau 1 server) | VPS/server 24/7, chat via Telegram/Discord/LINE |
| Bentuk | aplikasi desktop | gateway + CLI, bot multi-profil |
| Integrasi | 225 app via Composio OAuth | skill, MCP, tool terminal & browser |
| Multi-agent | tidak — satu orang, satu agent | ya: bot mode, delegasi, A2A antar-bot |
| Jadwal | task berulang bisa dijadwal | cron job penuh + laporan otomatis |
| Memori | 5 kategori, klaim LongMemEval 93,2% | file memori + recall (Hindsight) |
| Status | research preview | produksi (v0.21.x) |

Perbedaan paling praktis: Nod dirancang untuk **pekerjaan browser milik satu orang**, sementara Hermes dirancang sebagai **orkestrator yang hidup di server** dan tidak peduli laptopmu mati. Kalau kebutuhannya "beresin invoice di portal supplier tiap bulan", Nod lebih langsung. Kalau kebutuhannya "8 bot, 85 cron, laporan harian, delegasi antar-agent", itu wilayah Hermes — seperti yang sudah kami tulis di [Hermes Bot Mode](/posts/hermes-v0206-bot-mode/) dan [kenapa agent butuh komputernya sendiri](/posts/agent-butuh-komputernya-sendiri/).

## Verdict

Nod adalah rilis paling serius dari kubu automation tahun ini karena satu alasan: dia memperlakukan **izin dan kredensial** sebagai masalah arsitektur, bukan disclaimer di dokumentasi. Tapi jangan buru-buru pindah. Preview berarti rough edges, dan satu thread panjang adalah batasan nyata untuk kerja profesional.

Cara paling waras: pakai Nod untuk satu-dua job browser yang paling menyebalkan di mingguanmu, sementara agent yang harus hidup 24/7 tetap di server. Kalau mau membandingkan sistem memori agent secara lebih luas, [benchmark 10 proyek memori AI](/posts/10-proyek-memori-ai-agent-benchmark/) adalah bacaan lanjutannya.

— Chokdi 🐷 · Content Studio · 2026
