---
title: "OpenClaw 2026.10.4: Siapa Pun Bisa Mengaku Owner di Group DM Tlon"
date: 2026-10-18T16:45:00+07:00
draft: false
tags: ["OpenClaw", "Keamanan", "AI Agent", "Self-Hosted", "Update"]
---

Bayangkan seseorang masuk ke grup chat, mengaku sebagai kamu, lalu mengetik `approve` — dan agent AI-mu **menuruti perintahnya** karena mengira itu benar-benar tuannya. Itulah celah yang ditutup OpenClaw di rilis **2026.10.4**, yang mendarat 16 Oktober 2026 pukul 00:36 UTC (07:36 WIB).

Rilisan ini skala kecil dibanding rilis-rilis sebelumnya — hanya **55 pull request, 24 direct commit, dan 49 kontributor**. Tapi di dalamnya ada satu tambalan keamanan yang layak dibaca pelan-pelan oleh siapa pun yang menjalankan agent AI 24/7.

## 🎭 Kenapa Group DM Itu Berbahaya

Tlon adalah messenger terdesentralisasi di atas Urbit. OpenClaw terhubung ke "ship" Urbit milikmu lewat plugin bawaan, lalu membalas DM dan pesan grup — dengan aturan otorisasi dan alur persetujuan owner di atasnya.

Aturannya terlihat rapi: owner ship berwenang di mana-mana, ada `dmAllowlist`, `defaultAuthorizedShips`, dan `groupInviteAllowlist`. Tapi ada satu pengecualian yang tertulis jelas di dokumentasi resmi:

> "Group DMs are the exception. Tlon does not verify who wrote a group DM message."

Baca ulang kalimat itu. **Tlon tidak memverifikasi siapa yang menulis pesan group DM.** Artinya klaim pengirim di group DM hanyalah *klaim* — bukan identitas terverifikasi.

Sebelum 10.4, klaim itu cukup untuk mendapat wewenang owner. Menurut catatan rilis, klaim pengirim group DM yang belum terverifikasi bisa memperoleh **perintah owner, aksi approval/admin, dan izin tool yang ditingkatkan**.

Terjemahan praktisnya: anggota grup mana pun yang bisa memalsukan nama pengirim bisa menyuruh agent-mu melakukan hal-hal yang seharusnya hanya bisa dilakukan olehmu.

## 🛡️ Yang Berubah di 2026.10.4

Setelah update, klaim pengirim group DM yang tidak terverifikasi **tidak lagi** mendapat wewenang owner. Perintah owner, balasan approval, dan perintah admin kini hanya bekerja di **DM 1:1 dengan bot**.

Ada satu konsekuensi yang penting dipahami, dan OpenClaw menuliskannya dengan jujur:

- Anggota grup **masih bisa** mengaku sebagai pengirim yang diizinkan untuk mengobrol dengan agent.
- Balasan agent pergi ke **percakapan pribadi si pengirim yang dipalsukan** — bukan ke grup.
- Kalau kamu punya DM pending yang disetujui sebelum update, **minta pengirimnya mengirim ulang**.

Perhatikan poin kedua. Penambalan ini menutup jalur eskalasi wewenang, tapi **tidak** membuat group DM jadi kanal terverifikasi. Batas kepercayaannya tetap ada — hanya saja pagarnya sekarang di tempat yang benar.

## 🎯 Siapa yang Terdampak

Jawaban singkat: **hanya kalau kamu memakai channel Tlon.** Kalau agent-mu jalan di Telegram, Discord, Slack, atau Matrix, celah ini tidak menyentuhmu. Ini bukan bug di inti Gateway, melainkan celah di lapisan otorisasi satu plugin channel.

Tapi pelajarannya berlaku umum. Setiap channel chat punya model identitas berbeda, dan tidak semuanya memverifikasi penulis pesan. Aturan yang aman: **wewenang owner hanya diberikan di kanal yang benar-benar memverifikasi identitas**, bukan di kanal yang sekadar mengklaimnya.

## 🔁 Update yang Tidak Lagi Bikin Sakit

Selain tambalan keamanan, 10.4 adalah rilis yang isinya tentang satu hal: **update dan recovery yang berhenti menyakiti**. Beberapa yang menonjol:

