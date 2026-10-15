---
title: "Hermes Agent v0.22 \"Threshold\" — Setup Tanpa API Key & 600 Plugin"
date: 2026-10-16T01:20:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "AI Agent"]
---

Nous Research baru saja merilis **Hermes Agent v0.22.0** dengan nama "The Threshold Release" (13 Oktober 2026). Ini bukan update biasa: catatan rilis mereka sendiri menyebutnya sebagai jendela pengembangan **terbesar yang pernah project ini kirim** — sekitar 24.200 commit, 6.080 pull request, dan 7.180 issue yang ditutup sejak v0.21.0. Angkanya kurang lebih 2,5x siklus sebelumnya.

Kalau v0.21.0 membangun "pantheon"-nya, v0.22 ini soal **melewati pintu**. Fokusnya satu: bikin agent AI bisa dipakai tanpa harus jadi sysadmin dulu.

## 🚪 Masalah Sebenarnya: Satu Jam Pertama

Hambatan terbesar agent AI open source bukan kecerdasannya. Kekuatannya sudah ada sejak lama. Yang susah itu **pintunya**: cari API key, edit file config, cari setting yang benar. Orang kehilangan satu jam, merasa bodoh, lalu menyerah sebelum agent-nya melakukan satu hal berguna pun.

v0.22 menyerang titik itu langsung dengan pendekatan tiga langkah: masuk, colok, serahkan.

## 🔑 Langkah 1 — Masuk Tanpa API Key

Install desktop Hermes di komputer yang belum pernah pakai Hermes, dan yang muncul **bukan layar pengaturan, tapi percakapan setup**. Satu kartu per waktu: tanya nama, pilih warna aksen, pilih layout, lalu aplikasi dan plugin apa yang mau dipasang. Ditutup dengan tur singkat plus sampai empat task pertama yang sudah dipilihkan.

Bedanya di mana? Setup-nya jalan di model trial gratis bernama `nous/welcome`, **sekali per user OS** — jadi Anda benar-benar tidak butuh API key untuk mulai. Ada juga tool `set_theme`, jadi cukup ketik "bikin ungu, dark mode" di chat dan tampilannya langsung berubah.

Untuk yang mau jalan sepenuhnya lokal, ada **runtime llama.cpp satu klik**. Hermes memasang dan memelihara engine-nya sendiri, menilai setiap model katalog terhadap VRAM dan RAM Anda, lalu memilih build kualitas tertinggi yang muat. Katalognya termasuk Qwen3.8 27B, Qwen3.8 Flash Next, Qwen3.6 35B-A3B, dan DeepSeek V4 Flash — plus GGUF apa pun dari Hugging Face. Jalan di Windows, macOS, dan Linux. Download bisa pause/resume.

## 🔌 Langkah 2 — Connectors & 600 Plugin

Kalau dulu agent terkurung di terminal, sekarang ia bisa masuk ke aplikasi yang Anda pakai sehari-hari. **Connectors** membuat Hermes bisa bertindak di dalam aplikasi hosted lewat Nous tool gateway — minta app, login sekali di browser, tool-nya langsung aktif di turn yang sama. Satu halaman Connectors menggabungkan aplikasi hosted dan MCP server Anda, dan bisa menampung **beberapa akun bernama** dari satu aplikasi (misalnya akun kerja dan akun pribadi).

Katalog plugin tumbuh jadi **600 entri**, semuanya baru di siklus ini, dan setiap entri dipin ke commit yang sudah direview. Ini bagian yang paling sering dilewatkan orang: angka 600 itu bukan berarti "600 fitur baru", tapi 600 pintu masuk resmi yang kodenya sudah diperiksa — lebih aman dibanding asal clone dari GitHub.

Satu lagi yang praktis: **browser agent** sekarang bisa login ke situs pakai kredensial dari 1Password, Bitwarden, atau vault terenkripsi milik Hermes sendiri — dan modelnya **tidak pernah melihat password-nya**. Kode OTP diisi tanpa masuk ke percakapan, sementara isi kartu dan alamat di checkout wajib dikonfirmasi Anda dulu.

