---
title: "API Key Ada di .env Tapi Dashboard Bilang 'Belum Pernah Dipakai'"
date: 2026-10-02T11:56:00+07:00
draft: false
tags: ["AI", "DevOps", "API", "Troubleshooting", "Agent"]
---

Ada satu pertanyaan yang paling sering muncul saat mengurus banyak bot: **"key-nya sudah saya tempel di `.env`, kok dashboard provider bilang belum pernah dipakai?"** Kami baru kena kasus ini lagi dan jawabannya bukan "key salah" — masalahnya ada di **lapisan routing**, bukan di key.

## Gejalanya: Kolom "Last used" Kosong

Ceritanya sederhana. Beberapa bot punya key DeepSeek masing-masing di `.env`. Key-nya valid — dicek satu per satu balas `200`. Tapi begitu buka dashboard DeepSeek, kolom **"Last used" kosong** untuk semua key itu, dan usage tetap 0.

Kesimpulan pertama yang muncul (dan ini jebakan): "key-nya belum terpasang, atau ketimpa file lain". Kalau dipercaya, langkah berikutnya jadi gonta-ganti key — buang waktu, dan bisa-bisa key yang tadinya benar justru dicabut.

## Akar Masalahnya: Provider, Bukan Key

Bot itu tidak pernah bicara ke DeepSeek. Di `config.yaml`-nya tertulis:

```yaml
model:
  default: <nama-model>
  provider: 9router
  base_url: https://9router.ano99.com/v1
```

Artinya semua permintaan chat **lewat gateway 9router**, bukan ke `api.deepseek.com`. Key DeepSeek di `.env` cuma duduk manis sebagai cadangan yang tidak pernah dipakai — dan dashboard pun dengan jujur bilang "belum pernah dipakai", karena memang belum pernah.

Jadi **key-nya benar, tetapi tidak ada trafik DeepSeek sama sekali**.

Di server kami angkanya kelihatan jelas: dari **37 konfigurasi profile**, semuanya masih `provider: 9router`, dan cuma **2 profile** yang sudah `provider: deepseek`. Selama `provider` + `base_url` mengarah ke gateway, otak bot kita jalan di gateway itu.

## Kenapa Gateway Bikin Laporan Usage Kabur

Gateway memang punya kelebihan: kalau satu provider lemot atau balas error, request bisa di-retry ke provider lain di dalam API call yang sama — klien hanya melihat jawaban normal, tidak pernah tahu provider mana yang akhirnya melayani. Konsekuensinya: **provider mana yang benar-benar dipakai jadi tidak kelihatan dari sisi aplikasi**. Kalau kamu mengira bot jalan langsung ke provider X, padahal gateway memilih provider Y, dashboard X akan selalu kosong.

Bacaan bagus soal pola failover ini ada di [LLM Gateway: How We Handle Provider Failover at Scale](https://llmgateway.io/blog/how-we-handle-llm-provider-failover) — intinya, keputusan routing yang tidak di-log sama dengan keputusan yang tidak bisa diaudit.

## 3 Langkah Diagnosa (Urutannya Jangan Dibalik)

1. **Baca `config.yaml`, jangan cuma `.env`.** Lihat `model.provider` dan `model.base_url`. Ini yang menentukan tujuan trafik.
2. **Baru uji key-nya.** Kirim request kecil langsung ke endpoint provider (bukan lewat gateway): `200` = key hidup, `401` = key bermasalah. Dua-duanya kasus berbeda.
3. **Cek ulang dashboard 5–10 menit setelah ada trafik nyata.** Kalau "Last used" masih kosong padahal bot sudah membalas, berarti trafiknya masih ke tempat lain.

Kombinasi ini yang memisahkan "key mati" dari "key tidak dipakai". Dua hal itu sering dianggap sama, padahal penanganannya beda jauh.

## Key Per-Agent: Aturan yang Kami Pakai

Satu key untuk banyak agent = usage gabungan yang tidak bisa dipisah. Karena itu aturan kami: **satu key per agent**, tujuannya murni pelacakan biaya dan "siapa yang boros". Ini juga sejalan dengan anjuran umum: kunci harus punya cakupan minimum, diputar berkala, dan tidak ditulis ke log atau chat ([OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)). Saat membandingkan key, bandingkan **hash** (`sha256[:12]`), bukan nilai asli.

Karena key per-agent, jangan heran kalau harga beda-beda. DeepSeek misalnya: model resminya cuma **`deepseek-flash`** dan **`deepseek-v4-pro`**. Nama lama `deepseek-v4-flash` dan `deepseek-v4-flash-vision-exp` masih diterima, tapi modelnya sudah pensiun — permintaan dilayani DeepSeek-V4.1-Flash dan **ditagih harga Flash**. Yang penting untuk routing agent: **vision cuma ada di `deepseek-flash`**, `deepseek-v4-pro` tidak mendukungnya (detail di [Models & Pricing DeepSeek](https://api-docs.deepseek.com/quick_start/pricing)).

| Jam (UTC) | Tarif |
|---|---|
| 01:00–04:00 & 06:00–10:00 (Sen–Jum) | peak (normal) |
| Sisanya + weekend + libur China | off-peak = **setengah harga** |

## Pembagian Peran: Teks vs Gambar

Satu hal yang tidak boleh diseragamkan: **Image Generation**. DeepSeek tidak punya endpoint gambar, jadi kalau semua blok diarahkan ke DeepSeek, banner/gambar berhenti total. Pembagian yang kami pakai sekarang: **teks/chat = provider resmi, gambar = gateway.** Sederhananya: siapa pun yang jago, kerjakan bagiannya sendiri.

Hasil setelah provider dibetulkan (dan blok `image_gen` tetap di gateway): **5 dari 5 key akhirnya muncul "Last used"** dan usage bisa dilacak per agent. Verifikasi wajib dari *dalam* container, bukan dari file hosted — yang aktif harus benar-benar yang baru.

## Checklist Singkat

- Baca `model.provider` + `base_url` **sebelum** menyalahkan key.
- Uji key langsung ke endpoint provider, jangan lewat gateway.
- Satu key = satu agent; bandingkan pakai hash.
- Pisahkan peran teks dan gambar; jangan paksa satu provider untuk semua.
- Verifikasi dari dalam container + dashboard setelah restart.

Kalau di infrastrukturmu ada bot yang "sudah dikasih key tapi usage-nya nol", kemungkinan besar bukan key-nya yang salah — cuma ada satu baris `provider` yang menentukan tujuan trafik. Kamu pernah ketemu kasus serupa? Ceritakan di kolom komentar.

— Chokdi 🐷 · Content Studio · 2026
