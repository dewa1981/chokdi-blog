---
title: "Hermes Agent v0.23.5: 338 PR dalam 91 Jam, Rasio Hapus Kodenya Anjlok dari 43% ke 9%"
date: 2026-11-28T17:15:00+07:00
draft: false
tags: ["Hermes Agent", "Nous Research", "Rilis", "AI Agent", "November 2026"]
---

Tag **Hermes Agent v0.23.5** muncul Sabtu pagi ini, 28 November 2026 pukul 03.20 UTC — 10.20 WIB. Jaraknya hanya **91 jam** dari v0.23.4. Release note-nya masih menyebut diri "patch release", tapi angkanya lagi-lagi bukan angka patch: **338 PR** dan **1.262 commit** digulung jadi satu tag.

Yang membuat rilis ini beda dari tiga pendahulunya bukan besarannya, melainkan **komposisi** perubahannya. Dua rasio bergeser tajam — dan itu yang saya bedah di bawah.

## 📦 Tiga rilis, tiga profil angka

Semua angka di bawah diambil dari halaman release resmi di GitHub (diukur di commit tag masing-masing), bukan dari changelog agregator yang sering tertinggal satu versi:

- **v0.23.3** (tag 20 Nov): 370 PR, 1.657 commit, 3.948 file, **+222.379 / −96.154** baris
- **v0.23.4** (tag 24 Nov): 229 PR, 1.122 commit, 1.316 file, **+96.873 / −6.703** baris
- **v0.23.5** (tag 28 Nov): 338 PR, 1.262 commit, 1.146 file, **+57.989 / −5.346** baris

Dari tag v0.23.3 sampai v0.23.5 hanya delapan hari, tapi dua jendela rilis terakhir saja sudah berisi **567 PR** — sekitar **70 PR per hari**. Itu tempo repo dengan puluhan reviewer aktif.

## 🔬 Dua rasio yang bergeser

**1. Rasio hapus kode: 43,2% jadi 9,2%.** Di jendela v0.23.3, setiap 100 baris tambahan diikuti 43 baris yang dihapus; di v0.23.5 tinggal 9. Jendela v0.23.3 mengandung pembongkaran besar, sedangkan v0.23.5 hampir seluruhnya tambahan — "patch" ini gemuk karena isi baru, bukan bersih-bersih kode lama.

**2. Rasio issue ditutup per PR: 1,23 jadi 0,27.** v0.23.4 menutup 281 issue dengan 229 PR. v0.23.5 cuma menutup 92 issue, padahal PR-nya 338. Ada dua cara membacanya: pekerjaan baru lebih banyak daripada utang lama yang dibereskan, atau tumpukan bug besar sudah habis di siklus sebelumnya. Yang pasti, permukaan aplikasinya bertambah — dan itu relevan buat yang self-host.

## 🛠️ Yang masuk tanpa diceritakan di release note

Nous menulis satu paragraf yang mereka sebut "undocumented here on purpose" — sengaja tidak dijelaskan, tapi tetap dikirim. Ini yang paling terasa di pemakaian harian:

- **Chat gateway yang idle dikompres di latar belakang di semua jalur.** Untuk bot yang nyala berhari-hari (Telegram, Discord), konteks tidak lagi menumpuk sampai balasan melambat.
- **`read_file` bisa membaca dari offset negatif dan mendaftar isi folder.** Agent bisa lihat 20 baris terakhir log tanpa tahu jumlah barisnya dulu — kerja debugging jadi lebih pendek.
- **`search_files` berhenti kalau hasil content search sudah menjawab semuanya.** Mengurangi loop pencarian yang tidak perlu.
- **Preflight plugin bawaan sebelum gateway lokal start** (Desktop, Docker, CLI). Plugin rusak ketahuan sebelum gateway boot, bukan setelah crash-loop.
- **Entri plugin OAuth bisa mengunci redirect URI**, dan pengikatan kerja plugin ke profil diperbaiki untuk kasus profil di-rename, dipindah, atau dihapus.
- **Solstice provider pindah ke stateless Interactions API**; dashboard mulai menampilkan notis "dashboard kamu akan pindah"; tombol panah mentah jalan di picker sessions dan plugins.
- **CLI dan TUI mendukung protokol resume program OSC 7577** — program di terminal bisa lanjut setelah sesi di-reattach.

## ⏱️ Ritme merge tidak rata

Via GitHub Search API, PR yang merge per hari di jendela ini: **148 (24 Nov), 34 (25 Nov), 130 (26 Nov), 31 (27 Nov)**. Totalnya 343, sedikit di atas 338 karena hitungan harian masih memuat PR sebelum tag v0.23.4 dipotong.

Polanya bergelombang: dua hari besar, dua hari sepi — kerja dikumpulkan lalu di-merge berkelompok, bukan mengalir per jam.

## ⚠️ Sebelum `hermes update`

- **Desktop dari installer belum dapat versi ini** — release note menyebut Desktop ikut bundel berikutnya. Microsoft Store update lewat Store, Docker/Hermes Cloud pakai `nousresearch/hermes-agent:stable`, CLI pakai `hermes update`.
- **Catatan kurasi ditahan sampai v0.24.0.** 338 PR masuk tanpa ringkasan; kalau butuh detail, baca halaman compare `v0.23.4...v0.23.5` atau daftar commit.
- **Backup dulu**: salin config dan `state.db` (copy file, jangan buka database hidup dengan sqlite3).
- **Uji di staging**, lalu cek empat hal: gateway hidup, satu cron jalan, satu plugin favorit ter-load, dan sesi chat lama masih bisa dibuka.

## 🎥 YouTube masih satu versi di belakang

Saya periksa transkrip dua video terbaru. Short berbahasa Spanyol soal v0.23.4 menyebut "229 cambios y cierra 281 problemas" — persis angka release note resmi. Video berbahasa Inggris "776 NEW Hermes Agent Updates Are INSANE!" masih mengemas rilis v0.23 sebagai "776 update". Untuk v0.23.5, belum ada video yang membahasnya.

## Kesimpulan

v0.23.5 tidak akan dikenang dari judulnya. Yang layak dicatat: **338 PR dalam 91 jam, dengan komposisi yang bergeser dari pembongkaran ke penambahan** — lebih dari 9 dari 10 baris yang berubah adalah tambahan. Buat yang self-host, nilai rilis ini justru ada di tiga hal kecil: kompresi chat idle, `read_file` yang bisa baca ekor file, dan preflight plugin sebelum gateway start.

Update kalau kamu punya jendela uji. Kalau tidak, tunggu v0.24.0 — di situ baru ada catatan lengkapnya.

Kamu tim yang update tiap patch, atau tunggu rilis besar? Tulis di komentar.

**Baca juga:** [Hermes Agent v0.23.4: 229 PR dalam 4 Hari, 7 Perubahan yang Tidak Masuk Release Note](https://chokdi.ano99.com/posts/hermes-agent-v0234-229-pr-4-hari/) · [Hermes Agent v0.23.2 Rilis: 1.989 PR Ditumpuk Jadi Satu Patch, 6 Fitur yang Tidak Ada di Judul](https://chokdi.ano99.com/posts/hermes-agent-v0232-1989-pr-durable-subagent/) · [Hermes Agent Masuk Microsoft Teams & Azure: v0.23.3 Bawa 370 PR, Harga Masih Gelap](https://chokdi.ano99.com/posts/hermes-agent-teams-azure-v0233-november-2026/)

— Chokdi 🐷 · Content Studio · 2026