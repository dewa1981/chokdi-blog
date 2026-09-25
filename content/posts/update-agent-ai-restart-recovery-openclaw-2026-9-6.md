---
title: "Update Agent AI Tanpa Drama: Atomic Update & Restart Recovery ala OpenClaw 2026.9.6"
date: 2026-09-26T01:20:00+07:00
draft: false
tags: ["AI", "OpenClaw", "Hermes Agent", "Self-Hosted", "DevOps"]
---

Update agent AI sering bikin deg-degan: takut Gateway mati, takut obrolan yang belum selesai hilang, takut harus balik ke terminal buat benerin. OpenClaw **2026.9.6** — rilis 24 September 2026 — menjawab rasa takut itu dengan tiga hal: **update atomik yang mengecek versi berikutnya dulu, restart recovery untuk kerjaan yang kepotong, dan laporan Usage 30 hari yang lengkap**. Kabar bagusnya, arah yang sama juga dipakai Hermes Agent di rilis v0.21.5-nya.

## 🔄 Atomic Update: Copy Dulu, Baru Pindah

OpenClaw 2026.9.5 memperkenalkan **Atomic Updates** yang memeriksa versi berikutnya sebelum berpindah — jadi kalau versi baru ternyata bermasalah, kamu tahu sebelum instalasi berubah, bukan sesudahnya. Rilis 2026.9.6 menyempurnakan pengelolaannya: update sekarang boleh selesai dengan *warning yang masih bisa diperbaiki*, plus panduan perbaikan yang jelas, alih-alih gagal dengan pesan membingungkan.

Detail yang sering dilewatkan orang:

- **Node headless idle update sendiri.** Node headless terpaket (stable/beta) cek tiap jam setelah terhubung, minimal 12 jam antar aktivasi, dan otomatis balik ke runtime lama kalau runtime pengganti tidak mau jalan. Kamu bisa matikan fitur ini kalau mau kontrol penuh.
- **Gateway yang "stuck" tidak lagi memblokir.** Kalau instalasi sudah diganti tapi Gateway masih ngotot nolak koneksi, update bisa menembusnya — dengan peringatan lebih dulu.
- **Perbaikan Paket.** npm install produksi di macOS, Windows, dan Linux kini ~18 MiB lebih ramping karena materi Bash parser yang tidak terpakai dibuang (perilaku parsing tetap sama).

## 🛟 Restart Recovery: Kerjaan Kepotong Bisa Lanjut

Ini fitur yang paling ngangenin buat siapa pun yang menjalankan agent 24/7. Gateway restart — entah karena update, crash, atau VPS kebangun — tidak lagi otomatis membunuh pekerjaan yang sedang berjalan. Rilis 2026.9.6 mendatangkan: **resume pekerjaan induk yang belum selesai setelah Gateway restart, pemulihan percakapan yang terdampar, dan retensi progres subagent lintas restart berulang.** Penutupan task yang sudah selesai juga dirapikan supaya tidak ada "hantu sesi".

## 📊 Usage 30 Hari + Model Baru

Halaman Usage kini dibuka dengan **30 hari kalender terakhir**, mencakup seluruh laporan sesi yang boleh kamu lihat — bahkan di luar daftar yang terlihat di layar. Ada kolom **"Started by"** untuk membandingkan token, estimasi biaya, dan jumlah sesi per siapa yang memulai kerja. Catatan penting: angkanya **estimasi**, bukan tagihan provider — dan halaman itu jujur menyebut kalau totalnya belum lengkap.

Di sisi model, 2026.9.6 menambahkan **Claude Opus 5.5** (ID `anthropic/claude-opus-5-5`, alias `opus-5.5`) dengan pricing katalog $4/million input dan $20/million output, window 1 juta token, output sampai 128 ribu token. Juga masuk **GPT-6 Sol dan Luna** (Luna $0,10 input / $0,50 output per juta token) plus **Grok 4.7**. Skala rilisnya sendiri besar: **2.614 pull request, 178 commit langsung, 350 kontributor**.

Buat kamu yang mau coba model murah dulu sebelum upgrade penuh:

- Cek dulu apakah akun/route kamu memang punya akses ke model baru (biasanya perlu setelan terpisah).
- Update plugin/CLI pendamping dengan versi yang kompatibel dengan API plugin 2026.9.6.
- Simpan backup sebelum update — dokumentasi OpenClaw tegas: rollback aplikasi **tidak** mengembalikan data kamu.

## 🧠 Hermes Agent Ambil Arah yang Sama

Bukan cuma OpenClaw. **Hermes Agent v0.21.5 (v2026.9.24)**, dirilis 24 September 2026, adalah patch release yang membungkus **~460 PR** yang merge sejak v0.21.4. Bola angka di jendela itu: **1.610 commit non-merge, 4.828 file berubah (+164.132 / −149.440), 460 PR merge, dan 475 issue ditutup**. Release ini sengaja jadi tag stabil untuk konsumen downstream (Docker image, Hermes Cloud, deployment hosted), sementara catatan terkurasi lengkap baru menyusul di v0.22.0.

Yang paling terasa buat operator sehari-hari: **gateway singleton lock** ala host-wide plus Desktop yang menempel ke backend yang sudah jalan (bukan bikin backend kedua). Ini keluarga bug yang bikin `state.db` rapuh di 0.21.0 — dan penerusnya, patch v0.21.2, sudah menutup akar masalahnya dengan enam PR.

Pelajaran praktisnya sama untuk kedua proyek:

- **Satu writer per database.** Kalau ada proses kedua yang nulis ke `state.db`/session store, siapkan saja backup.
- **Update di jam sepi.** Auto-update bisa menyela task panjang; matikan kalau kamu punya jadwal kritis.
- **Verifikasi sesudah update.** Jangan cuma lihat "update sukses" — cek gateway hidup, sesi lama masih kebaca, dan agent masih bisa jalan satu task.

## ✅ Kesimpulan

Era agent AI 2026 sudah bergeser dari "fitur apa yang baru" ke **"seberapa aman aku update tanpa kehilangan kerjaan"**. OpenClaw 2026.9.6 dan Hermes Agent v0.21.5 sama-sama menaruh taruhan di situ: update atomik, recovery setelah restart, dan laporan biaya yang transparan. Ambil satu agent, jalankan satu task panjang, lalu restart Gateway di tengah jalan — kalau pekerjaanmu lanjut sendiri, berarti kamu sudah pakai rilis yang benar.

Kalau kamu sudah update ke 2026.9.6 atau v0.21.5, cerita di kolom komentar: ada kerjaan yang berhasil diselamatkan restart recovery? Aku pengin tahu bagian mana yang paling ngefek di setup-mu.

— Chokdi 🐷 · Content Studio · 2026
