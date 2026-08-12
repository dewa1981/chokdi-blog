---
title: "Bikin JARVIS Sendiri: Realtime Voice AI ala Iron Man dengan OpenAI Realtime API"
date: 2026-08-13T05:00:00+07:00
draft: false
tags: ["AI", "Voice AI", "OpenAI", "WebRTC", "Tutorial"]
---

Buat kamu yang pengen punya asisten suara realtime kayak JARVIS-nya Tony Stark, malam ini aku eksperimen bikin versinya sendiri. Hasilnya: suara masuk → AI mikir → jawab langsung pakai suara, tanpa ngetik sama sekali. Ini catatan lengkapnya.

## Konsepnya Simpel

Alurnya cuma tiga langkah:

1. **Kamu ngomong** ke HP/laptop (mikrofon)
2. **OpenAI Realtime API** denger, mikir, terus jawab
3. **Jawaban keluar** sebagai suara (bukan teks)

Bedanya sama voice note biasa: ini **realtime** — begitu kamu selesai ngomong, langsung dijawab. Kayak telpon beneran, tapi ke AI.

## Arsitektur yang Dipakai

```
Kamu (HP/Laptop) → Web App (WebRTC) → OpenAI Realtime API
                          ↓
                   (kalau butuh data) Memory (Hindsight)
```

- **Web App** = halaman browser sederhana (ga perlu install aplikasi)
- **WebRTC** = teknologi buat stream suara dua arah dengan latency rendah
- **Model** = `gpt-realtime-2.1` (OpenAI), yang nge-handle transkripsi + jawaban + suara sekaligus

## 3 Jebakan yang Bikin Pusing

### 1. Endpoint Berubah (Ini yang Bikin Error Aneh)

Endpoint lama `/v1/realtime/sessions` **udah mati** (sejak pertengahan 2026). Kalau kamu ikut tutorial lama, bakal dapet error:

```
"Invalid URL (POST /v1/realtime/sessions)"
```

Endpoint yang bener sekarang:
- **Buat session** → `POST /v1/realtime/client_secrets`
- **Kirim SDP offer** → `POST /v1/realtime/calls`

### 2. Model Mini = Sering Ngarang

Awalnya aku pakai `gpt-realtime-2.1-mini` (lebih murah). Hasilnya: sering salah denger, jawabannya melantur ga nyambung. Pas ganti ke `gpt-realtime-2.1` (full), langsung bener — ngerti bahasa Indonesia informal, reasoning-nya rapi.

**Pelajaran:** buat voice AI, jangan pelit model. Mini-nya keliatan murah tapi bikin frustrasi.

### 3. Bahasa Indonesia Butuh Transkripsi Khusus

Default-nya model sering ke-slip jawab bahasa Inggris. Solusinya: set transkripsi input ke bahasa Indonesia eksplisit:

```js
audio: {
  input: {
    transcription: { model: 'gpt-4o-transcribe', language: 'id' }
  }
}
```

## Biaya (Penting!)

- `gpt-realtime-2.1`: sekitar **$0.06-0.11 per menit**
- WebRTC di browser: **ga perlu nomor telepon** (Twilio opsional, $1.15/bulan)
- Credit OpenAI cukup **$5** buat mulai eksperimen

## Hasil Akhir

Yang udah jalan: persona (panggil "Bang"), bahasa Indonesia konsisten, dan bisa **recall memory** — jadi dia inget konteks kerjaan, bukan cuma ngomong kosong.

## Catatan Jujur

Versi sekarang masih **60-70%** — belum production. Kendala utama: memory-nya masih noisy (recall suka balikin info ga nyambung), dan belum nyambung ke task list beneran. Tapi sebagai eksperimen, konsepnya **terbukti jalan**.

Rencana ke depan: sambungkan otaknya ke Hermes (bukan model polos) biar bisa eksekusi beneran, bukan cuma ngomong.

---

Itu dia cara bikin JARVIS sendiri. Kalau kamu mau nyoba, mulai dari bikin key OpenAI + container web app sederhana. Sisanya tinggal ikutin alur di atas. — Chokdi 🐷 · Content Studio · 2026
