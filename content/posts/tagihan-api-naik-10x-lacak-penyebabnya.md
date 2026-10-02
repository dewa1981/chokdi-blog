---
title: "Tagihan API Naik 10x? Ini Cara Kami Melacak Penyebabnya"
date: 2026-10-03T00:15:00+07:00
draft: false
tags: ["API", "Monitoring", "Cron", "Web3", "Tips"]
---

Bulan lalu tagihan layanan RPC kami **$0,61**. Bulan ini **$6,43** — naik **10,5x**. Nominalnya memang masih receh, tapi bukan nominalnya yang bikin kami berhenti: pola naiknya. Kalau kenaikan 10x dibiarkan, bulan depan bisa jadi $64, dan sebulan lagi $640. Ini cara kami melacak penyebabnya dalam sekitar setengah jam, plus dua jebakan yang hampir bikin perbaikannya jadi sia-sia.

## 1. Baca invoice dulu — jangan tebak-tebakan

Langkah pertama bukan buka kode, tapi buka tagihan. Dari invoice ketemu dua angka penting:

- Total pemakaian: **14.293.844 compute unit (CU)** sebulan
- Tarif efektif akun kami: **$0,00000045 per CU** → total **$6,43**

Kenapa CU, bukan jumlah request? Karena penyedia RPC seperti Alchemy menagih berdasarkan **berat metode**, bukan jumlah panggilan. Di dokumentasi resminya, `eth_blockNumber` cuma 10 CU, `eth_call` 26 CU, sementara `eth_getLogs` 75 CU. Jadi 1.000 request ringan bisa lebih murah dari 50 request berat. Kalau kita cuma lihat "berapa kali script jalan", kita akan salah menyimpulkan.

## 2. Ubah tagihan jadi "biaya per eksekusi"

Ini trik yang paling cepat membuka mata. Kuncinya ada di `crontab`: script kami jalan **tiap 10 menit**.

- 144x sehari × 30 hari = **4.320x sebulan**
- 14.293.844 CU ÷ 4.320 = **±3.309 CU sekali jalan**

Angka ini yang menentukan arah perbaikan:

- Per-eksekusi **kecil** tapi tagihan besar → masalahnya **frekuensi** (jalan terlalu sering).
- Per-eksekusi **besar** → masalahnya **metode** (panggilan yang berat-berat).

Di kasus kami per-eksekusi termasuk besar, jadi frekuensi bukan penyebab utama — metodenya yang perlu dikuliti.

## 3. Cari siapa saja yang memakai kunci itu

Ini kesalahan klasik yang akhirnya kami temukan: **satu API key dipakai bareng beberapa sistem.** Akibatnya tagihan tidak bisa langsung diatribusi ke satu proyek, dan kuncinya tidak bisa dicabut tanpa mematikan yang lain.

Pelajarannya sederhana tapi mahal: **satu key untuk satu sistem.** Kalau penyedia tidak menyediakan statistik per-app, catat pemakaian manual — minimal sekali sebulan, saat tagihan turun.

## 4. Cari metode yang paling mahal

Setelah tahu Script A memakai kunci itu, kami bedah isi script-nya. Di kasus kami penyumbang terbesar adalah:

- Panggilan riwayat transfer (`getAssetTransfers`) di **dua chain** sekaligus
- Panggilan **Solana**: `getSignaturesForAddress` lalu `getParsedTransaction` **per transaksi**

Yang terakhir itu paling mahal, karena satu alamat bisa menghasilkan puluhan transaksi, dan tiap transaksi diparse satu-satu. Inilah "biaya senyap" yang tidak kelihatan kalau kita cuma menghitung jumlah request di log.

## 5. Matikan sumbernya — lalu verifikasi

Perbaikannya cuma satu baris: **comment baris cron-nya.** Tapi ada urutan yang harus dipatuhi:

1. Backup file cron dulu sebelum diubah.
2. Beri penanda siapa dan kapan yang mengubah (contoh: `# [PAUSE 2026-10-02]`), supaya orang berikutnya tidak bingung kenapa job tidak jalan.
3. Verifikasi tiga hal: file cron benar-benar ter-comment, **tidak ada proses yang masih jalan** (`pgrep -af payment_monitor` → kosong), dan file log **berhenti bertambah** (cek jam modifikasinya).

## Jebakan #1: backup di `/etc/cron.d/` tetap dijalankan cron

Ini jebakan yang hampir membuat kami tetap ditagih walau cron sudah "dimatikan". Semua file di folder `/etc/cron.d/` dibaca cron, **termasuk file backup** seperti `antiddos-payment.bak-20261002` — selama formatnya masih valid, job-nya tetap jalan.

Jadi "sudah aku backup di sebelah file aslinya" justru membuat job **dobel**. Solusinya: taruh backup di luar folder itu, misalnya `/root/backup-cron/`. Setelah dipindah, baru cek ulang isi folder cron dan pastikan hanya file yang memang seharusnya jalan yang tinggal di sana.

## Jebakan #2: log yang tidak pernah diputar

Log script ini sudah menumpuk **3,1 MB** karena setiap eksekusi menulis ke file yang sama tiap 10 menit selama berbulan-bulan. Tidak berbahaya, tapi mempersulit pembacaan dan memakan disk pelan-pelan. Pakai `logrotate`, atau minimal tulis ke file ber-tanggal.

## Pelajaran yang kami bawa

- **Alarm anggaran itu wajib, walaupun angkanya kecil.** Tagihan $6 tidak ada yang lihat. 10x dari angka kecil tetap 10x.
- **Satu key untuk satu sistem** — supaya bisa diatribusi dan dicabut tanpa efek samping.
- **Hitung biaya per eksekusi, bukan per bulan.** Angka per-eksekusi jauh lebih mudah dibandingkan dengan ekspektasi.
- **Verifikasi setelah mematikan sesuatu.** "Sudah dimatikan" tanpa bukti (0 proses + log berhenti) bukan bukti. Prinsip yang sama kami pakai waktu menemukan [cron yang bilang sukses tapi selalu menolak](/posts/cron-job-bilang-ok-tapi-bohong/) dan [sinkronisasi yang macet 12 jam tanpa alarm](/posts/git-sync-cron-macet-12-jam/).
- Kalau memang butuh data on-chain, pilih metode yang tepat dulu — lihat [12 hal yang bisa dilakukan dari satu perintah CLI](/posts/alchemy-cli-12-hal-on-chain-satu-perintah/).

## Kesimpulan

Tagihan API yang naik mendadak hampir selalu punya jejak: **CU per eksekusi × frekuensi × jumlah pemakai kunci**. Baca invoice, hitung per-eksekusi, cari pemakai kunci, bedah metode termahal, lalu matikan sumbernya — dan verifikasi. Empat langkah itu tidak butuh alat mahal, cuma butuh kemauan membuka dashboard sebelum menyalahkan kode.

Kalau di servermu ada script yang jalan tiap 5-10 menit dan memanggil API berbayar, cek hari ini: berapa CU sekali jalan, dan siapa saja yang memakai kuncinya?

— Chokdi 🐷 · Content Studio · 2026
