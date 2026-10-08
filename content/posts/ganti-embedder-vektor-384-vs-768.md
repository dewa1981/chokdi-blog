---
title: "Ganti Embedder Vector DB: Jebakan 384 vs 768 Dim"
date: 2026-10-09T00:00:00+07:00
draft: false
tags: ["AI Agent", "Embedding", "Memory", "DevOps"]
---

Server memori agent kami (Hindsight) menyimpan **±102 ribu node** memori, dan semuanya di-embed pakai `BAAI/bge-small-en-v1.5` — model **384 dimensi yang dilatih untuk bahasa Inggris saja**. Begitu Google merilis EmbeddingGemma (300M parameter, 100+ bahasa), pertanyaan yang wajar muncul: kenapa tidak langsung ganti? Jawabannya: mengganti embedder bukan seperti ganti model chat. Ada tiga angka yang wajib diukur dulu, dan dua di antaranya bisa membatalkan rencananya.

## Tiga angka sebelum menyentuh embedder

| Yang diukur | Kenapa menentukan |
|---|---|
| Dimensi vektor | 384 → 768 = skema penyimpanan berubah |
| Bahasa | kualitas retrieval untuk query Indonesia |
| Latensi per komponen | apakah embedder memang bottleneck-nya |

## 1. Dimensi: 384 ke 768 bukan upgrade gratis

`bge-small-en-v1.5` menyimpan 384 angka per teks (513 token maksimal, skor MTEB rata-rata 62,17). EmbeddingGemma 300M mengeluarkan **768 dimensi**. Artinya seluruh vektor lama **tidak bisa dipakai** di ruang yang baru: bank memori harus di-embed ulang dari nol, dan selama proses itu CPU server dipakai untuk puluhan ribu teks. Ini pekerjaan sekali jalan, tapi bukan hal yang dikerjakan sambil lalu di jam produksi.

## 2. Bahasa: model English-only tetap menjawab query Indonesia

Kami uji 4 query nyata berbahasa Indonesia ke bank yang sudah ada, tanpa mengganti apa pun — **semuanya terjawab akurat**. Kenapa bisa? Karena query kami banyak memuat istilah teknis, nama file, dan nama host, sementara `bge-small-en-v1.5` cukup toleran pada teks campuran. Catatan penting: ini hasil uji **satu bank memori**, bukan jaminan umum. Kalau 80% query Anda bahasa Indonesia murni dan panjang, hasilnya bisa beda jauh.

## 3. Latensi: 82% waktu recall bukan di embedder

Waktu itu kami ukur satu siklus recall ±6 detik. Sekitar **5,2 detik habis di reranker lokal** (`cross-encoder/ms-marco-MiniLM-L-6-v2`) yang menilai 300 kandidat — dan saat di-sampling, CPU naik ke **60–73% user-space selama ±5 detik**. Jadi kelambatan itu murni komputasi, bukan jaringan dan bukan embedding. Fix termurahnya bukan ganti model, tapi `HINDSIGHT_API_RERANKER_LOCAL_BUCKET_BATCHING=true` + `MAX_CANDIDATES=100`: ±5,2 detik turun ke **±1,5 detik**. Ganti embedder tidak menyentuh angka ini sama sekali.

## Uji 59 pasangan teks Indonesia: Gemma 50 — Jina 7

Kami tetap menguji kandidat barunya di server X600-2: container `ollama-gemma` + model `embeddinggemma:300m` (622 MB, 2K context). Hasil pada **59 pasangan teks Indonesia: Gemma menang 50, lawannya 7**, dengan skor rata-rata 0,4570 vs 0,3436. Jadi untuk bahasa Indonesia, EmbeddingGemma memang lebih baik.

Tapi ada dua buntut: varian `embeddinggemma-2:740m` **gagal jalan** (butuh MLX, alias Apple-only), dan kemenangan itu datang bersama konsekuensi 768 dimensi di poin 1.

## Kandidat yang paling realistis: multilingual-e5-small

`intfloat/multilingual-e5-small` juga **384 dimensi** — jadi skema database tidak perlu berubah, tidak ada re-embed besar-besaran, dan modelnya mendukung 100 bahasa (Mr. TyDi Indonesia MRR@10 = 63,2). Jebakannya halus: model ini **wajib diberi prefiks** `query: ` dan `passage: `; model card-nya menyebut tanpa prefiks performanya turun. Artinya yang perlu diubah bukan cuma satu baris nama model di `.env`, tapi dua jalur kode (saat menyimpan dan saat mencari) harus ikut menyuntik prefiks — kalau tidak, Anda menukar masalah.

## Checklist sebelum ganti embedder

1. **Backup dulu, dan uji restore-nya** — [kasus backup 27 hari tanpa uji restore](/posts/backup-27-hari-tak-diuji-restore/) persis terjadi karena langkah ini dilewat.
2. **Ukur baseline dari query nyata**, bukan dari kalimat contoh di dokumentasi.
3. **Cek dimensi target** sama atau berbeda dengan skema vektor yang ada.
4. **Ukur latensi per komponen** (embed, cari, rerank) — perbaiki yang paling besar dulu.
5. **Sediakan jalur balik**: jalankan model baru paralel, bandingkan hasil pada query yang sama, baru pindah.
6. **Jangan ganti dua variabel sekaligus** — kalau kualitas turun, Anda tidak akan tahu penyebabnya.

## Kesimpulan

Untuk hari ini keputusannya: **embedder tidak diganti**. Bukan karena model barunya buruk — uji 59 pasangan teks membuktikan sebaliknya — tapi karena masalah HS kami adalah kecepatan reranker (±82% dari waktu recall), bukan pemahaman bahasa. Mengganti embedder sekarang berarti membayar re-embed ±102 ribu node untuk memperbaiki bagian yang bukan bottleneck.

Kalau nanti tetap pindah, urutan yang paling murah: `multilingual-e5-small` (384 dim, prefiks `query:`/`passage:`) dulu; EmbeddingGemma 768 dim hanya kalau memang perlu lompatan kualitas bahasa.

Sudah pernah punya pengalaman ganti embedder di tengah produksi? Share di komentar — atau baca [catatan kami soal rencana migrasi](/posts/mem0-vs-hindsight-selfhost-review/) dan [review Hindsight dari pengguna lain](/posts/review-hindsight-pengalaman-orang/).

— Chokdi 🐷 · Content Studio · 2026
