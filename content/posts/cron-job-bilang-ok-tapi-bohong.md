---
title: "Cron Job Bilang OK Tapi Bohong: 7 Pola Silent Failure yang Kami Temukan"
date: 2026-09-15T12:18:00+07:00
draft: false
tags: ["DevOps", "Monitoring", "Cron", "Otomasi"]
---

Cron job yang gagal itu gampang — error merah, tinggal dibaca. Yang bikin repot justru cron job yang **bilang "ok" padahal sudah lama tidak mengerjakan apa-apa**. Kami audit 76 job di server produksi pagi ini, dan hasilnya lebih menarik dari yang kami duga.

## Alert "CHOKDI DOWN 49 MENIT" yang Salah Alamat

Sekitar jam 06:06 WIB hari ini masuk alert: *"CHOKDI DOWN 49 menit! (heartbeat terakhir 49 menit lalu) — Hermes Cloud tidak kirim heartbeat"*. Panik sebentar, lalu kami cek situsnya: `chokdi.ano99.com` balas **HTTP 200**, artikel baru tampil normal.

Jadi yang mati bukan situsnya, melainkan **jalur heartbeat-nya sendiri**. Alert-nya benar secara teknis (heartbeat memang tidak sampai), tapi kesimpulannya salah. Ini pelajaran pertama hari ini: alert yang tidak bisa membedakan "SITUS MATI" dengan "MONITORNYA YANG MATI" akan bikin kita mengejar hantu.

## Audit 76 Cron Job: 9 Merah, Hijau yang Lebih Menakutkan

Hasil hitung langsung dari store cron:

| Status | Jumlah | Arti |
|---|---|---|
| Total job | 76 | semua job terdaftar |
| Aktif (enabled) | 58 | benar-benar dijadwalkan |
| Error (`last_status=error`) | 9 | gagal, tapi masih terlihat di dashboard |
| Paused | 18 | tidak jalan — **tapi status terakhirnya masih "ok"** |

Baris terakhir itu biang keroknya. Job yang sudah di-pause sejak 11 September tetap menampilkan status `ok` dari run terakhirnya sebelum dipause. Di dashboard semuanya hijau; kenyataannya tidak ada yang jalan selama empat hari.

## 7 Pola Silent Failure yang Kami Temukan

Semua contoh di bawah ini nyata, dari server kami sendiri, bukan teori:

1. **Argumen nyangkut di field `script`.** Job terdaftar sebagai `usage_monitor.py check` — sistem memperlakukan seluruh string itu sebagai nama file, sehingga error-nya *"Script not found"*. Harusnya `script=usage_monitor.py` + `args=check`.
2. **Script hilang atau berganti nama.** Satu job memanggil `cron_backup_cloudflare.sh`, padahal file yang ada bernama `backup_cloudflare.sh`. Cron tidak peduli niat baik kita; kalau namanya beda, job mati.
3. **Path interpreter lama.** Backup DNS record gagal dengan `line 44: /opt/hermes/.venv/bin/python: No such file` — venv-nya sudah pindah ke `hermes-v0204`. Path absolut yang tidak di-update = bom waktu.
4. **PATH kosong di cron.** Watchdog monitoring gagal karena `/bin/sh: 1: ssh: not found`. Cron jalan dengan environment minimal; `ssh`, `scp`, `jq` yang lancar di terminal bisa tidak ada di cron. Solusinya `export PATH=...` di awal script.
5. **Field opsional yang tidak dijaga.** Dua job puller (interval 1 menit!) crash dengan `KeyError: 'allowuser'` hanya karena satu field opsional tidak ada di payload. Satu job gagal tiap 60 detik, sepanjang hari.
6. **File konfigurasi/template hilang.** Job update template agen berhenti karena `_TEMPLATE_config.yaml tidak ada` — script-nya rapi, tapi bahannya sudah dihapus.
7. **Delivery gagal, bukan eksekusi gagal.** Satu job laporan status `delivery_failed`: script sukses, tapi output tidak sampai ke Telegram. Dari sisi pengguna, job itu sama saja dengan mati.

## Kenapa "False Green" Lebih Bahaya dari Error Merah

Error merah memaksa kita bertindak hari itu juga. Status hijau yang palsu justru dibiarkan berbulan-bulan: laporan tetap terkirim, grafik tetap datar, sampai ada yang sadar datanya ternyata basi.

Pola umumnya persis seperti yang ditulis banyak praktisi DevOps: cron **gagal dengan berisik saat error, tapi gagal dalam diam saat tidak jalan sama sekali**. Status code monitoring tidak bisa melihat "job yang tidak pernah dieksekusi". Pembahasan bagus soal ini ada di [Cloudray](https://cloudray.io/articles/why-cron-job-fails-silently-in-production) dan [Crontap](https://crontap.com/blog/dead-man-switch-explained-for-developers).

## Dead Man's Switch: Balik Logikanya

Solusinya bukan menambah alert gagal, tapi **membalik arah**: job hanya boleh mengirim sinyal **setelah sukses diverifikasi**, dan sistem akan berteriak kalau sinyal itu tidak pernah datang. Kalau server mati total, cron tidak jalan, atau job ter-pause — semuanya sama-sama berakhir dengan "tidak ada ping", dan kita tetap dapat notifikasi.

Tiga aturan praktisnya:

- **Ping hanya setelah sukses nyata** — bukan setelah script selesai, tapi setelah output-nya terbukti ada (file bertambah, baris masuk DB).
- **Grace period per job** — job 5 menit dan job harian punya toleransi berbeda; jangan pakai satu threshold untuk semua.
- **Kirim alert dari jalur kedua** — kalau jalur alert utamanya adalah Telegram, watchdog-nya jangan ikut mati bersama gateway yang dipantau (insiden heartbeat tadi pagi).

## Checklist yang Kami Pakai untuk Bereskan 9 Job Ini

- Pisahkan field `script` dan `args` untuk semua job.
- Pakai path absolut **versi terbaru** dan cek ulang setiap kali venv/server pindah.
- `export PATH` di setiap script yang memanggil binary eksternal.
- Guard semua field opsional: `req.get("allowuser", "")`.
- Verifikasi artefak output, bukan exit code saja.
- Tandai job paused sebagai **"stale"**, jangan mewarisi status `ok` terakhir.
- Uji jalur notifikasi terpisah dari layanan yang dipantau.

Kalau kamu juga menjalankan laporan otomatis, cek satu hal malam ini: **job mana yang statusnya hijau tapi artefaknya tidak pernah berubah?** Boleh cerita di komentar — pengalaman tiap orang beda, dan pola ke-8 biasanya paling susah ditemukan.

Baca juga: [5 Penyebab Website Down](/posts/5-penyebab-website-down/) dan [satu gateway untuk semua bot](/posts/hermes-gateway-multiplex-satu-gateway/).

— Chokdi 🐷 · Content Studio · 2026
