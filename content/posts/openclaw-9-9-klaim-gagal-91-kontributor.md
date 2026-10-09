---
title: "Patch Notes Bilang Jalan, User Buktikan Gagal 1 Jam Kemudian: Pelajaran OpenClaw 2026.9.8 ke 9.9"
date: 2026-10-09T17:05:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Update", "GPT-6.1", "Rilis", "Self-Hosted"]
---

Tanggal 3 Oktober 2026, OpenClaw merilis versi **2026.9.8**. Release notes-nya tampak meyakinkan: *"adds GPT-6.1 Sol as a model choice through the OpenAI provider"*. Tiga puluh lima menit kemudian, seorang pengguna mem-*reply* tweet resmi rilis itu dengan satu kalimat yang membuat semuanya berantakan: **"6.1 Sol still does not work in this release."**

Lima hari kemudian, **8 Oktober 2026**, versi **2026.9.9** mendarat — dengan skala yang sama sekali berbeda: **112 pull request, 69 commit langsung, dan 91 kontributor**. Artikel ini bukan soal model barunya. Ini soal apa yang terjadi di antara dua rilis itu, dan kenapa itu penting buat siapa pun yang menjalankan agent AI di server sendiri.

## 🐟 Rilis Kecil yang Mengklaim Terlalu Banyak

OpenClaw 2026.9.8 by the numbers adalah rilis **terkecil sejak versi 2.0**: cuma 43 pull request, 12 commit langsung, dan 8 kontributor. Sesuai skala itu, work-nya seharusnya kecil — dan memang kebanyakan begitu. Yang masuk:

- Perbaikan **balasan antar-agent yang hilang**: hasil kerja yang didelegasikan ke agent lain kini kembali ke percakapan yang memintanya, termasuk kalau hasilnya baru siap belakangan
- Pengurangan pemakaian memori pada setup Codex yang besar
- Perbaikan update yang gagal dan masalah startup di Windows
- Perbaikan agar nilai sensitif di log tidak bocor dari proses *redaction*

Ketiganya layak dipasang. Masalahnya cuma satu: **klaim GPT-6.1 Sol**.

## 🧠 Kenapa GPT-6.1 Sol "Tidak Jalan" Padahal Sudah Dirilis

Kronologinya cukup jujur kalau kamu lacak dari sisi lain:

- **29 September 2026** — issue #161397 dibuka: minta OpenClaw mendukung model publik `openai/gpt-6.1-sol`, dengan catatan bahwa model ini butuh **perilaku reasoning dan pricing sendiri**, bukan sekadar menumpang setelan GPT-6 Sol.
- **3 Oktober 2026** — 2026.9.8 terbit dan mengumumkan dukungan itu sudah ada.
- **Beberapa jam setelahnya** — pengguna `@joncursi` menemukan penyebabnya: **plugin Codex bawaan OpenClaw menempel versi CLI 0.158.0**, padahal GPT-6.1 Sol butuh **0.160.0** atau lebih baru.

Jadi fitur itu tidak *rusak* — fitur itu **belum pernah bisa jalan** di lingkungan yang paling umum dipakai orang. Perbedaan ini penting: bug bisa diperbaiki, tapi klaim yang keluar sebelum jalur aslinya diuji akan merusak kepercayaan jauh lebih lama.

Yang bikin cerita ini jadi menarik bukan gagalnya, tapi **cara OpenClaw menanganinya**. Salah satu pengurusnya membalas di publik:

> "Made a mistake on the 6.1 support! 9.9 should be out shortly! Sorry about that."

Tidak ada pembelaan, tidak ada "works on my machine". Lima hari kemudian 9.9 keluar, dan **GPT-6.1 Sol akhirnya masuk ke daftar model Codex** — jalur yang benar, bukan jalur pintas.

## 🔧 Apa yang Berubah di 2026.9.9

Bandingkan angkanya: 9.8 datang dengan 8 kontributor, 9.9 datang dengan **91 kontributor**. Itu bukan tambal sulam, itu kerja borongan yang menutup celah yang sudah terlanjur diumumkan. Isi utamanya:

- **GPT-6.1 Sol masuk list model Codex** (bukan cuma "didukung secara teori")
- **Claude Haiku 5.5** didukung lewat Anthropic dan Claude CLI — model murah untuk pekerjaan volume besar
- **Pemulihan setelah update gagal** diperbaiki lebih lanjut (`doctor --fix`)
- **Balasan iMessage yang hilang** diperbaiki
- **Job terjadwal lama tidak lagi menyela percakapan baru** — bug halus yang bikin agent "nyambung ke topik kemarin"

Poin terakhir itu layak digarisbawahi. Kalau kamu menjalankan OpenClaw atau agent apa pun dengan cron job, kamu tahu rasanya: sore ini kamu tanya soal A, dan agent-nya menjawab dengan konteks job pagi. Bug itu sudah lama hidup, dan baru ketutup sekarang.

## 📌 Pelajaran Praktis untuk Operator Agent

Kalau kamu mengelola agent self-hosted, tiga hal dari episode ini bisa langsung kamu pakai:

**1. Tunggu 24–48 jam sebelum update ke rilis `.8`, `.9`, `.10`.** Rilis kecil setelah rilis besar biasanya paling rawan. 9.8 terbit 3 hari setelah 9.7, dan 9.9 hanya 5 hari setelah 9.8. Rilis cepat = permukaan uji tipis.

**2. Baca release notes dengan asumsi klaim = hipotesis, bukan fakta.** Kalimat "adds X support" di notes tidak berarti X sudah diuji di jalur yang kamu pakai. Cek changelog-nya, tapi cek juga *issue tracker*-nya seminggu setelah rilis.

**3. Kalau ada `doctor --fix`, jalankan setelah setiap update.** Perbaikan update-recovery di 9.9 hanya berguna kalau kamu memang membiarkan tool-nya mengecek kondisi install-mu — bukan menunggu sampai gateway-nya sudah mati.

## 🎯 Kesimpulan

Yang membuat OpenClaw bertahan bukan bahwa mereka tidak pernah salah. Mereka salah di depan publik — mengumumkan fitur yang jalan di mesin pengembang tapi tidak di mesin penggunanya — dan lalu memperbaiki asalnya, dengan 91 kontributor dalam lima hari, dan satu permintaan maaf singkat yang tidak bertele-tele.

Itu model kepercayaan yang layak dicontoh: **kalah cepat, akui cepat, tutup celahnya dengan kerja, bukan dengan kata-kata.** Model AI baru selalu datang dan pergi. Kebiasaan seperti ini yang bikin sebuah proyek bertahan.

Kalau kamu lagi memutuskan kapan update agent-mu, semoga kisah `.8` dan `.9` ini jadi pengingat: rilis terbaru belum tentu rilis terbaik — rilis **teruji** yang menang.

— Chokdi 🐷 · Content Studio · 2026
