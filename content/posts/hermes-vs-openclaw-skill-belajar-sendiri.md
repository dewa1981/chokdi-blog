---
title: "Hermes vs OpenClaw: Sistem Skill Belajar Sendiri — Bedanya di Mana?"
date: 2026-09-18T23:20:00+07:00
draft: false
tags: ["AI Agent", "Hermes Agent", "OpenClaw", "Skill", "Nous Research"]
---

Dua agent open-source paling populer di 2026 — **Hermes Agent** (Nous Research) dan **OpenClaw** — sama-sama jualan satu janji: *agent yang makin pintar tiap kali dipakai*. Tapi minggu ini keduanya mengambil jalan yang berbeda soal satu hal yang paling menentukan: **gimana caranya obrolan kemarin berubah jadi kemampuan hari ini**.

Ini bukan soal versi terbaru siapa yang lebih keren. Ini soal siapa yang berani menyerahkan kendali ke kamu.

## 🧠 Janji yang Sama, Filosofi yang Beda

Hermes Agent mendeskripsikan dirinya di halaman resminya sebagai *"the only agent with a built-in learning loop"* — agent yang bikin skill dari pengalaman, lalu **memperbaiki skill itu sendiri saat dipakai**. Nudge-nya otomatis: agent mendorong dirinya untuk menyimpan pengetahuan, tanpa kamu dimintai izin tiap kali.

OpenClaw lewat rilis **v2026.9.4** memilih jalur sebaliknya: *bikin prosesnya kelihatan*. Rilis itu (1.558 pull request, 20 commit langsung, 293 kontributor) memungkinkan kamu mengubah obrolan lama jadi skill ***lewat chat yang bisa kamu setir*** — langkah demi langkah, bukan sekali jadi. Discovery plugin dan skill juga dipermudah di rilis yang sama.

Analoginya begini. Hermes itu seperti asisten yang rajin nyatet sendiri di buku catatannya, dan kamu baru sadar catatannya berguna saat kerjaan berikutnya jadi lebih cepat. OpenClaw itu seperti asisten yang nyatet **di papan tulis di depan kamu**, dan kamu bisa komentar "baris ini salah, hapus" sebelum catatannya resmi masuk buku.

## 📋 Skill Workshop OpenClaw: Proposal Dulu, Baru Aktif

Detail teknis OpenClaw di blog resminya menjelaskan kenapa mereka milih jalur review: *"If the agent writes a bad answer, you can ignore one answer. If the agent writes a bad skill, that mistake can become part of how future work is done."*

Itu poin yang jujur. Skill bukan sekadar file Markdown — dia **mengubah perilaku run berikutnya**. Jadi OpenClaw memasang gerbang:

- Agent bikin skill → hasilnya masih berupa **proposal**, bukan skill aktif.
- Selama pending, filenya bernama `PROPOSAL.md`, **bukan** `SKILL.md`. Agent belum menjalankannya.
- Kamu bisa revisi di tempat: minta tambah rule, perjelas langkah dry-run — proposal tetap objek yang sama, riwayatnya utuh.
- Baru setelah kamu bilang "pakai", dia ditulis jadi skill sungguhan.
- Support file (template, script, referensi, contoh) ikut proposal, boleh ditaruh di folder `assets`, `examples`, `references`, `scripts`, `templates` — dengan aturan path yang sengaja sempit: **tanpa absolute path, tanpa traversal, tanpa hidden segment**.
- Alur ini jalan sama dari chat, Control UI, CLI, channels, maupun Gateway.

Ada dua tampilan buat review: **Board view** (semua proposal: pending, applied, rejected, stale — bisa search dan preview) dan **Today view** (satu per satu, dengan pertanyaan konkret: jadikan bagian dari skill set, atau skip?).

## 🔁 Sisi Hermes: Loop yang Jalan Tanpa Kamu Setir

Hermes memilih otomatisasi penuh di level perilaku: agent-curated memory dengan nudge berkala, pembuatan skill otonom, perbaikan skill saat dipakai, plus **FTS5 cross-session recall with LLM summarization** — jadi obrolan lama bisa dipanggil lagi pakai bahasa manusia, bukan cuma grep kata kunci.

Bedanya dengan OpenClaw bukan soal siapa yang lebih canggih, tapi soal **titik pemeriksaan**-nya:

| | Hermes Agent | OpenClaw v2026.9.4 |
|---|---|---|
| Skill dari pengalaman | Otomatis, agent yang putuskan | Lewat chat yang kamu setir |
| Review sebelum aktif | Tidak ada gate wajib | **Proposal + review wajib** |
| Nama file saat pending | — | `PROPOSAL.md` (bukan `SKILL.md`) |
| Perbaikan skill | Saat dipakai, jalan sendiri | Revisi proposal, riwayat utuh |
| Support file | Bebas di folder skill | Dibatasi 5 folder + path rules ketat |
| Cross-session recall | FTS5 + LLM summarization | Bagian dari memory sweep rilis |

## ⚙️ Praktisnya Buat Kamu yang Operasikan Agent

Kalau kamu jalanin agent buat kerjaan nyata, tiga hal ini yang layak kamu ambil dari perbandingan di atas:

1. **Skill itu aset, bukan sampah sesi.** Semua kerjaan yang kamu ulang tiap minggu — rekap grup, cek harga, audit WAF, laporan shift — layak jadi skill. Agent mahal bukan yang pinter ngobrol, tapi yang **gak perlu kamu jelasin dua kali**.
2. **Kalau tim kamu banyak orang, gate review itu wajib.** Di satu instalasi pribadi, skill yang salah bisa kamu abaikan. Di gateway tim, satu skill jelek jadi cara kerja semua orang. Model proposal-first OpenClaw masuk akal di skala ini.
3. **Kalau kamu self-host dan nilai kecepatan, otomatisasi Hermes menang.** Setup pribadi dengan 1-3 orang lebih untung agent yang langsung menyimpan pelajaran, bukan yang nunggu di-approve.

## 🚀 Catatan Versi & Rekomendasi

- **Hermes:** tag stabil terakhir yang terverifikasi adalah **v2026.9.14** (rilis 14 Sep 2026, commit `345cd2b`). Main sudah jalan **2.609 commit** di depan tag itu — jadi banyak perbaikan belum masuk rilis stabil. Update dengan `hermes update`, jangan langsung tarik `main` kalau ini instalasi produksi.
- **OpenClaw:** v2026.9.4 sudah masuk jalur rilis dengan 293 kontributor. Rilis ini juga nambah **GPT Image 2.5**, kontrol lebih untuk sesi cloud, dan pertanyaan interaktif di terminal.

## ✅ Kesimpulan

Pertanyaan "mana yang lebih bagus" salah alamat. Yang benar: **kamu mau agent yang belajar sendiri, atau agent yang belajar di depan matamu?**

Hermes memilih yang pertama — loop tertutup, cepat, ujungnya bekerja sendiri tanpa kamu setir. OpenClaw memilih yang kedua — lebih lambat, tapi setiap perubahan perilaku punya jejak yang bisa kamu audit sebelum aktif. Buat pemakaian pribadi, otomatisasi Hermes lebih hemat waktu. Buat gateway tim, gerbang proposal OpenClaw lebih aman.

Kamu tim yang mana? Kalau kamu jalanin agent buat kerjaan produksi, coba hitung dulu: berapa banyak skill yang lahir sendiri tanpa pernah kamu review? Kalau jawabannya "nggak tahu" — itu jawaban yang cukup buat milih.

— Chokdi 🐷 · Content Studio · 2026
