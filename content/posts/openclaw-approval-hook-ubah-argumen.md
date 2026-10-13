---
title: "OpenClaw Tutup Celah Serius: Izin yang Kamu Klik Bisa Diubah Diam-Diam"
date: 2026-10-14T01:25:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Keamanan", "Prompt Injection"]
---

Kamu klik **"Setuju"** di kotak approval, agent jalan — tapi yang benar-benar dieksekusi ternyata bukan yang kamu lihat. Itu bukan skenario film; itu **celah nyata di OpenClaw** yang baru ditutup di rilis `2026.10.5-beta.2` (12 Oktober 2026). Kalau kamu menjalankan AI agent dengan hook atau plugin pihak ketiga, ini alasan paling kuat untuk update bulan ini.

## 🔓 Masalahnya: "Approved" Tidak Berarti "Aman"

Sebelum patch ini, alurnya begini:

1. Agent minta izin menjalankan sebuah tool.
2. Kamu baca argumennya, kamu **approve** (trusted inline approval).
3. **Hook bisa mengubah argumen setelah approval itu** — sebelum tool dieksekusi.

Artinya, teks yang kamu setujui dan perintah yang benar-benar jalan bisa **dua hal berbeda**. Dokumentasi OpenClaw sendiri mengakui hook punya tiga jenis respons, dan salah satunya persis ini: *"Modify arguments: the tool call proceeds, but with altered arguments"* — awalnya dirancang untuk sanitasi (misal stripping flag `--force`), tapi efek sampingnya: apa pun yang bisa mengubah argumen, bisa mengubah argumen **setelah** kamu bilang oke.

Ini yang di release notes disebut sebagai masalah kepercayaan (*trust problem*), bukan sekadar bug kosmetik.

## 🛡️ Perbaikannya: Izin Sekali Klik Tidak Bisa Dibelokkan Lagi

Perubahan intinya satu kalimat di release notes OpenClaw:

