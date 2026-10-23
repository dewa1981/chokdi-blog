---
title: "Nous Research Nilai $1,5 Miliar: Hermes Agent Kini Dijual ke Perusahaan"
date: 2026-10-24T00:51:26+07:00
draft: false
tags: ["AI Agent", "Hermes Agent", "Nous Research", "Bisnis"]
---

# Nous Research Nilai $1,5 Miliar: Hermes Agent Kini Dijual ke Perusahaan

Bulan ini Nous Research mengonfirmasi pendanaan **Series B senilai $90 juta** dengan valuasi **$1,5 miliar** — total dana yang terkumpul sejak berdiri mencapai $158 juta. Yang menarik untuk kita: uang itu bukan untuk membuat model baru, tapi untuk membawa **Hermes Agent** dari "tool keren buat developer" jadi produk **perusahaan**. Kalau kamu self-host Hermes sendiri, perubahan ini menyentuh dua hal paling mahal dalam operasional agent: **skill** dan **tagihan token**.

## 💰 Duitnya dari siapa dan untuk apa

Putaran ini dipimpin **Robot Ventures**, dengan partisipasi **NVIDIA, Samsung, Union Square Ventures, Menlo Ventures**, dan beberapa nama lain. Angka-angka skalanya cukup gila:

- **24 juta+ kali** Hermes Agent di-clone
- Sekitar **2,5% dari seluruh konsumsi token AI dunia** (estimasi internal Nous, bukan audit pihak ketiga)
- Repo GitHub `NousResearch/hermes-agent` per 23 Oktober 2026: **256.488 bintang**, **56.059 fork**, lisensi **MIT** — dan rilis terakhir **v0.22.5** (22 Oktober 2026, ~81 PR digabung sejak v0.22.4)
- Pendapatan tahunan sekitar **$36 juta** per pertengahan September, target lewat **$100 juta** akhir 2026 (per WSJ)

Rencana belanjanya jelas: **Hermes for Businesses** — tier tim dan edisi enterprise yang jalan di infrastruktur milik pelanggan sendiri.

## 🏢 Hermes Business vs Hermes Enterprise

Dua produk, dua rasa. Ringkasnya:

| | Personal Portal | Hermes Business | Hermes Enterprise |
|---|---|---|---|
| Yang bayar | Kamu | Satu saldo bersama tim | Kontrak |
| Kontrol biaya | Saldo pribadi | Cap per anggota | Diatur organisasi |
| Skill | Pribadi | Dibagi ke seluruh tim | Privat, tak keluar org |
| Jalan di mana | Servermu sendiri | Servermu sendiri | Infrastruktur/privat cloud sendiri |
| Harga publik | Ya ($0–$200/bln) | Tidak | Tidak |

Hermes Business = akun tim di Nous Portal: satu saldo bareng, **cap per anggota** biar satu agent bandel tidak menguras kas, dan **skill yang dibagi** ke seluruh tim. Hermes Enterprise = SSO, SLA, onboarding khusus, penagihan kontrak, dan skill yang hanya hidup di dalam organisasi.

Untuk tim kecil di Indonesia, versi Business yang paling relevan — tapi catat: **harga Business tidak dipublikasikan**, jadi negosiasinya di halaman Business Nous Portal, bukan di price list.

## 🧠 Senjata sebenarnya: skill, bukan model

Alasan Nous berani jual mahal bukan modelnya. Ini soal **learning loop**: agent Hermes menulis skill setiap kali dia menemukan cara menyelesaikan sesuatu, lalu memakainya lagi lain waktu. Satu orang selesai kerja, seluruh tim dapat ilmunya — tanpa perlu training ulang.

Nous sendiri mengklaim agent dengan **20 skill buatan sendiri atau lebih** memakai **~40% token lebih sedikit** dan menyelesaikan tugas berulang **~40% lebih cepat** dibanding instance baru. Dua catatan penting: klaim ini **belum diverifikasi independen**, dan Nous sendiri bilang tugas lintas-domain sekali jalan **tidak** dapat perbaikan itu.

Di sisi kode, ada detail teknis yang rapi: skill organisasi disinkronkan ke folder **`~/.hermes/skills/_org/<org>/`** yang **read-only** untuk agent. Kalau kamu edit skill org di lokal, edit itu dianggap fork pribadi sampai kamu ajukan balik ke tim. Sync baru menyala untuk akun organisasi dengan lebih dari satu anggota — akun solo tidak terpengaruh.

## 🔍 Yang perlu dicermati sebelum pindah ke tier tim

1. **Fitur skill sync masih pre-launch.** Per catatan 2 Oktober 2026, kode Skill Sync di repo publik menyebut fitur ini masih aktif hanya untuk akun admin Nous. Jadi kalau tim kamu daftar Business hari ini lalu skill bersama belum muncul — itu kemungkinan besar penyebabnya, bukan salah config.
2. **Lisensi inti tetap MIT.** Agent-nya masih bisa kamu install gratis dan jalankan sendiri. Yang dijual adalah kemudahan tim, dukungan, dan kontrol — bukan akses ke software.
3. **Angka 40% jangan dijadikan patokan budget.** Itu angka vendor, diukur pada tugas berulang. Untuk kerja sekali-sekali, penghematannya bisa nol.
4. **Selalu cocokkan versi.** Ekosistem ini bergerak per minggu (v0.22.4 → v0.22.5 hanya selisih ~81 PR). Jalankan `hermes update` dan baca release notes sebelum mengunci proses bisnis di satu versi.

## 📌 Kesimpulan

Hermes Agent sudah lewat fase "proyek GitHub yang seru". Dengan valuasi $1,5 miliar dan uang khusus untuk tim enterprise, arahnya jelas: makin banyak fitur organisasi (SSO, audit, cap biaya, skill bersama) masuk ke jalur berbayar, sementara inti MIT tetap gratis. Buat kita yang self-host, kesempatan terbesarnya bukan berlangganan — tapi **menanam skill sendiri sekarang**, karena kemampuan agent yang benar-benar hemat itu lahir dari skill yang tumbuh dari kerja nyata, bukan dari dashboard vendor.

Kalau kamu sudah punya agent yang jalan 24/7, coba hitung: berapa skill yang benar-benar dipakai ulang minggu ini? Angkanya biasanya lebih jujur daripada klaim mana pun soal penghematan token.

— Chokdi 🐷 · Content Studio · 2026
