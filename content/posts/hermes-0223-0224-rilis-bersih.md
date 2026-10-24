---
title: "Versi 0.22.3 dan 0.22.4 Cuma Nambah 4,3 MB — tapi Hapus 20 Ribu Baris Kode: Bedah Rilis Hermes 3 Minggu Terakhir"
date: 2026-10-24T09:15:00+07:00
draft: false
tags: ["Hermes", "AI Agent", "Open Source", "Rilis", "DevOps"]
---

Tiga minggu terakhir ini Hermes Agent merilis **tujuh versi** — dari v0.21.6 (8 Oktober) sampai v0.22.4 (21 Oktober). Bagi yang cuma lihat nomor versi, kelihatannya rilis kecil-kecil saja. Padahal di dalam jendela itu ada satu rilis raksasa (v0.22.0, 24.200 commit) dan satu patch yang **isinya lebih banyak penghapusan daripada penambahan**.

Artikel ini membedah angkanya, bukan cuma fiturnya — karena cara Hermes merilis sekarang justru berubah, dan itu yang paling berpengaruh ke siapa pun yang menjalankan agen ini di VPS 24 jam.

## 📊 Tujuh rilis dalam tiga minggu: angkanya

Semua angka di bawah dikutip dari halaman GitHub Releases resmi `NousResearch/hermes-agent`, bukan dari rangkuman pihak ketiga.

| Versi | Tanggal | Isi jendela | Catatan |
|---|---|---|---|
| v0.21.6 | 8 Okt | ~2.100 PR | rilis pertama pipeline stable baru |
| v0.21.7 | 11 Okt | fokus 1 baris | `hermes update` pindah ke release tag |
| v0.22.0 | 13 Okt | 24.200 commit / 6.080 PR | **The Threshold Release**, 7.180 issue ditutup |
| v0.22.1 | 14 Okt | patch kecil | dibangun dari commit yang salah |
| v0.22.2 | 15 Okt | perbaikan gateway | dirilis ulang sebagai "0.22.1 yang seharusnya" |
| v0.22.3 | 21 Okt | 2.911 commit / 620 PR | +360.278 baris, **−64.308 baris** |
| v0.22.4 | 21 Okt | 14 commit / 13 PR | +1.475 baris, **−3.022 baris** |

Dua rilis di tanggal 21 Oktober itu beda karakter total: satu menumpuk fitur setara berbulan kerja, satu lagi kecil dan cuma membereskan desktop. Yang menarik, dua-duanya **sama-sama menghapus jauh lebih banyak daripada biasanya**: v0.22.3 membuang 64 ribu baris, v0.22.4 membuang dua kali lipat baris yang dia tambahkan.

Di rilis 0.22.0 ada satu klaim yang jarang terdengar dari proyek sebesar ini: basis kodenya jadi **sepertiga lebih kecil**. Kode yang lebih kecil berarti lebih sedikit tempat untuk bug bersembunyi — dan itu bukan jargon pemasaran, karena angkanya terlihat langsung di jendela rilis sesudahnya.

## 🚪 Kenapa disebut "The Threshold Release"

Inti v0.22.0 sederhana: **orang baru bisa ngobrol dengan agen tanpa punya API key.** Buka aplikasi desktop di komputer yang belum pernah pakai Hermes, yang muncul bukan layar setting, tapi sesi onboarding singkat yang berjalan di model uji gratis (`nous/welcome`, sekali per user OS). Satu kartu demi satu kartu: nama, warna aksen, layout, aplikasi mana yang mau disambung, plugin mana yang dipasang — lalu tur singkat dan sampai empat tugas pertama yang sudah disiapkan.

Bagi kami yang sudah jalan berbulan-bulan ini bukan fitur yang dipakai sehari-hari, tapi efek sampingnya besar: hambatan masuk untuk staf baru turun drastis. Dulu bikin satu agen baru = urusan config, key, dan terminal. Sekarang onboarding-nya mengurus itu sendiri.

Dua perubahan struktural lain di rilis yang sama:

- **Connectors** — agen bisa bekerja di dalam aplikasi hosted (Linear, Notion) lewat Nous tool gateway; desktop dapat halaman Connectors yang menggabungkan aplikasi hosted + server MCP dalam satu daftar (menggantikan tab MCP).
- **Stable release channel** — instalasi source tidak lagi mengikuti setiap commit di `main`, tapi pindah dari satu tag rilis ke tag berikutnya. Mau tetap di jalur berdarah? `hermes update --set-channel main`.

## 🔁 Satu Baris di v0.21.7 yang Mengubah Segalanya

Ini bagian yang paling relevan buat operator, dan letaknya cuma satu baris di catatan rilis: **"Updates now follow tagged releases."**

Sebelumnya, `hermes update` di instalasi source menarik apa pun yang kebetulan ada di `main`. Antara 24 September dan 8 Oktober, itu berarti **8.867 commit**. Tidak ada yang tahu kode apa yang sedang jalan di server sendiri — apalagi kalau agennya pegang kredensial produksi.

Sekarang setiap rilis lewat CI source, Docker, Nix, paket desktop bertanda tangan, dan uji instal/upgrade di tiap OS sebelum dipublish. Konsekuensi praktisnya: **update jadi lebih jarang tapi lebih bisa dipertanggungjawabkan**, dan rollback ke versi lama diberi label eksplisit serta tidak pernah terjadi tanpa bertanya.

## 🧹 v0.22.3: 620 PR, 326 Issue, dan Nol Catatan Kurasi

v0.22.3 adalah contoh paling jujur dari "rilis jendela": 2.911 commit non-merge, 4.206 file berubah, 620 PR merge, 326 issue ditutup — dan catatan kurasi lengkapnya **sengaja ditahan** sampai v0.23.0.

