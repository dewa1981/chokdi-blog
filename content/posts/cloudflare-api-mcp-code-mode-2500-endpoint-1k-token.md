---
title: "Cloudflare API MCP + Code Mode: Akses 2500 Endpoint dalam 1.000 Token (2026)"
date: 2026-09-02T11:20:00+07:00
draft: false
tags: ["Cloudflare", "MCP", "AI", "Agent", "DevOps", "Tutorial", "React"]
---

Ada video yang lagi rame di X nih, di-posting sama @jilles (Jilles Soeters): **Cloudflare API punya MCP yang gila**. Klaimnya bikin merinding — pakai Code Mode, seluruh Cloudflare API (~2.500 endpoint) bisa diakses cuma dalam **~1.000 token**. Di video itu dia demo: beli domain, deploy aplikasi React ke domainnya, suruh agent cek error, fix, terus re-deploy. Katanya "It's SICK 🔥" — dan aku sependapat, ini masa depan DevOps.

Buat yang nggak ngerti MCP dan kenapa ini penting — dolan dulu ke sini. Ini bukan sekadar tool keren, tapi bakal ngerubah cara kita kerja sama infrastruktur cloud.

## Apa itu MCP dan Kenapa Cloudflare Masuk List Ini?

**MCP (Model Context Protocol)** itu standar terbuka biar AI agent bisa "nyambung" ke tool/layanan eksternal. Bayangin kayak **colokan USB universal untuk AI**: satu protokol, tapi bisa nyolok ke banyak perangkat (layanan). Nggak lagi perlu integrasi custom satu-satu — sekali nyambung, agent langsung bisa "tanganin" layanan itu.

Nah, Cloudflare ngedukung MCP, dan ini penting karena Cloudflare itu **bukan cuma CDN**. Dia punya:

- DNS zone management
- Workers & Pages (serverless)
- R2 (object storage)
- Tunnel (anti-DDoS)
- WAF & firewall rules
- Stream, Images, dan puluhan layanan lain

Totalnya **~2.500 endpoint API**. Bayangin harus nulis integrasi manual buat semua itu — bisa-bisa berminggu-minggu. Dengan MCP, agent langsung bisa "ngobrol" sama semua layanan itu pakai bahasa natural.

## Magic-nya: Code Mode, Akses Penuh dalam ~1.000 Token

Yang bikin joss dari tweet Jilles itu bukan cuma "ada MCP" — tapi **Code Mode**-nya. Ini konsep yang jarang dibahas:

- Biasanya, MCP server punya daftar tool yang di-expose ke agent. Makin banyak tool, makin banyak token yang dikonsumsi tiap request (karena agent harus "tahu" semua tool).
- **Code Mode** ngerubah pendekatan: agent nggak perlu dapetin semua 2.500 tool sekaligus. Dia baca/manggil endpoint sesuai kebutuhan, dan **instruksi + konteks tool-nya super hemat** — cuma ~1.000 token buat seluruh API surface.

Artinya: **tanpa nambah-nambahin context window**. Agent tetap bisa akses endpoint apa pun di Cloudflare, tapi nggak boros token. Ini krusial buat yang mau deploy agent yang kerja lama tanpa biaya token meledak.

Bayangin kayak **peta list isi buku** vs **buku lengkap**: Code Mode kasih agent daftar isi yang super ringkas, dan agent baru baca halaman spesifiknya pas butuh. Hemat banget.

## Yang Didemo di Video (Workflow Keren)

Di video @jilles, dia nunjukin alur yang bikin DevOps jadi otomatis:

1. **Beli domain** — lewat API Cloudflare (Registrar), langsung dari agent.
2. **Deploy aplikasi React** ke domain itu (via Pages/Workers).
3. **Agent cek error** — dia suruh agent periksa ada masalah nggak.
4. **Agent fix sendiri** — kalau ada error, agent debug dan benerin kodenya.
5. **Re-deploy** — deploy ulang sampai aplikasinya bener.

Ini **loop agentic penuh**: dari ide → domain → deploy → monitoring → fix → deploy lagi, tanpa manusia campur tangan di tiap langkah. Buat yang biasa manual SSH + deploy, ini terasa kayak sihir.

## Kenapa Ini Penting untuk Bisnis Kita?

Kita udah satu ekosistem Cloudflare — tunnel, WAF, Pages, Workers, R2 semua di sana. Dengan MCP + Code Mode:

- **Nggak perlu lagi token API beda-beda** dan integrasi custom biar agent ngurus Cloudflare.
- **Agent bisa ngelapor error**, fix, deploy ulang — otomatis, nggak harus nunggu manusia.
- **Hemat token** — akses 2.500 endpoint tanpa nge-blow context window, bisa jalan lama tanpa biaya nembus langit.
- **Satu pintu** — semua resource Cloudflare diatur dari satu "percakapan" dengan AI.

Ini persis kayak lompatan yang dulu kita bahas: dari "aku tulis script manual buat tiap hal" → "aku suruh agent ngurusin". Sekarang agent bisa **ngurusin Cloudflare sendiri**.

## Cara Mulai & Tips

Buat yang penasaran coba:

1. **Cek dokumentasi resmi Cloudflare MCP** — mereka punya server MCP yang bisa disambung ke agent (Hermes, Claude, dll).
2. **Mulai dari task kecil** — deploy satu Worker atau kelola satu DNS zone, baru beranjak ke workflow kompleks.
3. **Kombinasikan dengan tool lain** — MCP Cloudflare bisa digabung sama MCP lain (misal database, monitoring) jadi satu agent yang ngurus seluruh stack.
4. **Perhatikan keamanan** — akses ke semua endpoint berarti **token/scopes WAJIB dibatasi** (least privilege). Agent kuat, tapi harus dikerangkeng. Nggak mau kan agent bisa hapus production zone.

## Kesimpulan

Tweet @jilles itu bukan hype kosong — **MCP Cloudflare + Code Mode itu game changer** buat cara kita kelola infrastruktur. Akses 2.500 endpoint dalam ~1.000 token artinya agent bisa ngurus seluruh Cloudflare kita tanpa boros konteks: beli domain, deploy, cek error, fix, re-deploy — semuanya bisa otomatis.

Ini kayak punya **asisten DevOps yang selalu siaga** 24/7 di dalam stack Cloudflare kita. Buat yang baru mulai, cobain dari yang kecil dulu, dan selalu batasin scope token biar aman. 🚀

Punya pengalaman cobain MCP Cloudflare atau mau coba bikin workflow otomatis deploy? Cerita di kolom komentar, ya!

— Chokdi 🐷 · Content Studio · 2026
