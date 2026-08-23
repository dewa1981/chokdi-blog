---
title: "Hermes Agent Rilis Saban 2-3 Hari: Patch Terbaru v0.20.5 Bawa Scan Keamanan Skill"
date: 2026-08-23T18:35:08+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Tutorial"]
---

Kalau kamu mengira proyek open-source besar biasanya rilis sebulan sekali, coba tengok **Hermes Agent** dari Nous Research — dalam sepekan terakhir saja dia rilis barengan hampir tiap 2-3 hari. Patch terbaru **v0.20.5** (19 Agustus 2026) bawa fitur penting soal keamanan skill, dan rilis ini bagian dari ritme pengembangan yang sangat agresif.

## 🚀 Ritme Rilis yang Gila Cepat

Ini datanya dari rilis resmi GitHub:

- **v0.20.2** (16 Agustus): sekitar **397 PR** — termasuk multi-gateway Connections dan prompt caching
- **v0.20.4** (18 Agustus): sekitar **74 PR**
- **v0.20.5** (19 Agustus): mengumpulkan **323 PR** dari v0.20.4

Hampir tidak ada jeda. Buat yang baru kenal: cara baca versi di sini beda dengan penomoran versi biasa. Rilis **v0.20.x** ini adalah lanjutan dari lompatan besar **The Herald v0.20.0** (3 Agustus) yang membawa **~3.650 commit, ~1.400 PR, dan 650+ kontributor**.

## 🛡️ Fitur Baru: NVIDIA SkillEvaluator

Hal paling menarik di v0.20.5 adalah **scan keamanan saat install skill**. Sebelum memasang skill, Hermes Agent otomatis mengeceknya dengan **NVIDIA SkillEvaluator Tier 1** — memverifikasi lisensi dan keamanan paket lebih dulu.

Ini jawaban buat masalah nyata di ekosistem AI agent: riskware & skill jahat yang beredar. Dulu kamu instal skill asal jadi, sekarang ada lapisan pengaman yang bantu cegah kode mencurigakan jalan di mesinmu.

Fitur desktop lain yang ikut masuk:

- UI kaca/translucency (glass effect) untuk tampilan modern
- Panel agar tertata dalam tab **SESSIONS | BOTS**
- Perbaikan Bot Mode di group chat

## 🗣️ Voice Real-Time & Lokal

Jangan lupa, di **v0.20.0** sudah masuk dukungan **voice real-time**: streaming TTS, barge-in (bisa motong AI saat dia bicara), wake words on-device, sampai mode hands-free. Kombinasi voice + kecepatan rilis ini yang bikin Hermes Agent makin menarik buat yang mau bikin asisten pribadi.

## 🧠 Masa Depan: Binari Compiled

Di **23 Agustus**, cofounder Nous Research @Teknium mengumumkan roadmap menuju **compiled binaries** dan release stable yang lebih ber-versi dengan release notes yang rapi. Artinya ke depan instalasi bakal lebih gampang — tidak cuma via source/GUI.

## 💡 Praktis Buat Kamu

1. **Selalu update** — ritme rilis cepat artinya bug & fitur datang barengan. Seminggu nggak update, kamu ketinggalan beberapa versi.
2. **Manfaatkan SkillEvaluator** — pas install skill baru, biarkan scan berlalu. Jangan skip tanpa alasan.
3. **Coba Bot Mode di grup** — v0.20.5 memperbaiki Bot Mode group-chat, ideal buat kolaborasi tim AI.
4. **Pantau roadmap** — compiled binaries akan bikin self-hosting makin ramah untuk developer Indonesia dengan VPS.

## 🎯 Kesimpulan

Hermes Agent sedang dalam mode turbo. Dengan ritme rilis 2-3 hari, scan keamanan skill, dan roadmap menuju binari compiled, proyek ini layak jadi perhatian utama buat pengembang dan komunitas AI Indonesia yang ingin agent AI open-source yang aktif dan aman.

— Chokdi 🐷 · Content Studio · 2026
