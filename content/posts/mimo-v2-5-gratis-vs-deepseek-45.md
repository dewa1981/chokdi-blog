---
title: "MiMo V2.5 vs DeepSeek: 1,32 Miliar Token Gratis & 3 Salah Diagnosa"
date: 2026-09-18T18:10:00+07:00
draft: false
tags: ["AI", "Model", "Self-Hosted"]
---

Kami hampir menulis kesimpulan yang salah ke dalam catatan sistem: "model MiMo menolak kerjaan kita, jadi harus pakai DeepSeek." Untung dicek ulang. Setelah ditelusuri, penyebabnya **bukan** kemampuan modelnya — tapi tiga kesalahan di sisi kami sendiri. Satu di antaranya membakar $45 tanpa perlu.

## Masalahnya: ekstraksi memori agent yang mahal

Setiap bot punya lapisan memori jangka panjang. Prosesnya sederhana: percakapan masuk → model mengekstrak fakta, entitas, dan pengalaman → disimpan sebagai berkas terstruktur. Pekerjaan ini tidak butuh model jenius, tapi volumenya besar: satu bot bisa mengirim puluhan ribu permintaan per bulan.

Awalnya semua dijalankan dengan DeepSeek. Hasilnya bagus, tapi tagihannya nyata. Setelah kami buka database gateway (`usageHistory`), angkanya seperti ini:

| Model | Request | Token input | Biaya |
|---|---|---|---|
| `xmtp/mimo-v2.5` | 52.198 | 1.324.909.981 | **$0.0000** |
| `xmtp/mimo-v2.5-pro` | 1.959 | 191.704.312 | **$0.0000** |
| `ds/deepseek-v4-flash` | 31.874 | 2.496.770.084 | **$45.08** |

**1,32 miliar token** lewat MiMo, biayanya nol. Bukan karena gratisan tanpa dasar: modelnya masuk paket langganan bulanan (Token Plan), jadi biaya marginalnya nol selama kuota belum habis. Kalau dihitung per token, DeepSeek memakan ~$45 untuk volume yang lebih kecil.

## Kenapa biayanya bisa nol

Dari [dokumentasi resmi MiMo](https://mimo.mi.com/docs/tokenplan/subscription), Token Plan punya empat tingkat: Lite $6/bulan (4,1 miliar credit), Standard $16 (11 miliar), Pro $50 (38 miliar), Max $100 (82 miliar). Selain itu:

- **Cache hit 50x lebih murah.** Konversi credit per token untuk `mimo-v2.5`: input kena cache = 2 credit, input luapan cache = 100 credit, output = 200 credit. Karena prompt ekstraksi memori polanya berulang, rasio cache hit tinggi — dan di sinilah paket langganan jadi jauh lebih murah dibanding bayar per token.
- **Diskon 0,8x di jam off-peak** (00:00–08:00 Beijing = 16:00–24:00 UTC). Pipeline yang bisa dijadwalkan malam sebaiknya dijadwalkan malam.
- **Satu paket menutup 6 model**: `mimo-v2.5-pro`, `mimo-v2.5`, plus varian ASR dan TTS.
- Modelnya sendiri bukan kelas ecek-ecek: MiMo-V2.5 adalah MoE sparse 310B parameter (15B aktif), konteks 1,1 juta token, dan natif omnimodal — di [OpenRouter](https://openrouter.ai/xiaomi/mimo-v2.5) skornya GPQA Diamond ~82,8% dan TAU-Bench Airline ~73%.

## 3 salah diagnosa yang bikin kami salah paham

Ini bagian yang lebih berguna daripada angka di atas, karena polanya bisa kejadian ke siapa saja yang mengurus agent.

**1. Bentuk argumen salah, bukan modelnya salah.** Tool `remember` menerima larik `messages` berisi objek `{role, content}` — bukan field `content` langsung. Kami kirim bentuk yang salah, balasannya `1 validation error ... messages Field required`. Lalu dibaca sebagai "model menolak". Pelajaran: error validasi schema itu urusan kita, bukan urusan model.

**2. Header MCP kurang satu.** Endpoint `/mcp` menolak `Accept: application/json` sendirian dengan HTTP 406: *"Client must accept both application/json and text/event-stream"*. Ini perilaku spec MCP Streamable HTTP, berlaku untuk semua server — bukan keanehan model tertentu.

**3. Yang diuji beda tugas.** Tes lama meminta model **membuat konten promosi**. Ditolak — dan itu wajar, karena banyak model punya batas jenis tugas seperti itu; di komunitas pun ada laporan serupa soal MiMo menjawab *"the request was rejected because it was considered high risk"*. Masalahnya, tugas produksi kami bukan membuat konten, tapi **mengekstrak memori**. Untuk tugas itu MiMo jalan sempurna.

Urutan diagnosa yang benar kalau model "menolak": **(1) bentuk payload → (2) header/protokol → (3) tugas yang diuji → (4) baru kualitas atau guardrail model.** Tiga langkah pertama penyebabnya ada di kita.

## Bukti setelah konfigurasi dibetulkan

Setelah skema dan header diperbaiki, seluruh uji dasar lolos:

- **`remember`** dengan data produksi → `Stored 1 message(s) and committed for memory extraction`
- **`find`** kueri semantik → `Found 2 item(s)`
- **`tree`** isi memori → **33 entri**, termasuk kategori `entities/`, `experience/`, `persona/`, dan `note/`
- **Log container** → **0 error, 0 penolakan**

Artinya ekstraksi *dan* klasifikasi jalan. Struktur memori yang terbentuk rapi, bukan sekadar tumpukan teks.

## Yang kami ubah di aturan operasi

1. **Pisahkan peran model.** Model ekstraksi/memori → pakai yang masuk paket langganan (biaya marginal nol). Model konten → pakai yang memang menerima brief kita apa adanya.
2. **Jangan simpulkan "model X menolak" dari satu prompt.** Satu tes dengan tugas yang salah tidak membuktikan apa pun. Uji dengan skema dan tugas yang benar dulu.
3. **`find` yang kosong bukan berarti gagal.** Pencarian memori peka kemiripan semantik; kueri yang jauh dari teks sumber memang bisa nihil. Verifikasi isi memori pakai `tree`, bukan cuma `find`.
4. **Catat angka biaya per model dari database**, bukan dari perasaan. Selisih $45 vs $0 cuma kelihatan kalau di-query.

Kalau kamu juga menjalankan beberapa agent dengan memori jangka panjang, cek dulu tagihan per model di gateway-mu sebelum memutuskan pindah model — bisa jadi yang salah bukan modelnya. Baca juga pembahasan kami soal [Mem0 MCP vs Hindsight MCP](/posts/mem0-mcp-vs-hindsight/) kalau sedang memilih lapisan memorinya, dan [audit Hermes Control Interface](/posts/audit-hermes-control-interface-hci/) kalau mau memantau token per model dari dashboard.

Punya pengalaman serupa — salah diagnosa model padahal bug-nya di harness sendiri? Tulis di komentar.

**Sumber:** [MiMo Token Plan](https://mimo.mi.com/docs/tokenplan/subscription) · [MiMo-V2.5 di OpenRouter](https://openrouter.ai/xiaomi/mimo-v2.5) · [volcengine/OpenViking](https://github.com/volcengine/OpenViking)

— Chokdi 🐷 · Content Studio · 2026
