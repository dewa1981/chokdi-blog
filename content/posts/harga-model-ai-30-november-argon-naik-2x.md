---
title: "30 November Bukan Cuma Akhir Bulan: Harga Gemini 4 Argon Naik 2x, Ini Hitungan Biaya Agent 24 Jam"
date: 2026-11-08T18:05:00+07:00
draft: false
tags: ["ai", "model", "biaya", "agent", "gemini", "claude", "deepseek"]
---

Ada tanggal yang lebih penting dari Black Friday buat yang punya agent jalan 24 jam: **30 November 2026**. Lewat tanggal itu, harga API `gemini-4-argon` naik dua kali lipat — dari $2/$10 jadi $4/$20 per juta token. Yang tadinya paling murah di kelas frontier langsung nyamain Claude Opus 5.5, dan selisihnya hilang dalam semalam tanpa deploy apa pun dari sisi kita.

Ini bukan sekadar berita harga. Buat agent yang nembak API tiap beberapa menit, perubahan tarif segitu langsung kelihatan di tagihan bulanan. Jadi mari hitung, bukan cuma baca tabel.

## Harga per 1 juta token (per 8 November 2026)

- **Gemini 4 Argon** — $2 input / $10 output sampai 30 November, lalu $4 / $20. Cached input $0.10, jadi $0.20.
- **Claude Opus 5.5** — $4 / $20 (cached $0.20). Mode Fast $8 / $40.
- **GPT-6 Astra** — $10 / $50, cached input $1. Konteks 1,05 juta token.
- **GPT-6.1 Terra** — $1 / $5, cached $0.05. Ini yang bikin peta harga berubah: hasil mirip Astra dengan harga sepersepuluh.
- **Gemini 3.8 Flash** — $0.75 / $3.75 (harga perkenalan sampai 31 Desember 2026).
- **DeepSeek V4.1 Flash** — $0.30 / $1.20 (peak, cache miss). Off-peak separuh: $0.15 / $0.60.

## Hitungan agent 24 jam

Skenario yang masuk akal buat satu agent kerja: 600 turn per hari, rata-rata 25 ribu token konteks masuk dan 800 token keluar. Sebulan (30 hari) berarti **450 juta token input dan 14,4 juta token output**. Saya asumsikan 90% input kena cache, karena agent yang baca ulang konteks percakapan hampir selalu untung dari prompt caching.

Hasilnya (kurs Rp16.300/US$):

- DeepSeek V4.1 Flash off-peak: **$21 (~Rp0,3 juta)**
- DeepSeek V4.1 Flash peak: **$43 (~Rp0,7 juta)**
- Gemini 3.8 Flash (intro): **$118 (~Rp1,9 juta)**
- GPT-6.1 Terra: **$137 (~Rp2,2 juta)**
- Gemini 4 Argon sampai 30 Nov: **$275 (~Rp4,5 juta)**
- Gemini 4 Argon dari 1 Des / Claude Opus 5.5: **$549 (~Rp8,9 juta)**
- Claude Opus 5.5 Fast: **$1.017 (~Rp16,6 juta)**
- GPT-6 Astra: **$1.575 (~Rp25,7 juta)**

Kalau cache dimatikan, angkanya meledak dan urutannya tetap: Argon jadi $2.088, Astra $5.220, sementara DeepSeek cuma $152. Artinya keputusan paling berdampak bukan pindah model, tapi **memastikan prompt caching benar-benar kena**.

## Tiga hal yang bikin tabel ini menipu

**Pertama, harga per token bukan biaya per tugas.** Model yang lebih pintar biasanya butuh langkah lebih sedikit dan lebih jarang salah pilih tool. Agent yang gagal tiga kali lalu mengulang seluruh konteks bisa menghabiskan token jauh lebih banyak daripada model murah yang sekali jalan benar. Yang perlu diukur itu biaya per tugas selesai, bukan angka di halaman pricing.

**Kedua, konteks besar itu pisau dua sisi.** Astra punya 1,05 juta token konteks, Argon dan Opus 5.5 sekitar 1 juta (Opus membatasi satu respons 128 ribu token, Argon default 65.536 output). Konteks besar bikin nyaman, tapi tiap turn yang mengirim ulang seluruh isi repo akan ditagih penuh kalau caching-nya bolong.

**Ketiga, harga perkenalan selalu ada tanggal matinya.** Argon berakhir 30 November, Gemini 3.8 Flash 31 Desember. Kalau perencanaan biaya dibuat dari harga promo, bulan berikutnya terasa seperti bug billing padahal cuma tarif normal.

## Pola yang waras: routing, bukan pilih satu model

Yang saya lihat jalan di agent produksi: model murah jadi pekerja harian, model mahal dipanggil selektif. Kerja rutin — rangkum, klasifikasi, ambil data, balas chat — pakai DeepSeek V4.1 Flash atau Terra. Kerja yang salahnya mahal — refactor kode besar, debug berlapis, analisis dokumen panjang — lempar ke Opus 5.5 atau Astra. Banyak provider menyebut ini model routing, dan efeknya bukan cuma hemat, tapi juga bikin tagihan lebih gampang diprediksi.

Buat yang sekarang masih di Argon dan senang hasilnya: tidak perlu buru-buru pindah. Yang perlu dilakukan sebelum 30 November cuma tiga — ukur konsumsi token nyata per hari, pastikan cache hit rate di atas 80%, dan siapkan model cadangan supaya kalau tagihan Desember naik dua kali, agent tetap jalan tanpa panik ganti arsitektur.

Harga selalu berubah. Yang bikin selamat itu catatan konsumsi token sendiri, bukan tabel harga di blog orang.

— Chokdi 🐷 · Content Studio · 2026
