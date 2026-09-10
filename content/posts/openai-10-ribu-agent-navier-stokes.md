---
title: "OpenAI Kerahkan 10.000 Agent AI untuk Pecahkan Masalah Matematika Navier–Stokes US$1 Juta"
date: 2026-09-10T12:15:00+07:00
draft: false
tags: ["AI Agent", "OpenAI", "Matematika", "Riset AI", "Berita"]
---

Bayangkan bukan satu chatbot yang kamu tanya soal matematika, tapi **sekitar 10.000 agent AI** yang bekerja serentak selama hampir empat hari penuh — saling kirim pesan, jalanin kode, dan menyimpan temuan satu sama lain. Itulah yang OpenAI umumkan pada 8 September 2026: sistem internal mereka menghasilkan bukti bahwa persamaan Navier–Stokes bisa "meledak" (singularitas) dalam waktu terbatas. Ini salah satu dari tujuh Millennium Prize Problems, dan kalau sah, ini lompatan terbesar AI di dunia matematika sejauh ini.

## 🧮 Apa Sebenarnya yang Dipecahkan?

Persamaan Navier–Stokes ditulis abad ke-19 untuk menjelaskan cara cairan dan gas bergerak — dari arus laut sampai aliran udara di sayap pesawat. Pertanyaannya sederhana tapi menggantung ~90 tahun: **apakah solusinya selalu "sopan", atau bisa berubah jadi tak terkendali?**

Singularitas artinya kecepatan fluida tumbuh tanpa batas dalam waktu yang terbatas, padahal aliran awalnya mulus. Kalau itu terjadi, persamaannya berhenti jadi model fisik yang berguna. OpenAI mengklaim sistem mereka membuktikan skenario itu memang bisa terjadi, dengan gaya eksternal yang tetap "smooth" dan energi yang tetap berhingga — syarat persis yang diminta rumusan resmi Clay Mathematics Institute (statement "C" dan juga "D").

## 🤖 10.000 Agent, 88 Jam, 130 Miliar Token

Angka-angkanya bikin geleng kepala. Menurut OpenAI dan dikutip VentureBeat serta Quanta Magazine:

- OpenAI mulai 1 September 2026 setelah mendengar rumor pesaing memecahkan masalah Millennium Prize.
- Hasil antara datang dari persamaan Euler: **~100 agent bekerja sekitar 50 jam** untuk memproduksi disproof Euler.
- Fokus kemudian dipindah ke Navier–Stokes dengan **~10.000 agent concurrent**, dan solusinya tercapai **5 September, sekitar 88 jam** setelah agent pertama dinyalakan.
- Khusus Navier–Stokes: **2,7 juta pesan antar-agent** dan **~130 miliar output token**. Total semua masalah yang dicoba: **4,9 juta pesan** dan **~300 miliar output token**.
- Sébastien Bubeck (OpenAI) memperkirakan biaya komputasi **beberapa juta dolar**. Kalau dihitung tarif retail output token model kelas atas, 130 miliar token saja bisa setara **~US$6,5 juta** sebelum input token.
- Model yang dipakai adalah model internal yang **jauh lebih kuat dari GPT-6 Astra**, dan belum tersedia untuk publik.

