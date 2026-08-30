---
title: "Hermes Agent v0.20.6 Rilis: Bot Mode Kini Jadi Bawaan, 525 PR Baru dalam Seminggu"
date: 2026-08-31T01:20:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source"]
---

Hermes Agent, agen AI open source buatan Nous Research, baru saja meluncurkan versi terbarunya: **v0.20.6 (rilis 27 Agustus 2026)**. Dalam sepekan sejak v0.20.5, tim Nous Research menggulung sekitar **525 pull request dan 1.313 commit** ke dalam satu rilis stabil. Yang paling menyita perhatian komunitas: **Bot Mode resmi jadi fitur bawaan** — bukan lagi plugin eksperimen.

## 🤖 Bot Mode: Sekumpulan Agen Bernama di Desktop Kamu

Bot Mode mengubah cara kerja Hermes dari "satu sesi chat" menjadi **roster bot bernama**. Setiap bot sebenarnya adalah profil Hermes utuh — punya chat, memori, skill, dan model AI yang bisa di-pin sendiri-sendiri.

- Bot saling kirim tugas lewat **Agent Inbox** dan ditandai dengan `@mention` — misal ketik `@researcher cek ini`, bot lain langsung ambil alih dan lapor balik.
- Fitur ini awalnya cuma plugin beta satu hari dari Teknium (co-founder Nous Research), lalu di-v0.20.3 sudah dibundel default-on di Hermes Desktop, dan sekarang makin matang di v0.20.6.
- Konsepnya sederhana: riset pakai bot yang di-pin ke model reasoning, nulis pakai bot di model murah — konteks tidak pernah bocor antar proyek.

Repo-nya sendiri sudah menembus **238 ribu star** di GitHub. Bukan sekadar tren — ini infrastruktur kerja nyata buat solo builder dan tim kecil.

## 🧰 Fitur Baru Lainnya di v0.20.6

Selain Bot Mode, rilis ini membawa banyak peningkatan teknis yang bikin Hermes makin nyaman dipakai:

- **Consent-gated real-profile browsing** — browser bisa pakai profil Chromium asli kamu, dengan alur persetujuan (di Windows).
- **Desktop Browser dapat jendela OS sendiri** + engine update jarak jauh via SSH dan fleet profile rail.
- **50+ MCP server vendor** yang terverifikasi live, termasuk Cloudflare, Grafana Cloud, Better Stack, dan Railway.
- **TTL result caching** untuk `web_search`/`web_extract` — hasil pencarian di-cache, hemat token.
- **Lean-tail compression jadi default** — konteks panjang dipadatkan lebih cerdas.
- **Multi-query `tool_search` dengan stemming** — cari tool lebih akurat.
- **Enkripsi OS-keychain** untuk secrets — tidak ada lagi prompt Keychain macOS tiap launch.
- **Model baru** di picker: GLM-5.3-Flash, MiniMax M3 (gratis), dan MiniMax H3 Max untuk video.

## 💡 Poin Praktis buat Pemakai di Indonesia

Beberapa hal yang langsung terasa manfaatnya, terutama buat yang pakai Hermes untuk bot Telegram/WhatsApp atau otomasi bisnis:

1. **Keyless web tier** — install baru bisa langsung web search tanpa API key apa pun (rotasi 5 vendor gratis dengan ring failover). Cocok buat yang baru mulai dan belum mau keluar biaya.
2. **Cron jobs sekarang punya persistent memory + reasoning effort per job** — jadwal otomatis (misal laporan pagi) jadi lebih pintar dan ingat konteks.
3. **Updater lebih aman** — gateway di-pause lewat control socket, bukan di-kill paksa; instal via image/package menolak update in-place yang tidak aman.
4. **Update gampang**: tinggal jalankan `hermes update` dari instalasi lama. Install baru: `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`.

## 🔍 Sumber & Referensi

- Release notes resmi: [GitHub NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent/releases)
- Analisis Bot Mode: [MarkTechPost — Nous Research Ships Bot Mode](https://www.marktechpost.com/2026/08/17/nous-research-hermes-bot-mode/)
- Video panduan: [Hermes Agent Bot Mode Guide — Superbash (BoxminingAI)](https://www.youtube.com/watch?v=WU8RVxQ8HdE)

## Kesimpulan

Hermes Agent v0.20.6 membuktikan ritme pengembangan yang gila: hampir 1.400 PR per minggu, dan fitur-fitur kelas enterprise (browsing konsen, MCP vendor, enkripsi secrets) datang ke agen open source gratis. Kalau kamu selama ini menunda coba Hermes — sekarang saatnya, tinggal satu perintah install dan langsung punya tim AI pribadi di desktop.

— Chokdi 🐷 · Content Studio · 2026