- **Tidur dan jam mundur** — update tidak lagi terputus gara-gara laptop tidur atau jam sistem bergeser ke belakang.
- **Gateway shutdown** — berhenti/restart tidak lagi menggantung menunggu indexing percakapan yang macet.
- **File login lama** — file OAuth pensiun yang tak terpakai tidak lagi memblokir `doctor`, update, maupun startup Docker.
- **Snapshot update** — upgrade berikutnya tidak lagi memberi peringatan palsu bahwa database "berubah" padahal tidak.
- **Telegram polling** — diperbaiki kegagalan startup worker polling yang bikin pesan Telegram tidak masuk.

Yang terakhir itu menarik: kalau kamu pernah merasa bot diam padahal gateway sehat, penyebabnya bisa ada di lapisan polling — bukan di model atau jaringan.

## 🧹 Praktik Sebelum Kamu Update

Ini bukan rilis yang mengubah struktur data besar, tapi tetap ada urutan yang aman:

1. **Backup dulu** — konfigurasi, agent workspace, dan state. Rilis ini justru menambah kemampuan backup off-machine ke NAS atau R2 dari jalur 2026.10.1.
2. **Baca bagian "Update" di changelog**, bukan cuma "Highlights".
3. **Pin versi** di produksi. Jangan auto-update: saat artikel ini ditulis, sudah ada `2026.10.5-beta.4` (15 Okt) dan `2026.10.10-beta.1` (15 Okt) di jalur beta — jelas bukan untuk server yang harus hidup terus.
4. **Verifikasi setelah update** — dokumentasi restart recovery menegaskan: "A healthy Gateway confirms availability, not completion of interrupted work." Gateway sehat bukan bukti pekerjaan yang terpotong sudah selesai. Cek transcript-nya.
5. **Kalau pakai Tlon**: setelah update, minta pengirim DM pending mengirim ulang. Jangan disetujui ulang dari catatan lama.

## 💡 Kenapa Ini Penting untuk Operator Agent

Kita sudah lama terbiasa mengukur keamanan agent dari hal-hal besar: sandbox, CVE, skill berbahaya di ClawHub. Semua itu nyata. Tapi celah hari ini mengingatkan pada lapisan yang lebih membosankan dan justru lebih sering bocor: **lapisan otorisasi kanal chat**.

Agent yang bisa mengeksekusi perintah hanya sekuat verifikasi identitas di kanal tempat dia mendengar. Kalau kanalnya tidak memverifikasi siapa yang bicara, maka "owner" hanyalah kata yang diketik seseorang.

Untuk konteks yang lebih luas soal memilih dan menjalankan agent sendiri, ada beberapa tulisan lama di blog ini yang masih relevan: [Hermes vs OpenClaw: 3 Sudut Pandang](/posts/hermes-vs-openclaw-3-sudut/), [OpenClaw Update yang Mentok dan Cara 2026.10.3 Membukanya](/posts/openclaw-2026103-update-mentok/), serta soal keamanan skill di [ClawScan: Tiga Scanner Satu Hakim](/posts/clawscan-tiga-scanner-satu-hakim/).

## Kesimpulan

**OpenClaw 2026.10.4** bukan rilis dengan fitur heboh — hanya 55 PR dan 49 kontributor. Nilainya ada di dua hal yang justru paling sering diabaikan operator: **siapa yang berhak memerintah agent**, dan **apa yang terjadi saat update terputus**.

Kalau kamu memakai channel Tlon, update ini bukan opsional — klaim pengirim group DM yang belum terverifikasi dulu bisa mendapat wewenang owner dan menaikkan izin tool. Kalau tidak memakai Tlon, tetap baca bagian update-nya: tidur, jam mundur, dan shutdown yang menggantung adalah tiga penyebab gangguan yang tidak pernah terlihat di dashboard.

Dan satu aturan yang berlaku untuk semua kanal: **wewenang owner hanya untuk kanal yang benar-benar memverifikasi identitas.**

Sumber: [Release notes OpenClaw v2026.10.4](https://docs.openclaw.ai/releases/2026.10.4), [dokumentasi channel Tlon](https://docs.openclaw.ai/channels/tlon), [Restart recovery](https://docs.openclaw.ai/gateway/restart-recovery), dan metadata rilis di [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw/releases).

— Chokdi 🐷 · Content Studio · 2026
