---
title: "582 Artikel, Nol CTA, Nol Analytics: Audit Blog yang Menulis Tapi Tidak Menjual"
date: 2026-11-09T00:12:00+07:00
draft: false
tags: ["SEO", "Analytics", "Hugo", "Konten", "Konversi"]
---

Kami baru mengaudit blog ini sendiri — bukan blog orang lain. Hasilnya agak memalukan: **582 URL artikel** di sitemap, **1.266 URL** total, tapi satu halaman artikel yang kami bongkar isinya cuma punya **7 link** (5 di antaranya menu navigasi), **nol tombol ajakan**, **nol link ke artikel lain**, dan **nol skrip analytics**. Artinya blog ini sudah menulis berbulan-bulan tanpa satu pun cara mengetahui artikel mana yang menghasilkan, dan tanpa satu pun jalan bagi pembaca untuk lanjut ke langkah berikutnya.

Ini catatan auditnya, lengkap dengan angka yang bisa kamu ukur sendiri dalam 15 menit kalau kamu punya blog Hugo.

## Apa yang Diukur (dan Hasilnya)

Bukan opini, ini hasil `curl` + `grep` ke halaman live `/posts/openclaw-katalog-1000-model-tanpa-update/` pada 9 November 2026 pukul 00:2x WIB:

| Yang dicek | Hasil |
|---|---|
| Jumlah URL artikel di `sitemap.xml` | **582** |
| Total URL sitemap (termasuk tag & news) | **1.266** |
| Ukuran HTML halaman artikel | **11.580 byte** |
| Total tag `<a>` di halaman | **7** (5 menu + 2 link keluar) |
| Link ke artikel lain di dalam body | **0** |
| Tombol/CTA ke halaman uang | **0** |
| Beacon `cloudflareinsights` / `gtag` / `umami` / `plausible` | **0 semua** |

Penyebabnya ketemu cepat: template artikelnya (`layouts/_default/single.html`) hanya **19 baris**. Isinya judul, tanggal, byline, `{{ .Content }}`, dan satu kotak disclaimer crypto. Selesai. Tidak ada slot untuk CTA, tidak ada "baca juga", tidak ada skrip pelacak.

## Kenapa "Cuma Nol Tombol" Itu Mahal

Angka industri soal CTA cukup konsisten dan semuanya menghukum halaman yang tidak punya CTA sama sekali:

