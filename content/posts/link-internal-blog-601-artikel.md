---
title: "Link Internal Blog 601 Artikel: 10 dari 15 Halaman Tidak Menaut ke Artikel Lain"
date: 2026-11-12T00:20:00+07:00
draft: false
tags: ["SEO", "Link Internal", "Hugo", "Blog"]
---

Sitemap berisi 1.304 URL dan semuanya balas HTTP 200 — kelihatannya beres. Tapi begitu saya buka badan artikelnya satu per satu, **10 dari 15 artikel sampel tidak punya satu pun link ke artikel lain di blog yang sama**. Sitemap memang memberi tahu Google daftar halaman, tapi tidak pernah menggantikan pekerjaan link internal: menghubungkan halaman satu ke halaman lain.

Ini catatan pengukuran apa adanya, plus perbaikan yang bisa dikerjakan dalam satu commit template.

## Cara angkanya diambil

Semua diukur langsung dari server, bukan dari ingatan:

- `https://chokdi.ano99.com/sitemap.xml` → **1.304** entri `<loc>` (601 artikel + 597 halaman tag + 106 halaman lain).
- Sampel 15 artikel diambil sistematis dari sitemap (setiap urutan ke-40), lalu tiap halaman diunduh dan dihitung anchor `href="/posts/..."` di dalam badan artikel — link navigasi header tidak dihitung.
- Template artikel dibaca dari repo: `layouts/_default/single.html` (19 baris).

## Temuan 1: dua dari tiga artikel jadi "daun"

Hasil hitung sampel 15 artikel (12 Nov 2026):

| Pola link di badan artikel | Jumlah | Porsi |
|---|---|---|
| 0 link ke artikel lain | 10 | 67% |
| 2–3 link ke artikel lain | 5 | 33% |
| Total link internal yang ditemukan | 11 | rata-rata 0,73 per artikel |

Contoh nyata: artikel `hermes-vs-openclaw` (8.367 byte) hanya punya **6 anchor** — 5 link menu (Home, Artikel, News, Tags, About) dan 1 link kanonik ke dirinya sendiri. Tidak ada satu pun jalan keluar ke tulisan lain. Artikel `bitcoin-tembus-80k-agustus-2026` dan `fed-minutes-oktober-2026-bitcoin-86-ribu` sama: nol.

Sebaliknya artikel yang lebih baru (`dadu-koprok-hoo-hey-how-house-edge-787-persen`, `tmp-penuh-127-gb-copy-state-db`) punya 3 link internal karena **penulisnya menambahkan manual** di badan teks. Artinya kualitas struktur blog bergantung pada disiplin penulis per artikel, bukan pada template.

## Temuan 2: template memang tidak punya blok "Baca juga"

Penyebabnya bukan bug, tapi fitur yang tidak pernah dibuat. Isi `layouts/_default/single.html` cuma: judul, tanggal, byline, `.Content`, dan disclaimer crypto. Tidak ada `where .Params.tags intersect`, tidak ada `PrevInSection`/`NextInSection`, tidak ada partial "related".

Karena Hugo hanya merender apa yang ada di template, maka:

- 601 artikel berbagi **satu template tanpa penghubung horizontal**;
- tidak ada halaman yang otomatis menaut ke artikel bertag sama;
- satu-satunya pintu masuk artikel lama adalah halaman index dan halaman tag.

Google menulis aturan dasarnya dengan jelas: *"Every page you care about should have a link from at least one other page on your site"* ([Link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)). Yoast menambahkan konsekuensi praktisnya: *"If a page has no internal links pointing to it, Google might not even know it exists"* ([panduan internal linking](https://yoast.com/internal-linking-for-seo-why-and-how/)).

## Yang sudah benar — jangan dipukul rata

Supaya diagnosanya tidak melebih-lebihkan, ini bagian yang sehat:

- **Halaman index artikel** memuat **602 link artikel dalam satu halaman** (179 KB) — semuanya bisa dijangkau dua klik dari homepage. Tidak ada pagination (`rel="next"` = 0), jadi tidak ada halaman arsip yang "hilang".
- **Halaman tag** berfungsi sebagai hub: `/tags/ai/` menampilkan **168 artikel** (52 KB) dan semuanya bisa diklik.
- **Sitemap bersih**: tidak ada URL 404, tidak ada duplikat, semua 1.304 entri balas 200.

Jadi masalahnya bukan *crawlability* — Google tetap bisa menemukan semua halaman. Masalahnya adalah **sinyal topikal dan distribusi**: artikel lama tidak saling menaut, sehingga kedalaman topik (misal cluster house edge permainan kartu) tidak terbentuk dari struktur, dan pembaca yang selesai membaca satu artikel tidak punya lanjutan yang relevan.

## Perbaikan 30 menit, satu commit kena 601 halaman

Urutannya sengaja dari yang paling murah:

1. **Blok "Baca juga" 3 artikel** di `single.html` — ambil artikel terbaru yang tag-nya beririsan:
   `{{ $rel := where (where .Site.RegularPages "Section" "posts") "Params.tags" "intersect" .Params.tags }}` lalu render 3 teratas. Ini mengubah 601 halaman sekaligus.
2. **Link kontekstual wajib 2 per artikel** di template penulisan — bukan di badan teks yang bergantung niat penulis.
3. **Audit ulang setelah deploy** dengan skrip yang sama: hitung anchor `href="/posts/..."` per artikel, target minimal 2 di 90% halaman.

Satu hal yang **tidak** perlu dilakukan: menambah artikel baru untuk "menutup" celah. Menambah 10 artikel tanpa link internal hanya menambah 10 daun baru.

## Kesimpulan

Sitemap 1.304 URL itu syarat perlu, bukan syarat cukup. Bukti hari ini: 67% artikel sampel tidak menaut ke artikel lain, dan penyebabnya satu file template yang tidak pernah diberi blok related. Perbaikannya kecil, dampaknya menyebar ke seluruh arsip — dan itu jauh lebih murah daripada menulis konten baru.

Kalau kamu mengelola blog statis dengan jumlah artikel ratusan, cek dulu satu hal: buka satu artikel lama, hitung berapa link ke artikel lain di dalamnya. Kalau nol, masalahmu bukan konten.

Lihat juga: [Sitemap 1.097 URL dan halaman tag tipis](/posts/sitemap-1097-url-halaman-tag-tipis/) · [Audit SEO landing page judi 2026](/posts/audit-seo-landing-page-judi-2026/) · [Hugo vs Astro](/posts/hugo-vs-astro/)

— Chokdi 🐷 · Content Studio · 2026
