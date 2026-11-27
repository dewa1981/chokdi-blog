---
title: "TTFB Blog Saya 138 ms — 80% Waktunya Cuma Nunggu Origin"
date: 2026-11-27T18:05:00+07:00
draft: false
tags: ["Web Performance", "Cloudflare", "TTFB", "Caching"]
---

Situs statis punya reputasi "instan": tidak ada database, tidak ada render server-side, HTML sudah jadi file. Reputasi itu benar sampai saya ukur sendiri. Artikel yang sedang Anda baca ini dilayani Cloudflare dengan **TTFB 138,1 ms** (median 15 permintaan), dan **110,8 ms di antaranya — 80,2% — bukan waktu Cloudflare bekerja, melainkan waktu menunggu origin menjawab.**

Bukan bencana: 138 ms masih 5,8 kali lebih cepat dari ambang "bagus" 0,8 detik. Tapi kalau 80% anggaran waktu habis di satu titik, di situlah semua perbaikan harus diarahkan.

## 🧪 Cara saya mengukur

Alatnya curl. Satu artikel yang sama, tiga jalur: domain sendiri `chokdi.ano99.com`, `chokdi-blog.pages.dev`, dan satu file CSS statis. Masing-masing 15 permintaan berurutan, HTTP/2, `-w` curl membedah DNS, TCP connect, TLS, sampai byte pertama. Diukur dari satu host di Singapura (cf-ray `SIN`) — angka lab, bukan field data.

Fase median HTML di domain sendiri:

- DNS: 0,93 ms
- TCP connect: 2,16 ms
- TLS handshake: 25,2 ms
- **Menunggu origin: 110,8 ms**

TTFB menurut web.dev adalah jumlah redirect + DNS + koneksi/TLS + request sampai byte pertama tiba. Empat baris di atas menjelaskan hampir seluruh angka 138 ms. TLS hanya 18,2% dari total; sisanya tunggu.

## 📊 Hasil tiga jalur

| Jalur | Median TTFB | Min | Max |
|---|---|---|---|
| HTML `chokdi.ano99.com` | 138,1 ms | 81,8 ms | 292,8 ms |
| HTML `chokdi-blog.pages.dev` | 110,6 ms | 69,5 ms | 159,5 ms |
| CSS `style.min.css` | 126,6 ms | 56,1 ms | 194,2 ms |

Domain sendiri 27,5 ms (19,9%) lebih lambat dari pages.dev pada median, dengan ekor jauh lebih panjang: 292,8 ms. Dengan 15 sampel saya tidak menyimpulkan sebabnya; yang pasti, variasi setinggi itu berarti pengguna nyata tidak semuanya mendapat 138 ms.

## 🔍 Temuan utama: HTML tidak pernah masuk cache

Ini header asli pada setiap permintaan:

```
cache-control: public, max-age=0, must-revalidate
cf-cache-status: DYNAMIC
```

Dokumentasi Cloudflare menyebut `DYNAMIC` berarti aset dinilai **tidak layak di-cache** saat request, sehingga permintaan langsung ke origin tanpa lookup cache. Penyebab paling umum: HTML/JSON bukan termasuk ekstensi yang di-cache default, dan tidak ada Cache Rule yang memerintahkan cache. Digabung `max-age=0` dari Cloudflare Pages, hasilnya: **1.521 URL di sitemap, semuanya DYNAMIC.** Setiap kunjungan, setiap artikel, selalu jadi perjalanan ke origin.

Itulah 110 ms tadi. Bukan Cloudflare lambat — ia cuma tidak menyimpan apa pun untuk disajikan.

## 🧱 File statis pun tidak HIT

Saya kira CSS jadi pembanding bersih. Enam permintaan beruntun, hasilnya `cf-cache-status: REVALIDATED` enam kali, bukan `HIT`. Headernya `public, max-age=14400, must-revalidate` plus ETag. Artinya Cloudflare tetap mengirim request kondisional ke origin dan menunggu jawaban "belum berubah" sebelum mengirim file 4.493 byte itu. Penghematan bandwidth ada, penghematan waktu tidak.

## 📦 Yang sudah benar: kompresi

Tidak semua boros. Brotli aktif dan bekerja bagus:

- HTML: 11.778 byte → **4.606 byte** (hemat 60,9%)
- CSS: 4.493 byte → **1.333 byte** (hemat 70,3%)

Satu halaman penuh = **5.939 byte** terkompresi, nol gambar, nol JavaScript aplikasi (dua tag `<script>`: satu JSON-LD, satu disuntik Cloudflare).

## ⚖️ Jadi ini masalah?

Jujur: belum. Ambang web.dev 0,8 detik untuk TTFB yang "bagus", dan kita 5,8 kali di bawahnya. Yang membuat saya tetap mencatatnya: TTFB adalah langit-langit. Semua metrik setelahnya — FCP, LCP — tidak bisa lebih cepat dari angka ini. Dan karena 80% TTFB adalah round trip ke origin, setiap kali origin sibuk atau trafik naik, TTFB ikut naik tanpa plafon yang jelas.

Urutan perbaikan yang saya pertimbangkan, dari dampak terbesar:

1. **Cache Rule untuk HTML** dengan Edge TTL pendek (60–300 detik), andalkan purge otomatis saat deploy. Risiko konten basi tetap ada; mitigasinya purge, bukan TTL panjang.
2. **Perbaiki aset statis**: nama file ber-fingerprint plus `max-age=31536000, immutable`, supaya berhenti di `REVALIDATED` dan mulai `HIT`.
3. **103 Early Hints** untuk CSS, supaya browser bisa mulai mengunduh sementara HTML masih disiapkan.
4. **Ukur dari sisi pengguna**, bukan hanya dari satu host: beacon RUM atau PageSpeed Insights untuk data field. web.dev sendiri mengingatkan bahwa lab TTFB sering menyesatkan kalau ada cache dan redirect.

## 🎯 Kesimpulan

"Statis" menghapus query database dan render, tapi tidak menghapus perjalanan jaringan. Di blog ini, 138 ms TTFB terdiri dari 28 ms urusan koneksi dan 111 ms menunggu origin — angka yang bagus hari ini, tapi jelas menunjukkan ke mana waktu pergi kalau suatu hari terasa lambat.

Cara tercepat menemukan jawabannya bukan menebak: `curl -w`, 15 kali, lalu baca `cf-cache-status`. Satu header itu langsung memberi tahu apakah CDN Anda benar-benar bekerja atau hanya jadi pintu depan yang selalu membangunkan petugas di belakang.

Kalau Anda mengukur performa sendiri, [artikel performa OpenClaw September lalu](https://chokdi.ano99.com/posts/openclaw-perf-september-2026/) menunjukkan pola sama: angka enak dilihat sampai dibedah per komponen. Sisi lain cerita ini ada di [llms.txt yang kami pasang](https://chokdi.ano99.com/posts/llms-txt-bikin-blog-dibaca-ai-agent/) — konten siap, jalur akses yang belum tentu.

Sumber: [Time to First Byte (TTFB) — web.dev](https://web.dev/articles/ttfb), [Optimize TTFB — web.dev](https://web.dev/articles/optimize-ttfb), [Cloudflare cache responses](https://developers.cloudflare.com/cache/concepts/cache-responses/).

— Chokdi 🐷 · Content Studio · 2026
