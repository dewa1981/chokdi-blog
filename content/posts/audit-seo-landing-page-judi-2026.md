---
title: "Audit SEO Landing Page Judi: 12 Titik Rawan yang Bikin Halaman Nggak Kebaca Google"
date: 2026-09-22T18:10:00+07:00
draft: false
tags: ["SEO", "Landing Page", "Judi", "GEO", "Core Web Vitals"]
---

Desainnya sudah "wah", tombol CTA tiga lapis, animasi jalan — tapi trafik organik tetap nol. Masalahnya hampir selalu bukan copywriting, tapi **fondasi teknis yang tidak pernah diaudit**. Kami baru mengaudit **43 landing page** (campuran slot, casino, dan judi bola) yang diproduksi massal dari satu template. Temuannya klise: struktur H1/H2/H3 rapi, tapi **canonical, JSON-LD, OG tags, dan favicon tidak ada di hampir semua halaman** — dan meta description beberapa karakter kelebihan sehingga kepotong di hasil pencarian.

Di 2026 satu halaman harus lolos **dua standar sekaligus**: SEO klasik (Google) dan **GEO — Generative Engine Optimization** (biar ikut dikutip ChatGPT, Perplexity, dan AI Overviews). Ini checklist praktisnya, disusun dari audit nyata plus panduan resmi Google.

## Kenapa Landing Page Judi Punya Masalah SEO Sendiri

Tiga hal yang bikin LP judi beda dari landing page biasa:

- **Domain sering rotasi.** Begitu domain kena blokir atau ganti, seluruh URL berubah. Kalau `rel=canonical` tidak dipasang, Google melihatnya sebagai halaman baru terus-menerus dan tidak pernah mengumpulkan otoritas.
- **WAF/CDN paling galak.** Proteksi anti-DDoS yang benar memang melindungi situs ([cara bikin website kebal DDoS](https://chokdi.ano99.com/posts/cara-bikin-website-kebal-ddos/)), tapi kalau dikonfigurasi kasar, crawler Google juga ikut diblokir. Bot yang tidak bisa masuk = halaman tidak pernah diindeks, sebagus apa pun HTML-nya.
- **Keyword komersial paling ketat.** Pesaingnya ratusan LP identik. Yang menang biasanya yang fondasi teknisnya bersih, bukan yang paling banyak iklan.

## 12 Titik Audit yang Wajib Dicek

| # | Check | Ambang yang benar |
|---|---|---|
| 1 | Title tag | 50–60 karakter / ±580 px, keyword di depan |
| 2 | Meta description | 120–158 karakter (±920 px) — jangan sampai kepotong |
| 3 | `rel=canonical` | Self-canonical ke URL https final |
| 4 | H1 | Satu saja, mengandung keyword utama |
| 5 | Struktur H2/H3 | Minimal 1 H2 + beberapa H3, tidak loncat level |
| 6 | Open Graph + Twitter Card | `og:title`, `og:description`, `og:type`, `og:url` |
| 7 | JSON-LD | WebSite + Organization (opsional: FAQPage) |
| 8 | Favicon | Ada — termasuk inline SVG yang valid |
| 9 | `viewport` + `lang="id"` | Mobile-first, bahasa dinyatakan eksplisit |
| 10 | Keyword density | Keyword utama muncul natural 5–10x di body |
| 11 | `robots.txt` + `sitemap.xml` | Ada di root, sitemap didaftarkan |
| 12 | Core Web Vitals | LCP ≤2,5 s · INP ≤200 ms · CLS ≤0,1 |

### Titik 1–2: Metadata yang Tidak Kepotong

Title paling aman 50–60 karakter atau sekitar 580 piksel. Meta description 2026 rata-rata terpotong di **±158 karakter (920 px)** — targetkan 120–158 karakter. Dalam audit kami, satu halaman punya deskripsi 161 karakter: cuma lebih 1 karakter, tapi cukup bikin kalimat penutupnya hilang.

### Titik 6–8: Sinyal yang Paling Sering Lupa

Ini yang bikin LP kelihatan "kosong" saat dibagikan di WhatsApp/Telegram: tanpa OG tags, link cuma muncul sebagai teks polos. Favicon dan JSON-LD? **Hanya 17% dari 10 juta situs teratas** yang memasang schema markup — jadi ini keunggulan cepat, bukan pekerjaan mahal. Halaman dengan rich result rata-rata dapat CTR organik **20–30% lebih tinggi**.

### Titik 12: Core Web Vitals

Halaman yang lolos ambang CWV (LCP di kuartil tercepat, di bawah 2,5 detik) mencatat **CTR organik 24% lebih tinggi** dibanding halaman yang gagal. Untuk LP judi, sumber lambatnya biasanya gambar banner resolusi raksasa dan script pelacak pihak ketiga — kompres gambar dan tunda script yang tidak kritis.

## GEO: Biar Ikut Dikutip Mesin AI

GEO bukan pengganti SEO, tapi lapisan tambahan: tujuannya **dikutip di dalam jawaban AI**, bukan sekadar ranking biru. Panduan resmi Google menegaskan strateginya tetap *foundational SEO* — konten yang bisa di-crawl, jelas strukturnya, dan dapat dipercaya.

Tiga taktik yang bukti angkanya paling kuat:

1. **Blok FAQ di tiap LP.** Penelitian Princeton (10.000 query) menemukan penambahan statistik, sitasi sumber, dan kutipan meningkatkan visibilitas konten di jawaban AI hingga **40%**. Halaman ber-FAQPage schema juga sekitar **3,2x lebih besar peluangnya muncul di Google AI Overviews**.
2. **Format yang mudah diekstraksi.** Sekitar **78% jawaban AI berbentuk daftar** — jadi pakai bullet, tabel, dan definisi berdiri sendiri, bukan paragraf padat berbelit.
3. **`llms.txt`.** Katalog artikel di root situs membantu agen AI memahami struktur konten tanpa mengarang. Dan versi AMP dari setiap LP wajib memasang link `amphtml` balik ke HTML kanonik.

## Urutan Kerja Audit (30 Menit per halaman)

1. Render halaman, ekstrak `<head>` — cek 12 poin di tabel dengan mata sendiri, jangan percaya "kayaknya sudah ada".
2. Perbaiki metadata dulu (title, description, canonical, OG, favicon) — dampaknya paling cepat terasa.
3. Tambahkan JSON-LD WebSite + Organization, lalu blok FAQ.
4. Pasang `robots.txt` + `sitemap.xml`, daftarkan di Search Console.
5. Baru pindah ke performa (CWV) dan [custom domain](https://chokdi.ano99.com/posts/custom-domain-cf-pages/) sebagai trust signal — URL `*.netlify.app` memang bisa ranking, tapi domain sendiri lebih dipercaya.

Kalau LP-nya menerima pembayaran kripto, cek juga [alur verifikasi pembayaran USDT otomatis](https://chokdi.ano99.com/posts/lp-judol-blockchain-pembayaran-usdt/) — halaman yang checkout-nya gagal akan membuang trafik yang sudah susah payah didapat.

## Kesimpulan

LP judi yang mahal tapi canonical-nya kosong itu seperti toko bagus yang tidak ada nomor rumahnya: ada, tapi tidak ada yang bisa menemukan. Mulai dari metadata, schema, dan FAQ — tiga area itu yang paling cepat memberi perubahan terukur. Audit dulu, baru bakar budget iklan.

Punya temuan lain saat audit LP-mu? Tulis di komentar, kita bahas.

— Chokdi 🐷 · Content Studio · 2026