Yang tetap disebutkan sebagai fitur nyata:

- notifikasi progress MCP bisa mengalir sebagai progress tool langsung;
- layout CLI klasik dirombak (transkrip glyph, status line di bawah composer);
- klien OAuth yang dideklarasikan plugin dan didaftarkan otomatis oleh Hermes;
- `hermes plugins update` menawarkan semua update plugin yang tersedia;
- hook plugin baru `post_compaction`;
- prompt terantre bisa diedit dari Desktop;
- baris hitung mundur `/loop` di CLI dan TUI.

Satu baris di daftar itu yang langsung kami tandai: **"session auto-prune back to opt-in with a one-time prompt when disk runs low"**. Artinya pemangkasan sesi otomatis tidak lagi jalan diam-diam; dia minta izin sekali, dan hanya saat disk menipis.

## 💾 Kenapa Satu Baris Prune Itu Penting

Kami pernah mengukur `state.db` produksi sendiri: **904 MB**, dan setelah diukur tabel per tabel dengan `dbstat`, **67%** isinya adalah index pencarian `messages_fts_trigram`, bukan isi percakapan. Menghapus 23% pesan hanya mengembalikan 9% ruang, sementara index-nya malah membengkak.

Jadi "hapus sesi lama" bukan obat yang manjur seperti yang orang kira. Di server ini `state.db` sekarang 602 MB dengan disk 619 GB terpakai 19% — belum darurat, tapi jelas butuh kebijakan, bukan tombol panik.

Karena itu perubahan perilaku di v0.22.3 masuk akal: pemangkasan otomatis yang agresif tanpa persetujuan adalah cara cepat kehilangan riwayat kerja. Disk yang menipis harus jadi pemicu **pertanyaan** dulu, bukan eksekusi.

## ⚠️ Dua Pelajaran dari v0.22.1–v0.22.2

Ini bagian yang jarang dikutip orang tapi paling berguna buat yang jalan di produksi:

1. **v0.22.1 dibangun dari commit yang salah.** Dia mengirim pekerjaan gateway yang belum dirilis, dan aplikasi Microsoft Store bisa nyangkut di "Connecting." v0.22.2 dirilis keesokan harinya sebagai "0.22.1 yang seharusnya". Nomor versi tidak menjamin isi — makanya `hermes status` dan tag rilis harus dicek, bukan diasumsikan.
2. **Known issue v0.22.2:** sesi yang berjalan di bawah gateway 0.22.1 tidak bisa dihapus di 0.22.2. Dua rilis beruntun, satu jebakan yang menempel. Ini alasan bagus untuk tidak loncat rilis sendiri-sendiri tanpa membaca bagian known issue dulu.

Pelajarannya: **baca catatan patch sebelum update, bukan sesudah masalah muncul.**

## ✅ Poin Praktis Kalau Kamu Juga Jalan di VPS

Kalau kamu (atau stafmu) menjalankan Hermes 24 jam, empat langkah ini yang paling masuk akal dari rentetan rilis di atas:

- **Pakai channel stable, jangan `main`.** `hermes update --set-channel main` cuma untuk yang memang mau jadi korban uji coba. Default sekarang sudah aman.
- **Cek channel & versi sebelum dan sesudah update** — `hermes status` satu layar, cukup untuk jadi bukti kalau ada yang bertanya "versi apa yang jalan?".
- **Ukur `state.db` dari salinan, bukan dari file hidup.** `cp` dulu, baru `sqlite3`; jangan pernah buka DB yang sedang ditulis gateway.
- **Backup config + `.env` sebelum loncat versi.** Rilis besar sering mengubah jalur config; punya satu tar kecil lebih murah daripada satu malam debug.

Untuk tim yang lebih dari satu orang, dua tambahan: onboarding v0.22.0 memotong waktu bikin agen baru, sementara plugin catalog 600 entri yang dipin ke commit ter-audit memperkecil risiko memasang kode sembarangan — asal tetap dibaca izinnya, bukan cuma diklik Install.

## Kesimpulan

Tiga minggu, tujuh rilis, satu rilis raksasa dan satu patch yang menghapus dua kali lebih banyak daripada menambah. Arah Hermes sekarang jelas: **lebih sedikit kejutan, lebih banyak bisa diaudit**. Update pindah ke tag, desktop jadi paket bertanda tangan, plugin dipin ke commit yang sudah di-review, dan pemangkasan sesi minta izin dulu.

Buat kami yang menjalankan agen ini untuk kerja harian, itu kabar bagus — bukan karena fiturnya banyak, tapi karena jumlah hal yang bisa gagal tanpa ketahuan jadi lebih kecil.

Kalau kamu juga jalan di VPS, cerita dong: versi berapa yang sekarang jalan di servermu, dan pernah kejebak loncat rilis? Tulis di kolom komentar atau balas di Telegram — kami baca semua.

Baca juga: [state.db 904 MB: 67% isinya index pencarian](/posts/hermes-state-db-904-mb-index-fts/) dan [plugin catalog Hermes 416 entri](/posts/katalog-plugin-hermes-416-entri/).

Sumber: [Hermes Agent Releases (GitHub)](https://github.com/NousResearch/hermes-agent/releases), [changelog Hermes Agent Oktober 2026](https://www.gradually.ai/en/changelogs/hermes-agent), [tulisan rilis di r/hermesagent](https://www.reddit.com/r/hermesagent/comments/1x5u50y/hermes_agent_v0220_the_threshold_release).

— Chokdi 🐷 · Content Studio · 2026
