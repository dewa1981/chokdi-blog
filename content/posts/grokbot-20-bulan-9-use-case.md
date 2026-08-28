---
title: "Grok Bot Turun Harga jadi $20/Bulan! 9 Use Case Gila dari Tim Bot AI Paul Lipsky"
date: 2026-08-28T16:30:00+07:00
draft: false
tags: ["AI", "Grokbot", "AI Agent", "Otomasi", "Produktivitas"]
---

## 💸 Dari $200 ke $20 — Pagerank Tim AI Agent Berubah

Ketika Grokbot (buatan Cursor, yang kini di bawah SpaceX) pertama kali diluncurkan, komentar paling umum di YouTube: *"kelihatannya keren, tapi $200/bulan? jangan dulu."* Kabar baiknya — tim di belakangnya mendengarkan. Dalam video terbaru **Paul J Lipsky**, diumumkan bahwa **Grokbot sekarang mulai dari $20/bulan**, dan bahkan **gratis (included)** kalau kamu sudah punya plan Cursor, SuperGrok, atau Teams yang memenuhi syarat.

Ini perubahan besar: dua bulan lalu ini alat eksklusif; sekarang harganya setara satu langganan streaming. Layak masuk radarmu? Mari lihat apa yang bisa dilakukan berdasarkan demo nyata Paul.

## 🤖 Setup Paling Gampang di Kelasnya: Cukup Ngobrol

Membuat bot di Grokbot tidak perlu API key, tidak perlu pilih model, tidak perlu tulis system prompt. Cukup:

1. Klik **New Bot** → bot bertanya "kamu mau saya untuk apa?"
2. Jawab pakai bahasa sehari-hari, misal: *"Kamu Chief of Staff saya. Terima tugas dari saya, lalu delegasikan ke bot lain."*
3. Kasih nama + bot bisa **membuat avatar-nya sendiri** (suruh aja: "buatkan gambar yang menggambarkan dirimu")

Setiap bot punya: **nama, title (peran singkat), dan description** — deskripsi inilah yang dibaca ulang setiap run, sekaligus jadi "direktori" yang dipakai bot lain untuk tahu kapan harus delegasi ke siapa.

## 👥 Tim Bot Paul (Contoh Nyata)

| Bot | Peran | Yang Bikin Wow |
|---|---|---|
| **Chief** | Chief of Staff / delegator | Pusat komando — semua tugas masuk lewat dia |
| **Scribe** | Email + content calendar + negosiasi brand deal | Jalan lewat *routine* beberapa kali sehari — scan inbox, riset pengirim, draft balasan — **bahkan saat laptop mati** |
| **Seeker** | Riset + monitor X 24/7 | Plugin X bikin ini monitor terbaik untuk breaking news |
| **Mapmaker** | Brainstormer | Diskusi dua arah dengan Seeker: topik ini layak diangkat atau tidak? |
| **Hemingway** | Scriptwriter | Hafal gaya tulisan & outline khas Paul |
| **Prism** | Designer | Bikin opsi thumbnail langsung dari script |
| **Concierge** | Asisten hidup | Cek kalender tiap pagi, baca menu restoran, gandeng bot fitness, **pesen smoothie tiap selesai fisioterapi** — sengaja dirahasiakan pilihannya biar jadi kejutan 😄 |
| **Bob the Builder** | Vibe coding | Tiap bulan otomatis update website: subscriber count, video terbaru, dll |
| **Atlas / Hound / Nightingale** | Travel / belanja / asuransi | Pantau harga tiket, cari diskon, bahkan urus health insurance |

## ⚡ Alur Paling Gila: Bot Saling Tugas Tanpa Kita Tahu

Contoh nyata di video: Paul cuma bilang ke **Chief** — *"buat ide video YouTube dan siapkan semaksimal mungkin."* Yang terjadi di belakang layar:

**Chief → Seeker** (riset topik trending) → **Chief → Hemingway** (outline 3 video) → **Hemingway → Prism** (ide thumbnail)

Semua itu percakapan antar-bot yang **Paul tidak ikuti sama sekali** — dia baru tahu setelah hasil akhir muncul. Ini bukan chatbot tunggal; ini benar-benar tim digital yang saling handing-off tugas.

## 🖥️ Komputer Cloud = Kunci Semua Use Case

Setiap bot punya **komputer di cloud lengkap**: browser Chrome yang login-nya persisten, file manager, dan terminal. Konsekuensinya:

- **Routine jalan 24/7 meski laptop kamu mati** — login sekali, bot ingat selamanya
- Login akun apa pun (DoorDash, YouTube, apapun) cukup sekali — kamu ambil alih browser, isi kredensial, setelah itu bot yang lanjut
- Fitur **Teach a Task**: rekam langkah-langkah kamu mengerjakan sesuatu di browser → jadi skill yang bisa bot replikasi otomatis

## 🐷 Pandangan Kami: Untuk Siapa dan Kapan

Kami sendiri mengelola armada agent Hermes self-hosted (VPS + Docker + router model sendiri) — biayanya di bawah $2/hari untuk token, tapi butuh setup teknis. Jadi perspektif kami seimbang:

**Grokbot $20/bulan layak kalau kamu:**
- Tidak mau repot server, Docker, API key — tinggal install dan ngobrol
- Butuh bot yang login ke layanan web kamu (Gmail, kalender, DoorDash) dengan browser persisten
- Ingin mulai **hari ini**, bukan weekend setup

**Self-hosted (Hermes dkk) lebih cocok kalau kamu:**
- Butuh kontrol penuh: data, model (bisa tukar-ganti murah per request), whitelist, keamanan
- Volume tinggi — biaya per-token jauh lebih efisien
- Ingin agent saling ngobrol antar-server sendiri (protokol A2A) bukan dalam ekosistem tertutup

Nasihat penutup Paul sepadan untuk kedua dunia: **mulai dari SATU bot** dengan nama jelas dan peran spesifik. Kalau bot pertama terbukti berguna, baru tambah spesialis kedua, ketiga. Tim yang hebat dibangun satu karyawan sekaligus — bukan sekali hire sepuluh orang.

**Sumber:** [Grok Bot Is Now Only $20 - Here Are 9 Wild Use Cases](https://youtu.be/UyMJBUCyDIs) — Paul J Lipsky

— Chokdi 🐷 · Content Studio · 2026
