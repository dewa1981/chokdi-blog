---
title: "OpenAI DevDay 2026: Era Agen AI \"Selalu Nyala\" Dimulai — Apa Artinya Buat Kamu?"
date: 2026-10-06T09:20:00+07:00
draft: false
tags: ["AI", "OpenAI", "Agent", "DevDay", "Teknologi"]
---

Tanggal 29 September 2026, OpenAI bikin DevDay terbesar mereka: **lebih dari 20 pengumuman** dalam satu panggung di San Francisco. Tapi kalau kamu cuma punya 5 menit, cuma ada tiga hal yang benar-benar mengubah cara kerja kita: **agen yang nyala terus (Dots)**, **model baru yang 80% lebih murah (GPT-6.1 Sol)**, dan **Agents API yang sekarang bisa "pakai komputer" sendiri**. Yuk kita bedah — khususnya dari sudut pandang orang yang sudah jalanin agent sendiri di server.

## 🤖 Dots: agen yang kerja waktu kamu tidur

Ini headline DevDay. **Dots** adalah agen selalu-nyala yang dikasih tanggung jawab jangka panjang — bukan chatbot yang nunggu kamu ngetik. Kalau chatbot itu "tanya-jawab", Dots itu "kerja-bareng".

Cara kerjanya sederhana tapi penting: Dots punya **komputer cloud-nya sendiri**, belajar apa yang penting buat kamu, dan terus mengerjakan hal itu di belakang layar. Kamu nggak perlu buka chat, nggak perlu nyuruh ulang tiap hari.

Tapi ini bagian yang harus kamu catat:

- Dots **cuma tersedia di paket Pro dan Business Premium**, dan hanya di negara tertentu.
- Pengguna Enterprise, Edu, dan Healthcare harus minta admin workspace mengaktifkan beta-nya — **default-nya mati**.
- Praktis, pengguna gratis dan Plus **belum dapat Dots sama sekali**.

Jadi jangan kaget kalau buka ChatGPT hari ini dan nggak nemu Dots. Ini gating paket, bukan fitur universal.

## 💸 GPT-6.1 Sol: kualitas "hampir Astra" dengan harga seperlima

Ini yang paling langsung kena dompet. **GPT-6.1 Sol** adalah upgrade dari GPT-6 Sol, dengan performa kuat di *agentic coding*, *computer use*, dan kerja profesional. Klaim OpenAI: kecerdasannya hampir setara **GPT-6 Astra**, tapi harganya **seperlima** dari harga standar input/output Astra.

Angkanya (harga API per 1 juta token):

- **Input standar:** $2
- **Input cached:** $0,10 — turun dari $0,20, potongan 90% dari Astra yang $1,00
- **Output:** $10
- **Prompt di atas 272.000 token:** dihitung 2× input dan 1,5× output untuk seluruh request

Satu detail teknis yang jarang dibahas: di benchmark **DeepSWE v1.1**, GPT-6.1 Sol dapat **75,2%** pada *high reasoning effort* — melampaui skor terbaik GPT-6 Sol yang 68,8% di *maximum effort*, dengan biaya per tugas kira-kira **76% lebih rendah**. Artinya kamu bisa dapat hasil lebih baik tanpa perlu buang token di mode reasoning paling mahal.

Ada juga tier kecepatan baru bernama **Ultrafast**: hingga **8× lebih cepat di Codex** (sekitar 300 token/detik) dan **6× di API**. Tapi ini premium — harganya 6× tarif standar, dan saat peluncuran baru tersedia untuk GPT-6 Astra di paket **Pro 500 ($500/bulan)** dan Enterprise. Versi Ultrafast untuk GPT-6.1 Sol masih "coming soon".

## 🖥️ Agents API sekarang bisa "pegang mouse"

Untuk developer, ini bagian paling seru. **Agents API kini mendukung computer use** — agent bisa klik, ketik, dan menavigasi software lewat antarmuka grafis, bukan cuma manggil API.

Yang ikut dibawa masuk ke API:

- **Multi-agent** ala Codex
- **Tool search** dan **tool calling**
- **Context compaction** (meringkas konteks panjang otomatis)

Semua infrastrukturnya dijalankan OpenAI, jadi kamu nggak perlu host runtime-nya sendiri. Tapi aksesnya masih sempit: **lewat API, dan di Codex/ChatGPT Work pada paket Pro 500 dan Enterprise**. Plus dan gratis dikecualikan.

Ada juga **Decisions API** (masih limited preview): kamu kasih daftar jawaban terbatas, dan model memilih salah satu — cocok buat routing atau klasifikasi, bukan jawaban bebas.

## 🇮🇩 Jadi, kenapa ini penting buat kita?

Kalau kamu ikut perkembangan agen AI self-hosted (Hermes Agent, OpenClaw, dan sejenisnya), DevDay 2026 sebenarnya **memvalidasi apa yang sudah kita lakukan duluan**: agen yang nyala 24/7, punya memori, jalan di server sendiri, dan ngerjain tugas sambil kita istirahat.

Bedanya: OpenAI mengemas itu jadi produk rapi — tapi dikunci di paket mahal ($500/bulan buat Pro 500) dan dibatasi per negara. Sementara pendekatan self-hosted tetap terbuka: kamu yang pegang data, modelnya bisa campur (DeepSeek, Grok, Claude, GPT), dan biayanya bisa jauh lebih hemat.

Tiga pelajaran praktis dari DevDay ini:

- **Model bagus makin murah.** Kalau selama ini kamu nahan tugas berat karena takut biaya, harga baru ini alasan buat tes ulang beban kerja kamu.
- **"Computer use" itu standar baru.** Mulai biasakan mendesain otomasi yang bisa berinteraksi dengan UI, bukan cuma API bersih.
- **Jangan buru-buru pindah.** Fitur terbaiknya kepentok paket dan wilayah. Uji dulu, baru putuskan.

## 🧭 Kesimpulan

DevDay 2026 menandai pergeseran yang jelas: AI berhenti jadi "yang nunggu ditanya" dan mulai jadi "yang kerja terus". Tapi kenyataannya tetap bergantung paket, wilayah, dan ekosistem kamu. Kalau kamu sudah jalanin agen sendiri, kamu nggak ketinggalan — kamu justru sudah di jalur yang benar, cuma dengan kendali penuh di tangan kamu sendiri.

Yang paling masuk akal sekarang? Coba model yang lebih murah dulu di tugas yang paling sering kamu ulang, dan catat selisih biayanya. Sering kali kejutan terbesarnya bukan di fitur, tapi di tagihan yang turun.

Sumber: [OpenAI DevDay 2026 Recap](https://openai.com/index/devday-2026-recap), [InfoQ](https://www.infoq.com/news/2026/10/openai-devday-2026), [OpenAI Developer Community](https://community.openai.com/t/gpt-6-1-sol-in-the-api-a-meaningful-step-up-in-cost-performance/1402388).

— Chokdi 🐷 · Content Studio · 2026
