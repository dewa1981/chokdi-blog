---
title: "Hermes Browser Use Mode: Satu Tool untuk Semua, Hemat Token Drastis"
date: 2026-08-11T21:00:00+07:00
draft: false
description: "Update Hermes Browser Use Mode CLI 3.0 — browser_exec satu tool ganti semua tool navigasi browser, hemat token hingga 61% untuk multi-item extraction."
tags: ["hermes", "browser-use", "ai-agent", "scraping", "token"]
---

## Browser Use Mode: Cara Baru Hermes Kendalikan Browser

Tim Nous Research baru rilis update signifikan untuk Hermes Agent — **Browser Use Mode** yang menyatukan semua tool navigasi browser jadi **satu tool `browser_exec`**. Ini bukan sekadar polish, tapi perubahan arsitektur yang bikin kerjaan research dan scraping jauh lebih hemat.

### Masalah Sebelumnya

Dulu, agent harus pakai **banyak tool terpisah** buat navigasi browser:

- Navigasi ke halaman
- Screenshot
- Klik elemen
- Ketik teks
- Scroll
- Baca snapshot

Setiap tool = satu putaran LLM = **boros token**. Buat tugas scraping yang butuh puluhan langkah, biayanya numpuk banget.

### Solusinya: Satu Tool `browser_exec`

Dengan update ini, Hermes cuma pakai **satu tool** yang handle semuanya. Hasilnya:

- **Multi-item extraction: hemat hingga 61% token** (klaim resmi Nous 48-66%, diukur 61% — konsisten)
- Single page read justru lebih boros (~2×) — jadi ini bukan untuk tugas sepele
- Sangat cocok buat research, scraping, channel harvesting

### Cara Setup (4 Langkah)

1. **Update Hermes** dulu ke versi terbaru
2. **Enable browser toolset**
3. **Install CLI** — kalau di local langsung ke step 5; di VPS perlu install Chrome + point ke bashrc
4. **Register browser use skill**

### ⚠️ Trap Penting di VPS

Ada satu masalah umum di VPS: kalau run pertama sukses tapi agent lapor `browser_exec` gagal dengan *"no ChromeDevTools protocol endpoint"* dan malah drive browser lewat terminal — **fix segera** dengan `hermes config set browser...`.

Kenapa penting? Karena mode ini bikin agent bisa **generate dan eksekusi Python di mesin** yang menjalankan Hermes. Makanya mode ini dibatasi untuk sesi dengan akses terminal. **Jangan kasih personal Chrome** — pakai browser yang disediakan tim Nous.

### Local vs VPS: Mana Lebih Baik?

| Skenario | Local | VPS |
|---|---|---|
| YouTube/IG/X (anti-bot keras) | ✅ Jauh lebih baik | ❌ Kena "confirm you're not a bot" |
| Website gampang (Wikipedia, docs, Hugo/WordPress, RSS, JSON API) | ✅ | ✅ Bisa |
| Website JS-rendered (Shopify, Next.js) | ✅ | ⚠️ Butuh Firecrawl |

- **Local machine** jauh lebih efektif — bisa tembus anti-bot website berat
- Di **VPS**, tetap bisa workaround: ekstrak metadata video, harvest data channel (judul/views/umur/deskripsi/komentar)
- Di VPS, stick ke website gampang yang bisa di-curl/fetch
- Pakai **Firecrawl** (subscription Nous) buat website JS-rendered dengan sedikit bot wall

### Orkestrasi Multi-Agent

Contoh menarik dari video: proses entirely dijalankan oleh **Kimi** (orchestrator agent) yang ngobrol ke Hermes agent dan menyuruhnya buka halaman video. Semua prompt datang dari Kimi, bukan manual. Kalau punya lebih dari satu agent, bisa pakai pola ini buat speed up kerjaan.

### Kustomisasi Tanpa Batas

Karena ini skill-based, kamu bisa buat/ubah file `SKILL.md` untuk ngatur:

- Cara agent browse halaman
- Cara agent compile & ringkas data
- Cara agent bikin laporan dari yang di-scrape

### Kesimpulan

Browser Use Mode adalah **game changer** untuk research dan scraping di Hermes Agent. Kuncinya:

- Gunakan untuk **multi-item extraction** (bukan baca 1 halaman)
- **Local > VPS** untuk website anti-bot
- Hemat token hingga **61%** pada tugas harvest besar
- Bisa diorkestrasi agent lain + dikustomisasi lewat skill

Tim Nous juga bilang lagi pivot ke arah lokal karena banyak nilai buat scraping. Jadi kalau kamu serius di dunia scraping, **local setup Hermes** layak dipertimbangkan.

Artikel terkait: [DeepSeek V4 Flash di Mac Studio](/posts/deepseek-v4-flash-mac-studio/), [Mac Studio M5 Ultra](/posts/mac-studio-m5-ultra-monster/)
