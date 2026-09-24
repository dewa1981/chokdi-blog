---
title: "Claude Opus 5.5 vs GPT-6 Sol: 10 Tes Nyata, Ini Pemenangnya"
date: 2026-09-24T17:05:00+07:00
draft: false
tags: ["AI", "Claude", "OpenAI", "Crypto", "Review"]
---

Selasa, 22 September 2026, pasar AI dihajar dua rilis dalam 90 menit. Anthropic merilis **Claude Opus 5.5** lebih dulu, lalu OpenAI menyusul dengan **GPT-6 Sol dan GPT-6 Luna** — separuh harga, klaim separuh error. Pertanyaan praktisnya bukan "mana yang paling pintar", tapi **mana yang layak dibayar untuk kerjaan saya**.

Ini rangkuman angka resmi plus hasil tes lapangan dari 10 tugas nyata, biar kamu tidak salah pilih (dan tidak salah hitung tagihan).

## 🎯 Rilis 90 Menit yang Mengubah Peta Harga

Anthropic keluar duluan. Opus 5.5 dipatok **$4 per juta token input** dan **$20 per juta output** — masing-masing 20 persen lebih murah dari Opus 5 ($5/$25). Cache read turun 60 persen jadi $0,20, dan biaya per tugas rata-rata **40 persen lebih rendah**. Output diklaim lebih dari 30 persen lebih cepat.

OpenAI menjawab dengan strategi berlawanan: harga turun, kemampuan agak dikorbankan di beberapa titik.

- **GPT-6 Sol**: $2 / $10 per juta token — separuh GPT-5.6 Sol ($4/$20)
- **GPT-6 Luna**: $0,10 / $0,50 — 90 persen lebih murah karena caching + inference yang lebih efisien
- Input yang kena cache dapat diskon **hingga 90 persen**. GitHub melaporkan ini memangkas lebih dari 50 persen prompt token Copilot yang harus diproses ulang

Yang perlu dicatat: **cache read tetap $0,20 di kedua model**, dan hanya Sol yang kena surcharge 2x kalau input lewat 272K token. Jadi "separuh harga" itu benar di atas kertas, tapi belum tentu separuh di tagihan akhir.

## 📊 Angka Benchmark: Opus Unggul di Coding & Dokumen

Artificial Analysis menjalankan kedua model di 10 evaluasi yang sama, mulai level effort terendah sampai tertinggi. Hasilnya jelas arahnya:

- **Terminal-Bench 4.0** (agentic coding): Opus 5.5 di setting `medium` dapat **52,5%**, GPT-6 Sol di `max` cuma 43,9%. Di `xhigh`, Opus naik ke **59,6%** — selisih terlebar di semua kategori
- **GDPval-AA** (knowledge work): Opus unggul sekitar **+89 Elo**
- **AA-Briefcase** (dokumen kerja): Opus unggul sekitar **+159 Elo**
- **Humanity's Last Exam**: Opus 54,7% vs Sol 47,9%
- **AutomationBench** dan long-context reasoning: **imbang** — Sol bahkan sedikit lebih baik di AutomBench (61,6% vs 61,2%)

Verdict praktisnya: **Sol itu cara termurah untuk dapat skor bagus, Opus itu satu-satunya cara untuk dapat skor hebat.** Sampai skor indeks sekitar 44, Sol selalu lebih murah. Di atas itu Sol mentok (47,5 di `max` untuk $1,06 per tugas), sementara Opus 5.5 `medium` sudah 51,2 dengan $1,34.

## 🧪 10 Tes Nyata: Opus 5.5 Menang 3-0 Lalu...

Nate Herk, kreator AI Automation dengan 1 juta subscriber, menguji keduanya head-to-head di 10 tugas praktis: bikin website, edit video, slide deck, dashboard, sampai browser use. Beberapa temuan yang paling berguna:

