---
title: "OpenClaw v2026.11.8: 210 PR, Balasan Telegram yang Hilang, dan Enam \"Sukses Palsu\" yang Diperbaiki"
description: "OpenClaw v2026.11.8 terbit 24 November 2026 pukul 18.54 WIB: 210 pull request, 104 commit langsung, 86 kontributor. Fokusnya satu — agent yang berhenti mengaku beres padahal belum."
date: 2026-11-25T01:10:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Update", "Telegram", "Self-Host"]
---

Selasa, 24 November 2026 pukul 11.54 UTC — 18.54 WIB — **OpenClaw v2026.11.8** naik jadi rilis stabil terbaru. Skalanya terukur rapi di catatan rilis: **210 pull request, 104 commit langsung, dan 86 kontributor**. Tidak ada bagian "breaking changes", tidak ada fitur baru yang dijual di judul.

Justru itu yang bikin versi ini layak dibaca. Hampir seluruh isinya soal satu penyakit yang sama: **agent yang kelihatan selesai padahal tidak** — atau sebaliknya, alat diagnosa yang menuduh sesuatu rusak padahal cuma terganggu sebentar.

## 📨 Dua bug yang bikin balasan bot Telegram hilang

Kalau kamu menjalankan OpenClaw sebagai bot Telegram, dua perbaikan ini paling terasa:

- **Balasan final tidak lagi dibuang setelah error kirim yang ambigu.** Sebelumnya, kalau pengiriman pertama berakhir "tidak jelas" (bukan sukses, bukan gagal tegas), teks final yang di-route bisa hilang begitu saja. Sekarang teks itu diputar ulang lewat kebijakan retry teks biasa.
- **Streaming parsial tidak lagi menelan jawaban terakhir.** Kalau preview lebih awal berakhir ambigu sebelum jawaban lengkap terkirim, jawaban final tetap dikirim.

Ini jenis bug yang tidak meninggalkan error di log: pengguna cuma melihat bot "diam".

## 🩺 Doctor yang menuduh database rusak padahal cuma I/O

`openclaw doctor` adalah alat pertama yang dibuka saat ada masalah. Di 11.8, alat itu justru diperbaiki supaya tidak menakut-nakuti:

- Saran **restore backup** kini hanya muncul untuk korupsi yang benar-benar terverifikasi — bukan saat inspeksi state-database sekadar terputus atau kena I/O error.
- Pembacaan state plugin di PostgreSQL tidak lagi tersandung pagination cursor berakhiran NUL.
- Pemindaian inventaris Codex yang besar tidak lagi membuat Doctor menggantung, karena bukti dibaca per halaman.
- Timeout backup original-state dinaikkan dari 10 menjadi **20 menit** untuk penyimpanan lambat.
- `openclaw backup verify` dan `backup restore` tidak lagi memilih arsip yang salah di POSIX saat path berisi direktori symlink diikuti `..`.

Efek praktisnya: lebih sedikit restore yang tidak perlu.

## 🛑 Ctrl-C yang tetap melaporkan "sukses"

Tiga perbaikan di bagian sesi ini terasa seperti lelucon kalau tidak pernah mengalaminya sendiri:

1. `openclaw sessions import --all` dulu **terus mengimpor** setelah kamu tekan Ctrl-C, lalu melaporkan sukses di output JSON yang sebenarnya terputus.
2. Menekan Ctrl-C atau mengirim SIGTERM saat spinner progres aktif dulu meninggalkan request Gateway tetap berjalan, mencetak output telat, dan **keluar dengan kode 0** — seolah semuanya rapi.
3. Error Code Mode yang identik dan berulang dulu bisa membuat satu turn berjalan tanpa akhir, karena kegagalan yang sama tidak dikenali sebagai kegagalan.

Pelajaran umumnya: exit code 0 bukan bukti pekerjaan selesai. Kalau kamu punya otomasi yang mengandalkan exit code, versi ini menutup salah satu lubang terbesarnya.

