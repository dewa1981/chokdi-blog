---
title: "Hermes Agent v0.20.6 Rilis: 525 PR dalam Seminggu, Ini yang Wajib Kamu Tahu"
date: 2026-08-29T01:35:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Tutorial"]
---

Nous Research baru saja merilis **Hermes Agent v0.20.6** pada 27 Agustus 2026 — dan angka di baliknya bikin melongo: sekitar **1.313 commit, 1.557 file berubah, plus 525 pull request** yang digabung hanya dalam satu minggu sejak v0.20.5. Sebagai salah satu open-source agent terbesar di dunia (sudah **238 ribu bintang** di GitHub), update ini bukan sekadar tambal sulam — ini sinyal kalau ekosistem agent AI makin serius.

Kabar ini juga jadi perhatian karena TechCrunch memberitakan Nous Research sedang negosiasi pendanaan baru dengan valuasi **US$1,5 miliar**. Kombinasi rilis agresif + valuasi gede = momentum yang layak disimak, terutama buat kamu yang mulai serius pakai agent AI. Berikut hal-hal praktis yang paling penting.

## 🚀 Real-Profile Browsing: Browser Bisa "Login" Sendiri

Fitur paling disorot di v0.20.6 adalah **consent-gated real-profile browsing**. Artinya, agent sekarang bisa browsing pakai profil Chromium default kamu — lengkap dengan sesi login yang sudah ada — tapi tetap butuh persetujuan di tiap langkah (ada alur *close-with-approval* khusus di Windows). Buat yang sering minta agent mengambil data dari akun pribadi, ini mengubah permainan: tidak perlu lagi repot login ulang atau kasih cookie manual.

Bonusnya, desktop Browser sekarang punya **jendela OS sendiri** plus *managed SSH remote-update engine* — pembaruan agent bisa dikelola dari jarak jauh dengan rapi.

## 🔌 50+ MCP Server Siap Pakai

Satu hal yang bikin Hermes makin "nyambung" ke dunia nyata: katalog MCP (Model Context Protocol) melebar ke **50+ server vendor yang sudah live-verified** — termasuk **Cloudflare, Grafana Cloud, Better Stack, dan Railway**. Artinya, integrasi ke infrastruktur favorit kamu tidak perlu lagi merakit sendiri dari nol; tinggal pilih dari katalog. Buat yang kerjaan sehari-harinya urusan server dan deploy (seperti admin VPS), ini langsung terasa manfaatnya.

## 🧠 Agent Makin Cerdas & Hemat

Beberapa penyempurnaan internal yang dampaknya terasa langsung di pemakaian harian:

- **TTL result caching** untuk `web_search` dan `web_extract` — hasil pencarian yang sama tidak perlu diambil ulang, lebih cepat dan hemat token.
- **Lean-tail compression jadi default** — obrolan panjang tidak gampang meledak konsumsi konteks.
- **Multi-query tool_search dengan stemming** — mencari tool yang tepat jadi lebih akurat dengan satu perintah.
- **Cron durable-incident acks** — pekerjaan terjadwal yang gagal lebih jelas statusnya, tidak senyap hilang.

## 🔒 Keamanan & Model Baru

Dari sisi keamanan: ada **opt-in OS-keychain encryption** untuk menyimpan secret (tidak lagi muncul prompt Keychain macOS tiap launch), dan updater sekarang **menjeda gateway lewat control socket** alih-alih mematikannya paksa — risiko crash saat update turun drastis. Instalasi via image/package juga menolak update in-place yang tidak aman.

Model baru ikut masuk ke picker: **GLM-5.3-Flash, MiniMax M3 (gratis), dan MiniMax H3 Max** untuk video. Jadi opsi model makin variatif, dari yang ringan sampai yang berat.

## 💡 Poin Praktis Buat Kamu

1. Update ke versi terbaru cukup jalankan `hermes update`; untuk instal baru: `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`.
2. Coba real-profile browsing untuk tugas yang butuh sesi login — tapi pastikan fitur consent tetap aktif demi keamanan.
3. Manfaatkan katalog MCP baru: kalau pakai Cloudflare atau Grafana, integrasinya tinggal pilih, bukan setup manual.
4. Catatan rilis lengkap akan dibundel di **v0.21.0** — update ini sengaja cepat untuk menstabilkan semua PR yang menumpuk.

## ✍️ Kesimpulan

Hermes Agent v0.20.6 membuktikan satu hal: ritme pengembangan agent open-source sekarang bukan bulanan lagi, tapi mingguan. Dengan browser yang bisa "login", 50+ MCP siap pakai, dan dukungan keamanan yang makin rapi, ini panggung yang bagus menuju v0.21.0. Kalau kamu masih ragu mencoba agent AI, sekarang saat yang pas — apalagi kabar valuasi US$1,5 miliar menunjukkan ekosistem ini serius.

Menurutmu fitur mana yang paling kamu tunggu? Tulis di kolom komentar ya — siapa tahu jadi bahasan artikel berikutnya.

— Chokdi 🐷 · Content Studio · 2026
