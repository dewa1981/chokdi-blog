---
title: "Anthropic Bekuk Hacker Rusia & 7 Lab Cina: Agent AI Kini Menyerang Otomatis"
date: 2026-09-11T18:20:00+07:00
draft: false
tags: ["AI Agent", "Keamanan", "Anthropic", "Berita"]
---

Selama ini kita menganggap AI cuma "asisten pintar" — yang diberi tugas lalu menunggu perintah berikutnya. Laporan baru Anthropic membalik anggapan itu: dalam 8 bulan terakhir, mereka membekukan **operasi serangan siber dan riset senjata biologi yang dijalankan oleh agent AI**, bukan oleh manusia yang mengetik satu-satu. Manusia cuma menetapkan target, lalu pergi tidur.

Laporan **"Detecting and countering misuse of AI: September 2026"** dirilis Kamis, 10 September 2026. Isinya merangkum kasus penyalahgunaan Claude antara **Desember 2025 sampai Agustus 2026** di tujuh area bahaya: operasi siber, operasi pengaruh, pengawasan, penipuan, penyalahgunaan biologis, pengembangan senjata konvensional, dan *distillation* (pencurian kemampuan model).

## 🕵️ GTG-20006: Malware yang Menulis Ulang Dirinya Sendiri

Kasus paling mencolok adalah **GTG-20006**, aktor yang atribusinya konsisten dengan **Midnight Blizzard** — grup spionase yang oleh pemerintah AS dikaitkan dengan SVR Rusia. Salah satu operatornya memakai handle "JackPoterz".

Yang bikin kasus ini berbeda: mereka tidak memakai Claude untuk bertanya soal cara hack. Mereka membangun **workflow AI yang mendeteksi kapan malware-nya tertangkap sistem keamanan, lalu otomatis menulis ulang kode itu sampai tidak terdeteksi lagi.** Siklus evasion yang dulu butuh analis manusia sekarang jalan sendiri di server hosting sekali pakai.

Hasilnya:

- **Lebih dari 20 organisasi** jadi target pengintaian dan operasi aktif: kementerian, badan intelijen, kedutaan, think tank, perusahaan industri pertahanan — terkonsentrasi di Ukraina dan Eropa.
- Sasaran utama: **staf pemerintah, militer, dan diplomatik Ukraina**. Mereka memindai layanan email dan sistem akses jarak jauh di **lebih dari dua lusin organisasi pemerintah Ukraina**.
- Target kedua: **rantai pasok drone**. Kotak surat minimal dua produsen komponen drone diekspor massal, dan satu **SDK software vision drone dicuri utuh** lalu dibongkar beberapa hari untuk mengambil arsitektur produk, bill of materials, sampai detail produk yang belum diumumkan.
- Taktiknya termasuk phishing, pembajakan Wi-Fi hotel, dan pengambilalihan WhatsApp.
- Menurut Anthropic, manusia terlibat **terutama untuk mengubah skill Claude Code** yang menjalankan workflow itu — bukan untuk mengoperasikan serangan secara langsung.

Anthropic menegaskan: **"Penggunaan AI sudah melampaui tanya-jawab dengan chatbot, dan melibatkan framework multi-agent"** yang mengeksekusi rekognisi, eksploitasi, dan eksfiltrasi data. Kerangka ofensif open-source seperti **PentAGI** mereplikasi sebagian besar scaffolding yang sama untuk siapa pun yang mau mengunduhnya.

## 💸 151 Juta Percakapan: Distilasi Ilegal Skala Industri

Di sisi lain, Anthropic menyatakan memutus serangan dari **tujuh lab berbasis di Cina**, termasuk **Alibaba, Moonshot, DeepSeek, dan Xiaomi**:

- Operasi yang dikaitkan dengan **Alibaba** disebut sebagai serangan **illicit distillation terbesar**: lebih dari **151 juta pertukaran** tercatat antara Mei–Juli 2026, memuncak hampir **3 juta per hari** dari **lebih dari 3.500 akun** yang dinilai fraudulent. Tujuannya mengekstrak kemampuan model Claude untuk memperbaiki model Qwen mereka.
- **Xiaomi** tercatat lebih dari **400.000 pertukaran dalam 20 hari** (Maret–April 2026).
- **Moonshot (pembuat chatbot Kimi) dan DeepSeek** dituding **melewatkan percakapan pelanggan langsung mereka** — yang kadang berisi informasi sensitif — melalui Claude, lalu memakai responsnya sebagai data latih. **MiniMax** membangun jaringan proxy via perusahaan cangkang yang hanya menawarkan model Anthropic dan OpenAI; **SenseTime** membeli transkrip percakapan user dari vendor data pihak ketiga.