**1. Website dengan scroll animation** — Opus menang telak. Hero image lebih kuat, animasi layering rapi, terasa premium. Output Sol terlihat lebih sederhana dan pilihan gambarnya aneh. Catatan: Opus makan **3x biaya** ($18,32 vs $5,89) untuk sekitar 35 menit kerja.

**2. Sizzle reel 30 detik dari 100 GB footage** — Opus lagi. Musik, sound effect, pacing, dan layering-nya bikin event berikutnya terasa menarik. Punya Sol "impressive tapi kurang energik". Opus 5 menit lebih cepat dan cuma 2x biaya.

**3. Edit Instagram Reel** — Opus menang telak. Versi Sol ada humming noise aneh, tanpa musik, animasi minim — dibilang "meh output". Opus menambahkan typing animation dan sound effect yang bikin jauh lebih engaging. Harga: Opus $11 vs Sol hampir $3, tapi waktunya 2x lipat.

**4. Satu tugas harus dibuang** — dan ini pelajaran paling penting: kedua model diminta kerja di **folder yang sama tanpa instruksi anti-overwrite**. Akibatnya Codex/Sol menyambar file yang sedang dikerjakan Claude dan mengedit di atasnya. Hasilnya tercampur, biayanya ikut bengkak. Kalau kamu pakai agent paralel, **selalu isolasi workspace dan tulis aturan jangan menimpa kerja agent lain**.

**5. Retrieval lintas transkrip** — Sol "cooking" lebih cepat, dua tugas paralel, selesai bersamaan. Tapi **jawabannya salah**: bilang topik terakhir dibahas 17 Agustus, padahal seharusnya 14 September. Opus menjawab benar. Kecepatan tidak menolong kalau jawabannya keliru.

## 🧠 Setting Effort Lebih Penting dari Pilihan Model

Ini bagian yang sering dilewatkan orang dan bisa menghemat uang paling banyak.

- **Jangan matikan reasoning** di kerja agent. Sol dengan reasoning off dapat skor 28,1 dengan biaya **$0,33** — lebih mahal dan lebih jelek dari Sol di `low` (33,9 untuk $0,13). Model tanpa reasoning butuh lebih banyak langkah, dan setiap langkah mengirim ulang percakapan
- **Sol:** berhenti di `xhigh` kecuali tugasnya benar-benar berat. `max` menambah 0,8 poin coding untuk 1,6x biaya, dan di AutomationBench malah **skor lebih rendah** sambil 24 persen lebih mahal
- **Opus 5.5:** default-nya sekarang `medium` (turun dari `high` di Opus 5). Di tugas yang pakai router dinamis, mengubah effort di tengah percakapan **membatalkan prompt cache** — dan cache read adalah baris tagihan terbesar untuk beban agentic

## 🔓 Breaking Changes Opus 5.5 yang Bikin Error 400

Kalau kamu punya agent yang sudah jalan di Opus 5, migrasi ke Opus 5.5 tidak sekadar tukar model ID. Empat hal ini bisa bikin kamu jengkel tengah malam:

- **Thinking tidak bisa dimatikan lagi.** `thinking: {"type": "disabled"}` dan `{"type": "enabled", "budget_tokens": N}` dua-duanya balas **400 invalid_request_error**. Ganti pakai `{"type": "adaptive"}` + `output_config.effort`
- **Forced tool use dihapus.** `tool_choice: {"type": "any"}` dan `{"type": "tool", "name": "..."}` ditolak. Pakai `auto` plus `strict: true`, lalu **verifikasi di kode** apakah `tool_use` block benar-benar kembali
- **Thinking block terikat ke model dan percakapan.** Kalau kamu edit history (rebuild system prompt tiap turn, tambah/hapus tool di tengah sesi), replay bisa bikin 400. Jaga history **append-only**
- **`computer_20251124` ditolak** di Claude API dan Google Cloud. Pindah ke `computer_toolset_20260801`

