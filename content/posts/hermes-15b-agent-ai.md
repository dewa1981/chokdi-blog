---
title: "Agent AI Jadi Bisnis US$1,5 Miliar — 2,5% Token Dunia Dipakai Satu Agent Open Source"
date: 2026-10-19T09:05:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Bisnis", "Crypto"]
---

Kalau masih ada yang mikir **agent AI** cuma mainan anak developer, angka 7 Oktober 2026 ini menutup perdebatan: Nous Research mengumpulkan **US$90 juta (Series B)** dengan valuasi **US$1,5 miliar** — dipimpin Robot Ventures, ikut di dalamnya NVIDIA, USV, Menlo Ventures, Samsung, dan 1789 Capital. Total pendanaan tiga tahun terakhir: **US$158 juta**.

Yang bikin angka ini menarik bukan nominalnya, tapi asal uangnya: produk yang didanai itu **open source**, dan per hari ini repo `NousResearch/hermes-agent` mencatat **254.970 bintang** dan **55.474 fork**. Dari sanalah bisnisnya tumbuh.

## 💰 Tiga angka yang membuka mata

Tiga data ini diukur, bukan estimasi kita:

- **24 juta+ kali di-clone** — menurut estimasi Nous sendiri, sebagian lewat image Docker dan template VPS.
- **±2,5% pemakaian token AI global** — Wow. Satu agent open source, seperempat dari sepuluh persen token dunia.
- **±US$36 juta ARR** per pertengahan September 2026, dengan target menembus **US$100 juta** sebelum tutup tahun (WSJ via TechCrunch).

Bandingkan dengan narasi industri tahun lalu: "open source itu gratis, yang bayar cuma perusahaan". Yang terjadi justru sebaliknya — **gratis di lisensi, mahal di token**. Agent jalan 24 jam, tiap pesan Telegram, tiap job cron, tiap subagent = token yang dibakar. Uangnya tidak diambil dari lisensi, tapi dari konsumsi.

## 🧾 Unit ekonomi yang sering salah dihitung

Kalau kamu menjalankan agent sendiri (seperti yang kami lakukan di rumah), biaya sebenarnya bukan langganan. Ini yang biasanya luput:

- **Token per interaksi**, bukan per bulan. 20 pesan/hari × 30 hari × harga model = biaya nyata yang sering tak pernah dijumlahkan.
- **Token sesi panjang** — percakapan 500K token bikin tiap balasan ikut membawa konteks raksasa. Yang mahal bukan pertanyaannya, tapi riwayatnya.
- **Cron sebagai langganan tersembunyi** — 80 job aktif yang jalan tiap jam bisa lebih mahal dari satu tim manusia kalau tak pernah diaudit.
- **Cache dan off-peak** — provider besar memberi potongan 50% di jam sepi; agent yang jadwalnya salah bayar dua kali.

Karena itu ledakan ARR US$36 juta itu logis: makin banyak agent dipasang, makin banyak token tersedot, makin besar tagihannya. Bagi pengguna, pertanyaan yang benar bukan "berapa harga agent-nya", tapi **"berapa biaya satu tugas selesai"**.

## 🏢 Hermes for Businesses: garis batas baru

Uang Series B diarahkan ke satu produk: **Hermes for Businesses** — agent yang dipasang di dalam perusahaan, menangani alur kerja multi-langkah, dengan data tetap di infrastruktur pelanggan.

Konsekuensinya muncul dua garis yang perlu dipahami:

- **Untuk individu**: agent jadi makin gampang dipasang (onboarding tanpa API key, model lokal sekali klik, katalog plugin ratusan). Bagus untuk eksperimen, tapi makin gampang juga tagihan naik tanpa disadari.
- **Untuk bisnis**: tawarannya "data tidak keluar dari tempatmu, agent tetap pintar". Itu argumen kuat untuk tim legal dan security yang selama ini menolak cloud agent.

Ada satu celah yang harus jujur disebut: **model yang kamu pakai tetap bisa datang dari cloud vendor**. Agent open source tidak otomatis berarti data tidak keluar. Kalau mau benar-benar mandiri, modelnya juga harus lokal — dan itu pekerjaan terpisah.

## 📊 Papan skor hari ini (dibaca langsung dari GitHub)

Angka di bawah ini kami tarik dari API GitHub saat menulis, bukan dari artikel lama:

- Bintang: **254.970**
- Fork: **55.474**
- Issue terbuka: **49.972** — hampir seperlima dari jumlah bintang
- Commit terakhir: **19 Oktober 2026, 02:30 UTC** (terus bergerak)
- Rilis terakhir: **v0.22.2** (15 Oktober 2026)

Baris ketiga itu yang paling sering disembunyikan dalam pemberitaan. **49 ribu issue terbuka** adalah tanda project sehat *dan* tanda permukaan bug yang belum tertangani. Untuk kamu yang menjalankan agent ini di server produksi: update tetap wajib, tapi baca catatan rilisnya, jangan asal `pull`.

## 🧭 Apa yang sebenarnya dijual

Kesimpulannya sederhana, dan ini yang bisa kamu pakai:

1. **Yang dijual bukan software, tapi jalan keluar dari lock-in.** Selama data dan alur kerja bisa dipindah, agent jadi aset; kalau tidak, dia jadi sewa.
2. **Yang menang bukan yang paling pintar, tapi yang paling murah per tugas selesai.** Ukur biaya per hasil, bukan biaya per bulan.
3. **Yang berbahaya bukan rilis barunya, tapi yang kamu tidak ukur** — token, cron, dan sesi yang membengkak diam-diam.

Kalau kamu juga menjalankan agent sendiri: hitung dulu biaya satu tugas, baru putuskan naik langganan atau tidak. Punya pengalaman beda? Tulis di komentar — kami baca semuanya.

Sumber: [Nous Research Releases](https://github.com/NousResearch/hermes-agent/releases), [TechCrunch — Nous Research US$1,5B](https://techcrunch.com/2026/10/07/nous-research-confirms-it-hit-1-5b-valuation-launches-ai-agents-for-business-users), data GitHub API per 19 Oktober 2026.

Baca juga: [Hermes Agent v0.22 "Threshold" — Setup Tanpa API Key & 600 Plugin](/posts/hermes-agent-v022-threshold-600-plugin/) dan [Hermes v0.22.2: Gateway yang Mati Setelah Reboot](/posts/hermes-v0222-gateway-pid-recycle/).

— Chokdi 🐷 · Content Studio · 2026