Kementerian Luar Negeri Cina menyatakan tidak mengetahui laporan ini dan menolak "distorsi fakta serta smear" terhadap negaranya. Alibaba, Moonshot, DeepSeek, dan Xiaomi tidak memberi komentar saat diminta Reuters.

## ☣️ Senjata Biologis dan Senjata Konvensional

Laporan yang sama mendokumentasikan **lima contoh ilmuwan memakai Claude dengan cara yang bisa mendukung pengembangan senjata biologi**. Salah satunya: seorang peneliti di wilayah yang tidak didukung Anthropic (daftar itu termasuk Rusia, Cina, Korea Utara) memakai infrastruktur VPS untuk mengakses Claude dan **berminggu-minggu merencanakan eksperimen adaptasi mamalia pada virus flu burung**. Akun terkait diblokir.

Selain itu, operator di **Cina, Rusia, dan Yaman** memakai Claude untuk "mengembangkan software senjata konvensional — termasuk senjata api, misil, drone bersenjata, bom, dan sistem penargetan serta kendali yang mengoperasikannya."

## 🎯 Pelajaran buat Kita yang Menjalankan Agent Sendiri

Kita tidak punya tim threat intelligence. Anthropic sendiri menahan laju ini dengan meringkas penalaran internal model, menambah lapisan "preserved thinking", dan meminta verifikasi identitas untuk akun bermasalah — tapi pertahanan paling dasar tetap ada di tangan kita:

- **Skill dan plugin = permukaan serangan.** Di GTG-20006, manusia justru turun tangan mengedit *skill* Claude Code yang menggerakkan workflow. Kalau kamu nginstal skill pihak ketiga, kamu sedang menjalankan kode orang lain — cerita [malware yang menyusup lewat skill OpenClaw](https://chokdi.ano99.com/posts/openclaw-clawhavoc-malware-skill/) bukan fiksi.
- **API key itu bukan sebatas biaya.** Akun yang dipakai lewat key curian sudah jadi salah satu jalur yang dilaporkan. Simpan di secret manager — lihat [pelajaran saat API key bocor di Cloud PC](https://chokdi.ano99.com/posts/jangan-install-hermes-di-cloud-pc-grok-bot-api-key/).
- **Jangan lewatkan data pelanggan ke model pihak ketiga tanpa aturan.** Kasus Moonshot–DeepSeek adalah pengingat: percakapan user bisa berakhir sebagai data latih orang lain.
- **Batasi izin agent dan catat semua aksinya.** Multi-agent memperbesar blast radius; kalau satu agent bisa mengubah kodenya sendiri tanpa jejak, kamu tidak akan tahu apa yang sudah terjadi. Bandingkan [5 mode eksekusi agent](https://chokdi.ano99.com/posts/5-mode-eksekusi-hermes/) dan pilih yang paling terkunci.

Kabar buruknya: "serangan canggih tidak lagi butuh penyerang canggih". Kabar baiknya: pertahanan paling dasar — higienitas kredensial, minim izin, log yang bisa dibaca — masih menahan sebagian besar kasus.

**Sumber:** [Anthropic — Detecting and countering misuse of AI: September 2026 (10 Sep 2026)](https://www.anthropic.com/threat-intelligence-report-september-2026) · [PDF laporan lengkap](https://www-cdn.anthropic.com/e50be2e51e7695dc4b1366a37a245a597377d3b5/Anthropic-Detecting-and-countering-091026.pdf) · [Reuters, 10 Sep 2026](https://www.reuters.com/legal/litigation/anthropic-disrupts-russian-chinese-ai-campaigns-targeting-its-claude-models-2026-09-10/)

Menurut kamu, tanggung jawab utama menahan penyalahgunaan agent ada di tangan developer model, atau di tangan kita yang memasang agent di server sendiri? Tulis pendapatmu di kolom komentar.

— Chokdi 🐷 · Content Studio · 2026
