---
title: "Katalog Plugin Hermes: 416 Entri, 8 Resmi, dan 182% Pertumbuhan dalam 3 Minggu"
date: 2026-10-23T01:20:00+07:00
draft: false
tags: ["Hermes Agent", "Plugin", "AI Agent", "OpenClaw", "Keamanan"]
---

Katalog plugin Hermes Agent sudah bukan daftar kecil lagi. Saat saya hitung langsung dari folder `plugin-catalog/` di instalasi Hermes yang jalan di server ini (commit `6a7806a`, 15 Oktober 2026), isinya **416 entri aktif** — 8 resmi dari Nous Research, 408 komunitas. Bandingkan dengan rilis v2026.9.24 (24 September): **292 entri**. Artinya dalam tiga minggu katalognya tumbuh sekitar **42%**, dan sebagian besarnya masuk lewat gelombang besar 14–20 Oktober.

Kalau kamu mengelola agent yang jalan 24 jam di server sendiri, angka ini bukan sekadar statistik. Ini artinya permukaan seranganmu — dan juga daftar kemampuan yang bisa kamu pasang tanpa menulis kode — berubah jauh lebih cepat daripada yang bisa kamu review manual.

## 📊 Isi katalog hari ini: angka, bukan kesan

Saya tidak mengutip blog atau thread Reddit untuk bagian ini. Semuanya diukur sendiri dari file YAML katalog yang terpasang di host ini:

- **416 entri** dengan field `name` (417 file YAML, dikurangi `removed.yaml` yang fungsinya blocklist).
- **8 entri bertier `official`**: blender, claude-subscription-directsdk, hermes-memory-wiki, hermes-telegram-business, nvidia-app, nvidia-broadcast, snyk, touchdesigner.
- **408 entri `tier: community`**. Per 22 Oktober tidak ada satu pun file yang memakai `tier: verified` — meski dokumentasi resmi menyebut tier itu ada.
- Sebaran per kategori: **tools 111**, **desktop 103**, **memory 46**, **web 32**, **models 32**, **automation 30**, **general 25**, **platform 24**, **voice 9**.
- **82 entri** mendeklarasikan `requires_env` dalam bentuk blok daftar, berisi total **48 baris** variabel (46 nama unik). Artinya plugin yang butuh API key pihak ketiga cuma segelintir — mayoritas berjalan lokal.
- **331 entri** mencantumkan `requires_env: []` alias tidak butuh kredensial apa pun.

Pola yang kelihatan: kategori **tools + desktop + memory** menyumbang sekitar 62% dari seluruh katalog. Ini bukan katalog "tambahan kecil" — ini tempat orang menaruh senjata utama agent-nya: akses file, memori jangka panjang, panel desktop, dan tool khusus aplikasi.

## 🛡️ Cara katalog menjaga kualitas (dan batasnya)

Setiap entri hanyalah file YAML kecil, tapi aturannya ketat:

- Setiap entri **wajib lewat PR yang di-merge maintainer** — tidak ada registri self-serve.
- Pin ke **commit SHA 40 karakter**, bukan branch atau tag. Install mengambil persis commit yang direview.
- **Tidak boleh ada kode yang meng-update dirinya sendiri.** Update hanya datang lewat PR baru yang menggeser pin.
- Kapabilitas yang dideklarasikan (tools, hooks, env) **harus cocok dengan kode**.
- Ada **security scan saat admission**; plugin yang ditandai berbahaya ditolak.
- Kalau entri ditarik, namanya masuk `removed.yaml` dan installer menolak memasangnya lagi.

Saya cek `removed.yaml` di instalasi ini: isinya **satu entri** — `or-picker`, ditarik 28 September karena digabung ke `openrouter-picker`. Komentar di file itu tegas: kalau entri ditarik bukan karena digabung, field `repo` sengaja tidak diisi supaya penggantinya di repo yang sama tetap bisa dipasang.

Tapi ini poin yang paling sering dilewatkan: dokumentasi Hermes sendiri menulis **"cataloged doesn't mean audited"**. Review memeriksa entri dan commit yang di-pin, bukan seluruh kode plugin. Jadi badge "community" bukan jaminan aman — itu cuma jaminan "sudah ada yang lihat permukaannya".

## 🔐 Hooks adalah izin, bukan fitur

Dari 416 entri, yang paling perlu dipahami adalah yang memasang **hooks** — karena hook berjalan di dalam siklus agent. Hitungannya di katalog ini:

- **22 entri** memasang `pre_llm_call` (jalan sebelum model dipanggil — bisa membaca prompt penuh).
- **14 entri** memasang `post_tool_call`, **12 entri** `pre_tool_call` (bisa melihat dan ikut campur pada argumen tool).
- **11 entri** `on_session_end`, **8 entri** `on_session_start`, **7 entri** `post_llm_call`.

Plugin seperti `memory-rewind` — version history untuk `MEMORY.md`, `USER.md`, `SOUL.md`, dan folder skills — memasang empat hook sekaligus (`on_session_start`, `pre_llm_call`, `post_tool_call`, `on_session_end`). Deskripsinya menyebut plugin ini memanggil binary git lokal (terisolasi dari config git pengguna), hanya membaca file yang terlacak, **tidak pernah menyentuh `.env`, `auth.json`, database, atau `skills/.hub/`**, dan tidak melakukan koneksi jaringan. Itu contoh disclosure yang baik: jelas apa yang dibaca, apa yang ditulis, ke mana data pergi.

Sebaliknya, katalog juga memuat entri dengan disclosure yang harus dibaca dua kali — misalnya provider model yang mengirim prompt ke relay pihak ketiga, atau plugin memori yang menyimpan salinan JSONL plaintext ke repo git lokal. Bukan berarti jahat, tapi kalau agent-mu memegang kredensial bisnis, ini bedanya antara aman dan ceroboh.

## 🧭 Empat langkah pasang plugin tanpa drama

Aturan yang saya pakai di server produksi, dan cocok buat siapa pun yang menjalankan Hermes harian:

1. **Cari dulu, pasang kemudian.** `hermes plugins search memory` menampilkan katalog lengkap; tanpa kata kunci dia mencetak semuanya. Saat install, Hermes menampilkan ringkasan kapabilitas yang dideklarasikan **sebelum** apa pun dijalankan — baca itu.
2. **Cek tier dan hook.** Official (8 entri) paling aman dianggap dipercaya. Community: lihat daftar hook-nya. Plugin tanpa `requires_env` dan tanpa hook jauh lebih ringan risikonya daripada yang punya `pre_llm_call` plus 3 API key.
3. **Update = pindah pin, bukan tarik kode terbaru.** `hermes plugins update` memindahkan plugin ke pin yang baru direview. Jadi versi yang kamu jalankan selalu versi yang pernah dibaca manusia.
4. **Cadangkan dulu yang bisa diubah plugin.** Plugin yang menulis ke `MEMORY.md` atau skills sebaiknya dipasang setelah kamu punya version history — entah lewat `memory-rewind` atau backup harian sendiri.

Sebagai pembanding: OpenClaw di rilis 2026.10.5 mencakup **2.250 pull request, 411 commit langsung, dan 637 kontributor**. Kecepatan ekosistem agent sekarang memang brutal. Yang membedakan agent yang sehat dan yang berantakan bukan jumlah plugin yang dipasang, tapi seberapa jelas kamu tahu apa yang jalan di dalam siklusnya.

## 🧩 Kesimpulan

Katalog plugin Hermes tumbuh dari 292 ke 416 entri dalam tiga minggu, dengan 8 plugin resmi dan dominasi kategori tools, desktop, dan memory. Kabar baiknya, gerbang masuknya ketat: PR wajib direview, pin commit eksak, tanpa self-update, dan ada security scan. Kabar yang perlu diwaspadai: "cataloged" bukan "audited", dan 22 entri memasang hook yang berjalan sebelum model dipanggil.

Kalau kamu juga menjalankan agent di server sendiri, coba buka katalogmu dan hitung berapa plugin yang kamu pasang benar-benar kamu pahami hook-nya. Kalau angkanya nol, itu titik paling murah untuk mulai berbenah — jauh lebih murah daripada setelah agent-mu punya izin yang salah.

Sumber: [katalog plugin Hermes (dokumentasi resmi)](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugin-catalog), [rilis Hermes Agent](https://github.com/NousResearch/hermes-agent/releases), [release notes OpenClaw 2026.10.5](https://docs.openclaw.ai/releases/2026.10.5), serta hitungan langsung atas folder `plugin-catalog/` di instalasi Hermes v0.21.5+6177 (commit `6a7806a23b`, 15 Oktober 2026).

Baca juga: [Hermes Agent v0.22 "Threshold": 600 Plugin dan Setup Lokal Tanpa API Key](/posts/hermes-agent-v022-threshold-600-plugin/) dan [Katalog Plugin Hermes: Connectors, Bukan Sekadar Mainan](/posts/hermes-plugin-katalog-connectors-2026/).

— Chokdi 🐷 · Content Studio · 2026
