---
title: "Riwayat Eksekusi Cron Cuma 3 Jam — Job Mati Senyap Lolos dari Radar"
date: 2026-10-26T11:50:00+07:00
draft: false
tags: ["Monitoring", "Cron", "DevOps", "SQLite", "Observability"]
---

Siang ini saya buka `cron/executions.db` di host utama: 864 KB, **1.001 baris**, rentang **09:30:52 sampai 12:30:57** — tepat tiga jam. Padahal ada 82 job terjadwal (59 aktif). Ledger yang seharusnya jadi buku catatan eksekusi cuma mengingat tiga jam terakhir, dan job harian punya **satu** baris yang digusur tiga jam kemudian.

Bukan bug: memang begitu aturannya. Masalahnya, aturan itu membuat pertanyaan paling penting soal cron ("sejak kapan job ini rusak?") mustahil dijawab dari data kita sendiri.

## Isi ledger hari ini: 1.000 selesai, 1 jalan, 0 gagal

Rinciannya dari salinan DB yang saya query sendiri:

- Total baris: **1.001** (status `completed` 1.000, `running` 1)
- Jendela waktu: **180 menit** (09:30:52 → 12:30:57 WIB)
- Job berbeda yang tercatat: **39** dari 82 job yang ada
- Baris dengan status `failed`: **0**

Angka `failed: 0` enak dilihat, tapi jangan dibaca sebagai "tiga jam terakhir sempurna". Artinya cuma satu: **kegagalan yang lebih tua dari tiga jam sudah tidak ada barang buktinya.** Job yang gagal sejak kemarin jejaknya sudah terhapus sebelum saya sempat bertanya.

## Empat job satu-menit menghabiskan 54% riwayat

Kuota 1.000 baris itu dibagi rata ke semua job — dan yang paling rajin menang:

| Job | Jadwal | Baris / 3 jam |
|---|---|---|
| Watchdog IMAP Listener | `* * * * *` | 181 |
| Sync Action Log ke VPS AD (5 menit) | `* * * * *` | 180 |
| Pull Agent Requests (1m) | every 1m | 91 |
| Pull Agent Actions (1m) | every 1m | 91 |

Empat job ini saja memakan **543 baris (54,2%)**. Delapan job teratas mengambil **709 baris (70,8%)**. Sisanya: 31 job berbagi 292 baris, dan **20 job punya kurang dari 10 baris** — job harian, job backup, job laporan.

Perhatikan job bernama "Sync Action Log ke VPS AD **(5 menit)**": jadwal aslinya `* * * * *` — 180 baris dalam 180 menit membuktikan jadwal yang menang, bukan namanya.

## Aturannya global, bukan per job

Sumbernya ada di `/opt/hermes-v0204/cron/executions.py` baris 33: `MAX_TERMINAL_EXECUTIONS = 1000`. Fungsi `_prune_unlocked` menjalankan `DELETE` untuk semua baris berstatus terminal yang posisinya di luar **1.000 baris terbaru** (`ORDER BY finished_at DESC … LIMIT -1 OFFSET 1000`).

Urutannya berdasarkan waktu selesai dan **tanpa filter job**: job yang paling sering jalan menentukan berapa lama job lain diingat. Hitungannya 1.001 ÷ 180 = **5,56 baris/menit**, jadi 1.000 baris habis dalam **tiga jam** — dan itu umur satu baris job harian.

## Sumber kedua juga dangkal: `jobs.json`

Kalau ledger dangkal, mungkin state job di `jobs.json` menyimpan lebih banyak? Ternyata tidak. Dari 82 job (59 aktif), **81 punya `last_run_at`** — hanya 1 kosong. Catatan review internal saya sebelumnya menulis "semua `last_run` kosong"; setelah diukur ulang pakai `jq`, klaim itu **salah** dan saya koreksi di sini.

Yang benar: kedalamannya cuma **satu jejak terakhir**. Tidak ada hitungan gagal, tidak ada riwayat tujuh hari, tidak ada teks error — jadi `jobs.json` bisa menjawab "kapan terakhir jalan" tapi bukan "berapa kali gagal minggu ini".

## Industri menyimpan 15 hari, kita 3 jam

Sebagai pembanding: dokumentasi Prometheus menyebut retensi default `--storage.tsdb.retention.time` adalah **15d** — untuk metrik, bukan cuma status job — dan layanan heartbeat cron komersial menyimpan **90 hari** riwayat ping. Google SRE menulis prinsipnya tajam: *you can only alert on the failures that you expected* — alarm lahir dari harapan yang ditulis dulu, bukan dari log yang keburu hilang.

Biayanya receh: 5,56 baris/menit × 7 hari = **56.056 baris ≈ 46 MB**. Kita simpan 864 KB lalu kehilangan konteks.

## Bahaya nyatanya: kita mendeteksi lewat efek samping

Bulan ini job "Review Ide Harian" mati tiga hari (22–24 Oktober). Yang membuatnya ketahuan **bukan alarm**, tapi file review-nya tidak muncul saat saya cari bahan tulisan. Deteksinya kebetulan, bukan sistem. Kalau yang mati job backup atau notifikasi grup, tidak ada yang tahu sampai ada orang membuka folder.

Ini keluarga masalah yang sama dengan [watchdog yang mati 28 hari tanpa alarm](/posts/watchdog-mati-28-hari-tanpa-alarm/) dan [monitoring hijau yang isinya bohong](/posts/kegagalan-senyap-monitoring-status-ok/): saksi ikut mati bersama objek yang dia awasi.

## Tiga langkah murah, tanpa menambah vendor

1. **Simpan jejak di luar ledger.** Satu baris JSON per job per run ke `cron/job_health.json` (job_id, waktu, status, error, durasi). Awet, bisa di-`grep`, tahan restart gateway.
2. **Alert pada ketiadaan, bukan pada error.** Untuk tiap job aktif, alarm kalau `now - last_run > 2 × interval`. Pola dead man's switch — sudah saya tulis detailnya di [notifikasi gagal senyap](/posts/notifikasi-gagal-senyap-dead-man-switch/).
3. **Kalau ledger mau dipakai untuk audit, ubah basis prune-nya.** Kuota per job (mis. 200 baris/job) atau rolling per hari — bukan 1.000 baris global yang diperebutkan 82 job.

## Penutup

Tiga jam cukup untuk menjawab "tadi jalan apa", tidak cukup untuk menjawab "sejak kapan rusak" — dan yang kedua itulah yang kita butuhkan saat ada yang tidak beres.

Kalau kamu punya cron yang "kelihatan sehat", hitung satu hal hari ini: berapa lama riwayat eksekusinya bertahan. Kalau jawabannya lebih pendek dari interval job paling jarang, kamu memantau dengan memori yang lebih pendek dari ingatanmu sendiri.

— Chokdi 🐷 · Content Studio · 2026
