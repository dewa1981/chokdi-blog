---
title: "Self-Host mem0 di VPS: 9 Jebakan yang Bikin Dashboard Blank"
date: 2026-09-20T12:15:00+07:00
draft: false
tags: ["mem0", "Self-Host", "AI Agent", "Docker", "Memory"]
---

mem0 itu lapisan memori untuk AI agent — tempat nyimpen fakta, preferensi, dan konteks obrolan biar agent ga lupa siapa kamu tiap sesi baru. Versi cloud-nya gampang: daftar, copy API key, beres. Tapi begitu kamu pilih **self-host**, semua kemudahan itu hilang dan gantinya 9 jebakan yang ga ada di quickstart resmi. Kami habiskan satu hari penuh pasang mem0 di VPS sendiri sampai dashboard-nya benar-benar bisa login.

## Kenapa repot-repot self-host?

Kalau kamu pakai mem0 cloud, memori agent kamu — yang isinya bisa jadi kebiasaan kerja, data klien, sampai potongan percakapan sensitif — disimpan di server orang lain, dengan harga yang bisa berubah tiap kuartal. Self-host memindahkan seluruh lapisan itu ke VPS kamu sendiri: Postgres jalan di mesinmu, embedding dihitung pakai key kamu, dan tidak ada satu pun request keluar ke mem0.ai.

Triknya: server self-host memakai **provider `openai`** yang sudah dibundel mem0, tapi `openai_base_url` diarahkan ke gateway LLM kita sendiri. Jadi kita tidak perlu patch library mem0 supaya bisa pakai provider baru — cukup arahkan base URL-nya. Hemat biaya besar, dan tetap dapat API + dashboard yang sama.

Kalau kamu masih ragu mau pakai mem0 atau engine lain, dua perbandingan yang pernah kami tulis bisa jadi bahan: [mem0 vs Hindsight untuk self-host](/posts/mem0-vs-hindsight-selfhost-review/) dan [mem0 MCP vs Hindsight](/posts/mem0-mcp-vs-hindsight/).

## Arsitektur: 3 container, satu database

Bundle self-host mem0 sebenarnya sederhana. Docker Compose di folder `server/` menjalankan tiga hal:

| Container | Port | Fungsi |
|---|---|---|
| `mem0-api` | 8888 | REST API (FastAPI + uvicorn) |
| `mem0-dashboard` | 3000 | Dashboard (Next.js) |
| `postgres` | 5432 | Postgres + **pgvector** (vector store) |

Dua port wajib kamu ingat: **8888** untuk API, **3000** untuk dashboard. Kalau pakai reverse proxy, proxy dua-duanya — bukan cuma dashboard-nya.

## 9 jebakan yang bikin dashboard blank

Semua poin ini kami alami sendiri, jadi anggap ini daftar periksa sebelum kamu mulai:

1. **Provider LLM hardcoded.** Set `GOOGLE_API_KEY` saja tidak cukup — default-nya tetap OpenAI. Ganti provider di config, bukan di env.
2. **Package tidak dibundel.** Beberapa provider butuh paket tambahan (mis. `google-genai`) di `requirements.txt`. Kalau tidak, container crash saat start.
3. **Nama model sudah usang.** Model embedding dan LLM berganti nama sepanjang tahun — cek dulu model apa yang masih hidup sebelum menulis config.
4. **Dimensi embedding tidak cocok (paling jahat).** pgvector default 1536 dimensi, sementara model embedding tertentu mengeluarkan 768. Gejalanya menipu: API membalas `event: ADD` seolah sukses, tapi `SELECT count(*)` tetap 0. Set `embedding_model_dims`, lalu **drop tabel** dan biarkan dibuat ulang.
5. **`openai_base_url` ikut ke embedder.** Ini bikin `provider_bad_request` karena endpoint chat dipakai untuk embedding. LLM dan embedder harus dipisah konfigurasinya.
6. **`DASHBOARD_URL` di-bake, bukan dibaca runtime.** Di dashboard Next.js, variabel `NEXT_PUBLIC_*` disuntik saat **build**. Restart container tidak mengubah apa pun — kamu wajib rebuild, kalau tidak frontend akan terus memanggil `http://localhost:8888`.
7. **`command:` di docker-compose menimpa CMD Dockerfile.** Ini sumber bug halus: `--reload` membuat dua proses jalan sekaligus, dan rate limiter jadi tidak berguna.
8. **Rate limiting butuh middleware.** Pasang slowapi dengan `app.state.limiter` + `SlowAPIMiddleware`; tanpa itu login dan registrasi bisa dibruteforce tanpa hambatan.
9. **Dashboard butuh HTTPS + domain.** Simpan sesi di HTTP dengan IP mentah sering gagal. Begitu diberi domain + TLS, login-nya langsung normal.

## Jebakan nomor 6 itu masalah komunitas, bukan salahmu

Kalau kamu cari "mem0 self-hosted login network error", kamu akan ketemu issue lama di repo mem0 yang masih dibalas sampai Agustus 2026: dashboard memanggil `localhost:8888`, dan jawaban di thread itu menyarankan set `API_BASE_URL=http://IP-SERVER:8888`. Saran itu **belum cukup**. Karena variabelnya `NEXT_PUBLIC_*`, menambahkannya ke `.env` tanpa rebuild hanya akan mengubah nama variabel, bukan isi bundle JavaScript yang sudah dikirim ke browser. Kalau kamu mentok di titik ini, langsung ke rebuild — jangan berputar-putar ganti port seperti kami.

## Verifikasi: jangan percaya respons API

Pelajarannya paling mahal: **respons API bisa berbohong**. Kasus dimensi embedding tadi membuat endpoint `/memories` membalas sukses sementara tabel memorinya kosong.

Selalu verifikasi dua sisi:

```bash
# sisi API
curl -X POST https://mem0-api.contoh.com/search \
  -H "Content-Type: application/json" \
  -d '{"query":"preferensi saya","user_id":"tester"}'

# sisi database — ini yang menentukan
SELECT count(*) FROM memories;
```

Kalau angka di database nol, masalahnya bukan di client kamu.

## Kesimpulan

Self-host mem0 bukan proyek sekali klik, tapi juga bukan hal yang mustahil. Panduan resminya ada di [docs.mem0.ai/open-source/setup](https://docs.mem0.ai/open-source/setup), dan kalau kamu mentok di masalah dashboard bisa dilihat di [issue #4993](https://github.com/mem0ai/mem0/issues/4993) — di sana kelihatan bahwa masalah `localhost:8888` masih hidup sampai sekarang. Sembilan poin di atas semuanya soal satu tema: **config yang tampak benar tapi tidak terbaca di tempat yang kamu kira**. Setelah semua itu beres, kamu punya lapisan memori agent yang jalan sepenuhnya di infrastruktur sendiri — plus dashboard yang bisa kamu lock ke IP tertentu saja supaya tidak ada orang lain yang bisa lihat isi memori agent kamu.

Kalau kamu juga menjalankan mem0 atau memory engine lain di VPS sendiri, bagi pengalamanmu di kolom komentar — terutama kalau kamu nemu jebakan kesepuluh yang belum kami tulis di sini.

— Chokdi 🐷 · Content Studio · 2026
