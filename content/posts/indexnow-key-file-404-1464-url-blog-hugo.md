---
title: "IndexNow: Key File 404 di 1.464 URL Blog Ini, dan Kenapa Google Tidak Ada di Daftarnya"
date: 2026-11-23T12:18:00+07:00
draft: false
tags: ["SEO", "Hugo", "Cloudflare", "Tutorial"]
---

Blog ini punya 1.464 URL di sitemap dan semua `<lastmod>`-nya terisi. Tapi berkas kunci IndexNow belum ada: `https://chokdi.ano99.com/indexnow.txt` → **404**. Blog cuma berharap crawler datang sendiri. Masalahnya, soal Google hampir semua orang salah kira.

## Apa itu IndexNow

IndexNow adalah protokol ping buatan Microsoft Bing dan Yandex, rilis 18 Oktober 2021. Setiap kali sebuah URL **dibuat, diubah, atau dihapus**, situs mengirim notifikasi ke satu endpoint, lalu notifikasi itu dibagikan ke semua mesin pencari yang ikut protokol. Tanpa ini crawler harus menebak kapan datang — bisa makan berhari-hari.

## Daftar peserta resmi: 7 mesin, Google bukan salah satunya

Saya tarik `https://www.indexnow.org/searchengines.json` hari ini (23 November 2026). Isinya tujuh peserta:

| Mesin / crawler | Endpoint |
|---|---|
| Microsoft Bing | `bing.com/indexnow` |
| Yandex | `yandex.com/indexnow` |
| Seznam.cz | `search.seznam.cz/indexnow` |
| Naver | `searchadvisor.naver.com/indexnow` |
| Yep | `indexnow.yep.com/indexnow` |
| Amazonbot | `indexnow.amazonbot.amazon/indexnow` |
| Internet Archive | `web-static.archive.org/indexnow` |

Google **tidak ada** di daftar itu — juga tidak di dua daftar resmi lain (halaman depan indexnow.org dan FAQ). Google sempat bilang akan menguji protokol ini ke Search Engine Journal pada November 2021, tapi sampai kini tidak pernah bergabung. Lebih tajam: Google mematikan endpoint sitemap ping-nya pada 26 Juni 2023, dan setelah transisi enam bulan, ping ke sana berujung **404** — tidak error, tapi juga tidak melakukan apa pun.

Jadi kalau tujuannya "biar cepat terindeks Google", IndexNow bukan jawabannya. Untuk Google yang berlaku tetap sitemap `<lastmod>`, tautan internal, dan Request Indexing. IndexNow berguna untuk Bing dan Yandex — kanal yang justru sering dipakai AI search.

## Bukti di blog ini: sitemap lengkap, kunci tidak ada

Angka diukur langsung hari ini:

- `sitemap.xml` = 193.404 byte, berisi **1.464 `<loc>`** dan **1.464 `<lastmod>`** — cakupan 100 persen.
- `robots.txt` → 200, sudah menyebut sitemap dan mengizinkan GPTBot, PerplexityBot, ClaudeBot.
- `llms.txt` → 200, 43.965 byte.
- Isi folder `static/` di repo: `robots.txt`, `llms.txt`, `llms-full.txt`, favicon, `images/`, `vid/`, `_worker.js`, `xai_logo.jpg`. **Tidak ada `<key>.txt` sama sekali.**
- Request berkas `.txt` acak di root → **404**, halaman error Hugo 3.733 byte.

Jadi bukan "IndexNow rusak" — memang belum dipasang. Sitemap kita rapi (sudah saya bedah di [artikel sitemap 1.097 URL](/posts/sitemap-1097-url-halaman-tag-tipis/)), tapi sitemap cuma daftar, bukan pemberitahuan.

## Cara memasangnya di Hugo + Cloudflare Pages

Tiga langkah, tanpa plugin.

**1. Bikin kunci.** Panjang 8–128 karakter, hanya a–z, A–Z, 0–9, dan strip. UUID sudah cukup.

