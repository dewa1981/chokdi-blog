---
title: "STT Bahasa Indonesia Terbaik 2026: Scribe Juara, 3 Jebakan yang Bikin Salah Dengar"
date: 2026-09-17T18:20:00+07:00
draft: false
tags: ["AI", "STT", "Speech to Text", "Tutorial"]
---

Kalau ngomong cepat sambil campur Hokkian dan English, apakah asisten suara dengar *"deposit dua ratus ribu"* — atau *"deposit 2000 ribu"*? Jawabannya ada di angka, bukan klaim brosur. Kami uji ulang STT 2026 pakai audio Indonesia, dan hasilnya: juaranya jelas, tapi ada **tiga jebakan** yang bikin salah dengar walaupun modelnya paling akurat.

## 🏆 Papan Skor Bahasa Indonesia

Benchmark resmi FLEURS, bahasa Indonesia:

| Model | WER (FLEURS Indonesia) |
|---|---|
| **ElevenLabs Scribe** | **2,4%** 🥇 |
| Gemini Flash 2 | 3,7% 🥈 |
| Whisper Large v3 | 7,7% 🥉 |
| Deepgram Nova 2 | 10,4% ❌ |

Di dataset Common Voice, Scribe tercatat 5,5% WER. Artinya Scribe **3x lebih akurat** dari Whisper Large v3 dan **4x lebih akurat** dari Deepgram Nova 2 untuk Bahasa Indonesia. Cara bacanya: WER = dari 100 kata yang diucapkan, berapa kata yang salah. 2,4% berarti sekitar dua-tiga kata meleset per seratus kata — bedanya antara pesan yang bisa diproses dan pesan yang harus diulang.

## 🔢 Jebakan #1: Kode Bahasa Dua Huruf Ditolak

Ini jebakan paling sepele tapi paling sering. ElevenLabs memakai standar **ISO 639-3 (tiga huruf)**: `idn` → error `Invalid language code`, sementara `ind` dan `ina` benar, dan kosong berarti auto-detect.

Masalahnya hampir semua orang menulis `id` (ISO 639-1, dua huruf) — kami pun begitu: `stt.language: id`. Kalau vendor menerima dua huruf, aman. Kalau tidak, dia jatuh ke auto-detect — dan auto-detect itu **ragu**: keyakinan deteksi bahasanya cuma 0,68 saat diuji. Lebih baik set eksplisit `ind` daripada berharap mesin menebak. Tiap vendor punya skema kode sendiri, jadi cek dokumentasinya, jangan asal copy dari tutorial lama.

## 🌏 Jebakan #2: Campur Bahasa (Indo + Hokkian + English)

Ini titik lemah semua STT, dan justru kebiasaan ngomong sehari-hari. Angkanya bikin kaget: Whisper Turbo-V3 jatuh dari **22,04% WER** di audio satu bahasa menjadi **58,67% WER** di audio campur Melayu-Inggris. Riset lain menunjukkan pola sama: monolingual 5% WER membengkak ke 15-20% begitu bahasa dicampur dalam satu kalimat. Sebabnya teknis — tokenizer monolingual tidak punya kosakata bahasa kedua, jadi fonem asing "dipaksa" jadi kata terdekat, dan keluarlah kalimat ngawur.

Obat yang tersedia sekarang:

1. **Model multilingual end-to-end** — Gladia Solaria-1 menangani code-switching native di 100+ bahasa; Speechmatics Ursa 2 klaim 35% lebih baik dari pesaing terdekat.
2. **Keyterm prompting** — daftarkan nama, username, dan istilah internal (AssemblyAI mendukung sampai 1.500 kata).
3. **Ukur switch-point WER** — hitung error khusus di 2-3 kata sekitar titik ganti bahasa, bukan WER rata-rata. Justru di situ pengguna paling cepat sadar.

## 🎯 Jebakan #3: Benchmark Vendor Bukan Audio Kamu

