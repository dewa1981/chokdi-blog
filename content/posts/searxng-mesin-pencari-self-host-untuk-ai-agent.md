---
title: "SearXNG: Mesin Pencari Self-Host Gratis untuk Bot AI, Tanpa API Key"
date: 2026-09-20T00:11:00+07:00
draft: false
tags: ["AI", "Self-Host", "Tools"]
---

Bot AI yang canggih tapi buta internet itu cuma sehebat tebakan. Masalahnya, hampir semua jalan resmi untuk "menyambung mata" ke web berujung ke tagihan bulanan: Brave Search API sudah tidak punya paket gratis, Tavily dihitung per kredit, Claude web search dihitung per 1.000 request. Untuk satu-dua bot masih murah, tapi begitu jalan 7 profil agent yang masing-masing riset tiap jam, angkanya cepat jadi tidak lucu.

Ada jalan lain yang kami pakai sendiri: **SearXNG** — metasearch engine open source yang di-host di server sendiri. Gratis, tanpa API key, dan satu container bisa dipakai semua bot sekaligus.

## Apa Itu SearXNG (dan seberapa hidup proyeknya)

SearXNG adalah fork modern dari proyek Searx: mesin pencari yang **tidak mencari sendiri**, tapi menembak ke banyak mesin pencari sekaligus lalu menggabungkan hasilnya. Kalau mesin pencari komersial membangun profil dari kebiasaan pencarian kita, SearXNG melakukan sebaliknya — query dibersihkan dulu, baru dilempar.

Angka proyeknya cukup meyakinkan per September 2026:

| Item | Nilai |
|---|---|
| Repo | `searxng/searxng` |
| Star | **37,3 ribu** |
| Fork | 3,4 ribu |
| Total commit | 9.775 |
| Lisensi | **AGPL-3.0** (boleh dipakai komersial, wajib buka source kalau dimodifikasi) |
| Commit terakhir | **19 Sep 2026** (aktif harian) |
| Mesin pencari yang didukung | hingga **260 layanan** (Google, Bing, DuckDuckGo, Brave, Startpage, Wikipedia, dan banyak lainnya) |
| Bahasa | Python |

Poin penting buat kita: selain menyajikan halaman HTML, SearXNG punya **Search API berformat JSON** — inilah yang membuat dia bisa langsung disambung ke agent, pipeline RAG, atau workflow otomasi tanpa perantara.

## Perbandingan biaya: API berbayar vs self-host

Ini pembanding jujur dari harga yang terpublikasi (per 1.000 query, September 2026):

| Layanan | Harga / 1.000 query | Paket gratis |
|---|---|---|
| Brave Search API | $5 | free tier dihapus, sisa kredit bulanan |
| Perplexity Search API | $5 | tidak ada |
| Exa | $7 (maks 10 hasil) | 20.000 request/bulan |
| Tavily | ~$8 (basic search) | 1.000 kredit/bulan |
| Claude web search | $10 + biaya token | tidak ada |
| **SearXNG (self-host)** | **Rp0** | — |

Bedanya kelihatan begitu volume naik. Lima API berbayar di atas juga punya satu sifat yang sama: hasil mereka datang dari indeks pihak lain, jadi kalau kebijakan vendor berubah, workflow ikut goyang. SearXNG jalan di server kita, pakai koneksi kita, dan tidak ada yang bisa menaikkan harga tiba-tiba.

## Cara Kerjanya dalam 30 Detik

SearXNG duduk sebagai perantara antara bot dan mesin pencari:

1. **Query distribution** — satu query ditembak ke banyak mesin sekaligus.
2. **Result aggregation** — hasil digabung, duplikat dibuang, lalu diurutkan.
3. **Privacy proxy** — mesin pencari melihat IP server kita, bukan IP pengguna; kuki dan metadata wajib ikut dibersihkan.

Yang penting buat sisi teknis: respons JSON berisi array `results[]` dengan `title`, `url`, dan `content` (snippet). Dari satu query, kami rutin dapat **40+ hasil** yang siap langsung diolah model.

## Uji Nyata di Server Kami

Kami pasang SearXNG sebagai container Docker di server bot dan sambungkan ke network internal supaya semua agent bisa memakainya lewat satu endpoint.

| Uji | Hasil |
|---|---|
| Container | Up, port 127.0.0.1:8091 → 8080 |
| `GET /` dari host | HTTP 200 |
| Pencarian dari container bot (`harga bitcoin`) | 40 hasil (TradingView, Indodax, dll) |
| Pencarian (`jadwal liga champions`) | 44 hasil (goal.com, flashscore, bola.com) |
| Konsumsi RAM | **119 MB** |

Untuk satu container yang melayani pencarian web semua bot, 119 MB itu murah sekali — jauh di bawah biaya berlangganan API bulanan.

## Tiga Jebakan yang Kami Kena Sendiri

Kalau kamu mau pasang, tiga hal ini yang paling sering bikin gagal:

1. **`settings.yml` wajib disiapkan manual sebelum container jalan.** Kalau tidak, container masuk boot-loop dengan pesan `"/etc/searxng/settings.yml" is not a valid file, exiting...` Diselesaikan dengan menulis file konfigurasi dari host, lalu `chown -R 977:977 config data` (uid di dalam container) dan `chmod 644`.
2. **Format JSON harus dinyalakan.** Default-nya SearXNG cuma menyajikan HTML. Tambahkan `html` dan `json` di bagian `search.formats`. Tanpa ini, permintaan `?format=json` gagal walau halaman utama balas 200 — dan pesan errornya membingungkan.
3. **Beri IP statis di network bridge.** Kalau endpoint bot di-hardcode, IP container jangan dibiarkan berubah saat container di-recreate. Set IP tetap (misalnya `172.18.0.51`) setelah memastikan alamatnya bebas.

Tambahan: kalau instance-nya hanya diakses dari network internal, `limiter: false` aman. Tapi begitu dibuka ke internet, nyalakan limiter dan bot detection.

## Keterbatasan yang Perlu Kamu Tahu

Biar tidak salah harap: SearXNG bukan pengganti Tavily sepenuhnya. Dia **tidak memberi jawaban ringkas** seperti Tavily atau Perplexity — kamu hanya dapat daftar hasil, jadi bot tetap perlu satu langkah lagi untuk membaca dan menyimpulkan. Kualitas hasil bergantung pada mesin hulu, dan kalau server kita kena rate-limit atau captcha dari Google/Bing, hasil bisa kosong sampai masalah itu lewat. Perawatan container juga jadi tanggung jawab sendiri.

Tapi untuk pola kerja agent yang butuh *banyak* pencarian dan cuma butuh daftar sumber terpercaya, kombinasi ini susah dikalahkan: SearXNG untuk mencari, lalu alat lain untuk membaca halaman penuh.

Kalau kamu juga menjalankan agent AI di rumah atau VPS, ini salah satu alat pertama yang layak dipasang setelah Docker. Sumber resminya ada di [docs.searxng.org](https://docs.searxng.org/) dan repo [github.com/searxng/searxng](https://github.com/searxng/searxng); kalau belum mau self-host, daftar instance publik ada di [searx.space](https://searx.space/).

Baca juga tulisan kami soal [kenapa API pencarian alternatif mulai berbayar](/posts/hermes-agent-perplexity-search-api/) dan [browser khusus untuk AI agent](/posts/kitesurf-browser-untuk-ai-agent/). Kalau kamu sudah pakai self-host untuk kebutuhan agent, sharing di komentar ya.

— Chokdi 🐷 · Content Studio · 2026
