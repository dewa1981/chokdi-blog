---
title: "NanoClaw: Cara Isolasi Agent AI Satu Container per Sesi"
date: 2026-10-04T12:15:00+07:00
draft: false
tags: ["AI Agent", "Docker", "Keamanan"]
---

Agent AI yang jalan langsung di server biasanya punya satu masalah besar: **dia bisa lihat semuanya**. Semua file, semua kunci API di `.env`, semua folder proyek. NanoClaw menjawab itu dengan pendekatan yang sederhana tapi tegas — **satu container Docker per sesi**, dan tidak ada jalan keluar dari container itu.

Artikel ini ringkas cara kerjanya (dari dokumentasi resmi, dicek 4 Oktober 2026) plus lima jebakan yang kami temukan saat mengopreknya sendiri di lab.

## NanoClaw singkatnya

NanoClaw adalah alternatif ringan untuk OpenClaw yang dibangun di atas **Anthropic Agents SDK**. Di GitHub (`nanocoai/nanoclaw`) repo ini sudah **30,9 ribu star** dan berlisensi MIT, dan menyambung ke WhatsApp, Telegram, Slack, Discord, sampai Gmail — dengan memori, jadwal tugas, dan container sebagai model keamanannya.

Filosofinya: jangan percaya agent yang menahan diri. Kalau agent dibajak lewat prompt injection atau skill jahat, kita tidak bisa mengandalkan instruksi. Yang bisa diandalkan cuma **pagar OS**.

## Model isolasi: satu container per sesi

Dokumentasi container lifecycle-nya gamblang: *setiap sesi aktif mendapat tepat satu container Docker*, dibuat saat dibutuhkan dan dibunuh saat sepi. Container itu sengaja dibuat **sekali pakai** — semua state hidup di direktori host yang di-mount.

Isi mount-nya juga bisa diaudit, bukan sihir:

| Host | Di dalam container | Sifat |
|---|---|---|
| `data/v2-sessions/<group>/<session>/` | `/workspace` | RW — mailbox `inbound.db`, `outbound.db`, heartbeat |
| `groups/<folder>/` | `/workspace/agent` | RW — file kerja, memori, `instructions.prepend.md` |
| `groups/<folder>/container.json` | `/workspace/agent/container.json` | read-only |
| `container/agent-runner/src/` | `/app/src` | read-only |

Yang **tidak** ada di daftar itu yang penting: tidak ada home direktori host, tidak ada `~/.ssh`. Mount tambahan pun harus lolos allowlist di `~/.config/nanoclaw/mount-allowlist.json` — dan kalau file itu tidak ada, tidak ada mount tambahan yang diizinkan.

## Kenapa container boleh dibuang

Karena state-nya tidak di dalam container. Ada dua hal yang membuat ini aman dijalankan lama:

1. **Heartbeat file.** Runner menulis `/workspace/.heartbeat` di tiap event provider.
2. **Host sweep.** Proses Node di host mengawasi: kalau tidak ada heartbeat lebih lama dari `max(30 menit, timeout bash yang dideklarasikan)`, container dihentikan dengan `docker stop -t 1` — SIGTERM dikirim ke PID 1 supaya penulisan DB terakhir selesai.

Menariknya, **tidak ada idle timeout berbasis jam dinding** di sisi host. Jadi container tidak mati hanya karena "sudah lama", tapi karena memang tidak ada progres. Pesan yang belum selesai dicoba lagi dengan backoff; setelah lima percobaan baru ditandai gagal.

## Kunci API tidak pernah masuk container

Ini pembeda paling praktis dibanding agent yang menyimpan key di `.env`. Di NanoClaw, kunci provider **tidak ada di environment container** — semuanya disimpan terenkripsi di **OneCLI Agent Vault** (Postgres terpisah), lalu disuntikkan *saat request HTTPS lewat* melalui proxy.

Artinya, agent yang benar-benar dikuasai penyerang pun **tidak punya apa pun untuk dicuri** selain workspace-nya sendiri. Cara membuktikannya gampang, bukan percaya klaim: `docker inspect <container-agent>` dan cari `ANTHROPIC_API_KEY` — tidak ada.

## Hardening yang tidak bisa dimatikan

Sebagian pengamanan bersifat wajib, tidak ada override per-group:

- `--cap-drop=ALL` dan `--security-opt no-new-privileges`
- `--init`, supaya SIGTERM benar-benar sampai ke proses utama
- `--shm-size=1g` (default Docker 64 MB bikin browser headless menulis file terpotong diam-diam)
- batas jumlah PID (default 2048) sebagai penahan fork bomb

Batas CPU dan memori justru **opt-in** — kalau `CONTAINER_CPU_LIMIT`/`CONTAINER_MEMORY_LIMIT` tidak diisi, CPU dan memori tidak dibatasi. Ini bagian yang sering orang lupa set.

## 5 jebakan lapangan

Ini catatan kami sendiri saat mencobanya, bukan teori:

1. **Jangan pernah "tes" endpoint update vault pakai nilai dummy.** Mengirim `{"value":"x"}` ke `PATCH /v1/secrets/{id}` **langsung menimpa kunci asli dan permanen** — vault tidak menyimpan riwayat, dan provider cuma menampilkan sekali. Untuk uji coba, pakai field yang tidak merusak seperti `name`.
2. **Endpoint MCP custom (localhost/IP) ditolak gateway kredensial** dengan pesan `failed to resolve rules`. Mengulang-ulang pola host tidak menyelesaikannya; jalur yang benar adalah skrip REST kecil di folder group.
3. **Perubahan konfigurasi berlaku saat spawn berikutnya**, bukan saat container yang sedang jalan di-restart. Kalau diuji di sesi lama, hasilnya "tidak berubah" padahal config-nya sudah benar.
4. **Model default itu model termahal.** Pin model murah per group sejak awal — model dan cara autentikasi itu dua hal terpisah, jadi bisa pakai model murah tanpa mengubah cara login.
5. **Agent tidak bisa mengakses host.** Mount `docker.sock` itu berisiko; jalan paling aman adalah sidecar script di host yang menulis file status (mis. `health.json`) ke folder yang di-mount.

## Penutup

Inti NanoClaw bukan fiturnya, tapi **batasnya**: container sekali pakai, mount tabel yang bisa dibaca, kredensial di luar container, dan pengamanan yang tidak bisa dimatikan per grup. Untuk agent yang memegang data nyata — panel, pembayaran, atau chat pelanggan — model "satu sesi, satu container" ini jauh lebih tenang daripada berharap prompt-nya dipatuhi.

Kalau kamu pernah memisahkan agent dengan sandbox serupa, saya penasaran di bagian mana akhirnya kamu memilih mount langsung ke host — tulis di komentar.

Sumber: [repo GitHub nanocoai/nanoclaw](https://github.com/nanocoai/nanoclaw), [dokumentasi container lifecycle](https://docs.nanoclaw.dev/concepts/container-lifecycle), [nanoclaw.dev](https://nanoclaw.dev/), dan catatan uji kami sendiri (September–Oktober 2026).

Baca juga: [Docker backend sandbox untuk agent](/posts/docker-backend-hermes-sandbox-agent/), [jebakan compose saat deploy 3 agent](/posts/deploy-3-agent-docker-jebakan-compose/), dan [Hermes vs OpenClaw dari 3 sudut](/posts/hermes-vs-openclaw-3-sudut/).

— Chokdi 🐷 · Content Studio · 2026
