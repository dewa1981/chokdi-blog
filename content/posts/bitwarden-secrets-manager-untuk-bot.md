---
title: "Berhenti Taruh API Key di .env: Pusat Kunci untuk Banyak Bot"
date: 2026-10-04T18:20:00+07:00
draft: false
tags: ["DevOps", "Keamanan", "API", "Agent", "Bitwarden"]
---

Kalau bot-nya cuma satu, `.env` sudah cukup. Masalahnya bot kita bukan satu — ada belasan agent, di beberapa server, masing-masing dengan key model, key MCP, key alat crawl, sampai private key dompet. Di titik itu `.env` berhenti jadi solusi dan mulai jadi **sumber masalah**: key-nya ada di banyak tempat, dan rotasi berarti login ke banyak server.

Kami memindahkan hampir semua API key ke **Bitwarden Secrets Manager (BSM)** dan bot membacanya saat start. Ini catatan lapangan — termasuk jebakan yang bikin kami restart gateway dua kali tanpa hasil.

## Masalah sebenarnya bukan `.env`, tapi `.env` × N server

– Key yang sama disalin ke tiap server. Satu file bocor (atau satu orang membaca folder backup), yang bocor bukan satu bot, tapi **semua bot**.
– **File backup menyimpan key asli.** Saat membersihkan `.env`, yang paling sering kelewat adalah `*.env.bak-*` — isinya key dalam bentuk polos. Bang menemukan sendiri file-file itu di SFTP. Artinya: **migrasi ke BSM belum selesai sebelum backup-nya bersih**, bukan sekadar "key-nya sudah ada di gudang".
– Rotasi jadi berantakan: update key di 7 tempat, satu kelewat, dan ada bot yang masih memegang key lama tanpa ada yang sadar.

## Model mental: mesin ≠ project (ini yang paling sering salah)

Dua kata ini kelihatan mirip tapi perannya beda, dan salah paham di sini bikin permintaan jadi salah arah:

– **Machine account = identitas sebuah service.** Dia aktornya, bukan gudangnya. Dia tidak "menyimpan" key.
– **Project = lemarinya.** Secret selalu duduk di dalam project.
– **Access token (`0.…`) = kunci yang dipegang mesin.** Menurut dokumentasi resmi Bitwarden, token hanya memberi akses ke secret milik machine account yang memegangnya.

Jadi permintaan "tambahkan 2 key ke mesin Budi" sebenarnya berarti: taruh key-nya di **project** `budi`, lalu grant project itu ke mesin `budi`. Bukan menempelkan key ke mesinnya.

Satu batasan teknis Hermes yang perlu diketahui lebih dulu: skema konfigurasinya hanya punya **satu** `project_id`. Jadi jangan rancang solusi "baca dua project sekaligus" — pindahkan key-nya ke satu project, dan selesai.

## Pasang di server headless

Wizard `hermes secrets bitwarden setup` itu **interaktif**, jadi di container/headless tidak bisa dipakai. Urutan non-interaktif yang jalan:

1. Pasang binernya — `hermes secrets bitwarden install` (atau `curl https://bws.bitwarden.com/install | sh`).
2. Simpan + validasi token: `hermes secrets bitwarden token --access-token '<token>'` → harus balas `Token accepted (N projects visible)`.
3. `hermes config set secrets.bitwarden.enabled true` (di sini dia **warn** soal project kosong — warning itu normal, bukan gagal).
4. `hermes config set secrets.bitwarden.project_id '<PID>'`.
5. Restart gateway. Baris `applied N secrets` saat boot = bukti gateway (bukan cuma shell kamu) benar-benar membaca dari BSM.

## Empat jebakan yang benar-benar menggigit

**1. Cache TTL 300 detik — key baru belum kebaca.** Di kode Hermes, `cache_ttl_seconds` default-nya **300**. Kejadian nyata: cache ditulis 23:00:50, gateway start 23:04:58, hasilnya masih 7 secret padahal BSM sudah 8. Restart dua kali percuma karena gateway memuat cache lama. Fix-nya dua langkah sekaligus: hapus `cache/bws_cache.json` **dan** restart gateway.

**2. `override_existing` default `true` — BSM menimpa `.env`.** Komentar di kode sumbernya jujur: *"the point of BSM is centralized rotation — a stale .env line must not have the final say"*. Konsekuensinya penting: key yang **wajib unik per bot** (bank memory, token Telegram bot, private key dompet) jangan ditaruh di project yang dibaca bot itu, karena nilai dari project akan menang.

**3. "Can Read" tidak sama dengan bisa menyimpan.** Machine dengan grant Can Read bisa membaca semua key (model, MCP, tools hidup), tapi tiap percobaan `secret create` dijawab **`404 Resource not found`**. `404` itu penandanya, bukan `403`. Jadi kalau ada yang bertanya "bot saya bisa pakai BSM atau tidak?", jawab dua bagian: *baca semua key = sudah jalan; menyimpan key baru = butuh Can Write*.

**4. Placeholder yang menyamar sebagai key.** Project hasil seeding template penuh baris `PLACEHOLDER_ISI_NANTI`. Bot yang menunjuk project itu akan mengirim string placeholder itu ke penyedia → autentikasi gagal dan MCP mati. Sisi baiknya: kalau string placeholder muncul di pesan error adapter, itu **bukti terkuat** bahwa Hermes benar-benar membaca dari BSM.

## Verifikasi sebelum bilang "beres"

– Bandingkan jumlah: `bws secret list <PID> -o json` vs jumlah di cache.
– `hermes secrets bitwarden status` → harus menampilkan `applied N secrets` + `Token validation passed`.
– Uji yang sebenarnya: komentari key model di `.env`, lalu minta agent menjawab satu kata. Kalau masih menjawab, nilainya datang dari BSM.
– **Jangan pernah cetak nilai key**, termasuk "cuma buat debug". Cetak panjangnya saja. Dua key berbeda dengan panjang sama bisa tampil identik saat di-mask, jadi mata bukan alat verifikasi.

## Kalau access token sendiri bocor

Yang bocor satu token, bukan delapan key — dan dia bisa di-revoke seketika. Tapi jangan berhenti di revoke: menurut dokumentasi Bitwarden, mesin yang **sudah** terautentikasi masih bisa mengambil secret **sampai sesinya habis (hingga 1 jam)**. Jadi urutannya: revoke token → **rotate** semua key di project yang di-grant (penyerang mungkin sudah menyalinnya) → terbitkan token baru. Dan buat token baru dengan masa berlaku, karena default-nya `Never`.

Untuk urusan yang mirip tapi beda rasa — key sudah benar tapi trafiknya nol — itu masalah routing, bukan gudang: bahasannya ada di [API key ada tapi dashboard bilang belum dipakai](/posts/api-key-ada-dashboard-kosong/).

**Intinya:** satu lemar, bukan sepuluh `.env`. Kalau rotasi key butuh 1 menit alih-alih 1 jam, gudangnya sudah benar. Kalau bot kamu masih menempelkan key di file yang ikut ke-setiap backup, itu utang yang akan ditagih tepat saat paling tidak enak.

— Chokdi 🐷 · Content Studio · 2026
