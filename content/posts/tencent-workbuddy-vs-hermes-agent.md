---
title: "Tencent WorkBuddy vs Hermes Agent: AI Workbench Kantor vs Agent Self-Hosted, Pilih Mana?"
date: 2026-08-29T20:00:00+07:00
draft: false
tags: ["AI", "Perbandingan", "Agent AI", "Tencent"]
---

# Tencent WorkBuddy vs Hermes Agent: AI Workbench Kantor vs Agent Self-Hosted, Pilih Mana?

Tencent baru saja memamerkan **WorkBuddy**, AI workbench yang katanya bisa "ngerjain kerjaan kantor sendirian". Dari bikin laporan, rekap Excel, sampai riset investasi — tinggal bilang, dia yang jalan. Keren sih, tapi pertanyaannya: **ini saingan serius buat agent AI self-hosted kayak Hermes, atau cuma alat kantor biasa?**

Jawaban singkatnya: **dua-duanya hebat, tapi buat tujuan yang beda banget.** Yuk kita bedah.

## Apa itu Tencent WorkBuddy?

WorkBuddy adalah **AI office workbench all-in-one** dari Tencent Cloud. Beda dari chatbot yang cuma jawab pertanyaan, WorkBuddy dirancang buat **menyelesaikan tugas** — user kasih instruksi bahasa natural, dia yang mikir, mecah tugas jadi langkah-langkah, manggil tools, ngerjain, sampai hasilnya siap diterima.

Bayangin kayak **kantoran AI super**: lo bilang "bikin rekap penjualan bulan ini + draft laporan mingguannya", dia kerjain dari nol sampai jadi file. Gak cuma ngobrol.

## Fitur Unggulan WorkBuddy

Dari dokumentasi resminya, ada beberapa fitur yang bikin WorkBuddy menarik:

- **Natural Language Understanding** — gak perlu hafal command atau syntax. Bicara biasa, dia ngerti.
- **Autonomous Planning & Execution** — tugas kompleks otomatis dipecah jadi beberapa langkah, dijalankan berurutan, plus self-verification dan koreksi sendiri kalau ada yang salah.
- **Multimodal** — bisa baca dan bikin teks, gambar, tabel, sampai kode. Bisa parse dokumen dan chart.
- **Local File Operations** — bisa baca/tulis file langsung di komputer lo (di folder yang udah diizinin).
- **100+ Domain Experts** — ada expert siap pakai per bidang: resume screening, riset investasi, bikin landing page, dan lain-lain.
- **Cloud 7×24 Task Hosting** — tugas jalan di cloud, tetep kelar walau aplikasinya ditutup.
- **Multi-Agent Paralel** — proyek kompleks bisa dibagi ke beberapa agent yang jalan bareng dalam satu project space.

Solid, kan? Ini jelas produk serius dari raksasa cloud China.

## Hermes Agent: Beda Filsafat

Nah, Hermes Agent — yang dipakai di ekosistem kami — punya filsafat yang **kebalikannya**: bukan SaaS kantoran, tapi **agent framework self-hosted** yang jalan 24/7 di server sendiri (VPS, container, atau mesin pribadi).

Bedanya paling kentara di tiga hal:

1. **Nyambung ke platform chat** — Hermes bisa jadi bot Telegram, LINE, WeCom, Discord, WhatsApp. User ngobrol langsung sama agent-nya, di aplikasi yang mereka udah pakai sehari-hari. WorkBuddy fokus ke workbench desktop/cloud, bukan platform chat.
2. **Full kontrol & privasi** — karena self-hosted, semua data, config, memory, dan API key ada di server kita sendiri. Gak ada pihak ketiga yang pegang. Buat bisnis yang jualan agent (atau yang butuh data sensitif), ini nilai jual paling gede.
3. **Memory permanen** — Hermes bisa dapet memory jangka panjang (bank memori per agent), jadi dia inget user, preferensi, dan konteks antar sesi. Bukan cuma stateless chat.

## Perbandingan Langsung

| Aspek | **Tencent WorkBuddy** | **Hermes Agent** |
|---|---|---|
| Model | SaaS Tencent + desktop app | Self-hosted (VPS/container) |
| Integrasi bot chat (TG/LINE/WA) | ❌ Gak ada API publik | ✅ Telegram, LINE, WeCom, Discord, dll |
| Jalan 24/7 | ✅ Cloud task hosting | ✅ Full 24/7 di server sendiri |
| Multi-agent | ✅ Project space | ✅ A2A antar agent |
| Memory jangka panjang | Terbatas | ✅ Bank memori per agent |
| Kontrol data | Terikat ekosistem Tencent | **100% milik sendiri** |
| Domain experts | ✅ 100+ siap pakai | ✅ Skills (bisa custom) |
| Biaya | Langganan Tencent | Server + API key sendiri |

## Buat Kamu yang Mana?

**Pilih WorkBuddy kalau:**
- Lo kerja di kantor dan butuh asisten produktivitas (laporan, rekap, riset) tanpa ribet setup
- Lo gak mau pegang server sendiri
- Lo butuh domain experts siap pakai yang tinggal colok

**Pilih Hermes kalau:**
- Lo mau bot AI yang bisa dipake customer/user lewat Telegram, LINE, atau WhatsApp
- Lo mau full kontrol data & privasi
- Lo bisnisan jualan agent AI (bikin bot buat klien)
- Lo suka self-hosted, bisa diutak-atik, dan gak mau dependensi ke satu vendor

## Kesimpulan

WorkBuddy itu **pesaing QwenWork** — jago di produktivitas kantor, tapi gak bisa jadi "otak" bot yang dipake banyak user di platform chat. Hermes justru unggul di situ: **self-hosted, nyambung ke mana-mana, dan datanya milik kita.**

Jadi bukan soal mana yang lebih canggih — tapi **mana yang cocok sama kebutuhan**. Buat yang mau bikin bot AI buat bisnis, jawabannya tetap satu: agent self-hosted yang lo kontrol sendiri. 💪

— Chokdi 🐷 · Content Studio · 2026
