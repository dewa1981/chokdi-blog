---
title: "Memory Tree OpenHuman: Bagaimana Ia Menyusun dan Memampatkan Konteks Agent"
date: 2026-09-15T00:20:00+07:00
draft: false
tags: ["AI", "AI Agent", "Open Source", "Rust"]
---

OpenHuman ramai dibahas karena angka bintangnya. Kami sudah membedah angka itu — termasuk fakta bahwa repo mesin memorinya cuma punya 7 star — di artikel [OpenHuman 39.774 Star, Tapi Mesin Memori TinyMemory Cuma 7 Star](/posts/openhuman-tinymemory-7-star/). Tapi justru ada bagian lain yang luput diperhatikan: **bagaimana OpenHuman sebenarnya menyimpan konteks dan menjalankan banyak agent sekaligus**. Itu bagian yang paling layak ditiru.

## Memori Disimpan Sebagai Pohon Markdown di SQLite

Kesalahan paling umum builder agent: menjejalkan semua riwayat percakapan ke context window, lalu berharap model "ingat". OpenHuman memilih jalan lain.

Data yang masuk dikompres menjadi **pohon Markdown ber-skor** yang tersimpan di SQLite di mesin kamu sendiri, lalu di-mirror sebagai vault Obsidian yang bisa dibuka dan diedit tangan. Situs resminya menyebutnya singkat: *"No vector-soup black box."*

Artinya tiga hal:

1. **Bisa diperiksa manusia.** Kalau agent menjawab aneh, kamu bisa buka file-nya dan lihat konteks apa yang dipakai.
2. **Bisa diedit manual.** Salah ingat? Hapus barisnya. Tidak perlu re-index embedding.
3. **Backup itu mudah.** Satu file SQLite plus folder Markdown — persis alasan SQLite tetap menang di banyak proyek, yang pernah kami bahas di [SQLite: Kenapa "Lite" Justru Menang](/posts/sqlite-kenapa-lite-justru-menang/).

Ada juga mekanisme **auto-fetch** yang menyuapi otak itu tiap 20 menit dari aplikasi yang tersambung (Gmail, Notion, GitHub, Slack, dan 100+ integrasi OAuth lainnya). Jadi agent sudah punya konteks pagi ini sebelum kamu mengetik pertanyaan.

## TokenJuice: Kompresi Sebelum Output Masuk Model

Fitur teknis yang paling sering dilewatkan: **TokenJuice**. Output dari tool dikompres *sebelum* dikirim ke model — informasi dianggap sama, token sampai **80% lebih hemat**.

README-nya jujur soal alasannya: *"A brain this big would be unaffordable without it."* Memang begitu. Memori besar tanpa lapisan kompresi bukan fitur, tapi tagihan API yang membengkak tiap bulan.

Pola ini gampang ditiru di stack apa pun: sebelum hasil tool masuk prompt, ringkas dulu jadi struktur (JSON padat, tabel, atau poin kunci) alih-alih menempelkan output mentah 4.000 baris.

## Orkestrasi: Workflow yang Di-approve, Graph yang Bisa Di-replay

Bagian kedua OpenHuman adalah mesin workflow-nya. Dipecah jadi dua komponen kecil:

| Komponen | Star | Fungsi |
|---|---|---|
| `tinyflows` | 37 | Engine workflow: ter-trigger, ada gerbang persetujuan |
| `tinyagents` | 55 | Graph run agent yang ter-checkpoint |

Alurnya cukup waras: agent **mengusulkan** otomatisasi, kamu meninjau di kanvas, lalu menyimpannya. Run-nya durable dan bisa disetujui sebelum jalan — bukan agent yang tiba-tiba mengirim email ke klien tanpa izin.

Yang paling berharga dari `tinyagents`: **setiap run bisa di-replay lengkap dengan biaya per pemanggilan**. Agent yang macet bisa diarahkan ulang; yang berhenti mengembalikan akar masalahnya, bukan cuma pesan error kosong.

Buat siapa pun yang pernah menunggu agent berjam-jam tanpa tahu bagian mana yang salah, ini bukan kemewahan — ini kebutuhan dasar.

## Split Brain: Refleks Cepat, Penalaran Berat

OpenHuman menjalankan dua lapisan: agent **refleks** yang cepat untuk menangani trafik masuk (triage, klasifikasi, jawaban pendek), dan **core penalaran** yang lebih berat untuk mendelegasikan ke fleet worker. Pola yang sama seperti kokpit pesawat: pilot tidak berpikir lama untuk hal yang butuh refleks.

Implikasi praktisnya soal biaya. Tidak semua tugas pantas dikirim ke model termahal. Triage dulu dengan model murah, eskalasi ke model besar hanya kalau perlu.

## Beda Arah dari Hermes Agent

Sebagai perbandingan, agent yang kami pakai sehari-hari — **Hermes Agent** — menempuh jalan berbeda untuk masalah yang sama:

| | OpenHuman | Hermes Agent |
|---|---|---|
| Bahasa | Rust + TypeScript | Python |
| Lisensi | GPL-3 | MIT |
| Cara "belajar" | Memori lokal + Memory Tree di SQLite | Skill yang menumpuk (compounding skills) |
| Fokus | Desktop app, integrasi OAuth | CLI, orkestrasi multi-agent |

OpenHuman menumpuk **konteks** tentang kamu; Hermes menumpuk **prosedur** dari pekerjaan yang sudah selesai. Dua-duanya sah, dan bisa dikombinasikan.

## Yang Bisa Kamu Tiru Minggu Ini

Kalau kamu sedang membangun agent, tiga keputusan OpenHuman ini bisa diadopsi tanpa pindah platform:

- **Simpan memori sebagai file yang bisa dibaca manusia.** Markdown + SQLite cukup untuk sebagian besar kasus.
- **Kompres output tool sebelum masuk prompt.** Targetkan penghematan puluhan persen, bukan nol.
- **Bikin run-nya bisa di-replay dan biaya per panggilan terlihat.** Kamu tidak bisa memperbaiki yang tidak bisa kamu lihat.

Bintang di GitHub tidak akan menyelamatkan arsitektur yang berantakan — tapi tiga hal di atas akan menghemat tagihanmu bulan depan.

Sudah coba pola memori seperti ini di proyek sendiri? Ceritakan di komentar, kami senang diuji balik.

— Chokdi 🐷 · Content Studio · 2026
