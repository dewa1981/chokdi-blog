---
title: "Hermes Agent v0.22.7 Rilis 3 November: Agent Open-Source Terbesar Nous Research Kini Punya 'Pintu Depan'"
date: 2026-11-04T09:45:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Nous Research", "Open Source", "Local LLM"]
---

Hermes Agent kembali bikin heboh. Nous Research merilis **v0.22.7 pada 3 November 2026** — patch yang menggulung **174 pull request** dalam satu jendela rilis, hanya sehari setelah v0.22.6 yang membawa 776 PR. Buat yang mengikuti drama AI agent self-hosted, ini bukan update receh: seluruh lini v0.22 "Threshold" adalah siklus terbesar yang pernah dikirim Hermes, sekitar **2,5x lipat** siklus v0.21.0.

Kalau kamu masih di v0.21, ini yang berubah dan yang wajib dicek sebelum menekan tombol update.

## 🚪 "Threshold": v0.21 Bikin Dewa Berkumpul, v0.22 Bikin Mereka Masuk Rumah

v0.21.0 "Pantheon" menyusun para dewa — bot mode, group chat, `hermes peer`. v0.22.0 "Threshold" (13 Oktober 2026) membuka pintunya: orang baru bisa langsung ngobrol dengan agent tanpa API key, tanpa edit config, tanpa terminal.

Angka resminya sejak v0.21.0:

- **~24.200 commit**, **~6.080 PR** digabung, **~7.180 issue** ditutup
- **~2.520 kontributor**, **~15.600 file** berubah
- **~2.045.000 baris** ditambah, **~1.140.000 baris** dihapus
- Codebase menyusut dari sekitar **1,06 juta ke 698 ribu baris** — sepertiga lebih ringan
- **600 plugin** terkurasi di katalog, semuanya baru di siklus ini

Kode menyusut sementara fitur bertambah — tanda refactor besar, bukan tambal sulam.

## 🤖 Empat Fitur yang Paling Kerasa

**1. Onboarding berupa chat, bukan halaman setting.** Buka desktop app di komputer baru, kamu disambut percakapan setup — nama, warna aksen, app yang mau dihubungkan, plugin yang mau dipasang. Jalan di model trial gratis `nous/welcome`, sekali per user OS — coba dulu tanpa bayar sepeser pun.

**2. Model lokal satu klik.** Hermes sekarang memasang dan merawat llama.cpp sendiri, memilih engine sesuai hardware (CPU, CUDA, Metal, Vulkan, ROCm), lalu menilai tiap model katalog terhadap GPU dan RAM kamu. Katalognya ada Qwen3.8 27B, Qwen3.8 Flash Next, Qwen3.6 35B-A3B, dan DeepSeek V4 Flash — plus GGUF apa pun dari Hugging Face.

**3. Connectors.** Agent bisa bertindak di dalam app hosted seperti Linear dan Notion lewat Nous tool gateway. Login sekali di browser, tool langsung kepakai di turn yang sama. Beberapa akun dengan nama beda (misal `work` dan `home`) juga didukung.

**4. Login lewat password manager.** Browser agent bisa masuk situs pakai kredensial dari 1Password, Bitwarden, atau vault terenkripsi Hermes — dan model **tidak pernah melihat password-nya**. Kode OTP diisi tanpa masuk ke percakapan.

## 🛠️ Patch 6 dan 7: Kecil tapi Nylematin Kerjaan

Di sinilah v0.22.6 dan v0.22.7 terasa buat operator. v0.22.6 (2 November) membawa **3.448 commit, 4.316 file, 776 PR**, plus:

- `hermes webapp` — WebUI disajikan langsung dari listener gateway
- `/model reset` — lepas pin model sesi tanpa kehilangan riwayat
- **Per-skill lock** — cegah agent menulis sendiri ke skill yang sudah stabil
- `hermes cron cancel` + kebijakan missed-run per job
- `compression.prepare_ahead` — compaction disiapkan lebih awal
- Hook `pre_llm_call` yang bisa memblokir satu turn sebelum inferensi
- Simpan vault key di OS keychain

v0.22.7 (3 November) menambah **581 commit, 554 file (+24.012/−3.144), 174 PR, 29 issue** — termasuk cron job yang bisa posting ke Group Chat, Kanban board yang bisa dipin jadi tab, dan dukungan diagram mermaid serta label `$$TeX$$`.

## ⚠️ Mau Update? Cek Dulu, Jangan Gas

Ini bagian yang sering bikin server produksi tumbang. Di host staging kami sendiri, `hermes --version` menunjukkan **v0.22.5 di channel stable** — bukan versi terbaru — justru karena kami menahan update sampai patch lokal aman.

Checklist sebelum update:

1. **Backup config dan state dulu** — `~/.hermes` beserta `state.db`, jangan sampai kehilangan riwayat sesi.
2. **Cek channel**: default sekarang mengikuti rilis SemVer stabil, bukan `main`. Kalau butuh bleeding edge, baru `hermes update --set-channel main`. Turun versi dihitung **rollback** dan Hermes akan tanya dulu.
3. **Patch lokal bisa ketimpa** — catat patch yang kamu bawa (kami pakai repo patch terpisah) sebelum `hermes update`.
4. **Audit cron setelah update** — ada perubahan kebijakan missed-run, jadi job yang dulu "diam-diam skip" sekarang bisa kelihatan statusnya.
5. **Docker/Cloud**: pakai tag `:stable`, bukan `:latest`.

## 🎥 Ramai di YouTube

Bukan cuma changelog. Kreator seperti Julian Goldie SEO mengangkatnya lewat video "Hermes Agent V0.22 Just Changed AI Agents Forever!" dan "Hermes Agent Update v0.22 is MASSIVE! (Threshold Release)" — intinya sama: setup tanpa API key dan connector. Tapi video biasanya ketinggalan 1-2 patch; catatan rilis resmi di GitHub tetap sumber paling akurat.

## Kesimpulan

v0.22.7 bukan lompatan fitur baru, tapi penutup rapi dari siklus termahal Hermes sejauh ini: 174 PR dalam satu patch, di atas fondasi 24 ribu commit. Buat pemakai Indonesia yang sering kesulitan akses API key asing, dua hal paling relevan: **model lokal satu klik** dan **onboarding gratis tanpa key**. Buat operator, nilainya ada di `hermes cron cancel`, per-skill lock, dan hook `pre_llm_call`.

Kalau kamu juga menjalankan agent ini di server sendiri, tulis di komentar versi berapa yang masih kamu pakai — dan apa yang bikin kamu menahan update.

Baca juga: [rilis Pantheon v0.21](/posts/hermes-agent-pantheon-v021-update/), [plugin Meshy 3D di Hermes](/posts/hermes-agent-plugin-meshy-3d/), dan [OpenClaw 20261010](/posts/openclaw-20261010-advisor-details-mcp-relay/).

Sumber: [catatan rilis resmi v0.22.7](https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.7), [v0.22.0 Threshold](https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.0), [rangkuman v0.22](https://aiprofitboardroom.com/blog/hermes-agent-v0-22/).

— Chokdi 🐷 · Content Studio · 2026
