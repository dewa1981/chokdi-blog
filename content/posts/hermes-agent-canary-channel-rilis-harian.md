---
title: 'Hermes Agent Canary: Rilis Tiap Hari Jam 13.45 WIB, Tapi Bukan "Versi Lebih Baru"'
description: "Build canary Hermes Agent terbaru v0.23.2+canary.20261118T064620Z terbit 18 November 07.55 UTC. Canary adalah aplikasi desktop terpisah dengan CLI hermes-canary — bukan channel yang bisa dipilih di hermes update. Ini bedanya, plus 4 jebakan."
date: 2026-11-19T01:22:01+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Update", "Self-Host"]
---

Kalau kamu memantau halaman rilis Hermes Agent, pemandangan terakhirnya agak membingungkan: di atas `v0.23.2` yang bertanda **Latest**, ada tumpukan tag lain bernama `v0.23.2+canary.20261118T064620Z`. Yang terbaru justru bukan yang "resmi". Build canary itu terbit **18 November 2026 pukul 07.55 UTC — 14.55 WIB**, sekitar sembilan jam sebelum artikel ini ditulis.

Pertanyaannya wajar: apa bedanya, dan haruskah pindah? Jawaban singkatnya: **canary bukan "versi lebih baru" dari stable — ia jalur yang berbeda, dan di banyak jenis instalasi kamu tidak bisa memilihnya sama sekali.** Ini penjelasan lengkapnya.

## 🏷️ Apa itu tag canary

Canary memakai ruang tag sendiri: `v<versi-stable>+canary.<YYYYMMDDTHHMMSSZ>`. Artinya build canary selalu menempel pada satu versi stable sebagai patokan — `v0.23.2+canary.20261118T064620Z` adalah build dari jalur v0.23.2 yang dirakit 18 November 06.46 UTC.

Dokumentasi internal Nous menyebut canary punya alur terjadwal sendiri, terpisah dari gerbang rilis stabil. Dan gerbang itu tegas: *"A successful builder alone is not a stable release."* Jadi build canary yang hijau **bukan** jaminan akan jadi stable — ia harus lulus admission dan promosi dulu.

Lima build terakhir: 13 Nov 06.44, 15 Nov 06.44, 16 Nov 07.00, 17 Nov 06.46, dan 18 Nov 06.46 UTC. Rata-rata sekitar **06.45 UTC atau 13.45 WIB** — jam yang sama hampir tiap hari.

## 🖥️ Canary itu aplikasi terpisah, bukan saklar

Ini bagian yang paling sering disalahpahami. Di desktop, **bundle canary adalah aplikasi yang berdiri sendiri**. Ia tidak menimpa stable, termasuk di Windows lewat MSIX. Ikonnya berlatar kuning (kuning gelap di dark mode), dan perintah CLI-nya **`hermes-canary`** — bukan `hermes`.

Konsekuensinya:

- Masing-masing aplikasi menyimpan state desktop sendiri, tidak bercampur.
- Update terjadi di dalam channel yang dipanggang di build-nya masing-masing.
- **Pindah channel berarti memasang aplikasi yang lain, bukan mengubah setting.** Tidak ada toggle di menu.

Ada lagi jenis ketiga: bundle commit satu kali (one-off) dengan ikon merah dan CLI `hermes-<short-sha>`. Ini tidak pernah mengecek update — sekali pasang, diam di situ.

## ⚙️ Kenapa `hermes update` tidak bisa ke canary

Untuk instalasi source (installer `install.sh`, `install.ps1`, Hermes-Setup), `hermes update` hanya mengikuti channel **stable**: rilis `vX.Y.Z` terakhir yang benar-benar dipublikasikan — "never a draft, prerelease or canary tag". Yang bisa kamu pilih cuma dua:

- `hermes update --set-channel main` — ikut setiap commit di `main`.
- `hermes update --set-channel stable` — kembali ke rilis saja.

