---
title: "Hermes Agent Rilis Bot Mode: Satu Profil Jadi Banyak Bot dengan Memori Terpisah"
date: 2026-08-19T12:34:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Multi-Agent"]
---

Nous Research baru saja meluncurkan fitur **Bot Mode** untuk Hermes Agent pada 17 Agustus 2026. Fitur ini mengubah cara kita membangun dan mengelola AI agent — satu aplikasi bisa menjalankan banyak bot dengan kepribadian, model, dan memori masing-masing. Ini bukan sekadar update kecil; ini lompatan besar untuk ekosistem AI agent open-source.

## 🤖 Apa Itu Bot Mode?

Bot Mode memungkinkan kamu membuat **banyak bot dari satu profil Hermes Agent**. Setiap bot punya:

- **Role dan kepribadian unik** — misalnya bot coding, bot riset, bot customer service
- **Model LLM berbeda** — bot A pakai GPT-5, bot B pakai model lokal, bebas pilih
- **Memori terisolasi** — percakapan bot A tidak bercampur dengan bot B
- **Skill tersendiri** — setiap bot bisa punya kemampuan spesifik

Bayangkan kamu punya tim AI: satu bot buat nulis kode, satu buat riset pasar, satu lagi buat handle customer support. Semuanya jalan di satu aplikasi yang sama, tapi konteksnya terpisah rapi.

## 🔄 Komunikasi Antar Bot

Fitur paling powerful dari Bot Mode adalah **Agent Inbox** — sistem pesan internal yang memungkinkan bot-bot saling berkomunikasi. Bot coding bisa minta tolong bot riset untuk cari dokumentasi API, lalu bot riset mengirimkan hasilnya langsung ke inbox bot coding.

Komunikasi bisa dilakukan dalam mode:
- **1-on-1** — bot A kirim pesan ke bot B
- **Group chat** — beberapa bot diskusi bareng dalam satu thread

Yang menarik, setiap bot tetap mempertahankan konteks dan memorinya sendiri. Tidak ada yang namanya "kecampur" antara percakapan bot coding dengan bot customer service.

## ⚙️ Teknis: Apa yang Berbeda?

Dari sisi teknis, Bot Mode adalah **lapisan UX baru** di atas sistem profil Hermes Agent yang sudah ada. Teknium (@Teknium), Cofounder & Lead Engineer Nous Research, menjelaskan bahwa fitur ini memanfaatkan arsitektur multi-profil yang sudah solid.

Beberapa highlight teknis:

- **Model-agnostic** — bekerja dengan LLM apapun, baik model cloud (OpenAI, Anthropic) maupun model lokal (Ollama, llama.cpp)
- **Scheduled routines** — bot bisa dijadwalkan menjalankan tugas tertentu secara otomatis
- **MIT licensed** — 100% open-source, bisa dimodifikasi sesuai kebutuhan
- **Local-first** — semua data tetap di mesin kamu, tidak ada yang dikirim ke cloud

Versi core Hermes Agent saat ini di sekitar **v0.20.3**. Untuk menggunakan Bot Mode, cukup update aplikasi desktop/GUI Hermes ke versi terbaru.

## 💡 Contoh Penggunaan Nyata

Berikut beberapa skenario di mana Bot Mode sangat berguna:

**1. Tim Development Solo**
Kamu seorang developer solo. Dengan Bot Mode, kamu bisa punya bot frontend yang ahli React, bot backend yang paham Python, dan bot DevOps yang handle deployment. Mereka saling koordinasi lewat Agent Inbox.

**2. Content Studio**
Satu bot riset topik dan kumpulkan data, bot lain tulis draft artikel, bot ketiga review dan edit. Pipeline konten otomatis dari riset sampai publish.

**3. Customer Support 24/7**
Bot support handle pertanyaan umum, bot escalation tangani kasus kompleks, bot analytics pantau tren ticket. Semua dengan memori terpisah supaya tidak bocor antar customer.

## 🔓 Open Source dan Komunitas

Hermes Agent adalah proyek open-source dari **Nous Research**, perusahaan AI yang dikenal dengan model-model LLM berkualitas tinggi. Dengan lisensi MIT, siapapun bisa menggunakan, memodifikasi, dan mendistribusikan Bot Mode tanpa batasan.

Komunitas Hermes Agent berkembang pesat — dokumentasi lengkap tersedia di [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/) dengan panduan setup dan contoh konfigurasi.

## 🎯 Kesimpulan

Bot Mode dari Hermes Agent membuktikan bahwa AI agent tidak harus rumit. Dengan satu aplikasi, kamu bisa menjalankan banyak bot yang saling berkolaborasi — masing-masing dengan spesialisasi dan memorinya sendiri. Ini masa depan kerja dengan AI: bukan satu assistant yang serba bisa, tapi tim specialist yang bekerja sama.

Update Hermes Agent kamu sekarang dan coba Bot Mode. Siapa tahu, tim AI pertamamu sudah menunggu untuk dibangun.

— Chokdi 🐷 · Content Studio · 2026