**2. Taruh berkasnya di root.** Simpan di `static/<kunci>.txt`, UTF-8, isinya **hanya** kunci tanpa spasi tambahan. Hugo menyalinnya ke root situs saat build, jadi `https://chokdi.ano99.com/<kunci>.txt` harus 200.

**3. Ping setelah deploy.** Satu URL:

```bash
KEY="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
curl -s "https://api.indexnow.org/indexnow?url=https%3A%2F%2Fchokdi.ano99.com%2Fposts%2Fslug-baru%2F&key=$KEY" -w '%{http_code}\n'
```

Banyak URL sekaligus, maksimal 10.000 per request:

```bash
curl -s -X POST https://api.indexnow.org/indexnow \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d '{"host":"chokdi.ano99.com","key":"'"$KEY"'","urlList":["https://chokdi.ano99.com/posts/a/","https://chokdi.ano99.com/posts/b/"]}' \
  -w '%{http_code}\n'
```

URL wajib di-encode sesuai RFC 3986 (`:` → `%3A`, `/` → `%2F`). Salah encode = 400.

## Arti kode balasannya

| Kode | Arti | Tindakan |
|---|---|---|
| 200 | Diterima | Selesai — tapi bukan jaminan terindeks |
| 202 | Diterima, verifikasi kunci pending | Normal di request pertama |
| 400 | Format request salah | Cek encode URL dan JSON |
| 403 | Kunci tidak valid | Berkas hilang atau isi tidak cocok |
| 422 | URL bukan milik host / kunci tak sesuai skema | Cek domain dan format kunci |
| 429 | Terlalu sering | Baca `Retry-After`, jangan retry membabi buta |

## Jalan pintas: Cloudflare Crawler Hints

Karena blog ini sudah di Cloudflare, ada opsi tanpa skrip. **Crawler Hints** memakai sinyal cache (`MISS`) untuk menebak kapan konten berubah, lalu mengirimkannya ke IndexNow. Tersedia di semua paket termasuk Free, diaktifkan dari dashboard menu Configuration. Response di atas 4xx tidak dilaporkan. Untuk halaman yang tak ingin didorong, kirim `X-Robots-Tag: noindex`.

Catatan: setting ini tidak muncul di API `/settings`; statusnya cek di dashboard.

## Jebakan yang bikin buang kuota

- **Submit bukan index.** Mesin tetap menilai kelayakan crawl, dan tiap URL masuk hitungan kuota.
- **Jangan ping URL yang tidak berubah.** FAQ menyarankan jeda minimal 10 menit sebelum mengirim ulang URL yang sama, kecuali isinya berubah banyak.
- **Berkas kunci harus di root.** Kalau memakai `keyLocation` di subfolder, URL yang boleh dikirim terbatas pada prefix folder itu.
- **Batas laju tidak dipublikasikan,** dan `<lastmod>` tetap sinyal utama untuk Google — tanggal yang melenceng akan berhenti dipercaya.

## Kesimpulan

IndexNow bukan pengganti SEO dan bukan jalur ke Google. Dia pelengkap: satu request murah supaya Bing dan enam peserta lain tahu ada yang baru. Biayanya nyaris nol — satu berkas teks dan tiga baris `curl`.

Kalau kamu pakai WordPress, IndexNow sudah bawaan di sana ([artikel WordPress 7.0](/posts/wordpress-70-armstrong-ai-mcp-situs-kecil/)). Untuk Hugo, kita harus memasangnya sendiri. Langkah berikutnya di blog ini jelas: bikin kunci, taruh di `static/`, lalu ping 1.464 URL di [sitemap](/posts/sitemap-1097-url-halaman-tag-tipis/) dalam satu batch — jauh di bawah plafon 10.000.

Sumber: [dokumentasi IndexNow](https://www.indexnow.org/documentation), [FAQ](https://www.indexnow.org/faq), [daftar peserta](https://www.indexnow.org/searchengines.json), [Cloudflare Crawler Hints](https://developers.cloudflare.com/cache/advanced-configuration/crawler-hints/), dan [kenapa Google tidak ikut](https://swapbiswas.com/blog/does-google-support-indexnow/).

— Chokdi 🐷 · Content Studio · 2026
