---
title: "Cara Connect Hermes Agent ke LINE: Jadikan LINE Asisten AI di Saku Kamu"
date: 2026-08-21T16:30:00+07:00
draft: false
tags: ["Hermes Agent", "LINE", "Tutorial", "AI Assistant", "Messaging"]
---

# Cara Connect Hermes Agent ke LINE: Jadikan LINE Asisten AI di Saku Kamu

LINE bukan cuma buat chat sama temen. Dengan Hermes Agent, LINE bisa jadi **asisten AI pribadi yang selalu ada di saku kamu** — tanya apa aja, kapan aja, langsung dijawab, bahkan bisa kirim gambar hasil generate. Artikel ini panduan lengkap connect Hermes Agent ke LINE Messaging API, langkah demi langkah, dari nol sampai test di HP.

## Kenapa LINE?

LINE adalah aplikasi pesan paling dominan di Jepang, Taiwan, dan Thailand. Kalau target pengguna kamu di sana, LINE adalah jalur paling natural untuk mereka menghubungi AI. Hermes Agent — framework AI agent open-source dari Nous Research — sudah punya dukungan resmi LINE via bundled plugin `plugins/platforms/line/`. Artinya: **tanpa install tambahan apa pun**, tinggal enable dan isi kredensial.

Yang bikin beda dari sekadar chatbot biasa: Hermes Agent punya **memori jangka panjang, skill yang bisa dibuat dari obrolan, dan kemampuan menjalankan tool** — cari di internet, generate gambar, catat todo, semua dari dalam LINE.

## Step 1: Buat Channel di LINE Developers

1. Buka **LINE Developers Console** di developers.line.biz, login pakai akun LINE kamu.
2. Klik **Create Provider** — ini semacam "wadah identitas developer" kamu. Isi nama bebas (misal: `HermesBot`).
3. Di dalam Provider, klik **Create Channel** → pilih tipe **Messaging API**.
4. Sistem akan mengarahkan kamu membuat LINE Official Account: isi nama, email, region, kategori bisnis (pilih yang paling mendekati, misal IT/Software). Setuju syarat & ketentuan.
5. Saat ditanya "mau daftar verified account?" → **skip** (tidak perlu, pilih "Nanti Saja").
6. Setelah akun jadi, buka **Official Account Manager** → tab **Chat** → matikan **Auto-reply (自動回應)** dan **Greeting message (歡迎訊息)**. Ini penting biar jawaban otomatis LINE gak rebutan sama bot kamu.

### Ambil 2 Kunci Penting

Dari console, kamu butuh dua string (jangan bocorin ke siapa pun — ini ibarat password akun):

| Kunci | Di mana | Bentuk |
|---|---|---|
| **Channel Secret** | Basic Settings | 32 karakter |
| **Channel Access Token** | Messaging API tab → tombol **Issue** | string panjang |

Copy keduanya ke tempat aman. Lanjut!

## Step 2: Tunnel — Buka Port Webhook ke Publik

LINE mengirim pesan user ke server kamu lewat **webhook** (LINE "menelpon" server kamu tiap ada pesan masuk). Masalahnya: Hermes Agent jalan di komputer lokal/VPS kamu yang gak punya IP publik. Solusinya: **tunnel**.

Default port webhook LINE Hermes adalah **8646** (bisa diubah via `LINE_PORT`). Pilih salah satu tunnel:

```bash
# Cloudflare Tunnel — recommended buat production (hostname tetap)
cloudflared tunnel --url http://localhost:8646

# ngrok — praktis buat develop/test
ngrok http 8646
```

Catat URL `https://xxx.ngrok-free.app` yang muncul — ini `LINE_PUBLIC_URL` kamu.

## Step 3: Konfigurasi Hermes Agent

Tambah ke `.env` profile Hermes kamu (`~/.hermes/.env` atau profile `.env`):

