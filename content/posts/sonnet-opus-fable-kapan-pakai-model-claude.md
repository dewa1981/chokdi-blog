---
title: "Sonnet, Opus, atau Fable: Kapan Pakai Model Claude yang Mana (Harga Resmi November 2026)"
date: 2026-11-16T12:10:00+07:00
draft: false
tags: ["AI", "Claude", "Biaya", "Tutorial"]
---

Ada tiga keluarga model Claude yang aktif sekarang: **Sonnet, Opus, dan Fable**. Hampir semua orang salah pilih di salah satu arah — pakai Opus untuk kerja sepele (boncos), atau pakai Sonnet untuk keputusan besar (dapat jawaban cepat tapi dangkal). Artikel ini isinya harga resmi terbaru plus aturan praktis kapan pakai yang mana, jadi kamu tidak perlu menebak lagi.

## Harga resmi per November 2026

Angka di bawah ini dari halaman pricing Anthropic (platform.claude.com), satuan **USD per 1 juta token (MTok)**:

| Model | Input | Output | Catatan |
|---|---|---|---|
| Haiku 5.5 | $0,10 | $0,50 | untuk prompt ≤100 ribu token; di atas itu $0,50 / $2,50 |
| Sonnet 5.5 | $2 | $10 | harga sama dengan Sonnet 5, tapi lebih hemat token per tugas |
| Opus 5.5 | $4 | $20 | turun 20% dari Opus 5 yang masih $5 / $25 |
| Fable 5.2 | $8 | $40 | paling mahal, paling kuat untuk kerja agent jangka panjang |
| Fable 5.1 | $10 | $50 | generasi sebelumnya, masih dilayani |

Dua hal yang sering kelewat:

1. **Output selalu 5x harga input.** Jadi percakapan panjang dengan jawaban panjang lebih mahal daripada prompt besar dengan jawaban pendek.
2. **Tokenizer model 4.7 ke atas menghasilkan sekitar 30% token lebih banyak** untuk teks yang sama. Artinya harga per token bisa turun, tapi tagihan belum tentu turun — yang penting adalah biaya per tugas selesai, bukan angka di rate card.

Untuk kerja asinkron yang tidak buru-buru, **Batch API memotong harga 50%**. Untuk konteks yang diulang-ulang (system prompt besar, dokumen panjang), **prompt caching** bikin baca cache cuma 0,025x–0,1x harga input, tergantung model.

## Analogi tiga level: tugas, masalah, tujuan

Cara paling gampang mengingat perbedaan ketiganya bukan dari benchmark, tapi dari **apa yang kamu serahkan ke model**:

- **Sonnet → kasih tugas.** "Bikin 5 varian headline", "refactor fungsi ini", "ringkas 20 halaman ini". Instruksi jelas, hasil bisa dicek cepat.
- **Opus → kasih masalah.** "Kenapa build ini gagal padahal log bersih?", "Arsitektur mana yang tahan 10x trafik?". Opus lebih lambat karena berpikir lebih panjang, dan justru itu yang dibayar.
- **Fable → kasih tujuan.** "Naikkan konversi landing page 20% dalam 2 minggu." Fable yang menyusun rencananya sendiri: apa yang diukur, langkah mana dulu, kapan berhenti.

Analogi ini sempat viral di komunitas Claude Code dengan istilah *senior hire* untuk Opus dan *konsultan luar* untuk Fable. Bukan istilah resmi Anthropic, tapi cukup akurat untuk dipakai sebagai pegangan.

## Aturan praktis per jenis kerja

**Pakai Sonnet 5.5 kalau:**
- Produksi konten harian: caption, artikel, deskripsi produk, balasan CS.
- Koding rutin yang polanya sudah jelas: CRUD, komponen UI, migrasi kecil.
- Klasifikasi dan ekstraksi data dalam jumlah banyak.
- Jadi **default** untuk hampir semua pekerjaan. Naik level hanya kalau Sonnet terbukti gagal di tugas itu, bukan karena takut hasilnya kurang.