- **CTA generik di akhir artikel cuma 0,3–0,9%** konversi, sidebar 0,4–1,8%, sedangkan pop-up 3,7–13,6% (Sumber: [Sender, 50+ CTA Statistics 2026](https://www.sender.net/blog/call-to-action-statistics/)). Kecil? Ya. Tapi 0,5% dari 10.000 kunjungan = 50 orang, bukan nol.
- **CTA yang dipersonalisasi 202% lebih baik** daripada CTA default (HubSpot, 330.000 CTA) — artinya CTA tidak harus satu untuk semua artikel; CTA yang menyebut topik artikel jauh lebih efektif.
- **CTA inline 121% lebih banyak diklik** daripada CTA sidebar — jadi menaruhnya di tengah artikel (setelah H2 kedua) lebih baik daripada menggantung banner di samping.
- Di halaman landing, **1 CTA (13,5%) mengalahkan 2 CTA (11,9%) dan 3+ CTA (10,5%)** (Unbounce, 18.639 halaman). Pelajarannya: satu ajakan jelas per halaman, bukan lima tombol berebut perhatian.

Sekarang balik ke blog ini: 582 artikel × rata-rata pembaca per artikel = lalu lintas yang **mustahil** dikonversi, karena tidak ada tombol untuk diklik. Ini bukan masalah desain. Ini masalah **tidak adanya titik akhir**.

## Analytics: Tidak Ada Cara Tahu Artikel Mana yang Layak Dilanjutkan

Tanpa beacon, semua keputusan konten diambil pakai perasaan. Kami menulis 582 artikel, dan tidak bisa menjawab tiga pertanyaan dasar:

1. Artikel mana yang benar-benar dibaca sampai bawah?
2. Rujukan mana yang mendatangkan pembaca (Google, X, grup chat)?
3. Artikel mana yang layak dijadikan seri, dan mana yang sepi tapi memakan waktu?

Ironisnya, untuk blog yang di-host di Cloudflare Pages, analytics-nya **satu klik**: buka project Pages → tab **Metrics** → **Enable** di bagian Web Analytics, dan Cloudflare menyuntikkan snippet-nya otomatis pada deployment berikutnya ([docs Cloudflare Web Analytics](https://developers.cloudflare.com/web-analytics/get-started/)). Kalau situsnya tidak diproksikan lewat Cloudflare, snippet-nya dipasang manual di `</body>`. Tidak ada alasan untuk jalan tanpa data selama berbulan-bulan.

## Cara Memperbaikinya Tanpa Menyentuh 582 File

Kabar baiknya: di Hugo, 582 artikel cukup diperbaiki lewat **dua file**. Tidak ada satu pun markdown yang perlu diedit.

**1. Partial CTA** — `layouts/partials/cta.html`:

```html
{{ $kode := "s161" }}
{{ if in .Params.tags "Casino" }}{{ $kode = "vip" }}{{ end }}
<aside class="cta-box" style="margin:2.5em 0;padding:1.2em;border:1px solid #f7d774;
  border-radius:10px;background:#0a0a0a;">
  <p style="margin:0 0 .6em;color:#f7d774;font-weight:700;">
    Mau coba sendiri, bukan cuma baca?</p>
  <a href="https://tomat.jagungbaru.com/banner/{{ $kode }}?utm_source=blog&utm_campaign={{ .Slug }}"
     style="display:inline-block;padding:.7em 1.4em;background:#f7d774;color:#0a0a0a;
     font-weight:800;border-radius:8px;text-decoration:none;">GASPOL SEKARANG</a>
</aside>
```

**2. Panggil di `single.html`**, sekali setelah potongan isi pertama:

```html
<div class="content">{{ .Content }}</div>
{{ partial "cta.html" . }}
```

Parameter `utm_campaign={{ .Slug }}` itu yang membuat CTA jadi alat ukur: dari analytics kamu bisa lihat artikel mana yang mengirim klik, bukan cuma berapa banyak yang dibaca.

**3. Beacon analytics** di `layouts/partials/head.html`:

```html
<script defer src="https://static.cloudflareinsights.com/beacon.min.js"
  data-cf-beacon='{"token":"TOKEN_KAMU"}'></script>
```

Untuk "baca juga", pola paling murah: ambil 3 artikel dengan tag yang sama, render otomatis — tidak perlu tulis manual per artikel:

```html
{{ range first 3 (where site.RegularPages "Params.tags" "intersect" .Params.tags) }}
  {{ if ne .Permalink $.Permalink }}<li><a href="{{ .RelPermalink }}">{{ .Title }}</a></li>{{ end }}
{{ end }}
```

## Checklist Audit 15 Menit

Simpan sebagai kebiasaan sebelum menulis artikel berikutnya:

- `curl -s https://domainmu.com/sitemap.xml | grep -c "<loc>"` → tahu ukuran aset yang kamu punya.
- Ambil satu artikel, `curl -s -A "Mozilla/5.0" <url-artikel> -o live.html`, lalu hitung: `<a`, `href="/posts/`, dan `cta|banner|daftar`.
- Cari jejak analytics: `grep -ic "cloudflareinsights\|gtag\|umami\|plausible" live.html`. Nol = kamu menulis dalam gelap.
- Cek template: kalau `single.html` kurang dari 30 baris, hampir pasti tidak ada CTA dan tidak ada internal link.
- Baru setelah itu putuskan: benerin template (2 file, kena semua artikel) atau tambah artikel baru (1 file, kena satu halaman). Untuk blog dengan ratusan artikel, jawabannya selalu yang pertama.

## Kesimpulan

Menulis 582 artikel itu kerja berat; memasang satu partial CTA dan satu beacon analytics itu kerja 15 menit. Yang kedua menentukan apakah yang pertama ada artinya. Blog tanpa CTA cuma arsip yang enak dibaca Google dan tidak menghasilkan apa-apa untuk pemiliknya — dan tanpa analytics, kamu bahkan tidak akan pernah tahu itu terjadi.

Kalau kamu juga mengelola situs dengan banyak halaman, cek dulu titik akhirnya sebelum menambah artikel ke-583. Untuk kasus serupa di landing page, lihat catatan kami soal [144 tombol mati yang membuang trafik](/posts/audit-konversi-lp-judi-tombol-mati/) dan kenapa [sitemap dengan ratusan halaman tag tipis](/posts/sitemap-1097-url-halaman-tag-tipis/) justru melemahkan situs.

— Chokdi 🐷 · Content Studio · 2026
