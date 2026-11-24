---
title: "Kenapa Koneksi PostgreSQL Mahal? 6 ms per Koneksi, Throughput Anjlok 107×"
date: 2026-11-24T18:10:00+07:00
draft: false
tags: ["PostgreSQL", "Database", "Benchmark", "PgBouncer"]
---

# Kenapa Koneksi PostgreSQL Mahal? 6 ms per Koneksi, Throughput Anjlok 107×

Aplikasi naik trafik, muncul `FATAL: sorry, too many clients already`. Refleks pertama: naikkan `max_connections`. Padahal pertanyaan yang lebih penting: **seberapa mahal sih satu koneksi PostgreSQL?** Kami ukur sendiri di container bersih, bukan mengutip forum. Hasilnya: koneksi baru menambah **±6 ms** sebelum query pertama selesai, dan pola "connect per transaksi" membuat throughput **107× lebih rendah** dibanding koneksi tetap.

## 🧩 Akarnya: satu koneksi, satu proses

PostgreSQL bukan server event-loop. Dokumentasi resminya menyebut model **process per user**: postmaster mendengarkan port, lalu **setiap permintaan koneksi memunculkan proses backend baru**. Semua backend berkomunikasi lewat semaphore dan shared memory.

Jadi satu `connect()` bukan cuma bikin socket. Ada `fork()`, inisialisasi backend, autentikasi, lalu pembacaan katalog sistem sebelum query pertama jalan. Dokumentasi juga menegaskan `max_connections` ikut menentukan alokasi resource, **termasuk shared memory** — menaikkannya bukan tanpa biaya.

## 🔬 Cara kami mengukur

PostgreSQL **18.6** (image Alpine) di Docker 29.7.2, host 8 vCPU / 64 GB RAM. Setelan: `max_connections=200`, `shared_buffers=256MB`, data pgbench skala 10, beban select-only. Yang dibandingkan cuma satu variabel: koneksi tetap vs koneksi baru tiap transaksi.

```bash
# koneksi tetap, 10 klien, 10 detik
pgbench -U bench -S    -c 10 -j 2 -T 10 bench
# koneksi baru tiap transaksi (flag -C)
pgbench -U bench -S -C -c 10 -j 2 -T 10 bench
```

## 📊 Hasil: 46.614 TPS jadi 433 TPS

| Skenario | Klien | Latensi rata-rata | TPS |
|---|---|---|---|
| Unix socket, koneksi tetap | 10 | 0,215 ms | **46.614** |
| Unix socket, koneksi baru tiap transaksi | 10 | 23,090 ms | **433** |
| TCP + SCRAM, koneksi tetap | 10 | 0,256 ms | 39.114 |
| TCP + SCRAM, koneksi baru tiap transaksi | 10 | 26,225 ms | 381 |
| Unix socket, koneksi tetap | 1 | 0,135 ms | 7.387 |
| Unix socket, koneksi baru tiap transaksi | 1 | 6,069 ms | 164,8 |

Selisih 6,069 ms dan 0,135 ms itu **≈5,93 ms murni biaya buka koneksi** untuk satu klien. Dengan 10 klien, throughput jatuh dari 46.614 ke 433 TPS — sekitar **107× lebih lambat**. Menarik: lewat TCP + SCRAM di loopback, biayanya 6,348 ms, cuma **+0,28 ms** dibanding unix socket. Jadi yang mahal bukan protokolnya, tapi **fork + inisialisasi backend**.

## 💾 Memori: RSS 14,5 MB, PSS 1,5 MB

Mitos populer: satu koneksi makan ~10 MB. Kami ukur dua cara, hasilnya jauh berbeda:

| Metrik | Baseline (9 proses) | Saat ada klien | Selisih per backend |
|---|---|---|---|
| RSS total | 113.556 KB | 854.804 KB | **14,5 MB** |
| PSS total | 49.479 KB | 64.878 KB (10 backend) | **1,5 MB** |

Kuncinya: `shared_buffers` 256 MB dipetakan ke **setiap** backend, dan halaman shared yang tersentuh ikut dihitung di RSS masing-masing proses. Itu sebabnya RSS membengkak dan terlihat seperti 14,5 MB per koneksi. PSS membagi halaman shared secara proporsional, jadi angka 1,5 MB (private hanya 886 KB) lebih jujur untuk backend idle.

Tapi jangan senang dulu: 1,5 MB itu **saat menganggur**. Begitu query berjalan, tiap backend bisa memakai `work_mem` per node sort atau hash. `work_mem` 4 MB × 3 node × 200 koneksi = 2,4 GB di skenario terburuk, belum termasuk catalog cache yang tumbuh setelah banyak query.

## 🚰 Pooler: 2 kB per koneksi

Di sinilah PgBouncer masuk. Dokumentasinya menyebut kebutuhan memorinya **2 kB per koneksi** karena tidak perlu melihat paket penuh sekaligus. Default-nya `pool_mode = session`, `default_pool_size = 20`, `max_client_conn = 100`, dan jumlah file descriptor yang perlu disiapkan = `max_client_conn + (pool_size × database × user)`.

Tapi transaction pooling memutus beberapa fitur: `SET`/`RESET`, `LISTEN`, `WITH HOLD CURSOR`, `PREPARE`/`DEALLOCATE`, dan session advisory lock tidak didukung. Prepared statement protocol-level tetap bisa, asal `max_prepared_statements` diisi bukan nol.

## ✅ Checklist praktis

1. **Ukur dulu** di beban nyata: bandingkan `pgbench -S` vs `pgbench -S -C`. Kalau selisihnya kecil, aplikasi memang sudah pakai koneksi tetap.
2. **Pasang pooler** sebelum menaikkan `max_connections`. Mulai dari session mode kalau aplikasi belum siap.
3. Kalau pindah ke transaction mode, matikan prepared statement sisi aplikasi atau aktifkan `max_prepared_statements`.
4. Hitung RAM realistis: private backend + `shared_buffers` + `work_mem` × konkurensi query.
5. Set `idle_in_transaction_session_timeout` supaya transaksi nyangkut tidak menahan slot koneksi.

## 🎯 Kesimpulan

Koneksi PostgreSQL mahal bukan karena protokolnya, tapi karena model proses-per-koneksi: satu `fork()`, satu backend, satu set cache katalog. Di mesin kami biayanya ±6 ms per koneksi dan 107× throughput saat pola connect-per-transaksi dipakai. Kalau aplikasi Anda membuka koneksi per request, pooler bukan optimasi kosmetik — itu yang menyelamatkan database dari kehabisan slot.

Baca juga soal [WAL streaming untuk PITR](/posts/postgres-pitr-wal-streaming-databasus/), [kesalahan port backup yang bikin file 0 byte](/posts/backup-postgres-port-salah-0-byte/), dan [kapan database branch masuk akal](/posts/agent-database-sendiri-branch-postgres/).

Sumber resmi: [How Connections Are Established](https://www.postgresql.org/docs/current/connect-estab.html) · [Connections and Authentication](https://www.postgresql.org/docs/current/runtime-config-connection.html) · [PgBouncer features](https://www.pgbouncer.org/features.html).

— Chokdi 🐷 · Content Studio · 2026
