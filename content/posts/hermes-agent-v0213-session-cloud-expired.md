---
title: "Hermes Agent v0.21.3 Rilis: Session Cloud/Desktop Tak Lagi Suka Expired"
date: 2026-09-15T05:15:00+07:00
draft: false
tags: ["Hermes Agent", "AI", "Update", "Self-Hosting"]
---

Habis update Hermes Agent, tiba-tiba kamu kelempar ke halaman login lagi padahal baru saja masuk? Atau dashboard Desktop nge-freeze pas dibuka pagi-pagi? Kalau iya, kamu bukan sendirian — dan kamu tidak perlu panik update ulang. Nous Research baru saja merilis **Hermes Agent v0.21.3 (v2026.9.14)** pada 14 September 2026, dan dua masalah itu justru jadi fokus utamanya.

Ini adalah *patch release*. Artinya bukan rilis fitur besar, tapi penambalan yang sengaja diterbitkan agar perbaikan spesifik sampai ke pengguna **Hermes Cloud** yang auto-update ke tag rilis terbaru.

## 📅 Konteks Rilis: Ada Apa di Balik v0.21.3?

Menurut catatan rilis resmi di repo GitHub-nya, tag ini menggulung **~338 PR** yang di-merge sejak v0.21.2. Kalau dihitung dari angka mentahnya, jendela rilis ini mencakup **1.036 non-merge commit** di **2.642 file** (+131.690 / −37.096 baris), dikerjakan oleh **140+ kontributor**.

Yang penting justru alasan tag ini dibuat, bukan jumlah barisnya. Tim menulisnya eksplisit: tag ini ada **supaya perbaikan sign-in remote gateway sampai ke Cloud agents**, karena agen Cloud auto-update ke tag rilis terbaru — sedangkan rilis sebelumnya trail di `main` saja.

## 🔐 Masalah #1: Session Remote Expired Saat Refresh Bersamaan

Ini masalah yang paling banyak dilaporkan pengguna Desktop/Cloud (isu #55712). Gejalanya begini:

- Kamu tinggal buka laptop, komputer bangun dari tidur (*wake burst*), lalu dashboard Desktop nembak beberapa request refresh sekaligus — bukan satu.
- Di sisi gateway, dua jalur refresh (cookie gate dan native bearer route milik Desktop) tidak saling menyapa. Beberapa request dengan token refresh yang sama tembus bersamaan.
- Portal mendeteksi token yang sama dipakai ulang → dianggap *reuse detection* alias indikasi token dicuri → **seluruh session dicabut**. Kamu terlempar keluar.

Perbaikannya elegan: kedua jalur refresh sekarang **menggabungkan (coalesce) request bersamaan yang membawa token refresh berputar yang sama**, sehingga satu token tidak mungkin "replay" ke deteksi reuse. Refresh juga dipindah keluar dari event loop, jadi kalau identity provider lambat, `/api/status` tidak ikut nge-freeze.

Efek sampingnya di sisi Portal (PR #1209): **batas idle 30 hari yang bergeser** plus **grace 5 menit untuk token yang baru diputar** — jadi sedikit keterlambatan jaringan tidak langsung membunuh sesi kamu.

## 🧹 Masalah #2: Proses Panjang Bocorkan Handle state.db Duplikat

Perbaikan kedua menutup isu #100896 dan #103339: proses yang hidup lama (gateway, backend dashboard/Desktop, ACP, pembaca CLI) menumpuk **handle penulis `state.db` duplikat**. Efeknya, database yang sehat tetap saja memunculkan peringatan `N live SessionDB handles` — sinyal yang bikin orang panik dan mulai curiga datanya rusak.

Sekarang pembaca menempel **read-only**, dan penulis in-process berbagi handle registry yang sama. Peringatan itu berhenti muncul di topologi yang normal.

## 🎁 Yang Ikut Numpang di Jendela Rilis Ini

Rilis ini juga membawa barang yang sengaja tidak dibuatkan dokumentasi panjang (disimpan untuk v0.22.0). Beberapa yang menarik untuk pengguna self-host:

- **Pemilihan reasoning effort** di setiap model picker, plus kontrol per-auxiliary di Desktop.
- **Login OpenRouter via OAuth PKCE** — tidak perlu lagi tempel API key manual.
- **Dukungan dekode gambar HEIF/HEIC/AVIF**.
- **JSON-RPC server→client** dan registry wire-contract Pydantic dengan TS/OpenRPC ter-generate untuk gateway TUI/Desktop.
- **MCP OAuth refresh token yang diikat ke issuer-nya**, plus pengingat re-auth harian di Desktop.
- Katalog FAL yang diperluas: **Wan 3.0, Kling 3.0 / Kling Image v3, MiniMax H3 Max Turbo, Gemini Omni Flash 1.1, dan Meta Muse**.
- Tabel tempel di **Slack** dan **Agent Sessions API**.
- Perbaikan isolasi *multiplexed-profile* dan liveness gateway.

## 🛠️ Cara Update

Tergantung cara kamu menginstal Hermes:

| Cara pasang | Perintah |
|---|---|
| Git install (VPS/self-host) | `hermes update` |
| Installer one-liner | jalankan ulang installer |
| Docker / Hermes Cloud | pakai tag `nousresearch/hermes-agent:v2026.9.14` |

Satu catatan penting untuk yang sudah memakai v0.21.x: kalau kamu tipe orang yang suka membuka `state.db` pakai `sqlite3` langsung saat gateway jalan — **jangan**. Koneksi mentah bisa membatalkan POSIX lock milik gateway dan memicu error WAL yang bikin sesi kamu terlihat "rusak" padahal datanya sehat. Ini akar masalah yang sama yang sedang dibereskan di seri 0.21.2 dan 0.21.3, jadi upayanya jelas mengarah ke arah sana.

## 💡 Kesimpulan

Hermes Agent v0.21.3 bukan rilis yang bikin kamu harus buru-buru uji fitur baru. Ini rilis yang bikin kamu **berhenti diganggu hal-hal sepele**: logout tiba-tiba, dashboard freeze, dan peringatan `state.db` palsu. Kalau kamu jalan di Hermes Cloud atau pakai Desktop yang sering sleep, tag ini murni perbaikan pengalaman — tidak ada alasan untuk menunda.

Sisi menariknya: v0.22.0 nanti akan membawa catatan rilis *curated* lengkap dari v0.21.0 ke atas. Jadi 338 PR yang sekarang masuk tanpa dokumentasi, nanti dibuka semuanya. Simpan sabar sedikit, karena jendela ini menyimpan banyak hal yang menarik.

Kalau kamu self-host Hermes, pernah kena kejadian session kepental saat laptop baru bangun tidur? Atau justru masalahmu beda? Cerita di kolom komentar — kalau cukup banyak yang sama, kita bedah jadi artikel troubleshooting tersendiri.

— Chokdi 🐷 · Content Studio · 2026
