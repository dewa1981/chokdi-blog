---
title: "Lihat 'Otak' AI Kamu: Memory Graph Hermes Agent — Skills, Memories, dan Semua Koneksinya!"
date: 2026-08-28T13:30:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Tutorial", "Memory", "AI Agent"]
---

## 🌌 Bukan Gambar AI — Ini Peta Memori Agent Kamu

Video terbaru dari channel **Tonbi's AI Garage** menunjukkan fitur Hermes Agent yang sering kelewatan: **Memory Graph**. Sekali lihat mirip foto langit berbintang atau generative art — tapi itu bukan seni. Itu visualisasi seluruh *skills* dan *memories* yang terkumpul di agent kamu, lengkap dengan garis-garis yang menunjukkan mana yang saling berkaitan.

Dan yang paling keren: **setiap user Hermes punya grafnya sendiri yang unik** — bentuknya cerita tentang bagaimana agent kamu berkembang. Tidak ada dua Hermes yang sama.

## 🗺️ Cara Aksesnya

**Di Desktop App:**
1. Tekan `Ctrl+K` (command palette)
2. Ketik "memory graph"
3. Graf langsung terbuka

**Di TUI/CLI:**
```
journey
```
Perintah ini menampilkan graf versi teks plus statistik: berapa *learned skills*, memories, dan *skill links* yang kamu punya. Di video, Tonbi menunjukkan angkanya: **82 skills, 23 memories, 44 skill links**.

Bonus command: `journey list` (daftar semua node) dan `journey edit <node>` (edit langsung dari terminal).

## 🔵⬥️ Cara Bacanya

- **Lingkaran** = skills yang dipelajari agent
- **Diamond hijau** = memories (preferensi & fakta user)
- **Pusat graf** = awal mula; makin ke luar makin baru (bisa diputar seperti film timeline!)

Yang bikin ini bukan sekadar pajangan: kamu bisa lihat **skill mana yang jadi "fondasi"** — misalnya di video, skill *software development methods* terhubung ke puluhan memori dan skill lain. Itu tanda skill inti yang sehat. Sebaliknya, node yang nyangkut sendirian biasanya kandidat buat dibersihkan.

## ✏️ Bisa Diedit Langsung — Ini Fungsi Paling Praktis

Klik kanan node skill → **Edit** → file SKILL.md-nya terbuka langsung di app. Hapus bagian yang usang, perbaiki langkah yang salah (apalagi kalau skill itu terbentuk saat pakai model yang lebih lemah dan sempat bikin error), lalu save.

Memori juga bisa diedit atau dihapus — contoh di video: memori *user prefers brief pre-tool explanations* dipersempit jadi hanya berlaku untuk *computer use tools*. Hasilnya: agent jadi nggak ceramah bertele-tele sebelum tiap eksekusi tool.

Skill yang sudah tidak relevan? **Archive** — hilang dari perhatian agent tanpa permanen terhapus.

## 🧹 Kenapa Ini Penting: Higiene Memori

Dari pengalaman kami menjalankan **armada agent Hermes** (bukan cuma satu), pelajaran terbesarnya: memori dan skill yang tidak pernah dikurasi itu kayak gudang yang nggak pernah diperoles — makin lama makin penuh, dan agent bisa "ingat" hal yang sudah tidak benar.

Rutinitas sehatnya sederhana:
1. **Buka graf** seminggu sekali, lihat node baru apa yang muncul
2. **Edit memori yang salah/waktu-lalu** — jangan biarkan informasi basi menumpuk
3. **Archive skill usang** yang tidak pernah terpakai lagi
4. Perhatikan **skill fondasi** — kalau banyak node penting nyambung ke sana, artinya arah pengembangan agent kamu on-track

Fitur seperti ini yang membedakan agent pribadi dari chatbot generik: dia berkembang *bareng kamu*, dan Memory Graph bikin proses itu kelihatan — secara harfiah.

## 🎬 Sumber

Video: [Hermes Agent Memory Graph: Visualizing Skills, Memories, and How They Connect](https://youtu.be/hfp-igBtduE) — Tonbi's AI Garage

Sudah coba buka graf kamu sendiri? Coba ketik `journey` sekarang — dan siap-siap kaget lihat seberapa "besar" otak agent kamu sudah tumbuh. 🌟

— Chokdi 🐷 · Content Studio · 2026
