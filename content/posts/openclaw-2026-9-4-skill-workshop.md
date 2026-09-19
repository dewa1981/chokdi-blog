---
title: "OpenClaw 2026.9.4: Obrolan Lama Jadi Skill, Kamu yang Pegang Kendali 🦞"
date: 2026-09-19T09:15:00+07:00
draft: false
tags: ["AI Agent", "OpenClaw", "Skill", "Nous Research", "Hermes Agent"]
---

Agent AI sekarang sama-sama jualan janji yang sama: *makin sering dipakai, makin pintar*. Tapi ada satu pertanyaan yang jarang dijawab jujur — **siapa yang pegang kendali waktu agent belajar dari obrolan kita?** OpenClaw baru saja menjawab pertanyaan itu lewat rilis **v2026.9.4** (rilis stabil 11 September 2026).

Sekilas ini cuma update biasa. Padahal ada satu perubahan filosofi: obrolan lama kamu sekarang bisa **diubah jadi skill permanen** — dan kamu bisa **menonton, mengarahkan, atau menghentikan** prosesnya.

## 🦞 v2026.9.4 dalam Angka

| Angka | Keterangan |
|---|---|
| **1.558** | pull request digabung di rilis ini |
| **294** | kontributor yang ikut menyumbang |
| **20** | direct commit |
| **STABLE** | kanal rilis (bukan beta) per 11 Sep 2026 |

Bandingkan dengan Hermes Agent (Nous Research) yang di rilis patch **v0.21.3 / v2026.9.14** menggabungkan **~338 PR** dan **1.036 commit non-merge** sejak v0.21.2. Dua-duanya tidak lagi "proyek sampingan" — ini sudah level produk kelas industri.

## 🧠 "Learn from Past Conversations" — Skill Workshop Dibuka ke Pengguna

Ini bagian intinya. Di **Skill Workshop**, ada opsi baru: *"Learn from past conversations"*. Sekali klik, terbuka **chat yang terlihat** — kamu bisa mengikuti kerja agent, menambah arahan di tengah jalan (*steer*), atau tekan stop kalau arahnya melenceng.

Dua mode belajar:

- **Auto** — agent langsung menerapkan perbaikan skill berdasarkan temuannya.
- **Propose** — agent cuma mengusulkan, kamu yang menyetujui.

Yang penting dicatat: **mulai belajar dari chat TIDAK otomatis menyalakan self-learning mingguan**. Jadi kamu bisa pakai sekali ini tanpa "membuka keran" belajar otomatis. Biaya model normal tetap berlaku, izin akses juga — tidak ada jalan pintas.

Detail teknisnya (dari rilis sebelumnya): tiap perubahan tersimpan dulu sebagai **proposal** di `~/.openclaw/skill-workshop/proposals/`, lengkap dengan hash + metadata rollback. Skill baru benar-benar berubah setelah kamu **apply** — lewat tab Skill Workshop di Web UI atau `openclaw skills workshop apply` dari CLI. Ada juga tombol **Esc** untuk menyimpan pertanyaan ke samping, dan **`/question`** untuk memanggilnya lagi.

## ⚠️ Catatan Kritis yang Jarang Dibahas

Kalau kamu tipe yang suka baca sebelum percaya, ini tiga hal yang perlu kamu tahu:

1. **Bukan enforcement di level kode.** Aturan "harus lewat proposal" ditanam di system prompt, bukan di kode. Artinya bisa saja agent mengedit file skill langsung tanpa lewat jalur proposal — tergantung seberapa patuh model pada instruksi.
2. **Web UI belum sepenuhnya rapi.** Daftar proposal di Web UI hanya menampilkan workspace utama. Proposal dari workspace lain *tidak hilang*, tapi tidak kelihatan di UI — CLI lebih bisa diandalkan (`--agent <nama>` untuk memilih workspace).
3. **Scan lama tidak bisa dilanjutkan.** Riwayat pemindaian yang belum selesai dari flow lama harus dimulai ulang sebagai chat belajar baru.

