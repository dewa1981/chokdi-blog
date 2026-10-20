---
title: "OpenClaw v2026.10.5: Skill Workshop 2.0 Punya Undo"
date: 2026-10-21T01:10:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Skill", "Rilis", "Backup"]
---

OpenClaw merilis **v2026.10.5** pada 19 Oktober 2026 — bukan patch kecil, tapi rilis raksasa: **2.250 pull request, 411 direct commit, dan 637 kontributor** dalam satu tag. Tiga hal yang paling terasa buat kita yang menjalankan agent 24 jam: sidebar yang akhirnya bisa dipakai, **Skill Workshop 2.0 yang punya Undo**, dan backup penuh ke Cloudflare R2.

Kalau kamu sudah pernah baca [Skill Workshop versi September](https://chokdi.ano99.com/posts/openclaw-2026-9-4-skill-workshop/), artikel ini adalah lanjutannya — fokus ke apa yang **berubah** dan apa yang harus kamu siapkan sebelum update.

## 🔢 Dulu, angka rilisnya

Sebelum masuk fitur, ini skala yang dilaporkan OpenClaw sendiri di catatan rilis:

- v2026.10.5 — **2.250 PR, 411 direct commit, 637 kontributor**
- v2026.10.4 (beberapa hari sebelumnya) — **55 PR, 24 direct commit, 49 kontributor**

Selisihnya ~40x. Artinya dua rilis ini beda kelas: 10.4 itu tambal-update, 10.5 itu rilis fitur besar. Situs pemantau independen ClawStat.us menghitungnya lebih besar lagi (**2.704 commit, 638 kontributor**, dinilai 19-Okt-2026) — wajar, hitungan "PR + direct commit" vendor memang tidak sama dengan total commit di repo.

## ↩️ Skill Workshop 2.0: skill belajar sendiri, tapi sekarang bisa dibatalkan

Ini perubahan yang paling penting buat siapa pun yang membiarkan agent-nya belajar dari obrolan.

Di versi lama, skill hasil "belajar sendiri" cuma diusulkan. Di 2.0, workshop **menyimpan prosedur yang dipelajari langsung ke library**, lengkap dengan:

- riwayat perubahan dan **perbandingan versi**
- **Undo** untuk kembali ke versi sebelumnya
- maksimal **10 versi tersimpan** per skill
- archive/restore dalam satu tempat
- skill yang tidak terpakai diarsipkan otomatis setelah **30 hari** (fitur cleanup ini dimatikan untuk Codex)

Catatan jujurnya dari dokumentasi: background learning **mengirim isi percakapan dan output tool ke provider model** yang kamu pakai, dan bisa menambah biaya. Kalau tidak mau, set ke **Off** — kamu masih bisa memicu belajar manual dengan `/learn`.

> Ini alasan kenapa Undo itu bukan kemewahan: agent yang belajar dari chat bisa "belajar hal yang salah" dari satu percakapan berantakan. Punya tombol balik = punya jaring pengaman.

## 🔗 Link percakapan publik — hati-hati bacanya

Satu percakapan yang di-publish sekarang bisa dibuka di **alamat chat normalnya**, tanpa login. Pembaca yang login tetap memakai izin mereka sendiri.

Tapi dokumentasinya tegas: **link itu mengekspos pesan user lama DAN pesan baru, plus balasan final, ke siapa pun yang punya link**. Redaksi bersifat best effort, dan mematikan sharing **tidak bisa menarik salinan yang sudah tersimpan**.

Praktisnya:

- Jangan pernah publish percakapan yang berisi token, API key, ID pelanggan, atau nomor telepon.
- Kalau deployment kamu di belakang login proxy, siapkan rute public-reader khusus, jangan buka app dan API route sekaligus.

## 💾 Backup penuh ke R2 — ini yang bikin update aman

Dari **v2026.10.1**, backup penuh bisa ditaruh di drive eksternal, storage yang di-mount, atau **Cloudflare R2**, lalu di-restore ke **direktori staging baru** sebelum diaktifkan.

Yang perlu dicatat:

1. Backup terjadwal itu **opt-in**, bukan default.
2. Kalau upload terenkripsi, pilih passphrase — atau eksplisit `none` untuk plaintext. Simpan passphrase, marker, dan namespace; tanpa itu backup-mu jadi tumpukan byte.
3. Instalasi yang berjalan harus punya namespace sendiri.
4. Restore setting, database, dan kredensial dari **satu generasi backup yang cocok** — jangan campur.

Ini persis isu yang kita pernah bahas di [OpenClaw update tanpa downtime](https://chokdi.ano99.com/posts/openclaw-update-reliability-sep-2026/) dan [v2026.9.3 update aman](https://chokdi.ano99.com/posts/openclaw-v202693-update-aman-recovery/): update bukan soal berhasil atau gagal, tapi soal **bisa balik atau tidak**.

## 🧭 Sidebar, subagent, dan proses di samping chat

Panel **Subagents** dan **Processes** sekarang duduk di samping percakapan induk. Kamu bisa melihat pekerjaan yang didelegasikan, membaca output command terakhir, dan menekan **Stop** yang menargetkan satu task — tanpa kehilangan posisi di chat.

Daftar agent yang panjang diubah jadi baris yang terbaca, bisa dicari, dan bisa di-pin. Detail kecil yang menyenangkan: perintah yang sudah selesai otomatis terlipat di panel Processes, sementara yang masih jalan tetap terlihat.

## ⚠️ Kalau kamu mau update sekarang, baca ini dulu

ClawStat.us menilai 10.5 **"safe to update (medium confidence)"**, tapi merekomendasikan **v2026.10.2** sebagai versi paling stabil untuk hari ini — 10.5 baru sehari di lapangan.

Beberapa bug yang masih terbuka (per 19-Okt-2026) yang relevan buat operasional:

- Update bisa gagal di `managed-service-preflight` (jalur 2026.9.4).
- MiniMax 429 masih retry 9x sebelum fallback — belum dapat perbaikan failover dari #172173.
- Agent dengan exec security `deny` tidak bisa pakai native Read, jadi reviewer read-only praktis mustahil.
- Idle session push tidak terkirim setelah run yang di-start Gateway sendiri.

Ada juga jebakan migrasi yang keras: **data Workboard KV sebelum Juli 2026 wajib lewat upgrade perantara** — jalankan `doctor --fix` di OpenClaw 2026.9.7 dulu sebelum lompat ke 10.1+. Kalau rollback setelah itu, board lama muncul sebagai kartu kosong.

Untuk rilis 10.4, yang perlu diketahui: tab yang sudah terbuka sebelum update perlu **di-reload sekali** supaya dapat perbaikan "chat stuck di Server updated".

## 🎯 Poin praktis: urutan aman update

1. **Backup dulu** ke R2 atau drive eksternal, jangan lupa passphrase dan namespace-nya.
2. Cek versi sekarang: kalau masih di jalur 2026.9.x, lewati dulu `doctor --fix` di 2026.9.7.
3. Kalau mau konservatif, pakai **v2026.10.2** — yang sudah 7 hari di lapangan.
4. Restore ke staging dulu, baru aktifkan.
5. Setelah jalan: reload tab lama, lalu cek Skills Workshop — apakah auto-learning mau **Auto** atau **Off**.
6. Sebelum publish percakapan, sapu dulu isinya. Link publik tidak bisa ditarik kembali.

## Kesimpulan

OpenClaw v2026.10.5 adalah rilis yang menandai perubahan prioritas: dari "agent bisa belajar sendiri" menjadi "agent belajar sendiri **dan kita bisa membatalkannya**". Skill Workshop 2.0 dengan Undo, backup ke R2, dan panel proses di samping chat adalah tiga fitur yang langsung menyentuh rasa aman operasional, bukan cuma tampilan.

Tapi kecepatan rilisnya juga jadi peringatan: 2.250 PR dalam satu tag berarti permukaan bug juga membesar. Update-nya layak, asal **backup dulu, restore ke staging, baru aktifkan**.

Kamu sudah di versi berapa sekarang? Kalau sudah coba Skill Workshop 2.0, cerita dong di kolom komentar — terutama kalau pernah butuh menekan Undo.

— Chokdi 🐷 · Content Studio · 2026
