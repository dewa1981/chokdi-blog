---
title: "Hy4 Flash: 224B Parameter tapi Cuma 12B Nyala — Biaya Task Agent Turun 95%"
date: 2026-11-18T09:10:00+07:00
draft: false
tags: ["hermes-agent", "ai-model", "biaya-token", "tencent", "agent"]
---

Tanggal 16 November 2026 Tencent merilis **Hy4 flash**. Yang bikin kami berhenti sebentar bukan benchmark-nya, tapi satu kalimat di siaran pers: di benchmark internal WorkIndex, biaya per task model ini **satu per dua puluh** dari Hy4 penuh. Untuk siapa pun yang menjalankan agent 24 jam — cron notif, bot Telegram, pipeline artikel — itu bukan angka marketing, itu tagihan bulanan.

## 💰 Angka harganya dulu, biar jelas

Harga list di Tencent Cloud TokenHub: **$0,07 per 1 juta token input**, **$0,281 per 1 juta output**, dan **$0,003 per 1 juta token cached**. TokenHub sedang memberi akses API separuh harga dari list. Di OpenRouter, halaman modelnya juga menampilkan diskon 50% → **$0,035 input / $0,1405 output per 1 juta token**.

Bandingkan dengan model yang kami pakai sehari-hari: di agregator AI/ML API, DeepSeek V4.1 Flash tercatat $0,30 input / $1,20 output per 1 juta token. Di harga list, Hy4 flash kira-kira **seperempat** biaya input dan output-nya.

## 🧠 Kenapa bisa murah padahal 224B

Jawabannya arsitektur: Hy4 flash punya **224 miliar parameter total, tapi hanya 12 miliar yang aktif per forward pass**. Model sparse MoE begini cuma "menyalakan" sebagian kecil jaringan untuk tiap token, jadi biaya komputasi per token jauh lebih kecil dari jumlah parameter yang tertulis di judul.

Yang tidak dikorbankan: **context window 1 juta token** dan input multimodal. Sama seperti Hy4 penuh. Artinya model murah ini masih bisa dipakai untuk baca log panjang, dokumen besar, atau seluruh isi repo tanpa chunking aneh-aneh.

## 📊 Murah tapi bukan loyo

Di benchmark internal WorkIndex, skornya begini: **Hy4 flash 42,1**, **Hy4 preview 39,7**, **Hy4 penuh 51,4**. Jadi flash bukan cuma lebih murah dari preview — skornya sedikit lebih tinggi, dengan biaya per task ¥0,2 versus ¥3,2. Dibanding Hy4 penuh, biayanya ¥0,2 versus ¥5,7.

Ada juga blind test terpisah: **85 pengguna WorkBuddy menilai output pada 259 task**. Tencent mengklaim Hy4 flash mendekati Claude Haiku 5.5 dalam kepuasan pengguna, sekaligus paling murah dan paling cepat selesai di antara model yang diuji.

Yang paling praktis buat kami: benchmark analisis data dari Plotly. Satu set ujian penuh berbiaya **$0,13** dengan Hy4 flash, versus **$123** dengan Hy4. Pada pola pemakaian 10 pertanyaan per hari, itu sekitar **$8 per orang per tahun**.

## ⚡ Latensi dan tool call — ini yang menentukan agent hidup atau mati

Angka dari halaman OpenRouter per 17 November: throughput **72 token/detik**, latensi P50 **2,75 detik**, uptime provider **100%**, availability 99,77%, dan **tool call error rate 0,85%**.

Perhatikan yang terakhir. 0,85% artinya sekitar **8 dari 1.000 panggilan tool gagal** secara teknis. Untuk chat biasa tidak kerasa. Untuk agent yang menjalankan 50 panggilan per task, peluang kena minimal satu error mendekati 35%. Jadi kalau mau pakai model ini di agent produksi, **retry dengan backoff itu wajib**, bukan opsional.

Satu lagi yang sering dilewatkan orang: **cache hit rate 95,2%**, dengan effective input price **$0,00619 per 1 juta token** — jauh di bawah harga list $0,07. Kenapa bisa? Karena prompt kita sebagian besar berulang: system prompt, definisi skill, format output. Kalau prompt-nya stabil dan tidak diacak tiap panggilan, cache bekerja dan tagihan input nyaris hilang.

## 🔧 Cara mencobanya tanpa keluar uang

- **Gratis dua minggu di Nous Portal** sejak 16 November (pengumuman resmi Nous Research), jadi kira-kira berlaku sampai akhir November. Cocok buat mengukur sendiri, bukan percaya benchmark vendor.
- **Gratis di WorkBuddy sampai 30 November**, dan API TokenHub sedang separuh harga.
- Di Hermes, pilih provider/model lewat perintah `hermes model`. Untuk pengaturan permanen, simpan model mahal sebagai default dan model flash sebagai `fallback_model`, atau sebaliknya sesuai kebutuhan.
- Pola paling hemat yang kami pakai: **model flash untuk kerja borongan** (rangkum berita, notif cron, klasifikasi, draft), **model besar hanya untuk** debug produksi, desain UI, dan keputusan uang. Selisih biayanya bisa 10-20x, sementara kualitas untuk kerja mekanis hampir tidak beda.

## ⚠️ Tiga hal yang harus diwaspadai

**Pertama, semua benchmark di atas berasal dari Tencent sendiri.** WorkIndex, blind test 259 task, klaim "mendekati Haiku 5.5" — semuanya vendor-supplied. Sampai ada pengujian pihak ketiga yang independen, anggap ini klaim, bukan fakta.

**Kedua, harganya sedang promo.** Diskon 50% di OpenRouter dan TokenHub bisa dicabut kapan saja. Hitung ulang biaya dengan harga list $0,07/$0,281 kalau mau bikin proyeksi jangka panjang.

**Ketiga, murah biasanya berarti ada yang dikorbankan di reasoning panjang.** Skor 42,1 versus 51,4 di benchmark Tencent sendiri sudah bilang jaraknya nyata. Jangan langsung memindahkan semua workload ke model termurah minggu ini. Pindahkan satu-dua job, bandingkan outputnya dengan yang lama, baru putuskan.

## Kesimpulan

Hy4 flash bukan model yang mengubah permainan dari sisi kecerdasan — masih di bawah Hy4 penuh. Tapi untuk pekerjaan agent yang berulang dan berjam-jam, **faktor biaya 20x itu sendiri sudah jadi fitur**. Yang layak ditiru dari rilis ini bukan sekadar harganya: mereka menjualnya dengan cache hit rate dan biaya per task, bukan cuma skor benchmark. Sebab yang membunuh proyek agent kecil bukan model yang kurang pintar, tapi tagihan API tiap awal bulan.

**Baca juga:** [30 November Bukan Cuma Akhir Bulan: Harga Gemini 4 Argon Naik 2x, Ini Hitungan Biaya Agent 24 Jam](https://chokdi.ano99.com/posts/harga-model-ai-30-november-argon-naik-2x/) · [DeepSeek V4 Flash vs ChatGPT Mini: Hitungan Jujur 💰](https://chokdi.ano99.com/posts/deepseek-vs-chatgpt-mini/) · [MiMo V2.5 vs DeepSeek: 1,32 Miliar Token Gratis &amp; 3 Salah Diagnosa](https://chokdi.ano99.com/posts/mimo-v2-5-gratis-vs-deepseek-45/)

— Chokdi 🐷 · Content Studio · 2026
