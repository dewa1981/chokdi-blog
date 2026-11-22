---
title: "10 Plugin Pemenang Hackathon Hermes Agent: Yang Menang Bukan yang Paling Viral, tapi yang Bikin Agent Susah Dibolongi"
date: 2026-11-22T09:20:00+07:00
draft: false
tags: ["Hermes Agent", "Plugin", "Hackathon", "AI Agent", "Nous Research", "Open Source"]
---

Nous Research mengumumkan pemenang **Hermes Agent Plugin Hackathon** pada 20 November malam waktu AS — 21 November dini hari WIB. Hampir **1.000 orang** mengirim entri dalam 7 hari, dan yang menang bukan plugin paling ramai di YouTube. Hampir semuanya pagar: alat yang membuat agent lebih susah dibohongi, disalahgunakan, atau menghapus kerja orang.

## 📊 Angka dulu

- **~1.000 entri**, hanya 7 hari (4–12 November).
- Total hadiah **$20.000**: juara 1 $10.000, juara 2 $5.000, juara 3 $2.500, juara 4 $1.500, juara 5 $1.000, lima runner-up dapat merch + $250 kredit.
- Dua lapis: **agent menilai semua entri**, lalu **lima juri komunitas** (@HermesWatcher, @KSimback, @rlaope, @LiorNsnd, @iamlukethedev) mengurutkan finalis jadi 10 besar.
- Marketplace pagi ini: **2.514 plugin**. Tanggal 7 November masih **1.063** — naik 2,4x dalam 15 hari.

## 🥇 Tiga besar

**1. Foreman** (PedValme, MIT). Gate deterministik untuk repo git: tanpa model, cuma standard library Python dan git. Dia baca diff sebelum `git commit`, `git push`, dan `gh pr create`, lalu blokir kalau perubahan menghapus test, menambah `@unittest.skip`, melemahkan perintah check, melewati hook, atau membawa secret. `gh pr merge` yang dijalankan agent **selalu** diblokir; merge cuma lewat `/foreman merge` yang kamu ketik sendiri.

**2. Housemate** (RaYYeR220). HP lama, tablet, laptop jadi speaker per ruangan lewat browser. Ucapkan wake word, tanya, jawabannya keluar di ruangan itu; kalau beberapa perangkat mendengar, yang paling dekat menjawab. Ada timer yang berbunyi di ruangan asalnya, intercom, dan approval lisan. Gateway jadi hub HTTPS + WebSocket di port 8742, perangkat dipasangkan lewat kode enam digit.

**3. Plan Mode** (100yenadmin, v1.6.0). Agent menjelajah read-only dan menulis rencana; **semua tool yang mengubah file diblokir sampai kamu setujui**. Setelah kartu persetujuan di-approve, dia eksekusi dan mencentang todo. Jalan di CLI, Telegram, Discord, Slack, Desktop, dan TUI; butuh Hermes 0.21.5+.

## 🛡️ Tujuh sisanya juga soal pagar

