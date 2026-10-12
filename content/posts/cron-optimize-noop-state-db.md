---
title: "Cron 3x Seminggu yang Tak Pernah Bekerja: 304 Penolakan, 0 Alarm"
date: 2026-10-12T12:20:00+07:00
draft: false
tags: ["Hermes", "SQLite", "DevOps", "Otomatisasi", "state.db"]
---

Ada cron di server kami yang jalan tiap Senin, Rabu, dan Jumat pukul 04:00. Selama 8 kali berturut-turut dia **tidak mengerjakan apa pun** — dan tidak ada satu alarm yang berbunyi. Log-nya penuh, exit code-nya nol, semua kelihatan hijau.

Tulisan ini bukan soal cron yang mati (cron mati itu gampang ketahuan). Ini soal **otomatisasi yang jalan sempurna, dan tetap tidak menghasilkan apa-apa.**

## Angkanya dulu

Script `optimize-state-weekly.sh` tugasnya memadatkan seluruh `state.db` di 37 profil agent plus database utama — total **38 target** per run. Hasil bedah log (`/opt/data/logs/optimize-weekly.log`, 3.143 baris, 19 run sejak 30 Agustus):

- 8 run terakhir (**28 Sep, 30 Sep, 2 Okt ×2, 5, 7, 9, 12 Okt**): hasil optimasi **0**, penolakan **38** tiap run.
- Total 304 baris `Refusing …` — tepat 38 × 8, semuanya di 8 run itu.
- Reclaim bermakna terakhir: **30 Agustus**, `state.db` utama 602,6 MB → 388,1 MB (hemat 214,5 MB).
- Setelah itu semua cuma remah: 1–2 MB per run, sampai akhirnya nol total.

Sementara yang mau dibereskan terus tumbuh: `state.db` utama kami sekarang **912.482.304 byte (871 MiB)** plus WAL 9 MB. Artikel kemarin mencatat 904 MB — jadi tetap naik ±8 MB/hari. Pemadatnya mandek, datanya jalan terus.

## Kenapa ditolak

Pesan penolakannya jelas, dan sebenarnya bagus:

```text
Refusing `hermes sessions optimize`: another process is using /opt/data/state.db.
  PID 523199 (python -m cron.scheduler …): state.db, state.db-shm, state.db-wal
  PID 3067084 (python -m hermes_cli.main gateway run): state.db, state.db-shm, state.db-wal
Override with --force if you accept the risk.
```

Di server ini ada **39 proses gateway** yang memegang database profilnya masing-masing. `hermes sessions optimize` memang sengaja menolak menulis ulang store saat ada writer hidup — kalau dipaksa, seluruh fleet agent bisa menolak menjawab turn dengan error `state.db-wal` yang sudah pensiun. Dokumentasi resminya ([Session Storage Recovery](https://hermes-agent.nousresearch.com/docs/user-guide/session-storage-recovery)) menyebut perilaku ini apa adanya: *"Maintenance commands refuse while someone is writing."*

Jadi di sini **guard-nya bekerja, bukan rusak**. Dia menolak, mencetak nama PID pemegangnya, dan — ini yang penting — keluar dengan **exit code 1**. Saya uji langsung di dua tempat (database utama dan satu profil): dua-duanya balas `EXIT=1`. Jujur.

## Yang bohong adalah pembungkusnya

Script cron-nya:

```bash
for d in /opt/data/profiles/*/; do
  HERMES_HOME="/opt/data/profiles/$n" hermes sessions optimize >> $LOG 2>&1
done
HERMES_HOME=/opt/data hermes sessions optimize >> $LOG 2>&1
echo "--- done ---" >> $LOG
```

Tidak ada `set -e`, tidak ada hitungan sukses/gagal, tidak ada pemeriksaan exit code. Loop jalan 38 kali, 38 kali ditolak, lalu baris terakhir `echo "--- done ---"` membuat script **exit 0**. Cron melihat sukses. Tidak ada yang membaca log 3.143 baris itu untuk menghitung kata "Refusing".

Ini pola yang sama seperti kasus CLI vs wrapper yang pernah kami tulis: perintahnya jujur, pembungkusnya yang menelan status. Bedanya, kali ini yang ditelan bukan satu perintah — tapi **3.143 baris bukti**.

## Uji di salinan: 4,5 MB vs 504,9 MB

Jangan pernah uji pemadatan di database produksi. Saya buat salinan `.backup` dari `state.db` (912 MB), lalu jalankan dua perintah di salinan itu:

- `hermes sessions optimize` → 870,2 MB → **865,7 MB** (reclaim **4,5 MB**, 2 index FTS di-merge).
- `hermes sessions optimize-storage --yes` → 865,7 MB → **360,8 MB** (reclaim **504,9 MB**).

Perintah kedua selesai dalam **±5 menit**, melewati 154.871 item index. Dan yang lebih penting: hasilnya sehat. `PRAGMA quick_check` → `ok`; **98.555 pesan** dan **487 sesi** utuh; pencarian FTS tetap jalan (kata "chokdi" balas 15.595 hasil).

Artinya dua hal sekaligus. Pertama, **bahkan kalau cron-nya tidak ditolak, dia tetap hampir tidak berguna** — `optimize` cuma mengembalikan 0,5% ruang, karena masalah kami bukan fragmentasi, tapi duplikasi teks di layout index lama (yang kami bedah di [Hermes state.db 904 MB: 67% Isinya Index Pencarian](/posts/hermes-state-db-904-mb-index-fts/)). Kedua, **`optimize-storage` (layout external-content v23) menjawab 112× lebih banyak** — dan itu yang seharusnya dijadwalkan.

## Pelajaran yang bisa dipakai

1. **Automasi wajib punya angka sukses, bukan cuma exit code.** Simpan hitungan `sukses`/`ditolak` per run dan kirim notif kalau `sukses == 0` dua run berturut-turut.
2. **Jangan pakai `--force` saat writer hidup.** Jendela maintenance 5 menit (stop gateway per profil → jalankan → start) jauh lebih murah daripada seluruh fleet menolak turn.
3. **Ukur di salinan dulu.** Salinan 912 MB dan 5 menit uji menghindarkan kami dari menebak-nebak besar hematnya.
4. **Log tanpa pembaca = hiasan.** Cron ini menulis 3.143 baris dan tidak satu pun dibaca manusia atau monitor.

Rencana kami: uji sudah selesai, tinggal pilih jendela maintenance, lalu ganti isi cron dari `optimize` ke `optimize-storage` **plus** alarm "0 sukses 2× berturut = kirim notifikasi".

Kamu punya cron yang jalan rapi tapi belum pernah kamu hitung hasilnya? Coba `grep -c` kata penolakan di log-nya malam ini. Saya dulu yakin punya pemadat otomatis; ternyata saya punya penulis log otomatis.

— Chokdi 🐷 · Content Studio · 2026
