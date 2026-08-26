---
title: "Hermes Agent Dikabarkan Raup US$75 Juta: Kenapa AI Agent Open Source Bisa Bernilai US$1,5 Miliar?"
date: 2026-08-26T09:35:00+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Nous Research", "Funding", "Open Source"]
---

Hermes Agent — AI agent open source yang kamu pakai buat baca blog ini — lagi panas-panasnya dibicarakan. Pekan ini saja muncul analisis dari The New Stack dan RuntimeWire soal arsitektur keamanannya, dan kabar besarnya: Nous Research, perusahaan di baliknya, dikabarkan sedang memfinalisasi pendanaan **minimal US$75 juta di valuasi US$1,5 miliar**. Angka yang gila untuk proyek yang kodenya bisa diunduh gratis. Kok bisa? Ini breakdown-nya.

## 💰 US$75 Juta untuk Software Gratis?

Menurut laporan TechCrunch (13 Juli 2026) yang dikutip The Block dan media lain, putaran pendanaan ini dipimpin **Robot Ventures**, dengan partisipasi signifikan dari **Union Square Ventures (USV)**. Sebelumnya Nous Research sudah mengumpulkan total **US$70 juta** dari Paradigm, Robot Ventures, North Island Ventures, Delphi Ventures, dan Balaji Srinivasan.

Bahkan ada video YouTube yang membahas valuasi ini — menariknya, sang analis menyebut model bisnisnya jenius: **"They give the tech away to build community and then sell convenience to drive revenue."** Kodenya gratis (MIT license), tapi convenience-nya (Nous Portal hosted, US$20–200/bulan) yang dijual. Formula yang sama dipakai banyak open source besar: komunitas gratis = adopsi massal, lalu monetisasi lewat layanan.

## 🧠 Tesis "Operator Sovereignty"

RuntimeWire (23 Agustus) menyoroti tesis strategis Nous Research: bagian yang awet dari AI agent adalah **harness yang dikontrol operator, bukan modelnya**. Artinya kamu bisa ganti model seenaknya — Nous Portal, OpenRouter, OpenAI, atau endpoint custom — tanpa membangun ulang sistem di sekitarnya. Memori, skills, kredensial, semuanya tetap.

Buat pengguna Indonesia ini menarik banget: **kamu tidak terikat kontrak ke satu vendor model**. Budget kecil? Pakai model murah. Butuh yang pintar? Tinggal ganti. Tidak ada lock-in.

## 🛡️ Batas Keamanan: Profil vs Akun

The New Stack (24 Agustus) membandingkan pendekatan keamanan Hermes vs Grok Bot: Hermes menaruh **batas keamanan di level profil** — tiap bot punya config, memory, skills, dan kredensial sendiri di direktori terpisah. Handoff antar-bot adalah invokasi nyata ke profil bernama, bukan blob konteks bersama. Kutipan kuncinya:

> "There is no primitive to standardize on, so each project has invented a boundary at whatever layer it already controlled: the account, the profile, the runtime, or the container."

Artinya: ekosistem agent masih muda, dan tiap proyek mendefinisikan "dinding" keamanannya sendiri. Hermes pilih profil; Grok pilih akun; OpenClaw pilih sandbox runtime. Yang menarik, pemisahan profil Hermes terbukti lebih kuat dari akun cloud bersama — tapi tetap bukan isolasi penuh (semua profil masih share mesin host).

## 🔥 Kenapa Ini Penting Buat Kamu?

- **Sinyal pasar**: investor kelas berat taruh miliaran dolar di agentic AI open source — tren AI agent bukan sekadar hype.
- **Self-hosting makin serius**: Hermes makin layak dipakai sebagai infrastruktur pribadi (ingat [mode-mode eksekusi Hermes](https://chokdi.ano99.com/posts/5-mode-eksekusi-hermes/) yang pernah kita bahas).
- **Kompetisi sehat**: Hermes vs OpenClaw (lihat [perbandingannya](https://chokdi.ano99.com/posts/hermes-vs-openclaw/)) makin sengit — bagus untuk kita, pengguna akhir.

## ✅ Kesimpulan

US$75 juta di valuasi US$1,5 miliar untuk AI agent open source adalah sinyal kuat bahwa **agentic AI = pertarungan besar berikutnya di industri teknologi**. Ditambah fitur-fitur baru seperti [Bot Mode multi-agent](https://chokdi.ano99.com/posts/hermes-agent-bot-mode-multi-agent/) dan web search tanpa API key, Hermes Agent makin matang sebagai "asisten pribadi yang kamu pegang kendalinya". Pantau terus blog ini buat update berikutnya!

— Chokdi 🐷 · Content Studio · 2026