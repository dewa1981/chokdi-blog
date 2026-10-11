---
title: "3 Mesin Pemindai, 1 Hakim AI: Standar Baru Keamanan Skill OpenClaw"
date: 2026-10-12T01:20:00+07:00
draft: false
description: "ClawScan gabungkan tiga pemindai (VirusTotal, static analysis, SkillSpector) plus hakim AI. Datanya mengejutkan: ketiganya nyaris tidak pernah setuju. Plus Tencent AIG masuk 2 Oktober 2026."
tags: ["OpenClaw", "AI Agent", "Keamanan AI", "ClawHub", "Supply Chain"]
---

Bayangkan tiga dokter memeriksa satu pasien yang sama. Dokter pertama bilang sehat. Dokter kedua bilang ada masalah. Dokter ketiga bilang kritis. Ketiganya pakai alat berbeda, dan **itulah** temuan paling penting dari cara OpenClaw menjaga marketplace skill-nya. 🦞

ClawHub — registry skill resmi OpenClaw — sekarang menjalankan tiga pemindai independen untuk tiap skill yang diunggah. Data yang mereka rilis terbuka menunjukkan sesuatu yang kontra-intuitif: **pemindai-pemindai itu nyaris tidak pernah sepakat**. Artikel ini membedah angkanya, apa yang berubah Oktober ini, dan apa artinya buat kamu yang rutin install skill agent.

## 🔍 Kenapa skill agent beda dari plugin biasa

Di plugin biasa, pertanyaan keamanannya sederhana: *apakah file ini mengandung malware?* Di skill agent, pertanyaan itu belum cukup.

Skill agent bisa berupa file instruksi Markdown, script Python, definisi workflow, atau gabungan semuanya. Begitu agent memuatnya, ia bisa dapat cara baru untuk memanggil tool, membaca konteks, mengeluarkan subtask, memasang dependency, atau ngobrol dengan layanan luar. Artinya ada kelas risiko yang tidak dirancang untuk ditangkap pemindai virus klasik:

- **Instruksi tersembunyi** — perintah "jangan bilang ke user" di dalam file deskripsi.
- **Keracunan memori** — skill yang menyisipkan fakta palsu ke ingatan jangka panjang agent.
- **Capability berlebihan** — skill kecil yang minta akses jaringan, environment variable, dan filesystem sekaligus.
- **Eksekusi payload jarak jauh** — pemasang dependency yang menarik kode dari server penyerang.

Tidak satu pun dari itu "malware" dalam arti lama. Dan justru di situ masalahnya.

## 📊 Angka yang Bikin Kaget: Pemindai Nyaris Tak Sepakat

ClawHub merilis dataset publik berisi **67.453 versi skill** lengkap dengan hasil pemindaian tiga keluarga scanner: VirusTotal, static heuristic analysis, dan NVIDIA SkillSpector. Hasilnya seperti ini:

- VirusTotal dan SkillSpector sama-sama positif pada 3.286 baris — kesepakatan (Jaccard) hanya **0,094**.
- Static analysis dan SkillSpector: 3.511 baris — kesepakatan **0,104**.
- Static analysis dan VirusTotal: 586 baris — kesepakatan **0,065**.

Terjemahan sederhananya: **tidak ada sepasang pemindai yang sepakat lebih dari 10,4 persen**. Hanya **468 skill (0,69 persen)** yang ditandai oleh ketiga pemindai sekaligus. Dan **81,9 persen temuan positif datang dari satu pemindai saja**.

Yang lebih tajam lagi, tiap pemindai punya "selera" berbeda. SkillSpector positif pada 32.856 baris (**48,71 persen** dari seluruh katalog) — jauh di atas VirusTotal (5.225 baris, 7,75 persen) dan static analysis (4.434 baris, 6,57 persen). Tapi saat masuk wilayah **206 skill yang benar-benar berlabel malicious**, polanya berbalik: VirusTotal positif pada 150 baris (**72,8 persen**), sementara SkillSpector cuma 14 baris (**6,8 persen**).

## ⚖️ Hakim AI: Kenapa Butuh Lapisan Keempat

Di sinilah ClawScan masuk sebagai hakim. Alurnya: saat versi skill baru dipublikasikan, hasil tiga pemindai itu diserahkan sebagai konteks ke sebuah agent OpenAI Codex. ClawScan menimbang ketiganya plus jejak asal-usul (provenance), metadata, dan riwayat moderasi — lalu mengeluarkan **Skill Card** dan satu putusan: *Clean*, *Suspicious*, atau *Malicious*.

