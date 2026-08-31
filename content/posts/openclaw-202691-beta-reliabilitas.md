---
title: "OpenClaw 2026.9.1-beta.1: Rilisan September yang Fokus Bikin Agen Tidak Mogok Lagi"
date: 2026-09-01T00:15:00+07:00
draft: false
tags: ["AI", "OpenClaw", "Open Source", "Update"]
---

OpenClaw membuka seri September dengan **2026.9.1-beta.1** yang rilis pada **28 Agustus 2026** — dan jangan berharap fitur baru yang heboh. Rilisan ini justru fokus ke satu hal yang lebih penting: **reliabilitas**. Setelah Agustus diisi patch keamanan besar, kali ini tim OpenClaw membenahi bagian paling menyebalkan bagi pengguna — gateway yang restart mendadak, worker yang mati tanpa kabar, dan config yang gagal tersimpan.

## Gateway Restart Recovery: Tugas Tidak Hilang Lagi

Ini headline utama rilisan ini. Sebelumnya, kalau gateway OpenClaw restart di tengah jalan — entah karena update, crash, atau server di-reboot — tugas (turn) yang sedang berjalan sering kali lenyap begitu saja. Pengguna harus mengulang dari awal, dan kalau sudah jalan lama, rasanya menyakitkan.

Dengan **gateway restart recovery** (PR [#130491](https://github.com/openclaw/openclaw/pull/130491) oleh @jalehman), turn yang sudah "diterima" (admitted) dan aman untuk restart akan dipertahankan melewati cleanup dan restart berulang. Checkpoint tetap tersimpan, dan jawaban akhir tetap terkirim. Artinya: OpenClaw sekarang bisa restart di tengah pekerjaan panjang tanpa bikin pengguna mengulang kerjaan.

## Worker Recovery: Dead Turn Tidak Menggantung

Masalah klasik lain di sistem multi-worker: worker yang mati atau macet membuat tugas delegasi menggantung tanpa kepastian. Rilisan ini memperbaiki **worker admission recovery** (PR [#130446](https://github.com/openclaw/openclaw/pull/130446)) — launch yang gagal melewati admission deadline akan di-aktifkan ulang, dan turn worker yang mati di-terminalisasi secara resmi, bukan dibiarkan "zombie". Pekerjaan delegasi yang terputus sekarang selesai dengan status yang jelas.

## Config Write Lebih Aman

Pernah `config.patch` gagal tiba-tiba? Penyebabnya ada di **watcher handoff** — saat penulisan config terjadi bersamaan dengan reload. Perbaikan di PR [#131515](https://github.com/openclaw/openclaw/pull/131515) membuat penulisan config yang sudah di-commit tetap "pending" sampai watcher melihat generasi config yang benar, sehingga perubahan tidak hilang di tengah proses.

## Codex 0.150.1 dan Node 24 LTS

Dua peningkatan teknis yang patut dicatat:

- **Codex runtime** di-bump ke **0.150.1** di semua platform (Linux, macOS, Windows) — membawa protokol kolaborasi, status, dan aktivitas terbaru ke managed bridge (PR [#130685](https://github.com/openclaw/openclaw/pull/130685)).
- **Installer Linux** sekarang menyediakan **Node 24 LTS** yang stabil dan mengunci RPM install ke repository NodeSource, sehingga instalasi baru tidak lagi berisiko memilih prerelease yang tidak kompatibel (PR [#130369](https://github.com/openclaw/openclaw/pull/130369)).

## Sentuhan Kecil di Control UI dan Model

- **Appearance per profil** — preferensi tampilan kini disimpan per user profile, jadi browser bersama tidak memaksa semua orang memakai satu tema (PR [#130340](https://github.com/openclaw/openclaw/pull/130340)).
- **File safety** — penyimpanan file agen yang sudah dikonfirmasi tidak lagi rusak saat ada operasi baca/refresh yang tumpang tindih (PR [#130468](https://github.com/openclaw/openclaw/pull/130468)).
- **Model browsing** tetap tersedia setelah aktivasi plugin otomatis, katalog provider tidak hilang (PR [#130481](https://github.com/openclaw/openclaw/pull/130481)).
- **Model selection scopes** — scope pemilihan model kini bisa dikonfigurasi (PR [#127813](https://github.com/openclaw/openclaw/pull/127813)).
- **Audit decisions** dicatat di batas eksekusi resmi untuk diagnostik operator yang lebih jelas (PR [#130358](https://github.com/openclaw/openclaw/pull/130358)).

## Perlu Update atau Tunggu?

Karena ini masih **beta** (`2026.9.1-beta.1`), kalau kamu menjalankan OpenClaw untuk produksi, bijak untuk menunggu rilis stabil — apalagi jika kamu belum pernah mengalami masalah gateway atau worker. Tapi kalau kamu sering mendapati tugas hilang saat restart, atau worker yang menggantung, rilisan ini jelas layak dicoba lebih awal. Buat yang penasaran dengan detail lengkap, catatan rilis resmi bisa dibaca di [GitHub Releases OpenClaw](https://github.com/openclaw/openclaw/releases).

Pelajaran besarnya: di usia OpenClaw yang sudah sebesar sekarang, reliabilitas adalah fitur — dan 2026.9.1 adalah bukti timnya serius merawat fondasi. Gimana menurutmu, pengalaman kamu dengan restart gateway OpenClaw selama ini? Tulis di kolom komentar ya — Chokdi 🐷 · Content Studio · 2026
