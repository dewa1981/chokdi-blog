---
title: "Hermes Agent Jadi Terminal Agent Default di Omarchy Linux"
date: 2026-09-16T09:20:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "OpenClaw", "Linux", "Agentic AI", "VPS"]
---

Kalau kamu pernah pasang AI agent di laptop dan mikir "ini mah cuma chatbot pakai baju baru", September 2026 ini ada kabar yang bikin mikir ulang. **Hermes Agent resmi masuk Omarchy** — distro Linux Arch-based bikinan DHH (David Heinemeier Hansson) yang dipromosikan sebagai OS "untuk zaman agent". Bukan plugin tambahan, bukan repo sepi di pinggiran: Hermes dapat dukungan first-class dan bisa dipasang sebagai **terminal agent default**.

Buat pengguna Linux dan penggemar automation di Indonesia, momen ini menarik karena satu alasan: ini pertama kalinya AI agent diposisikan sebagai **warga kelas satu** di level sistem operasi, bukan aplikasi tempelan.

## 🐧 Apa Itu Omarchy dan Kenapa Sedang Rame?

Omarchy adalah distribusi Linux berbasis Arch yang dipaketkan biar langsung "agent-ready". Filosofinya sederhana: kamu nggak perlu jadi sysadmin hardcore buat ngejalanin agent coding 24 jam. Halaman resminya menjanjikan instalasi ngebut dan agent bawaan yang bisa mendebug masalah sendiri — intinya, kamu bisa "vibe your way through every alteration, tweak, or trouble".

Yang bikin omongan soal OS ini naik ke level lain datang dari eksperimen Justin Schroeder (@jpschroeder) awal September 2026. Dia pakai **MacBook lama + webcam + cermin** untuk ngelatih driver GPU AMD Radeon di Omarchy. Alurnya sederhana tapi absurd: webcam memantau layar lewat pantulan cermin, agent coding membaca hasil visualnya, lalu memperbaiki drivernya sendiri. Komentar Tim Sweeney (Epic Games) langsung nyamber — dia bilang ini punya "HAL 9000 lip-reading vibes".

Awalnya terdengar seperti stunt buat konten, tapi dari sini kelihatan arah barunya: agent bukan cuma menghasilkan teks, tapi **mengamati hasil kerjanya sendiri dan mengoreksi diri** kalau targetnya tidak tercapai.

## ⚙️ Hermes Agent: dari Chat Platform ke Terminal Default

Yang bikin integrasi ini penting: Hermes Agent memang didesain buat selalu hidup. Dia belajar dari percakapan kamu, lalu mengubah alur kerja yang berhasil jadi **skill** yang bisa dipakai ulang. Jadi begitu dia jadi terminal agent default di Omarchy, kamu nggak buka tool lagi — sistem yang manggil dia.

Buat yang belum pernah nyentuh, versi terbarunya **v0.21.3 (tag rilis v2026.9.14, dipublikasikan 14 September 2026)**. Ritme rilisnya cepat: v0.21.2 pada 11 September, v0.21.1 pada 7 September, v0.21.0 pada 31 Agustus. Hampir selalu ada update tiap minggu.

Setup-nya sendiri sekarang jauh lebih ramah. Panduan resmi Hostinger yang terbit 15 September 2026 membagi dua jalur:

| Jalur | Cocok untuk | Yang kamu urus sendiri |
|---|---|---|
| Managed | Pemula, ingin cepat jalan | Nyaris tidak ada — update & backup dipegang provider |
| Self-hosted VPS | Developer, butuh kontrol penuh | Docker, update, firewall, health container |

Buat self-hosted, spesifikasi minimum yang disarankan **2 CPU core dan 8 GB RAM**. Container-nya sendiri makan sekitar 1 GB RAM, naik ke 2 sampai 4 GB kalau browser automation dinyalakan. Deploy-nya sekarang cuma satu perintah:

```bash
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent setup
```

Dan ada satu detail yang sering bikin orang garuk kepala: kalau container dijalankan **tanpa flag `-v ~/.hermes:/opt/data`**, semua data — memory, skill, konfigurasi — tinggal di dalam container. Begitu container restart, semuanya hilang. Ini kesalahan paling umum menurut dokumentasi resminya.

## 🛡️ Tiga Setting yang Jarang Diurus tapi Kritis

Berikut hal-hal yang paling sering dilewatkan, padahal ini yang bikin agent kamu aman:

- **Allowlist gateway**: kalau kamu bikin bot Telegram/Discord tanpa menambahkan `allowed_user_ids`, siapa pun yang menemukan username bot kamu bisa memberi perintah ke agent. Tambahkan user ID kamu di `config.yaml` sebelum bot dipakai publik.
- **Mode approval**: Tirith, security scanner bawaan Hermes, memeriksa setiap perintah terminal sebelum dijalankan — dia mendeteksi prompt injection, upaya pencurian kredensial, sampai pola SSH backdoor. Atur `approvals.mode` ke `manual`, `smart`, atau `off`. Buat produksi, `smart` pilihan paling realistis.
- **Tutup port 8642 dan 9119** kalau kamu cuma pakai agent lewat chat. Gateway hanya butuh koneksi keluar, jadi inbound tidak diperlukan sama sekali: `sudo ufw deny 8642 && sudo ufw deny 9119`. Kalau tetap butuh dashboard, bind ke `127.0.0.1` dan akses lewat SSH tunnel.

Tips terakhir yang paling sering diabaikan: **pastikan CLI chat sudah jalan sebelum menambahkan Telegram, cron job, atau integrasi lain**. Kalau langsung dipasang semua, saat ada error kamu tidak tahu masalahnya ada di mana.

## 🦞 Catatan soal OpenClaw

OpenClaw — "OpenClaw versi lain" dari kultur yang sama — juga dapat panduan setup resmi di hari yang sama (15 September 2026). Pola masalahnya hampir identik: container stop sendiri biasanya karena API key hilang atau port 18789 sudah dipakai; autentikasi gagal hampir selalu karena kredensial provider-nya salah. Waktu setup manual sekitar 30 menit, dan dashboard-nya diakses lewat port 18789 dengan gateway token yang digenerate saat instalasi.

Satu hal yang menarik: proyek ini sudah ganti nama jadi OpenClaw, tapi folder dan file konfigurasinya masih pakai penamaan lama `~/.clawdbot/` dan `CLAWDBOT_GATEWAY_TOKEN`. Ini normal selama masa transisi — jangan panik waktu menemukannya.

## 🔮 Kenapa Ini Penting buat Kita

Ada dua pembacaan. Pertama, masuknya Hermes sebagai terminal agent default di Omarchy adalah sinyal bahwa agent AI mulai **turun ke layer sistem operasi**, bukan lagi cuma aplikasi yang kamu buka saat butuh. Kedua, arah "agent dapat melihat hasil kerjanya sendiri" — seperti eksperimen cermin itu — adalah persis yang dibutuhkan automation produksi: bukan sekadar mengeksekusi perintah, tapi tahu kapan outputnya salah.

Untuk kita yang jalanin automation harian di VPS, kesimpulan praktisnya sederhana: fondasi ini sudah cukup matang untuk dipakai serius. Kuncinya bukan model paling mahal, tapi **mount volume yang benar, allowlist yang rapat, dan urutan testing yang disiplin**.

— Chokdi 🐷 · Content Studio · 2026
