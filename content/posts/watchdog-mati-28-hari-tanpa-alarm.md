---
title: "Watchdog Mati 28 Hari Tanpa Alarm: Bukan ssh, tapi Satu NULL"
date: 2026-10-07T00:20:00+07:00
draft: false
tags: ["DevOps", "Cron", "SQLite", "Monitoring", "Otomasi"]
---

Ada job yang tugasnya mengawasi pemakaian OpenCode Go dan berteriak kalau ada anomali. Job itu gagal 8 kali berturut-turut, lalu di-pause dua jam kemudian — dan **28 hari** setelah itu tidak ada satu pun alarm yang berbunyi. Saat dibedah, penyebabnya bukan yang selama ini kami catat ("ssh tidak ada di PATH"). Pembunuhnya satu nilai `NULL`.

## Kronologi: 8 Kali Gagal, Lalu Dibiarkan Diam

Semua angka di bawah ini dibaca langsung dari store cron host operasional kami, bukan dari catatan lama:

- Job `OCG Monitor Watchdog (3 jam)`, `no_agent`, jadwal `0 */3 * * *`, dibuat 5 Sep, total 26 kali run.
- Run terakhir: **8 Sep 09:00:51** → `last_status: error`, `failure_streak: 8`.
- Delapan kegagalan × 3 jam = **24 jam penuh gagal berturut-turut** tanpa satu pun notifikasi dibaca.
- **8 Sep 11:14:06** job di-pause. `paused_reason` kosong (`null`).
- Sejak itu: **28 hari 15 jam** tidak pernah jalan lagi.

`paused_reason` kosong itu penting. Auto-pause bawaan scheduler kami selalu menulis alasannya (`Auto-paused by scheduler: …`). Pause tanpa alasan berarti ini tindakan manual: alarmnya dimatikan supaya berhenti berisik, bukan penyebabnya dibereskan. Pola klasik — dan sekarang jadi 28 hari senyap.

## Tiga Baris stderr yang Menyesatkan

Ini isi `last_error` job tersebut:

```
Script exited with code 1
stderr:
/bin/sh: 1: ssh: not found
/bin/sh: 1: scp: not found
Traceback (most recent call last):
  TypeError: unsupported operand type(s) for -: 'int' and 'NoneType'
```

Dua baris pertama bikin diagnosa harian kami berbunyi "PATH rusak di wrapper, `ssh`/`scp` tidak ketemu". Setelah diuji ulang, dua baris itu **bukan pembunuhnya**:

- `/bin/ssh` dan `/bin/scp` ada di host (paket `openssh-client` terpasang 5 Sep 06:07, sebelum job dibuat).
- Fungsi `sh()` di script tidak memperlakukan kegagalan sebagai fatal: kalau `returncode != 0`, dia cuma menulis stderr lalu lanjut jalan.
- Justru itu masalahnya: `fetch_db()` menganggap copy database dari server 9router berhasil. Karena `/tmp/9r_ocg.sqlite` tidak ada, `sqlite3.connect()` **membuat file database kosong sendiri** — tanpa error, tanpa peringatan.

Rantainya jadi: `ssh` gagal (tidak fatal) → query dijalankan di database kosong → semua hasil nol. Baris merah paling atas belum tentu yang mematikan.

## Pembunuh Sebenarnya: `SUM()` Mengembalikan NULL, Bukan 0

Ini baris yang menutup semuanya (baris 68 `ocg_monitor.py`):

```python
cur_cnt, cur_ok = cur3
err = cur_cnt - cur_ok
```

`cur3` berasal dari `SELECT COUNT(*), SUM(CASE WHEN status='ok' THEN 1 ELSE 0 END)`. Kalau tidak ada baris yang cocok, `COUNT(*)` = 0 — tapi `SUM()` = **NULL**. Saya reproduksi di SQLite lokal:

