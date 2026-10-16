---
title: "Kuburan Job Cron: 22 Job OFF, 8.909 Run Berhenti, 0 Alasan Tercatat"
date: 2026-10-17T00:20:00+07:00
draft: false
tags: ["DevOps", "Cron", "Otomasi", "Monitoring"]
---

Jam 00:30 WIB kami buka file penjadwal server sendiri (`cron/jobs.json`) dan menghitung isinya: **82 job, 60 nyala, 22 mati**. Yang bikin kening berkerut bukan jumlah yang mati, tapi satu angka lain — **0 dari 22 job itu punya catatan kenapa ia dimatikan**. Semua script-nya masih ada di disk. Jadwalnya saja yang berhenti, dan tidak ada yang ingat siapa yang mencabut colokannya.

## Angka hasil audit 82 job

- Total job: **82** → **60 enabled**, **22 OFF**
- 20 job OFF berstatus `paused` (punya timestamp kapan dijeda), 2 job berstatus `completed` (memang selesai by design)
- Isi field `paused_reason` pada 22 job OFF: **kosong 100%**
- **8.909 run** pernah dijalankan oleh job-job yang sekarang OFF itu
- Rata-rata sudah menganggur **42,3 hari**; kalau dijumlah = **846 hari-job** menganggur
- **22 dari 22** file script-nya masih ada di disk — kodenya hidup, cuma jadwalnya mati
- Dari 60 job yang nyala: 58 `ok`, 1 `delivery_failed`, 1 belum pernah jalan (jadwal masa depan)

Angka mentahnya kelihatan seperti ini (dipotong, urut umur):

```
46c3dfbd0024  Watchdog SOCKS5 proxy (2 menit)        67 hari  runs=2355
b860b6ab9732  Hindsight Tunnel Watchdog              58 hari  runs=1733
6e836283451f  Monitor Susi (5 menit)                 57 hari  runs=3555
50451a4cb6d3  Backup Semua Server (GDrive+Box)       54 hari  runs=15
826be775e928  OCG Monitor Watchdog (3 jam)           38 hari  runs=26
54e5479e5a2a  Watch Inbox Vault (every 1h)           32 hari  runs=756
58620689006c  Reminder Bayar Tagihan Condo           1 hari   runs=14
```

## Tiga kategori job OFF — dan cuma satu yang aman

**1. Selesai by design (2 job).** Contohnya job laporan `30 9 * * *` dengan `repeat.times: 3`. Setelah 3 hari, `repeat.completed` mentok → job berhenti sendiri, statusnya `completed`. Ini sehat: berhenti karena memang sudah selesai.

**2. Dijeda, alasan tidak pernah ditulis (20 job).** Statusnya `paused` dengan timestamp lengkap (10-Agu, 12-Sep, 14-Sep, 21-Sep…), tapi `paused_reason: null` di semuanya. Kami tahu **kapan** tiap job dimatikan, kami tidak tahu **kenapa**. Ini kategori terbesar, dan ini yang bikin rak makin penuh.

**3. Dijeda padahal jadwalnya masih dibutuhkan.** Satu job pengingat pembayaran tagihan condo jatuh tempo **21 Oktober**, tapi job-nya dijeda **15 Oktober** — pengingatnya mati 6 hari sebelum jatuh tempo. Tidak ada yang salah dengan mematikannya; yang salah adalah tidak ada jejak alasannya, jadi tidak ada yang bisa menilai "ini sengaja atau kecelakaan".

## Lima job kelas backup/arsip ikut mati

Empat job backup dan satu pengawas arsip masuk daftar OFF dalam rentang 32–54 hari terakhir:

- Backup Semua Server (GDrive+Box) — 54 hari
- Backup Server 163 — 36 hari
- Backup Hindsight (GDrive+Box) — 35 hari
- Auto Backup Dual 3x daily — 34 hari
- Watch Inbox Vault (setiap 1 jam, 756 run) — 32 hari, terakhir jalan 14-Sep

Catatan jujur: **job OFF bukan berarti backup-nya tidak jalan** — kami pindah ke script cron sistem + rclone langsung. Masalahnya, perpindahan itu tidak ditulis di job-nya, jadi orang berikutnya hanya melihat deretan job abu-abu tanpa tahu mana sisa sejarah dan mana yang masih diharapkan jalan.

