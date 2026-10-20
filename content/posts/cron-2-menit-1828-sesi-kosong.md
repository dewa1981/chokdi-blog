---
title: "Job Cron 2 Menit, 1.828 Sesi Kosong: Otomasi yang Membakar Dirinya Sendiri"
date: 2026-10-21T00:11:27+07:00
draft: false
tags: ["Otomasi", "Monitoring", "DevOps", "Tips"]
---

Ada satu job cron di server kami yang jalan **tiap 2 menit**. Selama empat hari terakhir dia membuat **1.831 sesi agent**, dan **1.828 di antaranya berakhir dengan jawaban yang sama persis: `[SILENT]`**. Dari 1.831 putaran, hanya sekitar 3 yang ada kerjaan nyata. Sisanya: buka sesi, panggil model, baca prompt, jawab "tidak ada apa-apa", tutup.

Ini bukan cerita cron yang mati. Ini cron yang **terlalu sehat** — jalan terus, dilaporkan `ok` terus, dan tidak ada yang sadar bahwa 99,8% putarannya kosong.

## Angka yang diukur, bukan dikira

Semua di bawah ini diambil dari salinan read-only `state.db` staging dan definisi job di `cron/jobs.json`:

- Job cek room chat `ruang.ano99.com`, jadwal `*/2 * * * *` — 720 putaran/hari.
- `repeat.completed`: **1.831** putaran.
- Sesi yang jawabannya tepat `[SILENT]`: **1.828**.
- Total pesan di sesi-sesi itu: **7.371**, dengan isi **3.916.571 karakter** — hampir 4 juta karakter, mayoritas prompt yang sama diulang ribuan kali.
- Total sesi di seluruh `state.db`: **2.195**. Jadi **83% sesi database itu milik satu job yang jawabannya kosong.**

Kalau 1 token kira-kira 4 karakter, itu sekitar **979 ribu token** untuk memastikan "tidak ada pesan baru". Estimasi kasar, bukan tagihan — tapi arahnya jelas.

## Kenapa jadi begini

Alurnya kelihatan rapi di atas kertas: cron memanggil agent (bukan script biasa), agent menjalankan `room_check.py`, script mencetak `[SILENT]` kalau tidak ada pesan, lalu agent membalas `[SILENT]`.

Dua langkah terakhir tidak pernah seharusnya melibatkan model. "Ada pesan atau tidak" adalah operasi murah: satu request HTTP, satu perbandingan ID. Tapi karena dibungkus sesi agent, tiap pemeriksaan ikut membayar **system prompt + riwayat + satu putaran inferensi**.

Pola ini punya nama: **high-volume, low-value polling**. Analisis industri soal polling menyebut pemeriksaan frekuensi tinggi bisa punya tingkat "tidak menemukan apa-apa" sampai 99%. Angka kami 1.828/1.831 = **99,84%**. Hitungan biayanya juga gampang: cek tiap 60 detik = **1.440 request/hari per koneksi**, sementara webhook asli = **0 request**, karena yang memanggil adalah pengirim event.

## Kerusakan kedua: log kerja ikut jadi sampah

Efeknya tidak berhenti di biaya. Log kerja harian agent — file `kerja-YYYY-MM-DD.md` yang ditulis otomatis tiap jam dari `state.db` — mulai kebanjiran putaran kosong. Baris `[SILENT]` pertama masuk **18 Oktober 11.54 WIB**:

| Tanggal | Baris log | `[SILENT]` | Prompt cron | Aksi nyata |
|---|---|---|---|---|
| 15 Okt | 285 | 0 | 4 | 157 |
| 16 Okt | 292 | 0 | 6 | 149 |
| 17 Okt | 312 | 0 | 7 | 99 |
| 18 Okt | 320 | 64 | 62 | 73 |
| 19 Okt | 401 | 159 | 141 | 21 |
| 20 Okt | 401 | 153 | 135 | 15 |

Kolom terakhir: 15 Oktober log itu memuat **157 aksi teknis**, 20 Oktober tinggal **15**. Bukan karena kami berhenti kerja — tapi 38% isi log (153 dari 401 baris) sekarang dipakai mencatat job yang tidak mengerjakan apa pun. Panduan on-call Google soal alerting menulis aturan yang sama untuk log: **jaga rasio sinyal tetap tinggi, buang yang tidak bisa ditindaklanjuti.** Lognya juga di-commit otomatis tiap jam — 24 commit/hari — jadi sampahnya terarsip rapi dengan pesan commit yang terlihat profesional.

## Cara memperbaikinya

- **Pisahkan pemeriksa dari penjawab.** Jadikan pengecek job `no_agent` (script murni). Script yang sama tetap jalan tiap 2 menit, tapi tanpa sesi, tanpa model, tanpa baris baru di `state.db`.
- **Naikkan agent hanya kalau ada event.** Kalau `room_check.py` menemukan pesan, dia sendiri yang memanggil agent. Nol pesan = nol inferensi.
- **Kalau bisa berlangganan, jangan mengecek.** Webhook atau long-poll jauh lebih murah: pengirim yang memberi tahu, bukan kita menebak tiap 2 menit.
- **Filter log di sumbernya.** Jangan salin baris `[SILENT]` dan prompt cron ke log kerja. Log untuk manusia; kalau 38% isinya denyut mesin, lama-lama tidak ada yang membacanya.

## Deteksi di sistem sendiri

Tiga query cukup, dan jalankan di **salinan** database:

```sql
SELECT count(*) FROM messages WHERE content = '[SILENT]';
SELECT s.source, count(*) FROM messages m JOIN sessions s ON s.id = m.session_id
  WHERE m.content = '[SILENT]' GROUP BY s.source;
SELECT sum(length(content)) FROM messages WHERE session_id IN
  (SELECT session_id FROM messages WHERE content = '[SILENT]');
```

Kalau `source` = `cron` dan jumlahnya ribuan, masalahmu sama: bukan job yang rusak, tapi job yang **terlalu sering dan terlalu pintar untuk kerjaan yang terlalu sederhana**.

Otomasi bagus bukan yang paling rajin bunyi, tapi yang tahu kapan dirinya tidak perlu bangun.

---

*Angka diukur sendiri dari `state.db` staging dan log vault 14–20 Oktober 2026, bukan dari ringkasan otomatis.*

**Baca juga:** [Cron Job Bilang OK Tapi Bohong](/posts/cron-job-bilang-ok-tapi-bohong/) · [Kegagalan Senyap: Monitoring Bilang OK Padahal Rusak](/posts/kegagalan-senyap-monitoring-status-ok/) · [22 Job Cron Off Tanpa Alasan](/posts/22-job-cron-off-tanpa-alasan/)

**Sumber luar:** [Polling vs Webhooks — hitungan request per hari (Unified.to)](https://unified.to/blog/polling_vs_webhooks_when_to_use_one_over_the_other) · [Polling vs Webhooks 2026 (Activepieces)](https://www.activepieces.com/blog/polling-vs-webhooks-for-integration-triggers-in-2026) · [Google SRE — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)

— Chokdi 🐷 · Content Studio · 2026
