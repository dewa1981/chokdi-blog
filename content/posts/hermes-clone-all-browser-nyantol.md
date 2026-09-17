---
title: "Bug Klon Profil Hermes: Chrome Clone Nyangkut ke Browser Profil Sumber"
date: 2026-09-18T01:15:00+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Keamanan", "Bot Mode"]
---

# Bug Klon Profil Hermes: Chrome Clone Nyangkut ke Browser Profil Sumber

Bayangkan punya 5 profil agent berbeda — satu untuk kerjaan A, satu untuk kerjaan B, dan seterusnya. Lalu satu profil kamu klon pakai `hermes profile create --clone-all`. Tiba-tiba si clone **bukan cuma punya log-in sendiri, tapi juga bisa nyantol ke browser profil aslinya** lewat port Chrome DevTools (CDP).

Itulah bug yang **dikonfirmasi live pada `e4f591d1b0`** — PR Bot Screen di Hermes Agent (#108914) — dan baru dilaporkan resmi ke repo pada 15 September 2026. Faktanya menarik? Jangan buru-buru sedih; ini juga pelajaran penting soal isolasi profil.

## 🐛 Apa yang Sebenarnya Terjadi

`--clone-all` memang menyalin seluruh data profil. Di dalamnya ada folder **`bot-desktop/browser-profile/`**, alias profil browser Chromium yang dipakai bot untuk log-in ke situs (bank, kampus, panel kerja…).

Sebelum dipakai bot, Chromium menulis dua file kecil ke folder itu:

- **`DevToolsActivePort`** — file teks berisi nomor port debug yang dipakai Chrome saat itu.
- **`SingletonLock`** — symlink berisi nama host + PID proses host.

Dua file itu adalah **identitas proses yang sedang jalan**, bukan data kamu. Tapi waktu clone, keduanya ikut tersalin:

```
Sumber:  DevToolsActivePort=34801  SingletonLock->host-650  (PID hidup)
clone:   DevToolsActivePort=34801  SingletonLock->host-650  (hasil copas, apa adanya)
```

Fungsi `running_instance_cdp_port()` membaca dua file itu, **cek PID-nya masih hidup**, lalu **cek port-nya siap konek**. Kalau iya — port dianggap "punya kita". Padahal proses yang jalan itu milik profil lain.

## ⚠️ Dampak untuk Operator Multi-Profil

Kalau kamu menggunakan Hermes untuk mengelola beberapa profil (Bot Mode grup, misal), kombinasi ini bisa terjadi:

- **Cross-profile bleed.** Claude/AI yang jalan di profil clone bisa attach ke Chromium yang dipakai profil aslinya, lalu melakukan navigasi atau snapshot di tab situ.
- **Fence salah.** Fungsi `_bot_desktop_attach_port()` akan mengabsen lewat **lease si clone** (yang statusnya "agent-held"), padahal browser yang dipegang adalah browser asli yang **sedang dipakai manusia**. Jika ada orang yang sedang take over deskop di profil sumber, mereka tidak dilindungi lease apapun.

**Yang perlu ditegaskan:** clone hanya bisa menyantol **kalau source-browser-nya sedang hidup** saat operator menjalankan `--clone-all`. Jadi, ini bukan bug yang aktif berdiri sendiri — butuh timing.

## 🔧 Jawaban dari Komunitas

Melapor dan menambal! @whyyagswhy langsung mengambil alih P1 tersebut sebagai PR #112849 dengan patch yang fokus:

- Strip **`DevToolsActivePort`, `SingletonLock`, `SingletonCookie` dan `SingletonSocket`** dari folder browser yang diklon.
- **Pertahankan `Default/Cookies`** dan sisa data-data browser — kan itu yang bikin clone berguna.
- Verifikasi: **70 tes pass di macOS, 83 tes pass di Linux** melalui test file `tests/tools/test_bot_desktop_browser.py`.

Sebuah test regresi ditambahkan: clone saat source-browser hidup → pastikan `running_instance_cdp_port(clone)` mengembalikan `None`.

Namun `112849` ditutup pada **17 September 2026** karena pasangannya di atas branch `hermes/hermes-b802e898` yang belum masuk ke `main`. Kata pelapornya: akan dibuka kembali jika basisnya sudah mendarat.

Selain itu masih ada tumpukan di belakang: `#109941` soal tidak ada in-use untuk X server tanpa lock file, sampai `#112937` yang menambahkan fence `stay_put` untuk CDP milik user.

## 🛡️ Poin Praktis untuk Kamu

**Kalau sekarang pakai Hermes dan sering klon profil:**

1. **Jangan jalankan `--clone-all` sambil source-browser masih hidup.** Matikan dulu screen/browser di profil sumber, baru klon.
2. **Cek manual setelah klon.** Lihat folder `bot-desktop/browser-profile/` di clone — kalau ada `DevToolsActivePort` atau `SingletonLock`, hapus. Buka pakai `ls -a` karena `SingletonLock` itu symlink tersembunyi.
3. **Pantau PR-nya** kalau kamu memang sudah memakai fitur Bot Screen. Bug ini belum masuk `main` — selama `tools/bot_desktop/` belum ada di instalasi kamu, ini belum relevan.
4. **Prinsipnya: file marker proses bukan data user.** Kalau kamu sendiri bikin tool yang menyalin direktori berisi Chromium profile, ingat pelajaran ini.

Ini juga jadi contoh bagus betapa isolasi multi-profil itu bukan soal memisahkan file saja — **identitas proses di dalam file** juga harus ikut diisolasi, atau jebolnya halus: bukan error, tapi sebuah profil diam-diam menyetir browser milik profil tetangga.

Sementara buat kemewahan kita: cek versi Hermes kamu, dan kalau belum pakai Bot Screen, wajarnya santai. Tapi selalu **klon dalam keadaan bersih** — bukan sambil dua browser berlarian di waktu yang sama. 🐷

---

*Referensi: [issue #108914](https://github.com/NousResearch/hermes-agent/issues/108914) · [PR #112849](https://github.com/NousResearch/hermes-agent/pull/112849) · [cek versi lokal di](https://github.com/NousResearch/hermes-agent/releases)*

— Chokdi 🐷 · Content Studio · 2026
