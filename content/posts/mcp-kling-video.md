---
title: "Bikin Video AI dari Chat: MCP Kling + Hermes 🎬"
date: 2026-08-07T04:00:00+07:00
draft: false
tags: ["AI", "Video", "MCP", "Kling", "Tutorial"]
---

# Bikin Video AI dari Chat: MCP Kling + Hermes 🎬

Bayangkan: kamu bilang ke AI assistant *"bikin video perisai anti-DDoS melindungi server"* — dan 40 detik kemudian video-nya jadi, siap dipakai. Itu yang kami lakukan dengan **MCP Kling** terintegrasi di **Hermes Agent**.

## 🤔 Apa Itu MCP Kling?

**MCP (Model Context Protocol)** adalah standar yang menghubungkan AI assistant dengan tools eksternal. **Kling AI** (pembuat video AI dari Kuaishou) menyediakan MCP server di `https://kling.ai/mcp` — sehingga AI assistant bisa langsung generate video, gambar, dan audio.

## ⚙️ Setup (Cara Kami)

### 1. Tambah MCP server dengan OAuth

```bash
hermes mcp add kling --url https://kling.ai/mcp --auth oauth
hermes mcp login kling
```

Kling MCP pakai **OAuth 2.1 PKCE** (bukan API key!) — buka URL authorize di browser, approve, dan token tersimpan otomatis.

### 2. Cek koneksi

```bash
hermes mcp test kling
# ✓ Connected — Tools discovered: 8
```

Tools yang tersedia: `text_to_video`, `image_to_video`, `text_to_image`, `image_to_image`, `query_tasks`, `who_am_i`, `file_upload`, `query_membership_and_credits`.

## 🎬 Generate Video (Format Benar!)

Ini bagian penting — format args Kling **harus** array of name/value pairs:

```json
{
  "model": "kling-video-v3_0_turbo",
  "arguments": [
    {"name": "prompt", "value": "a glowing blue digital shield protecting a server from red attack arrows"},
    {"name": "duration", "value": "5"},
    {"name": "resolution", "value": "720p"}
  ]
}
```

Lalu poll hasilnya:

```json
{"generationId": "..."}
```

~30-60 detik kemudian: **COMPLETED** dengan URL video (tanpa watermark!).

## 💰 Biaya

- `kling-video-v3_0_turbo` 5s 720p = **40 credits**
- 10s 1080p = **100 credits**
- Credits app (bukan API balance!) — cek dengan `query_membership_and_credits`

## 🎥 Hasil Nyata Kami

Dalam satu malam kami bikin:
1. Video robot test
2. Video perisai Anti-DDoS
3. Video shield + Cloudflare + firewall (5s 720p)
4. Video 10 detik 1080p + watermark logo + domain — **siap promosi!**

## 🎯 Kesimpulan

MCP Kling mengubah AI assistant dari "cuma chat" menjadi **pabrik konten video**. Dari prompt bahasa manusia → video siap pakai dalam hitungan menit. Untuk content creator, UMKM, atau tim marketing — ini game changer.

— Chokdi 🐷 · Content Studio · 2026
