---
title: "LLM Lokal 35B di Mac mini: Kenapa Gambar Gagal & Cara Benerin Vision-nya 👁️"
date: 2026-09-21T00:10:00+07:00
draft: false
tags: ["AI", "LLM Lokal", "Tutorial", "Hermes"]
---

Model 35B jalan lokal di Mac mini M4 Pro 64 GB itu enak: **56 token/detik, gratis, dan data nggak keluar rumah**. Sampai suatu hari kami kirim gambar ke dia... dan langsung ditolak.

```
{"error":{"code":500,"message":"image input is not supported - hint: if this is
unexpected, you may need to provide the mmproj","type":"server_error"}}
```

Masalahnya bukan modelnya rusak, dan bukan RAM kurang. **Satu file kecil ketinggalan** — dan artikel ini isi jebakan lengkapnya, dari yang bikin buang 2 jam sampai solusi yang akhirnya kami pakai.

## Modelnya pintar, tapi buta

LLM teks itu seperti orang pintar yang matanya ditutup. Dia bisa ngobrol, ngoding, nyimpulin dokumen — tapi begitu ada gambar masuk, dia nggak punya "mata" untuk membacanya.

Matanya itu namanya **mmproj** (multimodal projector). Di llama.cpp, kemampuan multimodal ditangani library `libmtmd`: kamu butuh **dua file** — model teks (`*.gguf`) dan projector (`mmproj-*.gguf`). Tanpa pasangan itu, endpoint gambar otomatis ditolak.

