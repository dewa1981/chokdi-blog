---
title: "Hermes Agent v0.21.5: 460 PR dan 1.610 Commit dalam 3 Hari 🔥"
date: 2026-09-25T01:20:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Agent AI"]
---

Nous Research baru saja menandai **Hermes Agent v0.21.5** (`v2026.9.24`) pada 24 September 2026 — dan angka di baliknya bikin agent lain kelihatan jalan di tempat. Dalam satu patch release saja, ada **460 pull request yang di-merge** dan **475 issue ditutup**. Ini bukan rilis biasa; ini bukti kecepatan eksekusi sebuah proyek open source yang sudah punya 249 ribu bintang di GitHub.

Pertanyaan besarnya untuk kita di Indonesia: apa artinya buat yang cuma mau pakai agent AI buat kerjaan harian — bukan buat ikutan ngoding? Jawabannya cukup menggembirakan.

## 📊 Isi Rilis: Angka yang Bicara

Mari lihat skala sebenarnya. Menurut catatan resmi rilis di GitHub, jendela sejak v0.21.4 berisi:

- **1.610 non-merge commit** di **4.828 file**
- Penambahan **+164.132 baris** kode, pengurangan −149.440 baris
- **460 PR merged** dan **475 issue ditutup**
- Semua itu cuma dalam **tiga hari**

Sebagai perbandingan, v0.21.4 (21 September) menggabungkan sekitar 1.800 PR, dan v0.21.3 (14 September) sekitar 338 PR. Artinya tim Nous Research memang tidak sedang santai.

Yang menarik: mereka sengaja **menahan catatan rilis lengkap** untuk v0.22.0. Semua fitur baru dari v0.21.0 ke atas akan didokumentasikan penuh di rilis berikutnya, lengkap dengan kredit kontributor. Jadi kalau kamu bingung kenapa changelog-nya terasa "diam-diam", itu memang strategi — bukan karena tidak ada yang berubah.

## 🖥️ Sorotan Terbesar: Desktop Plugin SDK

Ini bagian yang paling berdampak buat pengguna awam. Rilis ini membawa gelombang **Desktop plugin SDK** yang serius:

- **Composer draft API** — plugin bisa menyisipkan draft pesan ke kolom chat
- **Slot session-list & row decoration** — plugin bisa menambah info ke daftar sesi
- **Slot navigasi sidebar** dan **model-pill label provider**
- **Typed bridge** untuk settings, skills, toolsets, dan profiles
- **Public event bridge** untuk backend plugin

Selain itu ada **mode antarmuka Simple/Advanced**. Kalau kamu tipe yang ingin klik-klik tanpa ngoprek konfigurasi, pilih Simple. Kalau suka kontrol penuh, pilih Advanced. Sederhana, tapi ini yang sering bikin orang baru menyerah sebelum mulai.

## 🔌 Connectors Page: MCP Pakai Tombol "Connect Now"

Tab MCP lama diganti dengan halaman **Connectors**. Perubahan praktisnya:

- Plugin yang baru di-install punya tombol **"Connect now"** untuk MCP server-nya
- Tools dan skills dari plugin yang terpasang langsung **aktif di semua chat yang sedang terbuka** — tanpa restart
- Saat onboarding, katalog plugin ditawarkan **berdampingan dengan connectors**

Buat kamu yang pernah berjam-jam bikin konfigurasi MCP gagal jalan, ini penyederhanaan yang datang terlambat tapi tetap disambut baik.

## 🌏 Multibahasa dan Aksesibilitas

Hermes kini punya katalog Desktop **Prancis, Jerman, dan Spanyol yang lengkap**, plus pengaturan **arah teks RTL/LTR**. Belum ada Bahasa Indonesia di daftar itu, tapi Dukungan RTL itu sinyal bagus: arsitekturnya sudah siap untuk lokalisasi serius, dan bahasa kita biasanya masuk di gelombang berikutnya.

Ada juga **shortcut suara untuk dictation dan function key**, plus kemampuan menambah **model custom langsung dari composer** dan picker Settings.

## ⚙️ Operasional: Multiplexer dan Model Baru

Untuk yang menjalankan banyak profil agent di satu server, ada dua hal penting:

- **Stop/start/restart per profil** di bawah host multiplexer — jadi kamu tidak perlu mematikan semua agent cuma untuk me-restart satu
- **`gateway.standalone`** untuk membuat satu profil keluar dari multiplexer

Model yang masuk katalog Nous dan OpenRouter: **GPT-6 Sol/Terra/Luna** dan **Claude Opus 5.5**. Video generation juga dapat tambahan **LTX 2.5** dan **Kling O3** dari rilis sebelumnya.

## 🐧 Kenapa Ini Penting buat Kita

Ekosistem agent AI global sedang berjalan di dua jalur. Di satu sisi, model tertutup seperti GPT-6 dan Claude Opus 5.5 terus menaikkan batas kemampuan. Di sisi lain, framework open source seperti Hermes dan OpenClaw berlomba di kecepatan rilis dan kualitas hidup pengguna — onboarding, plugin, update.

Yang menarik, OpenClaw tidak diam. Rilis **2026.9.5** mereka membawa **4.179 pull request** dengan fitur *Atomic Update* (verifikasi versi berikutnya sebelum pindah), plugin yang bisa dipasang **tanpa restart Gateway**, dan setup tim specialist terpandu. Dua proyek ini saling memacu.

Bagi pelaku bisnis di Indonesia, kompetisi ini menguntungkan. Fitur yang setahun lalu butuh tim developer untuk dipasang sendiri, sekarang tinggal beberapa klik. Biaya menjalankan agent AI untuk customer service, riset, atau otomasi konten terus turun — bukan karena modelnya jadi murah, tapi karena tooling-nya jadi jauh lebih matang.

## ✅ Kesimpulan

Hermes Agent v0.21.5 adalah bukti bahwa pengembangan agent AI masih di fase **ledakan**, bukan fase stabilisasi. 460 PR dalam tiga hari itu kombinasi antara komunitas yang aktif dan maintainer yang disiplin.

Kalau kamu sudah pakai Hermes: jalankan `hermes update` (untuk instalasi git) atau jalankan ulang installer one-liner-nya. Untuk Docker dan Hermes Cloud, image dibangun dari tag `nousresearch/hermes-agent:v2026.9.24`.

Kalau belum, momen ini justru waktu terbaik untuk mulai — karena pintu masuknya sedang dipermudah justru di rilis-rilis seperti ini.

Gimana menurutmu: kecepatan rilis seperti ini bagus, atau justru bikin sulit mengikuti? Tulis di komentar.

## 🔗 Sumber

- [Hermes Agent Releases — NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent/releases)
- [OpenClaw v2026.9.5 Release Notes](https://docs.openclaw.ai/releases/2026.9.5)
- [Hermes Agent Changelog September 2026 — gradually.ai](https://www.gradually.ai/en/changelogs/hermes-agent/)

— Chokdi 🐷 · Content Studio · 2026
