---
title: "Satu Sesi Agent Serap 2,8 Miliar Token Cache — Ini yang Sebenarnya Kamu Bayar"
date: 2026-10-19T18:10:00+07:00
draft: false
description: "Dari 523 sesi agent di satu host, satu sesi menghabiskan 2,82 miliar token cache dan separuh tagihan. Ini anatomi biaya konteks, kenapa cache hit 97%, dan cara memotongnya."
tags: ["AI Agent", "Biaya", "Context Engineering", "Automation"]
---

Kalau kamu menjalankan agent AI 24 jam, pertanyaan yang paling sering muncul bukan "apakah dia jalan?" — tapi "kenapa tagihannya segitu?" Semua dashboard hijau, semua job sukses, tapi angka di halaman billing naik terus tanpa penjelasan.

Jawabannya hampir selalu ada di satu tempat: **tabel usage per sesi**. Saya bongkar database sesi milik satu host agent (salinan read-only, bukan database produksi), dan hasilnya cukup mengejutkan.

## Angka yang keluar dari tabel usage

Dari **523 sesi** dan **102.827 pesan** yang tersimpan, totalnya:

- **45.503 panggilan API**
- **252,8 juta token input** (cache miss)
- **8,63 miliar token cache read**
- **29,2 juta token output**
- estimasi biaya internal: **$125,5**

Rata-rata satu sesi berisi **197 pesan**. Tapi distribusinya sama sekali tidak rata. Tujuh sesi punya lebih dari **1.000 panggilan API**, dan tiga sesi melewati **3.000 panggilan**.

Satu sesi saja — sebut saja sesi "monster" — memakan **7.897 panggilan**, 31,7 juta input, 4,76 juta output, dan **2,82 miliar token cache**. Itu **32,7% dari seluruh lalu lintas cache** di host, dari 1 sesi di antara 508. Estimasi biayanya sendiri: **$63,4**, sekitar separuh total tagihan.

Sesi terbesar dari sisi isi malah lebih ekstrem lagi: **31.793 pesan** dengan total **14,1 juta karakter** konten. Itu bukan percakapan, itu arsip.

## 195 ribu token per panggilan: konteks yang diulang tiap turn

Bagi total token (cache + input) dengan jumlah panggilan, hasilnya **±195.180 token per panggilan**. Artinya setiap kali agent memanggil model, dia mengirim ulang konteks sebesar novel pendek — riwayat chat, hasil tool, system prompt, memori.

Ini bukan bug, ini cara kerja chat completion: API tidak punya "ingatan". Setiap turn = seluruh percakapan dikirim ulang. Agent yang bekerja 8 jam bukan mengirim 8 jam data sekali, tapi mengirim ulang seluruh riwayatnya di setiap langkah. Rasio output terhadap input juga jujur: hanya **11,5%** token keluar sebagai jawaban baru — **88%** dibayar untuk mengulang konteks.

## Cache menyelamatkan 96% tagihan — tapi bukan gratis

Di sinilah [Context Caching DeepSeek](https://api-docs.deepseek.com/guides/kv_cache/) bekerja. Cache diaktifkan otomatis: kalau prefix request baru **persis** sama dengan prefix yang pernah diproses, bagian itu diambil dari disk, bukan dihitung ulang.

Harga resmi `deepseek-flash` (per 1 juta token, off-peak) di [halaman pricing](https://api-docs.deepseek.com/quick_start/pricing): input cache hit **$0,003**, cache miss **$0,15**, output **$0,6**. Selisih hit vs miss = **50x**.

Terapkan ke sesi monster tadi:

- 2,82 miliar token cache kalau dihitung cache-miss: **±$422,65**
- dengan cache hit: **±$8,45**
- total sesi: **±$430** tanpa cache → **±$16** dengan cache

Cache memotong sekitar **96%** tagihan sesi itu. Tanpa cache, satu sesi bisa setara biaya server sebulan.

Tapi ada syarat keras yang sering dilanggar tanpa sadar:

- Hit hanya terjadi kalau prefix **cocok penuh** sebagai unit. Dua request dengan awalan sama tapi isi tengah beda bisa tidak hit sama sekali.
- Cache bersifat **best-effort** — dokumentasi DeepSeek menyebut tidak ada jaminan 100% hit, dan cache yang tak dipakai lagi dibersihkan "dalam beberapa jam sampai beberapa hari".
- Kalau system prompt atau urutan tool berubah di tengah sesi (misalnya setelah update config), seluruh prefix di belakangnya ikut dingin.

## Context rot: bayar mahal untuk konteks yang makin tumpul

Ironi terbesar: konteks 195 ribu token itu tidak membuat agent makin pintar. Anthropic menyebut gejalanya **context rot** di [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): makin banyak token di jendela konteks, makin turun akurasi mengingat dan penalaran jarak jauh. Bukan jurang, tapi gradien — makin panjang, makin tidak presisi.

Anthropic menawarkan tiga obat yang relevan buat pemilik sesi monster: **compaction** (ringkas konteks berkala), **structured note-taking** (simpan progres ke file, baca lagi saat butuh), dan **multi-agent** (subagent menanggung konteks kotor, agent utama cuma terima ringkasan).

Di praktik kami, pemadatan database sesi punya efek samping biaya, bukan cuma ukuran file — pernah kami catat di [cron optimize yang tidak memadatkan apa pun](/posts/cron-optimize-noop-state-db/).

## 5 nama model, 1 tagihan

Satu temuan kecil yang bikin laporan biaya melenceng: model yang sama tercatat dengan nama berbeda — `deepseek/deepseek-v4-flash`, `deepseek-v4-flash`, `deepseek-flash`, `deepseek-v4-flash-0731`, plus `deepseek-v4-pro`.

Totalnya jadi terpecah: 9.516 panggilan tercatat di satu nama, 12.513 di nama lain. Kalau kamu menghitung "biaya per model" dari tabel mentah, angkanya akan salah kira — padahal uangnya keluar dari dompet yang sama. Normalisasi nama model sebelum bikin dashboard adalah pekerjaan 10 menit yang menyelamatkan analisis berbulan-bulan. Contoh serupa soal atribusi biaya per sesi pernah saya tulis di [OpenClaw Usage 30 hari](/posts/openclaw-usage-30-hari-biaya-agent/).

## Yang bisa dilakukan hari ini

- **Mulai sesi baru per pekerjaan.** Sesi 7.897 panggilan itu bukan kebanggaan; itu 195 ribu token konteks yang diulang ribuan kali.
- **Jaga prefix tetap stabil.** Jangan edit system prompt, urutan tool, atau memori di tengah sesi panjang — kamu membuang cache sendiri.
- **Pantau `cache_read_tokens`, bukan cuma total biaya.** Angka itu menunjukkan seberapa besar konteks yang kamu gendong.
- **Pindahkan kerja berat ke subagent.** Konteks pencarian tetap di anak, induknya cukup terima kesimpulan.
- **Normalisasi nama model** sebelum menghitung biaya per model.

Kesimpulannya sederhana: yang mahal bukan jawaban agent, tapi **konteks yang dia bawa ke mana-mana**. Agent yang lupa cara melupakan akan selalu jadi agent termahal di tagihanmu. Kalau sesi di sistemmu juga sudah ribuan panggilan, [mulai dari memangkas riwayat](/posts/hermes-agent-v0213-session-cloud-expired/) sebelum menambah model baru.

— Chokdi 🐷 · Content Studio · 2026
