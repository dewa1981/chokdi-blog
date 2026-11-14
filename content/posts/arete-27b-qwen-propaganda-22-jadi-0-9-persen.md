---
title: "Arete-27B: Qwen 27B Dicuci Satu Fine-Tune, Propaganda 22% Jadi 0,9%"
date: 2026-11-15T01:20:00+07:00
draft: false
tags: ["AI", "Open Source", "Qwen", "Nous Research", "Local LLM", "Model Open"]
---

Nous Research — rumahnya Hermes Agent — merilis **Arete-27B** awal November 2026. Bukan model baru dari nol: ini **Qwen3.8-27B milik Alibaba** yang di-*post-training* supaya berhenti mengulang narasi resmi Partai Komunis China. Hasil eval mereka: jawaban berbau propaganda turun dari **22% ke 0,9%**, sementara kemampuan umumnya nyaris tidak bergerak. Masalahnya buat kita: kalau satu fine-tune bisa mengubah "kepribadian" model, model apa pun yang kamu self-host bisa berganti nilai tanpa kamu sadari.

## 🧪 Bukan model baru — cuma satu fine-tune

Arete-27B berangkat dari Qwen3.8-27B, model open yang kuat untuk jalan lokal. Nous memilih basis itu karena paling performan di kelasnya **dan** paling banyak menunjukkan perilaku yang mereka incar: penolakan, pengalihan, sampai jawaban berbingkai resmi negara pada topik sensitif.

Yang dipakai cuma **supervised fine-tuning (SFT)**: tanpa RL, tanpa preference optimization, tanpa ubah arsitektur. Guru datanya model open bernama Inkling, supaya tidak kena batasan "illicit distillation" milik model komersial.

Resep latihannya biasa saja, dan justru itu poinnya:

- **28.886 contoh** latihan, sekitar **52,8 juta token**
- **2 epoch**, **1.202 step**, batch 48, konteks **64k**
- Learning rate 1e-5, AdamW, bf16 dengan master weight fp32
- Checkpoint yang dievaluasi: step 1.202

## 📊 Angkanya: 22% jadi 0,9%

| Model | Skor fakta (0–5) | Jawaban berbau propaganda |
|---|---|---|
| Inkling (guru) | 3,96 | 0,3% |
| Mistral Large 4 | 3,65 | 0,3% |
| Nemotron 3 Ultra | 3,22 | 0,6% |
| GLM 5.3 | 3,10 | 15% |
| **Arete-27B** | **2,98** | **0,9%** |
| DeepSeek V4.1 Flash | 2,39 | 16% |
| Qwen3.8-27B (basis) | 2,32 | 22% |

Bacanya gampang: Qwen biasa menjawab 22 dari 100 prompt dengan narasi resmi China. Setelah satu fine-tune, tinggal **0,9 dari 100**. Skor faktanya juga naik dari 2,32 ke 2,98 dari maksimal 5, dan jumlah jawaban bernilai nol turun dari **359 jadi 216** dari 803 prompt. Kategori yang paling jebol perbaikannya: kebebasan berpendapat — skor fakta 0,89 → 2,44, propaganda 60% → 1%.

Di benchmark kemampuan, **tidak ada regresi berarti**. Hermes Bench 65,77% → 65,60% (dianggap noise), Terminal-Bench-2.1 67% → 70% (mereka sendiri tidak mengklaim kenaikan itu).

## 🧭 Cara mereka mengukur — ini bagian yang paling berguna

Eval-nya dibuka publik, dan metodologinya bisa kita tiru:

- **803 prompt** dari statuta pemerintah, berita, dan laporan riset berbahasa Inggris; satu sumber maksimal menyumbang 13 prompt.
- Tujuh kategori nilai: kebebasan berpendapat, ideologi negara, negara vs pasar bebas, pendidikan, privasi data & pengawasan, demokrasi, lingkungan.
- Setiap prompt punya **2–4 fakta wajib** dari artikel sumber, plus frasa baku yang biasa dipakai negara.
- Juri: **Grok 4.7**, tidak diberi tahu model mana yang menulis jawaban (buta), rubrik dikunci dan diuji di pilot 25 prompt yang dinilai manusia lalu direvisi tiga kali.
- Prompt latihan yang beririsan dengan set evaluasi **dibuang** sebelum training.

Datanya ada di Hugging Face: `Propaganda_Eval` (eval) dan `arete-data-pairs` (data latih). Bobot Arete-27B juga terbuka, dan sebulan terakhir sudah diunduh sekitar 6.191 kali, dengan 53 versi kuantisasi dan 13 fine-tune turunan.

## 🚨 Lima hal yang wajib kamu waspadai

1. **Eval buatan sendiri tetap eval buatan sendiri.** Yang menilai dan yang melatih adalah pihak yang sama.
2. **803 prompt itu kecil.** Cukup untuk sinyal, belum cukup untuk klaim "bebas bias".
3. **Kategori nilainya ditentukan pembuatnya.** Pilih kategori lain, hasilnya bisa lain cerita.
4. **Juri LLM bukan juri netral.** Mereka mengakui sendiri rubriknya perlu direvisi tiga kali karena beda dengan penilaian manusia.
5. **Kapabilitas hanya diuji di dua benchmark.** Bukan jaminan untuk tugas coding atau agentic jangka panjang.

## 🛠️ Praktisnya buat yang self-host

- **Jalankan eval publik ke model kamu**, bukan cuma baca klaim vendor. Datasetnya terbuka, tinggal pasang model dan bandingkan.
- **Uji A/B di pekerjaan nyata kamu** — ringkas dokumen, jawab pertanyaan faktual, tulis kode. Skor benchmark tidak mewakili use case kamu.
- **Jangan bergantung pada satu model** untuk fact-finding. Risiko "gagal bersamaan" (correlated failure) itu nyata kalau semua agent kamu pakai bobot yang sama.
- **Catat versi dan dataset** setiap ganti model — tanpa itu, kamu tidak tahu kenapa jawaban berubah bulan depan.

## 💡 Kenapa ini lebih besar dari satu model

Nous menyebut satu temuan yang relevan buat yang kerja di lapangan: ada studi yang menemukan **kualitas kode ikut berubah** kalau model mengira dia sedang bekerja untuk entitas tertentu. Artinya bias model bukan cuma soal politik — bisa bocor jadi bug dan celah keamanan di produk kamu.

Kesimpulan mereka sederhana dan sulit dibantah: **nilai sebuah model open itu cuma satu fine-tune jauhnya.** Kalau nilai bisa diganti dalam hitungan jam training GPU, memilih model bukan lagi soal siapa paling pintar di benchmark — tapi soal **nilai siapa yang kamu bawa ke produkmu**, dan apakah kamu pernah memeriksanya.

Kamu sudah pernah nge-test bias model yang kamu pakai? Tulis di kolom komentar — atau mulai dari eval 803 prompt itu, hasilnya sering bikin kaget.

**Baca juga:** [Hermes Agent v0.22.7 Rilis 3 November: Agent Open-Source Terbesar Nous Research Kini Punya 'Pintu Depan'](https://chokdi.ano99.com/posts/hermes-agent-v0227-threshold-update-november-2026/) · [Hermes Agent v0.22 "Threshold" — Setup Tanpa API Key & 600 Plugin](https://chokdi.ano99.com/posts/hermes-agent-v022-threshold-600-plugin/) · [Hermes Agent v0.20.6 Rilis: 525 PR dalam Seminggu, Ini yang Wajib Kamu Tahu](https://chokdi.ano99.com/posts/hermes-agent-v0206-update/)

— Chokdi 🐷 · Content Studio · 2026
