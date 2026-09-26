---
title: "llms.txt: Bikin Blog Dibaca AI Agent, Bukan Cuma Googlebot"
date: 2026-09-27T00:20:00+07:00
draft: false
tags: ["AI Agent", "SEO", "Tutorial", "Cloudflare"]
---

Googlebot sudah bukan satu-satunya tamu yang mampir ke website kita. Sekarang yang datang baca itu Cursor, Claude Code, Copilot, dan ratusan agent lain — dan mereka tidak sabar merayapi HTML penuh iklan, menu, dan script. `llms.txt` adalah cara memberitahu mereka: "ini isi penting saya, baca yang ini saja."

Artikel ini bukan teori. Kami sudah menjalankannya di blog ini, dan di akhir ada bukti nyata plus lima kesalahan yang paling sering bikin file ini jadi sia-sia.

## Apa Itu llms.txt?

`llms.txt` adalah file Markdown di root domain — `https://domainkamu.com/llms.txt` — yang isinya ringkasan identitas + daftar link ke halaman paling penting, masing-masing dengan deskripsi satu baris.

Konsepnya diusulkan Jeremy Howard (Answer.AI) September 2024. Sampai 2026 ini statusnya **konvensi komunitas, bukan standar resmi IETF atau W3C** — jadi jangan harap ada validasi formal. Tapi sudah dipakai cukup luas untuk dianggap aman dipakai produksi.

Analogi paling gampang: **kalau `sitemap.xml` itu daftar semua barang di gudang, `llms.txt` itu daftar barang yang benar-benar kamu rekomendasikan ke pembeli.** Sitemap tidak mengkurasi apa pun. `llms.txt` justru intinya mengkurasi.

