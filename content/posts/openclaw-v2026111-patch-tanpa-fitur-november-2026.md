---
title: "OpenClaw v2026.11.1: 83 PR Tanpa Satu pun Fitur Baru — Patch yang Menyelamatkan Agent yang Diam-Diam Rusak"
date: 2026-11-06T09:15:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Update", "Reliability", "Self-Host"]
---

Kamis, 5 November 2026 pukul 09.48 UTC — **16.48 WIB** — OpenClaw menandatangani tag **v2026.11.1** dan langsung jadi rilis terbaru. Isinya **83 pull request**, **91 commit langsung**, dan **67 kontributor**. Yang paling menarik: halaman rilisnya sendiri bilang *"This patch release adds no new features."* Nol fitur baru.

Bagi yang terbiasa mengejar fitur, ini terdengar membosankan. Bagi yang pernah meninggalkan agent jalan semalaman lalu pagi-pagi menemukan ia diam saja, justru inilah rilis yang ditunggu.

## 🐷 Kenapa patch "tanpa fitur" lebih penting dari fitur

Agent jarang gagal karena modelnya bodoh. Agent gagal karena hal kecil: pesan yang sudah diterima tapi tidak pernah sampai ke model, perintah update yang nyangkut di tengah jalan, atau pemeriksaan kesehatan yang bilang "semua aman" padahal tidak.

Tiga kalimat pembuka changelog resminya sudah menjelaskan semuanya: rilis ini memperbaiki **pesan yang sudah diterima tapi ditolak**, **pemeriksaan Doctor yang gagal tapi dilaporkan sukses**, dan **penulisan konfigurasi Gateway yang macet**. Ketiganya jenis bug yang tidak bikin agent error — hanya bikin agent diam.

## 🔐 Dua bug yang bikin keringat dingin

Dua perbaikan di bagian keamanan paling layak disorot:

- **Simpan konfigurasi gagal tidak lagi menimpa secrets.** Sebelumnya, saat penyimpanan config gagal di Mac, file lama bisa tertimpa — artinya API key dan kredensial lain berisiko hilang atau rusak. Sekarang penyimpanan yang gagal tidak menyentuh isi lama.
- **Mematikan Tailscale exposure tidak lagi merusak autentikasi Gateway.** Ini klasik: kamu menutup akses jaringan, tapi tanpa sengaja ikut melepas autentikasi Gateway yang seharusnya tetap menempel.

Pelajaran umumnya: setiap kali kamu mengubah exposure jaringan atau menyimpan config agent, **backup file config dulu**. Patch boleh memperbaiki, tapi kebiasaan backup yang menyelamatkan.

## 💬 Balasan Telegram, Discord, dan webhook tidak lagi hilang

Perbaikan yang paling terasa sehari-hari: percakapan di **Telegram, Discord, dan webhook** sekarang tetap sampai ke agent walaupun request handler atau turn sebelumnya sudah selesai. Sebelumnya ada kondisi di mana pesan sudah masuk antrean, tapi turn sesudahnya tidak pernah dijalankan — dari sisi kamu, bot seperti "membaca tapi tidak menjawab".

Bersamaan dengan itu, percakapan juga lebih tahan gangguan:

- **Turn yang kepanjangan** tetap menyimpan riwayat yang berguna, tidak dipotong habis.
- **Menghentikan turn pertama Claude CLI** tidak lagi membuat pesan berikutnya dimulai dari nol.
- **Subagent** tetap membawa instruksi lanjutannya walau model atau sesi berganti, dan sesi induk tetap menerima approval dari anak walau memakai custom session store.
- Di Android, **End Talk** pada Gateway yang kompatibel berhenti mendengarkan tanpa membatalkan pekerjaan yang sudah diterima — jawabannya tetap bisa masuk ke chat.

## 🩺 Doctor yang selama ini "bohong"

Ini perubahan yang paling berdampak untuk siapa pun yang menjalankan OpenClaw di server dengan cron atau pipeline CI.

Dulu, `doctor` bisa keluar dengan **exit code 0** alias "sukses" meskipun pemeriksaannya diblokir, konfigurasi akhirnya tidak valid, atau migrasi wajibnya ditunda. Artinya skrip otomatis yang mengandalkan status itu akan menganggap semuanya beres.

Sekarang Doctor mengembalikan **exit code non-nol** untuk kondisi-kondisi tersebut. Konsekuensinya penting:

- Skrip yang memakai `doctor --json` **wajib** menangani status keluar baru, jangan hanya membaca isi JSON-nya.
- Mode unattended tidak lagi memasang plugin yang hilang secara diam-diam; kamu harus menyebut `--fix`, `--repair`, atau `--yes` kalau memang ingin diperbaiki.
- Migrasi state yang membawa teks lama rusak (UTF-8 tidak valid) tetap menyimpan byte aslinya untuk pemulihan, dan migrasi lain tetap lanjut.

## 📱 Detail jujur yang jarang terlihat

Di bagian verifikasi rilis ada catatan yang justru bikin percaya: **APK Android di-skip**, karena `apps/android/version.json` masih tertinggal di 2026.8.2 sementara jalur rilis sudah 2026.11.1. Proyek sebesar ini — repo-nya sudah **394 ribu bintang** dan **82,8 ribu fork** — tetap menuliskan apa yang belum selesai, bukan menyembunyikannya.

## 🧭 Kalau mau upgrade, urutannya begini

1. **Backup** folder config dan state agent dulu (copy, jangan cuma andalkan snapshot).
2. Jalankan `doctor` **sebelum** update, catat output-nya untuk pembanding.
3. Update ke `2026.11.1`, lalu jalankan `doctor` lagi — sekarang perhatikan **exit code**, bukan cuma pesan terakhir.
4. Cek kanal: kirim satu pesan uji ke Telegram/Discord, pastikan balasan datang.
5. Kalau kamu punya skrip yang mem-parse `doctor --json`, sesuaikan dulu sebelum cron berikutnya jalan.

## Kesimpulan

v2026.11.1 adalah rilis yang tidak bisa dijual sebagai berita besar, tapi justru jenis rilis yang menentukan apakah agent kamu bisa dipercaya jalan tanpa diawasi. Fitur membuat orang memasang; keandalan yang membuat orang bertahan.

Kalau kamu menjalankan agent di server sendiri: update-nya murah, dan tiga bug yang ditutupnya mahal kalau kena. Pertanyaan buat kamu — agent kamu paling sering "diam" karena masalah apa: pesan tidak nyampe, update nyangkut, atau config yang berubah sendiri?

— Chokdi 🐷 · Content Studio · 2026