- **Seedguard** (Investorquab): firewall secret. Private key, seed phrase, API key, dan kode 2FA diganti placeholder sebelum sampai ke model; tool yang di-arm masih bisa memakainya. Fail-closed, MIT, butuh Hermes ≥0.19.
- **Ariadne** (miracle352): rekam satu sesi lalu putar ulang **tanpa model, network, atau token**. Buat cek apakah update Hermes aman dengan memutar sesi sendiri di versi baru, bandingkan dua instalasi, atau bisect commit penyebab perubahan.
- **Mandate** (JoeProAI): least-privilege untuk cron. Dia amati kerja job, usulkan policy per-argumen, dan setelah kamu setujui, blokir panggilan di luar itu. Bench mereka: **29 dari 29 panggilan serangan diblokir**, 0 dari 120 run serangan berbuat jahat (default Hermes: 18 dari 120). Trade-off nyata: 39 dari 1.038 panggilan sah ikut diblokir.
- **safe-swap** (itsolaph): menulis ulang perintah shell berbahaya sebelum jalan. `git push --force` jadi `--force-with-lease --force-if-includes`, `rm -r` jadi pindah ke karantina, `git reset --hard` dan `git clean` bikin snapshot dulu. Ada `/swaps` dan `/unswap`.
- **Promise Keeper** (MokiMeow): bilang aturan sekali ("jangan sentuh folder prod"), dia usulkan aturan yang mengutip kata-katamu, lalu setiap tool call diperiksa dua kali oleh kode deterministik. Lokal, tanpa network.
- **Hermes Canvas** (0xbyt4): rencana agent digambar sebagai kotak di panel Desktop sebelah chat. Tiap kotak terikat ke file dan perintah check; hook menandai "sedang dikerjakan", "selesai", atau "gagal". Kotak pertanyaan bisa kamu jawab, catatan bisa kamu taruh, dan kotak yang dihapus memblokir tulisan berikutnya ke file-nya.
- **Hermes Gadget SDK** (adolandev): Hermes di **29 papan hardware**, termasuk ESP32-P4, M5Stack StickS3, dan "Cheap Yellow Display". ESP32 jadi gadget suara untuk Hermes.

## 🧠 Pola yang menang

Video "These 9 Plugins 10x'd Hermes Agent" (Teku AI, 17 November, 12.874 tayangan) isinya Phone Harness, asisten travel, dan Home Assistant. "I Tested 5 Official Hermes Plugins" (Percy Kintu, 19 November, 8.768 tayangan) menguji plugin resmi dari Claude subscription SDK sampai ElevenLabs music.

Dua-duanya berguna, tapi juri memilih arah lain: **7 dari 10 pemenang adalah guardrail atau verifikasi**, bukan fitur baru. Nilai plugin bukan "agent bisa lebih banyak", tapi "agent lebih susah merusak sesuatu saat kamu tidak melihat".

## 🛠️ Cara pasang dan cara aman mencobanya

Pola instalasinya satu: `hermes plugins install <nama-plugin> --enable`, lalu `hermes gateway restart` kalau pakai gateway messaging.

Tiga hal sebelum pasang semua:

1. **Kebanyakan masih v0.1.0.** Baru Plan Mode dan safe-swap yang lewat v1.0. Coba di profil staging, bukan agent produksi yang pegang cron dan kredensial.
2. **Plugin jalan dengan hak akses agent.** Baca *Disclosure* di marketplace: apa yang dibaca, apa yang ditulis, ada network call atau tidak. Yang menang di hackathon pun tetap kode pihak ketiga.
3. **Cek versi minimum.** Seedguard butuh Hermes ≥0.19, Plan Mode 0.21.5+. Di instalasi lama, plugin bisa gagal senyap.

## ✅ Kesimpulan

Sepuluh alat ini bisa dipakai hari ini; tiga langsung relevan buat siapa pun yang menjalankan agent tanpa ditunggui: **Mandate** untuk cron, **Foreman** untuk repo kode, **Seedguard** untuk kredensial. Kalau cuma sempat pasang satu, mulai dari Foreman — satu `git push --force` yang salah lebih mahal daripada semua waktu yang kamu hemat.

**Baca juga:** [Hackathon Plugin Hermes: Hadiah $20.000, Deadline 12 November 05.00 WIB](https://chokdi.ano99.com/posts/hermes-plugin-hackathon-20-ribu-deadline-12-november/) · [Katalog Plugin Hermes: 416 Entri, 8 Resmi, dan 182% Pertumbuhan dalam 3 Minggu](https://chokdi.ano99.com/posts/katalog-plugin-hermes-416-entri/) · [Hermes Agent 8 Pekan: 13 Rilis, Katalog Plugin 1.050+, dan Kenapa Upgrade Sekarang Lebih Aman](https://chokdi.ano99.com/posts/hermes-agent-262-ribu-stars-13-rilis-november-2026/)

— Chokdi 🐷 · Content Studio · 2026
