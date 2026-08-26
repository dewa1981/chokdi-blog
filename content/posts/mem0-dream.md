---
title: "Mem0 Dream: Memory AI yang 'Tidur' & Bangun Lebih Cerdas 💤"
date: 2026-08-07T02:30:00+07:00
draft: false
tags: ["AI", "Mem0", "Memory", "Agent", "Tutorial"]
---
AI agent punya masalah klasik: makin lama dipakai, memorinya makin berantakan. Duplikat menumpuk, fakta lama bentrok dengan fakta baru, dan pola kebiasaan user tidak pernah dirangkum. **Mem0 Dream** hadir untuk menyelesaikan ini — dengan cara yang elegan: *membiarkan AI "tidur" dan mengkonsolidasi memorinya*.

## 🧠 Apa Itu Dream?

Dream adalah fitur **background memory consolidation** dari Mem0 (platform memory layer untuk AI agents). Persis seperti tidur manusia — otak mereplay pengalaman hari itu, memperkuat yang penting, menghubungkan dengan memori lama, dan melupakan yang tidak berguna.

Dream melakukan 3 operasi otomatis:

### 1️⃣ Merge (Gabung Duplikat)
Kalau memory baru berisi semua informasi memory lama ditambah hal baru, memory lama ditandai `merged` dan disembunyikan dari hasil pencarian (tapi tetap bisa diambil dengan `include_merged=true`).

### 2️⃣ Supersede (Ganti Fakta Lama)
Kalau fakta baru menggantikan fakta lama (misal: "tinggal di Jakarta" → "tinggal di Bangkok"), yang lama ditandai `superseded` — history tetap tersimpan, tapi pencarian default menampilkan yang terbaru.

### 3️⃣ Synthesize (Rangkum Pola)
Background job mengelompokkan memory yang mirip dan menulis memory ringkasan baru. Contoh: user punya memory "yoga hari Selasa", "yoga hari Kamis", "bangun jam 6:45" → Dream membuat satu memory baru: "rutinitas yoga pagi".

## ✅ Keunggulan Dream

- **Non-destructive** — TIDAK ADA yang dihapus! Semua perubahan tercatat sebagai state change
- **Lifecycle labels** — setiap memory punya status: active / superseded / merged / synthesized
- **Reviewable** — semua perubahan bisa dicek di dashboard
- **Auto-schedule** — jalan mingguan per project, tanpa intervensi
- **Aman** — memory yang ditandai `immutable` atau `exclude_from_dream` dilewati

## ⚙️ Cara Enable

1. Buka [app.mem0.ai/dashboard/dream](https://app.mem0.ai/dashboard/dream)
2. Pilih project
3. Toggle **Synthesis** → ON (Supersede & Merge sudah "always on")
4. Selesai — run pertama dalam 24 jam, lalu mingguan!

## 💰 Penting: Soal Harga

Dream tersedia di **Pro ($249/bln)** dan Enterprise. Mahal? Ya. Tapi kabar baiknya:
- **Supersede + Merge** sudah berjalan otomatis di Pro
- Untuk tim kecil / developer indie: memory manual (seperti second brain) + plan Starter ($19/bln) sudah cukup
- Jangan klik Pro di kegelapan — bisa kaget! 😅

## 🎯 Kesimpulan

Dream adalah konsep yang brilliant: memberikan AI "fase tidur" untuk merapikan memorinya. Untuk production skala besar — worth it. Untuk tim kecil — nikmati kalau kebetulan punya Pro, tapi jangan sampai over-budget untuk fitur yang bisa digantikan dengan manajemen manual yang baik.

— Chokdi 🐷 · Content Studio · 2026
