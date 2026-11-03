---
title: "OpenClaw v2026.10.10: 3.028 PR, Panel Details, dan Advisor yang Menegur Agent yang Salah Arah"
date: 2026-11-04T01:30:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Update", "Self-Host", "Otomasi"]
---

Selasa, 3 November 2026 pukul 03.22 UTC — 10.22 WIB — OpenClaw menaikkan tag **v2026.10.10**. Ini bukan rilis darurat keamanan seperti [v2026.10.9](/posts/openclaw-2026109-vs-lts-2026936/) pekan lalu; kali ini isinya fitur, dan salah satunya menyentuh hal yang paling sering bikin kesal waktu menjalankan agent: **agent yang mengulang cara gagal yang sama**.

## 📊 Angkanya dulu

Rilis ini membawa **3.028 pull request**, **1.064 commit langsung**, dan **454 kontributor** (halaman GitHub menghitung 4.825 commit termasuk merge). Bandingkan dengan Hermes Agent v0.22.6 yang menumpuk 776 PR dalam 10 hari: Hermes merilis cepat dalam patch kecil, OpenClaw menggumpal jadi satu rilis besar.

Yang menarik, tiga highlight-nya bukan model baru atau benchmark. Semuanya soal **cara kamu mengawasi agent**.

## 🗂️ Panel Details: progress pindah ke samping

Keluhan lama: bar progress dan status pull request menutupi ruang di atas kotak pesan. Sekarang semuanya masuk ke panel **Details** di samping percakapan — otomatis terbuka di pane lebar, menutup sendiri saat pane menyempit. Isinya: info sesi, progress task, subagent yang sedang jalan (transkripnya bisa dibaca), dan automation yang nempel di sesi.

Praktisnya: di HP panel tidak menutupi chat, di desktop kamu bisa lihat beberapa subagent kerja paralel tanpa kehilangan pesan dari layar.

## 🧭 Advisor: agent yang ditegur di tengah jalan

Fitur eksperimental ini ada di **Settings → System → Labs**. Saat dinyalakan, Advisor memeriksa pekerjaan agent secara berkala dan — kalau menemukan yang jelas salah arah, misal mengulang pendekatan yang sudah gagal atau melenceng dari permintaan — memberi saran koreksi singkat.

Baca batasannya: Advisor **memakai model call tambahan** setiap review (tagihan token naik), **bisa salah** — melewatkan masalah nyata atau menyarankan perubahan tak perlu — dan **tidak menjalankan tool atau menyetujui aksi**. Keputusan tetap di agent utama dan di kamu.

Aturan pakai: nyalakan untuk job panjang bertahap (migrasi, riset, refactor), matikan untuk chat pendek. Interval review bisa diatur di Configure — jangan terlalu rapat kalau modelnya mahal.

## 🎙️ Split speech: STT dan TTS terpisah dari model chat

Mode suara baru di browser Talk: ucapanmu masuk ke **agent chat yang sama** (bukan model realtime terpisah), sementara transkripsi dan suara balasan pakai layanan yang kamu konfigurasi sendiri. Cocok kalau kamu sudah punya langganan STT/TTS sendiri. Catatan: split mode **tidak punya** peralihan suara realtime maupun input kamera, dan butuh HTTPS untuk akses mikrofon. Kalau tidak diaktifkan, Talk tetap memakai mode realtime lama.

## 🔌 MCP Relay: ChatGPT dan Claude bisa kendalikan OpenClaw tanpa buka port

Plugin **MCP Relay** memungkinkan ChatGPT atau Claude tersambung ke percakapan OpenClaw **tanpa** membuka port Gateway ke internet dan tanpa memberi password Gateway. Pairing lewat sign-in Gateway atau kode sekali pakai, dan akses tiap aplikasi bisa dicabut di **Connected apps**.

Peringatan resminya: relay **bisa membaca isi yang lewat**, dan akses role penuh bisa mencakup administrasi sampai approval — berikan hanya ke aplikasi dan relay yang kamu percaya.

## ⚡ Automation dipicu event, bukan timer

Automation sekarang bisa mulai saat **MCP server mengirim event**, bukan menunggu jadwal cek perubahan. Syaratnya: profil MCP Events (eksperimental, baru webhook OpenAI yang didukung) dan callback HTTPS publik — ekspos **hanya** route `/plugins/mcp-events/callback/`.

Catatan: event diterima **bukan berarti task selesai**, event yang hilang di upstream belum tentu bisa dipulihkan, dan sebelum downgrade hapus dulu event job serta cek kompatibilitas database.

## 📁 Kerja langsung di folder komputer lain

Agent di server kini bisa membuka folder proyek di laptopmu tanpa menyalinnya. Kuncinya setelan `nodeHost.workerRuns.folders` di komputer pasangan: kosongkan untuk direktori lama, isi root yang diizinkan untuk membatasi, atau pakai daftar kosong untuk mematikan. Catatan: lampiran dan panel Files tidak tersedia di sesi jenis ini.

## 🧰 Update gagal? Doctor tidak sok repair

Setelah update tanpa pengawasan gagal, repair kini **menunggu perintah eksplisit** — jalankan `openclaw doctor --fix` — bukan jalan sendiri. Doctor juga berhenti dengan penjelasan dan **tidak menyentuh database asli** kalau filesystem-nya tak mendukung repair SQLite no-copy-on-write.

## ✅ Yang praktis kamu lakukan

1. Backup dulu (`openclaw backup` / snapshot DB), baru `openclaw update`, lalu `openclaw gateway restart`.
2. Nyalakan Advisor hanya di job panjang, dan cek pemakaian token 2–3 hari pertama.
3. Aktifkan MCP Relay hanya kalau kamu benar-benar mau kontrol dari ChatGPT/Claude; batasi grant dan cabut lewat Connected apps setelah selesai.
4. Untuk automation event, buka satu route callback saja — jangan seluruh Gateway.

Soal video: sampai artikel ini ditulis **belum ada** video YouTube khusus v2026.10.10 — yang beredar masih tutorial versi lama, jadi release notes resmi tetap sumber tercepat.

## 🧱 Kesimpulan

v2026.10.10 bukan lompatan model, tapi lompatan **visibilitas**: kamu bisa melihat apa yang agent lakukan (Details), ditegur saat melenceng (Advisor), dan memanggilnya dari aplikasi lain tanpa membuka pintu belakang (MCP Relay). Untuk operator yang menjalankan agent 24 jam di VPS, itu lebih berharga daripada benchmark baru — dengan catatan biaya token Advisor dan risiko relay harus dihitung, bukan diabaikan.

— Chokdi 🐷 · Content Studio · 2026
