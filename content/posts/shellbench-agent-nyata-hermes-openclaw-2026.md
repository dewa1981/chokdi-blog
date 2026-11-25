---
title: "ShellBench: Agent AI Terbaik Cuma Selesai 6 dari 10 Tugas Nyata"
date: 2026-11-25T17:18:15+07:00
draft: false
tags: ["AI Agent", "OpenClaw", "Hermes", "Benchmark"]
---

Kalau kamu percaya agent AI bisa menggantikan pekerjaan administrasi, angka ini bakal bikin kamu berpikir ulang. ShellBench — benchmark baru yang dirilis 24 November 2026 — menemukan bahwa model terbaik di dunia hanya menyelesaikan sekitar **6 dari 10 tugas kantor nyata** secara utuh. Bukan karena tidak pintar, tapi karena satu syarat kecil yang terlewat sudah cukup membuat pekerjaan dianggap gagal.

Yang bikin benchmark ini relevan buat kita: **Hermes dan OpenClaw ikut diuji**, dan hasilnya mengejutkan.

## 🧪 Apa Itu ShellBench dan Kenapa Beda

Kebanyakan benchmark AI menguji hal rapi: jawab soal matematika, tulis fungsi Python, jawab pilihan ganda. ShellBench justru menguji kekacauan kerja sehari-hari.

Benchmark ini dibangun oleh OpenClaw Foundation bersama Parsewave, Hugging Face, Red Hat, dan UC Berkeley (dengan dukungan NVIDIA, Columbia University, serta komputasi dari AWS). Bahannya bukan soal buatan, tapi **lebih dari 10 juta interaksi agent anonim yang benar-benar terjadi**, lalu diringkas jadi 100 tugas.

Detail yang bikin deg-degan:

- **12 model** diuji: GPT-6 Astra, Claude Fable 5.2, GPT-6.1 Sol, Gemini 4 Carbon, Claude Opus 5.5, DeepSeek V4.1 Flash, Kimi K3.1 Pro, sampai GPT-6 Luna.
- **5 harness**: Claude Code, Codex, Hermes, OpenClaw, dan Pi.
- **53.100 run** dinilai, masing-masing workspace berisi median **188 file** — email, ekspor kalender, spreadsheet, log chat, struk, PDF.
- Perintahnya pendek: median hanya **43 kata**. Persis seperti kamu menyuruh asisten.

## 📊 Hasil 1: Model Terbaik Pun Cuma 62,5%

Di rata-rata lima harness, GPT-6 Astra memimpin dengan **62,5%**, disusul Claude Fable 5.2 (61,9%) dan GPT-6.1 Sol (61,4%). Jarak tiga teratas cuma **1,1 poin persen**.

Artinya: model paling mahal pun gagal memenuhi seluruh syarat di sekitar **4 dari 10 percobaan**. Dalam kerja nyata, satu syarat yang bocor bisa berarti laporan tidak layak dipakai.

## 🗂️ Hasil 2: Jawaban Benar, Tapi Bukti Tak Disebut = Gagal

Ini temuan paling menusuk. Di 77 tugas ada 87 kriteria yang mengecek apakah agent **menyebut file yang dipakai** sebagai bukti.

Contoh tugas merencanakan makan malam: **522 dari 531 percobaan** memilih restoran yang benar. Tapi **331 gagal** hanya karena rekomendasinya tidak menyebut file anggaran atau jadwal yang mendukung. Yang lolos penuh: **152 percobaan**.

Mengambil informasi, menalar, dan mempertahankannya sampai jawaban akhir adalah tiga kemampuan berbeda. Agent bisa menemukan data yang tepat, lalu tetap gagal menyampaikannya.

## 🔁 Hasil 3: Sekali Berhasil Bukan Berarti Konsisten

GPT-6 Astra menyelesaikan **75,1%** tugas setidaknya sekali dalam tiga percobaan. Tapi hanya **48,8%** yang berhasil di ketiga percobaan sekaligus.

Agent yang sukses sekali lalu gagal tiap percobaan ketiga tetap butuh pengawasan manusia. Konsistensi hanya kelihatan kalau diuji berulang, bukan sekali jalan.

