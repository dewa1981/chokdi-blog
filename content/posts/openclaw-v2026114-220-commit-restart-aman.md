---
title: "OpenClaw v2026.11.4: 220 Commit, 90 Kontributor — Rilis Stabil yang Bikin Upgrade Database Aman"
description: "OpenClaw 2026.11.4 keluar 16 November 2026 (220 commit, 125 PR, 90 kontributor). Fokusnya upgrade database yang aman, privasi side chat, dan restart yang tidak menghilangkan pesan."
date: 2026-11-17T01:21:28+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Keamanan", "Update", "Self-Host"]
---

Senin, 16 November 2026 pukul 11.17 WIB, OpenClaw menandatangani **v2026.11.4** — rilis stabil terbaru, terhitung kurang dari 24 jam sebelum artikel ini ditulis. Angkanya **220 commit, 125 pull request, dan 90 kontributor**. Tidak ada menu baru yang bisa dipamerkan, dan justru itu intinya: ini tambalan untuk orang yang menjalankan agent 24/7, bukan untuk orang yang suka demo fitur.

Konteksnya: dalam enam hari OpenClaw melepas tiga rilis stabil (2026.10.10, 11.1, 11.2) plus 11.3, dan sekarang 11.4. Kalau kamu mengelola bot di VPS, pertanyaannya bukan "apa yang baru" tapi **"kalau saya update, apa yang bisa rusak?"** — jawaban versi ini cukup melegakan.

## ⬆️ Inti rilis: upgrade tidak lagi bisa merusak database

Ini bagian yang paling layak dibaca, terutama kalau kamu pernah kena kasus CLI sudah versi baru sementara daemon Gateway masih versi lama.

Sebelum patch, urutan itu bisa memicu **migrasi database bersama melewati daemon yang masih lama**. Sesudah 11.4, CLI baru menolak memigrasikan database yang dipakai daemon lebih tua, sementara database instalasi lain tetap dibiarkan independen. Efek praktisnya: kamu bisa update paket lebih dulu tanpa takut daemon lama bangun dengan skema yang tidak dia kenal.

Tiga pengaman lain di rilis yang sama:

- **Save file basi ditolak** — editor yang masih memegang draf lama tidak menimpa file di workspace baru.
- **Perubahan delegasi wajib approval**, dan grant-nya diperiksa ulang di setiap efek — bukan sekali di awal.
- **PostgreSQL menghormati `synchronous_commit` dari server**, sementara transaksi port dan backup tetap durable.

## 🔐 Privasi: yang biasanya baru terasa setelah bocor

Rilis ini menutup beberapa jalur yang jarang dibahas di video, tapi sering jadi temuan audit:

- **Side chat** dibatasi ke pemirsa yang benar-benar terautentikasi, bukan siapa pun yang memegang tautan.
- **Foto dan screenshot dari paired-node** jadi privat secara default.
- **Proyeksi prompt internal** tidak lagi muncul di output tampilan.
- Teks berbentuk kredensial di ringkasan compaction disamarkan (riwayat tersimpan tidak diubah), dan kredensial PostgreSQL aktif tidak lagi diwariskan ke environment proses anak.
- **Kode setup iOS** tidak disimpan permanen setelah ditempel, dan daftar pengirim IRC yang dikosongkan kini berarti tolak semua — bukan jatuh ke akses lebih longgar.

Untuk agent yang menjawab pelanggan, dua poin pertama itu yang paling relevan: keduanya soal siapa yang boleh melihat percakapan orang lain.

## 🔁 Restart dan pesan yang menggantung

Mekanismenya sudah kita bahas di catatan [2026.11.5-beta.3](/posts/openclaw-2026-11-5-beta-3-restart-sesi-besar/). Ringkasnya: prompt yang belum dijawab **diselamatkan melewati restart Gateway**, balasan final WhatsApp tidak tertahan reload yang tidak berhubungan, dan pesan Signal yang sempat buffer saat reconnect benar-benar dikirim. Bagi pengguna jalur stabil, ini kali kedua perbaikan itu bisa dipasang tanpa ikut beta.

## 🧠 Sesi besar: memori worker dijaga, bukan ditambah

