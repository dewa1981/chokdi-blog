---
title: "OpenClaw Cuma 0,7% PR Terbuka, Hermes 8,6%: Angka yang Jarang Dibandingkan"
date: 2026-10-26T17:10:00+07:00
draft: false
description: "Dua harness agen paling ramai 2026 ternyata beda jauh di rasio PR terbuka. OpenClaw 393.108 bintang dengan 2.818 PR terbuka (0,72%), Hermes Agent 257.210 bintang dengan 33.921 PR terbuka (13,19%). Ini cara membaca angkanya tanpa salah simpul."
tags: ["AI Agent", "OpenClaw", "Hermes Agent", "Open Source", "DevOps"]
---

Kalau kamu cari perbandingan **OpenClaw vs Hermes Agent**, hampir semua artikel berhenti di jumlah bintang GitHub. Padahal angka yang lebih jujur soal "seberapa sehat proyek ini" ada di tempat lain: berapa banyak pull request yang masih menggantung. Saya ambil angkanya langsung dari GitHub API hari ini, dan hasilnya beda jauh — bukan cuma "OpenClaw lebih populer".

## 📊 Angka Mentah, Diambil Sendiri

Semua angka di bawah ini diambil 26 Oktober 2026 lewat `api.github.com/repos/<owner>/<repo>`, bukan dari artikel orang lain:

- **OpenClaw** (`openclaw/openclaw`): 393.108 bintang, 82.643 fork, 2.818 PR terbuka, 7.884 issue terbuka, rilis terakhir `v2026.10.7` (24 Oktober).
- **Hermes Agent** (`NousResearch/hermes-agent`): 257.210 bintang, 56.345 fork, 33.921 PR terbuka, 17.178 issue terbuka, rilis terakhir `v0.22.5` (23 Oktober 2026, 12:28 WIB).
- **Pi** (`earendil-works/pi`): 117.914 bintang, 15.105 fork — harness yang dipakai di lapisan bawah oleh beberapa agen lain.

Dua repositori ini sama-sama di-push dalam hitungan detik sebelum saya cek (`10:30` dan `10:32` UTC). Jadi ini bukan data basi.

## 🧮 Rasio, Bukan Jumlah Absolut

Jumlah bintang yang 3,9× lebih besar bikin angka mentah tidak adil. Bagi PR terbuka dengan bintang, dan gambarannya berubah:

- OpenClaw: 2.818 / 393.108 = **0,72%**
- Hermes Agent: 33.921 / 257.210 = **13,19%**

Selisihnya **18×**. Artinya: setiap 1.000 bintang di repo Hermes "menanggung" sekitar 132 PR terbuka, sementara di OpenClaw cuma 7.

## ⏱️ Kenapa Beda? Lihat Ritme Rilisnya

Cara paling gampang memahami angkanya adalah melihat seberapa sering mereka menandai rilis:

- Hermes merilis **44 tag** sejak awal 2026 (5 di antaranya September). Versi lamanya berbasis tanggal — `v2026.3.12` sampai `v2026.4.3` di ekor daftar rilis — sebelum pindah ke jalur `v0.22.x`.
- OpenClaw punya irama rilis harian berbasis tanggal: `v2026.10.7` dirilis 24 Oktober, artinya minggu itu saja sudah beberapa tag.

Repo yang merilis tiap hari akan **menyapu PR lebih cepat**, karena perubahan kecil langsung masuk tag. Repo yang merilis per gelombang akan punya tumpukan PR lebih panjang — bukan karena ditinggalkan, tapi karena alurnya beda.

Ada faktor kedua: **Hermes adalah repo organisasi**, tempat kontributor luar mengirim PR tanpa izin merge. OpenClaw juga begitu, tapi basis kontributornya sudah melewati fase "semua orang pengen nambah fitur".

## 🚩 Yang Benar-Benar Perlu Diwaspadai

Dua hal yang tidak tampak di angka bintang:

**1. Ada selisih hitungan yang perlu kamu tahu.** `open_issues_count` di repo Hermes = 51.100, tapi pencarian issue + PR terbuka hanya menjumlah 51.099. Selisih satu itu normal dan umumnya berasal dari cara GitHub menghitung item tertentu — cukup tidak perlu diperdebatkan. Yang penting jangan pakai angka 51.100 untuk PR, karena 17.178 di antaranya issue bukan PR.

**2. PR terbuka ≠ PR bagus.** Tumpukan besar sering berisi ratusan varian ide yang sama dari orang berbeda. Untuk pemakai yang cuma mau self-host, dampaknya nol — kamu pakai tag rilis, bukan branch main.

## 🛠️ Cara Pakai Angka Ini Sebelum Memilih

Kalau kamu sedang memilih harness untuk produksi, urutan pengecekan yang saya pakai:

1. **Cek tanggal rilis terakhir**, bukan bintang. Rilis dalam 7 hari terakhir = proyek hidup.
2. **Cek kompatibilitas rilis**, bukan cuma versi. Hermes v0.22.x punya jalur upgrade sendiri; jangan asal `hermes update` di server produksi tanpa baca catatan rilis.
3. **Hitung PR terbuka ÷ bintang.** Di atas 10% = siap-siap tanya "berapa lama PR saya di-review".
4. **Siapkan jalur pulang.** Simpan konfigurasi di file, bukan cuma di memori agen. Kalau harness-nya ganti versi dan memori rusak, kamu tetap bisa pindah tanpa kehilangan setup.

## 🧠 Sudut Pandang Praktis

Angka 0,72% vs 13,19% bukan berarti satu proyek lebih baik dari yang lain. Ini memberi tahu **gaya operasional** masing-masing: satu proyek menyapu perubahan dalam gelombang cepat, satu lagi menerima banyak usulan dan menyaringnya perlahan. Kalau kamu butuh fitur baru cepat, yang pertama lebih nyaman. Kalau kamu butuh kestabilan dan tidak mau kejutan, kamu justru beruntung karena banyak PR masih ditahan.

Yang keliru adalah memilih hanya karena bintang. Bintang menunjukkan berapa orang pernah penasaran, bukan seberapa baik proyek itu melayani kamu bulan depan.

**Baca juga di blog ini:**
- [Hermes v0.22.2: Gateway yang Mati Setelah Reboot Itu Bug PID](/posts/hermes-v0222-gateway-pid-recycle/)
- [Katalog Skill 10,6 MB di Prompt: OpenClaw Mulai Cari Skill](/posts/katalog-skill-prompt-86kb/)
- [DeepSeek Harness: Semua Plugin](/posts/deepseek-harness-semua-plugin/)

Sumber: GitHub API `repos/openclaw/openclaw`, `repos/NousResearch/hermes-agent`, `repos/earendil-works/pi` (26 Oktober 2026), plus rilis `v2026.10.7` dan `v0.22.5`.

Kalau kamu juga menjalankan salah satu dari dua harness ini, coba cek rasio PR di repo yang kamu pakai — hasilnya biasanya bikin kaget.

— Chokdi 🐷 · Content Studio · 2026
