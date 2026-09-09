---
title: "Perplexity Search API Resmi Masuk Hermes Agent — Ini Cara Mengaktifkannya"
date: 2026-09-09T12:20:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Tutorial", "Open Source"]
---

Kabar gembira buat pengguna Hermes Agent: sejak 9 September 2026, tool `web_search` dan `web_extract` di Hermes resmi mendukung **Perplexity Search API** sebagai backend opsional. Pengumuman ini disampaikan langsung lewat akun resmi Nous Research di X, dan ikut disambut Aravind Srinivas (CEO Perplexity) serta Denis Yarats (co-founder-nya). Artinya, agen AI open-source kini bisa "menyewa" mesin pencari komersial kelas atas — tanpa harus pindah dari Hermes.

## Apa yang baru sebenarnya?

Perplexity bukan pengganti backend default. Firecrawl tetap menjadi pilihan bawaan, dan Hermes juga masih punya opsi gratis lain (SearXNG, DuckDuckGo, Brave free tier, Exa, Parallel, Tavily, Keenable). Yang berubah: sekarang kamu punya **satu pilihan berbayar baru** yang kuat untuk `web_search` maupun `web_extract`.

Perplexity Search API mengakses indeks **400+ miliar URL** dan — sesuai dokumentasi resmi Hermes — bisa dipakai untuk dua hal sekaligus:

- **Search** — cari web dan dapatkan hasil terurut (✔)
- **Extract** — ambil konten dari URL, lengkap dengan *query-relevant snippets* (✔)

Keunggulannya: hasilnya bukan sekadar daftar link, tapi sudah disertai konteks jawaban — cocok buat riset yang butuh presisi, misalnya riset berita, perbandingan produk, atau verifikasi fakta untuk konten berbahasa Indonesia.

## Cara mengaktifkan (3 langkah)

1. **Dapatkan API key** dari Perplexity (paket Search API, dibayar per-request). Taruh key-nya di file `.env` Hermes sebagai `PERPLEXITY_API_KEY=...`.
2. **Pilih provider lewat wizard** — jalankan `hermes tools`, pilih Perplexity sebagai backend `web_search`. Bisa juga diatur manual lewat `config.yaml` pada bagian `web.backend`.
3. **Tes dulu** — minta Hermes menjalankan `web_search` dengan query apa pun. Kalau hasilnya muncul normal, berarti Perplexity sudah aktif.

Kabar baiknya, konfigurasinya fleksibel: kamu bisa memakai **provider berbeda untuk search vs extract**. Contohnya pakai SearXNG gratis untuk `web_search` dan Perplexity untuk `web_extract` — hemat biaya, tetap akurat. Ini didukung fitur *per-capability configuration* yang memang sudah lama ada di Hermes.

## Kenapa ini menarik?

- **Kolaborasi open-source × proprietary API** — momen langka: proyek agen open-source diadopsi resmi oleh perusahaan search engine besar, bukan malah dianggap pesaing.
- **Riset makin akurat** — buat yang sering bikin artikel, laporan, atau riset pasar, kombinasi Hermes + Perplexity bisa mengurangi hasil *nyasar* yang sering terjadi di search engine gratisan.
- **Momentum ekosistem** — Denis Yarats bilang timnya sedang "banyak menggarap improvement di search stack" biar paling akurat dan hemat biaya; sementara Teknium (lead engineer Hermes) bercanda: *"the world will be perplexing no more"*.

Buat yang belum familiar dengan cara Hermes mengeksekusi tugas, baca dulu artikel soal [5 mode eksekusi Hermes](/posts/5-mode-eksekusi-hermes/) — di situ dijelaskan kenapa tool seperti `web_search` bisa dipanggil otomatis oleh agen. Kalau kamu penasaran arah pengembangan Hermes ke depan, artikel soal [Bot Mode multi-agent](/posts/hermes-agent-bot-mode-multi-agent/) juga layak dibaca.

## Kesimpulan

Masuknya Perplexity Search API ke Hermes Agent adalah kemenangan buat pengguna: makin banyak pilihan backend, makin akurat hasil riset, dan tetap satu ekosistem yang rapi. Fitur ini sudah live di codebase dan tinggal diaktifkan dengan API key — cocok dicoba siapa pun yang butuh kualitas riset kelas komersial dari agen AI self-hosted.

Sumber: [pengumuman resmi Nous Research](https://x.com/NousResearch/status/2097485341250752979) dan [dokumentasi Web Search Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-search).

Sudah coba Perplexity di Hermes? Cerita pengalamanmu di kolom komentar ya — penasaran seberapa beda hasilnya dibanding backend gratis.

— Chokdi 🐷 · Content Studio · 2026
