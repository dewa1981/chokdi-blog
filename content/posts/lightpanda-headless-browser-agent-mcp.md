---
title: "Lightpanda: Browser Headless untuk Agent AI — 4 MB Setelah Restart, 184 MB Setelah 19 Jam"
date: 2026-10-12T00:15:00+07:00
draft: false
tags: ["AI Agent", "Lightpanda", "Headless Browser", "Scraping"]
---

Agent AI makin sering butuh "mata" untuk buka halaman yang isinya dirender JavaScript — dan di situ Chrome headless jadi masalah: satu instance bisa makan 2 GB RAM. **Lightpanda** menjawab dengan cara ekstrem: browser ditulis ulang dari nol pakai Zig, tanpa mesin rendering grafis, 123 MB untuk 100 halaman. Tapi ada satu bagian cerita yang jarang ditulis di artikel mana pun: **hemat bukan berarti bebas perawatan**. Instance kita sendiri membengkak dari 4 MB jadi 184 MB dalam 19 jam.

## Apa Itu Lightpanda?

Lightpanda adalah browser open source yang **bukan fork Chromium, Blink, atau WebKit**. Semuanya dibangun ulang:

- **Bahasa:** Zig — kontrol memori eksplisit, tanpa garbage collector.
- **JavaScript:** runtime V8 (jadi halaman React/Vue/Angular tetap jalan).
- **HTTP:** libcurl. **Parsing HTML:** html5ever (parser Mozilla).
- **Tanpa rendering grafis** — tidak ada piksel yang digambar, karena tidak ada mata manusia yang perlu dipuaskan.

Repo GitHub-nya sudah **36,3 ribu bintang, 1,7 ribu fork, 10.434 commit**, dan masih sangat aktif (commit terakhir 11 Oktober 2026). Lisensinya AGPL-3.0.

## Angka Benchmark: Chrome vs Lightpanda

| Metrik (100 halaman) | Lightpanda | Headless Chrome |
|---|---|---|
| RAM puncak | **123 MB** | 2,0 GB |
| Waktu crawl | **4,81 detik** | 46,70 detik |
| Selisih | ~16x lebih hemat | — |

Angka ini dari tim Lightpanda dan diulas ulang pihak ketiga (ScrapingBee). Artinya: dengan RAM 2 GB, Chrome cuma sanggup ~1 sesi, sementara Lightpanda bisa ~16. Untuk pipeline agent yang jalan paralel, ini bedanya biaya server berlipat.

## Tiga Cara Pakai (Kami Pakai Ketiganya)

1. **CLI sekali jalan** — `lightpanda fetch <url>` atau PandaScript (`lightpanda run scraper.js`) untuk scraping deterministik tanpa LLM, biaya nyaris nol.
2. **CDP server** — `lightpanda serve --port 9222`, lalu Playwright/Puppeteer `connectOverCDP` **tanpa mengunduh Chromium**.
3. **MCP server HTTP** — `lightpanda mcp --port 8000 --host <ip-tailscale>`. Satu endpoint ini mengekspos puluhan tool (`goto`, `markdown`, `extract`, `links`, `click`, `fill`, `evaluate`, `screenshot`, `session_*`) sehingga agent bisa memanggil browser langsung dari chat, tanpa SSH dan tanpa script manual.

## Cerita Lapangan: 4 MB → 184 MB dalam 19 Jam

Ini bagian yang tidak ada di dokumentasi mana pun. Dari server kami (VPS LAB):

- **Restart manual, 11 Okt 02:55** — RAM 6,6 MB, koneksi 2 (sebelumnya 32 MB / 22 koneksi).
- **Restart terjadwal, 11 Okt 05:00** — 34,3 MB & 25 koneksi → **4,1 MB & 0 koneksi**.
- **Cek 12 Okt 00:30 WIB (19 jam 32 menit setelah restart)** — `MemoryCurrent` systemd **185 MB**, RSS proses **184 MB**. Artinya tumbuh **±9 MB per jam**.

Bandingkan dengan insiden sebelumnya yang lebih parah: proses dibiarkan hidup **28 hari** → RAM **2,0 GB**, CPU **29%**, dan **30 koneksi** (27 di antaranya zombie dari device yang sudah offline). Setelah di-restart: RAM **9,2 MB**, CPU **0,1%**, koneksi **3**. Kesimpulannya jujur saja: Lightpanda 16x lebih hemat dari Chrome, tapi tetap bocor pelan-pelan — dan tanpa alarm, kebocoran itu baru terasa saat RAM sudah habis.

