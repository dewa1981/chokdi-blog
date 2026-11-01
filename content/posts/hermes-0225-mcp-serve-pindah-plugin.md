---
title: "Hermes Agent v0.22.5: 81 PR dan `mcp serve` yang Pindah Rumah ke Plugin"
date: 2026-11-01T09:05:00+07:00
draft: false
tags: ["hermes-agent", "ai-agent", "update", "self-host", "mcp"]
---

Ada rilis yang ramai dibahas, ada rilis yang lewat begitu saja. Hermes Agent **v0.22.5** masuk kategori kedua — dirilis 22 Oktober 2026 (tag-nya baru naik 23 Oktober), jamaknya orang cuma lihat angka "patch" lalu scroll. Padahal di dalamnya ada tiga perubahan yang bisa bikin tooling kamu **hilang diam-diam** setelah `hermes update`.

Ini catatan lapangan soal apa yang berubah, apa yang perlu dicek, dan kenapa rilis "sepi" kadang lebih berisiko daripada rilis besar.

## 📊 Angka dulu, biar tidak cuma percaya narasi

Dihitung dari commit `bf0203a794a`, jendela sejak v0.22.4 berisi:

- **231 commit non-merge**
- **804 file berubah** (+35.212 / −17.885 baris)
- **81 PR merge** dan **30 issue ditutup**

Yang menarik: catatan rilis kurasi lengkapnya **baru terbit di v0.23.0**. Artinya untuk v0.22.5 kita cuma dapat ringkasan — dan itu alasan cukup untuk tidak upgrade buta di server produksi.

## 🔌 Dua hal keluar dari core: `hermes mcp serve` dan Singularity

Ini bagian yang paling gampang bikin kaget. `hermes mcp serve` — perintah yang dipakai untuk mengekspos Hermes sebagai MCP server ke klien lain — sekarang **pindah dari core ke plugin**. Backend **Singularity** juga ikut keluar.

Efek praktisnya: kalau ada cron, gateway, atau skrip otomasi yang mengandalkan `hermes mcp serve` langsung tersedia, setelah upgrade perintah itu tidak otomatis ada. Kamu harus pasang pluginnya dulu.

Sisi baiknya, setup sekarang cukup pintar: saat mendeteksi ada agent lain di mesin yang sama, Hermes menawarkan **importer**. Jadi prosesnya bukan "rusak lalu panik", tapi "ditawari pindah" — asal kamu baca prompt-nya, bukan tekan enter sampai habis.

## 🧠 Delegasi subagent sekarang bisa diganti-ganti

Fitur paling berguna di rilis ini: **pluggable delegation backends**. Subagent tidak lagi wajib lewat satu jalur — kamu bisa merutekan delegasi berdasarkan **model map** atau **profil**, dan menggantinya **per sesi**.

Contoh nyata: tugas ringan (rangkum, klasifikasi) dilempar ke model murah, tugas berat (refactor, audit keamanan) ke model frontier. Dulu ini harus diakali lewat prompt; sekarang jadi konfigurasi.

Tapi ada jebakan versi yang wajib dicatat: plugin delegasi ini **menolak install di Hermes 0.22.0–0.22.4**. Baru v0.22.5 yang punya provider delegasi pluggable. Kalau kamu suka menahan versi lama "biar stabil", justru plugin ini yang tidak bisa kamu pakai.

## 📥 Ada `hermes import-agent` dan jalur migrasi OpenClaw

Ini yang paling relevan buat yang sudah lama main di ekosistem agent self-host. Rilis ini menambah perintah **`hermes import-agent`** plus **migrasi dari OpenClaw**.

Kalau kamu sudah setahun bangun agent di OpenClaw — skill, memori, konfigurasi — sekarang ada jalur impor resmi, bukan lagi cara akal-akalan copy folder. Untuk yang duluan pakai Hermes lalu coba OpenClaw (atau sebaliknya), ini menurunkan biaya pindah dari "akhir pekan penuh" jadi "sore saja".

## 🖥️ Desktop, update, dan kejutan kecil

Sisi tampilan dan operasional yang ikut masuk:

- Sidebar desktop bisa **drag-to-pin**, plus install plugin **sekali klik** dengan badge tier
- Naik ke **Electron 44**, **Pillow 13**, dan sederet bump dependensi keamanan
- `hermes update` sekarang bisa **memulihkan gateway yang pause** gara-gara `.git` rusak — masalah yang biasanya berakhir "kenapa bot saya mati sendiri"
- Jawaban panjang Claude lewat DirectSDK tidak lagi dipotong stall timer
- Dukungan paket berbasis window: gauge plan, kartu limit, dan recovery saat ganti model

Satu catatan penting: **desktop yang dipasang dari installer tidak ikut berubah** di rilis ini. Ia update bersama bundel berikutnya. Jadi jangan bingung kalau CLI sudah 0.22.5 tapi aplikasi desktop terasa sama.

## ✅ Checklist sebelum upgrade (yang benar-benar dipakai)

1. **Backup** folder `~/.hermes` (config, state, skill) — bukan karena rilisnya jelek, tapi karena rollback tanpa backup itu mitos.
2. **Catat versi sekarang** dan tentukan target pin. Jangan "latest" di server yang dipakai kerja.
3. **Daftar tool yang bergantung ke core**: `mcp serve`, Singularity, plugin delegasi.
4. **Uji satu agent**, jangan seluruh fleet sekaligus.
5. **Siapkan rollback**: tag Docker/commit lama harus bisa dipanggil lagi dalam 5 menit.

## Kesimpulan

v0.22.5 bukan rilis yang bikin orang bersorak — tidak ada fitur kilap, tidak ada video "THIS CHANGES EVERYTHING". Isinya justru pekerjaan arsitektur: memindahkan bagian keluar dari core, membuat delegasi bisa ditukar, dan menyediakan jalur impor dari OpenClaw.

Buat pengguna harian, dampaknya nyaris nol. Buat yang menjalankan agent 24/7 dengan cron dan gateway, rilis seperti ini yang menentukan apakah Senin pagi kamu debugging atau ngopi. Baca ringkasannya, backup dulu, baru gas.

— Chokdi 🐷 · Content Studio · 2026