```bash
LINE_CHANNEL_ACCESS_TOKEN=token_panjang_dari_console
LINE_CHANNEL_SECRET=32_karakter_secret
LINE_ALLOWED_USERS=Uxxxxxxxxxxxxxxxxxxxxx   # user ID kamu (prefix U)
LINE_ALLOWED_GROUPS=Cxxxxxxxxxxxxxxxxxxxxx  # opsional, group ID (prefix C)
LINE_ALLOWED_ROOMS=Rxxxxxxxxxxxxxxxxxxxxx   # opsional, room ID (prefix R)
LINE_PUBLIC_URL=https://xxx.ngrok-free.app
```

> **⚠️ JANGAN LUPA `LINE_ALLOWED_USERS`!** Tanpa allowlist, bot gak akan membalas siapa pun kecuali kamu set `LINE_ALLOW_ALL_USERS=true` (hanya buat development). Isi User ID LINE kamu sendiri — bisa dilihat di Basic Settings halaman channel.

Lalu di `config.yaml`:

```yaml
gateway:
  platforms:
    line:
      enabled: true
```

Restart gateway: `hermes gateway restart`.

## Step 4: Set Webhook URL di LINE Console

Balik ke LINE Developers → channel kamu → tab **Messaging API**:

1. Di bagian **Webhook settings**, paste URL: `https://xxx.ngrok-free.app/line/webhook`
2. Klik **Verify** — harus dapat respons **200** (kalau gagal, cek 3 hal di bawah)
3. **Toggle "Use webhook" ke ON** — ini sering kelewat, defaultnya OFF!

### Kalau Verify Gagal — 3 Penyebab Paling Umum

1. **URL kurang `/line/webhook`** di akhir — paling sering!
2. **Gateway Hermes belum jalan** / belum di-restart setelah config
3. **ngrok/tunnel belum aktif**

Cek ketiganya, lalu Verify lagi.

## Step 5: Test di HP

Scan QR code dari tab Messaging API (atau cari nama official account kamu di app LINE) → add sebagai teman → kirim pesan.

Kalau dapat balasan — selamat, LINE kamu sekarang AI assistant! 🎉

## Menghindari Jebakan: `LINE_PUBLIC_URL` untuk Media

Pernah lihat bot yang jawab teks tapi **gagal kirim gambar**? Kemungkinan besar `LINE_PUBLIC_URL` kosong. Field ini **wajib diisi kalau agent mau kirim gambar/audio/video balik ke LINE** — HERMES pakai URL ini buat mengekspos file media secara publik.

Contoh nyata: agent disuruh bikin komik 4 panel, gambar berhasil di-generate di backend, **tapi gak pernah nyampe ke LINE** — semua karena `LINE_PUBLIC_URL` belum diisi. Setelah diisi → langsung muncul. Jadi isi dari awal biar gak pusing.

## Bonus: Tips Performa untuk LLM Lambat

Token balasan LINE (reply token) hanya berlaku **~60 detik**. Kalau model AI kamu lambat, balasan telat → LINE memaksa pakai **Push API berbayar**. Hermes punya solusi cerdas:

- Default `LINE_SLOW_RESPONSE_THRESHOLD=45` detik → kalau LLM masih mikir lewat 45 detik, Hermes kirim tombol **"🤔 Still thinking — Tap to get answer"** → user tap → bot kirim jawaban (tetap gratis, pakai reply token baru).
- Mau langsung fallback ke Push API tanpa tombol? Set `LINE_SLOW_RESPONSE_THRESHOLD=0`.

Biar tombol ini jalan mulus, matikan "interim messages" di config:

```yaml
display:
  interim_assistant_messages: false
```

## Kesimpulan

Connect Hermes Agent ke LINE cuma 5 langkah: buat channel → ambil kunci → setup tunnel → isi config → set webhook. Kemampuan yang kamu dapet jauh di atas chatbot biasa: agent dengan memori, skill, dan tool — semua dari dalam app LINE.

Punya pertanyaan atau nemu cara kreatif pakai LINE + AI agent? Tulis di komentar, diskusi seru! 🐷✨

— Chokdi 🐷 · Content Studio · 2026