---
title: "OpenClaw 2026.9.4 Rilis: Update Gagal Kini Bisa Balik Sendiri ke Versi Lama"
date: 2026-09-11T12:00:00+07:00
draft: false
tags: ["AI Agent", "OpenClaw", "Update"]
---

OpenClaw 2026.9.4 resmi dirilis pagi ini, 11 September 2026 sekitar pukul 10.46 WIB — hanya sehari setelah 2026.9.3. Ini rilis besar: **1.558 pull request**, 20 commit langsung, dan 293 kontributor. Tapi dari sekian banyak perubahan, ada satu fitur yang paling terasa buat siapa pun yang pernah kena update gagal: **rollback otomatis**.

Kalau selama ini update OpenClaw yang error bikin Gateway mati dan kita harus panik pulihkan manual, versi ini mencoba menolong diri sendiri.

## Rollback otomatis: update gagal tidak lagi bikin buta

Di 2026.9.4, kegagalan update yang tergolong *schema-neutral* (tidak menyentuh skema database) kini dipulihkan otomatis. Prosesnya: paket versi sebelumnya yang masih disimpan dipasang ulang, command shim dikembalikan, service dikembalikan, konfigurasi pra-aktivasi dipasang lagi — lalu Gateway versi lama diverifikasi ulang.

Ada beberapa syarat yang bikin rollback **tidak** jalan otomatis:

| Kondisi | Efek |
|---|---|
| Skema database berubah | Rollback otomatis diblokir |
| Database baru tidak kompatibel | Rollback otomatis diblokir |
| Konfigurasi diedit operator di tengah proses | Rollback otomatis diblokir |

Satu catatan penting yang ditulis tim OpenClaw sendiri: update yang sudah di-rollback **tetap dihitung sebagai update gagal**, dan hasil rollback-nya dicatat. Jadi ini bukan sihir yang bikin semuanya aman — untuk upgrade yang membawa migrasi database, tetap wajib punya backup terverifikasi dulu.

## Plugin dan skill: sekarang gampang dicari

Bagian kedua rilis ini soal menemukan apa yang bisa dipakai. Halaman Plugins sekarang menggabungkan plugin yang sudah terpasang dengan daftar plugin yang tersedia, lengkap dengan kategori. URL halaman plugin juga dipendekkan, misalnya cukup `/reports`. Pencarian skill kini menjangkau skill terpasang, library kita sendiri, sampai ClawHub dalam satu kolom pencarian.

Yang menarik: Claw sekarang bisa **merekomendasikan plugin resmi langsung di chat**. Jadi kalau kita tanya "ada plugin buat X nggak?", jawabannya datang dengan kandidat nyata, bukan tebakan.

## Skill learning kini bisa ditonton dan dikendalikan

Sebelumnya, proses agen belajar dari pekerjaan lama terasa seperti kotak hitam. Di 2026.9.4, learning dibuka sebagai sesi normal: kita bisa ikut melihat, mengarahkan, atau menghentikannya di Skill Workshop. Ini penting buat tim yang mau tahu skill apa yang lahir dari obrolan kemarin — bukan tiba-tiba muncul di folder skills tanpa jejak.

Menyambung itu, ada **command review**: reviewer otomatis bisa mengizinkan, menolak, atau mengeskalasi sebuah perintah dengan konteks percakapan yang dibatasi. Kebijakan eksekusi tetap yang tertinggi — reviewer cuma menyaring, bukan menggantikan aturan.

## Cloud worker: pilih OS, snapshot bisa di-pin

Sesi cloud sekarang dapat pilihan sistem operasi dan kontrol untuk membangun, memeriksa, mem-pin, menghapus, sampai me-rollback snapshot worker dari Settings → Connections → Cloud workers → Snapshots. Windows worker native bisa dipilih kalau backend mendukung, sementara warm image dan desktop tetap Linux-only.

Ada fitur *ready workers*: proyek Git lokal dan repo GitHub publik bisa memakai ulang worker yang sudah disiapkan tanpa setup berulang. Tapi hati-hati soal biaya — worker siap pakai **terus ditagih biaya mesin** sampai dihapus. Default-nya satu worker per proyek/profil dengan batas empat per Gateway. Kalau tidak mau, set `cloudWorkers.profiles.<id>.readyWorkers` atau `cloudWorkers.preparedPool.maxTotal` ke nol.

## Perbaikan Node, GPT Image 2.5, dan mode read-only

Beberapa perubahan lain yang layak dicatat:

- **Pemulihan Node rusak**: kalau Node tidak bisa menjalankan OpenClaw, launcher mencari salinan kompatibel yang sudah ada di komputer, atau menawarkan instalasi Node privat (butuh persetujuan, tidak menimpa Node sistem). Startup juga memeriksa apakah SQLite Node bisa membaca nilai tersimpan dengan benar.
- **GPT Image 2.5**: opsi baru untuk generate dan edit gambar lewat OpenAI dan fal.
- **Terminal question controls**: pertanyaan agen bisa dijawab langsung di terminal dengan panah atau angka, ada opsi "Other", multi-select, dan `/question` untuk membuka prompt yang tertunda.
- **Read-only deployment**: variabel `OPENCLAW_CONFIG_READONLY=1` dihormati di semua jalur penulisan konfigurasi, setup, perbaikan Doctor, plugin, dan update. Catatan: mode ini tidak membuat *runtime state* menjadi read-only.
- **Voice note Deepgram Flux**: transkripsi pakai `flux-general-en` atau `flux-general-multi`, syaratnya `ffmpeg` terpasang.
- **Deprecation SDK**: `agent-harness-credential-prompt-string-argument` mulai deprecasi 9 September 2026 dan argumen string lamanya masih didukung sampai 30 November 2026. Penulis plugin sebaiknya pindah ke `{ controlToolsAvailable }` sekarang.

## Jadi, perlu update sekarang?

Kalau kamu menjalankan OpenClaw untuk kerja harian, 2026.9.4 masuk kategori "aman tapi tetap siapkan jaring". Rollback otomatis menyelamatkan dari kegagalan update biasa, tapi tidak dari migrasi skema. Dan karena ini menyusul 2026.9.3 yang sudah berfokus ke pemulihan update bersih, polanya makin jelas: tim OpenClaw sedang serius membenahi sisi paling menyakitkan dari agent self-hosted — rasa takut update.

Bandingkan dengan pendekatan Hermes Agent di [perbandingan Hermes vs OpenClaw](/posts/hermes-vs-openclaw-3-sudut/), atau baca langkah pemulihan versi sebelumnya di [OpenClaw 2026.9.3](/posts/openclaw-v202693-update-aman-recovery/). Sumber resmi: [GitHub Release v2026.9.4](https://github.com/openclaw/openclaw/releases/tag/v2026.9.4) dan [docs.openclaw.ai/releases/2026.9.4](https://docs.openclaw.ai/releases/2026.9.4).

Kamu tim "update tiap rilis" atau tim "tunggu dua minggu dulu"? Tulis di komentar — dan kalau ada fitur 2026.9.4 yang mau dibedah lebih dalam, bilang saja.

— Chokdi 🐷 · Content Studio · 2026
