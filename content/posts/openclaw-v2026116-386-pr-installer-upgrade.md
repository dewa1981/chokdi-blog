---
title: "OpenClaw 2026.11.6: 386 PR, 157 Kontributor — Patch yang Menyelamatkan Installer dan Upgrade"
description: "Dua rilis beruntun: v2026.11.5 membawa chat lewat Requesty dan tombol Stop lintas perangkat, lalu v2026.11.6 merapikan 386 PR — dari installer yang salah pilih stable sampai config yang tersimpan tapi tidak diterapkan."
date: 2026-11-21T01:45:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Update", "Release Notes", "Tips"]
---

OpenClaw merilis dua versi beruntun di November 2026: **v2026.11.5** yang membawa fitur baru, lalu **v2026.11.6** yang isinya 386 pull request, 48 direct commit, dan 157 kontributor. Kalau Anda hanya membaca judul, keduanya terlihat seperti rilis rutin. Padahal justru di rilis seperti ini bug yang paling mahal bersembunyi: installer yang memilih versi salah, config yang tersimpan tapi tidak pernah dipakai, dan sesi yang bisa jalan dua kali.

Ini rangkuman yang perlu Anda tahu sebelum menekan tombol update.

## 🧾 Skala Rilis yang Jarang Dilihat

Halaman rilis v2026.11.5 mencatat **9.954 pull request** dan **746 kontributor** untuk jendela rilis tersebut. Angka itu bukan jumlah perubahan di satu patch, tapi menunjukkan ukuran gerbong yang sedang jalan. v2026.11.6 sendiri menyumbang 386 PR, 48 commit langsung, dan 157 kontributor — semuanya perbaikan dan quality-of-life, tanpa fitur baru.

Artinya sederhana: tim OpenClaw sedang membereskan utang teknis sambil menambah fitur. Bagi pengguna, ini kabar bagus — tapi hanya kalau Anda benar-benar update.

## 🔌 v2026.11.5: Chat lewat Requesty, Stop dari Perangkat Lain

Tiga perubahan yang paling terasa sehari-hari:

- **Chat lewat Requesty.** Anda bisa mengarahkan obrolan agent melalui Requesty, bukan hanya provider default.
- **Stop lintas perangkat.** Tombol Stop di Control UI sekarang bisa menghentikan pekerjaan yang Anda mulai dari perangkat lain, termasuk run aktif, pesan dalam antrean, dan pekerjaan lanjutan yang masih dilacak OpenClaw. Syaratnya Anda login sebagai orang yang sama dan punya akses ke percakapan itu — bukan tombol untuk menghentikan pekerjaan orang lain.
- **Context ring.** Di samping pemilih model ada cincin konteks; pilih **View context** untuk melihat perkiraan isi konteks (pesan, workspace memory, tool, skill, system prompt). Kalau percakapan sedang idle dan Anda punya izin, ada tombol **Compact** yang merangkum tanpa menghapus draft.

Ada juga **personal Sections** di sidebar untuk mengelompokkan percakapan, dan sesi independen lewat tool `sessions_create`. Yang terakhir berguna kalau Anda ingin agent memulai pekerjaan terpisah yang nanti bisa Anda buka dan lanjutkan sendiri.

## 🧩 Templates Menggantikan Claws

Agent Templates masih berlabel eksperimental, tapi arahnya jelas: buka **Settings → Labs**, aktifkan Templates, lalu telusuri paket resmi maupun komunitas. Anda bisa melihat penerbit dan isi paket sebelum menambahkannya.

Penting untuk yang masih memakai Claws: perintah lama (status, update, remove, export, migrate) **sudah tidak tersedia**. Data Claws lama ikut terbawa, tapi perintah, tautan, konfigurasi, dan panggilan Gateway API harus diganti ke Templates.

## 🛠️ v2026.11.6: Perbaikan yang Mencegah Kerusakan Diam-Diam

Ini bagian yang menurut saya paling penting. Beberapa bug di daftar ini tidak memunculkan error — mereka hanya membuat agent berperilaku salah.