**Pakai Opus 5.5 kalau:**
- Sedang debug masalah yang tidak ketemu akarnya setelah 2–3 percobaan.
- Butuh keputusan arsitektur, audit keamanan, atau review kode yang menyentuh uang/data.
- Tugas multi-langkah panjang: agent yang harus mempertahankan konteks belasan langkah.
- Hitungan kasarnya: Opus 2x harga Sonnet per token, tapi kalau dia selesai dalam 1 percobaan sementara Sonnet butuh 3, Opus justru lebih murah.

**Pakai Fable 5.2 kalau:**
- Kamu menyerahkan **tujuan**, bukan instruksi — misalnya riset kompetitor end-to-end, atau membangun fitur dari brief satu paragraf.
- Pekerjaan agent jangka panjang (berjam-jam, banyak tool call) yang kalau salah arah biayanya jauh lebih besar daripada selisih harga token.
- Kamu sudah punya cara mengukur hasil. Tanpa evaluasi, Fable hanya jadi cara mahal untuk merasa produktif.

**Pakai Haiku 5.5 kalau:** routing, klasifikasi, ekstraksi field, moderasi, atau apa pun yang dipanggil ribuan kali sehari dengan jawaban pendek. Di harga $0,10 input, ini satu-satunya tier yang masuk akal untuk volume besar.

## Tiga jebakan yang bikin tagihan membengkak

**1. Menghitung harga per token, bukan per tugas.** Fable yang selesai 1x bisa lebih murah dari Sonnet yang iterasi 6x. Sebaliknya, Fable untuk rename variabel jelas pemborosan. Ukur dulu, baru pindah tier.

**2. Lupa fast mode.** Opus 5.5 punya fast mode yang harganya **2x lipat** ($8 / $40). Enak untuk kerja interaktif yang butuh jawaban cepat, mahal untuk kerja batch yang bisa ditinggal tidur.

**3. Menyimpan model lama di kode.** Opus 4.8 dan Opus 5 masih $5 / $25 — 25% lebih mahal daripada Opus 5.5 yang lebih baru dan lebih kuat. Kalau ada ID model lama nyangkut di config, itu ongkos yang dibayar tanpa dapat manfaat.

## Contoh routing untuk kerja nyata

Ini yang kami pakai sendiri di Content Studio Chokdi, dan hasilnya cukup jelas:

- **Banner dan aset gambar** → model image, bukan Claude. Tidak ada alasan membakar token teks untuk ini.
- **Draft artikel dan copy** → Sonnet. 80% selesai di sini.
- **Audit kode dan pipeline** → Opus. Bayar 2x untuk menghindari satu bug produksi yang biayanya 100x.
- **Riset pasar dan rencana konten bulanan** → Fable, karena yang diserahkan memang tujuan, bukan tugas.
- **Cek judul, tag, dan klasifikasi kategori** → Haiku, karena volumenya besar dan jawabannya pendek.

Kalau kamu memakai Hermes Agent, routing ini bisa diatur per cron job dan per panggilan — lihat cara kami menangani katalog plugin yang gagal senyap di [artikel plugin catalog 2 MB](/posts/hermes-agent-v0231-plugin-catalog-2mb-gagal-senyap/) dan pembaruan terbaru di [Hermes v0.23.0](/posts/hermes-agent-v0230-hearth-desktop-di-browser/).

## Kesimpulan

Urutan yang aman: **mulai dari Sonnet, naik ke Opus saat macet, pindah ke Fable saat yang kamu punya cuma tujuan.** Haiku untuk volume, bukan untuk berpikir.

Dan kalau kamu memakai langganan Claude Pro atau Max, ingat: kuota langganan dan tarif API itu dua dunia berbeda. Langganan mengatur pemakaian di aplikasi resmi; API menagih per token. Mencampur keduanya adalah sumber kejutan tagihan paling umum.

Kamu sendiri paling sering pakai tier yang mana? Kalau ada tugas yang hasilnya mengecewakan di Sonnet, tulis di komentar — biasanya itu sinyal paling jujur bahwa saatnya naik ke Opus.

— Chokdi 🐷 · Content Studio · 2026
