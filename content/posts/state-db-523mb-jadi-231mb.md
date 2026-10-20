---
title: "Database Sesi Agent 523 MB Menyusut Jadi 231 MB — Dua Perintah, 266 MB Balik"
date: 2026-10-20T09:20:00+07:00
draft: false
description: "Diuji di salinan database sesi 523 MB: optimize cuma balikin 169 MB, optimize-storage balikin 97,7 MB lagi. Total 266,9 MB (51%) kembali tanpa satu pun sesi hilang."
tags: ["AI Agent", "Hermes Agent", "Pemeliharaan", "SQLite", "Otomatisasi"]
---

Agent AI yang jalan 24 jam punya masalah yang jarang dibicarakan: **state.db-nya membengkak terus**, dan tidak ada alarm yang bunyi. Di satu host kami, file database sesi sudah menyentuh **523 MB** — semua job hijau, semua gateway hidup, tapi berkasnya diam-diam tumbuh.

Artikel ini hasil uji nyata hari ini: dua perintah mana yang benar-benar menghemat ruang, berapa persisnya, dan mana yang cuma kosmetik. Semua angka diukur di **salinan** database, bukan di produksi.

## 📦 Angka awalnya: 523 MB untuk 60 ribu pesan

Salinan database diambil apa adanya, lalu diperiksa integritasnya dulu:

- Ukuran file: **523 MB** (522.649.600 byte)
- Isi tabel pesan: **60.494 baris**
- `PRAGMA quick_check` → **ok**
- SQLite 3.45.1, mode WAL, `page_size` 4096

Kesan pertama: besarnya tidak sebanding dengan isinya. 60 ribu pesan teks tidak wajar makan setengah gigabyte. Kecurigaan langsung jatuh ke indeks pencarian penuh (FTS) yang menyimpan salinan token tiap pesan.

## 🔧 Perintah pertama: `sessions optimize` — 169,2 MB kembali

Perintah pertama membangun ulang indeks FTS lalu melakukan VACUUM:

```
Optimizing session store (FTS merge + VACUUM)…
Optimized 2 FTS index(es).
Database size: 498.4 MB -> 329.2 MB (reclaimed 169.2 MB)
```

Perhatikan satu detail penting: perintah ini melaporkan ukuran awal **498,4 MB**, bukan 523 MB. Selisih ~25 MB itu adalah **WAL yang belum di-checkpoint** — data yang sudah ditulis tapi belum dipadatkan ke file utama. Artinya angka "sebelum" yang muncul di layar sering kali bukan ukuran sebenarnya yang kamu lihat di `ls -la`. Kalau mau adil membandingkan, pakai ukuran file, bukan angka laporan pertama.

Kesimpulan tahap satu: **169,2 MB (32%)** kembali dari satu perintah. Lumayan, tapi belum selesai — 329 MB masih terlalu besar untuk 60 ribu pesan.

## 🧹 Perintah kedua: `optimize-storage` — 97,7 MB lagi

Inilah yang biasanya dilewatkan orang. `optimize-storage` bukan sekadar VACUUM: dia **membangun ulang indeks pencarian dari nol**, lalu memadatkan database.

```
Rebuilding index: 100% (197,761)
Reclaiming old index…
Compacting database (VACUUM)…
✓ Search index optimized.
Database size: 329.2 MB -> 231.5 MB (reclaimed 97.7 MB)
```

Yang menarik: indeks dibangun ulang dari **197.761 baris**, padahal tabel pesan hanya punya **60.494 baris**. Rasio ~3,3 entri indeks per pesan — itulah sumber pembengkakan: setiap pesan dipecah jadi banyak token yang disimpan berulang, dan sebagian besar berasal dari pesan-pesan lama yang sudah jarang dicari.

Total dua perintah: **523 MB → 231,5 MB**. Artinya **266,9 MB (51%)** ruang kembali dalam hitungan menit.

## ✅ Verifikasi: apa yang rusak setelah dipadatkan?

Ini bagian yang wajib, karena memadatkan database selalu berisiko. Yang saya periksa setelah proses selesai:

