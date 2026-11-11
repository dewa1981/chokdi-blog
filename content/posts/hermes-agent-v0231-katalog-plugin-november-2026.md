---
title: "Hermes Agent v0.23.1: Patch Kecil yang Menyelamatkan Plugin Install Kamu"
date: 2026-11-11T09:20:00+07:00
draft: false
tags: ["Hermes Agent", "Update", "Plugin", "Self-Host", "AI Agent"]
---

Ada rilis yang heboh, ada rilis yang kelihatan sepele tapi justru menyelamatkan kerjaan harian. **Hermes Agent v0.23.1** masuk kategori kedua. Dirilis 9 November 2026 (tag publik 10 November), patch ini tidak menambah menu baru yang bisa dipamerkan — dia memperbaiki satu bug yang bikin `hermes plugins install` gagal **tanpa error apa pun**.

Kalau kamu pernah feeling "kok plugin yang baru rilis nggak ketemu ya?", artikel ini buat kamu.

## 🐛 Bug-nya: katalog plugin diam-diam dipakai versi lama

Sejak situs katalog plugin deploy 9 November, file `plugin-catalog.json` yang dipublikasikan membengkak melewati batas 2 MiB yang diterima client. Efeknya bukan crash, bukan warning — client **diam-diam fallback** ke katalog yang ikut di installer kamu.

Tiga gejala yang muncul di permukaan:

- `hermes plugins install <nama>` tidak menemukan plugin yang ditambahkan setelah update terakhirmu.
- Yang terpasang justru versi yang di-pin di rilis kamu, bukan versi terkini.
- Entri `removed` yang baru tidak terbaca, jadi plugin yang sudah dicabut masih terlihat "aman".

Fix-nya sederhana dan masuk akal: batas dinaikkan dari 2 MiB ke **16 MiB**, jadi katalog live dipakai lagi (PR #151860, menutup issue #151856, kontribusi @100yenadmin). Catatan penting: **selama kamu masih di v0.23.0 atau lebih lama, fallback itu tetap terjadi.** Update adalah satu-satunya jalan keluar.

## 📊 Skala di balik "patch kecil"

Jangan tertipu label patch. Diukur di commit `3b421578588`, jendela sejak v0.23.0 berisi:

- **2.578 non-merge commit** di **2.781 file** berubah
- **+151.690 / −62.595** baris
- **618 pull request** merged dan **409 issue** ditutup

Artinya v0.23.1 adalah cara tim Nous "membekukan" kerja tiga minggu terakhir supaya aman dipakai, sementara catatan kurasi lengkapnya menyusul di v0.24.0. Jadi kalau kamu buka changelog dan merasa kurang lengkap — memang sengaja.

## 🧰 Fitur yang ikut "nyelip" di rilis ini

Beberapa hal tidak ditulis panjang di notes, tapi sudah ada di build:

- **Esc untuk backtrack** di TUI dan CLI klasik (menggantikan picker daftar rewind).
- **Group chat tanpa Desktop**: gateway bisa menjalankan group chat dan menampung bot dari komputer lain.
- **Koneksi gateway tersimpan** yang dipakai bersama oleh Desktop dan Webapp.
- **In-app browser** bisa login pakai profil browser asli kamu, plus isi kredensial tersimpan dari address bar.
- `hermes gateway attach` untuk client lokal, dan `hermes clipboard image --json` untuk pipeline gambar.
- **Plugin API baru**: nilai environment per-session, method/event JSON-RPC plugin, task bantu `llm.oneshot`, `conversation_id` yang stabil saat kompresi, hook `on_session_open`, dan hook `post_curator_run`.

Bagi yang suka otomasi, dua hook terakhir itu bernilai bisnis: kamu bisa memicu skrip sendiri tepat saat session dibuka atau setelah kurator skill selesai jalan — tanpa polling.

## ⚙️ Cara update (pilih sesuai cara install)

- **CLI**: jalankan `hermes update`, atau ulangi one-liner installer.
- **Docker / Hermes Cloud**: pakai tag `nousresearch/hermes-agent:stable` (atau `:latest`).
- **Microsoft Store app**: update lewat Store seperti biasa.
- **Desktop dari installer (.exe/.dmg)**: tidak berubah di rilis ini, ikut bundel berikutnya.

Sebelum update, biasakan tiga hal ini — murah, tapi sering menyelamatkan: backup `~/.hermes` (config, profile, skill), catat versi sekarang (`hermes --version`), dan pastikan gateway bisa di-restart tanpa kehilangan session. Setelah update, cek plugin yang kamu pakai masih ke-load, lalu baru nyalakan cron.

## 🎯 Kenapa ini relevan buat pengguna agent di Indonesia

Mayoritas dari kita menjalankan agent di VPS kecil, model murah, dan koneksi seadanya. Di setup seperti itu, kegagalan senyap adalah musuh terbesar: plugin tidak terpasang, kamu kira sudah terpasang, lalu heran kok agent "bodoh" padahal skill-nya belum ada. Bug katalog 2 MiB itu persis jenis kegagalan yang bikin waktu habis buat debug yang salah arah.

Kalau kamu masih rajin ikut tutorial video (misalnya panduan setup Hermes Agent untuk pemula di YouTube), perhatikan satu hal: tutorial biasanya mengajarkan install, jarang mengajarkan **verifikasi setelah update**. Tambahkan sendiri langkah cek katalog dan daftar plugin setiap kali habis update — 30 detik, hemat berjam-jam.

## 🧭 Kesimpulan

v0.23.1 bukan rilis untuk pamer. Dia rilis untuk memastikan yang sudah kamu pasang benar-benar bekerja: katalog plugin kembali live, bug kegagalan senyap hilang, dan sebagian fitur besar sudah mendarat lebih awal. Update sekarang, verifikasi plugin, dan tunggu catatan lengkap di v0.24.0.

Sumber: [GitHub Releases Hermes Agent v0.23.1](https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.1) · [Dokumentasi Hermes Agent](https://hermes-agent.nousresearch.com/docs/) · [OpenClaw v2026.11.2 release notes](https://docs.openclaw.ai/releases) sebagai pembanding ritme rilis agent open source.

— Chokdi 🐷 · Content Studio · 2026