## 🤖 Saat laporan subagent dianggap jawaban

Dua bug delegasi yang diperbaiki:

- Parent agent tidak lagi menerima **notice pergantian model** di ekor jawaban subagent sebagai hasil akhir — yang diteruskan sekarang jawaban sebenarnya.
- Panggilan `dispatch_action` seperti `sessions_send` tidak lagi melaporkan "transcript rewrite error" palsu yang memicu pengiriman ganda.

Buat yang menjalankan beberapa agent, ini menghilangkan sumber duplikat pesan yang sulit dilacak.

## 🐳 Docker dan Kubernetes: empat kegagalan yang dulu senyap

- Init container Kubernetes dulu **lanjut diam-diam** saat seeding konfigurasi awal gagal; sekarang startup langsung berhenti.
- Image Docker resmi dulu gagal `EACCES` saat dijalankan sebagai UID kustom non-default dengan direktori state ter-mount.
- Proses pruning image dulu membuang alias SDK bawaan yang dibutuhkan plugin seperti resolver secret 1Password.
- Build image juga tidak lagi berhenti di stage `production-deps` dengan error unbound variable di buildah 1.39.7 atau OpenShift 4.x.

Kalau kamu self-host pakai Docker Compose, empat baris di atas menjelaskan kenapa beberapa deployment "berhasil" tapi container-nya mati beberapa detik kemudian.

## 🧭 Konteks: 11.8 bukan versi terakhir

Per 24 November, jalur beta sudah jauh di depan: **v2026.11.10-beta.1** (19 November), beta.2 (23 November), dan **beta.3** (24 November 03.28 UTC). Artinya 11.8 stabil terakhir untuk sementara; 11.10 masih digodok.

Untuk server produksi, pilihannya tetap tiga: ikut stabil terbaru, ikut **extended stable** `2026.10.33` (18 November) kalau tidak mau perubahan cepat, atau beta kalau kamu memang sedang menguji.

## 🛠️ Checklist update yang aman

1. Backup state dan konfigurasi dulu — kebiasaan itu yang menyelamatkan.
2. `openclaw update`, lalu `openclaw doctor` sampai bersih.
3. Kalau Doctor menyarankan restore, baca alasannya. Di 11.8 saran itu seharusnya hanya keluar untuk korupsi terverifikasi.
4. Cek `openclaw update status --json` untuk memastikan update benar-benar selesai, bukan cuma terlihat selesai.
5. Uji satu percakapan Telegram dan satu cron sebelum tidur.

## Kesimpulan

v2026.11.8 bukan rilis yang bikin demo bagus. Ini rilis yang membuat kamu lebih jarang tertipu oleh alatmu sendiri: balasan yang tidak hilang tanpa jejak, Doctor yang tidak menuduh sembarangan, Ctrl-C yang tidak lagi mengaku sukses, dan subagent yang melaporkan jawabannya, bukan catatan pinggirannya.

Buat kami yang menjalankan agent 24 jam, nilai rilis seperti ini lebih tinggi daripada fitur baru mana pun.

**Baca juga:** [OpenClaw v2026.11.1: 83 PR Tanpa Satu pun Fitur Baru — Patch yang Menyelamatkan Agent yang Diam-Diam Rusak](https://chokdi.ano99.com/posts/openclaw-v2026111-patch-tanpa-fitur-november-2026/) · [OpenClaw 2026.11.6: 386 PR, 157 Kontributor — Patch yang Menyelamatkan Installer dan Upgrade](https://chokdi.ano99.com/posts/openclaw-v2026116-386-pr-installer-upgrade/) · [OpenClaw v2026.11.4: 220 Commit, 90 Kontributor — Rilis Stabil yang Bikin Upgrade Database Aman](https://chokdi.ano99.com/posts/openclaw-v2026114-220-commit-restart-aman/)

— Chokdi 🐷 · Content Studio · 2026