Ada juga `hermes update --channel main` untuk sekali jalan tanpa menyimpan pilihan. Pilihannya disimpan per instalasi di `update.installs` dalam `config.yaml`. Jadi kalau tujuanmu "paling baru tapi bukan canary", jawabannya **main** — commit demi commit, bukan rilis.

## 🪤 Empat jebakan yang perlu kamu tahu

**1. Rollback itu nyata, dan namanya memang "rollback".** Menjalankan `--set-channel stable` akan memaku checkout ke commit rilis yang persis — termasuk kalau commit itu lebih lama. Desktop menyebutnya rollback, dan `hermes update --check` akan bilang checkout kamu lebih baru, bukan menawarkan update.

**2. Di Termux, canary bisa menjebakmu di versi bawah.** Channel apt-nya dipisah: suite `hermes-stable` dan `hermes-canary`. Versi canary membawa `~canary.<timestamp>` yang **urutannya lebih rendah** dari versi stable pasangannya. Untuk pindah channel, kamu harus mengubah path channel *dan* suite di `hermes-agent.list`, lalu `pkg update && pkg upgrade hermes-agent`. Bonus catatan: halaman Termux saat ini memberi peringatan bahwa paketnya sedang rusak dan perbaikannya sedang dikerjakan.

**3. Hijau di canary bukan berarti aman untuk produksi.** Canary dibangun tiap hari dari tumpukan PR yang belum tentu masuk stable. Untuk bot 24 jam yang menyentuh uang atau transaksi, stable tetap pilihan benar.

**4. Jangan tertukar CLI.** Menjalankan `hermes` padahal yang terpasang canary, atau sebaliknya, adalah sumber kebingungan klasik — dua aplikasi, dua state, dua perintah. Cek `hermes --version` sebelum menyimpulkan apa pun.

## ✅ Checklist sebelum mencoba canary

1. **Bukan di server produksi.** Pakai container, VM, atau mesin kedua.
2. **Backup dulu**: salin `state.db` (jangan buka yang live langsung), `config.yaml`, dan `.env`.
3. **Pisahkan identitas**: sadari bahwa canary memakai `hermes-canary` dan state desktop sendiri.
4. **Catat versi awal** dengan `hermes --version`, supaya kamu bisa membandingkan setelah update.
5. **Siapkan jalan pulang**: untuk instalasi source, `--set-channel stable` memaku ke rilis terakhir.

Halaman unduhan canary terpisah ada di `hermes-assets.nousresearch.com/releases/canary/index.html` — kami cek, respons 200.

## 🎯 Kesimpulan

Canary bukan "stable yang lebih baru". Ia jalur build harian dengan aplikasi desktop sendiri, ruang tag sendiri, dan gerbang rilis yang belum dilewati. Kalau kamu ingin fitur paling mutakhir di instalasi source, channel yang tersedia adalah **main** — bukan canary. Kalau kamu ingin build desktop terbaru untuk uji coba atau lapor bug, pasang aplikasi canary secara terpisah dan jangan sentuh yang stable. Untuk bot produksi, diam di stable itu membosankan tapi benar.

**Baca juga:** [Hermes Agent v0.23.2 Rilis: 1.989 PR Ditumpuk Jadi Satu Patch, 6 Fitur yang Tidak Ada di Judul](https://chokdi.ano99.com/posts/hermes-agent-v0232-1989-pr-durable-subagent/) · [Hermes Agent Berhenti Ikut `main` — Update Sekarang Ikut Rilis Bertag](https://chokdi.ano99.com/posts/hermes-update-ikut-rilis-bertag/) · [Hermes Agent 8 Pekan: 13 Rilis, Katalog Plugin 1.050+, dan Kenapa Upgrade Sekarang Lebih Aman](https://chokdi.ano99.com/posts/hermes-agent-262-ribu-stars-13-rilis-november-2026/)

— Chokdi 🐷 · Content Studio · 2026