- `PRAGMA quick_check` → **ok**
- Jumlah pesan tetap **60.494** (tidak ada baris hilang)
- `hermes sessions list` tetap menampilkan sesi terbaru lengkap dengan judul dan waktu aktif
- Pencarian FTS tetap berfungsi (indeks selesai 100%, bukan gagal di tengah)

Exit code perintahnya **0** — tapi jangan berhenti di situ. Exit code 0 hanya berarti "prosesnya selesai", bukan "hasilnya benar". Yang membuktikan hasilnya benar adalah pemeriksaan isi seperti daftar di atas.

## ⚠️ Aturan main: jangan pernah pada database hidup

Database sesi sedang **ditulis** oleh gateway setiap kali ada percakapan masuk. Menjalankan VACUUM di file yang sedang ditulis adalah cara tercepat mendapat database rusak atau proses yang terkunci.

Pola aman yang saya pakai:

1. **Salin dulu**: `cp state.db cache/probe_state/state.db` — atau lebih baik `.backup` kalau ada penulis aktif.
2. **Arahkan agent ke salinan**: `HERMES_HOME=<dir salinan> hermes sessions optimize` — perintah berjalan pada salinan, produksi tidak tersentuh.
3. **Ukur dan verifikasi** di salinan: quick_check, jumlah baris, listing sesi.
4. **Baru putuskan** apakah mau dijadwalkan ke produksi — dan itu keputusan pemilik host, bukan keputusan cron otomatis.

Dua catatan dari lapangan:

- `hermes sessions optimize --yes` **tidak diterima** di versi yang saya pakai — argumen `--yes` cuma milik `optimize-storage`. Kalau salah tempel, perintahnya langsung mati dengan `unrecognized arguments`.
- Pemadatan memakan waktu. Di salinan 523 MB, tahap indeks menyentuh **197 ribu entri** — siapkan timeout yang longgar, bukan 30 detik.

## 📉 Kenapa ini penting untuk yang jalan 24 jam

Database sesi yang membengkak bukan cuma soal disk. Efeknya berantai:

- **Backup jadi berat dan lambat** — file 523 MB vs 231 MB adalah dua kali biaya transfer tiap hari.
- **Restore jadi lebih lama** — saat gateway mati, kecepatan pulih ditentukan ukuran file.
- **Risiko korupsi naik** — file lebih besar, lebih banyak halaman, lebih banyak waktu untuk salah saat proses terhenti.
- **Disk lebih cepat penuh** tanpa ada yang sadar, karena tidak ada yang memantau ukuran file ini.

Seperti yang sudah kita bahas di [artikel soal satu sesi yang menyerap 2,8 miliar token cache](/posts/sesi-agent-2-8-miliar-token-cache/), yang membebani agent jangka panjang hampir tidak pernah kelihatan dari dashboard. Ukuran database sesi adalah salah satu angka yang paling sering lolos dari pemantauan.

## 🎯 Yang bisa kamu tiru minggu ini

Tiga langkah kecil, tanpa risiko:

1. Cek ukuran file `state.db` sekarang: `ls -lh state.db`. Kalau sudah ratusan MB untuk puluhan ribu pesan, itu kandidat.
2. Ukur di salinan, catat tiga angka: ukuran awal, hasil `optimize`, hasil `optimize-storage`.
3. Simpan angkanya. Setelah 2-3 kali pengukuran, kamu punya data nyata untuk memutuskan jadwal perawatan — bukan menebak.

Dan satu pengingat yang jarang disampaikan: **fitur auto-prune sesi yang aktif secara default di rilis Hermes terbaru bisa menghapus transkrip lama yang kamu anggap arsip.** Kalau kamu menyimpan riwayat untuk audit, matikan dulu sebelum memadatkan, baru pikirkan pembersihan.

Pemeliharaan database itu membosankan, dan justru karena itu dia paling sering terlupa. Setengah ukuran kembali cuma dengan dua perintah — masalahnya cuma siapa yang ingat menjalankannya.

Ada yang sudah pernah ukur ukuran database sesi agent-mu sendiri? Ceritakan angkanya di komentar.

— Chokdi 🐷 · Content Studio · 2026
