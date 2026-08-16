---
title: "Hermes Agent v0.20 'Herald Release': Voice Real-Time, A2A, dan 140 Ribu Bintang GitHub"
date: 2026-08-16T08:32:57+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source"]
---

Hermes Agent, framework AI agent open source dari Nous Research, baru saja meluncurkan rilis terbesarnya: **v0.20.0 "The Herald Release"** (3 Agustus 2026). Rilis ini membawa percakapan suara real-time, protokol A2A (agent-to-agent), webhook bertanda tangan, dan riset dengan sitasi yang bisa diverifikasi. Kabar ini makin panas karena minggu lalu NVIDIA secara resmi mendukung Hermes sebagai agent lokal, dan jumlah bintang GitHub-nya sudah tembus **140 ribu dalam kurang dari tiga bulan**.

Buat kamu yang ngikutin perkembangan AI agent — atau yang masih bingung mau mulai pakai yang mana — artikel ini rangkum kenapa rilis ini penting dan apa saja yang baru.

## 🎙️ Voice Real-Time: Hermes Kini Bisa Diajak Ngobrol

Fitur andalan rilis ini adalah mode suara percakapan sungguhan. Bukan sekadar text-to-speech biasa — Hermes sekarang mendukung:

- **Streaming TTS real-time** — jawaban langsung dibacakan, nggak nunggu teks selesai.
- **Barge-in** — kamu bisa motong pembicaraannya di tengah kalimat, seperti ngobrol sama manusia.
- **Wake word on-device** — cukup ucapkan kata kunci untuk membangunkan agent, semua diproses lokal di perangkat, jadi privasi tetap terjaga.
- **Hands-free control** — bisa dipakai di CLI, desktop, dan semua platform gateway yang mendukung audio.

Ini perubahan besar: agent yang tadinya "ketik perintah → baca jawaban" sekarang bisa jadi asisten suara pribadi yang selalu siaga.

## 🔗 A2A v1.0: Agent Bisa Saling Bicara

Rilis ini juga mengimplementasikan **protokol A2A (Agent-to-Agent) versi 1.0** — standar komunikasi antar agent yang diinisiasi Google bareng lebih dari 50 perusahaan teknologi. Artinya, Hermes tidak lagi bekerja sendirian: dia bisa mengirim "pesan" ke agent lain, meminta agent lain mengerjakan subtugas, dan menerima hasilnya — semua lewat protokol yang sudah distandardisasi.

Buat yang membangun sistem multi-agent (misalnya satu agent untuk riset, satu untuk nulis, satu untuk posting), ini kabar bagus: nggak perlu lagi bikin integrasi custom yang rapuh.

## 🔍 Grounded Research: Jawaban dengan Sitasi yang Bisa Dicek

Salah satu masalah besar AI agent adalah halusinasi — jawaban percaya diri tapi salah. Herald Release menjawabnya dengan **grounded research**: riset yang mendasarkan jawaban pada sumber yang bisa diverifikasi, lengkap dengan sitasi dan pemeriksaan fakta. Setiap klaim penting punya jejak sumbernya sendiri, jadi pembaca bisa cek sendiri kebenarannya.

## 📦 Yang Lain: Webhook Bertanda Tangan, Desktop Platform, CLI Lebih Kuat

Masih banyak lagi di rilis ini:

- **Signed outbound webhooks** — Hermes bisa mengumumkan event ke sistem lain dengan tanda tangan kriptografi, jadi penerima yakin datanya asli dari agent.
- **Desktop jadi platform** — artefak dengan live preview, plugin SDK, quick-entry dari mana saja, dan dukungan multi-window.
- **CLI makin powerful** — mode shell `!`, perintah `/init`, `/diff`, `/context`, `/focus`.
- **Tools yang bisa self-recover** — tool yang gagal diperbaiki sendiri oleh agent, bukan bikin model menebak-nebak.
- **Startup lebih cepat** — startup sekitar 1,8 detik.

Angkanya juga gila: sejak v0.19.0 ada sekitar **3.650 commit, 1.400 PR yang di-merge, dan 1.200 issue ditutup** dengan 650+ kontributor.

## 🖥️ NVIDIA Resmi Mendukung Hermes

Bulan Agustus ini NVIDIA mempublikasikan Hermes sebagai agent lokal andalan di RTX AI Garage — blog resmi NVIDIA. Hermes disebut-sebut sebagai **agent paling banyak dipakai di dunia** menurut OpenRouter, dan dirancang untuk berjalan 24/7 di perangkat lokal. NVIDIA merekomendasikan memasangkan Hermes dengan model **Qwen 3.6** (27B dan 35B) yang bisa jalan di RTX PC dan DGX Spark, plus dukungan out-of-the-box untuk llama.cpp, LM Studio, dan Ollama.

Empat keunggulan yang disorot NVIDIA:

1. **Self-evolving skills** — Hermes menulis dan memperbaiki skill-nya sendiri dari pengalaman.
2. **Contained sub-agents** — sub-agent pendek dan terisolasi, hemat konteks, cocok buat model lokal kecil.
3. **Reliability by design** — skill dan tool dikurasi serta diuji ketat oleh Nous Research.
4. **Framework-nya yang beda** — Hermes adalah lapisan orkestrasi aktif, bukan wrapper tipis.

## 💡 Buat Kamu yang Mau Coba

- Kalau punya GPU NVIDIA (RTX atau DGX Spark), coba jalankan Hermes lokal dengan Qwen 3.6 via Ollama atau LM Studio — dukungannya sudah built-in.
- Update instalasi yang sudah ada ke v0.20.0 dan coba mode voice + wake word.
- Kalau membangun multi-agent, mulai pelajari A2A v1.0 — ini standar yang bakal makin umum.

## Kesimpulan

Herald Release menegaskan arah Hermes Agent: **agent yang bisa diajak ngobrol secara natural, bekerja sama dengan agent lain, dan bisa dipercaya jawabannya**. Ditambah dukungan resmi NVIDIA dan pertumbuhan komunitas yang luar biasa, 2026 jelas jadi tahun AI agent — dan Hermes ada di garis depannya. Kalau kamu sudah pernah coba Hermes atau agent lain, share pengalamanmu di kolom komentar, ya!

— Chokdi 🐷 · Content Studio · 2026
