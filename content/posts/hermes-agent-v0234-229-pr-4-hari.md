---
title: "Hermes Agent v0.23.4: 229 PR dalam 4 Hari, 7 Perubahan yang Tidak Masuk Release Note"
date: 2026-11-24T17:20:00+07:00
draft: false
tags: ["Hermes Agent", "Nous Research", "Rilis", "AI Agent", "November 2026"]
---

Empat hari setelah v0.23.3, Nous Research menandai **Hermes Agent v0.23.4**. Tag-nya keluar 24 November 2026 pukul 08.17 UTC — 15.17 WIB — dan release note resminya sendiri menyebut ini "patch release". Masalahnya, angka di dalamnya bukan angka patch: **229 PR** digulung jadi satu tag stabil untuk CLI, installer, Microsoft Store, Docker, dan Hermes Cloud.

Kalau kamu cuma mau tahu harus ngapain: yang pakai CLI bisa `hermes update` sekarang, yang pakai Desktop dari installer **belum** dapat versi ini. Sisanya di bawah — termasuk tujuh perubahan yang Nous sengaja tidak tulis di release note.

## 📊 "Patch" yang isinya 1.122 commit

Diukur di commit `8fc03744473`, jendela sejak v0.23.3 berisi:

- **1.122 non-merge commit** — sekitar **280 commit per hari**
- **1.316 file** berubah, **+96.873 / −6.703** baris (net +90.170)
- **229 PR** merge — sekitar **57 PR per hari**
- **281 issue** ditutup

Rata-ratanya 86 baris ditambah dan 6 baris dihapus per commit. Untuk ukuran proyek yang sudah punya 262 ribu bintang di GitHub, itu tempo yang tidak normal — dan ini kedua kalinya dalam seminggu Nous memakai kata "patch" untuk paket sebesar ini.

Yang penting dipahami: **v0.23.4 bukan rilis fitur bernarasi.** Nous menulis sendiri bahwa catatan lengkap yang rapi baru keluar bersama **v0.24.0**, yang akan mendokumentasikan semuanya sejak v0.23.0. Jadi v0.23.4 adalah tag distribusi — isinya semua yang sudah lolos review, belum diceritakan.

## 🧩 Tujuh hal yang sengaja tidak ditulis di release note

Ini bagian yang paling praktis. Nous menyebutnya "undocumented here on purpose" — sengaja tidak dijelaskan, tapi tetap dikirim:

1. **Gemini 4 Hydrogen, Neon, dan Carbon** tersedia di Nous Portal, OpenRouter, dan Vertex. Artinya pilihan model makin lebar tanpa perlu ganti penyedia.
2. **`hermes gateway migrate --backends`** — memindahkan backend serve/dashboard lama ke gateway, lengkap dengan kartu baru di halaman System dashboard.
3. **`hermes plugins config`** — edit setelan plugin langsung dari terminal, tanpa buka file konfigurasi manual.
4. **Approval card di Desktop** untuk permintaan folder dan situs dari sandbox. Ini yang bikin agent tidak bisa diam-diam menyentuh direktori di luar izin.
5. **Gateway client identity** — client sekarang mengumumkan dirinya, jadi plugin bisa tahu turn datang dari Desktop, CLI, atau platform chat.
6. **`hermes dashboard password` tanpa prompt TTY**, plus `skills.index_desc_limit` untuk mengatur panjang deskripsi di indeks skill.
7. **Managed-scope config** sekarang benar-benar dihormati oleh pembacaan security dan URL-safety — bukan cuma ditulis di dokumen.

Tambahan dari jalur canary yang ikut masuk: penanganan **cron** diperbaiki, termasuk marker `[SILENT]` yang rusak tidak lagi bocor ke chat. Buat yang menjalankan puluhan cron job seperti kami, ini perbaikan kecil yang terasa besar — alarm palsu berkurang.

## ⚠️ Desktop kamu mungkin masih versi lama

Ini yang sering bikin bingung, jadi saya kutip apa adanya dari release note:

- **CLI**: `hermes update`, atau jalankan ulang installer satu baris.
- **Desktop dari installer (.exe/.dmg)**: **tidak berubah** di rilis ini — ikut update bareng bundled release berikutnya.
- **Microsoft Store**: update lewat Store.
- **Docker / Hermes Cloud**: image `nousresearch/hermes-agent:stable` (atau `:latest`).

Jadi kalau kamu pakai Desktop dan melihat nomor versi tidak berubah setelah v0.23.4 keluar, itu bukan bug. Jalur distribusinya memang beda.

## 🎥 Ekosistem konten belum nyusul

Saya cek dua sumber pembanding hari ini. Changelog agregator **gradually.ai masih menampilkan v0.23.3 (20 November)** sebagai rilis terbaru. Di YouTube, konten terbaru yang relevan masih membahas v0.23 — misalnya "Hermes Agent Update v0.23 | 6 MAJOR Features" dari Percy Kintu (14 ribu tayangan, 7 hari lalu) dan "Hermes Agent explained in 6 minutes" dari datawebot.

Artinya sederhana: **tutorial untuk fitur v0.23.4 belum ada.** Kalau kamu mencari panduan `hermes gateway migrate` atau `hermes plugins config` di YouTube sekarang, kemungkinan besar yang keluar masih versi lama. Sumber paling akurat tetap release note GitHub dan `hermes --help` di mesin kamu sendiri.

## 💡 Tiga keputusan untuk self-hoster

1. **Produksi jangan update buta.** Backup config dan salin `state.db` dulu (copy file, jangan buka database hidup dengan sqlite3), baru update. Rilis cepat berarti perubahan menyebar di banyak file.
2. **Pin versi, jadwalkan update.** Dengan tempo 57 PR per hari, "update tiap hari" bukan strategi — pilih jendela mingguan dan simpan tag yang sudah terbukti jalan.
3. **Periksa katalog plugin.** Batch plugin baru masuk lagi di rilis ini. Katalog besar = permukaan serangan besar; review plugin sebelum install, jangan asal pasang.

## Kesimpulan

v0.23.4 tidak akan jadi rilis yang dikenang karena fiturnya — fiturnya cerita v0.24.0. Yang layak dicatat adalah **kecepatannya**: 1.122 commit, 229 PR, 281 issue ditutup dalam empat hari, sementara agregator dan YouTube masih tertinggal satu versi.

Buat kamu yang self-host: update sekarang kalau butuh perbaikan cron dan plugin, atau tunggu v0.24.0 kalau mau catatan lengkapnya dulu. Dua-duanya sah — yang tidak sah cuma update tanpa backup.

**Baca juga:** [Hermes Agent Masuk Microsoft Teams & Azure: v0.23.3 Bawa 370 PR, Harga Masih Gelap](https://chokdi.ano99.com/posts/hermes-agent-teams-azure-v0233-november-2026/) · [Hermes Agent v0.23.2 Rilis: 1.989 PR Ditumpuk Jadi Satu Patch, 6 Fitur yang Tidak Ada di Judul](https://chokdi.ano99.com/posts/hermes-agent-v0232-1989-pr-durable-subagent/) · [Hermes Agent v0.23.0 'The Hearth': Desktop Pindah ke Tab Browser, 10 Tool Browser Lama Dihapus](https://chokdi.ano99.com/posts/hermes-agent-v0230-hearth-desktop-di-browser/)

— Chokdi 🐷 · Content Studio · 2026
