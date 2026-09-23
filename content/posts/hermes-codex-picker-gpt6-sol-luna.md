---
title: "GPT-6 Sol & Luna Akhirnya Muncul di Picker Codex Hermes Agent"
date: 2026-09-23T09:20:00+07:00
draft: false
tags: ["Hermes Agent", "GPT-6", "Codex", "Update", "AI Agent"]
---

Kalau kamu pakai langganan ChatGPT/Codex lewat provider `openai-codex` di Hermes Agent, ada kabar bagus: model **GPT-6 Sol** dan **GPT-6 Luna** akhirnya muncul sendiri di picker `/model`, tanpa kamu harus hafal dan ngetik slug-nya manual. Perbaikannya masuk ke `main` pada 22 September 2026 lewat PR #119436, dan akar masalahnya ternyata bukan soal kuota — tapi soal **satu angka versi klien**.

## 🐛 Gejala: Model Ada di Akun, Tapi Tidak Ada di Daftar

Laporan datang dari @Stone441 di issue #119412 (dibuka 22 September 2026, 18:38 UTC):

- Picker Codex Hermes **tidak menampilkan** `gpt-6-sol` dan `gpt-6-luna`, padahal Codex CLI di mesin yang sama mendaftarkan keduanya.
- Refresh picker tidak menolong — hasilnya sama.
- Yang aneh: kalau dia paksa pakai `/model gpt-6-sol`, chat-nya **berhasil**. Hermes cuma memberi peringatan bahwa slug itu tidak ada di daftar.
- Dia sudah verifikasi **inferensi asli** untuk Sol — jadi bukan soal entitlement.

Modelnya bisa dipakai, tapi tidak bisa ditemukan. Itu kelas bug yang paling menyebalkan: bukan rusak, hanya tidak kelihatan.

## 🔍 Akar Masalah: Sentinel `0.0.0` Sudah Basi

Endpoint katalog Codex menyaring model berdasarkan parameter `client_version`. Tiap model punya syarat `minimal_client_version` sendiri.

Selama ini Hermes mengirim `client_version=0.0.0` sebagai **sentinel "tanpa gate"**. Dulu itu trik yang benar: versi paling tua pasti lolos semua gate. Tapi setelah GPT-6 Sol/Luna digelar, `0.0.0` berubah jadi **daftar warisan yang dibekukan**.

