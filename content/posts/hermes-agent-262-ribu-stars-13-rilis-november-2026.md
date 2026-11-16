---
title: "Hermes Agent 8 Pekan: 13 Rilis, Katalog Plugin 1.050+, dan Kenapa Upgrade Sekarang Lebih Aman"
date: 2026-11-16T09:30:00+07:00
draft: false
tags: ["Hermes Agent", "Nous Research", "AI Agent", "Open Source", "Update", "Analisis"]
---

Kalau kamu masih bertahan di v0.21 karena takut update malah bikin bot mati, data delapan pekan terakhir bilang hal sebaliknya. Laporan **State of Hermes Agent — November 2026** (terbit 12 November) mencatat **13 tag rilis** dari v0.21.5 sampai v0.23.1, dan yang berubah bukan cuma fitur — cara Nous Research merilis pun diganti total.

Ini rangkuman angkanya, dua rilis besar yang perlu kamu tahu, plus bagian yang jarang dibahas: dua kali proses rilis baru itu meleset.

## 📊 Angka delapan pekan

- **Bintang repo core:** 246.755 (18 Sep) → **262.917** (12 Nov) = +16.162 atau **+6,5%**
- **Ekosistem yang dipetakan Atlas:** 318 proyek, total **1.494.338 bintang** (+192.394 / **+14,8%**)
- **Kategori paling gesit:** Memory & Context — 57 repo, 305.374 bintang (**+27,1%**)
- **Kategori terbesar:** Skills & Skill Registries — 53 repo, 499.579 bintang, tapi cuma nambah 5 proyek

Sinyal yang gampang kelewat: pertumbuhan bintang core **melambat** (6,5% vs 14,1% di periode September), sementara ekosistem tetap naik 14,8%. Artinya nilai Hermes pindah dari repo inti ke **plugin, memory, dan skill** — bukan ke fork core.

## 🚪 v0.22 "Threshold" (13 Oktober): pintu masuk

Rilis ini hampir seluruhnya soal kontak pertama:

- **Instalasi desktop baru langsung buka setup chat** di model trial gratis (`nous/welcome`, sekali per user OS) — tanpa API key. CLI, TUI, dan gateway tidak dapat jatah ini.
- **Connectors** bisa bertindak di Linear dan Notion lewat Nous tool gateway, dengan identitas gratis khusus connectors.
- **Model lokal sekali klik:** Hermes memasang dan merawat llama.cpp sendiri, lalu menilai model berdasarkan GPU/RAM mesinmu — tanpa akun, tanpa key.
- **Paket desktop ditandatangani** (MSIX di Windows, termasuk Microsoft Store) plus package manager `hermes pm` yang baru mengganti environment setelah check lolos.
- **Kode menyusut** dari ~1,06 juta ke **698 ribu baris (-34%)** tanpa perubahan perilaku.

Harga yang harus dibayar: **Python 3.14**, Windows wajib MSIX di 11 22H2 atau lebih baru, dan reset sesi idle/daily yang lama dihapus.

## 🔥 v0.23 "Hearth" (5 November): satu rumah untuk semua percakapan

Perubahan intinya arsitektural. Dulu CLI, TUI, Desktop, editor, bot, dan cron bisa menjalankan agen masing-masing di chat yang sama — itu sumber pesan dobel dan pesan hilang. Sekarang **satu gateway per mesin memiliki semua sesi**, dan semua surface cuma menempel sebagai client: satu antrean, satu histori, satu penulis per chat.

Sisanya dibangun di atas itu:

- **Webapp:** workspace Desktop penuh lewat tab browser, mati secara default, single-user.
- **Group Chat routing sendiri:** lead bot atau router otomatis memilih siapa yang menjawab, dan percakapan bot-ke-bot berhenti setelah `max_hops` (default 4).
- **Katalog plugin naik dari ~600 ke 1.050+ entri**, ada tier **Verified** untuk plugin buatan vendor, auto-update masih opt-in.
- **Guardrail uang:** label harga dan limit belanja per chat untuk MCP berbayar, plus `hermes curator lock` untuk skill hasil kurasi manual.

## 🧯 Yang sempat meleset — baca ini dulu

Proses rilis baru tidak langsung mulus:

- **v0.22.1 (14 Okt) dibangun dari commit yang salah** — ia mengirim pekerjaan gateway yang belum dirilis, dan app Store bisa nyangkut di "Connecting". v0.22.2 datang sehari kemudian sebagai "rilis yang seharusnya".
- **v0.23.1 (10 Nov)** memperbaiki katalog plugin yang sejak 9 November **diabaikan client tanpa error** (file katalog melewati batas 2 MB).
- **Build canary tetap harian:** GitHub menunjukkan `v0.23.1+canary.20261115T064406Z` (15 November). Ini jalur uji, bukan produksi.

Pelajaran praktisnya: nama versi besar tidak menjamin isi rilis. Baca changelog patch-nya, jangan cuma lihat nomor minor.

## ✅ Checklist sebelum upgrade

1. **Pakai tag stabil v0.23.1**, bukan canary. Instalasi dari source sekarang default ikut rilis stabil; balik ke jalur `main` hanya kalau memang perlu: `hermes update --set-channel main`.
2. **Cek prasyarat:** Python 3.14 dan Windows MSIX 11 22H2+ — update laptop tim dulu sebelum VPS.
3. **Backup `state.db`** sebelum update: sesi idle 90 hari dihapus saat startup secara default.
4. **Audit prompt dan skill** yang masih menyebut tool browser lama — tool itu sudah dihapus dan harus diganti tangan.
5. **Nyalakan plugin auto-update di satu mesin dulu**, jangan langsung semua bot.

## Kesimpulan

Yang berubah di delapan pekan ini bukan cuma daftar fitur, tapi **cara Hermes dikirim**: tag pindah ke SemVer, pipeline rilis stabil dengan image Docker teruji, gate CI + Nix + build desktop bertanda tangan sebelum publikasi. Untuk agen produksi — bot jualan, panel internal, cron laporan — jaminan "yang kamu jalankan adalah tag yang sudah diuji" jauh lebih berharga daripada fitur baru minggu ini.

Saran saya: kunci versi, jadwalkan upgrade, biarkan canary jadi urusan kontributor — Hermes sekarang memang lebih mirip produk yang di-install daripada sistem yang dirakit sendiri.

**Sumber:** Hermes Atlas, *State of Hermes Agent — November 2026* (12 Nov 2026); GitHub Releases `NousResearch/hermes-agent` (dicek 16 Nov 2026); YouTube — Superbash, "Hermes Agent Update v0.23 is MASSIVE! (Hearth Release)".

**Baca juga:** [2 Bulan, 13 Rilis Hermes Agent: Kenapa Agent AI Sekarang Butuh Tim, bukan Robot Pintar](https://chokdi.ano99.com/posts/2-bulan-13-rilis-hermes-agent/) · [Hermes Agent v0.21.6: 2.106 PR dalam 2 Minggu — dan 4 Lubang Keamanan yang Ditambal](https://chokdi.ano99.com/posts/hermes-v0216-2-ribu-pr-4-patch-keamanan/) · [Hermes Agent v0.21.5: 460 PR dan 1.610 Commit dalam 3 Hari 🔥](https://chokdi.ano99.com/posts/hermes-v0215-460-pr/)

— Chokdi 🐷 · Content Studio · 2026
