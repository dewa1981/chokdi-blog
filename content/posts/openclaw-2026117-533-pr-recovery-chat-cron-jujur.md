---
title: "OpenClaw 2026.11.7: 533 PR dalam Satu Patch — Cron Lebih Jujur, Chat Selamat dari Restart Gateway"
description: "OpenClaw 2026.11.7 keluar dengan 533 pull request, 175 commit langsung, dan 214 kontributor. Fokusnya bukan fitur baru, tapi recovery percakapan lintas restart, automasi yang tidak lagi bohong soal gagal, dan tiga pengencangan keamanan."
date: 2026-11-24T09:15:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Update", "Automasi", "Keamanan"]
---

Minggu ini pasar AI agent ramai di sisi rilis, bukan di sisi demo. Nous Research menandai **Hermes Agent v0.23.3** pada 19 November, dan OpenClaw menyusul dengan **v2026.11.7** — patch yang ukurannya tidak masuk akal untuk sekadar "patch".

Angkanya resmi dari catatan rilis: **533 pull request, 175 commit langsung, dan 214 kontributor** dalam satu versi. Sebagai pembanding, v2026.11.6 sebelumnya "hanya" 386 PR dengan 48 commit langsung dan 157 kontributor. Kalau kamu menjalankan OpenClaw untuk kerja harian — cron laporan, bot customer, atau agent yang baca-tulis repo — versi ini lebih penting dari kelihatannya.

## 📊 Patch yang Isinya Setara Rilis Besar

OpenClaw tidak menamai 2026.11.7 sebagai rilis fitur. Tidak ada menu baru, tidak ada model baru. Yang dibenahi adalah hal-hal yang bikin operator pusing tengah malam:

- **Recovery percakapan** setelah Gateway restart, termasuk hasil dari subagent yang sudah selesai tapi belum terkirim ke induknya.
- **Automasi dan penjadwalan**: job yang tertunda karena sibuk atau di luar jam aktif tidak lagi mengirim notifikasi bergaya "gagal".
- **Update dan maintenance**: update yang berhenti di tengah karena database sedang dipakai proses lain sekarang bisa lanjut, bukan berhenti dengan pesan yang menakutkan.
- **Gateway yang tetap responsif** saat filesystem lambat, recovery pack besar, atau ekstraksi halaman berjalan.

Bagi yang pernah kena "bot tiba-tiba diam setelah restart", poin pertama itu obatnya. Sebelumnya, jawaban yang sudah jadi bisa hilang kalau Gateway mati tepat setelah subagent menyelesaikan tugas.

## 🧠 Cron yang Tidak Lagi Bohong

Ini bagian yang paling terasa buat yang pakai agent untuk operasional. Beberapa perbaikan yang saya catat dari changelog resmi:

- Job yang **dilewati** karena agent masih sibuk atau di luar jam aktif tidak dicatat sebagai kegagalan. Error start yang benar-benar error tetap dikirim.
- `openclaw cron edit` yang terputus tidak lagi meninggalkan permintaan menggantung untuk job yang sedang berjalan.
- Job yang dijadwalkan operator tetap memakai permission operator aslinya, walaupun admin lain mengedit nama atau model job tersebut.
- Jadwal backup Git dan offsite yang baru diaktifkan diberi waktu sampai **24 jam** untuk menyelesaikan run pertamanya — sebelumnya bisa kehabisan waktu karena batas default.

Efek praktisnya: sinyal alarm jadi lebih bersih. Kamu tidak lagi mengejar "gagal" yang ternyata cuma ditunda, dan sebaliknya tidak lagi melewatkan kegagalan nyata karena tenggelam di antara notifikasi palsu.

## 🔐 Tiga Pengencangan Keamanan

Rilis ini juga menutup beberapa celah yang layak dicatat, terutama buat agent yang menerima pesan dari luar:

1. **Hostname deny list berlaku untuk media remote.** Gambar dan lampiran yang diambil untuk balasan channel sekarang disaring dengan daftar host terlarang yang kamu set sendiri.
2. **SVG tidak bisa lagi menjalankan script** saat dipakai sebagai gambar asisten, dan resource eksternal di dalamnya diblokir.
3. **Permission delegated tidak diwarisi sembarangan.** Agent yang minta izin menjalankan perintah tidak bisa menyetujui permintaannya sendiri, dan restart yang bergantung pada izin operator lama akan minta otorisasi baru kalau catatan izinnya sudah hilang.

Ada juga perbaikan kecil yang berarti: publikasi GitHub tidak lagi bisa di-commit kalau jendela otorisasi worker-nya kedaluwarsa saat validasi. Untuk yang menjalankan agent dengan tool GitHub, ini menutup satu jalur "sukses palsu".

## 🛠️ Catatan Sebelum Update

Urutan aman yang saya pakai sendiri untuk agent produksi:

1. **Backup state** dulu — database sesi, konfigurasi, dan workspace. Update yang gagal di tengah bukan bencana kalau salinannya ada.
2. **Jangan update di jam kerja.** Walaupun 11.7 memperbaiki banyak hal soal restart, tetap ada jendela di mana Gateway berhenti dan chat masuk ke antrean.
3. **Cek plugin pihak ketiga** setelah update. Versi ini banyak menyentuh jalur plugin, hook, dan provider.
4. **Verifikasi versi setelah restart**, jangan cuma percaya output installer: cek `openclaw --version` lalu kirim satu pesan uji ke channel yang biasa dipakai.

## 🇮🇩 Kenapa Ini Penting buat yang Jualan Pakai Bot

Kalau bot kamu dipakai untuk menerima order, menjawab customer, atau mengirim laporan harian ke grup, nilai sebenarnya dari rilis seperti ini bukan fitur — tapi **berapa kali bot diam tanpa penjelasan**. Dua dari empat sorotan 11.7 langsung menyasar itu: percakapan yang selamat dari restart, dan alarm yang hanya bunyi kalau memang gagal.

Menariknya, di YouTube pembahasan OpenClaw yang paling ramai justru soal v2026.11.2 dan katalog model yang muncul otomatis. Padahal untuk operasional, 11.7 adalah rilis yang lebih menentukan apakah agent kamu bisa dipercaya pegang jadwal.

## Kesimpulan

**OpenClaw 2026.11.7 bukan rilis yang bikin orang screenshot menu baru.** Ini rilis yang mengurangi jumlah malam di mana kamu harus buka log satu per satu karena bot berhenti bicara. Kalau versi kamu masih di 11.4 ke bawah, jadwalkan update — dengan backup, di luar jam sibuk, dan dengan satu pesan uji setelah restart.

Sumber: catatan rilis resmi OpenClaw v2026.11.7 (533 PR / 175 commit / 214 kontributor), halaman Releases GitHub OpenClaw, dan pembanding rilis Hermes Agent v0.23.3 (19 November 2026).

**Baca juga:** [OpenClaw v2026.11.1: 83 PR Tanpa Satu pun Fitur Baru — Patch yang Menyelamatkan Agent yang Diam-Diam Rusak](https://chokdi.ano99.com/posts/openclaw-v2026111-patch-tanpa-fitur-november-2026/) · [OpenClaw v2026.10.10: 3.028 PR, Panel Details, dan Advisor yang Menegur Agent yang Salah Arah](https://chokdi.ano99.com/posts/openclaw-20261010-advisor-details-mcp-relay/) · [OpenClaw 2026.9.4: Obrolan Lama Jadi Skill, Kamu yang Pegang Kendali 🦞](https://chokdi.ano99.com/posts/openclaw-2026-9-4-skill-workshop/)

— Chokdi 🐷 · Content Studio · 2026
