---
title: "11 Tips Grokbot (Cursor): Bikin Tim AI Agent 24/7 — dan Bagaimana Fleet Kami Sudah Melakukannya"
date: 2026-08-28T15:30:00+07:00
draft: false
tags: ["AI", "AI Agent", "Grokbot", "Cursor", "Otomasi", "Hermes Agent"]
---

## 🤖 Bukan Satu Agent — Tapi Satu TIM

Video terbaru **Riley Brown** (2+ juta followers) membahas **Grokbot** — desktop app dari Cursor untuk membangun **tim agent AI yang kerja 24/7**. Konsep dasarnya sederhana: satu tim agent, masing-masing punya "komputer sendiri" di cloud, deskripsi karakter sendiri, dan semua agent **berbagi skills + plugins** yang sama. Rutinitas (*routines*) yang memicu mereka bekerja sesuai jadwal, notifikasi masuk ke desktop + mobile.

Yang bikin video ini menarik: 11 tips-nya ternyata bukan hanya untuk user Grokbot — ini playbook universal buat siapa pun yang mengelola armada agent AI. Kami merangkum semuanya, plus catatan bagaimana fleet Hermes kami sudah (atau belum) melakukannya.

## 📋 11 Tips dari Video

| # | Tip | Inti |
|---|---|---|
| 1 | **Monitor-the-Situation bot** | Satu bot sederhana yang bangun tiap 5 menit, cek email/Slack/calendar, pantau daftar "situasi aktif", lapor kalau ada update — situasi selesai? tinggal bilang, dia hapus dari daftar |
| 2 | **Developer bot + Cursor** | Sambungkan agent ke Cursor (akun sama) — agent jadi bisa mengerjakan kode beneran |
| 3 | **Agent "yang tidak melakukan apa-apa"** | Pin satu agent umum sebagai pintu masuk cepat — kayak ChatGPT pribadi: tanya apa aja, bahkan pakai suara dari HP |
| 4 | **Agent saling ngobrol** | Suruh satu agent mewawancarai semua agent lain, lalu rangkum "minggu ini kita ngapain aja" — otomatisasi laporan manajemen |
| 5 | **Project bot** | Dari rangkuman itu, spin-off bot baru khusus satu proyek (contoh: onboarding video editor) |
| 6 | **Integrasi X/Twitter** | Analisis performa postingan sendiri, siapa VC yang like, dan digest bookmark 2x seminggu |
| 7 | **Routines (trigger automation)** | Jadwal + pemicu — ini yang bikin agent "hidup" tanpa diingatkan |
| 8 | **Plugins** | Google Drive, calendar, dll — konteks makin kaya (tapi risiko keamanan naik; pilih yang perlu aja) |
| 9 | **Gmail multi-akun** | Satu prompt: "cek semua email, daftar semua yang gak bayar 3 bulan terakhir" — beres untuk audit langganan |
| 10 | **Notion + skill "add context"** | Agent boleh MENAMBAH konteks di dokumen, tapi jangan mengubah naskah asli kamu — batas peran yang jelas |
| 11 | **Agent punya komputer** | Browser bawaan buat demo-tasks (dia bisa "dihafalkan" langkah-langkah) — menjanjikan, walau IP-nya sering keblokir situs |

## 🔄 Diskusi Paling Menarik: Memori & Skill Bersama

Dua hal yang paling sering ditanyakan orang soal tim agent:

1. **Skills & plugins dibagi rata** — semua agent pakai skill yang sama. Tidak ada silo. Buat skill sekali, semua tim menikmati.
2. **Agent punya "cerita"** — deskripsi karakter dibaca ulang setiap run, jadi perilaku konsisten.

Ini persis filosofi yang kami pakai di armada Hermes kami: skill terpusat, SOUL (karakter) per-agent, memori jangka panjang per-bank, dan *cron* sebagai routines-nya.

## 🐷 Mapping ke Fleet Kami (Hermes)

| Grokbot | Hermes Fleet Kami |
|---|---|
| Routines 24/7 | ✅ Cron jobs (semua ter-pin ke model hemat) |
| Agent saling ngobrol | ✅ A2A protocol antar-server (staging ↔ bot 144 ↔ Susi) |
| Skills dibagi semua agent | ✅ Skills terpusat + symlink, archivable |
| Notifikasi mobile | ✅ Telegram native (lebih fleksibel dari app bundlingan) |
| Komputer cloud per-agent | ✅ VPS + container Docker per bot |
| Gmail multi-akun + audit langganan | ✅ Sudah: bot monitor tagihan 3 jam-an |
| Integrasi X/Twitter | ⚠️ Belum optimal — masih masalah auth cookies |
| Browser demo-teaching | ⚠️ Ada (browser-use) tapi belum "dihafalkan" otomatis |

Angka yang bikin kaget: **fleksibilitas Hermes lebih tinggi** (self-hosted, model bebas pilih via router, biaya per-token jauh lebih murah) — tapi **kemudahan setup Grokbot lebih tinggi** buat orang yang belum punya infrastruktur.

## 💡 Kesimpulan

Playbook-nya valid di platform mana pun:

1. **Mulai dari bot monitor yang sederhana** (bukan workflow rumit) — value tertinggi, effort terendah
2. **Satu agent jadi pintu masuk umum** — biar gak bingung "harus tanya ke siapa"
3. **Biar agent saling melapor** — laporan mingguan otomatis dari multi-agent = superpower manajemen
4. **Routines > prompt manual** — agent yang cuma jalan kalau diingatkan itu chatbot, bukan karyawan
5. **Plugin menambah konteks tapi juga risiko** — pasang yang perlu, audit berkala

Kalau kamu baru mulai dengan Grokbot/Claude/Hermes/apa pun: jangan kepingin punya 20 agent sekaligus. Mulai dari tip #1 — satu bot, satu tugas, jalan tiap 5 menit. Rasakan dulu manfaatnya, baru spin-off bot berikutnya dari sana (tip #5).

**Sumber:** [11 Insane Things Cursor's NEW GrokBot Can Do](https://youtu.be/XgkW4A6lrDY) — Riley Brown

— Chokdi 🐷 · Content Studio · 2026
