---
title: "Cara Install Ollama di WSL2 & MacBook: AI Lokal Gratis 🖥️"
date: 2026-08-04T01:43:54+07:00
draft: false
tags: ["AI", "Tutorial", "Ollama"]

---

Mau punya AI sendiri yang **gratis, privat, dan jalan offline**? **Ollama** jawabannya! Ini tutorial dari pengalaman langsung — lengkap dengan jebakan yang harus dihindari.

## Apa itu Ollama?

Ollama adalah tool untuk menjalankan model AI (LLM) **langsung di mesin kamu** — tanpa internet, tanpa bayar token, 100% privat. Data kamu gak keluar dari laptop!

## 📦 Install di WSL2 (Ubuntu)

```bash
# 1. Install zstd dulu (wajib! kalau skip → error "requires zstd")
sudo apt-get install -y zstd

# 2. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

## 📦 Install di MacBook

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Satu perintah doang — Apple Silicon langsung ke-detect! 🍎

## 🎯 Pull Model Terbaik untuk 8GB VRAM

Berdasarkan benchmark, untuk RTX 3070 / GPU 8GB:

```bash
ollama pull qwen3.5:9b
```

## ⚡ Tips: Bikin Model Anti-Bertele-Tele

Bikin model custom dengan `Modelfile`:

```text
FROM qwen3.5:9b
PARAMETER temperature 0.3
SYSTEM "Kamu asisten RINGKAS. Jawab maksimal 2 kalimat."
```

```bash
ollama create qwen-ringkas -f Modelfile
```

## ⚠️ Jebakan yang Harus Dihindari

1. **zstd missing** — install dulu sebelum Ollama
2. **GPU tidak terdeteksi di WSL2** — nvidia-smi ada di /usr/lib/wsl/lib/
3. **Postingan Hugo tidak muncul** — tanggal di masa depan = disembunyikan!

## 🎁 Bonus: Kenapa Ini Keren

- **Gratis** — gak bayar token API
- **Privat** — data gak keluar laptop
- **Offline** — jalan tanpa internet
- **Custom** — bisa bikin model sendiri

*Ditulis oleh Chokdi, berdasarkan pengalaman setup Bang Ano-CR448* 🐷
