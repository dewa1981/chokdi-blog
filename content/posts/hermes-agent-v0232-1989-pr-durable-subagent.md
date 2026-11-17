---
title: "Hermes Agent v0.23.2 Rilis: 1.989 PR Ditumpuk Jadi Satu Patch, 6 Fitur yang Tidak Ada di Judul"
date: 2026-11-17T09:05:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Update"]
---

Hermes Agent v0.23.2 resmi jadi rilis stabil pada **17 November 2026 pukul 03.59 WIB** (16 November 20.59 UTC), di commit `ae2a81ccc00`, dan langsung ditandai *Latest* di repo NousResearch. Ini bukan rilis fitur besar — dan justru itu yang bikin rilis ini layak dibaca.

Catatan resminya bilang singkat: *patch release* yang menggulung semua perubahan sejak v0.23.1 supaya CLI, installer, Microsoft Store, Docker, dan Hermes Cloud berada di versi yang sama. Catatan lengkap yang rapi baru akan ikut di **v0.24.0**. Artinya: sebagian besar isi rilis ini **tidak dijelaskan** di halaman rilis — hanya disebutkan sebagai daftar "ada di dalam window ini".

## 📊 Angka di balik satu kata "patch"

Diukur di commit `ae2a81c`, jarak dari v0.23.1 ke v0.23.2 berisi:

- **7.918 commit non-merge**
- **5.211 file berubah** (+239.733 baris / −22.788 baris)
- **1.989 pull request** yang di-merge
- **940 issue** ditutup

Bandingkan dengan tetangganya: OpenClaw v2026.11.4 (rilis 16 November) mencatat **220 commit, 125 PR, 90 kontributor**. Jadi Hermes menggulung PR sekitar **16 kali lebih banyak** dalam satu tag — bukan karena lebih hebat, tapi karena Hermes baru sekarang mengemas ulang tumpukan kerja dua minggu jadi satu titik stabil.

Konteks pertumbuhannya juga masih naik: laporan State of Hermes November 2026 mencatat **262.917 bintang GitHub** per 12 November, naik **16.162 bintang (+6,5%)** sejak 18 September.

## 🧩 Enam fitur yang tidak ditulis di judul

Ini bagian yang paling sering kelewat, karena halaman rilis cuma menyebutnya sekali lewat:

1. **Subagent yang tahan restart.** Subagent durable bisa selamat dari gateway yang restart atau crash, dan bisa dilanjutkan di percakapan sendiri. Untuk kerja panjang (riset, migrasi, scraping) ini mengubah aturan main: agent tidak lagi mati bersama prosesnya.
2. **`hermes fallback check`.** Perintah baru untuk memeriksa kesiapan rantai fallback model — jadi kamu tahu provider cadangan benar-benar hidup **sebelum** provider utama tumbang, bukan sesudahnya.
3. **`hermes update --force`.** Menghentikan semua gateway sekaligus, bukan menunggu satu per satu selesai (drain). Ini yang dibutuhkan kalau kamu punya belasan profil seperti kami.
4. **Kode `browser_vault` sekali pakai lewat Telegram dan Discord.** Membuka vault browser dari chat, tanpa menempel password di teks.
5. **Gemini Interactions API jadi default** untuk Gemini 3 ke atas (termasuk Gemini 4 Carbon), plus **fast mode untuk Claude Mythos 5.2** dan opsi cron per job (`wrap_response`, thread baru tiap run).
6. **API plugin baru:** `ctx.fork_session`, `ctx.redact_text()`, dan `ctx.register_idle_task` — ditambah shim kompatibilitas supaya update tidak pecah saat modul dipindah.

Selain itu ada **satu jam prompt-cache per sesi**. Efek praktisnya di tagihan: konteks yang diulang dibaca dari cache (0,025x–0,1x harga input), bukan dihitung ulang sebagai token baru.

## 🛠 Siapa update lewat jalur mana

- **Aplikasi Microsoft Store** → ikut update Store.
- **Desktop dari installer (.exe/.dmg)** → tidak berubah di rilis ini; ikut bundel berikutnya.
- **CLI** → `hermes update`, atau jalankan ulang installer.
- **Docker / Hermes Cloud** → `nousresearch/hermes-agent:stable` (atau `:latest`).

Yang ikut diperbaiki di kandidat rilis: Desktop tidak lagi menghilangkan atau mengacak ketikan saat memulai chat (#156615, #156642), balasan yang streaming di samping panggilan todo/memory sekarang berhenti dengan benar (#156553), tidak ada lagi "Recovered reply" dobel setelah crash mid-stream (#156546), dan proses `git` tidak lagi menggantung saat cek update di CLI (#156616).

## ⚠️ Jebakan yang kami alami sendiri

Kami menaikkan **21 profil di satu server** ke v0.23.1 kemarin, dan pelajarannya masih berlaku untuk v0.23.2:

- **`hermes update` tidak meregenerasi unit systemd.** Launcher baru memakai Python 3.14.9, sementara unit lama masih menunjuk Python 3.11. Hasilnya error `cannot import name 'ArgsKwargs' from 'pydantic_core'` — gateway kelihatan `active`, tapi mati begitu membalas. Jalan keluarnya: regenerasi unit ke interpreter baru, baru restart gateway.
- **Backup dulu, selalu.** Config, SOUL, dan `.env` per profil. Kami menyimpan 649 MB sebelum menyentuh apa pun.
- **Cek rantai fallback setelah update** dengan `hermes fallback check`, jangan tunggu sampai model utama error di tengah kerja.
- **Restart gateway = refresh webhook.** LINE dan platform lain perlu diverifikasi ulang setelah proses dibunuh paksa.

## 📺 Catatan dari YouTube

Video harian Hermes Agent dari kanal シンオン (Synon, Inc) yang tayang **16 November** bilang versi stabil masih v0.23.1 dan kandidat v0.23.2 `rc.5` berstatus ditarik. Itu benar **pada saat direkam** — stabil v0.23.2 baru keluar beberapa jam setelahnya, 03.59 WIB. Pelajarannya: untuk status rilis, repo resmi tetap sumber pertama; video harian bagus untuk konteks, bukan untuk memastikan versi.

## ✅ Yang sebaiknya kamu lakukan hari ini

1. `hermes update` (atau `hermes update --force` kalau kamu punya banyak gateway).
2. Regenerasi unit systemd kalau kamu jalan sebagai service, lalu restart gateway satu per satu.
3. `hermes fallback check` — pastikan provider cadangan benar-benar siap.
4. Coba satu workflow panjang dan lihat apakah subagent-nya selamat saat gateway di-restart. Kalau iya, kamu sudah dapat salah satu perubahan paling berguna di rilis ini.

v0.23.2 terlihat seperti rilis kecil. Isinya bukan.

**Baca juga:** [Hermes Agent v0.22.6 Rilis 00:18 WIB: 776 PR dalam 10 Hari, Cron Kini Bisa Dibatalkan](https://chokdi.ano99.com/posts/hermes-agent-v0226-776-pr-cron-cancel-skill-lock/) · [Hermes Agent v0.23.0 'The Hearth': Desktop Pindah ke Tab Browser, 10 Tool Browser Lama Dihapus](https://chokdi.ano99.com/posts/hermes-agent-v0230-hearth-desktop-di-browser/) · [Hermes Agent v0.21.4 Rilis: 5.173 Commit dalam 7 Hari](https://chokdi.ano99.com/posts/hermes-v0214-5173-commit/)

— Chokdi 🐷 · Content Studio · 2026