| `client_version` | Slug yang terlihat |
|---|---|
| `0.0.0` (cara lama Hermes) | `gpt-6-astra`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-5.5` |
| `0.155.0` (versi cache Codex CLI) | ditambah **`gpt-6-sol`** dan **`gpt-6-luna`** → total 9 entri |

Angka ini bukan karangan: pelapor membandingkan dua request ke endpoint yang sama dengan akun OAuth yang sama. Lalu maintainer @teknium1 mengonfirmasi dengan token nyata — `0.155.0`, `0.160.0`, `1.0.0`, dan `99.0.0` semuanya mengembalikan 9 entri lengkap.

Yang bikin bug ini diam: `0.0.0` **tidak error**. Dia balas HTTP 200 dengan isi yang sah. Karena itu `get_codex_model_ids()` menganggap hasilnya final dan tidak pernah fallback ke cache lokal `~/.codex/models_cache.json`.

## 🔧 Perbaikannya: Tanya sebagai Klien Terbaru Dulu

PR #119436 (merge 22 September 2026, 20:07:46 UTC, commit `7ce190446e`) membalik urutannya — selesai dalam **~1,5 jam** dari lapor ke merge.

- `CODEX_MODELS_CATALOG_URL` → **`CODEX_MODELS_CATALOG_URLS`** (sekarang tuple).
- `agent/model_metadata.py`: konstanta baru `CODEX_NEWEST_CLIENT_VERSION = "99.0.0"` dicoba **pertama**; sentinel `CODEX_UNGATED_CLIENT_VERSION = "0.0.0"` jadi cadangan.
- `fetch_codex_catalog_entries()` mengembalikan katalog pertama yang balas HTTP 200 dengan daftar `models` non-kosong; jawaban kosong atau non-200 → jatuh ke sentinel.
- `hermes_cli/codex_models.py::_fetch_models_from_api` memakai helper yang sama, jadi picker **dan** probe context window selalu sepakat.

Satu keputusan desain yang menarik: PR komunitas lain (#119420, @KoNit-K) menyelesaikannya dengan membaca `client_version` dari cache CLI lokal. Itu **ditolak**, dan alasannya masuk akal — kalau cache hilang, user balik ke `0.0.0`; kalau cache basi, `gpt-6-sol` tetap tersembunyi karena butuh ≥ `0.155.0`.

## 🧪 Hasil Verifikasi di `main`

| Pemeriksaan | Hasil |
|---|---|
| Dua tes baru di `test_codex_models.py` | **merah di `origin/main`** (2 failed) → hijau di head |
| 5 suite terkait | **177 lulus, 0 gagal** |
| Picker sesudah patch | `gpt-6-astra, -900k, gpt-6-sol, -900k, gpt-6-luna, -900k`, `gpt-6-terra` |
| Probe context window | `fresh=True`, `gpt-6-sol: 272000`, `gpt-6-luna: 272000` |
| Varian `-900k` | `gpt-6-sol-900k` → **872.000** token (batas `max_context_window` live) |

Yang paling penting: tombol **Refresh** di picker sekarang benar-benar menyelesaikan masalah, bukan cuma mengulang request yang sama.

## ⚠️ Yang Jujur Perlu Kamu Tahu

- Perbaikan ini ada di `main`, **belum masuk tag stabil**. Tag terakhir masih `v2026.9.21` (v0.21.4, 21 September 2026 18:10:55Z), dan `main` sudah **475 commit** di depannya (status `ahead`). Kalau kamu install dari tag stabil, picker masih menyembunyikan Sol/Luna.
- Efeknya **cuma di katalog**. Kalau kamu terbiasa `/model gpt-6-sol` manual, tidak ada yang berubah selain peringatan yang hilang.
- Sol dan Luna **tetap tergantung entitlement akun**. Katalog yang dikembalikan adalah katalog akunmu apa adanya — bukan model yang dipaksakan muncul untuk semua orang.
- Sesi lama tidak berubah; yang berubah adalah model apa yang ditawarkan ke sesi baru.

## ✅ Langkah Praktis

1. Masih di tag stabil? Tunggu rilis berikutnya, atau jalankan Hermes dari checkout `main` kalau kamu nyaman.
2. Sesudah update: buka `/model`, tekan Refresh → cek `gpt-6-sol` dan `gpt-6-luna` sudah ada.
3. Mau pastikan context window-nya terbaca benar? `gpt-6-sol` harus 272K, varian `-900k` naik ke 872K.
4. Kalau modelnya tetap tidak muncul padahal CLI Codex di komputermu melihatnya: cek versi kode yang jalan (`hermes --version`), karena di tag stabil lama masalahnya memang belum diperbaiki.

## 🧭 Kesimpulan

Satu konstanta `"0.0.0"` yang dulu pintar berubah jadi bumerang setelah vendor mengubah arti parameter kompatibilitas. Solusinya bukan membaca cache lokal yang rapuh, tapi **bertanya sebagai klien terbaru dan menyimpan sentinel lama sebagai jaring pengaman** — plus dua tes yang sengaja dibuat merah di `main` supaya kontrak barunya terkunci.

Kalau kamu self-host Hermes dengan langganan Codex, ini alasan bagus untuk rajin lihat `main` di antara dua rilis: perbaikan kecil seperti ini jarang masuk berita, tapi efeknya terasa tiap hari.

Kamu pakai Sol, Luna, atau tetap Astra? Tulis di komentar.

---

Baca juga: [Hermes Agent v0.21.4 Rilis: 5.173 Commit dalam 7 Hari](/posts/hermes-v0214-5173-commit/) dan [OpenClaw 2.0 vs v2026.9.2: Dukungan GPT-6 Astra](/posts/openclaw-2-0-gpt6-astra/).

Sumber: [Issue #119412](https://github.com/NousResearch/hermes-agent/issues/119412), [PR #119436](https://github.com/NousResearch/hermes-agent/pulls/119436), source `agent/model_metadata.py` + `hermes_cli/codex_models.py` di `main`.

— Chokdi 🐷 · Content Studio · 2026
