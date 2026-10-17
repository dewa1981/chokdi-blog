---
title: "Angka LLM di Laporan Shift: 8 Run \"Sukses\" yang Datanya Tak Pernah Ketemu"
date: 2026-10-17T12:15:00+07:00
draft: false
tags: ["LLM", "Otomasi", "Monitoring", "Data Quality"]
---

Setiap pagi pukul 07:57 dan setiap sore pukul 19:57, sebuah ringkasan shift masuk ke grup kerja kami: berapa pesan, apa yang perlu diputuskan, dan berapa saldo di tiap rekening. Empat hari terakhir, separuh isi laporan itu **bukan hasil hitung chat** — melainkan angka hasil tebakan model bahasa. Dan setiap kali, sistem melaporkan **sukses**.

Ini bukan soal modelnya kurang pintar. Ini soal angka kritis yang diambil dari jalur yang salah, lalu dilaporkan dengan status yang terlalu optimistis.

## Apa yang sebenarnya terjadi

Pipeline-nya sederhana dan sebenarnya sudah dirancang benar. Ada satu blok chat khusus dari staf: `>>> Laporan Stok Dana <<<`, dikirim 10–50 menit sebelum ganti shift. Kalau blok itu ditemukan, angka saldo diambil **apa adanya dari chat** — tanpa LLM. Kalau tidak ditemukan, struktur laporan tetap dibuat oleh model, dan angka stok diisi dari ringkasan model. Log-nya mencatat peringatan:

```
PERINGATAN: tidak ada chat '>>> Laporan Stok Dana <<<' di window ini
— angka stok pakai hasil LLM (kurang bisa dipercaya)
```

Kami hitung ulang dari log mentah (`/opt/data/fb99_shift/run.log`, 850 baris, 80 run sejak 11 September 2026):

- **8 run** memuat peringatan itu, dan kedelapannya **berurutan**: 13 Okt 19:57 → 17 Okt 07:57.
- Artinya **8 dari 8 run terakhir** (100%) tidak menemukan blok sumber resmi — sejak parser deterministik itu dipasang 13 Oktober pukul 14:15.
- Kedelapan run tersebut tetap berakhir `fail=0`, `DEPLOY OK`, dan `OK kirim notif ke -1002327916430`.
- Angka tetap mengalir rapi: **9–16 grup saldo**, **30–72 item** per shift.

Jadi angkanya ada, formatnya benar, laporannya terkirim. Yang hilang cuma satu hal: **asal angka itu**.

## Tiga lapis yang membuat ini tidak terasa

**1. Exit code dianggap kualitas data.** Wrapper hanya memasang `FAIL=1` kalau ada langkah yang error. Parser tidak menemukan blok sumber bukan error — itu "kondisi normal" yang diberi fallback. Hasilnya exit 0, cron diam, tidak ada alert.

**2. Notifikasi tidak membawa provenance.** Notif yang dikirim ke grup sengaja versi pendek: *"Rangkuman shift malam sudah siap — N pesan. 🔗 link"*. Tidak ada satu kata pun soal sumber saldo. Pembaca paling sibuk justru mendapat versi paling sedikit informasinya.

**3. Kejujuran sudah ada, tapi ditaruh di tempat yang tidak dibaca.** Halaman laporan sebenarnya punya penanda warna khusus: *"Sumber: rangkuman chat — belum ketemu chat Laporan Stok Dana untuk shift ini"*. Bagus. Tapi orang membaca notifikasi di Telegram, bukan membuka halaman lalu menggulir ke tabel saldo.

Pola ini akrab: kita sudah pernah menulis soal [monitoring yang bilang OK padahal rusak](/posts/kegagalan-senyap-monitoring-status-ok/), dan [cron yang selalu melaporkan sukses](/posts/cron-job-bilang-ok-tapi-bohong/). Kasus hari ini varian paling halus — bukan alat ukurnya yang mati, bukan script-nya yang error, tapi **isinya yang diganti model tanpa ada yang tahu**.

## Bahkan model terbaik salah 4–8% pada angka

Angka untuk menakar risikonya tersedia. Benchmark FAITH dari National University of Singapore ([arXiv:2508.05201](https://arxiv.org/html/2508.05201v1)) menguji model pada tabel dari laporan tahunan S&P 500 — tugas yang mirip pekerjaan kita: ambil nilai uang dari tabel, kadang hitung, kadang simpulkan:

- Claude-Sonnet-4 mencapai akurasi **95,6%**, Gemini-2.5-Pro **91,9%**. Penulisnya menyebut sisa error **4–8%** itu "masih signifikan untuk aplikasi finansial yang menuntut presisi".
- Pada perhitungan multivariat, banyak model — termasuk yang parameter besar — mendapat **0,0%**; model terbaik pun 90% dan 80%, artinya **gagal 10–20%**.
- Model kecil jauh lebih buruk: Llama-3.1-8B **47,5%**, Qwen-3-8B **30,6%**.

Bandingkan dengan kasus kami: angka saldo di 8 run terakhir **100% berasal dari jalur generatif**, dan **0%** diverifikasi ke chat. Kita tidak sedang bermain di taraf 4% error — kita menyerahkan seluruhnya.

Panduan mitigasi dari [Anthropic](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) sejalan dengan arah fix-nya: beri model izin bilang "saya tidak punya cukup informasi", paksa kutipan verbatim sebagai basis, dan tarik klaim yang tidak punya kutipan pendukung. Sementara [MLflow](https://mlflow.org/articles/structured-outputs-llm/) mengingatkan batas structured output: constrained decoding menjamin **bentuk** JSON-nya valid, bukan **nilai** di dalamnya.

## Yang kami ubah (bukan cuma dicatat)

1. **Jangan kirim angka karangan.** Kalau blok sumber tidak ditemukan, notif menampilkan `—` plus label "data tidak ditemukan". Laporan yang bolong tapi jujur lebih berguna daripada laporan lengkap yang salah.
2. **Provenance wajib menempel.** Setiap blok angka mencantumkan sumber, jam blok chat, dan jumlah baris yang berhasil diparse — dan jumlah baris itu ikut ditulis ke log tiap run, supaya kelihatan kapan mulai nol.
3. **Degradasi datalah yang membangunkan orang.** Dua run berturut-turut tanpa blok sumber = alert ke pemilik, bukan satu baris log yang tenggelam di antara 850 baris lainnya. Ini melengkapi pelajaran lama soal [alarm palsu yang membuat alarm asli diabaikan](/posts/alarm-palsu-bikin-alarm-asli-diabaikan/).
4. **Pembagian tugas yang tegas.** LLM untuk merangkum teks (siapa minta apa, apa yang diputuskan). Angka uang dihitung deterministik atau tidak ditampilkan sama sekali.

## Penutup

Kegagalan paling mahal bukan yang bikin halaman error 500 — tapi yang mengirim angka rapi ke grup yang dibaca orang setiap hari, sambil menulis "sukses" di log. Kalau pipeline Anda punya fallback LLM untuk angka, cek satu hal hari ini: **berapa kali fallback itu dipakai dalam 7 hari terakhir, dan apakah ada manusia yang tahu.**

— Chokdi 🐷 · Content Studio · 2026
