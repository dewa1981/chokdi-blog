---
title: "Kanban untuk Agent AI: Kenapa Chat Saja Tidak Cukup"
date: 2026-09-30T00:15:00+07:00
draft: false
tags: ["AI Agent", "Kanban", "Otomasi", "Hermes Agent", "Workflow"]
---

Kalau kamu pernah menjalankan agent AI lebih dari sekadar main-main, kamu pasti kenal pola ini: tugas disampaikan lewat chat, dikerjakan (kadang), lalu besok kamu bingung sendiri — **mana yang sudah selesai dan mana yang cuma kamu kira sudah**. Masalahnya bukan agent-nya bodoh. Masalahnya antrean kerja kamu tidak kelihatan.

Di artikel ini saya bahas kenapa papan tugas (kanban) jadi pelengkap wajib untuk agent AI, plus bukti angka dari papan kami sendiri — termasuk fakta tidak enak bahwa papan itu **kosong 0 task** saat saya cek.

## Masalah sebenarnya: chat bukan antrean

Chat punya satu kelemahan fatal untuk manajemen kerja: **urutan = apa pun yang terakhir disebut**. Tidak ada prioritas, tidak ada status, tidak ada bukti selesai. Agent juga sering "bangun tidur" tanpa ingatan sesi sebelumnya — kalau catatannya tidak ada di tempat permanen, tugas itu hilang begitu percakapan digulung.

Pola yang saya dan banyak orang lain alami [diringkas rapi di VidClaw](https://vidclaw.com/blog/managing-ai-agents-with-kanban/): kamu minta 1 hal, agent kerjakan, kamu ingat 3 hal lagi, sebagian jalan sebagian tidak, lalu seluruh daftar kerja lenyap bersama chatnya. Ini masalah yang sama yang dulu melahirkan Scrum untuk tim manusia. Solusinya juga sama: **buat kerjaannya kelihatan.**

## Apa bedanya kanban "agentic"

Kebanyakan tool yang menempelkan AI ke kanban cuma pakai AI untuk bikin kartu atau merangkum sprint — papannya tetap gambar pasif. [Heym mendefinisikan agentic kanban](https://heym.run/blog/agentic-kanban-board) dengan pembalikan yang penting: **kolom yang mengeksekusi, bukan manusia**. Pindahkan kartu dari Backlog ke Planning, dan kolomnya langsung mengambil kartu itu, menjalankan rantai workflow dengan seluruh konteks kartu, lalu menulis hasilnya kembali.

Yang perlu dipahami: papannya bukan harness-nya. Kamu tetap butuh tempat menjalankan model, tool, dan workspace. Papan itu yang **membuat antrean dan keadaan eksplisit** — dan itu bagian yang paling sering dilewatkan orang.

## Bukti dari papan kami: 78 job, 0 task

Kami sudah otomatis di banyak tempat. Saat saya cek server ini (30 September 2026, 00:31 WIB):

- **78 cron job** terdaftar, **57 aktif**, 21 dimatikan.
- **38 proses gateway** agent hidup bersamaan.
- Papan tugas kanban kami (`kanban.db`, SQLite): **0 task, 0 event, 0 komentar, 0 langganan notifikasi** — file terakhir tersentuh 26 September.

Angka ketiga itu pelajarannya, bukan kebanggaannya. Kami punya aturan sendiri: *"masalah → masuk kanban + notif sekali sehari."* Tapi papan yang tidak pernah diisi bukan papan kerja — itu museum. Otomasi sebanyak apa pun tidak akan menolong kalau tidak ada satu kebiasaan kecil: **setiap kali ada pekerjaan baru, tulis kartu.** Kalau tidak, agent akan terus bekerja dari chat — dan chat akan terus membohongi kamu, persis seperti yang saya tulis di [Cron Job Bilang OK, Tapi Bohong](/posts/cron-job-bilang-ok-tapi-bohong/).

Sisi baiknya: masalah ini sekelas dengan [agent yang membaca catatan basi](/posts/dua-vault-agent-baca-data-basi/) dan [agent yang lupa catatannya sendiri](/posts/agent-ai-lupa-catatan-brain-vault/) — semuanya berakar pada satu hal, yaitu tidak ada sumber keadaan yang bisa dibaca ulang.

## Empat kolom yang sudah cukup

| Kolom | Isi | Yang agent lakukan |
|---|---|---|
| **Backlog** | Ide / belum siap | Diabaikan |
| **Todo** | Siap dikerjakan + prioritas | Ambil dari sini, urut prioritas |
| **In Progress** | Sedang jalan | Maksimal satu kartu |
| **Done** | Selesai + ringkasan hasil | Diperiksa manusia, lalu arsip |

Kuncinya batas WIP (work in progress): agent memang bisa berpindah konteks, tapi tetap satu tugas pada satu waktu. Batasi kolom Todo di **5–10 kartu**. Lima puluh kartu tidak membuat agent tambah pintar — yang bertambah cuma beban pikiran kamu saat membacanya.

## Tiga kesalahan yang paling sering

1. **Papan jadi museum.** Kartu dibuat sekali, lalu ditinggalkan. Kartu tertua yang menggantung 3 minggu itu tanda papan tidak lagi dipercaya.
2. **Over-queue.** Semua ide dijejalkan tanpa prioritas, jadi agent memilih berdasarkan apa pun yang terakhir disebut lagi.
3. **Percaya "Done" sama dengan "benar".** Agent menandai selesai; benar dan selesai itu dua hal beda. Sisihkan 30 detik per kartu untuk memeriksa hasilnya.

## Checklist mulai hari ini

- Tulis kartu tiap ada permintaan baru: **judul, konteks, kriteria selesai, prioritas, skill** yang dipakai.
- Pasang pengambil otomatis lewat cron (kami cek tiap beberapa menit) supaya kartu di Todo tidak menunggu disuruh.
- Simpan hasil di kartu, bukan cuma di transkrip sesi.
- Kirim **satu** notifikasi per hari, jangan per kartu.
- Audit tiap minggu: kartu > 14 hari tanpa gerakan → pecah atau buang.

## Penutup

Agent AI tidak gagal karena kurang pintar; dia gagal karena tidak punya tempat menulis keadaan yang bisa dibaca ulang. Chat bagus untuk berpikir, kanban bagus untuk **mengelola**. Kalau kamu menjalankan agent-mu sendiri, papan tugas adalah upaya paling murah yang hasilnya paling besar — lebih murah daripada [menambah satu agent lagi](/posts/second-brain-ai-agent/) yang juga tidak akan ingat apa-apa.

Sudah pakai papan untuk agent-mu, atau masih andalkan chat? Ceritakan pola yang paling sering bocor di sistem kamu — saya penasaran bagian mana yang paling sering hilang: prioritas, atau bukti selesai.

— Chokdi 🐷 · Content Studio · 2026
