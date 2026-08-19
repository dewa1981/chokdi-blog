---
title: "Hermes Agent Bot Mode: Ubah Profil Jadi Tim Bot AI yang Saling Ngobrol 🤖"
date: 2026-08-19T09:00:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Bot Mode", "Open Source", "Automation"]
---

# Hermes Agent Bot Mode: Ubah Profil Jadi Tim Bot AI yang Saling Ngobrol 🤖

Bayangkan punya tim asisten AI yang tiap anggotanya punya kepribadian, memori, dan model sendiri — dan mereka bisa saling *bertukar tugas* pakai `@mention` kayak di grup chat. Itulah yang baru aja diluncurkan Nous Research lewat **Bot Mode** di Hermes Agent versi **v0.20.3**. Buat kita yang sehari-hari kerja pakai agent AI, ini salah satu update paling seru di ekosistem open source tahun ini. Yuk kita bedah, Bang! 🔥

## 🚀 Apa Itu Bot Mode?

Sebelumnya Hermes Agent punya daftar *session* percakapan tunggal. Sekarang diganti jadi **roster bot bernama**. Setiap bot itu sebenarnya **profil Hermes beneran** — lengkap dengan chat, memori, skills, dan model yang di-pin sendiri-sendiri di bawah `~/.hermes/profiles/<nama>/`.

Yang keren, bot-bot ini bisa **kirim pesan satu sama lain** lewat *Agent Inbox* yang persisten. Ketik `@researcher coba cek ini` di bot aktif, maka bot itu langsung *hand off* tugas dan balik lapor. Ini bukan sekadar UI — di balik layar itu perintah CLI nyata:

```bash
hermes -p <bot> chat -c "Agent Inbox" -q "..."
```

## 🧩 Kenapa Ini Opsi yang Praktis?

Yang paling penting: **satu bot = satu profil**, jadi tidak ada layer penyimpanan baru. Surface area-nya kecil, karena field-nya nunggangin RPC gateway `profiles.*` yang sudah ada (`list`, `create`, `describe`, `configure`). Avatar pakai RPC `image.generate`. Routine-nya cuma cron job Hermes biasa ber-namespace `[bot:nama] <routine>`, dan tetap muncul di `hermes cron list`.

Fitur yang berkembang setelah beta:

- **Groups** — organisir roster jadi section berlabel yang sinkron antar mesin.
- **Group chat** — ruang bersama untuk **2 sampai 6 bot**, maksimal 3 ronde giliran. Bot yang di-`@mention` wajib jawab; kalau tak ada yang di-mention, semua jawab singkat atau *pass*.
- **Multi-source roster** — tarik bot dari semua koneksi di Settings → Connections.

## 💰 Gratis, Tapi Perlu Diingat Batasannya

Bot Mode dan Hermes Agent sama-sama **MIT license**. Awalnya cuma *one-day public beta plugin* dari co-founder Teknium, lalu resmi di-package **default-on** di Hermes Desktop via PR #87886, dan repositori standalone-nya diarsipkan (kini develop in-tree di `apps/desktop/src/plugins/hermes-bots/`).

⚠️ **Catatan penting:** ini tool *workstation*, bukan infrastruktur enterprise. Belum ada admin console, SSO, audit log pusat, atau policy layer. Kalau butuh kontrol terkelola untuk produksi, ada jalur cloud — contohnya **Cloudways Managed AI Agent Hosting** yang baru GA, mendukung deploy Hermes & OpenClaw dengan security patching, backup otomatis, SSH access, dan koneksi ke Slack/Discord/Telegram/WhatsApp.

## 💡 Tips Praktis

1. **Mulai dari kecil** — jangan bikin 10 bot langsung. Mulai 2–3 (misal scout, reviewer, publisher), pelajari dulu polanya.
2. **Pin model per bot** — bot riset di-pin ke reasoning model, bot penulis di model yang lebih murah. Hemat token.
3. **Pisahkan konteks** — bot per proyek tidak bocor konteks satu sama lain. Bagus buat multiklien.
4. **Manfaatkan routine** — jadwalkan digest inbox atau laporan malam pakai cron `[bot:nama]`.
5. **Pahami batas ronde** — group chat cuma 3 ronde serial; desain alur handoff dengan sadar diri.

## 🎯 Kesimpulan

Bot Mode mengubah Hermes dari satu agen jadi **tim agent yang bisa kolaborasi** — dengan memori, model, dan kepribadian yang terpisah, plus handoff antar-bot yang mulus via `@mention`. Karena berbasis profil yang sudah ada, fitur ini kecil di permukaan tapi besar dampaknya. Buat solo builder, startup, dan tim engineering kecil, ini jalan pintas ke *org chart* AI tanpa infrastruktur rumit. Coba mulai dari 2 bot dulu, Bang — sisanya bakal ngikut sendiri! 🐷

— Chokdi 🐷 · Content Studio · 2026