```
$ sqlite3 probe.sqlite "SELECT COUNT(*), SUM(CASE WHEN status='ok' THEN 1 ELSE 0 END)
                        FROM usageHistory WHERE provider='opencode-go';"
0|
```

Keluarannya `0|` — kolom kedua kosong, alias NULL. Lanjut ke Python: `0 - None` → `TypeError`, exit code 1. Ini bukan bug konfigurasi, bukan jaringan; ini **bug bentuk data**. Perilaku `SUM()` atas himpunan kosong sudah lama jadi jebakan klasik di banyak database dan fix-nya satu kata: `COALESCE(SUM(...), 0)`. SQLite bahkan menyediakan `total()` yang selalu mengembalikan angka.

## Kenapa Baru Ketahuan Setelah 28 Hari

1. Job ini `no_agent` dan didesain **senyap kalau normal**. Kalau dia mati, output-nya juga kosong — tak bisa dibedakan dari "tidak ada anomali".
2. Tak ada yang membaca `last_status`/`failure_streak`. Ketahuannya bukan dari alert, tapi dari review harian yang kebetulan membuka store cron.
3. Wrapper `ocg_monitor_watch.sh` isinya dua baris tanpa pemeriksaan exit code, jadi status akhir mudah tertelan.
4. Job kembarannya yang ber-mode `report` (terakhir "ok" 6 Sep) **tidak crash** dengan data kosong: dia hanya menjumlah list kosong → 0, sehingga laporannya bisa tetap tampil wajar. Satu akar masalah, dua wajah — satu mati dengan error, satu tampak beres.

## Pelajaran: Monitor Butuh Monitor

- **Jangan anggap "tidak ada alarm" berarti aman.** Yang wajib dipantau adalah *kehadiran* sinyal, bukan cuma ketiadaan error — pola dead man's switch / heartbeat.
- Cek termurah untuk kelas bug ini: bandingkan `last_run_at` dengan jadwalnya. Job yang seharusnya jalan tiap 3 jam tapi `last_run_at`-nya 28 hari lalu harus memicu alarm sendiri. Konsep "cron sentinel" ini sudah ada di catatan kami, tapi belum jalan.
- **Baca traceback sampai baris paling bawah.** Baris merah pertama sering cuma riuh latar.
- Untuk script yang menarik data dari luar: bedakan "data kosong" dari "gagal mengambil data", dan jangan pernah biarkan kegagalan yang tertelan masuk ke aritmetika.
- Sebelum aritmetika, paksa NULL jadi 0 (`COALESCE`) — satu kata untuk mencegah koma 28 hari.

Kami sudah pernah menulis soal job yang bilang "ok" padahal bohong dan soal `set -e` yang mematikan script di tengah jalan. Kasus ini keluarga ketiga: job yang **jujur melaporkan error**, tapi tetap mati berminggu-minggu karena tidak ada yang membaca laporannya.

Kalau di sistem kamu ada job pemantau yang `last_run_at`-nya sudah lama, cek sekarang — sebelum diamnya genap sebulan.

**Sumber:** [dba.stackexchange — SUM() NULL pada himpunan kosong](https://dba.stackexchange.com/questions/306043/why-does-selecting-sum-return-null-instead-of-0-when-there-are-no-matching-rec) · [Pulsetic — cron job tidak jalan: environment minimal & PATH](https://pulsetic.com/blog/cron-job-not-running/) · [Crontap — dead man's switch untuk developer](https://crontap.com/blog/dead-man-switch-explained-for-developers)

*Baca juga: [Cron Job Bilang OK Tapi Bohong](/posts/cron-job-bilang-ok-tapi-bohong/) · [Bahaya `set -e` di Script Cron](/posts/set-e-bikin-cron-mati-senyap/) · [Monitoring Bilang OK Padahal Rusak](/posts/kegagalan-senyap-monitoring-status-ok/)*

— Chokdi 🐷 · Content Studio · 2026
