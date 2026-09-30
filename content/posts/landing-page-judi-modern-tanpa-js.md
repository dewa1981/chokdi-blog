---
title: "Landing Page Judi Modern: Container Query, Popover API, dan Cuma 8 Baris JavaScript"
date: 2026-10-01T00:15:00+07:00
draft: false
tags: ["Landing Page", "CSS", "Frontend", "Web Modern"]
---

Landing page judi itu tugasnya cuma satu: bikin orang klik tombol daftar. Tapi banyak LP justru
membebani HP pengunjung dengan framework 100 KB yang harus selesai di-download **dulu** sebelum
tombolnya bisa diklik. Hari ini kami bikin varian LP SLOT161 pakai panduan **Modern Web Guidance**
dari Chrome — hasilnya logika UI **nol JavaScript**, dan total JS di halaman cuma **8 baris
polyfill**. Ini catatan lengkapnya, termasuk empat jebakan yang kami kena.

## Kenapa kami tinggalkan cara "framework dulu"

Untuk LP satu halaman, React/Vue bukan cuma berlebihan — dia menambah waktu tunggu tepat di detik
paling mahal. Browser sekarang sudah punya fitur bawaan yang dulu wajib ditulis manual pakai JS:
popover, dialog, animasi masuk, sampai komponen yang menyesuaikan diri ke lebar wadahnya. Kalau
bisa deklaratif di HTML/CSS, kenapa harus lewat runtime?

Hasil eksperimen: `slot161_modern.html`, **20 KB** total, satu file, tanpa dependency runtime.

## Enam fitur platform yang benar-benar dipakai

| Fitur | Dipakai untuk | Efek nyata |
|---|---|---|
| **Container Query** (`@container` + `container-type`) | kartu bonus + tabel pembayaran | Komponen adaptif ke lebar **dirinya**, bukan lebar layar — bisa dipindah ke sidebar/main tanpa nulis media query baru |
| **Popover API + Invoker Commands** (`commandfor`/`command`) | popup bonus | Nol baris JS; browser yang urus fokus, tombol Esc, dan top-layer |
| **`@starting-style`** | animasi masuk elemen | Animasi saat elemen pertama dirender, tanpa JS/Animation API |
| **`scrollbar-color`/`scrollbar-width`** | scrollbar | Scrollbar ikut tema brand lewat CSS variable |
| **`text-wrap: balance/pretty` + `:has()`** | judul & FAQ | Judul tak ada baris menggantung; parent FAQ di-style tanpa JS |

Angka nyata di file itu: atribut `popover` muncul **22×**, `commandfor` **6×**, `@starting-style`
**5×**, `@container` **3×**, `text-wrap` **4×**, `:has()` **3×**, `scrollbar-color` **2×**.

Satu catatan jujur: `fetchpriority` sudah masuk daftar siap pakai, tapi **belum dipakai** di varian
ini karena tidak ada gambar hero. Kalau nanti ada gambar LCP, jangan pasang `loading="lazy"` di
situ — itu justru menunda gambar terpenting.

## Isi 8 baris JavaScript-nya apa?

Bukan logika UI. Isinya cuma **polyfill kondisional**:

```js
if (!('commandForElement' in HTMLButtonElement.prototype)) {
  import('https://esm.run/invokers-polyfill').catch(()=>{});
}
if (!('popover' in HTMLElement.prototype)) {
  import('https://unpkg.com/@oddbird/popover-polyfill@latest/dist/popover.min.js').catch(()=>{});
}
```

Sembilan dari sepuluh pengunjung tidak pernah men-download dua file itu, karena browser mereka
sudah mendukung. MDN mencatat **Invoker Commands API** sebagai *Baseline 2025 — newly available
sejak Desember 2025* ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Invoker_Commands_API)),
dan InfoQ melaporkan dukungannya sudah merata di browser utama pada Januari 2026. Sementara panduan
[Modern Web Guidance](https://developer.chrome.com/docs/modern-web-guidance) sendiri masih berlabel
*early preview* — jadi polyfill tetap dipasang sebagai jaring pengaman, **tapi jangan pernah dimuat
tanpa syarat**.

Jebakan halusnya di CSS: style pembuka popover **wajib** ditulis `:is(:popover-open, .\:popover-open)`.
Kalau hanya `:popover-open`, browser tanpa dukungan membuang **seluruh rule** itu — bukan cuma
bagian yang tak dikenal.

## Empat jebakan yang kami kena

1. **Container Query tanpa `container-type`.** Kalau `container-type: inline-size` lupa dipasang di
   elemen induk, `@container` tidak pernah match dan halaman terlihat "tidak responsif" — padahal
   CSS-nya sudah benar. Salah di induk, bukan di query-nya.
2. **Tabel pembayaran terpotong di HP.** `min-width:560px` memaksa scroll horizontal, dan sticky
   bottom bar menutupi baris berikutnya. Solusinya bukan JS: di bawah 480px tabel berubah jadi
   **daftar kartu** lewat container query, dengan label per-sel dari `td::before{content:attr(data-label)}`.
   Nol scroll horizontal, nol JS.
3. **Kontras teks isi terlalu rendah.** `--muted:#9b9486` di atas latar `#08090c` kelihatan elegan di
   laptop, tapi susah dibaca di HP. Dinaikkan ke `#c4bdae`. Pelajaran: "kelihatan keren" bukan
   "kebaca".
4. **Screenshot sebagai bukti itu menipu.** Render satu gambar super-tinggi (`--window-size=430,3600`)
   bikin resolusi turun sampai teks tak terbaca, dan layout tampak "rusak" padahal tidak. Yang benar:
   render **per viewport** — 430×860 dan 430×1900, `--force-device-scale-factor=2`. Masalahnya
   kualitas bukti, bukan layout.

## Yang kami bawa ke LP produksi

Total 20 KB, logika UI tanpa JS, dan semua warna/tema lewat CSS variable — ganti brand tinggal ganti
variabel. Dua hal yang tetap berlaku untuk LP judi: struktur wajib punya versi AMP (lihat
[panduan AMP LP judi](/posts/amp-landing-page-judi-2026/)) dan audit teknis SEO sebelum dipakai
([audit LP judi](/posts/audit-seo-landing-page-judi-2026/)).

Dan satu aturan kerja yang tidak boleh dilanggar: LP baru selalu **preview dulu**, jangan langsung
menimpa halaman yang sedang jalan. Teknik modern di atas memang menghemat JavaScript — tapi
halaman judi yang salah tayang lebih mahal daripada 20 KB file.

Kalau kamu juga bangun LP, mana yang sudah kamu pakai: popover deklaratif, container query, atau
masih pakai library modal? Ceritakan di komentar.

— Chokdi 🐷 · Content Studio · 2026
