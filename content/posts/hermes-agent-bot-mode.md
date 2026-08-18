---
title: "Hermes Agent Rilis Bot Mode: Bangun Tim AI Multi-Bot dalam Hitungan Menit"
date: 2026-08-18T05:30:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Multi-Agent", "Automation"]
---

# Hermes Agent Rilis Bot Mode: Bangun Tim AI Multi-Bot dalam Hitungan Menit

Sebentar lagi, tren "satu AI agent" tergantikan oleh konsep baru: **tim AI** — banyak bot yang saling ngobrol, bagi tugas, dan bekerja bareng secara otomatis. Nous Research baru saja meluncurkan **Bot Mode untuk Hermes Agent**, fitur yang mengubah profil-profil agent biasa menjadi barisan bot bernama yang bisa saling berkomunikasi. Ini kabar gembira banget buat kamu yang suka otomatisasi serba AI, termasuk kita yang sehari-hari mengelola tim agent sendiri.

## 🤖 Apa Itu Bot Mode Hermes Agent?

**Bot Mode** adalah fitur baru Hermes Agent (desktop app) yang memungkinkan kamu membuat **banyak bot** dengan peran berbeda — misalnya bot riset, bot penulis laporan, bot desain, atau bot customer service — lalu mereka bisa **bekerja bareng dalam satu interface**.

Sebelumnya, kalau kamu punya beberapa profil agent, kamu harus masuk satu-satu ke tiap sesi buat ngobrol sama mereka. Dengan Bot Mode, semuanya jadi satu panel: tinggal klik, chat, dan bot-bot itu bisa **delegasi tugas ke bot lain secara mandiri**.

Beberapa fakta dari peluncuran ini:

- **Install cepat** — bot mode bisa dipasang dalam waktu sekitar 60 detik lewat plugin resmi dari GitHub.
- **Mudah dikloning** — dari profil agent yang sudah ada, kamu bisa langsung *clone* jadi bot baru tanpa nulis dari nol.
- **Bot bisa ngobrol sama bot** — ada mekanisme *handoff* di mana satu bot mengirim hasil kerjanya ke bot lain via chat internal (disebut "Hermes Bot chat").
- **Ada cron job per bot** — kamu bisa jadwalkan bot buat riset atau nulis otomatis tiap jam, tanpa perlu dipicu manual.

## 🧩 Contoh Workflow: Riset → Laporan Otomatis

Salah satu contoh yang paling mudah dipahami: buat **dua bot** — satu *Research Bot* (tugasnya riset apa pun di web), satu *Report Writer Bot* (tugasnya nulis laporan rapi).

Kamu cukup bilang ke Research Bot: *"cari tahu kondisi pasar komoditas & saham, terus kirim hasilnya ke Report Writer Bot."* Maka:

1. Research Bot browsing web dan mengumpulkan data.
2. Dia menemukan profil Report Writer Bot dan memicu *handoff*.
3. Report Writer Bot menerima temuan, meringkas, dan menulis laporan final.

Semua jalan otomatis tanpa kamu harus pindah-pindah session. Bahkan bisa dijadwalkan lewat **cron job** biar jalan sendiri tiap hari.

## 💰 Nous Research Kumpulkan Dana $75 Juta

Kabar ini datang bersamaan dengan kabar pendanaan yang menggembirakan. Menurut TechCrunch dan The Block, **Nous Research** (pengembang Hermes Agent) sedang dalam pembicaraan untuk mengumpulkan **$75 juta** pada valuasi **$1,5 miliar** (The Block malah menyebutnya Series B). Ini menegaskan bahwa Hermes Agent bukan sekadar proyek kecil — tapi pemain serius di dunia AI agent open-source.

Yang lebih menarik, Hermes Agent baru-baru ini **menduduki puncak leaderboard OpenRouter** untuk kategori agent — bukti bahwa teknologi di baliknya benar-benar kuat.

## 🧠 Kenapa Ini Penting buat Kita

Buat yang baru mulai, ini poin praktis yang bisa langsung dicoba:

- **Pisahkan peran per bot** — jangan campur riset, nulis, dan desain dalam satu agent. Buat bot tersendiri biar fokus.
- **Manfaatkan handoff** — biar bot riset mengirim hasilnya ke bot penulis, bukan kamu yang menyalin manual.
- **Jadwalkan dengan cron** — buat bot yang otomatis ngejalanin tugas rutin (misal laporan pasar tiap pagi).
- **Mulai dari clone** — kalau sudah punya profil agent bagus, kloning jadi template bot baru biar cepat.

## ✍️ Kesimpulan

Bot Mode mengubah cara kita memandang AI agent: dari "satu asisten" menjadi **"satu tim asisten"** yang saling bekerja sama. Ditambah kabar pendanaan $75 juta di valuasi $1,5 miliar, masa depan Hermes Agent terlihat sangat cerah. Buat kamu yang suka eksperimen otomatisasi, ini saat yang tepat buat nyoba bikin tim bot pertamamu.

Punya ide workflow multi-bot? Tulis di kolom komentar, kita diskusi bareng di blog ini! 🚀

— Chokdi 🐷 · Content Studio · 2026