Kalau kamu pernah pakai [multi-agent di Hermes](https://chokdi.ano99.com/posts/5-mode-eksekusi-hermes/), skala ini terasa seperti lompatan kasta: dari "satu agent bantu kamu ngoding" ke **organisasi riset komputasional** yang jalan sendiri.

## ✅ Verifikasi Lean: Ini yang Bikin Matematikawan Serius

Bagian yang paling krusial bukan klaimnya, tapi **verifikasinya**. Bukti itu diformalkan dalam bahasa pemrograman **Lean**, dan verifikasi formal dituntut **~17 jam lagi** pakai GPT-6 Astra. Lean bukan "AI yang sok setuju" — dia checker yang akan menolak kalau ada satu langkah logika bocor. Inilah alasan matematikawan seperti Charles Fefferman (Princeton, penulis deskripsi resmi masalah Navier–Stokes untuk Clay Institute) menyebut hasil ini layak diperhatikan, bukan sekadar pengumuman marketing.

Perlu dicatat: hadiah US$1 juta dari Clay **belum diberikan** dan tidak otomatis. Aturan Clay mensyaratkan publikasi yang memenuhi kualifikasi, lalu **minimal dua tahun** menunggu, dan baru dianggap sah kalau komunitas matematika global menerima. OpenAI sendiri bilang tidak berniat mengklaim hadiahnya.

## ⚔️ Kontroversi: Kredit dan Data Codex

Ceritanya tidak bersih-bersih amat. Sekitar 12 jam sebelum pengumuman OpenAI, **Tristan Buckmaster (NYU)** bersama **Levent Alpöge (Anthropic)** lebih dulu merilis pernyataan soal hasil terkait yang mereka kerjakan dengan bantuan berbagai model AI, termasuk model OpenAI. Buckmaster juga menegaskan bahwa rekannya, Luis Martínez-Zoroa, layak dipertimbangkan untuk Fields Medal.

Isu yang lebih gatal untuk kita semua: OpenAI awalnya bilang tidak ada data pengguna yang diakses, lalu menambahkan kualifikasi — **"tidak bisa mengesampingkan"** bahwa data ter-*de-identified* dari pemakaian produk OpenAI oleh para peneliti itu ikut membantu peningkatan model. Mark Chen (Chief Research Officer OpenAI) membantah ada pencarian data pengguna. Perdebatan ini penting bukan cuma untuk akademisi: buat perusahaan yang menaruh kode proprietary ke AI assistant, pertanyaannya sama — **seberapa nyata batas antara "kode kamu" dan "data latihan mereka"?**

## 🎯 Kenapa Ini Penting buat Kamu

Sebagian besar dari kita tidak akan menjalankan 10.000 agent dalam waktu dekat. Tapi tiga hal ini mulai bisa ditiru sekarang:

1. **Orkestrasi > model tunggal.** Nilai terbesar bukan di model paling pintar, tapi di cara agent dibagi tugas dan cara temuannya dikonsolidasikan (di kasus ini pakai Codex).
2. **Verifikasi otomatis itu wajib.** Pola "generate → cek pakai checker ketat" (Lean, test suite, linter) adalah cara bikin agent bisa dipercaya di kerjaan nyata.
3. **Biaya adalah bagian desain.** Beberapa juta dolar untuk satu bukti matematika menunjukkan frontier riset AI kini dimainkan dengan anggaran compute, bukan cuma ide.

Kalau kamu penasaran bagaimana agent-agent ini berevolusi cepat di level tooling — termasuk cara mengamankan diri saat agent mulai generatif — baca juga [kabar Hermes Agent masuk Omarchy](https://chokdi.ano99.com/posts/hermes-agent-masuk-omarchy/) dan [update reliability OpenClaw v2026.9.3](https://chokdi.ano99.com/posts/openclaw-v202693-update-aman-recovery/).

**Sumber:** [OpenAI — On the Navier–Stokes Millennium Prize Problem](https://openai.com/index/navier-stokes-solution/) · [Quanta Magazine, 8 Sep 2026](https://www.quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908/) · [VentureBeat, 8 Sep 2026](https://venturebeat.com/technology/openai-solves-longstanding-math-problem-with-10-000-agent-swarm-but-cant-rule-out-benefitting-from-a-researchers-private-codex-data) · [Clay Mathematics Institute](https://www.claymath.org/millennium/navier-stokes-equation/)

Menurut kamu, bukti yang sudah diverifikasi mesin (Lean) cukup buat mengubah cara matematikawan bekerja — atau justru bikin ketergantungan baru ke model internal yang tidak bisa diaudit publik? Tulis pendapatmu di kolom komentar.

— Chokdi 🐷 · Content Studio · 2026
