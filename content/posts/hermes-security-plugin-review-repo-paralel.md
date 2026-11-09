---
title: "Hermes Security: 10 Subagent Baca Repo 360 Ribu Baris, Laporan Siap SARIF"
date: 2026-11-10T01:11:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Nous Research", "Keamanan", "DevSecOps"]
---

Nous Research merilis plugin resmi **hermes-security** pada 8 November 2026 (pukul 18:47 UTC, atau 9 November 02:47 WIB). Penulisnya Mark S. (@mark_s), engineer Hermes Agent yang mencantumkan CISSP di bio-nya. Masalah yang disasar sederhana: scanner biasa menyodorkan tumpukan alert tanpa pernah menjawab satu pertanyaan penting — **penyerang benar-benar bisa mencapai kode itu?**

Plugin ini menjawabnya dengan cara yang beda: bukan mencocokkan pola, tapi menyusun model ancaman lalu memakai subagent untuk membuktikan jalur serangnya.

## 🛡️ Mulai dari Model Ancaman, Bukan dari Daftar Aturan

Langkah pertama bukan scan, tapi berpikir: apa saja yang bisa dijangkau penyerang, dan input mana yang benar-benar dipercaya. Setelah itu kode dipotong **per folder menjadi bagian sekitar 4.000 baris** — kira-kira sebanyak yang bisa dibaca satu reviewer dalam sekali jalan.

Yang membaca sampai **10 reviewer subagent paralel**, ditambah satu reviewer tambahan yang tidak melihat potongan, melainkan seluruh cakupan: mencari entry point dan trust boundary. Setiap kandidat temuan dicek ulang ke kode aslinya, lalu dilacak apakah ada jalur nyata dari input ke perilaku berbahaya. Kalau jalurnya tidak bisa dibuktikan, kandidat dibuang — tapi tetap dicatat di laporan sebagai "ditolak", lengkap dengan alasannya.

Bagian terakhir itu yang paling berharga: kita bisa melihat apa yang **sudah** diperiksa dan dinyatakan aman.

## 📦 Angka yang Perlu Diingat

- **90 chunk ≈ 360.000 baris** — selama production code masih muat, seluruhnya dibaca, tidak ada sampling.
- Repo lebih besar: file diurutkan berdasarkan perilaku berisiko (route, input request, perintah shell, SQL, deserialisasi, auth, webhook), yang paling berisiko dibaca lebih dulu sampai kuota habis.
- Dua chunk paling berisiko dapat **reviewer kedua yang independen**.
- Reviewer yang gagal menyelesaikan file-nya diganti reviewer baru, sampai **6 putaran** selama tiap putaran ada kemajuan.
- Tiga mode: **standard**, **deep** (tidak melewati file apa pun, default 3 pass independen), dan **diff** (hanya perubahan belum di-commit, atau branch dibanding default branch).
- File di atas **8 MB**, symlink, kode vendored, dan file spesial dilewati — dan semuanya muncul di laporan beserta alasannya.

## 🧪 Tes Konfirmasi: Repro Ditulis, Tapi Bukan Sandbox

Opsi "Run tests to confirm findings" membuat agent menulis reproduksi kecil dan menjalankannya di **salinan sementara** repo, dengan variabel environment yang mirip kredensial dibuang lebih dulu.

Dokumentasinya jujur: itu **bukan sandbox**, kode repo dijalankan sebagai user kita. Untuk menguji aplikasi yang hidup dibutuhkan grant per-scan — satu origin, satu jam, 200 request — dan grant itu **tidak bisa dikeluarkan tool agent sendiri**. Agent tidak bisa diam-diam menembaki produksi.

## 🧾 Laporan: Bukti, yang Ditolak, dan Celah Cakupan

Hasil scan diekspor ke **Markdown, JSON, CSV, dan SARIF**. Format terakhir itu yang bikin plugin ini muat di pipeline yang sudah ada — GitHub Code Scanning, misalnya, bisa langsung membaca SARIF.

Laporan memisahkan temuan yang **didukung bukti kode** dari temuan yang **terkonfirmasi tes**, menyimpan kandidat yang ditolak, dan mencatat bagian mana yang tidak terbaca (coverage gap). Pemetaannya mengacu ke OWASP Top 10:2025 dan ASVS 5.0.0, meski Nous menegaskan itu bukan sertifikasi.

## ⚠️ Tiga Hal yang Sering Dilewatkan

**1. Belum ada benchmark.** Nous belum mempublikasikan angka recall atau precision dibanding Semgrep, CodeQL, atau korpus kerentanan publik. Artinya plugin ini belum terbukti "lebih baik" dari SAST — ia menawarkan cara kerja yang berbeda, bukan skor yang lebih tinggi. Dokumentasinya sendiri mengingatkan model bisa melewatkan isu atau salah membaca kode, jadi kesimpulan tetap perlu dicek manusia.

**2. Kode dikirim ke provider model.** Review dilakukan oleh model yang dikonfigurasi di Hermes. Kalau repo berisi kode klien atau rahasia dagang, ini keputusan kebijakan data, bukan sekadar soal teknis.

**3. Dependency check menyentuh jaringan.** Scan pertama mengunduh **osv-scanner sekitar 55 MB** dari GitHub dan menolaknya kalau SHA-256 tidak cocok. Lockfile dicek ke api.osv.dev dan api.deps.dev, versi runtime ke endoflife.date — bisa dimatikan lewat `HERMES_SECURITY_DEPENDENCY_CHECK=off`. Satu hal yang benar secara desain: **advisory saja tidak otomatis jadi temuan**; kode harus terbukti mencapai perilaku rentan itu.

## 🚀 Cara Pasang

```sh
# butuh Hermes >= 0.21.5 dan Python >= 3.11
hermes plugins install hermes-security --enable
# restart Hermes setelahnya
```

Pemakaian: minta di chat ("scan repo ini untuk isu keamanan"), pakai slash command `/security`, atau dari CLI `hermes security-review`. Di Hermes Desktop ada halaman **Security** tersendiri — tapi seperti plugin Desktop lain, ia **mati secara default** dan harus dinyalakan di Capabilities → Plugins. Kalau Desktop terhubung ke Hermes di mesin lain, instal lewat dialog Desktop supaya halaman itu ikut terbawa.

## Kesimpulan

hermes-security paling masuk akal untuk repo di bawah 360 ribu baris production code, untuk **scan diff sebelum merge**, dan untuk tim yang butuh bukti "bisa dieksploitasi atau tidak" alih-alih daftar alert. Ia belum pengganti SAST di pipeline kepatuhan dan belum punya angka pembanding — posisinya pelengkap, bukan pengganti.

Arah desainnya yang menarik: output dibuat bisa diperiksa ulang (bukti, kandidat ditolak, coverage gap), bukan cuma skor — pola yang sama dengan [rilis v0.23.0 "The Hearth"](/posts/hermes-agent-v0230-hearth-desktop-di-browser/). [v0.22.7](/posts/hermes-agent-v0227-threshold-update-november-2026/) sudah cukup sebagai syarat minimum, dan kalau kamu sedang bikin plugin sendiri, [deadline hackathon 12 November](/posts/hermes-plugin-hackathon-20-ribu-deadline-12-november/) masih terbuka.

Sudah coba scan repo sendiri? Bandingkan hasilnya dengan scanner yang biasa kamu pakai — selisih false positive-nya biasanya lebih informatif daripada jumlah temuannya.

— Chokdi 🐷 · Content Studio · 2026
