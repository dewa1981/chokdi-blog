---
title: "OpenHuman Tembus 39.782 Star di GitHub, Tapi Memory Engine-nya Cuma 7 Star"
date: 2026-09-15T00:20:00+07:00
draft: false
tags: ["AI", "Open Source", "AI Agent", "Rust"]
---

OpenHuman dari TinyHumans AI sudah dibahas di mana-mana: desktop agent open source, 39.782 star, juara trending GitHub. Tapi ada satu angka yang hampir tidak pernah disebut siapa pun — repo memory engine-nya sendiri cuma punya **7 star**. Justru dari angka yang jomplang itu kita bisa belajar hal paling penting soal membangun agent AI.

## Apa Itu OpenHuman?

OpenHuman adalah agent AI desktop open source berlisensi GPL-3 yang jalan langsung di laptop (Mac, Windows, Linux). Dibuat oleh TinyHumans AI dengan bahasa **Rust** sebagai tulangnya. Repo-nya lahir 18 Februari 2026, dan per 15 September 2026 datanya seperti ini:

| Metrik | Angka |
|---|---|
| Star | **39.782** |
| Fork | 3.922 |
| Open issue | 188 |
| Rilis | 56 (terakhir v0.63.12) |
| Kontributor | 176+ |
| Push terakhir | 14 Sep 2026 |

Menurut README-nya, dalam sepekan pertama peluncuran OpenHuman jadi repo nomor satu di trending GitHub selama **sembilan hari berturut-turut**. Statusnya masih ditandai "early beta" — jujur, dan itu bagus.

Yang ditawarkan bukan cuma chatbot. Ada tiga pilar: **otak** (memori persisten lokal), **orkestrator** (menjalankan banyak agent sekaligus), dan **peneliti** (nyisir data sendiri plus web sebelum kamu selesai nanya).

## Paradoks 39.782 vs 7

Ini bagian yang menarik. Tim TinyHumans tidak menaruh semua kode di satu repo raksasa. Mereka memecahnya:

| Repo | Star | Peran |
|---|---|---|
| `openhuman` | **39.782** | Harness + aplikasi desktop |
| `tinycortex` | 253 | Model memori ("second brain") |
| `tinyagents` | 55 | Graph run agent yang ter-checkpoint |
| `tinyflows` | 37 | Engine workflow otomatis |
| `tinymemory` | **7** | Router memori ke interface standar |

Perhatikan polanya: **bintang menumpuk di pintu depan, bukan di komponen dapur.** Orang memberi star ke produk yang bisa mereka unduh dan coba, bukan ke library internal. Itu bukan berarti komponennya jelek — `tinymemory` bahkan mendeskripsikan dirinya sebagai "route any memory system into a standardized interface", yang justru ide arsitektur paling waras di daftar ini.

Pelajaran untuk kita yang juga ngoprek agent: jangan takut memecah sistem jadi paket kecil. Yang menentukan kualitas bukan jumlah star per repo, tapi seberapa bersih **kontrak antar komponen**-nya.

## Otaknya: Markdown di SQLite, Bukan Black Box

Cara OpenHuman menyimpan memori patut ditiru. Data kamu dikompres jadi **pohon Markdown ber-skor** yang disimpan di SQLite lokal, lalu di-mirror sebagai vault Obsidian yang bisa dibuka dan diedit tangan. Bukan "vector soup" yang isinya tidak bisa diperiksa manusia.

Ada fitur **auto-fetch** yang menyuapi otak itu tiap 20 menit — jadi agent sudah punya konteks hari ini sebelum kamu tanya. Pola *local-first + format yang bisa dibaca manusia* ini persis alasan SQLite menang di banyak proyek: file tunggal, tanpa server, gampang di-backup. Kami sudah bahas panjang soal ini di artikel [SQLite: Kenapa "Lite" Justru Menang](/posts/sqlite-kenapa-lite-justru-menang/).

### TokenJuice: Kompresi Sebelum Sampai Model

Detail teknis favorit saya: **TokenJuice**. Output tool dikompres *sebelum* masuk ke model — informasi sama, token sampai 80% lebih hemat. README-nya blak-blakan: "A brain this big would be unaffordable without it." Betul. Memori besar tanpa kompresi = tagihan API meledak.

## Orkestrasi: Graph yang Bisa Di-replay

Workflow dijalankan lewat `tinyflows` dengan pemicu, gerbang persetujuan, dan kanvas review. `tinyagents` menjalankan graph ter-checkpoint: agent yang macet bisa di-arahkan ulang, yang berhenti mengembalikan akar masalahnya, dan setiap run bisa di-replay lengkap dengan **biaya per pemanggilan**.

Fitur terakhir itu sering dilupakan builder: bukan cuma "agent-nya jalan", tapi "berapa rupiah satu run ini". Pola arsitekturnya *split brain* — agent refleks cepat untuk triase, core penalaran berat untuk delegasi.

## Bandingkan dengan Hermes Agent

Sebagai pembanding sesama agent open source: **Hermes Agent** (Nous Research) ditulis Python, MIT, dan per hari yang sama mencetak **245.415 star** dengan 51.110 fork. Arahnya beda — Hermes menekankan *compounding skills*, tiap tugas selesai dievaluasi dan disimpan jadi skill baru. Catatan pendekatan itu ada di [Second Brain untuk AI Agent](/posts/second-brain-ai-agent/).

| | OpenHuman | Hermes Agent |
|---|---|---|
| Bahasa | Rust + TypeScript | Python |
| Lisensi | GPL-3 | MIT |
| Fokus | Memori lokal + desktop app | Skill yang menumpuk |
| Star | 39.782 | 245.415 |

Dua-duanya bukan "yang lebih baik", tapi dua jawaban berbeda atas pertanyaan yang sama: bagaimana agent tetap pintar setelah percakapan pertama lewat.

## Lima Pelajaran Praktis

1. **Produk di depan, komponen di belakang.** Star mengalir ke yang bisa dicoba.
2. **Local-first = SQLite + file yang bisa dibaca manusia.** Hindari black box.
3. **Kompresi token itu fitur wajib**, bukan optimasi belakangan.
4. **Graph ter-checkpoint mengalahkan sekali jalan.** Agent macet harus bisa di-steer.
5. **Tulis interface dulu, implementasi belakangan.** Dasbor bagus tidak menyelamatkan arsitektur berantakan.

## Kesimpulan

OpenHuman menarik bukan karena 39.782 star-nya, tapi karena keputusan desainnya berani: memori manusia-readable, paket dipecah kecil, dan biaya per run dihitung terbuka. Kalau kamu sedang bangun agent sendiri, tiga hal itu lebih berguna daripada mengejar bintang di GitHub.

Kamu sudah coba OpenHuman atau masih setia sama harness sendiri? Tulis di kolom komentar — atau baca dulu [perbandingan WorkBuddy vs Hermes Agent](/posts/tencent-workbuddy-vs-hermes-agent/) biar ada bahan pembanding.

— Chokdi 🐷 · Content Studio · 2026