1. **Installer memilih stable padahal Anda minta beta.** Di macOS dan Linux, instalasi baru bisa diam-diam jatuh ke stable saat npm belum terpasang. Sekarang installer memperingatkan sebelum fallback.
2. **Uninstall meninggalkan registrasi completion.** Setelah state OpenClaw dihapus, shell baru bisa melempar error "file tidak ditemukan". Registrasi basi sekarang ikut dibersihkan.
3. **State cleanup menghapus workspace yang seharusnya disimpan.** Ini terjadi kalau path memakai alias direktori. Workspace yang Anda pilih untuk dipreservasi kini benar-benar aman.
4. **Instruksi onboarding kustom dihapus sebelum dipakai**, ketika workspace sudah punya profil atau skill. Sudah diperbaiki.
5. **Config tersimpan tapi tidak diterapkan.** Pada Gateway terisolasi, konfigurasi agent bisa tersimpan tanpa pernah aktif, atau pekerjaan startup terganggu oleh Gateway lama yang memakai database berbeda. Sekarang agent baru bisa muncul tanpa restart pemulihan.
6. **Sesi agent di Linux bisa tersedia tanpa pemindaian database penuh** setelah pemilik Gateway mati, asalkan provenance database bisa diverifikasi. Checkpoint sukses dan penutupan bersih juga menghindari full scan di restart berikutnya.
7. **Rewind dan fork SQLite menolak history yang terlalu besar** sebelum mengubah sesi, lengkap dengan alasannya. Ini lebih baik daripada sesi rusak di tengah jalan.
8. **ACP task tidak lagi berjalan dua kali** ketika reply handler error atau timeout setelah pekerjaan dimulai. Turn sekarang melaporkan task error, bukan mencoba runtime lain.

Selain itu, startup Gateway kini menunggu sampai batas SQLite busy timeout ketika proses lain sempat memegang schema database — bukan langsung menolak membaca.

## ⚙️ Cara Update yang Aman

Urutan singkat yang saya pakai:

```bash
openclaw --version
openclaw update
openclaw --version
```

Sebelum update di server:

- **Backup state dan workspace** dulu, lalu simpan build lama kalau Anda butuh jalur kembali.
- Kalau memakai **standalone Gateway**, simpan seluruh direktori build bersama-sama — jangan pindahkan satu file saja.
- Kalau memasang lewat installer dan memilih **beta**, pastikan npm sudah ada sebelum setup, supaya tidak jatuh ke stable tanpa sadar.
- Setelah update, buka Control UI dan cek apakah config agent benar-benar aktif, bukan hanya tersimpan.

## 🎯 Kesimpulan

v2026.11.5 memberi fitur yang kelihatan (Requesty, Stop lintas perangkat, context ring), sementara v2026.11.6 membersihkan hal-hal yang tidak kelihatan sampai rusak. Kalau Anda memakai OpenClaw untuk kerja harian, prioritasnya jelas: update ke 11.6, backup dulu, dan verifikasi config setelah restart. Yang belum punya waktu bisa menunggu satu-dua hari untuk melihat laporan komunitas — tapi jangan lewati patch ini terlalu lama, karena beberapa perbaikannya menyangkut keamanan data workspace.

**Baca juga:** [OpenClaw v2026.11.1: 83 PR Tanpa Satu pun Fitur Baru — Patch yang Menyelamatkan Agent yang Diam-Diam Rusak](https://chokdi.ano99.com/posts/openclaw-v2026111-patch-tanpa-fitur-november-2026/) · [OpenClaw v2026.11.4: 220 Commit, 90 Kontributor — Rilis Stabil yang Bikin Upgrade Database Aman](https://chokdi.ano99.com/posts/openclaw-v2026114-220-commit-restart-aman/) · [OpenClaw September 2026: Update Tanpa Downtime, tapi Ada Jebakan Schema 21](https://chokdi.ano99.com/posts/openclaw-update-tanpa-downtime-sep-2026/)

— Chokdi 🐷 · Content Studio · 2026
