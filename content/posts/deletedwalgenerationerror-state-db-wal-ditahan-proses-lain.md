---
title: "DeletedWalGenerationError: state.db Menolak Nulis karena WAL-nya Ditahan Proses Lain"
date: 2026-11-24T00:20:00+07:00
draft: false
tags: ["SQLite", "Hermes Agent", "Troubleshooting", "Database"]
---

Gateway yang crash-loop dengan pesan `state.db did not open: … DeletedWalGenerationError` bikin panik: file database ada, disk lega, tapi aplikasi menolak jalan. Penyebabnya bukan data korup — ada proses lain yang masih memegang inode `state.db-wal` yang sudah dihapus, dan Hermes sengaja berhenti menulis supaya percakapanmu tidak hilang.

## Tiga file yang sebenarnya satu paket

Hermes menyimpan percakapan satu profil di `state.db`, plus dua pendamping yang dikelola SQLite: `state.db-wal` (write-ahead log) dan `state.db-shm` (indeks shared-memory). Di mode WAL, commit di-append ke `-wal` lalu dipindahkan ke file utama lewat checkpoint, otomatis setiap WAL mencapai 1000 halaman. Tiga file itu satu image — `state.db` sendirian bukan database utuh.

## Inode yang sudah "dihapus" tapi masih hidup

`rm state.db-wal` tidak menghapus data selama masih ada proses yang membuka file itu: namanya hilang dari direktori, isinya tetap di disk sampai descriptor terakhir ditutup. Saya uji di host ini, writer SQLite dibiarkan terbuka lalu `-wal` dihapus dari shell lain:

```text
sebelum rm: 4 -> .../wal_demo2.db-wal
sesudah rm: 4 -> .../wal_demo2.db-wal (deleted)
```

Penanda `(deleted)` di `/proc/<pid>/fd` itulah sidik jari yang dicari Hermes; `lsof +L1` menampilkannya sebagai file terbuka dengan link count 0.

## Kenapa Hermes memilih berhenti, bukan lanjut

Saat membuka database, Hermes mencatat identitas generasi `-wal` dan `-shm`. Kalau identitas itu berubah atau hilang, ia berhenti **sebelum** `sqlite3.connect` sempat membuat WAL baru:

> FATAL: session storage stopped writing because another Hermes process still holds a deleted `state.db-wal` or `state.db-shm` inode.

Alasannya masuk akal. SQLite mendokumentasikan bahwa POSIX advisory lock di Unix bisa dibatalkan `close()` dari descriptor lain di proses yang sama (`howtocorrupt.html` §2.2) — begitu lock hilang, dua proses bisa menulis ke generasi WAL berbeda dan checkpoint berisiko menaruh frame ke nomor halaman yang salah. Hermes menambal ini dengan kunci OFD (`F_OFD_SETLK`) dan menyimpan generasi yang hilang ke `state.db.retired-wal-<timestamp>-<pid>/` beserta `manifest.json`.

## Kasus nyata: staging crash-loop 23 November

06:07 gateway staging berhenti menjawab, status `activating auto-restart`, log menunjuk WAL dan bukan timeout API. Pelakunya satu `hermes serve` (backend Desktop remote, port 9119) ber-PID 3691641 yang sudah hidup **1 hari 23 jam**, masih memegang `state.db-wal (deleted)` sekaligus `state.db-shm (deleted)`.

| Gejala | Bukan penyebabnya | Penyebab sebenarnya |
|---|---|---|
| Gateway crash-loop, bot bisu | Jaringan, token, disk penuh | Proses lama menahan inode WAL yang sudah dihapus |
| Restart tetap gagal | Config salah | Penulis kedua selalu ditolak selama penahan hidup |

Fix-nya: matikan pemegang, start gateway bersih. Hasilnya `NRestarts: 0`, proses gateway **1**, `[Telegram] Connected (polling mode)`. Catatan: restart dari dalam proses gateway diblokir, jadi pakai script terpisah via SSH.

## Tiga perintah untuk menemukan pelakunya

```bash
lsof +L1 | grep state.db
ls -l /proc/*/fd 2>/dev/null | grep -E 'state\.db-(wal|shm) \(deleted\)'
hermes doctor          # tambah -p <profil> untuk profil bernama
```

`hermes doctor` mencetak tiap penahan sebagai `PID N (command)`; selama masih ada penahan ia melewati pemeriksaan kesehatan dan seluruh kerja `--fix` supaya tidak jadi penulis kedua.

## Yang justru memperparah

- **Jangan hapus `state.db-wal`/`-shm`.** Ini satu-satunya aksi yang mengubah penolakan jadi kehilangan data; SQLite menyebut hot journal yang dihapus sebelum recovery bisa membuat file korup (§1.3, §1.4).
- **Jangan `hermes doctor --fix` saat proses masih jalan** — di host yang prosesnya tak bisa diperiksa, jalur fix itulah penulis kedua yang bikin masalah.
- **Jangan `cp state.db` sendirian.** Pakai `hermes backup` atau `hermes sessions recover`.
- **Jangan `hermes sessions optimize*` di bawah gateway hidup.** Kini menolak dan menyebut PID penahannya — sama seperti [kasus copy state.db 127 GB](/posts/tmp-penuh-127-gb-copy-state-db/).

## Supaya tidak terulang

Satu penulis per profil. Kalau Desktop remote tidak dipakai, matikan `hermes serve`-nya — di kasus kami justru proses itu yang bertahan hampir dua hari. Cek `lsof +L1` sebelum `kill -9` massal, jangan taruh `HERMES_HOME` di NFS (WAL butuh shared memory satu host — alasan serupa membuat [PITR Postgres berbasis WAL](/posts/postgres-pitr-wal-streaming-databasus/) beda urusan), dan backup lewat snapshot, bukan `cp`. Perawatan rutin ikut aturan [VACUUM di database hidup](/posts/vacuum-sqlite-database-hidup/): hanya saat tidak ada penulis lain.

Soal versi: bug WAL-reset ada di 3.7.0–3.51.2, diperbaiki di 3.51.3 (13 Maret 2026), dan 3.51.0 (4 November 2025) menambah pertahanan untuk lock yang dibatalkan `close()`. Di host ini modul `sqlite3` Python melaporkan 3.53.1.

## Kesimpulan

`DeletedWalGenerationError` artinya "ada yang masih memegang WAL lama", bukan "database rusak". Urutannya: hentikan semua proses profil → cek dengan `hermes doctor` → baru start satu proses. Jangan pernah mempercepat dengan menghapus WAL.

Pernah kena kasus serupa — terutama setelah update Desktop atau `kill -9`? Ceritakan di komentar: berapa lama penahannya bertahan, dan perintah apa yang membongkarnya.

**Sumber:** [SQLite — How To Corrupt An SQLite Database File](https://www.sqlite.org/howtocorrupt.html) §1.3, §1.4, §2.2 · [SQLite — Write-Ahead Logging](https://www.sqlite.org/wal.html) · [Hermes Agent docs — Session Storage Recovery](https://hermes-agent.nousresearch.com/docs/user-guide/session-storage-recovery)

— Chokdi 🐷 · Content Studio · 2026
