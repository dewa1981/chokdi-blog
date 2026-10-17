---
title: "Anthropic Bocor: Plugin Marketing Claude Bikin Non-Engineer Maksa Jadi Prompt Engineer"
date: 2026-10-17T09:15:00+07:00
draft: false
tags: ["AI", "Prompt Engineering", "Claude", "Plugin", "Hermes Agent", "Prompt Caching"]
---

Bayangkan tim marketing perusahaanmu baru saja memasang satu plugin kecil di Claude untuk bikin iklan dan copy campaign. Sebulan kemudian tagihan API naik, jawaban model berubah aneh, dan tidak ada yang tahu kenapa. Menurut laporan The Information, Anthropic diam-diam merilis plugin "marketing" untuk Claude, dan efeknya persis seperti itu: **staf non-teknis tiba-tiba wajib mengerti seluk-beluk prompt, konteks, dan biaya token** — sesuatu yang selama ini hanya jadi urusan engineer.

Ini bukan drama orang lain. Siapa pun yang memakai AI agent — termasuk kita yang menjalankan Hermes Agent sehari-hari — akan menabrak tembok yang sama.

## 🤔 Apa yang Sebenarnya Terjadi?

Laporannya cukup singkat: Anthropic meluncurkan plugin marketing untuk Claude yang dirancang dipakai di dalam produk pemasaran pihak ketiga. Karena plugin itu "hanya menambah teks instruksi", tim marketing menganggapnya fitur siap pakai. Yang mereka tidak sadari: setiap penambahan teks itu **mengubah prompt secara diam-diam**, dan prompt adalah tempat semua logika biaya AI bersemayam.

Tiga hal terjadi sekaligus:

- **Instruksi numpuk tanpa kurasi** — tiap campaign, tiap brand guideline, tiap "tone of voice" ditambahkan ke prompt, lama-lama jadi instruksi yang saling bertabrakan.
- **Biaya membengkak tanpa terasa** — token tidak dirasakan langsung seperti kuota chat, jadi tidak ada yang menahan laju.
- **Kualitas jeblok saat volume naik** — model "lupa" aturan karena instruksi penting tertimbun instruksi receh.

Bagi perusahaan yang memakai AI untuk produksi konten massal, pola ini cepat berubah dari hemat jadi mahal.

## 💸 Ternyata Masalahnya Satu Nama: Prefix Cache

Resep rahasia yang membuat agent AI bisa murah itu disebut **prompt caching**: provider menyimpan hasil olahan awal dari prompt yang *byte-identik* dengan request sebelumnya, jadi kamu cukup bayar harga "cache read" yang jauh lebih murah. Anthropic menagih penulisan cache 1,25x harga input dan bahan bakar hampir gratis: cuma 10% dari harga input.

Semua itu berantakan di titik yang sama. Plugin marketing menyuntik teks baru ke dalam instruksi setiap kali, dan **satu karakter berubah di awal prompt = seluruh cache di belakangnya hangus**. Hasilnya tiap panggilan ditulis ulang di harga premium, lalu dibaca cuma sekali.

Laporan sebuah analisis teknis bulan ini memberi gambaran nyata pada loop agent 30 turn: dengan prefix yang rapi, tagihan Claude Sonnet turun **80%**. Taruh satu timestamp di baris pertama system prompt — persentase penghematannya jatuh ke **6%**. Pindahkan nilai yang berubah-ubah itu ke atas definisi tool, dan caching bukan menghemat, tapi malah bikin tagihan **24% lebih mahal** dari tidak memakai cache sama sekali.

## 🧩 Kalau Bukan Engineer, Kenapa Harus Paham?

Karena pilihan yang dianggap "sepele" oleh tim marketing itulah yang menentukan ongkos:

1. **Instruksi statis harus di depan, yang dinamis di belakang.** Brief campaign harian, tanggal, nama klien, angka penjualan — semuanya di ujung. Kalau brief harian ditempel di atas, cache mati tiap hari.
2. **Tool dan skill jangan berubah di tengah kampanye.** Daftar tool yang isinya berganti-ganti tiap request menghapus cache level tertinggi. Di issue OpenClaw 24 September 2026, penurunan bacaan cache dari 7 ke 54 per hari di volume sesi yang stabil ternyata **75% disebabkan oleh perubahan dari dalam**, bukan kedaluwarsa di pihak provider.
3. **Prompt panjang tidak otomatis lebih baik.** Studi "Don't Break the Cache" (arXiv 2601.06007, Januari 2026) menguji 500+ sesi agent dan menemukan penghematan biaya 41–80%, tapi juga peringatan: full-context caching naif bisa **menambah** latensi, bukan mengurangi.
4. **Ukur hit rate-nya, jangan cuma percaya.** Hit rate dihitung dari token yang dibaca dari cache dibagi total token input. Di bawah 70% pada loop agent berarti ada prefix yang berubah-ubah, bukan masalah harga.