Kutipan paling jujur soal ini dari analisis independen Coval: *"Vendor benchmarks are marketing copy with measurements attached."* Benchmark pakai audio bersih; di produksi kamu menghadapi noise dan suara tumpang tindih.

Masalah khas yang jarang masuk brosur: **entity preservation collapse** — akurasi umum di atas 95%, tapi angka, nama orang, dan ID jatuh ke 50-70%. Untuk transkripsi rapat itu tidak apa-apa. Untuk perintah yang memindahkan nominal uang, itu bencana.

## 🧪 Uji Sendiri 15 Menit: Round-Trip TTS → STT

Tulis kalimat, jadikan suara dengan TTS, suruh STT membacanya kembali, bandingkan dengan teks asli.

**Input TTS:** *"Halo Bang, ini tes suara untuk benchmark. Deposit manual dua ratus ribu ke username Budi satu dua tiga sudah diproses. Silakan cek di panel ya."*

**Output STT:** *"Halo Bang, ini tes suara untuk benchmark. Deposit manual 200.000 ke username Budi123 sudah diproses. Silakan cek di panel ya."*

**Hasil: WER 0% — sempurna.** Plus dua bonus: "dua ratus ribu" otomatis jadi `200.000`, dan "Budi satu dua tiga" otomatis dirangkai jadi `Budi123`. Normalisasi seperti ini yang bikin output STT langsung layak dipakai sistem lain, tanpa parser tambahan.

Susun test set kecil yang mewakili kerjaan kamu: angka dan nominal, nama dan username, kalimat campur bahasa, rekaman berisik, dan istilah khusus domain. Lima kalimat ini lebih berguna daripada membaca sepuluh tabel benchmark.

## 💰 Lanskap Harga 2026

| Provider | Async | Real-time |
|---|---|---|
| Deepgram Nova-3 | ~$0,26 | ~$0,35 |
| AssemblyAI Universal-2 | $0,21 | ~$0,45 |
| ElevenLabs Scribe | ~$0,22-0,40 | ~$0,39 |
| Gladia Solaria | dari $0,20 | dari $0,25 |

Rilis penting sepanjang 2026: Microsoft MAI-Transcribe-1, Deepgram Flux Multilingual yang menyatukan deteksi akhir-bicara (hemat 200-600 ms respons), OpenAI GPT-Realtime-Whisper ($0,017/menit), dan NVIDIA Parakeet-TDT-0.6B-v3 (6,34% WER) buat yang mau self-host. WER di audio bersih sudah plateau di 2-3% — pertarungan sekarang pindah ke **latensi, deteksi giliran bicara, dan code-switching**.

Kalau mau lihat bagaimana transkripsi ini dipakai membangun asisten pribadi yang benar-benar jalan, baca catatan kami soal [membangun JARVIS realtime voice AI](/posts/bikin-jarvis-realtime-voice-ai/). Untuk sisi sebaliknya — asisten suara besar yang justru tertinggal — ada tulisan [Siri dan antiklimaks AI](/posts/apple-siri-ai-antiklimaks/).

## Kesimpulan

Untuk Bahasa Indonesia 2026, **ElevenLabs Scribe juara dengan 2,4% WER** — dan sudah terpasang di setup kami, tanpa alasan pindah. Tapi juara benchmark tidak menyelamatkan kamu dari tiga hal: kode bahasa yang salah tulis, kalimat campur bahasa, dan asumsi bahwa akurasi umum berarti akurasi pada angka dan nama.

Resep amannya sederhana: set kode bahasa eksplisit, uji lima kalimat yang mirip kerjaan kamu sendiri, dan hitung error di bagian yang paling mahal kalau salah. STT yang bagus bukan yang menang di tabel, tapi yang bisa dipercaya saat nominal uang disebut.

**Gas, tapi pake akal!** 💎

— Chokdi 🐷 · Content Studio · 2026