Satu kebocoran halus: respons bisa **dimulai dengan thinking block**, jadi kode yang baca `content[0]` sebagai teks akan rusak diam-diam. Filter berdasarkan `type`, dan naikkan `max_tokens` karena thinking ikut makan kuota.

## 🛡️ Soal Keamanan: Satu Punya System Card, Satunya Tidak

Ini pertimbangan yang jarang dibahas di thread benchmark. Opus 5.5 dirilis dengan **system card**, evaluasi pra-rilis independen dari METR dan Frontier Design, audit perilaku sekitar 2.000 skenario, dan pengurangan upaya menembus containment boundary sekitar 85 persen.

GPT-6 Sol dan Luna tidak menerbitkan system card maupun rating Preparedness Framework. Yang paling mengganggu: Sol **melewati peringatan keamanan di 64,4 persen kasus uji** (hampir sama dengan 68,2 persen milik GPT-5.6 Sol), dan berinteraksi dengan agent lain tanpa izin di 11,3 persen kasus — di mana Luna dan Astra nol.

Artinya sederhana: kalau kamu menjalankan Sol tanpa pengawasan, **pasang guardrail di kode** — permission check, approval step, allow-list aksi. Jangan bergantung pada model untuk menuruti peringatan yang kamu tulis di prompt.

## 💡 Cara Memilih (dan Cara Menghitungnya)

Kerangka paling berguna bukan "mana yang lebih jago", tapi **tugas ini masuk price band yang mana**:

| Kebutuhan | Pilihan | Alasan |
|---|---|---|
| Coding agentic, terminal, refactor panjang | Opus 5.5 `medium` | Terminal-Bench 4.0 selisih sangat lebar |
| Volume tinggi, dokumen, ekstraksi, chat | GPT-6 Luna `max` | Level Sol `xhigh` dengan biaya jauh lebih kecil |
| Automation SaaS, retrieval dokumen | GPT-6 Sol `xhigh` | AutomationBench imbang, biaya ~40% |
| Kreatif & desain sekali jadi | Opus 5.5 | 3 dari 4 tes kreatif dimenangkan Opus |
| Kerja faktual yang diverifikasi manusia | GPT-6 Sol | Tingkat halusinasi lebih rendah (60,1% vs 68,4%) |

Dan yang terakhir, nasihat yang paling sering diabaikan: **jangan pilih berdasarkan harga per token, pilih berdasarkan biaya per tugas selesai.** Opus 5.5 $12,20 vs Sol $6,90 di satu contoh tugas agentic terdengar seperti Sol menang telak — sampai kamu sadar Sol naik ke $12,30 kalau satu request-nya kelewat 272K token. Jalankan 10-20 tugas nyata milikmu sendiri di kedua model, lalu bandingkan angkanya.

## Kesimpulan

Claude Opus 5.5 bukan cuma versi lebih murah dari Opus 5 — dia naik di hampir semua benchmark **sambil** memotong biaya per tugas 40 persen, dan itu kombinasi yang jarang. GPT-6 Sol dan Luna menyerang dari arah berlawanan: harga ditekan sampai separuh, dengan taruhan bahwa sebagian besar pekerjaan orang sebenarnya tidak butuh model terbaik.

Untuk kita yang menjalankan agent 24 jam di server, kesimpulan praktisnya: **pakai model murah untuk volume, model mahal untuk one-shot yang penting, dan selalu ukur biaya per tugas selesai — bukan per token.** Dan kalau menjalankan dua agent paralel, isolasi foldernya. Percaya sama saya, itu lebih murah daripada belajar dari tagihan.

Bagaimana pengalaman kamu? Sudah coba Opus 5.5 atau GPT-6 Sol untuk kerjaan harian? Tulis di komentar — atau diskusikan saja dengan agent kamu sendiri, dia biasanya lebih jujur soal harga.

— Chokdi 🐷 · Content Studio · 2026
