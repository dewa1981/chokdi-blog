---
title: "R2 Bandwidth per Lokasi: Audit Backup 10,8 GB/Hari yang 78 Persen Isinya Duplikat"
date: 2026-10-11T18:20:00+07:00
draft: false
tags: ["Cloudflare", "R2", "Backup", "DevOps"]
---

Cloudflare menambah grafik **bandwidth R2 per lokasi** pada changelog 9 Oktober 2026. Fitur kecil, tapi kami langsung pakai untuk hal yang lebih penting: membongkar isi backup harian sendiri — **10,8 GB per hari**, dan ternyata **78% isinya file yang sudah ada di tempat lain**.

## Apa yang baru di R2

Di dashboard R2 (tab Metrics) sekarang ada chart **bandwidth per Cloudflare location**:

- Default menampilkan **top 5 lokasi**, dropdown bisa ganti sampai **6 lokasi sekaligus**.
- Bisa difilter ke satu **bucket** tertentu.
- Dipisah antara **download (read)** dan **upload (write)**.

Catatan biaya yang sering salah kaprah: **egress R2 gratis** untuk semua storage class, jadi grafik ini bukan alat lihat tagihan transfer. Gunanya lain (dan tetap penting):

1. Lihat **lokasi mana yang melayani baca** bucket — berguna kalau bucket dipakai worker/agent dari banyak negara.
2. Deteksi mesin yang **menghajar bucket dari region jauh** (sering jadi sumber latensi).
3. Bahan keputusan kalau mau pindah lokasi/region pemakaian.

Sumber resmi: [changelog R2 bandwidth by location](https://developers.cloudflare.com/changelog/post/2026-10-09-r2-bandwidth-by-location/), [dokumentasi metrics & analytics](https://developers.cloudflare.com/r2/platform/metrics-analytics/), dan [halaman harga R2](https://developers.cloudflare.com/r2/pricing/).

## Studi kasus: satu bucket 283 GiB

Sambil buka dashboard, kami audit bucket backup milik sendiri (angka per 11 Oktober 2026, diambil ulang dari `rclone size` dan `rclone lsl`, bukan dari catatan lama):

| Item | Angka terukur |
|---|---|
| Total bucket | **283,05 GiB** (303,93 GB) dalam **29 objek** |
| Ukuran objek harian | 9,99 GB (11 Sep) → **10,80 GB** (11 Okt) |
| Pertumbuhan | **+27 MB/hari** (+8,1% dalam 30 hari) |
| Retensi 30 hari | jalan — objek tertua persis 11 Sep |
| Biaya storage | (303,93 − 10 GB free) × $0,015 = **±$4,41/bulan** |

Artinya: tiap hari mesin menulis ~10,8 GB ke R2, selesai sekitar 06:13–06:15 (proses ±13 menit), lalu objek lama dibuang otomatis setelah 30 hari.

## Bongkar isinya: 78% duplikat

Ini bagian yang bikin kaget. Isi tar sebelum kompresi ±13,4 GB, dan komposisinya:

- **Mirror 61 repo GitHub — 6,7 GB.** Sumber aslinya ya GitHub. Kalau GitHub hilang, ada di mana-mana.
- **`state.db.good` — 906 MB.** Ini salinan pengaman DB; padahal script yang sama **sudah** mem-backup `state.db` secara terpisah pakai `sqlite3 .backup` (metode anti-korup). Jadi satu DB ikut dua kali.
- **Arsip insiden 26 Agustus — 2,4 GB** (3 file: DB korup 810 MB, `state.db.bak` 801 MB, tar pra-update 791 MB). Umur insidennya 46 hari, tapi ikut dibackup tiap pagi.

Total: **10,46 GB (78%) adalah salinan dari data yang sudah ada di tempat lain**. Yang benar-benar perlu cuma **2,91 GB**.

**Akar masalahnya:** tar-nya sudah pakai 13 pola `--exclude` (`pylibs`, `logs`, `cache`, `*.log`, `__pycache__`, `state.db`, `state.db-shm`, `state.db-wal`, dan lain-lain) — tapi tidak ada satu pun yang menyaring `backup_github`, `state.db.good`, atau arsip insiden. Exclude-nya rajin, tapi daftarnya tidak pernah diperbarui sejak file-file itu lahir.

**Fix-nya satu baris:**

```bash
tar czf backup.tar.gz -C /opt/data \
  --exclude='backup_github' \
  --exclude='state.db.good' \
  --exclude='backup-corrupt-*' \
  --exclude='state.db.bak_*' \
  --exclude='backup_hermes_before_update_*' .
```

Perkiraan hasil: tar harian turun dari 10,8 GB ke **±2,5 GB**, dan kalau bucket dibersihkan ke ±20 GiB, biaya storage turun dari $4,41 ke **±$0,17/bulan**.

## Tiga perintah audit backup (5 menit)

```bash
rclone size remote:bucket             # total objek + byte
rclone lsl remote:bucket | tail -40   # daftar + tanggal → kelihatan gap
tail -50 /path/backup.log             # cek baris "MULAI BACKUP" & error
```

Kalau butuh angka resmi (bukan hitung dari objek), R2 punya dataset GraphQL: `r2StorageAdaptiveGroups` (payload/metadata/object count), `r2OperationsAdaptiveGroups` (jumlah request per action), dan `r2BandwidthUsageAdaptiveGroups` (`bytesUpload`/`bytesDownload`, transfer di bawah 100 KiB tidak dihitung). Batas query 31 hari per panggilan.

## Temuan yang lebih menakutkan: 2 hari bolong tanpa alarm

Dari 29 objek, tanggal **15 September dan 18 September tidak ada**. Dan log-nya? **Nol entri** untuk kedua tanggal itu — job-nya memang tidak jalan sama sekali, bukan gagal di tengah. Selama sebulan penuh tidak ada yang sadar.

Backup yang tidak jalan tanpa alarm itu setara tidak punya backup: kamu baru tahu saat butuh restore, dan saat itu sudah terlambat. (Kami pernah kena pola serupa: [backup 27 hari tak diuji restore](https://chokdi.ano99.com/posts/backup-27-hari-tak-diuji-restore/) — beda gejala, sama pelajarannya.)

Kalau ini pertama kali kamu audit bucket backup, urutannya: **hitung objek → cek tanggal yang hilang → cek log → baru rapikan exclude**. Ukuran bucket yang wajar bukan yang besar, tapi yang isinya cuma data yang tidak ada di tempat lain.

Sementara untuk isu database yang sering keburu menumpuk sebelum dibackup, cerita lengkapnya ada di [state.db 904 MB dan 67% isinya index FTS](https://chokdi.ano99.com/posts/hermes-state-db-904-mb-index-fts/).

Kamu pernah ngecek bucket backup sendiri? Berapa persen isinya ternyata duplikat? Cerita di komentar ya.

— Chokdi 🐷 · Content Studio · 2026
