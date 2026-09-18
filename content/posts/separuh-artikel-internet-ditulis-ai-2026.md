---
title: "Separuh Artikel di Internet Sekarang Ditulis AI — Kita Tim yang Mana? 🐷"
date: 2026-09-19T00:10:00+07:00
draft: false
tags: ["AI", "Konten", "Riset", "SEO"]
---

Ada angka yang bikin kami berhenti sebentar waktu baca risetnya: **separuh artikel yang diterbitkan di internet sekarang ditulis AI** — bukan diedit AI, tapi digenerate AI dari nol. Dan yang nulis angka itu bukan orang yang jualan alat deteksi AI. Mereka agensi growth yang hidupnya dari SEO.

Tulisan ini bukan ceramah soal "AI jahat". Kami sendiri jalanin pipeline konten otomatis — artikel ini juga keluar dari proses itu. Justru karena itu kami penasaran: kalau separuh web sekarang suara mesin, bagian mana yang masih dihitung?

## 📊 Angka yang Dilaporkan Graphite

Graphite (agensi growth di balik riset ini) sampel **55.400 artikel** dari Common Crawl — arsip web yang juga dipakai buat latih LLM. Filter ketat: bahasa Inggris, ada schema markup `article`, minimal 100 kata, tanggal publikasi Januari 2020–Maret 2026. Untuk menilai AI atau bukan, mereka pakai **tiga detektor sekaligus**: Pangram, Copyleaks, dan GPTZero, lalu dirata-rata. Bukan satu detektor yang bisa salah arah.

Hasilnya:

| Periode | Artikel primarily AI-generated |
|---------|-------------------------------|
| 12 bulan setelah ChatGPT rilis (Nov 2023) | 35,9% |
| Q1 2025 | 49,6% (48,4% human) |
| Q4 2025 | 50,9% (pertama kali lewat separuh) |
| Q1 2026 | 49,9% |

Artinya sejak awal 2025, **jumlah artikel buatan AI kira-kira sama banyak dengan artikel buatan manusia** — dan angkanya berhenti di situ, tidak terus naik. Lima kuartal terakhir datar di kisaran 50%.

Kenapa plateau? Ini bagian favorit kami. Hipotesis Graphite: **artikel yang murni AI-generated kebanyakan tidak muncul di Google dan tidak dikutip ChatGPT**. Di studi terpisah mereka cek hasil pencarian — artikel yang ditulis AI jarang nongol. Jadi bukan karena orang berhenti pakai AI, tapi karena hasilnya tidak dapat trafik. Yang tidak dapat trafik, ya tidak diproduksi lagi dalam jumlah besar.

Ada catatan metodenya juga, biar jujur: detektor AI bisa salah. Graphite ukur itu duluan — false positive di kisaran 1,36–1,84% (diuji ke 15.700 artikel terbit sebelum ChatGPT, jadi hampir pasti tulisan manusia), dan false negative rata-rata 0,07–1,97% (diuji ke 2.000 artikel buatan GPT-5, Gemini 3.1 Pro, dan Claude Opus 4.6). Jadi angkanya bukan tafsiran liar.

## 🔍 Versi Pew Research: 10% Halaman, 1 dari 3 Halaman Baru

Pew Research Center (20 Agustus 2026) pendekatannya beda: 490.000 halaman berbahasa Inggris dari Common Crawl, dites pakai Open Pangram. Hasil di sampel 10.000 halaman Juli 2026: **10% halaman menunjukkan tanda kuat ditulis AI**.

Kelihatan kecil? Internet penuh halaman lama yang mustahil ditulis AI. Kalau disaring hanya halaman yang terbit **setelah ChatGPT rilis**, angkanya jadi **lebih dari sepertiga**. Dan di domain `.com` sudah 9,35% — dua kali lipat domain `.org` (4,59%), dan sekitar 10x `.edu`/`.gov` (sekitar 1%). Rasionalnya masuk: `.edu` dan `.gov` punya proses review, sementara `.com` dikejar trafik.

Pew juga kasih "sidik jari" bahasa AI, dan ini yang bikin kami ketawa sendiri:

- **Em dash (—)** muncul sekitar **2x lebih sering** dibanding snapshot 2023
- **Oxford comma** naik **63%**

Perhatikan betapa banget kami pakai em dash di artikel ini. Jadi kalau mesin detektor menuduh kami AI: iya, kena. Tapi tuduhannya cuma menebak gaya, bukan isi.

## 🧠 Yang Bikin Tulisan Masih Diperhitungkan

Ada dosen Digital & Data Studies di Binghamton University, Francesco Agniellini, yang nanggapi temuan ini di The Conversation. Dia menarik tulisan Umberto Eco tahun 1960-an soal dua kubu menghadapi media baru: kaum "apokaliptik" yang takut budaya rusak, dan kaum "terintegrasi" yang menganggapnya pembebasan. Kesimpulan Eco: dua-duanya lebay. Yang berguna itu melihat siapa pakai alatnya, untuk apa, dan siapa yang diuntungkan.

Kami setuju, dan dari sisi praktik lapangan ada tiga hal yang bikin konten tetap dihitung — semuanya bukan soal kalimat:

1. **Pengalaman yang tidak ada di data latihan.** Kalau kami nulis "cron ini gagal karena tanggal frontmatter di masa depan bikin Hugo skip build", itu bukan hasil ringkasan artikel orang. Itu dari log yang kami baca sambil ngopi jam 3 pagi.
2. **Angka yang bisa dicek.** Timestamp, status code, biaya token, log deploy. AI gampang bikin angka kelihatan meyakinkan; yang sulit adalah angka yang benar-benar keluar dari terminal.
3. **Sudut pandang.** Mesin bisa meringkas dua sumber. Yang dia tidak bisa: bilang sumbernya lemah, atau memilih berpihak.

## 🎯 Jadi, Buat Kita Artinya Apa?

Internet sekarang bukan lagi lomba siapa bisa memproduksi kalimat tercepat — bagian itu sudah selesai, mesin menang. Yang jadi langka justru sebaliknya: **tulisan yang punya jejak kejadian nyata**.

Buat kami yang jalanin pabrik konten 12 jam sehari, ini kabar bagus sekaligus peringatan. Bagus, karena volume bukan lagi nilai. Peringatan, karena pipeline yang cuma "minta AI nulis 10 artikel soal topik X" akan menghasilkan 10 file yang tidak dibaca siapa pun. Bedanya cuma satu: apakah ada yang benar-benar dikerjakan sebelum ditulis.

Kalau kamu nulis pakai AI, silakan. Tapi sisipkan sesuatu yang tidak bisa dihasilkan model lain — screenshot error, angka asli, keputusan yang kamu ambil dan alasannya. Itu bagian yang bikin pembaca tinggal, dan kebetulan juga bagian yang bikin detektor AI bingung.

— Chokdi 🐷 · Content Studio · 2026
