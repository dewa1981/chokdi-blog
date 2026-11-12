---
title: "OpenClaw v2026.11.3: Patch Keamanan — Verifikasi Sertifikat Mati Kalau Fingerprint Kosong"
description: "Rilis keamanan OpenClaw 2026.11.3 (11 Nov 2026): TLS pin mati saat fingerprint kosong, approval shell bocor, env.vars ikut kebaca. Plus kenapa update bisa bikin Gateway mati."
date: 2026-11-12T09:12:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Keamanan", "Update", "Self-Host"]
---

Rabu, 11 November 2026 pukul 01.53 WIB, tag **v2026.11.3** ditandatangani dan langsung jadi rilis stabil terbaru OpenClaw. Halaman rilisnya menyebut ini **security release** dengan **nol fitur baru**: 56 pull request, 44 commit langsung, 36 kontributor. Kalau kamu menjalankan agent di server sendiri, ini wajib dibaca.

Sebab isi utamanya bukan tombol baru, tapi tiga hal yang selama ini diam-diam membuat rasa aman kamu salah.

## 🔓 Tiga celah yang paling layak dikhawatirkan

**1. Fingerprint TLS kosong = verifikasi sertifikat mati.** Ini yang paling serius. Sebelum patch, kalau transfer worker pakai pin TLS kosong, verifikasi sertifikat untuk upload dan download workspace **berhenti jalan**. Artinya koneksi tetap dianggap sah walau sertifikatnya bukan dari server yang kamu percaya. Sekarang pin kosong kembali memakai verifikasi CA normal, dan pin HTTPS yang formatnya rusak justru **ditolak**. Celah serupa juga ditutup di sisi node: flag fingerprint kosong tidak lagi mematikan pin sertifikat yang sudah tersimpan untuk endpoint Gateway yang sama.

**2. Approval otomatis bocor lewat `test` dan `[`.** Perintah shell dinamis seperti `test` dan `[` sebelumnya bisa lolos tanpa otorisasi normal di allowlist Gateway. Ini pintu kecil, tapi pintu kecil di agent = eksekusi perintah tanpa izin. Sekarang keduanya **wajib otorisasi normal**. Efek sampingnya perlu dicatat: beberapa nama file literal berisi karakter khusus kini bisa ditolak kalau approval dimatikan.

**3. Config bacanya terlalu terbuka.** `env.vars` yang berisi nilai inline bisa muncul di hasil baca konfigurasi, dan output config mentah tetap dicetak walau tidak bisa disensor dengan aman. Versi ini menutup keduanya.

Selain tiga itu, ada beberapa tambahan: preview gambar percakapan tidak lagi bisa membaca **di luar folder yang diizinkan** pada sesi required-sandbox — termasuk saat mode Full Access; environment daemon Signal yang dikelola OpenClaw tidak lagi mewarisi variabel kredensial yang tak berhubungan; dan teks completion privat tidak lagi bocor ke subscriber pesan sesi maupun ke Control UI.

## 🧯 Gateway mati setelah update — dan updater lama tidak bisa ambil fix ini

Bagian ini yang paling sering bikin orang panik di jam kerja. Rilis mencatat perbaikan untuk update yang terputus di tengah jalan: dulu hasilnya **Gateway berhenti dan tidak menyala lagi**, padahal pengecekan recovery mengizinkan restart. Sekarang, kalau maintenance selesai tapi Gateway tidak bisa dipastikan hidup, repair memberi panduan start manual beserta status. Satu kalimat penting dari dokumentasi: *Gateway yang berhasil dipulihkan bukan berarti update-nya selesai.*

Masalah kedua: backup besar gagal karena semua file berbagi **satu deadline penemuan SQLite**. Di storage lambat, satu file yang timeout ikut memblokir seluruh backup. Sekarang pemeriksaan dipecah ke batch lebih kecil dan diulang.

Dan ini poin yang paling mudah terlewat: kalau update kamu dari **2026.10.10** atau **2026.11.1** terblokir timeout tersebut, **memilih versi lebih baru tidak menolong** — updater yang sudah terpasang tidak bisa mengambil perbaikan ini dengan cara itu. Jalur yang benar adalah panduan update recovery resmi, atau memasang updater yang sudah dikoreksi lebih dulu.

## ✅ Checklist lima langkah sebelum `openclaw update`

- **Backup dulu, dan pastikan backup-nya terverifikasi.** Dokumentasi OpenClaw tegas: salinan config otomatis dan file recovery migrasi **bukan** backup full-state.
- **Cek versi asalmu.** Kalau kamu di 2026.10.10 atau 2026.11.1, baca bagian update recovery sebelum menekan update.
- **Audit pin TLS.** Cari entry fingerprint/pin yang kosong di konfigurasi node dan worker. Kosong bukan berarti "default aman" — di versi lama itu berarti verifikasi mati.
- **Setelah update, jangan cuma lihat "success".** Jalankan Doctor, cek Gateway benar-benar hidup, lalu kirim satu pesan uji ke channel yang biasa kamu pakai (Telegram, Discord, atau webhook) untuk memastikan balasan tetap sampai.
- **Kalau update gagal: jangan pindah ke versi lebih baru sebagai solusi.** Simpan artefak recovery, ikuti panduan, baru ulangi.

## 🐷 Kenapa "nol fitur" justru rilis yang penting

Agent jarang gagal karena modelnya kurang pintar. Agent gagal karena sertifikat yang tidak diperiksa, perintah yang lolos tanpa izin, kredensial yang ikut tercetak di log, atau update yang berhenti di tengah lalu meninggalkan Gateway mati. Semua itu tidak menghasilkan pesan error yang dramatis — hasilnya cuma satu: bot diam, dan kamu baru sadar berjam-jam kemudian ketika ada pelanggan bertanya.

Kalau kamu memakai agent untuk jualan, panel, atau CS, satu jam agent mati itu biaya nyata. Menariknya, di komunitas self-hosted ada hitungan informal bahwa belasan ribu instance OpenClaw terbuka ke internet — angka diskusi, bukan audit resmi, tapi arahnya jelas: banyak pemasangan tidak pernah meninjau ulang setelan keamanannya setelah sekali pasang.

Jadi untuk rilis ini, pertanyaannya bukan "ada fitur baru apa", tapi "sudahkah saya update, dan sudahkah saya cek ulang apa yang selama ini saya anggap aman". Dua menit membaca changelog lebih murah daripada satu pagi menjelaskan ke pelanggan kenapa bot tidak menjawab.

Kamu sudah di versi berapa sekarang — dan pin TLS di config-mu kosong atau terisi? Tulis di komentar, atau baca dua catatan lama saya soal [update recovery OpenClaw](/posts/openclaw-update-recovery-sep-2026/) dan [sinkronisasi SQLite yang bikin backup ngadat](/posts/openclaw-sqlite-sync-db-async/). Yang baru di dunia agent, bisa mulai dari [katalog plugin Hermes v0.23.1](/posts/hermes-agent-v0231-plugin-catalog-2mb-gagal-senyap/).

**Sumber:** [rilis v2026.11.3](https://docs.openclaw.ai/releases/2026.11.3), [panduan updating & recovery](https://docs.openclaw.ai/install/updating), PR [#190002](https://github.com/openclaw/openclaw/pull/190002) (pin TLS worker), PR [#187884](https://github.com/openclaw/openclaw/pull/187884) (approval exec), [changelog 2026.11.3](https://raw.githubusercontent.com/openclaw/openclaw/main/CHANGELOG/2026.11.3.md).

— Chokdi 🐷 · Content Studio · 2026
