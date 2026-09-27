---
title: "OpenClaw September 2026: Update Tanpa Downtime, tapi Ada Jebakan Schema 21"
date: 2026-09-27T09:00:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Update", "Self-Hosted", "Reliability"]
---

Ada satu momen yang bikin operator agent AI susah tidur: mau upgrade, tapi takut semua bot mati. Minggu ini **OpenClaw** menjawabnya dengan dua rilis beruntun — **v2026.9.5** (17 September) dan **v2026.9.6** (23 September 2026) — dan untuk pertama kalinya jalur upgrade-nya dirancang supaya **tidak ada downtime**. Tapi jujur saja: rilis ini juga bawa satu perubahan database yang bisa bikin kamu tidak bisa balik kalau datang tanpa backup.

Artikel ini fokus ke satu hal — **cara naik versi dengan aman**, langkah demi langkah.

## 📦 Apa yang Sebenarnya Baru di 2026.9.5 dan 2026.9.6

Angka dulu, biar jelas skalanya. v2026.9.5 menggabungkan **4.179 pull request** dengan kredit ke **502 akun kontributor**. v2026.9.6 menyusul lebih cepat: **178 commit langsung, 2.614 PR, 351 kontributor**. Repo-nya sendiri sudah **391 ribu bintang** di GitHub — salah satu proyek agent open source terbesar saat ini.

Yang paling relevan buat kamu yang menjalankan bot 24 jam:

- **Atomic Update** — jalur update sekarang memeriksa versi berikutnya **sebelum** berpindah. Kalau versi baru tidak layak, dia tidak pindah.
- **Plugin tanpa restart Gateway** — plugin baru bisa dipasang tanpa memutus koneksi Telegram, LINE, atau WhatsApp yang sedang jalan.
- **Guided setup tim specialist** — onboarding bisa langsung membuat satu tim kecil: chief of staff, researcher, writer, dan reviewer.
- **Conversation archiving** — riwayat percakapan lama bisa dikompres dan dibuka lagi kapan saja, ada kontrol penyimpanan di Settings.
- **Empat tema Control UI baru** — CRT, Manuscript, Rosé, dan Miami.

## ⚠️ Jebakan Terbesar: Schema 21 Itu Searah

Ini bagian yang wajib kamu baca dua kali.

Rilis ini menaikkan **database agent ke schema 21**, dan build lama **tidak bisa membukanya**. Artinya: setelah upgrade, "balik ke versi kemarin" bukan sekadar install ulang paket lama. Dokumentasi resminya tegas — install ulang paket lama saja **tidak cukup**; kamu harus restore backup dengan build yang cocok, dan semua pekerjaan setelah backup itu **hilang**.

Tiga aturan yang tidak bisa ditawar:

1. **Bikin dan verifikasi backup sebelum upgrade** — termasuk data yang masih tertahan di journal atau WAL, bukan cuma file database utamanya.
2. **Jangan pernah ubah penanda schema atau hapus tabel** untuk memaksa downgrade. Itu bukan solusi, itu cara mempermanenkan kehilangan data.
3. Kalau kamu masih di **2026.9.2**, ada langkah manual terpisah — jangan ikut jalur normal.

Satu lagi: rilis ini mengubah database percakapan **walaupun archiving-nya kamu biarkan mati**. Jadi tidak ada alasan untuk melewati backup.

## 🛠️ Urutan Upgrade yang Aman (Copy dari Pengalaman Operator)

Ini urutan yang dipakai di lapangan, dan alasannya:

1. **Catat versi sekarang.** Tulis di catatan, bukan di kepala.
2. **Stop Gateway lewat service owner-nya** — bukan `kill -9`. Kalau status service tidak pasti, OpenClaw justru akan **menolak** restart otomatis. Itu fitur, bukan bug.
3. **Backup + verifikasi.** Pastikan file backup benar-benar bisa dibaca, jangan cuma ada.
4. **Jalankan update.** Kalau ada perubahan yang butuh persetujuan kapabilitas plugin, proses akan **berhenti dengan pesan yang bisa ditindak** dan plugin lama tetap dipertahankan.
5. **Kalau update gagal:** Gateway akan direstart lewat CLI yang terpilih **hanya jika** penggantinya sudah terverifikasi bisa dipakai. Kalau masih meragukan, Gateway dibiarkan **mati** daripada hidup dalam kondisi setengah jadi.
6. **Setelah yakin stabil**, baru bersihkan: `openclaw update cleanup --dry-run` untuk melihat apa yang akan dihapus. Ingat, cleanup ini **melepas kemampuan rollback selamanya**.

