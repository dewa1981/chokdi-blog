---
title: "Web Search Hermes Agent Kini Gratis & Ngebut: Perplexity Fast Search 160 ms"
date: 2026-10-05T01:20:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Perplexity", "Open Source", "Tutorial"]
---

Kalau kamu pengguna **Hermes Agent**, ada kabar bagus: sejak 24 September 2026, tool `web_search` di Hermes nggak cuma cepat — tapi **gratis** buat semua pengguna Nous Portal. Yang bikin cepat? Ini bukan model AI yang ngarang ringkasan, tapi mesin pencari yang memang dirancang untuk agen: **Perplexity Fast Search**.

Masalahnya, kabar ini beredar lebih cepat daripada dokumentasinya. Banyak yang sudah update Hermes tapi Fast Search-nya tetap nggak nyala. Kenapa? Ada jebakan versi yang perlu kamu tahu sebelum buru-buru ganti backend pencarian.

## ⚡ Apa itu Perplexity Fast Search?

Fast Search adalah mode khusus dari Perplexity Search API yang dibuat untuk **agen**, bukan manusia. Bedanya penting: agen mengirim banyak pencarian kecil berturut-turut dan menunggu hasilnya satu per satu. Kalau tiap pencarian makan 2-3 detik, agen jadi lambat dan mahal.

Perplexity memangkas itu drastis. Angka resminya:

- **160 milidetik di p50** — separuh pencarian selesai dalam waktu ini
- **230 milidetik di p95** — 95% pencarian selesai di bawah angka ini

Sebagai perbandingan, kedipan mata manusia sekitar 300-400 ms. Jadi hasil pencarianmu datang **lebih cepat dari kedipan mata**, dan karena Fast Search mengembalikan hasil terurut dari indeks Perplexity sendiri (tanpa LLM menulis ulang cuplikannya), isinya juga lebih jujur dan nggak "dibumbui".

## 🔌 Kenapa kamu nggak perlu API key sama sekali

Ini bagian yang paling menarik, dan yang paling sering salah dipahami.

Fast Search di Hermes bukan backend yang kamu daftar sendiri. Dia ada di balik **managed web search** milik Nous Tool Gateway. Artinya:

- Kamu **tidak butuh akun Perplexity**
- Kamu **tidak butuh `PERPLEXITY_API_KEY`**
- Hermes menandatangani permintaan pakai login **Nous Portal** kamu, lalu gateway yang meneruskan ke Perplexity

Jadi urusan tagihan ada di lapisan gateway, bukan di kunci API yang kamu tempel di `.env`. Kalau kamu pernah bingung "kok bisa gratis, Perplexity kan bayar" — jawabannya di situ: Nous yang menanggung jalur gateway-nya.

## 🆓 Siapa saja yang dapat gratis?

Ini tabel yang bikin banyak orang salah paham. Aturan gratisnya nggak semata soal "punya langganan berbayar atau tidak":

- **Langganan Nous Portal berbayar** → Gratis Fast Search ✅
- **Akun Portal terdaftar, kredit nol** → Tetap gratis ✅ (setelah perbaikan 1 Oktober 2026)
- **Guest tanpa akun Portal** → Bukan Fast Search; Hermes pakai "keyless ring" (Exa, Parallel, Firecrawl, Keenable bergilir)
- **Pakai `PERPLEXITY_API_KEY` sendiri** → Tidak gratis; ditagih Perplexity per request

Catatan penting untuk baris kedua: sebelum perbaikan yang mendarat **1 Oktober 2026**, akun terdaftar dengan kredit nol diam-diam jatuh ke keyless ring tanpa memberi tahu penggunanya. Jadi kalau kamu punya akun Portal tapi saldo nol dan merasa pencariannya biasa-biasa saja — kemungkinan besar kamu kena bug ini.

Satu lagi: **hanya `web_search` yang gratis**. `web_extract` (yang membaca halaman penuh) tetap tool gateway berbayar, dan managed extraction masih jalan di atas Firecrawl.

## ⚠️ Jebakan versi: stable v0.21.5 BELUM punya Fast Search

Ini bagian yang paling sering bikin orang frustrasi, dan ini fakta yang harus kamu tahu.

**Hermes v0.21.5 — versi stable saat pengumuman keluar — dirilis di hari yang sama dengan pengumumannya, tapi TIDAK memuat rute managed Perplexity.** Rutenya di-merge ke `main` setelah build stable dipotong. Praktisnya:

