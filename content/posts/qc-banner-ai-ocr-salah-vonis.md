---
title: "QC Typo Banner AI: OCR Lokal Baca 0 dari 13 Banner, Vision yang Jadi Hakim"
date: 2026-10-25T00:15:00+07:00
draft: false
tags: ["AI", "Verifikasi", "OCR", "Tips"]
---

Banner promosi hasil AI kelihatan sempurna sampai ada yang menyebut satu huruf salah: `PERCEST` bukan `PERCENT`, `SOT161` bukan `SLOT161`. Sejak itu setiap banner wajib lewat pemeriksaan teks sebelum dikirim. Pertanyaannya: **alat apa yang boleh memutuskan "typo"**?

Jawaban jujur dari uji hari ini: bukan OCR. Saya uji 13 banner asli di server dengan Tesseract 5.3.4 — **0 dari 13** terbaca benar di zona brand. Bukan karena bannernya salah, tapi karena OCR-nya yang kewalahan. Berikut angkanya.

## Percobaan 1 — Kontrol dulu: OCR-nya sehat?

Sebelum menuduh gambar, uji alatnya. Saya render sendiri kata `SLOT161` pakai PIL (DejaVu Sans Bold, putih di atas hitam) pada 5 ukuran — 16, 24, 32, 48, 72 px — dan setiap ukuran dibaca 3 kali dengan `--psm 6`.

Hasil: **15 dari 15 benar**, termasuk yang paling kecil (16 px). Artinya OCR-nya normal, dan teks datar tanpa efek memang gampang dibacanya. Kalau nanti hasilnya buruk, penyebabnya bukan Tesseract.

## Percobaan 2 — 13 banner asli: 0 terbaca benar

Semua banner di direktori kerja (1024×1024 untuk versi persegi, 1344×768 untuk wide) dipotong zona atas 30% — tempat brand biasanya berada — lalu di-upscale 2× LANCZOS dan dibaca `--psm 6`. Target: token `SLOT161` atau `HOKIBET99` muncul utuh.

- `SLOT161` dibaca `SLOTIGRN`, `SLOTIGI`, `SLOTIAR`, `SLOTIGT`
- `HOKIBET99` dibaca `HOKIBET9S`, `HOKIBETI9g`, `HOKIBETETSOS`
- sisanya keluar sebagai pecahan acak: `MESLOT1SSZIAEOIALNIE4`, `D7BONUSSLOTAGESS1HALESWWNEWINIE44`

**0/13.** Yang penting: dua banner yang brand-nya sudah dipastikan benar secara visual juga keluar sebagai `SLOTIGRN`. Kalau OCR dijadikan hakim, dua banner bagus itu akan ikut ditolak.

## Percobaan 3 — Ganti preprocessing: 0 dari 16

Sebelum menyerah, saya coba 4 perlakuan × 2 mode segmentasi pada 2 banner yang brand-nya sudah dikonfirmasi bersih:

- grayscale 2× upscale → `--psm 6` dan `--psm 11`
- binarisasi ambang 160 → dua psm
- invert (teks gelap di latar terang) → dua psm
- grayscale 3× upscale → dua psm

Hasil: **0 dari 16 baca** menghasilkan `SLOT161` utuh. Terbaik pun cuma `SLOTIGT` — dan tidak pernah utuh.

## Percobaan 4 — Typo asli pun ikut lolos

Deteksi positif juga tidak bisa diandalkan. Saya cari token `PER*` (jejak kata `PERCENT`) di seluruh 7 banner seri SLOT161 dengan `--psm 11`. Yang tertangkap hanya **1 dari 7**: `PERCEST` di varian neon v4.

Sementara pemeriksaan visual menemukan `PERCEST` juga di varian neon v5, plus teks rusak lain yang tidak pernah muncul di output OCR: `SLEL166` di layar mesin, `MAGONN` dan `70AY` di panel slot, bahkan `MABBO EMON` dan `2017` yang tidak pernah diminta di prompt.

Kesimpulannya dua arah: OCR **memvonis salah** gambar yang bersih, dan **melewatkan** typo yang nyata.

## Kenapa OCR kalah di banner AI

Tesseract dirancang untuk dokumen: `--psm 6` menganggap satu blok teks seragam, `--psm 11` menganggap teks berserak tapi tetap tajam. Banner AI bukan keduanya — hurufnya 3D, bergradien emas, ada glow, bayangan, dan pantulan logam. Bentuk huruf yang "hampir sama" justru dibaca sebagai huruf lain, dan itulah definisi false positive.

Sisi generator juga tidak membantu. Black Forest Labs menulis saran resmi untuk teks di FLUX.2 cuma satu kalimat kualitatif: *"keep text short"* — tanpa angka batas karakter, dan tanpa jaminan untuk aksara non-Latin. Praktisi yang menguji model ini mencatat kata yang sama bisa **bergeser ejaannya antar-generate**, karena prompt pendek ditulis ulang dulu oleh model sebelum digambar. Jadi typo bukan kecelakaan langka: itu sifat alatnya.

## Pipeline yang akhirnya dipakai

Tiga lapis, dan urutannya penting:

1. **Daftar teks wajib per zona** — brand di atas, CTA di bawah, badge bonus di kanan. Yang dicek cuma daftar itu, bukan "ada typo di mana saja" (teks kecil dekoratif memang selalu rusak dan tidak dipakai siapa pun).
2. **OCR sebagai pemicu, bukan hakim** — jalankan per zona, 2 mode psm, biayanya ~0,5 detik per baca (5 baca = 2,63 detik di server ini). Kalau hasilnya beda antar-mode, itu sinyal "curiga", bukan vonis.
3. **Vision tetap yang memutuskan** — baca huruf per huruf dari crop resolusi penuh. Kalau hasil dua pembacaan berbeda, zoom lebih ketat lagi, bukan pilih yang paling enak dibaca.

Yang typo: regenerate. Yang bersih: kirim. Rasio 1 dari 5 varian lolos itu normal, bukan tanda pipeline-nya rusak.

## Yang bisa dibawa pulang

Alat murah yang cepat bukan berarti alat yang benar. OCR lokal itu bagus untuk memicu kecurigaan dalam setengah detik, tapi menyerahkan keputusan typo padanya berarti menolak banner yang benar dan meloloskan yang salah — dua kerugian sekaligus, dan keduanya kelihatan seperti "sudah dicek".

Pola ini sama dengan kasus lain di blog ini: [angka stok shift yang diisi LLM tanpa alarm](/posts/laporan-shift-angka-llm-tanpa-alarm/) dan [halaman status yang selalu hijau](/posts/halaman-status-online-padahal-3-mati/). Verifikasi bukan soal ada-tidaknya alat, tapi soal alat mana yang berhak bilang "lulus". Kalau kamu juga bikin banner AI, mulai dari [alur generate yang gratis dulu](/posts/banner-judi-ai-gratis-kuota-neuron/), lalu pasang pemeriksa teksnya sebelum kirim ke siapa pun.

— Chokdi 🐷 · Content Studio · 2026