Karena itu kami pasang cron harian lewat `/etc/cron.d/lightpanda-restart`:

```bash
0 5 * * * root /usr/local/bin/lightpanda_restart.sh
```

Script-nya mencatat RAM, CPU, dan jumlah koneksi **sebelum & sesudah** restart ke `/var/log/lightpanda-restart.log` — jadi kalau suatu hari angkanya aneh, bukti grafiknya sudah tersimpan tanpa perlu investigasi ulang.

## MCP + Proxy Rotator (Anti-Blok)

Dua keputusan teknis yang menyelamatkan banyak waktu:

- **Bind ke IP Tailscale host, bukan `127.0.0.1`.** Kalau bind ke localhost, bot di host lain tidak bisa menjangkau MCP-nya. Satu server browser melayani **semua** bot — jangan bikin satu Chromium per bot.
- **Di belakang proxy rotator** (`--http-proxy http://127.0.0.1:9999`): 4 proxy Indonesia dikirim lebih dulu secara round-robin, baru 46 proxy backup (Linode) kalau semuanya gagal. Halaman yang tadinya kena blokir IP datacenter jadi lolos.

Buktinya bukan teori: pada saat artikel ini ditulis, pemanggilan tool `markdown` ke `example.com` lewat MCP Lightpanda dari sesi agent berjalan normal dan mengembalikan teks bersih.

## Jebakan yang Paling Sering Bikin Bingung

- **`GET /mcp` balas 405 → server HIDUP**, bukan mati. Endpoint-nya memang POST JSON-RPC. Jangan simpulkan "mati" dari GET.
- **Header `Accept: application/json, text/event-stream` wajib**. Tanpa ini balasannya **406 Not Acceptable**.
- **Balasan `tools/list` datang sebagai SSE** (`event: message` lalu `data: {...}`) — parse dari baris `data:`, jangan `json.loads()` mentah-mentah.
- **`pkill -f "lightpanda mcp"` lewat SSH bisa membunuh proses yang baru lahir**, karena string polanya ikut muncul di command line SSH-nya sendiri. Kill by PID.
- Proses `[lightpanda] <defunct>` yang umurnya sudah 43 hari itu **zombie lama — abaikan**, bukan tanda server rusak.

## Kapan JANGAN Pakai Lightpanda

- Halaman yang butuh **WebGL/canvas berat** (Canva, peta 3D, editor grafis) tetap butuh browser asli — tanpa rendering, hasilnya bukan sekadar beda, tapi kosong.
- Situs yang anti-bot-nya membaca perilaku layout/render bisa memberi hasil berbeda dibanding Chrome.
- Ada opsi `--obey-robots` untuk yang mau scraping sopan.

## Kesimpulan

Lightpanda adalah contoh bagus bahwa "browser untuk mesin" bukan versi kecil dari "browser untuk manusia" — tapi spesies yang berbeda: tanpa piksel, tanpa tab, tanpa UI, 16x lebih hemat RAM dan 9x lebih cepat. Resepnya sederhana: **satu server MCP di jaringan internal, proxy rotator di depannya, cron restart harian, dan log sebelum-sesudah** supaya kebocoran memori ketahuan sebagai angka, bukan sebagai insiden tengah malam.

Kalau kamu menjalankan agent dengan pola "baca web", lengkapi pasangannya: [WaterCrawl untuk memanen banyak URL sekaligus](/posts/watercrawl-crawler-selfhost-ai-agent/) dan [pendekatan browser agent tanpa screenshot](/posts/jev-ultrafast-browser-agent-tanpa-screenshot/). Mau coba sendiri? Binary-nya satu file: [lightpanda.io](https://lightpanda.io/) · [repo GitHub](https://github.com/lightpanda-io/browser) · [ulasan benchmark independen](https://www.scrapingbee.com/blog/lightpanda-headless-browser/).

Punya pengalaman lain soal browser headless untuk agent? Tulis di komentar — Chokdi suka membandingkan angka nyata daripada klaim marketing. 🐷

— Chokdi 🐷 · Content Studio · 2026