Ada juga versi besarnya, `llms-full.txt`, yang menempelkan seluruh isi teks halaman jadi satu file. Format ini dikembangkan Mintlify bersama Anthropic lalu masuk ke proposal resmi di [llmstxt.org](https://llmstxt.org/).

## robots.txt vs sitemap.xml vs llms.txt

Tiga file ini sering dianggap sama. Padahal kerjanya beda dan sebenarnya saling melengkapi.

| File | Pertanyaan yang dijawab | Siapa yang baca |
|---|---|---|
| `robots.txt` | "Kamu boleh masuk atau tidak?" | Semua crawler |
| `sitemap.xml` | "Ada URL apa saja di sini?" | Mesin pencari |
| `llms.txt` | "Dari semua ini, mana yang penting?" | AI agent & LLM |

`robots.txt` hanya kasih izin di level URL. Dia tidak pernah bilang halaman mana yang paling berharga, dan tidak menjelaskan bisnis kamu itu apa. Itu lubang yang diisi `llms.txt`.

## Data 2026: Adopsi Masih Tipis

Bagian ini yang biasanya dilewatkan artikel lain. Faktanya, jangan berharap keajaiban instan.

- **Cloudflare Radar** memindai 200.000 domain terpopuler: `robots.txt` hampir universal (78% situs punya), tapi **Content Signals hanya 4%**, dan negosiasi konten Markdown (`Accept: text/markdown`) baru **3,9%**. Standar baru seperti MCP Server Card dan API Catalog (RFC 9727) bahkan muncul di **kurang dari 15 situs** dari seluruh dataset.
- **Riset SE Ranking** atas 300.000 domain menemukan adopsi `llms.txt` sekitar **10,13%** — roughly satu dari sepuluh situs.
- **Limy** menganalisis 515 juta event trafik bot LLM: dari jumlah itu, hanya **408 request** yang menyentuh `/llms.txt`. GPTBot, ClaudeBot, PerplexityBot, dan Google-Extended umumnya lewat begitu saja.
- **Google bilang tidak.** Juli 2025 Gary Illyes menyatakan Google tidak mendukung `llms.txt` dan tidak berencana. John Mueller bahkan menyamakannya dengan meta keywords yang sudah mati.

Kesimpulan jujurnya: **kalau tujuanmu naik peringkat di Google, `llms.txt` bukan jawabannya.** Siapa pun yang menjualnya sebagai "faktor ranking GEO" sedang menjual sesuatu yang tidak didukung data.

### Lalu Kenapa Tetap Perlu Dibuat?

Karena nilai aslinya bukan di mesin pencari, tapi di **lapisan agent**. Ini yang disebut pergeseran dari B2C/B2B ke **B2A — Business to Agent**.

Menurut data Limy, agent coding seperti Cursor, Windsurf, Claude Code, Copilot, Cline, dan Aider **rutin** mencari `/llms.txt` dan `/llms-full.txt` begitu diarahkan ke sebuah situs dokumentasi. LangChain bahkan punya MCP server bernama `mcpdoc` yang tugasnya membuka file `llms.txt` untuk host semacam Cursor dan Claude Desktop.

Alasannya teknis dan masuk akal: HTML itu berisik. Menu, JavaScript, iklan, tracking pixel menghabiskan context window sebelum model sampai ke isi. Situs yang menyajikan Markdown dilaporkan menghemat token hingga **10x** — artinya agent lebih cepat, lebih murah, dan lebih akurat.

Jadi posisinya jelas: **untuk AI search nilainya spekulatif, untuk agentic web nilainya sudah nyata hari ini.**

## 4 Pondasi Agentic Readiness

`llms.txt` saja tidak cukup. Cloudflare baru-baru ini meluncurkan [isitagentready.com](https://isitagentready.com/) untuk menilai kesiapan sebuah situs dari 4 dimensi:

1. **Discoverability** — `robots.txt`, `sitemap.xml`, Link headers
2. **Content** — Markdown for Agents (sajikan `text/markdown`)
3. **Bot Access Control** — Content Signals, aturan bot AI, Web Bot Auth
4. **Capabilities** — MCP Server Card, API Catalog, WebMCP, OAuth discovery

Menariknya, Chrome juga sudah menyiapkan audit **Agentic Browsing** di Lighthouse dengan toolkit agent-ready — dan salah satu poin utamanya: accessibility tree yang rapi itu justru cara utama agent memahami halaman kamu. Aksesibilitas yang bagus untuk manusia ternyata juga untuk mesin.

Urutan pengerjaan yang realistis: **mulai dari `llms.txt` + `llms-full.txt` dulu** (paling murah, paling cepat), baru tambah Public API, lalu MCP tools kalau memang sudah butuh.

## Format yang Benar (dan 5 Kesalahan Fatal)

Struktur bakunya sederhana: judul H1, satu ringkasan singkat, lalu section-section berisi link.

```markdown
# Nama Situs

> Satu paragraf singkat: situs ini apa, untuk siapa, dan isinya apa.

## Artikel Utama
- [Judul Artikel](https://situs.com/artikel-a): deskripsi satu baris
- [Judul Artikel Lain](https://situs.com/artikel-b): deskripsi satu baris

## Optional
- [Halaman Arsip](https://situs.com/arsip): boleh dilewatkan
```

Lima kesalahan yang paling sering terjadi:

1. **Dipakai sebagai sitemap.** File berisi 200 URL justru merusak tujuannya. `llms.txt` = kurasi, bukan daftar lengkap.
2. **Copy template tanpa kustomisasi.** Ringkasan generik = sinyal ke model bahwa situs ini tidak serius.
3. **Bertentangan dengan `robots.txt`.** Dua file ini harus diedit sebagai satu paket, bukan terpisah.
4. **File basi.** Tulis manual lalu lupa update begitu ada artikel baru. Solusinya auto-generate.
5. **Tidak diukur.** Tanpa cek log, kamu tidak akan pernah tahu apakah ada yang benar-benar baca.

Untuk pengukuran, cek access log CDN/server kamu untuk hit ke `/llms.txt` dan `/llms-full.txt`, difilter dengan user agent AI. Bisa juga tanam honeypot link di dalam file — URL yang cuma akan diikuti pembaca otomatis.

## Kami Sudah Jalan: Bukti dari Blog Ini

Blog yang sedang kamu baca ini sudah menyajikan keduanya, dan semuanya **di-generate otomatis**, bukan ditulis tangan:

- `https://chokdi.ano99.com/llms.txt` → status **200 OK**, berisi katalog **272 artikel** dalam format terkurasi
- `https://chokdi.ano99.com/llms-full.txt` → status **200 OK**, data lengkap **1.352 baris** berisi judul, tanggal, dan tag semua artikel

Caranya: sebuah script kecil membaca frontmatter dari semua file Markdown artikel, mengambil `title`, `date`, dan `tags`, lalu menulis ulang kedua file statis itu. Dijalankan ulang setiap kali ada artikel baru, lalu push. Karena situsnya statis (Hugo + Cloudflare Pages), file itu langsung tayang di root domain tanpa server tambahan.

Kenapa kami tetap kerjakan padahal data adopsinya masih tipis? Karena ongkosnya nyaris nol dan risikonya juga nol — tidak ada satu pun bukti yang menunjukkan file ini merugikan peringkat. Sementara kalau gelombang agent benar-benar datang, situs yang sudah siap tinggal panen.

## Kesimpulan

`llms.txt` bukan trik SEO, dan jangan percaya siapa pun yang bilang begitu. Dia adalah **infrastruktur untuk web yang dibaca agent** — murah, aman, dan posisinya jelas di antara `robots.txt` dan MCP.

Kalau kamu punya situs statis atau blog dengan puluhan artikel, mulai hari ini: bikin `llms.txt`, tambahkan `llms-full.txt`, auto-generate dari frontmatter, lalu cek pakai [isitagentready.com](https://isitagentready.com/). Tiga puluh menit kerja, dan kamu sudah masuk 10% situs yang siap agent.

Kalau kamu mau lihat contohnya langsung, cek [/llms.txt](/llms.txt) di blog ini dan bandingkan dengan [llms-full.txt](/llms-full.txt) — perhatikan bedanya antara indeks dan korpus penuh.

Ada pertanyaan soal implementasi di platform lain, atau mau bahas MCP Server Card? Tulis di komentar.

— Chokdi 🐷 · Content Studio · 2026
