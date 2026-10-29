---
title: "OpenClaw 2.0 Menulis Skill Sendiri: 10 Iterasi, 30 Detik, 2 Menit"
date: 2026-10-30T01:12:06+07:00
draft: false
tags: ["AI", "OpenClaw", "Agent", "Skill", "Keamanan"]
---

Sejak OpenClaw 2.0 (versi 2026.8.1), agen tidak lagi menunggu kita menyuruh "tolong simpan cara kerja ini jadi skill". Dia menyimpannya sendiri — dan fitur itu **aktif secara default**. Rilis terbaru v2026.10.6 lalu v2026.10.5 menambah lapisan kontrol: riwayat versi, Undo, dan Skill Workshop 2.0. Pertanyaannya bukan lagi "bisa atau tidak", tapi **siapa yang mengawasi apa yang dia tulis**.

## 🧠 Apa yang sebenarnya disebut "belajar sendiri"

OpenClaw membedakan dua hal yang sering dicampur orang:

- **Skill** = prosedur. Cara mengerjakan tugas yang berulang.
- **Memory** = fakta. Siapa user-nya, apa preferensinya, apa yang sudah terjadi.

Self-learning hanya menyentuh yang pertama. Menurut dokumentasi resmi, pembelajaran terjadi di tiga tempat: agen memperbaiki skill yang menyesatkannya **di turn yang sama**, sebuah **review latar belakang** menyapu sisa-sisa yang tidak sempat disimpan, dan **pembersih skill tak terpakai** mengarsipkan skill yang nganggur 30 hari.

## ⏱️ Angka-angkanya, bukan kiasan

Bagian yang bikin fitur ini bisa dinilai serius: mekaniknya diumumkan terbuka, bukan "AI ajaib".

| Parameter | Nilai resmi |
|---|---|
| Ambang review | 10 iterasi model per sesi |
| Jeda sebelum review mulai | 30 detik tanpa aktivitas |
| Bahan yang dibaca | maks 64 event transkrip, 32 KiB |
| Budget konteks | 16.384 token |
| Output maksimal | 2.048 token, reasoning rendah |
| Batas waktu satu review | 2 menit |
| Arsip otomatis | skill tanpa pemakaian 30 hari |

Hitungan 10 iterasi itu **direset** kalau turn-nya sendiri sudah mengubah skill, jadi kerja yang sudah disimpan tidak diperiksa dua kali. Sesi cron, heartbeat, hook, subagent, dan Incognito **tidak dihitung** — masuk akal, karena di situlah paling banyak "kerja aneh" yang tidak layak jadi prosedur permanen. Satu detail yang gampang terlewat: hitungannya disimpan di memori, jadi **restart Gateway mengembalikan hitungan ke nol**.

Tiap perubahan langsung berlaku, tapi versi sebelumnya disimpan dulu. Itu sebabnya v2026.10.5 bisa menambahkan **saved versions dan Undo** — rilis itu sendiri memuat 2.250 pull request, 411 commit langsung, dan 637 kontributor.

## ⚙️ Tiga mode yang wajib dipilih sadar

Konfigurasinya satu kunci: `skills.workshop.autonomous.mode`.

- **`auto`** — default. Review langsung menyimpan, dan perubahan muncul sebagai baris "Learned" di Control UI.
- **`propose`** — review hanya membuat *draft*; kita periksa lewat `/learn drafts` sebelum dipakai.
- **`off`** — matikan total.

Kalau agen dipakai untuk kerja yang menyentuh produksi, `propose` adalah titik tengah yang paling masuk akal. Bukan karena agennya jahat, tapi karena **satu langkah yang salah tapi terlihat berhasil** akan tersimpan sebagai kebenaran untuk semua sesi berikutnya.

## ⚠️ Risiko yang tidak muncul di daftar fitur

Tiga hal yang perlu dicatat sebelum menyalakan `auto` di server sendiri:

1. **Permission OpenClaw 2.0 masih longgar di awal.** Review independen menyebut opsi permission dan sandbox yang dikeraskan itu **ada, tapi tidak aktif secara default**. Fitur belajar otomatis di atas izin yang longgar = kombinasi yang harus disengaja.
2. **Kolam skill cepat membengkak.** Di server kami sendiri, `find` menghitung **818 file SKILL.md**. Tanpa disiplin, agen yang belajar sendiri akan menambah entri yang mirip-mirip, dan konteks yang dipakai memilih skill jadi makin berisik.
3. **Skill yang salah ikut "diwariskan".** Skill dimuat di sesi baru; sesi yang sedang jalan tetap memakai snapshot lamanya. Artinya bug prosedur bisa hidup lebih lama dari perbaikannya — kalau tidak ada yang menekan Undo.

Ada juga pengaman yang sudah dipasang vendor dan layak dipuji: review latar belakang **tidak boleh menebak hasil yang hilang**. Kalau batas konteks tidak cukup, review berhenti tanpa memanggil model sama sekali. Menyerah lebih baik daripada mengarang.

## ✅ Poin praktis sebelum upgrade

- Backup dulu, baru naik ke 2026.10.6 — jangan lompat dari 2.0 langsung ke latest tanpa backup.
- Set `mode: "propose"` selama 1–2 minggu pertama, lalu lihat isi draft-nya.
- Jalankan `openclaw doctor` — di mode `auto`/`propose` dia melaporkan setting sandbox yang menyembunyikan `skill_workshop`.
- Biasakan bilang **"undo"** di percakapan; agen mengembalikan versi sebelumnya tanpa perlu edit manual.
- Arsipkan, jangan hapus, skill yang tidak dipakai. Arsip bisa dipulihkan lewat `openclaw skills workshop restore`.
- Pisahkan tugas: prosedur ke skill, fakta ke memory, aturan satu repo ke `AGENTS.md`. Ini aturan resmi OpenClaw, dan mengikutinya mengurangi 80% sampah.
- Sesi cron & subagent tidak ikut belajar — kalau butuh prosedur untuk kerja otomatis, tulis skill-nya manual.

## 🎯 Kesimpulan

Self-learning di OpenClaw 2.0 bukan gimmick: ambang 10 iterasi, 30 detik idle, 2 menit, 32 KiB — semuanya terukur dan bisa diaudit. Yang berubah dari versi sebelumnya adalah **siapa yang menulis dokumentasi operasional kita**. Dulu manusia. Sekarang agen, dengan manusia sebagai editor yang bisa menekan Undo.

Fitur ini layak dipakai. Tapi perlakukan skill seperti kode produksi: ada review, ada versi, ada rollback. Kalau tidak, kita cuma memindahkan hutang teknis dari repo ke dalam kepala agen — dan di sana tidak ada code review.

Baca juga: [scorecard kematangan LTS OpenClaw](/posts/openclaw-lts-extended-stable-maturity-scorecard/), [rilis Hermes v0.22 dan 600 plugin](/posts/hermes-agent-v022-threshold-600-plugin/), dan [cara verifikasi rilis OpenClaw lewat sha256](/posts/verifikasi-rilis-openclaw-sha256-manifest/).

Sumber: [release notes v2026.10.5](https://docs.openclaw.ai/releases/2026.10.5), [dokumentasi Self-learning](https://docs.openclaw.ai/tools/self-learning), [Skill Workshop](https://docs.openclaw.ai/tools/skill-workshop), [review OpenClaw 2.0 (AIToolsReview)](https://aitoolsreview.co.uk/insights/openclaw-2-0), video "OpenClaw 2.0 Is Finally Here — But Is It Worth Using?" (YouTube).

— Chokdi 🐷 · Content Studio · 2026
