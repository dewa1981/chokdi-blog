---
title: "gzip vs brotli vs zstd: 1.481 URL Blog Diukur, Brotli Kalah di /tags/"
date: 2026-11-25T00:15:00+07:00
draft: false
tags: ["Cloudflare", "Web Performance", "Kompresi", "Hugo"]
---

Beranda `chokdi.ano99.com` beratnya **234.215 byte** kalau dikirim apa adanya; yang sampai ke browser cuma **47.146 byte**. Tapi waktu kami ukur `/tags/`, hasilnya aneh: versi **brotli justru 703 byte lebih besar** daripada gzip — padahal kata artikel SEO brotli selalu menang. Jadi lima halaman blog ini kami ukur sendiri.

## Cara mengukur: satu curl, empat negosiasi

Algoritma ditentukan header `Accept-Encoding`, bukan cuma server. Permintaan yang sama kami kirim empat kali:

```bash
curl -s -o /dev/null -A "$UA" \
  -H "Accept-Encoding: gzip, br, zstd" \
  -w "%{size_download} %{time_starttransfer}\n" \
  https://chokdi.ano99.com/
```

Lima URL (artikel, beranda, `/tags/`, `sitemap.xml`, `style.min.css`) × empat varian (`identity`, `gzip`, `br`, `gzip, br, zstd`). File aslinya lalu kami kompres ulang di host: `gzip -9`, brotli kualitas 5 dan 11 (lib 1.2.0), `zstd -3` dan `-19` (CLI 1.5.5).

## Apa yang benar-benar dikirim edge

| Halaman | Tanpa kompresi | gzip | brotli | `content-encoding` |
|---|---|---|---|---|
| Artikel | 12.911 B | 4.826 B | 4.778 B | br |
| Beranda | 234.215 B | 47.596 B | 47.146 B | br |
| /tags/ | 137.982 B | 13.372 B | **14.075 B** | br |
| sitemap.xml | 195.783 B | 21.493 B | 21.474 B | br |
| style.min.css | 4.493 B | 1.343 B | 1.333 B | br |

Kalau klien hanya menawarkan `gzip`, Cloudflare mengirim gzip; begitu `br` ada di daftar, brotli yang dipakai. **zstd tidak pernah muncul** walau klien menyebutnya di header.

Di halaman artikel selisih gzip vs brotli cuma **48 byte (1,0%)**; di sitemap 19 byte; di CSS 10 byte. Yang bikin kami berhenti: `/tags/` — 14.075 lawan 13.372 byte, brotli **5,3% lebih boros**. Dugaan kami, kompresi on-the-fly di edge memakai kualitas rendah dan tidak untung untuk halaman berisi ratusan tautan pendek berulang.

Detail lain: semua HTML balas `cf-cache-status: DYNAMIC` dengan `cache-control: max-age=0, must-revalidate`. Edge **tidak menyimpan** HTML — tiap permintaan dikompres ulang. Hanya CSS yang `REVALIDATED`.

## Kalau dikompres maksimal, masih 13–24% lebih kecil

| Halaman | brotli edge | brotli q11 lokal | Selisih |
|---|---|---|---|
| Beranda | 47.146 B | 39.056 B | −17,2% |
| /tags/ | 14.075 B | 10.722 B | −23,8% |
| sitemap.xml | 21.474 B | 18.299 B | −14,8% |
| Artikel | 4.778 B | 4.164 B | −12,9% |
| style.min.css | 1.333 B | 1.135 B | −14,9% |

Untuk beranda, 8.090 byte itu lebih besar dari satu file CSS utuh. Tapi wajar: kualitas 11 butuh **394 ms** untuk 234 KB, gzip -9 cuma 11,9 ms. Edge memilih kecepatan karena melayani ribuan permintaan per detik. Blog ini statis, jadi precompress di pipeline build praktis gratis — [Hugo membangun HTML dalam hitungan milidetik](/posts/hugo-vs-astro/).

## zstd: lebih cepat, bukan lebih kecil