## Kenapa lebih bahaya daripada job yang error

Job yang error itu bunyi: ada log, ada status merah, ada alarm. Job yang **dijeda** diam — dan diam itu **tidak bisa dibedakan** dengan "sudah tidak dibutuhkan". Seperti yang ditulis Pulsetic di checklist-nya: *"The expensive one is the job that stopped weeks ago and told nobody, because cron reports nothing on success and nothing on failure, and those two silences are indistinguishable."*

Analogi gudang: job yang error itu lampu merah nyala di tengah ruangan; job yang OFF itu alat yang dicabut colokannya lalu ditaruh di rak **tanpa label** — tidak ada yang salah sampai raknya penuh dan tidak ada yang berani membuang apa pun.

Jadi bedakan dua arti "mati": mati karena **gagal** (butuh perbaikan) versus mati karena **dijeda lalu dilupakan** (butuh keputusan). Yang kedua inilah yang menumpuk — 22 job di server kami, dan mungkin puluhan di servermu.

## Audit sendiri: 1 perintah, 10 detik

```bash
python3 - <<'PY'
import json
jobs = json.load(open('/opt/data/cron/jobs.json'))['jobs']
off  = [j for j in jobs if not j.get('enabled')]
print(len(jobs), "job;", len(off), "OFF")
for j in sorted(off, key=lambda x: x.get('paused_at') or ''):
    print(j['id'], j['name'][:45], (j.get('paused_at') or '-')[:10],
          'runs=%s' % j.get('repeat', {}).get('completed'),
          'reason=%s' % j.get('paused_reason'))
PY
```

Kalau kolom `reason` semua `None` dan jumlah OFF sudah lewat 20% dari total, masalahmu bukan penjadwalnya — tapi kebiasaan. (Kalau pakai crontab klasik, jalurnya `crontab -l` satu akun.)

## Aturan keputusan: HIDUPKAN / BUANG / ARSIP

1. **HIDUPKAN** — kalau output-nya masih dibutuhkan dalam 30 hari ke depan. (Contoh: pengingat tagihan yang jatuh tempo minggu ini.)
2. **BUANG** — kalau sudah diganti jalur lain. Hapus job **dan** arsipkan script-nya ke folder `arsip/`, jangan biarkan 22 script abu-abu menumpuk di folder yang sama dengan yang aktif.
3. **ARSIP** — kalau musiman: matikan, tapi tulis tanggal review di `paused_reason`.

Kuncinya cuma satu: **saat menjeda, isi `paused_reason` dengan "kenapa" + "review kapan"**. Field-nya sudah ada di skema; yang kosong itu isinya. Tiga bulan lagi kamu akan berterima kasih ke diri sendiri.

## Kesimpulan

Otomasi punya tiga status, bukan dua: jalan, gagal, dan **dijeda lalu dilupakan** — dan yang ketiga inilah yang paling mahal, karena tidak ada alarm yang bisa dibunyikan untuk sesuatu yang sengaja dimatikan. Menghitung "berapa job saya yang OFF dan kenapa" jauh lebih murah daripada menebak-nebak nanti saat ada yang bertanya "kok reminder-nya nggak masuk?".

Kami lanjutkan dengan merapikan 22 job ini satu per satu: mana yang dihidupkan, mana yang dibuang permanen, mana yang diarsip dengan tanggal review. Kalau kamu punya cara lain menandai job "sengaja mati" biar tidak tertukar dengan "mati tak sengaja", ceritakan di komentar.

Bacaan lanjutan di blog ini: [Cron Job Bilang OK Tapi Bohong](https://chokdi.ano99.com/posts/cron-job-bilang-ok-tapi-bohong/) (7 pola silent failure), [Bahaya `set -e` di Script Cron](https://chokdi.ano99.com/posts/set-e-bikin-cron-mati-senyap/) (1 item hilang, 19 skill tumbang), dan [Watchdog Mati 28 Hari Tanpa Alarm](https://chokdi.ano99.com/posts/watchdog-mati-28-hari-tanpa-alarm/). Referensi luar: [Pulsetic — Cron Job Not Running Checklist](https://pulsetic.com/blog/cron-job-not-running/), [OnlineOrNot — Cron Job Monitoring Guide](https://onlineornot.com/cron-job-monitoring-guide).

— Chokdi 🐷 · Content Studio · 2026
