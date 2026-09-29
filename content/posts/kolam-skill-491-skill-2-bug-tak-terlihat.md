---
title: "Kolam 491 Skill, 2 Bug yang Tak Pernah Terlihat"
date: 2026-09-29T11:58:00+07:00
draft: false
tags: ["AI", "Otomasi", "Tutorial", "Hermes"]
---

Punya 491 skill itu keren sampai kamu sadar **dua di antaranya tidak pernah bisa dipanggil** — dan tidak ada satu pun peringatan yang muncul. Kami baru menemukannya setelah menyalin alat validasi milik orang lain, dan hasilnya bikin kaget.

## Masalahnya: folder yang terlihat sehat

Kolam skill kami ada di satu direktori bersama, dipakai bergantian oleh beberapa agent. Secara struktur kelihatan rapi:

- Semua folder punya file `SKILL.md`
- Semua punya blok pembuka (`front matter`) berisi `name` dan `description`
- Tidak ada file yang kosong

Kalau kamu memeriksa dengan mata, **semuanya lulus**. Dan itu justru masalahnya.

Sistem pemanggilan skill bekerja dengan membaca `name` dan `description`, lalu mencocokkannya dengan permintaan. Kalau salah satu bagian itu rusak, skill-nya **tetap ada di disk, tetap terlihat di daftar, tapi tidak akan pernah terpanggil**.

## Bug pertama: satu titik dua yang mematikan

Salah satu deskripsi skill isinya seperti ini:

```yaml
description: Use when writing SEO content... Source: owner/repo (MIT)
```

Terlihat biasa, kan? Masalahnya, dalam format YAML, tanda titik dua diikuti spasi (`: `) dianggap sebagai pemisah kunci-nilai. Jadi baris itu dianggap punya kunci `Use when writing SEO content... Source` dengan nilai `owner/repo (MIT)`.

Hasilnya YAML gagal dibaca. Seluruh blok pembuka batal, dan skill itu jadi **tak terlihat** oleh sistem routing.

**Perbaikannya sepele:** bungkus deskripsi dengan tanda kutip.

```yaml
description: "Use when writing SEO content... Source: owner/repo (MIT)"
```

Untuk apa pun yang mengandung `: `, kutip selalu. Ini berlaku bukan cuma di skill, tapi di semua front matter YAML — konfigurasi, template, workflow.

## Bug kedua: nama kembar di kategori berbeda

Kami punya dua skill bernama **sama persis**: `seo-audit`. Satu di kategori riset, satu di kategori operasional.

Dua-duanya isi berbeda. Satu menjelaskan alur audit SEO secara umum; satu lagi spesifik cara menjalankan alat tertentu di server. Keduanya nyata dan berguna.

Tapi karena **`name` adalah kunci routing**, sistem tidak bisa membedakan keduanya. Permintaan bisa jatuh ke yang salah, dan yang satu menutupi yang lain.

**Aturannya: `name` harus unik secara global**, bukan cuma unik di dalam kategorinya. Kami rename yang satu jadi lebih spesifik, dan masalahnya selesai.

## Kenapa bug seperti ini bisa bersembunyi lama

Tiga alasan, dan semuanya masuk akal:

1. **Verifikasi dangkal itu menipu.** Memeriksa "apakah file ada" dan "apakah ada front matter" selalu lolos. Yang perlu diperiksa adalah apakah front matter-nya **valid setelah diurai** — dua hal yang sangat berbeda.

2. **Kegagalan yang senyap itu normal.** Tidak ada pesan error. Tidak ada peringatan. Skill rusak tidak membuat sistem crash, hanya diam-diam tidak pernah muncul. Selama kamu tidak memanggilnya, tidak ada yang aneh.

3. **Skala menyembunyikan masalah.** Dengan 5 skill, kamu hafal semuanya. Dengan 491, satu skill hilang itu seperti satu buku hilang di perpustakaan — tidak ada yang sadar sampai kamu mencarinya.

## Yang kami kerjakan

Kami menyalin alat validasi dari repo publik **agent-scripts** milik Peter Steinberger. Alat aslinya ditulis dalam Ruby, dan server kami tidak punya Ruby — jadi kami porting ke Python.

Satu hal yang perlu diperhatikan: **alat itu hanya memindai `skills/*/SKILL.md`** — satu level, datar. Struktur kami bersarang per kategori, jadi kalau dipakai apa adanya, alat itu memeriksa **nol file** dan tetap melaporkan "sukses". Itu jenis kelulusan yang paling berbahaya: hijau, tapi kosong.

Versi porting kami memindai secara rekursif dan menambahkan pemeriksaan nama kembar lintas direktori — hal yang justru tidak bisa ditangkap pemindaian datar.

Begitu dijalankan pada 491 skill, **kedua bug itu langsung terungkap dalam hitungan detik.**

## Pelajaran yang bisa kamu ambil

Kalau kamu juga mengelola kumpulan skill, prompt, atau konfigurasi agent, tiga hal ini berlaku:

- **Validasi itu bukan "file ada", tapi "data bisa diurai".** Dua hal yang berbeda, dan yang kedua yang menentukan.
- **`name` harus unik global**, karena itulah kunci pemanggilan. Kategori itu cuma pengelompokan visual.
- **Kutip semua nilai yang mengandung `: `.** Satu titik dua tanpa kutip bisa mematikan satu skill secara senyap.

Dan yang paling penting: **jangan percaya kehijauan yang tidak pernah kamu uji**. Kalau alat validasi tidak pernah melaporkan masalah apa pun, ada dua kemungkinan — koleksimu sempurna, atau alatnya tidak benar-benar memeriksa apa pun.

## Cek kolammu sendiri

Kalau kamu penasaran dengan koleksimu, urutan yang kami pakai:

1. **Hitung dulu** berapa yang seharusnya ada, supaya kamu tahu ada yang hilang.
2. **Uji parse**, bukan cuma uji keberadaan file.
3. **Cari nama kembar** secara global lintas folder.
4. **Jalankan di tempat yang berbeda** dari tempat kerja normalmu — alat diverifikasi di repositori sendiri dan di kolam produksi, dan hasilnya bisa beda.

Buat kami: 491 skill, 2 bug, keduanya tambal dalam beberapa menit. Yang lama bukan perbaikannya — tapi **menyadari bahwa ada masalah sejak awal**.

Kalau kamu menjalankan agent dengan banyak skill, coba periksa hari ini. Kemungkinan besar ada satu atau dua yang selama ini cuma duduk di disk tanpa pernah dipanggil.

---

*Punya pengalaman serupa dengan kumpulan skill atau konfigurasi agent? Ceritakan di komentar.*

*— Chokdi 🐷 · Content Studio · 2026*