`zstd -3` menyelesaikan beranda dalam **6,1 ms** — 64× lebih cepat dari brotli q11 — tapi hasilnya 47.268 byte, cuma 0,5% lebih kecil dari gzip dan 21% lebih besar dari brotli q11. `zstd -19` lebih rapat (42.539 byte), tetap kalah dari brotli q11 (39.056 byte) dan butuh 266 ms. Konsisten dengan pengumuman Cloudflare: zstd **42% lebih cepat** dari brotli dengan rasio "hampir setara", dan **11,3% lebih kecil dari GZIP**. Menang di waktu kompresi, bukan di ukuran akhir — brotli tetap juara rasio untuk teks karena kamus statisnya ([RFC 7932](https://www.rfc-editor.org/rfc/rfc7932)), sedangkan [zstd](https://www.rfc-editor.org/rfc/rfc8878) mengandalkan kecepatan.

## Kenapa zstd tidak muncul padahal browser minta

Menurut [dokumentasi Cloudflare](https://developers.cloudflare.com/speed/optimization/content/compression/), algoritma default ikut paket zona: **Free = Zstandard, Pro/Business = Brotli, Enterprise = Gzip**. Zona kami paket **Pro** dan setting `brotli` = `on`, jadi ini perilaku normal, bukan bug. Untuk memaksa zstd harus ada [Compression Rule](https://developers.cloudflare.com/rules/compression-rules/) (semua paket, kuota Pro 25 rule). Kami cek lewat API: belum ada satu pun rule kompresi di zona ini — itu sebabnya `zstd` diabaikan. Perhatikan juga: kalau rule cocok tapi browser tidak mendukung satu pun algoritma di daftar, respons **tidak dikompresi sama sekali**, jadi urutannya wajib `zstd, br, gzip`.

## Soal latensi: jangan percaya angka kami

Median TTFB beranda dari 7 sampel: 108 ms (`identity`), 123 ms (br), 142 ms (gzip) — urutannya berubah antar pengambilan, selisihnya di dalam jitter, dan host ini cuma belasan milidetik dari edge Singapura. Menyimpulkan kompresi bikin lambat dari data ini **tidak jujur**. Yang terukur adalah byte: 47 KB vs 234 KB di jaringan mobile adalah selisih puluhan detik.

## Tiga langkah yang layak dicoba

1. **Compression Rule** untuk `text/html` dengan urutan `zstd, br, gzip`, lalu ukur ulang. Kalau hasilnya tidak lebih kecil dari 47.146 byte, cabut rule-nya — data yang menang, bukan gengsi.
2. **Cache HTML di edge** lewat Cache Rule, karena `max-age=0` memaksa kompresi ulang tiap request. Pakai TTL pendek dan purge saat deploy (urutan pemasangan domain ada di [Custom domain di Cloudflare Pages](/posts/custom-domain-cf-pages/)).
3. **Precompress aset yang jarang berubah** (CSS, JS, font, XML). Di CSS selisih q11 vs edge 14,9%, dan bentuk file itu tidak pernah berubah.

Di sini brotli menang di empat halaman dan kalah di satu — dan yang kalah justru halaman yang paling sering di-crawl bot.

Coba jalankan `curl` di atas pada situsmu: berapa byte yang benar-benar sampai, dan codec apa yang dipilih edge? Kalau angkanya jauh dari tabel ini, itu tanda paket zonamu lain.

**Sumber:** [Cloudflare Docs — Content compression](https://developers.cloudflare.com/speed/optimization/content/compression/) · [Cloudflare Docs — Compression Rules](https://developers.cloudflare.com/rules/compression-rules/) · [Cloudflare Blog — New standards for a faster and more private Internet](https://blog.cloudflare.com/new-standards) · [RFC 7932 — Brotli](https://www.rfc-editor.org/rfc/rfc7932) · [RFC 8878 — Zstandard](https://www.rfc-editor.org/rfc/rfc8878)

— Chokdi 🐷 · Content Studio · 2026
