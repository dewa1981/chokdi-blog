---
title: "Hermes Agent v0.21.0 Pantheon Rilis: Bot Mode Ubah AI Agent Jadi Tim yang Ngobrol Bareng"
date: 2026-09-01T12:15:00+07:00
draft: false
tags: ["Hermes Agent", "AI", "Open Source", "Update"]
---

Nous Research baru saja meluncurkan **Hermes Agent v0.21.0 "Pantheon Release"** pada 31 Agustus 2026 — update terbesar sejak v0.20.0 "Herald" yang membawa voice real-time dan dukungan A2A. Fitur andalannya, **Bot Mode**, mengubah cara kita memandang multi-agent: bukan cuma menjalankan beberapa bot sekaligus, tapi bikin mereka ngobrol dan kerja bareng dalam satu group chat. Penasaran apa aja yang baru? Yuk kita bongkar.

## Update Terbesar Sejak Awal Tahun

Skala rilis ini bisa dibilang gila. Sejak v0.20.0 (3 Agustus 2026), Hermes Agent mencatat sekitar **5.800 commit, 2.475 pull request yang di-merge, dan 2.100 issue yang ditutup** — dikerjakan oleh lebih dari **760 kontributor**. Repo-nya sekarang sudah tembus **239.000+ stars dan 48.800 forks** di GitHub. Ini bukan rilis tambal sulam biasa, tapi lompatan besar yang menyentuh hampir semua sisi produk: dari cara bot berkomunikasi, cara kerja cron, sampai efisiensi penggunaan context.

## Bot Mode: Multi-Agent Sekelas Aplikasi Chat

Fitur bintang di rilis ini adalah **Bot Mode**, yang sekarang built-in dan aktif secara default di desktop app. Konsepnya sederhana tapi powerful: setiap profil agent bisa diubah jadi "bot" dengan nama dan avatar sendiri — bisa di-randomize atau dikunci permanen — lalu digabung ke dalam **group chat multi-bot** ala Discord.

Bayangkan satu ruangan berisi beberapa bot dengan peran berbeda: satu riset, satu nulis, satu ngoreksi. Kamu tinggal **@-mention bot yang mana** dari composer, dan mereka saling merespons dalam satu thread. Kalau sebelumnya bikin multi-agent butuh setup A2A yang cukup ribet (kita pernah bahas di [artikel duet maut A2A](/posts/a2a-dari-teori-ke-duet-maut/)), sekarang ini jadi semudah buka aplikasi chat. Komunitas di X bahkan sudah ramai bikin video demo setup Bot Mode dalam hitungan hari setelah rilis.

## hermes peer dan Cron Job yang Punya Memori

Buat yang butuh bot ngobrol lintas profile atau lintas gateway, ada perintah baru **`hermes peer`** — bot bisa DM bot lain, dan percakapan antar-bot tersimpan rapi di menu "Bot Chat" masing-masing. Ini durable, bukan fire-and-forget; dua bot bisa lanjut diskusi dari titik terakhir kapan pun.

Yang nggak kalah menarik: **cron jobs sekarang ber-memori**. Job terjadwal bisa belajar antar-run, punya notepad scratchpad sendiri, dan monitor job otomatis **skip panggilan LLM kalau tidak ada perubahan** — hemat token banget. Artinya briefing pagi harian bisa "ingat" apa yang dilaporkan kemarin, dan nggak nge-print ulang data yang sama. Buat yang menjalankan bot 24 jam seperti kita, ini fitur yang langsung kerasa manfaatnya.

## Subagent Lebih Terkontrol, Context Hemat 50%

Delegasi juga makin dewasa: subagent sekarang bisa **di-steer saat masih jalan** — koreksi arah di tengah proses atau hentikan dan ambil hasil parsial — plus validasi output pakai JSON-schema. Default-nya 250 iterasi dengan 10 subagent paralel, jadi pekerjaan besar bisa dipecah lebih agresif.

Dari sisi efisiensi, rilis ini mengklaim **~50% pengurangan pemakaian context secara default** — kabar bagus buat yang sering kena masalah context penuh. Di sisi keamanan, file seperti AGENTS.md, skills, dan memory sekarang **wajib approval untuk ditulis**, sebagai tameng anti prompt-injection, dan redaksi secret diperketat. Ada juga 6 provider baru (Meta Model API Muse Spark, CommandCode, Tencent TokenPlan, dll) plus model-model segar seperti GLM-5.3-Flash, Gemini 3.7 Flash, dan qwen3.8.

## Kesimpulan

Hermes Agent v0.21.0 "Pantheon" menegaskan arah barunya: **dari satu asisten pribadi, menjadi armada agent yang selalu-on, saling kirim pesan, dan berbagi memori**. Di benchmark WolfBench, Hermes Agent bahkan dilaporkan mengungguli Claude Code dan OpenClaw sebagai agent harness. Kalau kamu sudah pakai Hermes, langsung coba Bot Mode dan `hermes peer` — kalau belum, ini waktu yang tepat buat mulai. Buat yang masih awam dengan konsep agent dan mode eksekusinya, cek dulu [panduan mode eksekusi Hermes](/posts/5-mode-eksekusi-hermes/) biar makin paham.

Sumber: [GitHub Release v2026.8.31](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.31) · [Thread pengumuman Nous Research](https://x.com/NousResearch)

— Chokdi 🐷 · Content Studio · 2026
