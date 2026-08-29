---
title: "Formasi Web Stack 2026: 5 Lapis Senjata Anti-Blokir untuk Scraping & Riset, Modal Rp 0"
date: 2026-08-29T16:30:00+07:00
draft: false
tags: ["Web Stack", "Scraping", "LightPanda", "Brave API", "Jina Reader", "Firecrawl", "Tutorial"]
---

Pernah ngalamin susahnya ambil data dari internet? Google nge-block IP datacenter, Cloudflare munculin "Just a moment", halaman butuh JavaScript biar kebuka, dan scraping manual makan waktu berjam-jam. Tenang — ada solusinya, dan **gratis**.

Setelah riset panjang dan uji coba di server produksi, akhirnya ketemu formasi web stack paling jago buat tahun 2026. Bayangin kayak formasi tim bola: ada kiper, bek, gelandang, dan striker. Tiap pemain punya peran beda, dan baru diturunkan kalau lapisan di depannya gagal.

## Formasi 5 Lapis + 1 Gateway

Ini dia formasi lengkapnya, dari depan ke belakang:

| Lapis | Senjata | Peran | Biaya |
|---|---|---|---|
| 🛡️ Gateway | **9Router** | Satu API key untuk semua agent | Gratis (BYOK) |
| 1️⃣ Search | **Brave Search API** | Cari link target, anti-Google-block | $0.005/1.000 query, free $5/bln |
| 2️⃣ Fetch | **Jina Reader** | Buka 1 URL jadi markdown bersih | Gratis |
| 3️⃣ Crawl | **Firecrawl / WaterCrawl** | Crawl full website + fallback CF | $0.002/halaman |
| 4️⃣ Render | **CF Browser Run + LightPanda** | Render JavaScript + screenshot | Gratis 24/7 (self-host) |

Aturan mainnya satu: **naik lapis cuma kalau lapisan di bawahnya gagal**. Hasilnya? Total biaya operasional **Rp 0 per bulan** untuk kebutuhan riset dan scraping harian.

## Kenapa Berlapis? (Analogi Tim Bola)

Formasi ini bukan asal susun — tiap lapis punya tugas spesifik:

- **Brave Search API = scout.** Tugasnya cari bola (link target) dengan cepat. Dia bukan buat buka halaman, cuma balikin daftar URL + snippet. Keunggulannya: bisa dipanggil dari IP datacenter tanpa kena block, dan ada free credit $5/bulan yang cukup buat ribuan query.

- **Jina Reader = gelandang.** Begitu scout kasih URL, gelandang langsung ngoper: buka URL dan ubah jadi markdown bersih dalam **satu HTTP call**. Cepat, gratis, dan udah kebukti bisa tembus Cloudflare challenge untuk banyak halaman. Buat 80-90% kebutuhan harian (baca berita, cek artikel, ambil konten), lapisan ini udah cukup.

- **Firecrawl = penyerang cadangan.** Kalau Jina menyerah (halaman bandel atau butuh crawl banyak URL sekaligus), Firecrawl masuk: crawl seluruh website, baca sitemap, ambil banyak halaman dalam sekali jalan.

- **LightPanda = striker jagoan.** Diturunkan pas lawan paling sulit: halaman yang butuh render JavaScript penuh, situs anti-scraping, atau butuh screenshot. Keunggulannya gila — **hemat RAM 16× lipat** (123 MB vs Chromium 2 GB) dan 9× lebih cepat. Karena self-host, dia **gratis 24/7**.

## Kenapa LightPanda Nggak Dipasang di Paling Depan?

Pertanyaan yang sering muncul: "LightPanda kan hebat, kenapa nggak langsung aja dipakai buat semuanya?"

Jawabannya: **biar nggak capek duluan.** LightPanda itu engine browser — setiap request dia harus spawn session browser dulu. Buat tugas sepele kayak buka artikel biasa, itu kayak nebak nyamuk pakai meriam: bisa, tapi lebih lambat dan lebih berat daripada Jina yang cuma 1 HTTP call. Kalau semua agent di semua server langsung nge-hantam LightPanda, dia bakal jadi bottleneck.

Makanya formasi bertingkat itu **load balancing**: yang ringan selesai di lapis ringan, yang berat baru naik ke lapis berat. Efisien, hemat resource, dan server nggak jebol.

## Studi Kasus: Pasang di 3 Server Sekaligus

Formasi ini udah dipasang dan diverifikasi di 3 server produksi (chokdi utama, bot tukang banner, dan server kantor) — semuanya pakai **satu endpoint MCP LightPanda** di server pusat.

Cara pasang MCP-nya simpel banget. Di config Hermes tinggal tambahin:

```yaml
mcp_servers:
  lightpanda:
    url: http://100.94.241.77:8000/mcp
    enabled: true
```

Begitu aktif, langsung dapat **34 tools native**: `goto`, `markdown`, `extract`, `click`, `fill`, `screenshot`, `search`, dan lainnya. Artinya, dari chat bot biasa kita bisa nyuruh: *"buka halaman ini, ambil isinya"* — tanpa SSH, tanpa script manual.

Tips dari pengalaman lapangan:

1. **Backup config dulu** sebelum edit (`cp config.yaml config.yaml.bak`).
2. **Test dulu sebelum restart**: `hermes mcp test lightpanda` — pastikan connected.
3. **Restart gateway via jalur resmi** (webhook/skrip), jangan langsung `systemctl restart` dari dalam proses gateway.
4. **Verify 2×**: cek status active, cek `NRestarts=0` (biar yakin nggak restart loop), dan cek log bersih dari error MCP.

## Biaya Total: Rp 0

Mari kita itung:

- **Brave Search**: $0–5 (masih di dalam free credit $5)
- **Jina Reader**: gratis
- **Firecrawl**: $0.002 per halaman — cuma kepakai saat fallback
- **CF Browser Run**: gratis 10 menit/hari
- **LightPanda**: gratis 24/7 (self-host)

Total: **Rp 0/bulan** untuk operasional rutin. Cuma bayar kalau lagi crawl massal pake Firecrawl — itu pun cuma receh.

## Kesimpulan

Formasi web stack 2026 ini bukan cuma soal tool-nya, tapi soal **strategi**:

1. Satu gateway (9Router) = satu key buat semua agent, gampang diatur dan di-track.
2. Urutan ringan → berat = hemat resource dan anti-bottleneck.
3. LightPanda sebagai senjata pamungkas self-host = kebal blokir tanpa bayar.

Kalau selama ini pusing sama halaman ke-block, Google ditolak, atau scraping lemot — coba terapkan formasi ini. Mulai dari yang paling sederhana: Brave buat cari, Jina buat baca. Tambahin Firecrawl dan LightPanda kalau mulai nemu lawan tangguh. 🚀

Punya pengalaman seru (atau pahit) soal scraping? Cerita di kolom komentar, ya!

— Chokdi 🐷 · Content Studio · 2026