- **Di stable v0.21.5:** Perplexity hanya bisa dipakai sebagai *bring-your-own-key* (berbayar)
- **Di `main` atau canary:** Fast Search managed sudah bisa dipakai hari ini
- **Di rilis stable berikutnya:** fitur ini baru akan mendarat

Jadi kalau kamu di stable dan menunggu fitur ini muncul sendiri — tunggu rilis stable berikutnya, jangan buang waktu ganti-ganti setting.

## 🛠️ Cara mengaktifkan (kalau build-mu sudah mendukung)

Kalau build-mu sudah punya rute managed Perplexity, ada tiga jalan:

1. `hermes setup --portal` — untuk instalasi baru: login Portal + Tool Gateway sekaligus
2. `hermes tools` — pilih **Web Search & Extract → Nous Subscription**
3. `hermes config set web.backend nous` — set backend langsung dari CLI

Kalau kamu sudah login ke akun Portal terdaftar dan **belum pernah** menyetel backend web sendiri, Hermes memilih managed search secara otomatis. Tapi ingat: **setting eksplisit dan API key selalu menang**. Jadi kalau kamu pernah menyetel `web.backend: tavily`, Hermes akan tetap pakai Tavily sampai kamu mengubahnya sendiri. Ini penyebab kedua paling umum "kok fast search nggak nyala".

Cara cek yang sedang aktif:

```bash
hermes portal info
```

Lihat baris **Web tools**. Bonus: kalau sebuah panggilan jatuh ke penyedia lain, hasil tool-nya memberi tahu kamu — `served_by` menyebut siapa yang menjawab, dan `rescued_from` menyebut siapa yang gagal. Jadi ada bug report 25 September dari pengguna Portal yang pencariannya diam-diam fallback padahal tool melaporkan "success". Pelajarannya: **jangan asumsikan — baca `served_by`**. Kalau di situ bukan Perplexity, kamu belum benar-benar di Fast Search.

## 🎛️ Masih mau pakai kunci sendiri?

Perplexity sudah tersedia sebagai backend web biasa sejak **v0.21.1**, dan itu termasuk di jalur stable. Cocok kalau kamu mau hasil Perplexity tanpa akun Portal. Tambahkan `PERPLEXITY_API_KEY` di `~/.hermes/.env`, lalu set `web.backend: "perplexity"` di `config.yaml`. Konsekuensinya: ditagih per request oleh Perplexity.

Satu catatan praktis: dengan Perplexity, `web_extract` mengembalikan **potongan halaman yang relevan dengan query**, bukan halaman utuh. Kalau kamu butuh halaman penuh, pisahkan backend-nya — `search_backend: "perplexity"` untuk pencarian, `extract_backend: "firecrawl"` untuk pembacaan halaman.

Bagi yang sama sekali belum punya akun Portal: pencarian tetap jalan. Instalasi baru tanpa kredensial web akan bergilir memakai tier publik gratis **Exa, Parallel, Firecrawl, dan Keenable**. Kalau salah satu kena rate limit, permintaan pindah ke berikutnya. Lebih lambat dan kurang bisa diprediksi, tapi nggak butuh signup.

## 🧭 Kesimpulan

Fast Search bukan sekadar "pencarian lebih cepat". Dia mengubah pola pakai agen: tugas yang dulu berat karena harus mikir dua kali sebelum memanggil `web_search`, sekarang jadi murah dan cepat. Kalau kamu menjalankan agen untuk riset harian, memantau berita, atau pipeline konten otomatis seperti yang kami jalankan di Chokdi, ini penghematan waktu yang terasa setiap hari.

Tiga hal untuk diingat: **(1)** akun Portal — walau kredit nol — dapat Fast Search gratis; **(2)** stable v0.21.5 belum memuatnya, tunggu rilis stable berikutnya atau pindah ke canary dengan hati-hati (backup `~/.hermes` dulu, karena format data bisa berubah dan nggak bisa di-rollback); **(3)** setting backend lama kamu menang atas default baru — cek `hermes portal info`.

Kalau kamu baru mau mulai dari sisi berbayar/byok, baca juga catatan kami sebelumnya di [Perplexity Search API resmi masuk Hermes Agent](/posts/hermes-agent-perplexity-search-api/) — dua artikel ini saling melengkapi.

Kamu sudah cek `served_by` di hasil tool terakhirmu? Tulis di komentar backend apa yang sebenarnya melayani pencarianmu — kami penasaran berapa banyak yang masih diam-diam di keyless ring.

— Chokdi 🐷 · Content Studio · 2026
