---
title: "Grok Bot $20/Bulan: 12 Use Case & 4 Power Moves yang Bikin Kerja Otomatis"
date: 2026-08-30T10:30:00+07:00
draft: false
tags: ["AI", "Grokbot", "AI Agent", "Otomasi", "Produktivitas", "Tutorial"]
---

Dua minggu lalu Grok Bot butuh $300/bulan. Sekarang mulai **$20/bulan** — dan baru-baru ini kanal *That AI Trick* merilis panduan lengkap berjudul *"Grok Bot Full Guide: 12 Use Cases That Feel Like Cheating"* yang membedah semua kemampuannya. Ini rangkuman lengkapnya: 12 use case, 4 power moves, plus **limitasi yang jarang dibahas** — biar kamu nggak beli kucing dalam karung.

## 🤖 Dulu vs Sekarang: Kenapa Harga Turun Drastis

Grok Bot (produk **SpaceX AI** — hasil merger xAI, dibangun oleh tim Cursor yang dibeli SpaceX $60 miliar) meluncur early-beta 11 Agustus 2026. Awalnya cuma plan $300. Per 26 Agustus, **semua plan Cursor ($20+) dan semua plan SuperGrok ($30+) sudah termasuk Grok Bot**.

Konsepnya beda dari chatbot biasa: Grok Bot **berpikir dalam peran, bukan tugas**. Kamu nggak buka "chat baru" tiap mau kerja — kamu punya **bot yang punya pekerjaan tetap**. Tiap bot terdiri dari 4 komponen:

1. **Profile** — nama + deskripsi pekerjaan. Deskripsi ini dibaca ulang setiap bot jalan, jadi bot nggak pernah lupa perannya.
2. **Komputer cloud** — satu mesin 24/7 dengan browser, file system, dan terminal. Bisa login ke portal/situs sekali, dan login itu disimpan.
3. **Plugin & skill** — Gmail, Calendar, Drive, Slack, Notion, X, dan marketplace. Connect sekali, semua bot bisa pakai.
4. **Routines** — jadwal ("tiap Senin & Kamis jam 8 pagi") atau trigger event ("kalau ada Slack message", "kalau ada git push", bahkan webhook).

## 🎯 12 Use Case dari Video

| # | Use Case | Yang Dilakukan | "Wow"-nya |
|---|----------|----------------|-----------|
| 1 | **Email triage** | Bot "Inbox" sortir 40 email/hari jam 7:30, arsip otomatis, draf balasan pakai gaya suaramu, approval sebelum kirim | 40 email → cuma 4 yang butuh kamu, 10 menit |
| 2 | **Label Gmail** | Bot kasih label otomatis: wholesale, supplier, customer, sponsor, noise | Gmail kebersihan tanpa usaha |
| 3 | **Calendar bot** | Brief 30 menit sebelum meeting (siapa, history, yang masih open) + pindahin jadwal cukup 1 kalimat | Nggak perlu buka 3 aplikasi |
| 4 | **Meeting notes** | Transcript rapat → summary + action items + auto-assign via Slack | 20 menit setelah rapat, kerjaan udah jalan |
| 5 | **Browser work** | Bot buka browser cloud, bandingin harga supplier, isi form, unduh invoice — termasuk fitur **Teach a Task** (kamu demo 1x, bot rekam jadi skill) | Bot bisa "belajar" dari gerakanmu |
| 6 | **Coding tanpa editor** | Bot "dev" = project manager: bikin plan → delegate ke Cursor agents → PR siap + screenshot | Kamu lihat plan, screenshot, dan tombol — bukan kode |
| 7 | **Personal bot** | Pesan makan siang, cek kalender pribadi — **selalu berhenti di pembayaran** | Aturan uang: selalu minta "yes" |
| 8 | **Bersihkan laptop** | Jalan di komputermu sendiri (execution on local computer): cari file gede >90 hari, tanya dulu sebelum hapus | 11GB balik tanpa takut salah hapus |
| 9 | **Messenger** | ⚠️ Belum ada bridge Telegram/WhatsApp resmi — orang wiring manual (hack, bukan fitur) | Official cuma: iPhone app + push notification per bot |
| 10 | **Content bot** | Plugin X: analisis post terbaik, lead list dari likes, draf 3 post pakai suaramu | Lead list muncul dari tombol like! |
| 11 | **Quotes dari file** | Spreadsheet masuk → bikin quote pakai price sheet di Drive → flag diskon >10% → handoff ke bot email | Spreadsheet → email kirim dalam 4 menit |
| 12 | **Sunday review** | Bot "Atlas" tanya SEMUA bot 1 minggunya → 1 halaman ringkasan + 3 keputusan | Review mingguan jadi bacaan kopi pagi |

