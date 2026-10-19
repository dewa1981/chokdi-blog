---
title: "Hermes v0.22 Threshold: Setup Tanpa API Key, Tapi Cek 1 Setelan Ini Dulu"
date: 2026-10-20T01:20:00+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Nous Research", "Update", "Self-Hosting"]
---

Nous Research merilis **Hermes Agent v0.22.0 "Threshold"** pada 13 Oktober 2026 — dan jujur saja, ini rilis terbesar yang pernah mereka keluarkan: **~24.200 commit, ~6.080 pull request, 2.520 kontributor**, sekitar 2,5x lipat siklus v0.21.0. Tapi yang bikin rilis ini beda bukan angka besarnya, melainkan satu kalimat di catatan rilis: *"a newcomer is talking to Hermes before they own an API key."*

Artinya? Sekarang orang baru bisa pakai agent AI tanpa daftar akun, tanpa bayar, tanpa nyentuh terminal. Justru di situ ada satu setelan yang **wajib kamu cek dulu sebelum pencet update**.

## 🚪 Apa Itu "Threshold" dan Kenapa Namanya Begitu

Hermes adalah dewa ambang pintu dalam mitologi Yunani. v0.21.0 "Pantheon" mengumpulkan para dewa — agent jadi tim yang saling kirim pesan. v0.22.0 adalah soal **melewati pintu itu**: dari "orang yang sudah paham infrastruktur" jadi "siapa saja yang bisa buka aplikasi".

Tiga pintu yang dibukanya:

- **Setup lewat chat, bukan halaman setting.** Buka aplikasi desktop di komputer yang belum pernah pakai Hermes, dan yang muncul bukan form panjang — tapi percakapan pendek. Satu kartu per giliran: namamu, warna aksen, layout, aplikasi mana yang mau disambung, plugin mana yang mau dipasang. Lalu tur singkat dan sampai empat tugas pertama yang sudah dipilihkan.
- **Model gratis di awal.** Setup itu jalan di model trial `nous/welcome` (sekali per user OS), jadi kamu bisa ngobrol dengan agent sebelum punya key apa pun.
- **Model lokal satu klik.** Runtime `llama.cpp` dipasang otomatis dan Hermes memilih model yang pas dengan hardware-mu — prompt tidak pernah keluar dari mesin sendiri.

Buat kita yang biasa ngoprek VPS, ini kelihatan sepele. Tapi buat staf atau teman yang selama ini kita bantu setup manual lewat SSH, ini yang bikin beda.

## 🔌 Connectors: Agent Masuk ke Aplikasi yang Sudah Kamu Pakai

Bagian kedua yang paling praktis: **Connectors**. Agent tidak lagi cuma duduk di terminal menunggu disuruh — dia bisa dibawa masuk ke aplikasi yang kamu pakai sehari-hari, tanpa akun untuk mulai.

Di sisi lain, v0.22.0 juga merapikan hal-hal yang bikin pusing operator:

- **Rilis stable yang sudah dites.** Instalasi sekarang mengikuti rilis SemVer stable, jadi `hermes update` melompat dari satu rilis ke rilis berikutnya — bukan commit per commit seperti dulu.
- **Snapshot sebelum ubah apa pun.** Sebelum `hermes update` menyentuh kode, dia menyimpan snapshot config tiap profil, keys, dan cron job. Ini yang menyelamatkanmu kalau update terhenti di tengah.
- **Paket desktop ditandatangani**, termasuk versi Microsoft Store, dan satu package manager di bawah semuanya.
- **Katalog 600 plugin** yang sudah direview, plus gelombang model Claude 5.5 / GPT-6.

Dan satu lagi yang jarang disebut: **codebase-nya sepertiga lebih kecil**. Rilis ini membuang banyak kode mati sambil menambah fitur — prestasi tersendiri.

## ⚠️ Setelan yang Wajib Dicek: Auto-Prune Sesi

Ini poin yang paling penting buat siapa pun yang jalanin Hermes 24 jam — dan ini bukan teori, kita cek langsung di server sendiri.

Di **v0.22.0, auto-delete sesi lama AKTIF secara default**: sesi yang sudah berakhir dan tidak aktif selama `sessions.retention_days` (default **90 hari**) dihapus saat startup. Yang dihapus hanya sesi yang sudah berakhir — sesi aktif tidak pernah disentuh, dan umurnya dihitung dari aktivitas terakhir, bukan dari kapan dimulai.

Masalahnya: **riwayat sesi inilah yang bikin `session_search` bisa mengingat percakapan lama.** Kalau kamu andalkan agent untuk "ingat apa yang kita kerjakan bulan lalu", auto-prune akan memangkasnya pelan-pelan tanpa alarm.

Contoh nyata dari server staging kami:

```yaml
# /root/.hermes/config.yaml
sessions:
  auto_prune: true
  retention_days: 14
```

Dua baris itu artinya: setiap kali gateway start, sesi yang sudah berakhir dan nganggur lebih dari **14 hari** dihapus. Dengan `state.db` yang sudah **515 MB**, pemangkasan ini sebenarnya berguna — tapi kalau kamu tidak sadar, kamu baru tahu setelah agent bilang "aku tidak punya catatan itu".

Cara aman:

1. **Cek dulu** isi `config.yaml` bagian `sessions:` sebelum update.
2. Kalau riwayat penting, set `auto_prune: false`, atau naikkan `retention_days`.
3. Kalau database-nya sudah besar, lebih baik bersihkan **manual** dengan `hermes sessions prune` — kamu yang memutuskan kapan.

## 🧯 Kenapa v0.22.2 Penting (Jangan Loncat Langsung)

Rilis besar hampir selalu diikuti patch cepat, dan v0.22.0 bukan pengecualian. Catatan pembuka v0.22.2 (15 Oktober 2026) jujur sekali: **v0.22.1 dibangun dari commit yang salah** — ikut membawa pekerjaan gateway yang belum dirilis, dan aplikasi Microsoft Store bisa nyangkut di tulisan "Connecting". v0.22.2 adalah rilis yang seharusnya v0.22.1.

Jadi urutan yang benar: **v0.22.0 → v0.22.2**. Jangan berhenti di v0.22.1 hanya karena nomornya lebih baru dari sebelumnya.

## 🎯 Kesimpulan

v0.22.0 "Threshold" mengubah Hermes dari alat orang teknis jadi aplikasi yang bisa dibuka siapa saja — setup lewat chat, model lokal satu klik, connectors, dan update yang jauh lebih aman karena selalu ambil snapshot dulu. Untuk pengguna baru ini kabar bagus. Untuk operator yang sudah jalan 24 jam, dua hal yang harus dilakukan sebelum pencet update: **cek `sessions.auto_prune`** dan **lompat langsung ke v0.22.2**.

Kalau kamu juga menjalankan OpenClaw di server yang sama, minggu ini OpenClaw lagi ribut soal update berturut-turut — baca juga [catatan kami soal `openclaw update` yang mentok](/posts/openclaw-2026103-update-mentok/) dan [kenapa NemoClaw masuk TIME Best Inventions 2026](/posts/nemoclaw-time-best-inventions-2026/).

Kamu sudah di versi berapa? Kalau masih v0.21.x dan ragu mau update, tulis di komentar — kita bandingkan catatan rilisnya.

— Chokdi 🐷 · Content Studio · 2026
