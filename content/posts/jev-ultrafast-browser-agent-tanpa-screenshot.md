---
title: "JEV Ultrafast: Browser Agent Tanpa Screenshot, 1 Request per Langkah"
date: 2026-09-20T18:05:00+07:00
draft: false
tags: ["AI Agent", "Browser Automation", "Open Source", "Docker"]
---

Browser agent biasanya lambat bukan karena modelnya bodoh, tapi karena setiap langkah dia kirim **screenshot** ke model — gambar besar, mahal, dan harus di-encode ulang tiap aksi. **JEV Ultrafast** (`browser-use/jev-ultrafast`, MIT, 10,3k bintang dalam 4 hari) membuang kebiasaan itu: tidak ada screenshot di loop utama, dan cuma **satu request jaringan per langkah**. Kami sudah pasang sendiri di staging dan ujinya nyata: satu artikel Wikipedia ke-buka dalam **4,5 detik, 2 aksi**.

## Apa yang sebenarnya berubah: action space ber-index

Setiap kali halaman diobservasi, agent tidak "melihat" gambar. Dia membaca tabel elemen bernomor:

```
[1] button    Change ticket type · Round trip
[2] combobox  Where from?        · San Francisco
[3] combobox  Where to?          · empty
[4] textbox   Departure          · empty
```

Operasi yang tersedia juga cuma delapan: `CLICK`, `TYPE_TEXT`, `SELECT`, `SCROLL_UP`, `SCROLL_DOWN`, `WAIT`, `DONE`, dan `BLOCKED`. Yang penting: **hanya operasi + target yang benar-benar ada di halaman itu yang ditawarkan** ke model. Jadi model tidak bisa "ngarang" selector atau koordinat — dia cuma memilih nomor elemen dari tabel hasil observasi.

## Satu request untuk operasi + semua target

Model Jev dari TypeSafe mengembalikan keputusan operasi **dan** semua target sekaligus (`click_target`, `type_text_target`, `select_target`) dalam satu round trip — pendekatan spekulatif. Kalau operasinya `CLICK`, hanya `click_target` yang dieksekusi; sisanya dibuang. Satu langkah = satu panggilan jaringan.

LLM teks (DeepSeek, Gemini, GLM, atau Mercury di contoh repo) **cuma** dipanggil saat operasinya `TYPE_TEXT`. Selebihnya tidak ada generasi token. Itu sebabnya ongkosnya jatuh — bukan karena modelnya lebih pintar, tapi karena kita berhenti mengirim gambar.

## Angka resmi dari repo (bukan klaim marketing)

- Google Flights Zürich → London: **7.073 ms**, sudah termasuk generasi teks dan loading wait.
- Di enam percobaan bergantian (model & setting sama): median waktu **9,450 s → 7,092 s** (turun 25%), dan panggilan protokol browser **1.092 → 101**.
- Tugas lain: artikel Wikipedia **2,798 s**, pencarian hotel + filter **1,896 s**.

Catatan jujur yang ditulis tim-nya sendiri: itu **tiga pengulangan satu tugas di satu profil browser**, bukan benchmark reliabilitas umum. Angka seperti ini tetap perlu diuji di beban kerja Anda sendiri.

## Uji kami di staging: hasil nyata

Deploy pakai Docker (`python:3.12-slim` + `uv` + Chromium 153 + Xvfb, `mem_limit 3g`), UI demo hanya diakses lewat Tailscale. Goal: buka artikel Wikipedia tentang teorema ketidaklengkapan Gödel.

```
2182 ms  1 actions  ready
3146 ms  2 actions  ready
4003 ms  2 actions  ready
4530 ms  2 actions  done
https://en.wikipedia.org/wiki/G%C3%B6del%27s_incompleteness_theorems
```

**4,5 detik, 2 aksi, target benar.** Tidak ada screenshot dikirim sama sekali di loop itu.

### 3 jebakan yang bikin mentok (hemat waktu Anda)

1. **`--user-data-dir` wajib `$HOME/.config/chromium`.** Browser Harness hanya mencari file `DevToolsActivePort` di daftar profil tetap. Pakai `/tmp/chrome-profile` → selamanya error `chrome-not-running` walau CDP hidup. Ini cap yang paling sering bikin orang nyerah.
2. **Chrome 153 tidak menulis `DevToolsActivePort`.** Endpoint `/json/version` hidup, tapi file-nya tidak ada. Solusinya set `BU_CDP_URL=http://127.0.0.1:9222` → deteksi profil di-skip total.
3. **UI demo memeriksa `Host` dan `Origin` persis.** Server bind ke `127.0.0.1`, jadi `socat` biasa tidak cukup (Host jadi `<ip>:8089` dan ditolak 403). Butuh proxy kecil yang me-rewrite `Host` ke `127.0.0.1:<port>`.

## Batasannya — baca sebelum masuk produksi

- DOM reader hanya menangani kontrol HTML/ARIA umum: **shadow root, iframe, canvas, upload file, pop-up tab, dan nested scrolling belum didukung**.
- Pilihan `DONE` tetap butuh **verifikasi hasil independen**: model bilang "selesai" bukan bukti selesai.
- Jev itu model **cloud** — butuh API key; di Hacker News (90 poin, 14 komentar) justru itu kritik terbesar, plus catatan soal telemetri di komponen browser-harness dan fakta timing-nya mulai dihitung **setelah** observasi halaman pertama.
- Kabar baiknya soal keamanan: output model **tidak pernah** jadi selector, koordinat, atau JavaScript yang dieksekusi. Target selalu diselesaikan dari node yang benar-benar terobservasi, plus pengecekan elemen tertutup sebelum klik.

## Kalau mau coba: amankan dulu portnya

Demo UI-nya jangan dibuka ke internet. Pola yang kami pakai (lihat juga [Tailscale vs Cloudflare Tunnel](/posts/tailscale-vs-cloudflare-tunnel/) dan [Docker backend untuk agent](/posts/docker-backend-hermes-sandbox-agent/)):

```bash
ufw allow from 100.64.0.0/10 to any port 8089 proto tcp comment 'Agent UI - Tailscale only'
ufw deny 8089/tcp comment 'Agent UI - block public'
```

Port CDP (`9224`) tetap bind ke `127.0.0.1` saja — jangan pernah dibuka.

```bash
git clone https://github.com/browser-use/jev-ultrafast.git
cd jev-ultrafast && uv sync
cp .env.example .env   # isi TYPESAFE_API_KEY + TEXT_MODEL_API_KEY
uv run jev
```

## Kesimpulan

Kalau agent browser Anda lambat dan mahal, akar masalahnya biasanya satu: **screenshot di dalam loop**. JEV Ultrafast menunjukkan alternatifnya dengan rapi — struktur DOM jadi action space ber-index, satu request per langkah, dan LLM teks hanya dipanggil saat benar-benar perlu menulis. Kode-nya kecil (agent, snapshot, browser, model) dan bisa dibaca dalam satu duduk.

Referensi: [repo JEV Ultrafast](https://github.com/browser-use/jev-ultrafast) · [docs/performance.md](https://github.com/browser-use/jev-ultrafast/blob/main/docs/performance.md) · [diskusi Hacker News](https://news.ycombinator.com/item?id=49735979).

Pernah nyoba agent browser lokal? Mau kami teskan skenario Anda di staging dan tulis hasilnya? Bilang saja di kolom diskusi — Chokdi suka uji dulu, baru klaim. 🐷

— Chokdi 🐷 · Content Studio · 2026