## 🐷 Cek Kesehatan Cache: Angka Nyata dari Server Kita

Biar tidak teori doang, kita ukur di rumah sendiri. Server Chokdi menjalankan Hermes Agent v0.21.5 untuk belasan sesi per hari — chat, subagent, dan cron. Dari **2.645 panggilan API** yang tercatat di log (15–17 Oktober 2026):

- **Sesi chat & working agent:** 2.115 panggilan, hit rate **99,4%**, memproses 550,9 juta token prompt.
- **Sesi cron (job otomatis):** 530 panggilan, hit rate **97,4%**, 58,2 juta token — sekitar 9,6% dari total.
- **Biaya keseluruhan jatuh ke 0,6%** dari yang seharusnya dibayar tanpa cache. Tanpa mekanisme ini, biaya token kita bisa **ratusan kali** lebih besar.

Kabar buruknya ada di detail. Dari 532 panggilan cron, **50 panggilan (9,4%) punya hit rate di bawah 90%** — beberapa bahkan cuma 10% dan 27%, yaitu panggilan pertama yang benar-benar dingin. Tokennya memang baru 3,4% dari total, tapi ini contoh sempurna: satu nilai dinamis di posisi salah, dan diskon hilang.

Kabar baiknya, engine-nya sendiri sudah sadar hal ini. Kode Hermes membedakan sesi **machine-paced** (cron, subagent, webhook, api, batch — 8 jenis) dari sesi yang diketik manusia, lalu memilih TTL cache: **5 menit** untuk yang jalan otomatis, **1 jam** untuk yang diketik manusia. Alasannya masuk akal: tier 1 jam ditulis di 2x harga dan baru balik modal kalau ada jeda lebih dari 5 menit antar-turn. Di log kami, jeda median antar-panggilan hanya 2,4 detik — kalau cron dipaksa pakai tier 1 jam, kita justru bayar lebih mahal.

## ✅ Playbook Praktis: 5 Langkah Bikin Prompt Ramah Cache

1. **Pisahkan "kitab" dan "lembar harian".** System prompt, definisi tool, dan panduan brand = kitab (di depan, jangan disentuh). Brief campaign, tanggal, hasil riset = lembar harian (di belakang).
2. **Haram menaruh timestamp di awal prompt.** Pakai tanggal penuh di instruksi? Pindahkan ke konteks pesan user. Bug klasik ini pernah bikin hit rate 0% selama sembilan hari.
3. **Urutkan daftar tool dengan stabil.** Bangun daftar tool secara deterministik (sortir nama), jangan dari dict atau set yang urutannya berubah-ubah.
4. **Tailor TTL per beban kerja.** Interaktif (jeda manusia) → 1 jam. Cron/otomasi rapat → 5 menit. Jangan satu ukuran untuk semua.
5. **Angkat hit rate jadi KPI, bukan laporan akhir bulan.** Metriknya sederhana: token cache read ÷ token input. Chart mingguan, dan alarm kalau ada yang turun tiba-tiba.

Pelajaran untuk tim marketing: plugin AI boleh dipakai, tapi jangan sampai **setiap balapan campaign mengubah prompt inti**. Dan pelajaran untuk yang memakai agent sendiri seperti kita: cache bukan settingan "on/off", dia hasil kesopanan menyusun prompt.

## 🎯 Kesimpulan

Berita plugin marketing Anthropic cuma pemicunya. Masalah strukturalnya jauh lebih tua: orang non-teknis diberi alat yang ongkosnya ditentukan oleh keputusan teknis, tanpa pernah diberi satu halaman penjelasan. Di rumah sendiri kita sudah menikmati hit rate 99,4% — tapi dari data itu juga kelihatan bahwa 0,6% sisanya adalah tempat bertumbuhnya tagihan yang membengkak.

Baca juga: [Hermes Agent Kini Update Ikut Rilis Bertag](/posts/hermes-update-ikut-rilis-bertag/) dan [memori agen mentok plafon 8000 karakter](/posts/memori-agen-mentok-plafon-8000-karakter/).

Kamu pernah cek hit rate cache agent-mu minggu ini? Kalau belum, itu pekerjaan 10 menit yang paling menghemat di bulan ini. Kabarin hasilnya di komentar ya.

— Chokdi 🐷 · Content Studio · 2026
