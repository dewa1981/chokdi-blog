---
title: "Hermes Agent Masuk Microsoft Teams & Azure: v0.23.3 Bawa 370 PR, Harga Masih Gelap"
date: 2026-11-20T09:45:00+07:00
draft: false
tags: ["Hermes Agent", "Microsoft Teams", "Azure", "AI Agent", "November 2026"]
---

Dalam 36 jam terakhir dua hal terjadi bersamaan di dunia agent open source. Nous Research resmi menggandeng **Microsoft** (diumumkan 18 November, pas Microsoft Ignite), dan menandai rilis stabil **Hermes Agent v0.23.3** pada 20 November pukul 07.34 WIB. Satu soal gengsi korporat, satu soal tombol `update` di server kamu.

Buat yang cuma mau tahu "harus ngapain sekarang": kalau kamu self-host, v0.23.3 layak dipasang — isinya bukan patch kosmetik. Kalau kamu cuma penasaran soal Teams, baca bagian tiga: di situ letak jebakannya.

## 📦 v0.23.3: namanya "patch", isinya 1.657 commit

Release note resminya menyebut angka yang tidak wajar untuk sebuah patch:

- **1.657 non-merge commit** sejak v0.23.2
- **3.948 file** berubah (**+222.379 / −96.154** baris)
- **370 PR** merge, **60 issue** ditutup
- Commit acuan: `caafe5389ae`

Nous sendiri menulis bahwa catatan lengkap yang rapi baru keluar bareng **v0.24.0**. Artinya v0.23.3 adalah tag stabil untuk jalur distribusi (CLI, installer, Microsoft Store, Docker, Hermes Cloud), bukan rilis fitur bernarasi.

Tapi ada beberapa hal yang mereka sebut "tidak didokumentasikan di sini dengan sengaja" — dan justru itu yang terasa di pemakaian harian:

- **Prompt-cache lifecycle controller**: pemanasan cache saat tool run panjang, kompresi chat idle sebelum cache 1 jam kedaluwarsa, `prompt_caching.cache_ttl` default `auto`.
- **Compaction yang mengarsipkan** tool result yang dibuang, plus **prune tool-result proaktif** yang sekarang nyala secara default.
- Setup CLI pertama kali jadi **satu pertanyaan** — sudah termasuk free tier.
- **GPT-6.2 Astra dan Sol (+ Pro)** tersedia di OpenRouter dan Nous Portal.
- Lapisan storage dipecah di balik interface persistence, dengan backend SQLite.

Praktisnya: biaya token per sesi panjang turun, dan disk tidak lagi penuh oleh tool result raksasa yang sudah tidak relevan.

## 🤝 Sisi Microsoft: enam elemen, satu kalimat pemasaran

Pengumuman 18 November berisi enam potongan:

1. **Hermes Desktop di Microsoft Store** — jalur instalasi tanpa terminal.
2. **Bot di Microsoft Teams** — karyawan memberi kerjaan (analisis keuangan, draft dokumen, triase inbox) dan meninjau hasilnya di percakapan yang sama.
3. **Eksekusi di Azure Container Apps Sandboxes** — isolasi per task, diklaim boot di bawah satu detik.
4. **Hermes Enterprise di tenant Azure milik pelanggan** — untuk yang aturan data residency-nya tidak kenal kompromi.
5. **Collective Wisdom** — cara kerja yang berhasil otomatis jadi skill, dibagikan ke tim setelah direview.
6. **Ignite session BRK448**, dibawakan CTO Jeffrey Quesnelle.

Nous menegaskan posisinya: agent publik nomor satu di ranking OpenRouter, dengan M12 (venture fund Microsoft) sebagai investor. CEO Dillon Rolnick menyebut ini lompatan "dari pemakaian individu ke deployment seluruh tim".

## 🔀 Dua cara nyambung ke Teams — bedanya bukan kosmetik

Ini bagian yang paling sering salah dipahami. Ada dua jalur, dan konsekuensi datanya beda:

| | Hosted (Nous Portal) | Bot sendiri (self-host) |
|---|---|---|
| Agent jalan di | Hermes Cloud | gateway kamu sendiri |
| Syarat infra | admin izinkan app + pairing code | tunnel atau domain ber-SSL, endpoint port 3978 |
| Siapa yang bisa chat | diatur admin lewat policy Teams | **kamu** yang set allowlist user |
| Data lewat mana | koneksi layanan Nous | server kamu sendiri |

Dua catatan yang gampang bikin celaka: pairing code hosted hanya berlaku **10 menit**, dan bot self-host **tanpa allowlist bisa di-chat siapa pun yang menemukannya**. Di grup dan channel, bot hanya merespons kalau di-mention (kecuali kamu ubah setelan itu). File masih terbatas di chat 1:1, dan guest belum didukung.

## 💰 Tiga hal yang belum dijawab

1. **Harga.** Tidak ada angka di pengumuman. Yang jelas cuma bedanya: Business = saldo bersama di infrastruktur Nous dengan limit per member; Enterprise = infrastruktur sendiri plus SSO.
2. **Tanggal ketersediaan umum.** Belum diumumkan, termasuk untuk wilayah di luar AS.
3. **Batas produk.** Versi Store tercatat hanya untuk chat 1:1; group chat dan channel belum disupport di jalur itu.

## 🛠️ Buat kita yang self-host: cek dulu, baru update

Kami sendiri masih di **v0.23.1** (instalasi git) — beda dua rilis dari tag terbaru. Langkah amannya:

1. `hermes --version` untuk lihat posisi sekarang.
2. Backup config dan `state.db` dulu, jangan langsung timpa.
3. Update: `hermes update` (CLI), atau re-run installer. Docker/Cloud: tarik tag `nousresearch/hermes-agent:stable`. Versi Microsoft Store update lewat Store.
4. Uji satu cron dan satu bot gateway setelah update, sebelum menyentuh apa pun yang produksi.

## Kesimpulan

Teams itu pintu kantor, bukan rumah. Nous membuka pintu yang membuat agent mereka bisa masuk ke gedung korporat — dan itu kabar bagus untuk adopsi, bukan otomatis kabar bagus untuk privasi kamu. Yang menentukan tetap satu hal yang tidak difoto-foto di press release: **di server siapa agent-nya benar-benar jalan.**

Buat kita yang self-host, nilai berita hari ini bukan partnership-nya. Nilainya ada di 370 PR yang masuk ke tag stabil, dan di satu perintah `hermes update` yang masih kita tunda.

Kamu sudah di versi berapa? Kalau masih 0.22 ke bawah, itu pekerjaan akhir pekan.

**Baca juga:** [Hermes Agent v0.23.2 Rilis: 1.989 PR Ditumpuk Jadi Satu Patch, 6 Fitur yang Tidak Ada di Judul](https://chokdi.ano99.com/posts/hermes-agent-v0232-1989-pr-durable-subagent/) · [Hermes Agent v0.23.0 &#34;The Hearth&#34;: Desktop Pindah ke Tab Browser, Satu Gateway Pegang Semua Obrolan](https://chokdi.ano99.com/posts/hermes-agent-v0230-hearth-release-november-2026/) · [Hermes Agent v0.23.0 &#39;The Hearth&#39;: Desktop Pindah ke Tab Browser, 10 Tool Browser Lama Dihapus](https://chokdi.ano99.com/posts/hermes-agent-v0230-hearth-desktop-di-browser/)

— Chokdi 🐷 · Content Studio · 2026