## 🛡️ Hasil 4: 15,7% Run Gagal Minimal Satu Cek Keamanan

Dari seluruh 53.100 run, **15,7% gagal minimal satu pemeriksaan keamanan** — jebakan phishing, instruksi pembayaran palsu, data sensitif, atau aksi tak bisa dibatalkan. Total ada **381 kriteria keamanan**.

Lebih penting lagi: di antara 26.151 run yang **lolos semua kriteria kebenaran**, masih ada **2.589 run (9,9%)** yang gagal syarat keamanan. Jadi agent yang rajin menyelesaikan tugas belum tentu aman.

## ⚙️ Hasil 5: Model Lebih Menentukan, Tapi Harness Tetap Penting

Dalam satu harness, selisih model terbaik dan terburuk mencapai **45,7 poin persen**. Ganti harness dengan model yang sama cuma menggeser **6,2 poin**. Jadi pilih model dulu, baru harness.

Tapi harness tidak bisa dianggap sama. Rata-rata pass rate antar harness sangat rapat:

- OpenClaw: **45,23%**
- Pi: **45,22%**
- Hermes: **45,11%**
- Codex CLI: **45,04%**
- Claude Code: **42,87%**

Selisih tertinggi–terendah hanya **2,36 poin**. Pi paling cepat (median **1,31 menit** per run), OpenClaw **2,86 menit**. Kesimpulannya: harness open source tidak kalah, dan Claude Code justru ada di dasar kelompok.

## 💰 Hasil 6: Kapabilitas dan Biaya Tak Selalu Sejalan

Tiga model teratas dipisah 1,1 poin, tapi biayanya beda jauh per run:

- GPT-6 Astra: 62,5% dengan **$1,10**
- Claude Fable 5.2: 61,9% dengan **$0,83**
- GPT-6.1 Sol: 61,4% dengan **$0,19** — hampir seperenam biaya pemimpin
- DeepSeek V4.1 Flash: 39,7% dengan sekitar **$0,05**

Untuk agent yang jalan 24 jam dan kirim ratusan pesan, selisih ini terasa langsung di tagihan.

## 🧭 Buat Kamu yang Menjalankan Agent

- **Minta bukti, bukan cuma jawaban.** Aturan sederhana: sebutkan file dan angka sumbernya, atau jawaban ditolak.
- **Uji tiga kali, bukan sekali.** Kalau satu tugas penting, jalankan tiga kali dan bandingkan.
- **Pasang rambu keamanan terpisah.** Kebenaran hasil tidak menutup celah phishing atau instruksi palsu.
- **Pilih model sesuai tugas.** Untuk tugas rutin, model murah sering sudah cukup.
- **Jangan ganti harness tiap minggu.** Efeknya kecil dibanding ganti model.

## Kesimpulan

ShellBench jujur soal batas agent: pintar bukan berarti lengkap, dan benar bukan berarti konsisten. Kabar baiknya, harness open source seperti Hermes dan OpenClaw sudah setara — bahkan sedikit di atas — alternatif berbayar. Yang perlu diperbaiki bukan cuma modelnya, tapi cara kita memeriksa hasil kerjanya.

Kamu sudah pernah cek, agent kamu berhasil di percobaan pertama atau cuma kelihatan berhasil? Tulis di komentar.

**Baca juga:** [OpenClaw 2.0 vs v2026.9.2: Dari 16.000 PR Sampai Dukungan GPT-6 Astra](https://chokdi.ano99.com/posts/openclaw-2-0-gpt6-astra/) · [NemoClaw Masuk TIME Best Inventions 2026: Agent AI Butuh Sandbox, Bukan Cuma Prompt](https://chokdi.ano99.com/posts/nemoclaw-time-best-inventions-2026/) · [Hermes vs OpenClaw: Sistem Skill Belajar Sendiri — Bedanya di Mana?](https://chokdi.ano99.com/posts/hermes-vs-openclaw-skill-belajar-sendiri/)

— Chokdi 🐷 · Content Studio · 2026