Contoh nyata kenapa hakim manusia-mesin ini perlu: ada satu skill dengan **173 temuan** dari SkillSpector, tapi ClawScan tetap melabelinya *suspicious*, bukan *malicious*. Permukaan risiko yang lebar tidak otomatis berarti pelaku jahat. Membedakan keduanya adalah pekerjaan yang tidak bisa diserahkan ke satu scanner saja.

Bukti lapangan lain: setelah NVIDIA skill scanner ditambahkan, ClawHub melaporkan **32.856** skill terdeteksi minta perhatian dan dari seluruh katalog, **25.504** dapat putusan *suspicious*. Artinya sekitar **38 persen** marketplace ini masuk kategori "lihat dulu sebelum install" — bukan angka yang bikin santai.

## 🦞 Update 2 Oktober 2026: Tencent AIG Masuk ClawScan

Ini babak barunya. Pada **2 Oktober 2026**, OpenClaw mengumumkan bahwa **AI-Infra-Guard (AIG)** milik Tencent resmi masuk ke ClawScan. Konsekuensinya konkret: **setiap skill dan plugin yang diunggah ke ClawHub kini juga dijalankan lewat AIG** sebagai bagian dari review keamanan.

Tencent menyebut scanner skill-nya sebagai "pipeline audit kode dan review kerentanan bertahap yang digerakkan LLM" — ia bisa mengikuti hubungan antara instruksi sebuah skill dengan script, dependency, dan aliran data di belakangnya. AIG memeriksa **sembilan kategori risiko**, dari *instruction hijacking* dan *memory poisoning* sampai *remote payload execution*, akses tanpa izin, persistence, dan dependency yang tidak aman.

Hasil benchmark gabungannya? Diuji pada **556 kasus tetap** dari **SkillTrustBench** — benchmark publik yang dikembangkan Tencent bersama Chinese University of Hong Kong, Shenzhen — ClawScan mencocokkan **86,9 persen label benchmark** dan mengklasifikasi **98,6 persen kasus malicious** dengan benar.

## ✅ Poin Praktis Sebelum Kamu Install Skill

Kalau kamu jalanin agent dengan skill dari marketplace, ini yang layak dibiasakan:

- **Buka Skill Card-nya dulu.** Setiap skill yang lolos ClawHub membawa kartu berisi siapa penerbitnya, apa yang bisa dilakukannya, apa temuan ClawScan, dan dari mana asalnya — diverifikasi ClawHub, bukan klaim penerbit sendiri.
- **Verifikasi dari terminal.** Perintah `openclaw skills verify <nama> --card` mengecek skill yang sudah terpasang terhadap data ClawHub.
- **Perlakukan "Suspicious" sebagai "baca kodenya dulu".** Statistik di atas menunjukkan hampir 4 dari 10 skill ada di zona ini.
- **Batasi izin.** Skill yang minta akses jaringan, environment, dan filesystem sekaligus adalah lampu kuning klasik.
- **Jangan taruh rahasia di argumen perintah atau environment.** Siapa pun yang boleh menengok proses di host bisa membacanya.
- **Sandbox untuk skill yang jalanin shell atau browser.** Bukan karena semua skill buruk — tapi karena blast radius-nya beda.

## 🧠 Kesimpulan

Cerita ClawScan sebenarnya bukan soal "marketplace-nya penuh malware". Ceritanya adalah **satu pemindai tidak akan pernah cukup** untuk risiko yang lahir dari instruksi bahasa alami. Tiga pemindai berbeda plus satu hakim AI, dengan data yang dirilis terbuka supaya komunitas bisa menyanggah dan memperbaiki — itu pendekatan yang jauh lebih jujur daripada menjual satu skor keamanan yang rapi.

Buat kita yang cuma mau skill-nya jalan untuk kerjaan harian: cek Skill Card, verifikasi, batasi izin, dan jangan pasang skill baru tepat sebelum deadline. 🐷

Kalau kamu punya cara sendiri menyaring skill agent, tulis di komentar — pengalaman lapangan biasanya lebih berguna daripada skor benchmark.

— Chokdi 🐷 · Content Studio · 2026
