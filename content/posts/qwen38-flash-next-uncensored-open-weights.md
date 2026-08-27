---
title: "Qwen3.8-Flash-Next-Uncensored Rilis Open Weights: 262K Konteks, Native MLX, Tanpa Filter!"
date: 2026-08-28T11:00:00+07:00
draft: false
tags: ["AI", "Qwen", "Open Weights", "LLM", "Local LLM", "Apple Silicon"]
---

## 🐳 OrcaRouter Bocorkan "Senjata" Baru — Dan Kali Ini Tanpa Sensor!

Minggu ini dunia open-source LLM lagi rame banget. Setelah Z.ai resmikan GLM-5.3-Flash, giliran **OrcaRouter** yang nge-shock: mereka rilis bobot (weights) untuk model bernama **Qwen3.8-Flash-Next-Uncensored** — varian keluarga Qwen3.8 yang **dilepas tanpa content filter**.

Pengumumannya singkat tapi pedas, di-post via akun X @orcarouter pada 27 Agustus 2026:

> "We're excited to ship our weights for Qwen3.8-Flash-Next-Uncensored. Built, as always, for security researchers, red teams & blue teams. GGUF + native MLX. Up to 262K context. Run it locally. Break things responsibly. Have fun."

Post-nya langsung disambut ratusan ribu penasaran — hampir 900 likes dalam hitungan jam.

## 📋 Spesifikasi Singkat

| Detail | Keterangan |
|---|---|
| Model | Qwen3.8-Flash-Next varian **Uncensored** |
| Format | **GGUF** (untuk llama.cpp/Ollama) + **native MLX** (Apple Silicon) |
| Konteks | Hingga **262.000 token** |
| Target | Security researchers, red team & blue team |
| Lisensi | Open weights — bisa diunduh & dijalankan lokal |
| Sumber | HuggingFace: `orcarouter/Qwen3.8-Flash-Next-Uncensored` (GGUF & MLX) |

## 🍎 Native MLX — Kabar Gembira Buat Pengguna Mac

Yang bikin release ini spesial: tersedia **native MLX**, format deep-learning optimized buatan Apple khusus chip Apple Silicon (M-series). Artinya:

- **Mac Mini / MacBook M1-M5** bisa jalanin model ini jauh lebih hemat RAM dibanding format GGUF biasa
- Cocok buat eksperimen **self-host LLM offline** — tanpa biaya per-token, tanpa kirim data ke cloud
- Buat yang nunggu Mac Studio M5 Ultra buat jadi "otak lokal 24/7", model semacam ini adalah kandidat kuat isi harddisk-nya

## ⚠️ "Uncensored" Itu Kayu Api Dua Sisi

Varian uncensored memang jadi andalan buat:

1. **Red team / pentester** — butuh model yang gak menolak analisis malware, exploit, atau payload
2. **Kreator konten dewasa/komersial** — model standar sering nolak topik tertentu
3. **Riset alignment** — mempelajari bagaimana filter memengaruhi perilaku model

Tapi ingat: kebebasan penuh = tanggung jawab penuh. Jalankan secara lokal, jangan dibikin jadi layanan publik tanpa pengawasan, dan patuhi hukum setempat.

## 🤔 Catatan dari Kami: Pantau, Jangan Buru-buru

Di tim kami, keluarga Qwen3.8-Flash sudah masuk radar sejak lama — terutama untuk kebutuhan **multimodal** (kekuatan utama Qwen3.8 dibanding pesaingnya). Tapi ada dua alasan kenapa kami **belum** memakainya untuk produksi:

1. **API resmi Qwen3.8-Flash masih belum tersedia** — yang rilis sejauh ini masih open weights (justru varian Next/uncensored ini lebih dulu bocor keluar). Untuk stack produksi yang butuh stabilitas 24/7, kami tetap pakai **DeepSeek V4 Flash** yang API-nya matang dan terbukti.
2. **Varian pihak ketiga perlu diaudit dulu** — sebelum dipercaya nempel ke infrastruktur.

Kalau kebutuhanmu adalah eksperimen lokal di Mac — terutama buat testing prompt yang suka ditolak model standar — ini layak banget dicoba. GGUF-nya buat Ollama/llama.cpp, MLX-nya buat yang mau performa maksimal di Apple Silicon.

## 🎯 Kesimpulan

Rilis Qwen3.8-Flash-Next-Uncensored menandakan dua tren sekaligus: **open weights makin cepat mengejar API komersial**, dan **pasaran "model tanpa filter" makin serius** (bukan cuma proyek abal-abal di HuggingFace). Buat developer Indonesia yang mau belajar self-host LLM, ini momen bagus buat mulai — modal cukup Mac M-series atau GPU dengan VRAM memadai.

Pantau terus — begitu API resmi Qwen3.8-Flash rilis, dijamin jadi pertimbangan besar untuk berbagai workload multimodal. 😉

— Chokdi 🐷 · Content Studio · 2026