## 🤝 Langkah 3 — Serahkan Kerja Panjang

Ini bagian yang bikin agent akhirnya layak dipercaya untuk kerja nyata:

- **Bot Screen** — bot yang jalan di gateway Linux bisa punya desktop sendiri yang di-stream ke Hermes Desktop. Saat kena login, 2FA, atau CAPTCHA, Anda ambil alih layarnya, selesaikan langkah itu, lalu kembalikan kontrol sambil bot melanjutkan kerja. Default mati, butuh paket host.
- **Reasoning yang bertahan** — penalaran sebelumnya sekarang diputar ulang secara default di setiap provider yang bisa membacanya, termasuk saat resume, branch, dan compaction. Kerja multi-langkah panjang tidak lagi kehilangan arah pikir.
- **Tahan provider lemot** — kalau provider sedang buruk, Hermes menunggu error 503, 529, dan timeout sementara dalam siklus terbatas yang terlihat, bukan langsung mengakhiri turn Anda. `agent.auto_recovery_cycles` default 5, dan watchdog liveness turn default 600 detik.
- **Cron self-heal** — job terjadwal sekarang mengikuti model utama Anda dan **jalan ulang otomatis** setelah 5, 15, dan 30 menit kalau fire-nya tidak sampai ke model.

## 📦 Update Channel: Stable, Bukan Bleeding Edge

Perubahan yang paling berdampak jangka panjang buat yang nge-host: install source sekarang mengikuti **tag rilis SemVer resmi**, bukan tiap commit di `main`. Install yang lebih baru dari rilis terakhir tidak akan "diturunkan" — ia menunggu rilis berikutnya. Mau tetap ikut `main`? Jalankan `hermes update --set-channel main`. Rollback tidak pernah terjadi tanpa bertanya.

Package desktop sekarang paket bertanda tangan yang membawa Python dan Node sendiri, jadi peluncuran pertama tidak build apa-apa. Windows dapat MSIX bertanda tangan (butuh Windows 11 22H2+), macOS dapat build notarized untuk Apple Silicon. Python 3.14 jadi runtime untuk install terkelola.

## ⚠️ Catatan Upgrade yang Wajib Dibaca

Empat hal ini yang paling sering bikin kaget:

1. **Windows desktop sekarang MSIX-only**; app macOS default-nya Apple Silicon saja.
2. **Chat tidak lagi reset otomatis** pada timer idle atau harian. Pakai `/new` atau `/reset` kalau mau mulai segar.
3. **Sesi lama dipangkas otomatis** — sesi yang sudah berakhir dan tidak aktif 90 hari dihapus saat startup. Sesi yang di-pin atau masih terbuka aman, dan `sessions.auto_prune: false` mematikan perilaku ini.
4. **Memory provider pindah jadi plugin katalog** (Honcho, Supermemory, Hindsight, Mem0, OpenViking, Holographic). User lama dimigrasi dengan data utuh.

Poin nomor 4 itu yang paling penting untuk tim yang sudah jalan di produksi: memory bukan lagi bagian core, tapi plugin. Artinya jalur upgrade harus dites dulu di staging sebelum menyentuh instance yang dipakai kerja sehari-hari.

## 🎯 Kesimpulan

v0.22 "Threshold" menandai pergeseran pola pikir Nous Research: dari "lihat seberapa kuat agent ini" jadi "lihat seberapa mudah orang mulai memakainya". Yang teknis tetap teknis — tapi pintunya sekarang jauh lebih lebar.

Saran praktis: kalau Anda masih di v0.21.x, jangan langsung upgrade produksi. Nyalakan di mesin kedua dulu, jalankan setup chat-nya, tes Connectors dan plugin, baru pindahkan. Dan baca bagian Upgrade notes-nya sampai habis — terutama soal auto-prune sesi 90 hari dan migrasi memory provider.

Kalau Anda sudah mencoba v0.22, mana yang paling kepakai: local models, Connectors, atau Bot Screen? Ceritakan di kolom komentar.

— Chokdi 🐷 · Content Studio · 2026
