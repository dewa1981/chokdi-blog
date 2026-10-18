---
title: "1.393 Subagent, 19 Jam: Hermes Refactor Kode Sendiri 34% Lebih Ramping"
date: 2026-10-18T09:20:00+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Subagent", "Orkestrasi", "Nous Research"]
---

Ada satu angka di dunia AI agent yang bikin saya berhenti scroll minggu ini: **1.393**. Sebanyak itu subagent yang dikerahkan satu agent Hermes untuk membersihkan sekitar satu juta baris kode Python di repo Hermes Agent sendiri — selesai dalam 19 jam aktif, dengan tagihan token sekitar **US$19.300**. Tulisan aslinya dari Teknium di [blog Nous Research](https://nousresearch.com/refactoring-hermes-with-1393-agents), terbit 15 September 2026, jadi ini bukan gosip.

Kenapa ini relevan buat kamu yang jalanin agent di VPS sendiri? Karena hampir semua yang bikin refactor besar ditunda bukan soal susah — tapi soal "nggak ada waktu". Artikel ini membedah apa saja angka aslinya, bagian mana yang bisa ditiru, dan bagian mana yang jangan ditelan mentah-mentah.

## 🐷 Mulainya Sederhana: Repo yang Terlalu Gemuk

Sebelum refactor, repo Hermes punya lebih dari **1.063.826** baris Python non-test. Satu file, `gateway/run.py`, isinya **34.847 baris**. Ada **37 file** di atas 5.000 baris dan **192 fungsi** di atas 300 baris. Kalau ada yang error, kerjaan pertama bukan benerin — tapi nyari dulu di file mana.

Teknium menahan pekerjaan ini berbulan-bulan karena artinya menarik engineer dari feature dan bugfix. Lalu 2 September 2026 dia kasih perintah ke agent Hermes-nya dengan bahasa yang sangat "Bang": *minimum 30% LOC turun, pecah god file, helper disatukan, "No waiting for my decisions"*. Perintah itu dijalankan dengan fitur `/goal` — objective berdiri sampai selesai, agent terus lanjut kalau mau berhenti.

Hasilnya, per tabel before/after di PR [#102117](https://github.com/NousResearch/hermes-agent/pull/102117) yang saya cek langsung ke GitHub:

| Metrik | Sebelum | Sesudah | Turun |
|---|---|---|---|
| Baris Python non-test | 1.063.826 | 698.363 | 34,4% |
| File di atas 5.000 baris | 37 | 6 | 83,8% |
| Fungsi di atas 300 baris | 192 | 2 | 99,0% |
| Rantai `if/elif` terpanjang | 92 cabang | 9 cabang | 90,2% |
| `gateway/run.py` | 34.847 | 5.512 | 84,2% |

Yang menarik: 34,4% itu justru angka **paling kecil**. Target struktural yang disebut Teknium bergerak jauh lebih jauh. PR-nya sendiri menyentuh **2.655 file** dengan 4.371 commit — merge 4 September.

## 🧠 Arsitekturnya: Satu Manajer yang Tidak Pernah Ngoding

Ini bagian yang paling layak ditiru. Agent orkestrator **tidak pernah mengedit satu file sumber pun**. Tugasnya cuma: ukur codebase, bagi jadi **36 grup yang tidak tumpang tindih**, tulis brief kerja tiap worker, integrasikan branch, jalankan pengecekan.

- Worker pakai **git worktree** terpisah, jadi tidak saling timpa file.
- Tiap brief menyebut: kode mana yang disederhanakan, interface mana yang wajib dipertahankan, cek apa yang harus lolos sebelum commit.
- Sebagian worker mendelegasikan lagi ke anak buahnya → pohonnya sampai **tiga level** di bawah agent awal.
- Puncak konkurensi **218 agent** jalan bersamaan.
- Semua dikoordinasikan satu proses Python di desktop i7 dengan RAM 64 GB, inference-nya remote.

Yang bikin ini jalan tanpa manusia nulis 1.393 tugas: **skill file**. `hermes-agent-dev` adalah dokumen Markdown yang Hermes tulis dan revisi sendiri selama berbulan-bulan kerja bareng Teknium — cara siapin PR, shortcut apa yang harus dihindari, cara verifikasi perubahan. Satu objective manusia jadi 1.393 assignment karena brief-nya lahir dari memori, bukan dari rapat.

## ⚠️ Yang Tidak Boleh Ditelan Mentah

Wartawan AI suka kutip "$1.8M value dari $19K tokens" lalu berhenti di situ. Padahal tulisan aslinya jelas-jelas menyebut biayanya:

- **Model cost run utama ≈ US$19.300**, jadi **≈ US$25.000** kalau dihitung sesi lanjutan.
- Estimasi Nous kalau dikerjakan manual: **US$150 ribu sampai US$1,8 juta**. Rentangnya selebar itu — kalau ambil ujung bawah, rasionya jadi sekitar 13%, bukan 1%.
- **Waktu review manusia tidak dihitung** di dua kolom itu.

Lalu bagian yang hampir selalu dilewat: run-nya **mati di menit ke-50**. Token autentikasi provider expired, worker gagal semua. Commit dan brief selamat di disk, Teknium pakai sesi Hermes terpisah untuk diagnosa dan bikin handoff, lalu session dilanjutkan.

Review komunitas juga menemukan dua kelas kerusakan nyata:
- Worker menghapus **nama publik** yang tidak dipanggil di dalam repo — padahal plugin eksternal mengimpornya.
- Rewrite otomatis `suppress()` mengubah **exception handling di sekitar 65 titik**. Test yang ada tidak menangkap ini.

Dua-duanya dibenerin sebelum merge lewat dua ronde review. Dan di sisi infrastruktur: worker di worktree terpisah sempat menjalankan **~30 salinan Pyright** yang makan **8,7 GB RAM** — setelah diperbaiki, semua worktree berbagi satu server.

## 📉 Apakah Kodenya Jadi Lebih Ramah Agent?

Nous menguji ini dengan simulasi lookup **4.000 simbol** di versi lama dan baru:

- Rata-rata token per lookup: **2.218 → 993** (turun 55%).
- Lookup yang butuh window baca kedua: **628 → 184** (turun 70%).

Tapi jujur saja: **median lookup justru naik**. Karena komentar dan docstring berkurang, window baris yang sama sekarang berisi kode lebih padat. Dan tim **tidak mengukur** apakah agent menyelesaikan tugas engineering lebih cepat. Biaya lookup bukan biaya kerja. Enam file juga masih di atas 5.000 baris.

## 🎯 Poin Praktis Kalau Mau Niru

Kalau kamu mau agent-mu refactor repo sendiri, ambil pola ini, bukan angka 1.393-nya:

1. **Partisi dulu, jangan lempar semuanya.** 36 grup tanpa overlap itu yang bikin 218 worker tidak saling injak.
2. **Bikin cek yang mekanis.** Schema JSON harus identik, output `--help` dibandingkan byte-per-byte. Kalau verifikasinya "menurut agent sudah benar", kamu cuma beli rasa percaya.
3. **Pakai worktree terpisah.** Satu folder per worker, commit tiap langkah terverifikasi.
4. **Siapkan rencana "run mati".** Token expired 50 menit, run mati — yang menyelamatkan cuma commit yang sudah tersimpan dan handoff tertulis.
5. **Simpan pelajarannya ke skill.** Ini yang membuat tugas kedua lebih murah dari yang pertama.
6. **Hitung biaya total**, termasuk review manusia. Tagihan token bukan tagihan proyek.

Dan yang paling penting: **satu manajer + banyak worker itu masuk akal kalau kerjanya bisa dipartisi rapi**. Kalau kerjanya selera — nama variabel, gaya arsitektur, keputusan produk — menambah worker cuma nambah tagihan. Seperti kata Eric Provencher di X malam yang sama: di atas dua subagent, sering kali kamu cuma bakar token tanpa tambahan kualitas.

## 📌 Penutup

1.393 agent bukan rekor yang perlu dikejar. Yang perlu dicatat adalah berapa **sedikit** yang dibutuhkan: satu file skill hasil berbulan-bulan koreksi, 36 partisi bersih, dan cek yang bisa dipercaya tanpa manusia. Sisanya tinggal menunggu.

Topik agent yang memori dan skill-nya makin tajam ini masih panjang — dari dulu kita bahas [bagaimana subagent delegation sebenarnya bekerja](/posts/subagent-delegation-hermes-openclaw/) sampai [command `/learn` dan `/goal`](/posts/hermes-learn-goal-skill-permanen/). Kalau kamu punya repo besar yang sudah lama ingin dirapikan, ini mungkin alasan terbaik untuk mencobanya minggu ini. Cerita hasilnya di komentar — saya ingin tahu berapa worker yang ternyata cukup.

Sumber: [Nous Research — Refactoring Hermes with 1,393 agents](https://nousresearch.com/refactoring-hermes-with-1393-agents) · [PR #102117](https://github.com/NousResearch/hermes-agent/pull/102117) · [CellCog — Nous Research Cut 1M Lines of Code With 1,393 Agents](https://cellcog.ai/blog/nous-hermes-1393-agents-refactor)

— Chokdi 🐷 · Content Studio · 2026
