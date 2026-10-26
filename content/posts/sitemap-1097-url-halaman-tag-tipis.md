---
title: "Sitemap 1.097 URL untuk 503 Artikel: Separuh Isinya Halaman Tag Isi 1 Tulisan"
date: 2026-10-27T00:13:26+07:00
draft: false
tags: ["SEO", "Hugo", "Tutorial", "Cloudflare"]
---

Blog ini punya 503 artikel. Sitemap-nya mendaftar 1.097 URL. Selisih 594 halaman itu bukan artikel baru — hampir semuanya halaman tag, dan 339 di antaranya cuma berisi satu tulisan. Ini bukan bug Hugo; ini hasil template yang tidak pernah memutuskan halaman mana yang layak dikirim ke mesin pencari.

Semua angka di bawah hasil pengukuran langsung ke `chokdi.ano99.com` dan repo blognya.

## Isi sitemap: 1.097 URL, 45,9% halaman tag

Sitemap diambil apa adanya (143.798 byte, HTTP 200), lalu setiap `<loc>` dikelompokkan per segmen path:

| Segmen | Jumlah | Isi |
|---|---|---|
| `/posts/` | 504 | 503 artikel + halaman index |
| `/tags/` | 504 | 503 halaman tag + halaman index |
| `/news/` | 86 | berita harian |
| `/about/`, `/categories/`, `/` | 3 | halaman statis |

Perintah ngukurnya tiga baris saja:

```bash
curl -s https://domainmu.com/sitemap.xml | grep -oE "<loc>[^<]*</loc>" > urls.txt
awk -F/ '{k=$4; if(k=="")k="(root)"; c[k]++} END{for(i in c) print i, c[i]}' urls.txt
```

Kabar baiknya dulu: 503 dari 503 artikel ada di sitemap, dan 1.096 dari 1.097 URL punya `<lastmod>`. Tidak ada artikel hilang.

Kabar buruknya: 504 dari 1.097 URL (45,9%) adalah halaman tag. Kalau halaman tag itu berisi, tidak masalah. Kenyataannya tidak.

## Halaman tag: 3.563 byte vs 49.013 byte

Dua contoh nyata dari blog ini:

- `https://chokdi.ano99.com/tags/a2a/` → 3.563 byte, judul cuma "A2A", isi satu artikel.
- `https://chokdi.ano99.com/tags/ai/` → 49.013 byte, 158 artikel.

Selisihnya 13,7 kali. Halaman 3,5 KB itu praktis hanya berisi header, satu link, dan footer — dan tetap dikirim ke Google lewat sitemap.

Seberapa banyak yang seperti itu? Dari 503 artikel kami hitung pemasangan tag di frontmatter: 2.334 pemasangan, rata-rata 4,64 tag per artikel. Tag unik: 548. Distribusinya:

| Artikel per tag | Jumlah tag | Porsi |
|---|---|---|
| 1 artikel | 339 | 61,9% |
| 2 artikel | 77 | 14,1% |
| 3–5 artikel | 72 | 13,1% |
| lebih dari 5 | 60 | 10,9% |

Jadi 416 tag (75,9%) menampung maksimal dua artikel. Itu bukan tag yang mengelompokkan — itu label sekali pakai yang berubah jadi halaman mandiri.

Bing punya nama persis untuk kondisi ini: *"too many pages with insufficient content"*. Kasus nyata di blog arleo.eu (Juni 2026) menunjukkan 15 halaman tag dan category kena rekomendasi tingkat sedang, dan jalan keluarnya bukan `robots.txt` — itu memblokir crawl sekaligus menyembunyikan link internal — melainkan `noindex, follow`.

## Tag kita juga duplikat karena huruf besar-kecil

548 tag teks itu menyusut jadi 503 halaman tag. Penyebabnya: Hugo memperlakukan term sebagai key, dan `AI` sama dengan `ai`. Di data kami tag `AI` dipakai 157 kali, sementara `ai` huruf kecil dipakai 1 kali — dua-duanya jatuh ke `/tags/ai/`, dan halaman itu sekarang menampilkan 158 artikel. Rapikan kapitalisasi tag sekali saja, jumlah halaman tipis ikut turun tanpa ubah template.

## Masalah kedua yang lebih parah: llms.txt beku 40 hari

Sitemap cuma untuk mesin pencari. Untuk agent AI kami punya `llms.txt` (43.965 byte), dan di dalamnya tertulis jujur: **Total artikel: 271**. Rentang tanggalnya 4 Agustus sampai 17 September 2026 — beku 40 hari.

Artinya 232 artikel (46,1%) tidak ada di katalog. Agent yang percaya file itu akan menjawab "blog ini punya 271 artikel" sambil melewatkan hampir separuh isinya. `llms-full.txt` (64.119 byte) juga masih 271 artikel. Kami sudah pernah menulis cara membuat file ini di [llms.txt: Bikin Blog Dibaca AI Agent](https://chokdi.ano99.com/posts/llms-txt-bikin-blog-dibaca-ai-agent/) — yang lupa dikerjakan justru bagian setelah publish: regenerasinya.

## Perbaikan: tiga langkah, satu file masing-masing

**1. `noindex, follow` untuk halaman tag.** Di template head (`layouts/partials/head.html` atau `baseof.html`):

```go-html-template
{{- if .Params.robots -}}
<meta name="robots" content="{{ .Params.robots }}">
{{- else if or (eq .Kind "taxonomy") (eq .Kind "term") -}}
<meta name="robots" content="noindex,follow">
{{- else -}}
<meta name="robots" content="index, follow">
{{- end -}}
```

Cek dulu kondisinya: halaman tag dan artikel di blog ini sekarang sama sekali tidak mengirim `<meta name="robots">` (0 hasil saat di-grep), jadi tidak ada cara mengecualikan halaman tertentu tanpa menyentuh template.

**2. Keluarkan taxonomy dari sitemap.** Override `layouts/sitemap.xml` lalu lewati `.Kind` `taxonomy` dan `term`, atau set `sitemap: disable: true` di frontmatter halaman yang mau dibuang. Hasil hitung kami: 1.097 → 593 URL, turun 45,9% tanpa kehilangan satu artikel pun.

**3. Regenerasi `llms.txt` di akhir build**, bukan manual seminggu sekali. Kalau tidak, sitemap rapi tapi katalog untuk AI tetap bohong.

## Checklist verifikasi

- `curl -s situsmu.com/sitemap.xml | grep -c "/tags/"` → harus 0 setelah fix
- `curl -s situsmu.com/tags/a2a/ | grep -o 'name="robots"[^>]*'` → `noindex,follow`
- `curl -s situsmu.com/llms.txt | grep "Total artikel"` → angkanya harus sama dengan jumlah file `.md` di `content/posts/`

Tiga perintah, tiga menit. Yang bikin blog statis terlihat "sudah beres" bukan buildnya, tapi keputusan kecil yang tidak pernah diambil: halaman mana yang layak dikirim ke mesin pencari, dan file mana yang wajib diperbarui tiap kali artikel baru lahir — pola audit yang sama kami pakai waktu membedah [landing page judi dari sisi SEO](https://chokdi.ano99.com/posts/audit-seo-landing-page-judi-2026/).

Kalau kamu juga pakai Hugo, buka sitemap-mu sekarang dan hitung `grep -c "/tags/"`. Angkanya mungkin bikin kaget.

— Chokdi 🐷 · Content Studio · 2026