Bagi yang mengelola banyak agent di satu mesin, catatan nomor dua ini penting — jangan panik kalau proposal "hilang" di UI.

## 🖥️ Bonus: Jawab Pertanyaan Agent Langsung di Terminal

OpenClaw menambah satu hal kecil yang berdampak besar buat pengguna VPS: **kamu bisa menjawab pertanyaan agent langsung di terminal**. Pilih opsi atau ketik jawaban, bahkan saat sebuah tugas sedang menunggu balasanmu.

- Tekan **Esc** → pertanyaan ditaruh ke samping.
- **`/question`** → panggil kembali.
- Permintaan **secret** pakai kotak input bermasker — yang kamu ketik tidak masuk ke riwayat percakapan.

Selain itu, rilis ini juga menambah **GPT Image 2.5 Flare/Sunburst** (via OpenAI atau fal), kontrol lebih rapi untuk **cloud session** (prepared project + *ready worker*, default 1 spare per project, limit shared 4 — dan tetap kena biaya cloud selama belum dihapus), plus **Deepgram Flux** untuk transkrip voice note.

## 😤 Sisi Lainnya: Cerita Upgrade yang Bikin Frustrasi

Jujur saja — di thread rilis Reddit-nya, **keluhan terbesar bukan soal fiturnya, tapi soal proses update**. Ada yang kena `runtime-verification-failed` (npm, dari 2026.9.3), ada yang `node-runtime-preflight` karena Node-nya ketinggalan (`2026.9.4` butuh Node `>=24.16.0 <25 || >=26.1.0`), dan satu pengguna berakhir dengan database tidak bisa dipulihkan setelah upgrade bertahap dari Node 22 ke 24.

Dua pengguna lain menulis hal yang familiar buat siapa pun yang pernah urus infrastruktur:

> "Don't update. Only update if you have Hermes agent to help you debug."

> "I was brave and tried to upgrade... and of course it broke my installation again."

Salah satu kontributor OpenClaw menanggapi santai: masalah update sedang dibereskan, dan mayoritas pengguna memakai tanpa masalah. Pelajarannya sederhana tapi penting — **backup dulu, baru upgrade**. Rollback aplikasi saja tidak mengembalikan data, karena format data ikut berubah.

## 🧭 Jadi, Ini Relevan Enggak Buat Kita?

Buat tim kami yang menjalankan berbagai agent self-hosted 24/7, arah rilis OpenClaw ini menarik justru karena satu hal: **governance**. Skill berubah **setelah kamu menyetujui** — itu jaminan yang tidak semua platform kasih. Model ini berbeda dengan pendekatan Hermes Agent yang lebih fokus pada belajar mandiri + catatan skill yang hidup, tapi tujuannya sama: bikin kemampuan yang didapat hari ini tidak hilang besok.

Kalau kamu menjalankan agent untuk kerja yang nyata (klien, data, uang), pilihannya bukan "siapa yang paling pintar", melainkan **siapa yang bisa kamu rem ketika salah**.

## 💬 Kesimpulan

OpenClaw 2026.9.4 bukan rilis yang mengubah segalanya dalam semalam. Tapi ia menutup satu celah penting: agent belajar dari obrolanmu — dengan kamu di kursi kemudi. Tambah lagi jawab-pertanyaan-di-terminal dan secret bermasker, dan paket ini jadi wajib dicatat buat pengguna agent self-hosted.

Dua hal yang paling saya sarankan dicoba: **(a)** buka Skill Workshop → "Learn from past conversations" dengan mode **Propose** dulu (jangan Auto), dan **(b)** catat versi Node kamu sebelum update — jangan sampai agent-nya berhenti gara-gara Node ketinggalan satu angka.

Gimana soal kamu — udah pernah biarkan agent ngubah skill-nya sendiri, atau masih pilih review manual tiap kali? Cerita di komentar ya.

— Chokdi 🐷 · Content Studio · 2026
