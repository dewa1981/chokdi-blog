---
title: "Hermes Agent v0.23 'The Hearth' Rilis 6 November: Desktop Pindah ke Tab Browser, Satu Gateway untuk Semua Sesi"
date: 2026-11-06T17:30:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Nous Research", "Open Source", "Self-Hosted"]
---

Nous Research menutup siklus v0.22 dengan cara yang tidak main-main. **Hermes Agent v0.23.0 "The Hearth Release"** terbit 5 November 2026 pukul 21:32 UTC — **6 November dini hari, 04:32 WIB**. Angka resminya sejak v0.22.0: **~10.080 commit**, **~1.950 pull request** digabung, **~8.720 file** berubah, **+725.200/−201.400 baris**, **~850 issue** ditutup, dan **666 kontributor**. Rilis ini menggulung seluruh patch v0.22.1–v0.22.7.

Kalau v0.22 "Threshold" membukakan pintu, v0.23 membangun perapiannya. Buat operator yang menjalankan agent 24 jam, itu terasa di dua hal: **satu gateway** dan **Desktop di browser**.

## 🖥️ Desktop Utuh di Dalam Tab Browser

Ini headline-nya. Gateway kamu sendiri kini menyajikan **seluruh workspace Desktop** — chat, Group Chat, plugin, setting — lewat browser, di jaringan lokal maupun URL publik dengan sign-in. Nyalakan `webapp.enabled: true` atau Settings → Web Access, lalu `hermes webapp`.

Fitur ini **mati secara default** dan bersifat **single-user**: tab yang login bertindak sebagai kamu, dengan sesi dan Group Chat yang sama seperti Desktop native. Plugin Desktop ikut jalan di browser, dan ada polesan ponsel — judul tab berkedip saat ada chat yang butuh perhatian, notifikasi browser, dan satu tap ke kolom ketik di iPhone.

## 🧠 Satu Gateway Punya Semua Percakapan

Dulu CLI, TUI, Desktop, editor (ACP), bot messaging, dan cron bisa masing-masing menjalankan **salinan agent sendiri** terhadap chat yang sama — sumber klasik pesan tertulis dua kali atau hilang di antara surface.

Sekarang tiap mesin punya **satu gateway yang memiliki semua sesi**, dan semua surface menempel sebagai klien: satu antrean, satu histori. Prompt yang mengantre bisa diedit dari Desktop tanpa jalan dua kali, dan Desktop memegang **semua gateway sekaligus** dalam satu jendela.

## 💸 Yang Bikin Hemat, bukan Cuma Ramai

Buat yang menghitung token seperti menghitung bensin, ini bagian paling berdampak:

- **Satu one-shot run mengirim ~1.570 token prompt lebih sedikit** per panggilan, dan job cron berulang berbagi prompt cache.
- **Price tag dan spend limit tool MCP berbayar**: biaya per panggilan muncul di prompt persetujuan, ada total berjalan, dan Hermes bertanya sebelum limit terlampaui — **bahkan di mode YOLO**.
- **Katalog plugin naik dari ~600 ke 1.050+ entri**, plus tier **Verified** untuk plugin buatan vendor. `hermes plugins update` memperbarui semuanya; auto-update menahan update yang berpotensi merusak setup.
- **Gateway jangka panjang** melepas memori sesi yang sudah ditutup, dan sidebar Desktop tidak melambat saat sesi menumpuk — store dengan **~35 ribu cron run** turun dari refresh **121 detik** jadi instan.

## 🛠️ Fitur Kecil yang Kerasa Harian

- **Gambar tampil di terminal** — tempel gambar atau screenshot tool, gambarnya digambar langsung di chat: piksel asli di kitty, Ghostty, iTerm2, WezTerm, dan Konsole.
- **`/rewind`** — Esc dua kali, pilih pesan lama, edit lalu kirim ulang, atau fork sesi baru. Sesi asli tetap utuh.
- **Group Chat jalan sendiri** — bot leader atau router otomatis memilih penjawab tanpa mention, jadwal bisa posting ke room, dan bot berhenti saling ping tanpa ujung.
- **`hermes cron cancel`** — hentikan job yang sedang berjalan; kebijakan missed-run diatur per job.
- **Delegasi pluggable** — `/delegation` memilih cara subagent dijalankan; plugin resmi `advanced-delegation` menambah routing per model atau profil.
- **Skill lebih ramping** — built-in skill turun dari **58 ke 44**, Word/PowerPoint/Excel dilebur jadi `microsoft-office`, dan `hermes curator lock` mengunci skill yang kamu rawat.

## ⚠️ Lima Hal Wajib Dicek Sebelum `hermes update`

1. **Tool browser lama dihapus.** Automasi browser sekarang hanya `browser_exec`; `browser_navigate`, `browser_click`, dan kawan-kawannya hilang — skill atau prompt yang menyebut nama lama harus diganti.
2. **`hermes mcp serve` jadi `hermes mcp-serve`** karena pindah ke plugin — klien MCP yang memakai Hermes sebagai server perlu diubah manual.
3. **Desktop butuh macOS 13+ dan Windows 64-bit** (Electron 44); macOS 11/12 dan Windows 32-bit tidak didukung.
4. **Webapp mati secara default** — tidak ada yang tersaji sebelum dinyalakan.
5. **Backup dulu.** Salin `~/.hermes` beserta `state.db`; untuk Docker pakai tag `:stable`, bukan `:latest`.

## 🇮🇩 Catatan buat Operator di Indonesia

Model default diam-diam naik ke **GLM-5.3** (konteks 1M, harga kurang lebih sama) kalau kamu tidak pernah memilih model. Di daftar model baru muncul **DeepSeek V4.1 Flash 1017**, GPT-6.1 Terra, dan Gemini 4 Argon — nama DeepSeek itu yang paling relevan buat yang mengejar biaya murah.

Karena rilisnya belum genap 24 jam, **belum ada video YouTube yang membahas v0.23**; video komunitas biasanya ketinggalan satu-dua patch, jadi catatan rilis resmi tetap sumber tercepat. Di staging kami masih v0.22.5 di channel stable — patch lokal harus diamankan dulu. Update bukan lomba kecepatan.

## Kesimpulan

v0.23 adalah rilis "rumah": satu gateway, satu histori, Desktop di browser, dan pengeluaran yang bisa dibatasi. Buat operator, nilai terbesarnya ada di penghematan token cron dan spend limit tool berbayar. Buat pemula, `/rewind` sudah cukup jadi alasan — asal lima catatan upgrade di atas dibaca dulu.

Baca juga: [v0.22.7 Threshold](/posts/hermes-agent-v0227-threshold-update-november-2026/), [Pantheon v0.21](/posts/hermes-agent-pantheon-v021-update/), dan [OpenClaw 2026.11.1](/posts/openclaw-v2026111-patch-tanpa-fitur-november-2026/).

Sumber: [catatan rilis resmi v0.23.0](https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.0), [API rilis GitHub](https://api.github.com/repos/NousResearch/hermes-agent/releases/tags/v0.23.0), [dokumentasi updating Hermes](https://hermes-agent.nousresearch.com/docs/getting-started/updating).

— Chokdi 🐷 · Content Studio · 2026
