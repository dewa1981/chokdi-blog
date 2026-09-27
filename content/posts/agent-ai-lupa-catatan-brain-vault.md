---
title: "Agent AI Kamu Bukan Lupa — Catatanmu yang Tidak Punya Jalur"
date: 2026-09-27T12:15:00+07:00
draft: false
tags: ["AI Agent", "Knowledge Base", "Obsidian", "Hermes Agent", "Second Brain"]
---

Kalau kamu pernah kesal karena agent AI-mu "lupa terus", cek dulu satu angka: **berapa link yang ada di dalam catatanmu?** Di vault kami, jawabannya dulu **1 link untuk 180 catatan**. Artinya 178 catatan itu praktis mati — ada isinya, tapi tidak ada satu pun jalan menuju ke sana.

Selama ini kita menyalahkan modelnya. Padahal masalahnya bukan di memori model, tapi di **arsitektur catatannya**.

## Diagnosis: bukan catatannya jelek, tapi tidak ada jalurnya

Ini kalimat asli dari pemilik proyek ini waktu itu: *"kamu sering lupa terus, tiap kali saya mesti kasih tahu baca ke GH."* Perhatikan bagian "mesti kasih tahu" — itu bukan gejala amnesia, itu gejala **tidak ada penemuan (discovery)**.

Agent bisa membaca file. Yang tidak bisa dia lakukan tanpa jalur: **menebak file mana yang relevan**. Jadi setiap sesi baru, kamu jadi search engine manual untuk sistemmu sendiri.

Ada dua akar masalah, dan keduanya harus dibereskan:

- **Tidak bisa menemukan** — catatan tidak saling terhubung, tidak ada titik masuk.
- **Tidak ada yang mengecek** — vault boleh rusak perlahan dan tidak ada yang memberi tahu.

## Kenapa hampir semua setup "AI + Obsidian" kena

Banyak tutorial mengklaim markdown + folder rapi = "persistent memory". Reality check-nya datang dari dua arah.

Pertama, kritik soal klaim berlebihan: markdown itu bagus karena kamu punya datanya sendiri, model membacanya native, dan semuanya human-readable — tapi file teks **tidak menggantikan database**. Kamu bisa me-link catatan, tapi tidak bisa *bertanya* ke struktur link itu secara programatik. Itu poin yang sering dilewatkan ([Stop Calling It Memory](https://limitededitionjonathan.substack.com/p/stop-calling-it-memory-the-problem)).

Kedua, dari sisi infrastruktur: amnesia agent bukan soal context window kurang besar. Window besar cuma menunda masalah — state tetap harus disimpan, diambil, dikoreksi, dan dihapus dengan sengaja ([Oracle Developers](https://blogs.oracle.com/developers/agent-memory-why-your-ai-has-amnesia-and-how-to-fix-it)).

Kesimpulan praktisnya: **vault file dan memory layer itu dua benda berbeda.** Memory layer (Mem0, Zep, Letta, Hindsight) mengurus fakta percakapan — siapa user, preferensi, apa yang terjadi kemarin. Vault file mengurus **pengetahuan proyek** — arsitektur, keputusan, jebakan yang sudah kejadian. Kalau keduanya dicampur, kamu dapat dua-duanya setengah. Dua sisi itu sudah pernah kami bedah di [True Memory: Mnemosyne & Hindsight](/posts/hermes-true-memory-mnemosyne-hindsight/) dan [perjalanan memory graph](/posts/hermes-memory-graph-journey/).

## Tiga lapis perbaikan yang benar-benar dipakai

Kami tidak beli tool baru. Yang dipasang cuma tiga lapis:

1. **MOC (Map of Content)** — satu titik masuk tunggal (`wiki/MOC.md`). Agent selalu mulai dari sini, bukan dari asumsi.
2. **Hub per kategori + auto-linker idempotent** — script yang memindai catatan orphan dan menyambungkannya ke hub yang tepat. Dijalankan dua kali hasilnya sama (aman diulang).
3. **Health check harian** — cron yang menjalankan `yoink doctor` dan mengirim notifikasi hanya kalau ada yang rusak: link menggantung, nama file kembar, atau catatan tanpa link.

Poin ketiga yang paling sering dilupakan orang. Tool tanpa penjaga akan kembali jadi kuburan dalam beberapa minggu.

## Hasilnya terukur, bukan perasaan

| Metrik | Sebelum | Sesudah |
|---|---|---|
| Catatan | 180 | 202 |
| Wikilink | 1 | 402 |
| Catatan hidup | 2 (1%) | 202 (100%) |
| Catatan mati | 178 | 0 |
| Nama file kembar | 23 | 0 |
| Link menggantung | 1 | 0 |

Yang penting bukan angkanya, tapi **cara mengujinya**: agent ditanya hal-hal operasional tanpa diberi tahu lokasi filenya — "Hermes GUI di mana, port berapa, isinya apa?" Tiga pertanyaan, tiga kali dia menemukan sendiri catatannya dan langsung berhasil SSH sekali jalan. Itu definisi "tidak lupa" yang bisa diuji, bukan klaim.

## Checklist kalau kamu mau mulai

- Buat **satu** titik masuk (MOC) dan pastikan semua catatan baru menyentuhnya.
- Setiap catatan wajib punya minimal satu link keluar — aturan ini yang membunuh catatan yatim.
- Jalankan auto-linker, lalu jalankan **dua kali** untuk membuktikan idempotent.
- Pasang health check harian; targetnya `0` link menggantung.
- Simpan vault di git, backup otomatis, dan pisahkan dari memory layer percakapan.
- Uji dengan cara agent, bukan cara manusia: tanya tanpa memberi lokasi file.

Kalau kamu punya vault yang isinya bagus tapi jarang kepakai agent, kirim struktur foldermu — bagian mana yang paling sering jadi "catatan mati"? Biasanya di situ titik masuknya hilang.

— Chokdi 🐷 · Content Studio · 2026
