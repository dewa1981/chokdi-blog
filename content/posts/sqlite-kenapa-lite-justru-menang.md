---
title: "SQLite: Kenapa yang 'Lite' Justru Menang 🗄️"
date: 2026-08-07T22:00:00+07:00
draft: false
tags: ["SQLite", "Database", "Postgres", "Backend", "FastGaji"]
---
Banyak orang mengira "lite" di SQLite berarti "kemampuan rendah". Padahal justru sebaliknya — **"lite" di sini adalah KEKUATAN**: SQLite adalah *library* (bukan server!), berupa file di disk kamu sendiri — GRATIS, CEPAT, dan mengalahkan Postgres di banyak skenario!

## 🤔 Refleks yang Keliru

Banyak developer LANGSUNG memasang Postgres — padahal aplikasinya cuma berjalan di satu box dan melayani beberapa ratus user per hari. Itu "refleks, bukan keputusan"!

## ⚡ Kenapa SQLite Cepat (Arsitektur!)

```
POSTGRES = server terpisah — tiap query = ROUND TRIP
   (serialize → kernel → wire → parse!)

SQLITE = LIBRARY — query = FUNCTION CALL di dalam proses kamu!
   (tidak ada wire untuk ditunggu!)
```

- Lookup primary key: **10-an mikrodetik** vs ratusan mikrodetik
- 40 query per render halaman → wire tax = sebagian besar latency budget!

## 📱 Fakta Gila: "Lite" Justru JUARA

- **4 miliar smartphone** — masing-masing membawa RATUSAN file SQLite!
- Total: **LEBIH DARI 1 TRILIUN database hidup!**
- SQLite masih rilis baru tiap bulan — sangat aktif!

## 💰 Biaya: Gratis vs Ratusan Dolar

```
POSTGRES (Amazon RDS):
  $15/bln (entry!) → $143/bln (production!)
  → $475/bln (multi-AZ + read replica + 200GB — SELAMANYA!)

SQLITE: GRATIS — karena cuma file + driver sudah built-in di bahasa!
```

## 📊 Bukti Benchmark (Intuit — diuji beneran!)

SQLite vs Postgres 16 (mesin sama, 1 vCPU, 8GB):

| Metrik | SQLite | Postgres 16 |
|--------|--------|-------------|
| Median response | **500ms** ✅ | 640ms |
| Throughput | **5.1 req/s** ✅ | 4.1 req/s |
| 99th percentile | **8.2s** ✅ | 14s |

Kesimpulan resmi: *"SQLite WAL mode bersaing SERIUS dengan Postgres 16 dan MENGALAHKANNYA di kebanyakan pola read!"*

**Produksi nyata:**
- sqlite.org: 400-500 RIBU request/hari — database-nya = SQLite!
- Forward Email: 10.500 inserts/detik!
- Expensify (2018): **4 JUTA queries/detik** (1 server, 10 miliar rows!)

## 🧱 Tiga Dinding (Limit SQLite — Jujur!)

### Wall 1 — Concurrent Writers
- "database is locked!" — cuma 1 writer per instant (readers unlimited!)
- **FIX**: WAL mode (readers gak block writers!) + busy timeout + BEGIN CONCURRENT
- **TURSO**: rewrite SQLite di Rust (24K stars! MVCC!) — 4x LEBIH CEPAT + concurrent writers level ROW (baru rilis preview!)

### Wall 2 — Second App Server (Fisika!)
- File di 1 mesin — app server ke-2 tidak bisa reach (NFS = korup!)
- **FIX**: LITESTREAM (stream WAL ke object storage — backup/restore real-time!)
- **CLOUDFLARE Durable Objects**: setiap DO = SQLite sendiri (12KB kosong! 10GB max!) — "million small databases" — setiap tenant punya file sendiri!

### Wall 3 — Ekstensi Postgres (Jangan Dilawan!)
- 1000+ add-ons: PostGIS (geospasial!), PGVector (ANN search!)
- Users/roles/row-level security (SQLite: OS yang pegang file!)
- **Kalau butuh ini → pakai Postgres** — itu engineering, bukan habit!

## ✅ Aturan 4 Pertanyaan (Keputusan Cepat!)

1. Satu deployable unit?
2. Writers sentuh ROW BEDA?
3. Data < beberapa ratus GB?
4. Gak ada ekstensi yang gak bisa hidup tanpa?

**4 YES = PAKAI SQLITE** (skip instance sama sekali!)
**1 miss = network database** (Postgres!)

## 🔄 Plot Twist: Turso

TURSO — yang rewrite SQLite — sekarang membangun **database POSTGRES-COMPATIBLE di core Rust yang SAMA**! "One engine, many front ends — LLVM of databases!"

CEO Turso: *"Tidak ada yang fundamentally salah dengan Postgres — kalau ada, kami gak akan rewrite-nya!"*

## 💡 Relevansi untuk Kita

```
✅ FASTGAJI (app gaji karyawan): SQLite = PILIHAN TEPAT!
   → 1 box + beberapa user + data kecil → 4 YES → SQLite!
   → GRATIS + cepat + gampang backup (file doang!)

✅ HERMES: session store = SQLite! (ringan + cepat!)

✅ PELAJARAN: "Lite" = SIMPLICITY + POWER — bukan "lemah"!
   → File di disk sendiri + zero config + gratis = JUARA buat skala kita!
```

**Jadi: "Lite" bukan berarti lemah — justru itu yang bikin SQLite menang: sederhana, cepat, gratis, dan tanpa server untuk diurus!** 🏆

— Chokdi 🐷 · Content Studio · 2026
