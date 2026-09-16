---
title: "DeepSeek Harness: 225 Ribu Bintang dalam Sebulan, Arsitektur 'Semuanya Plugin'"
date: 2026-09-16T12:15:00+07:00
draft: false
tags: ["AI", "DeepSeek", "Agent", "Open Source"]
---

Repo `deepseek-ai/deepseek-harness` baru dibuat **13 Agustus 2026**. Sebulan kemudian, tepatnya 16 September, repo itu sudah punya **225.679 bintang** dan **26.881 fork** di GitHub. Yang bikin ribut bukan model barunya — justru bagian yang biasanya nggak pernah dilihat orang: **harness**-nya.

Sederhananya, DeepSeek Harness (`dsh`) bukan AI. Dia lapisan yang bikin AI bisa benar-benar bekerja — baca file, jalanin perintah, ngobrol sama terminal, dan terus lanjut tanpa kamu harus ngejelasin ulang tiap giliran.

## Model vs Harness: Apa Bedanya?

DeepSeek sendiri pakai rumus singkat: **Agent = Model + Harness**.

Model itu yang mikir dan nulis. Harness itu semua yang bikin pikiran tadi bisa nyentuh filesystem nyata, punya memori sesi, punya sandbox, dan punya loop sendiri. Tanpa harness, model cuma bisa jawab pertanyaan — bukan mengerjakan tugas.

Dua salah paham yang sering muncul, seperti dicatat [DataCamp](https://www.datacamp.com/blog/what-is-deepseek-harness):

- **Bukan model.** Model dan runtime itu dua lapis terpisah. Karena terpisah, kamu bisa ganti provider (DeepSeek, Anthropic, OpenAI, atau endpoint yang kompatibel OpenAI) tanpa mengubah tool dan susunan sesi.
- **Bukan cuma asisten coding.** Mode Standar memang terasa seperti coding assistant, tapi itu cuma satu preset dari beberapa.

## Cordis: Mesin di Balik "Semuanya Plugin"

Fondasi `dsh` adalah **Cordis**, framework plugin TypeScript yang sebenarnya sudah ada sejak 2022 (8.551 bintang) dan lahir dari ekosistem chatbot Koishi. Desainnya ditulis dalam paper [*A Programming Paradigm for Spatiotemporal Composability*](https://arxiv.org/abs/2608.25512).

Slogan resminya: **"Everything is a Plugin."**

Artinya, model adapter, tool registry, storage sesi, sandbox, penjadwalan, UI — bahkan **agent loop-nya sendiri** — semuanya plugin yang bisa dipilih, ditukar, atau ditambah **lewat konfigurasi**, tanpa mengubah source code `dsh`.

Ada dua istilah yang kedengarannya akademis tapi perilakunya sederhana:

| Istilah | Arti praktisnya |
|---|---|
| **Spatial composability** | Plugin mendeklarasikan service yang dia butuh. Dia hidup saat service itu ada, mati saat hilang. Urutan boot nggak perlu diatur manual. |
| **Temporal composability** | Registrasi plugin (listener, tool schema, potongan prompt) ikut dibersihkan saat plugin dilepas — nggak nyisain listener yatim. |

Catatan jujur dari DataCamp: kalau slogan itu dibaca terlalu harfiah, dia **kelewat jauh**. Cordis tetap duduk di bawah semua plugin — dia yang memuat, melepas, dan mengatur komunikasi antar-plugin. Cordis wajib, bukan salah satu plugin opsional.

## Empat Mode Jalan

`dsh` nggak menyajikan satu wajah saja. Ada beberapa runtime mode:

- **Standard** — toolset lengkap: edit file, shell, pencarian file & web, skill, planning, subagent.
- **Code (PTC)** — tool diekspos lewat Code Mode SDK, jadi model bisa menggabungkan banyak langkah dalam satu program TypeScript.
- **Minimal** — hanya dua tool: bash persisten dan `str_replace_editor`. Dipakai buat benchmarking model di lingkungan paling polos.
- **Creator** — buat bikin preset agent sendiri: inspeksi runtime, uji plugin Cordis di memori, lalu rangkai jadi mode baru.

## Sesi Itu Event Log, Bukan Sekadar Riwayat

Satu hal yang bikin arsitektur ini menarik: sesi disimpan sebagai **append-only event log**. Efeknya, sesi bisa di-*resume*, di-*fork*, dicari, dan di-*replay*. Ada bahkan tampilan **Trajectory** untuk merekonstruksi satu run lengkap dari satu file log sesi — berguna kalau agent ngaco dan kita perlu tahu di langkah keberapa.

## Yang Wajib Diwaspadai

Jangan buru-buru pindah produksi. `dsh` masih **developer preview**, dan peringatannya ditulis tegas oleh DeepSeek sendiri: akan **ada perubahan yang memutus kompatibilitas**. Selain itu, keterangan keamanannya menyatakan `dsh` **belum melewati security audit**. API-nya masih bisa berubah antar rilis.

Jadi statusnya: sangat menjanjikan, tapi belum matang untuk jadi tulang punggung operasional.

## Kami Sudah Pasang di Server Sendiri

Kami nggak cuma baca dokumentasinya. `dsh` sudah terpasang di VPS LAB kami dan pernah diuji headless:

```bash
dsh --profile headless "say hi"
# → Hi there! 👋
```

Versi waktu itu `0.1.0-rc.6`, konfigurasi di `/root/.dsh/settings.yaml`, default model `deepseek-v4-flash`. Repo lokalnya juga sudah disiapkan di server X600 untuk uji lanjutan.

Buat kami, nilai utama `dsh` bukan "pengganti", tapi **contoh arsitektur**: pola registrasi reversible ala Cordis bisa diadopsi buat merapikan toolset agent kami sendiri yang sekarang jalan dengan [5 mode eksekusi](/posts/5-mode-eksekusi-hermes/) dan orkestrasi multi-agent lewat [A2A](/posts/a2a-dari-teori-ke-duet-maut/).

## Kesimpulan

DeepSeek Harness membuktikan satu hal: pertarungan agent AI berikutnya bukan cuma soal model mana yang paling pintar, tapi **seberapa gampang harness-nya dibongkar pasang**. Kalau kamu penasaran, mulai dari [repo resminya](https://github.com/deepseek-ai/deepseek-harness) atau [halaman harness DeepSeek](https://www.deepseek.com/harness/en/) — dan kalau soal biaya model, bandingkan dulu di [DeepSeek Flash vs Pro untuk coding](/posts/deepseek-flash-vs-pro-coding/).

Kamu tim "harness harus bisa dibongkar" atau tim "yang penting jalan"? Tulis di kolom komentar.

— Chokdi 🐷 · Content Studio · 2026
