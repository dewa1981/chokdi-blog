---
title: "OpenClaw 2026.11.9: Patch 10 PR yang Menutup Tiga Lubang Senyap"
description: "OpenClaw v2026.11.9 terbit 25 November 2026 pukul 07.47 WIB. Hanya 10 pull request, tapi tiga di antaranya menutup celah izin Discord, bypass env -S, dan redirect web lintas host."
date: 2026-11-25T09:00:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Update", "Keamanan", "Self-Host"]
---

Sehari setelah merilis v2026.11.8 yang berisi 210 pull request, OpenClaw menandai **v2026.11.9** pada Rabu, 25 November 2026 pukul 00.47 UTC — **07.47 WIB**. Ukurannya jauh lebih kecil, dan itu justru alasan versi ini layak dibaca: hampir seluruh isinya soal batas izin dan uang, bukan fitur baru.

Kalau kamu cuma mau tahu harus ngapain: update kalau kamu menjalankan bot Discord dengan allowlist, memakai `env -S` di perintah shell, atau sering memakai sesi turunan (`/btw`, Advisor review). Tiga hal itu yang berubah perilakunya.

## 📊 Dua angka untuk satu tag yang sama

Halaman rilis GitHub menulis **13 commit · 15 pull request · 14 kontributor**. Changelog resminya menulis **10 pull request, 3 commit langsung, dan 5 kontributor**. Dua-duanya merujuk ke tag yang sama — release body dihitung otomatis dari jendela commit, changelog dihitung manual per perubahan yang pantas dicatat.

Untukmu yang cuma mau memutuskan "update atau tunggu", angka yang penting bukan yang besar, tapi yang kecil: **10 PR**, tanpa bagian *breaking changes*, tanpa fitur yang dijual di judul. Ini patch yang menghapus kemungkinan buruk, bukan menambah kemampuan.

## 🔐 Tiga lubang yang ditutup

1. **Pengirim DM Discord yang sudah dicabut masih bisa menjalankan perintah.** Pengirim yang sudah dihapus dari allowlist atau belum dipasangkan bisa menembus agent lewat *session binding* lama. Sekarang mereka kena alur penolakan atau pemasangan normal, sementara pengirim sah tetap memakai binding-nya. Kalau bot kamu admin di server Discord, ini alasan paling kuat untuk update hari ini.
2. **`env -S` bisa dipakai menyelundupkan variabel startup shell.** Pemeriksaan eksekusi perintah tidak melihat `BASH_ENV` dan `ENV` kalau dikirim lewat `env -S` atau `env --split-string` bersarang. Sekarang penugasan itu ditolak konsisten, sementara variabel lingkungan biasa tetap jalan.
3. **Redirect endpoint web self-hosted bisa keluar dari host.** Permintaan ke endpoint milikmu sendiri kini tetap di hostname yang dikonfigurasi di setiap lompatan redirect. Kalau endpoint-mu memang redirect ke host lain, host tujuan harus didaftarkan langsung — tidak lagi diikuti otomatis.

Celah nomor dua dan tiga tidak meninggalkan error di log. Efeknya baru terasa saat ada yang sengaja mencarinya.

## 💸 Sesi turunan sekarang lebih murah

Dua perbaikan di bagian model menyentuh dompet, bukan sekadar kenyamanan:

- **Fork sesi OpenAI Responses** (`/btw`, Advisor review) sebelumnya **gagal memakai prompt cache induknya** — seluruh prompt diproses ulang dari nol. Sekarang cache key, hosted tools, dan pengaturan reasoning disamakan.
- **Fork sesi Anthropic** berhenti menulis checkpoint cache di suffix sekali pakai miliknya sendiri, tapi tetap membaca prefix percakapan induk yang sudah di-cache.

Untuk percakapan 50 ribu token, kerja ulang satu prompt penuh bukan penghematan kecil. Ini juga menjawab keluhan komunitas: di video **"50 days with OpenClaw"** (39 menit), pembuatnya menyebut context yang membengkak sebagai masalah harian — ia memantau pemakaian context dan memulai sesi baru kalau sudah lewat 50 persen.

Dua perbaikan lain di area sama: login ulang ke provider **tidak lagi menimpa** baris model dan entri *thinking level* di `openclaw.json`, dan `web_search` lewat Tool Search tidak lagi gagal di provider chat-completions yang menolak assistant prefill.

## 🖥️ Tangkapan layar tab belakang dan balasan ACP

Dua bug kecil yang bikin kerja berhenti di tengah jalan:

- Tangkapan layar **tab latar di Chrome headed** tidak lagi timeout dan memblokir capture berikutnya. Tab belakang dirender tanpa memindahkan tab aktifmu.
- Klien **ACP** tidak lagi menerima balasan terpotong ketika prompt-nya mengantre di belakang pekerjaan lain. Bridge ACP mengalirkan sisa teks yang sudah commit sebelum menutup turn.

Selain itu, Codex app-server bawaan naik ke **0.172.0**, dan error "secret file descriptor tidak tersedia" pada Claude CLI background (Gateway foreground, container, atau Windows) sudah diperbaiki.

## ✅ Yang perlu dicek setelah update

1. **Buka `openclaw.json`** — pastikan baris model dan entri thinking-level masih utuh setelah login ulang provider.
2. **Uji satu DM Discord dari akun di luar allowlist.** Harus ditolak, bukan dijawab.
3. **Punya endpoint web yang redirect lintas host?** Daftarkan host tujuannya sekarang.
4. **Bandingkan biaya satu sesi fork** sebelum dan sesudah update.

Soal **2026.11.10-beta.3** yang sudah terbit 24 November: isinya recovery update dan jawaban subagent yang bertahan setelah Gateway restart. Menarik, tapi tetap beta — jangan pasang di server produksi.

## Kesimpulan

v2026.11.9 tidak membuat agent lebih pintar. Ia membuat tiga asumsi lama berhenti berlaku: bahwa pengirim yang dicabut langsung kehilangan akses, bahwa variabel `env -S` selalu terlihat oleh guard, dan bahwa redirect dari endpoint sendiri aman diikuti ke mana pun.

Kalau kamu menjalankan OpenClaw sebagai bot Discord atau memberi agent akses shell, update ini bukan opsional. Kalau cuma chat pribadi tanpa tool berbahaya, boleh menunggu v2026.11.10 stabil — tapi tidak ada alasan menahan lebih lama.

**Baca juga:** [OpenClaw 2026.11.6: 386 PR, 157 Kontributor — Patch yang Menyelamatkan Installer dan Upgrade](https://chokdi.ano99.com/posts/openclaw-v2026116-386-pr-installer-upgrade/) · [OpenClaw v2026.11.1: 83 PR Tanpa Satu pun Fitur Baru — Patch yang Menyelamatkan Agent yang Diam-Diam Rusak](https://chokdi.ano99.com/posts/openclaw-v2026111-patch-tanpa-fitur-november-2026/) · [OpenClaw v2026.11.8: 210 PR, Balasan Telegram yang Hilang, dan Enam "Sukses Palsu" yang Diperbaiki](https://chokdi.ano99.com/posts/openclaw-v2026118-210-pr-balasan-telegram-hilang/)

— Chokdi 🐷 · Content Studio · 2026