## 💪 4 Power Moves (yang Bikin Tim Bot JADI SISTEM)

**1. Chief of Staff ("Atlas")** — satu pintu masuk. Deskripsinya cuma: *"delegasikan dulu ke bot lain kalau ada yang lebih cocok, baru kerjakan sendiri."* Kamu tanya Atlas 1 kalimat → Atlas ngobrol sama Scout, Dev, Cal → balas 1 paragraf: 3 blocker, 2 owner, 1 tanggal. **Bot bisa saling kirim pesan** (baca-only buat kamu) dan ada group chat 2-6 bot.

**2. Skill "Grill Me"** — bot mewawancarai kamu habis-habisan tentang goals, constraints, decision makers, sampai paham konteks. Hasilnya disimpan jadi **shared knowledge** (file di cloud computer yang dibaca semua bot baru).

**3. Bot yang "Watch"** — cek Slack/email/kalender tiap 5 menit, **diam kalau nggak ada perubahan**, notif cuma kalau ada update. Plus routines bisa dipicu **event & webhook**: pesan Slack, git push, order masuk >$500, dll.

**4. Project bots + Pallet + Log** — 1 bot per project besar (konteks nggak nyampur), pallet ⌘K buat navigasi cepat, dan aturan "setelah selesai kerja, tulis 1 baris ke Notion" → 1 halaman berisi aktivitas seluruh tim.

## ⚠️ Limitasi yang Jarang Dibahas (Penting!)

- **Nggak ada model picker** — model Grok di-route otomatis, kamu nggak bisa pilih.
- **Satu komputer cloud dishare semua bot** — kalau macet, semua macet bareng; bot satu bisa lihat file/session bot lain (bukan tembok isolasi — hati-hati buat bot client!).
- **Browser cloud sering kena captcha** — bot bakal serahin ke kamu buat diselesaikan.
- **Usage boros** — limits bisa habis dalam hitungan hari; set monthly limit manual.
- **Belum ada audit log** terpusat.
- **No Android, no iPad, no Linux app** resmi — cuma Mac, Windows, iPhone.

## 🐷 Pandangan Kami: Grok Bot vs Armada Hermes

Kami sendiri menjalankan armada agent Hermes self-hosted (VPS + Docker + model router sendiri), jadi penilaiannya seimbang. **Grok Bot cocok kalau kamu:** nggak mau urus server/Docker/API key, butuh bot yang login ke layanan webmu, dan mau mulai hari ini juga.

**Armada self-hosted (Hermes) menang kalau kamu:** butuh kontrol penuh (model bisa ganti-ganti murah, data di tangan sendiri), volume tinggi (biaya per-token jauh lebih efisien), dan butuh isolasi ketat antar agent. Baca juga: [Grok Bot Turun ke $20/Bulan: 9 Use Case dari Paul Lipsky](/posts/grokbot-20-bulan-9-use-case/) dan [11 Tips Membangun Tim Agent AI](/posts/grokbot-11-tips-tim-agent-ai/).

Nasihat penutup yang sepadan untuk semua dunia: **mulai dari SATU bot** dengan nama jelas dan peran spesifik. Tim yang hebat dibangun satu karyawan sekaligus — bukan sekali hire sepuluh orang.

**Sumber:** [Grok Bot Full Guide: 12 Use Cases That Feel Like Cheating](https://youtu.be/_zi2VLRuZa4) — That AI Trick (30 Agu 2026)

— Chokdi 🐷 · Content Studio · 2026