Ini bukan kasus kami saja. Ada laporan identik di [issue llama.cpp #19917](https://github.com/ggml-org/llama.cpp/issues/19917) untuk Qwen3.5-35B-A3B — pesan error 500-nya sama persis. Jawaban di thread itu cuma satu: unduh file `mmproj` dari repo model yang sama.

## Cara pasang mmproj dengan benar

Dari [dokumentasi resmi multimodal llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md), ada dua pola:

```bash
# 1. taruh file manual
llama-server -m model-Q4_K_M.gguf --mmproj mmproj-F16.gguf

# 2. biar llama.cpp yang urus (repo pendukung, mis. ggml-org/gemma-4-31b-it-GGUF)
llama-server -hf ggml-org/gemma-4-31b-it-GGUF

# kalau VRAM mepet, projector bisa dipaksa tetap di CPU
llama-server -hf ggml-org/gemma-4-31b-it-GGUF --no-mmproj-offload
```

Tiga aturan yang bikin orang gagal di sini:

1. **mmproj harus satu keluarga dengan modelnya.** Model tune seperti Artemis-31B (tune Gemma 4) boleh pakai mmproj punya Gemma 4 31B — tapi mmproj InternVL nggak akan nyala di Qwen.
2. **Nama file wajib diawali `mmproj`.** Kalau model + mmproj ditaruh satu folder, keduanya harus ada di subdirektori sendiri (lihat server README llama.cpp) — kalau tidak, projector-nya dianggap model kedua.
3. **Jangan taruh mmproj sembarangan di folder model.** Di kasus kami, file mmproj yang ditaruh di `~/.hermes/models/` malah muncul di `/v1/models` sebagai **model** — sementara vision tetap mati.

## Jebakan utama: file ada, tapi tetap nggak kepasang

Ini bagian yang paling bikin frustrasi. Filenya ada. Argumennya kosong.

Ternyata Hermes mengambil mmproj dari **katalog internalnya** (`hermes_cli/local_runtime/catalog.py`), bukan dari hasil scan folder model. Model yang diunduh manual dari Hugging Face — misalnya varian uncensored — nggak punya entri katalog, jadi walau file mmproj sudah tersedia di disk, path-nya **tidak pernah disuntik** ke argv `llama-server`.

Cara memastikan (bukan nebak): cek argumen proses yang benar-benar jalan, lalu cari `--mmproj`:

```bash
ps -eo pid,cmd | grep llama-server
```

Kalau `--mmproj` nggak ada di situ, ya memang belum kepasang — mau file-nya sebesar apa pun.

## Solusi 2: pisah tugas — teks lokal, gambar ke cloud

Daripada berkelahi dengan katalog, kami pilih pembagian kerja yang lebih waras:

- **teks tetap 100% lokal** — model uncensored, tanpa sensor, tanpa biaya token;
- **gambar dilempar ke model yang vision-nya native**.

Di Hermes cukup satu blok konfigurasi:

```yaml
auxiliary:
  vision:
    provider: deepseek   # eksplisit — JANGAN "auto"
    model: deepseek-flash
```

**Catatan penting:** `provider: auto` artinya ikut model utama — yang justru buta tadi. Setelah restart `hermes serve`, verifikasi lewat log:

```bash
grep "Vision auto-detect" ~/.hermes/logs/agent.log | tail -1
# -> Vision auto-detect: using main provider deepseek (deepseek-flash)
```

Hasilnya: teks jalan lokal, gambar jalan di cloud, dan keduanya nggak saling ganggu. Biaya hanya keluar saat ada gambar.

## Hasil terukur di M4 Pro 64 GB

| Metrik | Angka nyata |
|---|---|
| Decode | **55,9–56,4 tok/s** (3 level tes) |
| Load pertama | ~10–11 detik |
| RAM model | 31,3 GB |
| Retrieval 4.451 token | ✅ benar (kode di awal dokumen ketemu) |

Angka itu kelihatan mustahil kalau dibandingkan patokan umum: model **dense** 30B kelas Q4 di Mac biasanya cuma 12–18 tok/s. Penyebabnya arsitektur: model yang kami pakai adalah **Qwen3.6-35B-A3B** — MoE 35B total tapi hanya ~3B parameter aktif per token (lihat juga [benchmark Qwen3.6-35B MoE](https://www.gilesthomas.com/2026/07/benchmarking-qwen-3-6-35b-moe-rtx-3090)). Jadi kalau kamu milih model lokal, **cek dulu apakah dia MoE** — bedanya bisa 3–4x kecepatan.

## Jebakan terakhir: ctx-size di presets.ini ketimpa tiap boot

Satu lagi yang hampir bikin salah diagnosa. Kami kira modelnya lambat karena context window kegedean, lalu set `ctx-size = 262144` di `presets.ini` — hilang tiap boot. Ternyata `presets.ini` **digenerate ulang dari kapasitas RAM total** (64 GB), bukan dari RAM bebas, jadi model 20 GB dijalankan dengan `-c 1048576` dan KV cache q8_0 membengkak ke 12–13 GB.

Yang benar-benar ngefek: **bebaskan RAM sungguhan**. Setelah aplikasi berat (browser, chat, wallet, cloud sync) ditutup, RAM bebas naik dari 25% ke 30% dan decode stabil di 56 tok/s. Kesimpulannya: ctx besar bukan penyebab utamanya — **kontensi RAM aplikasi lain** penyebabnya.

## Kesimpulan

Tiga pelajaran yang bisa kamu pakai besok:

1. Model lokal buta bukan berarti rusak — cek `--mmproj` dulu sebelum ganti model.
2. Menaruh file mmproj di disk nggak cukup kalau aplikasinya baca mmproj dari katalog.
3. Routing vision ke cloud jauh lebih hemat waktu daripada memaksa semuanya lokal.

Kalau kamu baru mau mulai AI lokal, baca dulu [cara install Ollama di WSL2 dan MacBook](/posts/install-ollama-ai-lokal-gratis/) dan [cara memuat model lokal sekali klik di Hermes Desktop](/posts/hermes-desktop-model-lokal-sekali-klik/). Punya pengalaman lain soal mmproj? Tulis di kolom komentar — kami baca.

— Chokdi 🐷 · Content Studio · 2026
