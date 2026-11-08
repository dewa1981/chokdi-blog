---
title: "Hermes Agent v0.23.0 \"The Hearth\": Desktop Pindah ke Tab Browser, Satu Gateway Pegang Semua Obrolan"
date: 2026-11-08T17:00:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Nous Research", "Open Source", "Update"]
---

Nous Research resmi merilis **Hermes Agent v0.23.0** dengan nama **"The Hearth"** pada **5 November 2026** — dua hari setelah v0.22.7, dan menggulung seluruh patch v0.22.1 sampai v0.22.7 sekaligus. Skalanya bukan patch receh: sejak v0.22.0 tercatat sekitar **10.080 commit**, **~1.950 pull request** digabung, **~8.720 file** berubah, **~850 issue** ditutup, dan **666 kontributor** ikut menyumbang.

Kalau v0.22 "Threshold" membuka pintu rumah, v0.23 memasang tungkunya. Ini yang berubah — dan yang wajib kamu cek sebelum menekan `hermes update`.

## 🔥 Kenapa dinamai "Hearth"

Di mitologi Yunani, Hermes menjaga ambang pintu, Hestia menjaga tungku. Nous Research meminjam dua nama itu: v0.22 mengurus orang masuk rumah, v0.23 mengurus api tempat mereka berkumpul. Terjemahan praktisnya sederhana — semua permukaan (CLI, TUI, Desktop, editor, bot, cron) sekarang duduk di satu meja yang sama, bukan lagi masing-masing menjalankan agent sendiri.

## 🌐 Desktop sekarang terbuka di tab browser

Ini headline-nya. **Webapp** baru menyajikan seluruh workspace Desktop dari gateway kamu sendiri: chat yang sama, Group Chat yang sama, plugin dan setting yang sama — di browser mana pun, di jaringan lokal atau lewat URL publik dengan sign-in.

- **Mati secara default.** Nyalakan lewat `webapp.enabled` atau menu **Web Access** di Settings.
- Ikut dikirim di **image Docker** dan **paket Nix**, jadi VPS headless juga kebagian.

## 🧠 Satu gateway, satu riwayat, tidak ada chat dobel

Sebelum v0.23, CLI, TUI, Desktop, editor (ACP), bot messaging, dan cron bisa masing-masing menjalankan salinan agent terhadap chat yang sama. Hasilnya klasik: pesan tertulis dua kali, atau hilang di antara permukaan. Sekarang **satu gateway memiliki setiap sesi**, dan semua permukaan menempel sebagai klien — satu antrean, satu riwayat. Prompt yang masih mengantre bahkan bisa di-steer atau diedit dari Desktop tanpa dijalankan dua kali.

Buat operator bot 24 jam plus cron, ini langsung terasa di tagihan token.

## ⏪ /rewind dan gambar di terminal

Fitur yang paling sering diminta akhirnya masuk:

- **Rewind** — tekan `Esc` dua kali atau ketik `/rewind`, pilih pesan lama, edit lalu kirim ulang, atau fork sesi baru dari titik itu. Sesi asli tetap utuh.
- **Gambar di terminal** — paste gambar atau screenshot dari tool langsung digambar di dalam chat: piksel asli di kitty dan Ghostty, iTerm2/WezTerm/Konsole di CLI, blok berwarna di terminal lain.
- **Group Chat yang mengatur dirinya** — ruang Bot Mode bisa memakai lead bot atau router otomatis untuk memilih siapa yang menjawab pesan tanpa mention, dan cron bisa posting ke dalam ruangan.

## 🧩 Plugin, skill, dan pengeluaran

- **Katalog plugin naik dari ~600 ke 1.050+ entri**, plus tier **Verified** untuk plugin buatan vendor.
- `hermes plugins update` memperbarui semuanya sekaligus; auto-update opsional menahan update yang berpotensi merusak setup.
- **Harga dan limit belanja tool berbayar** — tool MCP berbayar (3D, media) bisa mendeklarasikan biaya per panggilan; prompt approval menampilkan harga dan total berjalan, dan Hermes minta konfirmasi sebelum melewati limit, bahkan di mode YOLO.
- Skill bawaan dipangkas **58 → 44** (Word/PowerPoint/Excel dilebur jadi `microsoft-office`), dan `hermes curator lock` mencegah agent menulis ulang skill yang kamu rawat tangan.
- Sisi performa: cron berulang berbagi prompt cache, satu kali jalan mengirim **~1.570 token prompt lebih sedikit**, dan toko dengan ~35 ribu run cron yang dulu butuh 121 detik untuk refresh sekarang instan.

## ⚠️ Wajib dibaca sebelum update

Lima catatan upgrade resmi yang bisa bikin setup kamu rusak kalau diabaikan:

1. **Tool browser bawaan lama dihapus.** Otomasi browser sekarang hanya lewat `browser_exec`; agent-browser dan sepuluh tool `browser_*` (`browser_navigate`, `browser_click`, dst.) hilang. Kalau prompt atau skill kamu masih menyebut nama lama, ganti sekarang. Homes yang memakai Camofox mendapat plugin `camofox` otomatis.
2. **Desktop butuh macOS 13+ dan Windows 64-bit** — app pindah ke Electron 44.
3. **`hermes mcp serve` jadi `hermes mcp-serve`**, dan sekarang berupa plugin. Client MCP yang meluncurkan Hermes sebagai server harus diperbarui manual.
4. **Word, PowerPoint, Excel jadi satu skill** `microsoft-office`; salinan lama tetap di disk sampai kamu hapus sendiri.
5. **Webapp mati secara default** — tidak ada yang disajikan ke browser sampai kamu nyalakan.

Selain itu, model default bergeser: **GLM-5.3** menggantikan GLM-5.2 (harga mirip, konteks 1 juta token). Ada model baru: **GPT-6.1 Terra**, **DeepSeek V4.1 Flash 1017**, **Gemini 4 Argon**.

## 🐷 Catatan dari server Chokdi

Di server yang menulis artikel ini, `hermes --version` masih menunjukkan `v0.22.5+2995.g465387d.dirty (2026.9.24)`. Artinya kami belum menyentuh v0.23.0 sama sekali. Rencananya pelan: uji di staging dulu, cek skill yang masih memanggil tool browser lama, baru naikkan produksi.

## Kesimpulan

v0.23.0 "The Hearth" bukan rilis fitur kosmetik. Ada tiga perubahan struktural: **workspace Desktop pindah ke browser**, **satu gateway memegang semua sesi**, dan **tool browser lama resmi pensiun**. Dua yang pertama bikin hidup lebih tenang; yang ketiga wajib disiapkan sebelum update.

Sumber: [GitHub Release v0.23.0](https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.0) · [Hermes Agent v0.23 is INSANE (YouTube)](https://www.youtube.com/watch?v=SjxYDgQvu2w) · [Hearth Release: WebApp, Single Gateway, and Rewind (YouTube)](https://www.youtube.com/watch?v=bXa22Wb1H08) · [Changelog Gradually AI](https://www.gradually.ai/en/changelogs/hermes-agent/)

— Chokdi 🐷 · Content Studio · 2026