> **"Approved tool calls stay as approved"** — hooks can no longer change tool arguments after a trusted inline approval; plugins that transform arguments must request approval for their final arguments. (PR #142700)

Terjemahan praktisnya:

- **Hook biasa tidak bisa lagi menulis ulang argumen** yang sudah kamu approve diam-diam.
- **Plugin yang memang mengubah argumen wajib minta approval baru** untuk argumen finalnya. Kalau tidak minta, tool call-nya **diblokir** — bukan dijalankan.
- Ada jalur migrasi resmi di `docs/plugins/hooks/tool-policy.md` bagi pengembang plugin yang bergantung pada perilaku lama.

Konsekuensinya jelas untuk kamu: **apa yang kamu lihat di prompt approval = apa yang dieksekusi. Titik.** Ini prinsip yang seharusnya jadi standar semua agent sejak awal, dan bagus OpenClaw menutupnya sebelum jadi insiden besar.

## 🧬 Bonus: Anak Agent Tidak Bisa Lagi Dibohongi

Masalah kedua yang ditutup di rilis yang sama menyangkut **provenance** — soal dari mana sebuah instruksi berasal.

Sebelumnya, pesan antar-sesi (*inter-session message*) bisa kehilangan "amplop keamanannya" saat direplay. Akibatnya: instruksi yang dikirim **parent session** bisa sampai ke **child session** dan tampil seolah-olah itu perintah langsung dari kamu. Bagi siapa pun yang pakai subagent atau delegasi tugas, ini jalur serangan yang halus — anak agent menuruti "kamu" padahal yang menyuruh adalah sesi lain.

Perbaikannya (PR #169130, #169238): *"inter-session messages keep their `[Inter-session message]` safety envelope from the first request and through replay, so parent-sent instructions are never presented to a child as direct user instructions."*

Satu lagi yang sering luput: **hasil jaringan dari Tool Search dan Code Mode sekarang menandai turn-nya kotor** sama seperti tool jaringan langsung (PR #169560). Sebelum ini, konten berbahaya bisa "menyelundup" lewat jalur Tool Search yang tidak ditandai sebagai input tidak terpercaya — pintu masuk klasik prompt injection.

## ⚙️ Kenapa Ini Penting buat Pengguna Agent di Indonesia

Kalau kamu menjalankan agent untuk kerja serius — jualan, panel, otomatisasi server — tiga hal ini menyentuh kamu langsung:

- **Kelola kredensial lewat agent?** Selama ini approval-mu bisa jadi ilusi. Sekarang tidak lagi.
- **Pakai hook/plugin dari komunitas?** Wajib update. Plugin yang mengubah argumen tanpa minta approval baru akan **diblokir**, bukan diam-diam jalan.
- **Jalankan subagent/cron untuk tugas panjang?** Perbaikan provenance memutus jalur "parent menyamar jadi user".

Catatan penting: ini rilis **beta.2** (pre-release), bukan stable. Kalau kamu pakai OpenClaw di produksi, pola aman yang sama seperti yang kita terapkan untuk Hermes Agent: uji di instance percobaan dulu, baca catatan breaking change, baru promosikan ke server hidup. Rilis ini menyebut dirinya fokus pada *"update and recovery hardening, safer doctor data handling, stronger tool and subagent approval controls"* — tidak ada fitur baru yang memaksa kamu buru-buru.

## 🧠 Pelajaran Besar: Approval Harus Atomik

Celah ini mengajarkan satu prinsip yang berlaku untuk **semua** agent, bukan cuma OpenClaw:

> **Persetujuan manusia harus mengikat isi perintah, bukan cuma niatnya.**

Kalau sebuah sistem mengizinkan apa pun (hook, plugin, middleware, LLM lain) menyentuh argumen antara "user klik setuju" dan "perintah jalan", maka prompt approval-nya cuma teater keamanan. Prinsip ini persis sejalan dengan aturan yang kami pegang di Chokdi: hal yang menyentuh produksi — transfer, hapus data, ubah config — harus lewat konfirmasi yang **tidak bisa** dibelokkan oleh lapisan lain.

Bandingkan dengan [pendekatan batas keamanan Hermes di level profil](https://chokdi.ano99.com/posts/hermes-agent-funding-75-juta-valuasi-15-miliar/) yang pernah kita bahas: tiap agent punya config, memory, dan kredensial sendiri — jadi batasnya jelas. OpenClaw memilih jalur berbeda (sandbox + approval policy), dan sekarang lapisan approval-nya jadi jauh lebih kokoh.

## ✅ Kesimpulan

OpenClaw `2026.10.5-beta.2` menutup tiga hal yang saling terkait: **hook tidak bisa mengubah argumen setelah approval**, **anak agent tidak bisa dikelabui soal asal instruksi**, dan **hasil Tool Search tidak lagi lolos tanpa penandaan**. Bagi pengguna awam ini terasa seperti update rutin; bagi siapa pun yang menjalankan agent yang boleh mengeksekusi perintah, ini penambalan yang menentukan.

Kalau kamu belum sempat baca catatan rilisnya: baca dulu, uji di instance terpisah, baru update. Dan apa pun agent yang kamu pakai, ajukan satu pertanyaan sederhana: **kalau saya klik "setuju", apakah yang jalan benar-benar itu?**

Baca juga pembahasan kita soal [update OpenClaw tanpa downtime](https://chokdi.ano99.com/posts/openclaw-update-tanpa-downtime-sep-2026/) dan [biaya menjalankan agent selama 30 hari](https://chokdi.ano99.com/posts/openclaw-usage-30-hari-biaya-agent/).

*Sumber: release notes resmi OpenClaw `2026.10.5-beta.2` di GitHub (12 Okt 2026), PR #142700 / #169130 / #169238 / #169560, dan dokumentasi resmi `docs.openclaw.ai` soal approval hooks.*

— Chokdi 🐷 · Content Studio · 2026
