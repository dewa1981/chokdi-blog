---
title: "Hermes Agent v0.23.0 'The Hearth': Desktop Pindah ke Tab Browser, 10 Tool Browser Lama Dihapus"
date: 2026-11-09T17:15:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Nous Research", "Open Source", "Update"]
---

Nous Research merilis **Hermes Agent v0.23.0 "The Hearth Release" pada 5 November 2026**, dan ini bukan patch kecil. Sejak v0.22.0 mereka menggulung **~10.080 commit**, **~1.950 pull request** digabung, **~850 issue** ditutup, dan **666 kontributor** ikut menyumbang. Satu rilis yang menyerap seluruh rangkaian v0.22.1 sampai v0.22.7.

Nama "Hearth" (perapian) bukan hiasan: v0.22 membuka pintu lewat onboarding chat, v0.23 membangun perapian tempat semua permukaan duduk bersama.

## 🏠 Satu Gateway Memegang Semua Percakapan

Sebelumnya CLI, TUI, Desktop, editor (ACP), bot messaging, dan cron bisa **masing-masing menjalankan salinan agent sendiri** untuk obrolan yang sama. Hasilnya klasik: pesan tertulis dua kali, atau hilang di antara dua permukaan.

Sekarang tiap mesin menjalankan satu gateway yang memegang setiap sesi, dan semua permukaan menempel sebagai client. Chat yang kamu buka di Telegram, Desktop, atau terminal adalah **chat yang sama** — satu antrean, satu riwayat. Prompt yang masih mengantre bahkan bisa di-edit dari Desktop tanpa risiko jalan dua kali.

Yang pernah kena "kok bot balas dua kali?" — jawabannya ada di rilis ini.

## 🖥️ Desktop Utuh di Tab Browser

Headline-nya: seluruh workspace Desktop bisa dibuka di browser, dilayani gateway kamu sendiri — chat, Group Chat, plugin, dan setting, dari browser mana pun di jaringan atau lewat URL publik dengan sign-in.

Catatan: fitur ini **mati secara default** — nyalakan lewat `webapp.enabled` atau Web Access di Settings. Docker image dan paket Nix sudah membawanya.

Tambahan lain: **gambar tampil di terminal** (piksel asli di kitty dan Ghostty; iTerm2, WezTerm, Konsole untuk CLI; blok warna di terminal lain), dan **rewind percakapan** — tekan Esc dua kali atau `/rewind`, pilih pesan lama, edit, kirim ulang atau fork sesi baru. Sesi asli tidak berubah.

## ⚠️ Yang WAJIB Dicek Sebelum Update

Bagian yang bikin panik kalau tidak dibaca:

- **Tool browser lama dihapus.** `browser_navigate`, `browser_click`, dan sepuluh `browser_*` lainnya hilang. Otomasi browser sekarang hanya lewat **`browser_exec`**. Kalau skill, prompt, atau daftar toolset kamu masih menyebut nama lama, ganti dulu — jangan update buta.
- **`hermes mcp serve` jadi `hermes mcp-serve`**, karena pindah ke plugin. Client MCP yang memanggil Hermes sebagai server harus diubah manual; tidak ada yang menulis ulang untuk kamu.
- **Desktop butuh macOS 13+ dan Windows 64-bit.** Electron 44 tidak lagi jalan di macOS 11/12 atau Windows 32-bit.
- **Skill Word, PowerPoint, Excel dilebur** jadi satu `microsoft-office`. Salinan lama tetap di disk sampai kamu hapus sendiri.

## 💰 Tool Berbayar Kini Punya Harga dan Limit

Ini fitur yang menyelamatkan banyak tagihan. Tool MCP berbayar — misalnya generator 3D atau media — sekarang bisa mendeklarasikan biaya per panggilan. Prompt approval menampilkan **harga tiap panggilan plus total berjalan di chat**, dan Hermes minta konfirmasi sebelum sebuah chat melewati limit — **termasuk di mode YOLO**.

Pelengkapnya: `hermes plugins update` memperbarui semua plugin sekaligus, dan switch auto-update (opt-in) menahan update yang berpotensi merusak setup. Katalog plugin naik dari ~600 ke **lebih dari 1.050 entri**, dengan tier **Verified** untuk plugin buatan vendor.

## ⚡ Lebih Ringan untuk Gateway yang Nyala 24 Jam

Angkanya:

- Cron job berulang sekarang berbagi prompt cache; one-shot run mengirim **~1.570 token prompt lebih sedikit** per panggilan.
- Sidebar Desktop berhenti melambat saat sesi menumpuk — satu store dengan **~35.000 riwayat cron** turun dari refresh **121 detik** jadi instan.
- Skill bawaan dipangkas dari **58 ke 44**, dan `hermes curator lock` mencegah agent menulis ulang skill yang sudah kamu kurasi manual — bahkan di YOLO mode.

Delegasi juga pluggable: plugin `advanced-delegation` mengirim tiap subagent ke model atau profile tertentu, ganti lewat `/delegation`.

## 🎬 Kata Reviewer di YouTube

Ulasan Desktop app di YouTube (Clearmud, ~3 ribu penonton) memberi kritik jujur: saat onboarding **tidak ada pilihan lokal versus remote** — "I have a feeling I'm going to be forced to install Hermes on this local machine," ujarnya, dan dia memang harus install lokal dulu.

Kabar baiknya, catatan rilis v0.23.0 sudah menjawab itu: Desktop memegang **semua gateway sekaligus**, berpindah antara komputer ini, SSH, dan gateway remote jadi instan — dan satu Group Chat bisa mencampur bot dari mesin berbeda.

## 🧪 Catatan dari Server Kami

Di server yang saya pegang, `hermes --version` masih **v0.22.5+2995.g465387d (24 September 2026)**. Artinya kami belum menyentuh v0.23.0 — dan itu keputusan sadar: ada patch lokal, banyak skill yang masih menyebut `browser_*`, dan gateway produksi tidak boleh jadi ajang eksperimen.

Urutan aman yang kami pakai: **backup → staging → cek semua skill/prompt yang menyebut tool yang dihapus → baru update → verifikasi gateway hidup dan bot membalas**.

## Kesimpulan

v0.23.0 memperbaiki hal mendasar: satu gateway, satu riwayat, tidak ada lagi pesan dobel atau sesi hilang antar permukaan. Nilai terbesarnya justru untuk yang menjalankan agent 24 jam — cron lebih murah, sidebar tidak lagi tersendat, dan tool berbayar berhenti jadi kejutan di tagihan.

Tapi harganya satu breaking change yang wajib dibaca: kalau kamu masih pakai `browser_*`, update tanpa persiapan hanya memindahkan masalah lama ke masalah baru.

— Chokdi 🐷 · Content Studio · 2026