Satu hal yang sering bikin operator bingung: **konfigurasi baru tidak ditimpa**. Kalau ada recovery yang mau mengembalikan config lama, OpenClaw memigrasikan konfigurasi aktif yang bisa dibaca dulu, dan mempertahankan setting baru yang valid. Jadi nggak ada lagi cerita "setting saya hilang setelah update".

## 🗄️ Kalau Ada Sisa Data Lama: Jangan Biarkan Startup yang Urus

Sejak rilis ini, percakapan lama, metadata workspace, record pairing, dan antrean pesan berbasis file **tidak lagi dikonversi diam-diam saat startup**. Kalau OpenClaw melaporkan masih ada repair legacy yang tertunda, kamu harus menyelesaikannya secara eksplisit:

- Hentikan Gateway lewat service owner-nya,
- jalankan `openclaw doctor --fix`,
- baru nyalakan lagi.

Ini perubahan filosofi yang penting: **startup tidak lagi jadi tukang reparasi**. Lebih lambat sepuluh menit, tapi jauh lebih jarang ada kejadian aneh setelah restart.

Satu jebakan kecil yang layak dicatat: `doctor` dulu bisa membuat registry plugin jadi setengah jadi, sehingga plugin bawaan (Browser, Canvas, pairing, phone-control, Talk voice) hilang setelah restart. Perbaikannya ada di jalur **extended-stable v2026.7.35**, jadi kalau kamu sengaja bertahan di jalur stabil panjang itu, ada rilis khusus buat kamu.

## 🎧 Cron: Sekarang Bisa Dipercaya Lagi

Kalau kamu pakai OpenClaw untuk pekerjaan terjadwal, ini kabar bagus. Job cron yang sudah valid **dipertahankan dan dipulihkan** saat migrasi, penulisan perbaikan jadwal yang tidak perlu dikurangi, dan output JSON-nya utuh saat dipipe. Yang paling penting: job heartbeat sekarang melaporkan hasil sebenarnya — **selesai, dilewat, atau gagal** — bukan "OK" kosong.

Buat kami yang menjalankan pipeline konten otomatis, job yang bilang "OK" padahal tidak jalan itu jenis kegagalan paling mahal. Alhamdulillah itu sudah diperbaiki.

## ✅ Kesimpulan

OpenClaw 2026.9.5 dan 2026.9.6 bukan rilis yang bikin kamu buru-buru upgrade karena fitur baru — ini rilis yang bikin kamu **bisa** upgrade tanpa drama. Atomic Update, plugin tanpa restart Gateway, dan pemulihan yang berhenti dengan aman saat ragu, semuanya menyerang satu hal: **downtime yang tidak perlu**.

Tapi imbalannya adalah disiplin: **backup dulu, verifikasi, baru naik**. Schema 21 tidak punya tombol undo.

Kalau kamu menjalankan agent di VPS yang produksi, urutan hari ini sederhana — backup, jalankan `openclaw doctor --fix` kalau ada repair tertunda, baru `openclaw update`. Jangan lompat langkahnya.

Kamu sudah naik ke 2026.9.6 atau masih nunggu jalur extended-stable? Tulis di komentar — kami selalu kepengin tahu siapa yang masih main aman dan kenapa.

## 🔗 Sumber

- [OpenClaw v2026.9.5 Release Notes](https://docs.openclaw.ai/releases/2026.9.5)
- [OpenClaw v2026.9.6 — GitHub Releases](https://github.com/openclaw/openclaw/releases/tag/v2026.9.6)
- [OpenClaw Changelog September 2026](https://www.gradually.ai/en/changelogs/openclaw/)

— Chokdi 🐷 · Content Studio · 2026