Pemangkasan transcript besar, ekspor memori berpaging, dan perbaikan Doctor sekarang **dibatasi** supaya tidak menghabiskan memori worker. Startup penyimpanan besar juga diubah: plugin dinyalakan sebelum pemindaian orphan, dan kandidat recovery dipindai tanpa memuat ringkasan sesi lain. Detail kecil yang gampang terlewat — kalau penggabungan Doctor gagal, `MEMORY.md` **dipertahankan**, bukan diganti file kosong.

## 🧩 Perbaikan kecil yang bikin pusing di lapangan

- Tool schema **Gemini dan Vertex** tidak lagi mengirim `enum` pada tipe non-string, jadi parameter boolean diterima.
- **Claude CLI** menguras event inisialisasi supaya pesan hook tidak membuat startup deadlock.
- Katalog model **Z.AI** tidak lagi diarahkan ke endpoint salah, pemilihan off-catalog tidak menerima hasil basi, dan request **Claude 5** tidak lagi dipotong 32.000 token.
- Doctor tidak mengimpor kredensial plaintext kalau provider sudah punya SecretRef, dan mount skill bersarang di sandbox dilindungi dari parent writable.

## ⚠️ 11.5 sudah di depan pintu

Di hari yang sama terbit **v2026.11.5-beta.4**: widget interaktif dirender sebagai pesan Telegram, pembacaan transcript saat database disiapkan, dan perbaikan kontinuitas otomasi. Masih *prerelease* — untuk bot yang dipakai jualan atau menagih pelanggan, tetap di 11.4.

## 🔍 Cek fakta: klaim "1.000 model muncul otomatis" di YouTube

Ada video 9 November (kanal Jarvis AI Podcast) yang menyebut OpenClaw 2026.11.2 membawa katalog model hosted berisi sekitar **1.000 model** yang menyegarkan diri tanpa restart gateway. Changelog resmi 2026.11.2 justru berbunyi **"patch release with no new features"** — 113 pull request, 53 commit langsung, 64 kontributor. Isu katalog model memang ada, tapi baru mendarat di 11.4 sebagai perbaikan. Kesimpulannya: **baca changelog, jangan baca judul video**.

## ✅ Checklist update ala Chokdi

1. **Backup dulu** — salin file database, jangan buka yang sedang live.
2. **Catat versi sekarang**, lalu **staging dulu** kalau bot-mu menyentuh uang atau pesan pelanggan.
3. Update, lalu periksa empat hal: gateway hidup, pesan terjawab, memori tidak membengkak, channel tersambung.
4. Naikkan ke produksi **satu server sekali jalan**.

## Kesimpulan

v2026.11.4 bukan rilis yang bikin kamu screenshot menu baru. Ini rilis yang membuat **upgrade antar versi daemon aman**, side chat tidak bisa dibaca orang yang salah, dan pesan yang belum dijawab tidak hilang saat restart. Untuk ongkos satu kali update, itu tukar yang bagus.

Kamu di versi berapa — dan channel apa yang paling sering bikin pesan hilang? Tulis di komentar.

**Sumber:** [rilis v2026.11.4](https://github.com/openclaw/openclaw/releases/tag/v2026.11.4), [changelog 2026.11.4](https://raw.githubusercontent.com/openclaw/openclaw/main/CHANGELOG/2026.11.4.md), [changelog 2026.11.2](https://raw.githubusercontent.com/openclaw/openclaw/main/CHANGELOG/2026.11.2.md), [video Jarvis AI Podcast 9 Nov 2026](https://www.youtube.com/watch?v=ydiOIzB0EUc), [Hermes Agent v0.23.1 (rilis stabil pembanding)](https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.1).

**Baca juga:** [OpenClaw v2026.11.1: 83 PR Tanpa Satu pun Fitur Baru — Patch yang Menyelamatkan Agent yang Diam-Diam Rusak](https://chokdi.ano99.com/posts/openclaw-v2026111-patch-tanpa-fitur-november-2026/) · [OpenClaw September 2026: Update Tanpa Downtime, tapi Ada Jebakan Schema 21](https://chokdi.ano99.com/posts/openclaw-update-tanpa-downtime-sep-2026/) · [OpenClaw 2026.9.4 Rilis: Update Gagal Kini Bisa Balik Sendiri ke Versi Lama](https://chokdi.ano99.com/posts/openclaw-202694-rollback-update-gagal/)

— Chokdi 🐷 · Content Studio · 2026
