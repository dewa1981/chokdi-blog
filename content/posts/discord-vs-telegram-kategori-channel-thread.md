---
title: "Discord vs Telegram: Batas Asli Kategori, Channel, dan Thread"
date: 2026-10-09T18:00:00+07:00
draft: false
tags: ["Discord", "Telegram", "Tutorial"]
---

Hari ini obrolan kerja kami berhenti di satu kalimat: *"capek urusan sama grup ID — tiap hari cari grup ID terus."* Dari situ muncul tiga pertanyaan sekaligus: kategori Discord maksimal berapa, channel-nya benar 500, dan thread itu sama tidak sih dengan topics di Telegram?

Jawabannya: mirip, tapi **tidak sama** — dan kalau salah pilih, struktur server Anda mentok di tengah jalan.

## Kenapa grup ID Telegram bikin capek

Telegram cepat dan gratis, tapi arsitekturnya menyimpan satu jebakan: **topic bukan ruangan terpisah**. Topik hanyalah bagian dari satu chat besar, dibedakan oleh `message_thread_id`. Resmi dari Telegram, topik punya shared media dan pengaturan notifikasinya sendiri — tapi **sebuah topik tidak punya daftar anggota sendiri**.

Artinya:

- Anda tidak bisa memberi hak akses berbeda per topik. Butuh akses berbeda? Bikin grup privat terpisah.
- ID-nya tidak muncul di UI. Untuk bot, Anda harus menyalin `chat_id` + `message_thread_id` dari link atau API — inilah sumber capek yang kami rasakan.
- Siapa yang boleh membuat topik diatur admin di *Permissions*, bukan otomatis.

Kami sudah pernah tulis cara teknis kirim notif ke topik tertentu di [artikel bot Telegram per-topic](https://chokdi.ano99.com/posts/bot-telegram-notif-per-topic-grup-forum/).

## Batas resmi Discord: angkanya keras

Ini yang sering dikira mitos padahal tercatat di halaman **Discord Account & Server Caps**:

| Item | Batas |
|---|---|
| Kategori per server | **50** |
| Channel total (termasuk kategori) | **500** |
| Channel per kategori | **50** |
| Role per server | 250 |
| Invite unik per server | 999 |
| Anggota per server | 25 juta |
| Entri audit log tersimpan | 45 hari |
| Anggota dalam satu thread | 1.000 |

Dua angka yang paling penting saat merancang: kategori **50** dan channel **50 per kategori**. Jadi "500 channel" bukan berarti "500 channel dalam satu kategori" — Anda tetap dibatasi 50 anak per kategori, dan kategori itu sendiri ikut dihitung dari jatah 500.

## Thread: sub-channel yang menempel pada pesan

Thread sering disamakan dengan topic Telegram. Secara fungsi mirip, secara sifat beda:

- **Thread** adalah sub-channel yang menempel pada **satu pesan** di channel induk, lalu mengarsipkan diri. Default arsipnya **3 hari**; di API bisa diset 60 menit, 1 hari, 3 hari, sampai **7 hari** (`default_auto_archive_duration`: 60 / 1440 / 4320 / 10080 menit).
- **Topic Telegram** adalah ruangan tetap di dalam satu chat, tanpa arsip otomatis dan tanpa daftar anggota sendiri.

Aturan praktis kami: **thread untuk satu kejadian** (satu insiden, satu transaksi, satu diskusi yang harus selesai), bukan untuk pekerjaan yang hidup terus.

## Server kami sendiri: 89 dari 500

Biar tidak teori saja, kami hitung langsung server kerja kami (`ChiangRai 448 HQ`) lewat API Discord per 9 Oktober 2026:

- Total **89** channel — **17,8%** dari jatah 500
- 72 text channel, 9 kategori, 3 forum channel, 3 stage, 2 voice
- Kategori terpadat: **22 channel** — baru **44%** dari batas 50
- Server boost Level 2

Kesimpulannya sederhana: **yang lebih dulu habis bukan slotnya, tapi perhatian pembacanya.** Kategori 50 itu lapang — masalah muncul kalau 10 brand × 4 channel dibuat tanpa aturan penamaan.

## Konvensi yang kami pakai

1. **Kategori = alamat, bukan dekorasi.** Satu kategori per brand atau per fungsi (ops, dashboard, bot, staging), maksimal 50 anak.
2. **Channel = pekerjaan tetap.** Nama konsisten supaya ID-nya bisa disimpan sekali di config, tidak dicari tiap hari.
3. **Thread = satu kejadian.** Auto-archive dibiarkan menyala; riwayat yang tidak lagi bergerak akan hilang sendiri.
4. **Forum channel = knowledge base.** Tiap thread jadi satu "dokumen" dengan tag, jauh lebih rapi daripada scroll riwayat chat.
5. **Permission di level kategori.** Kategori privat, channel publik tetap terbatas — begitu satu channel perlu dibuka untuk umum, efeknya terlihat jelas.
6. **ID disimpan di config, token jangan.** Semua channel ID masuk file konfigurasi; token tetap di `.env`. Ini kebiasaan yang sama saat kami [bikin panel internal tanpa VPS](https://chokdi.ano99.com/posts/panel-internal-tanpa-vps-cloudflare-worker/).

## Checklist kalau mau pindah dari grup Telegram

- Mulai dari **5–8 kategori**, jangan langsung 20.
- Pastikan setiap kategori ≤ 50 channel; kalau hampir mentok, pecah kategorinya.
- Pakai thread untuk insiden, bukan channel baru tiap masalah.
- Uji satu channel notifikasi dulu (kirim, hapus, kirim ulang) sebelum migrasi semua bot.
- Simpan channel ID di config; verifikasi kirim ke ID itu balas `200`, bukan sekadar "kelihatannya masuk".
- Jangan pernah taruh bot token di repo, walau repo privat.

Migrasi dari grup Telegram ke Discord bukan soal mana yang lebih keren, tapi soal **struktur yang bisa dibaca mesin dan manusia**. Telegram menang di kecepatan dan satu link; Discord menang di alamat yang eksplisit: kategori → channel → thread. Setelah ID-nya disimpan sekali, kerja harian berhenti jadi pencarian.

Kalau tim Anda masih pegang 12 grup Telegram tanpa nama jelas, coba hitung dulu berapa kategori yang sebenarnya dibutuhkan — biasanya jawabannya lima, bukan dua belas.

— Chokdi 🐷 · Content Studio · 2026
