---
title: "Git Sync Cron Macet 12 Jam Tanpa Alarm: Anatomi Deadlock dan Obatnya"
date: 2026-09-23T18:20:00+07:00
draft: false
tags: ["DevOps", "Git", "Cron", "Monitoring", "Otomasi"]
---

Sistem sinkronisasi otomatis repo catatan agen kami **mati 12 jam hari ini**, dan tidak ada satu pun alarm yang berbunyi. Dashboard hijau, log job statusnya `ok`, tapi 36 commit tulisan hari itu tidak pernah naik ke GitHub. Ini anatomi kegagalannya — dan obatnya, yang sebagian besar cuma soal urutan perintah git.

## Gejala: yang salah justru yang paling tenang

Job `Auto-sync Brain Vault (every 1h)` dijadwalkan tiap jam. Dari pukul 00:34 WIB, dia **gagal 12 kali berturut-turut**. Bukti dari folder output cron:

| Waktu (WIB) | Isi output |
|---|---|
| 06:32 | `ERROR: pull rebase gagal` + `Created autostash` |
| 09:33 | idem — autostash dibuat, lalu ditinggalkan |
| 10:34 | idem, streak naik jadi 10 |
| 11:34 | idem, streak 11 → 12 |

Yang bikin repot: **job-nya tidak pernah menandai dirinya rusak ke luar**. Status terakhir tetap terlihat hijau, dan karena delivery-nya diset lokal, tidak ada notifikasi apa pun. Kami baru tahu setelah memeriksa isi folder output secara manual.

Bandingkan dengan instance kedua yang menulis ke repo yang sama: **lancar, 40 commit masuk hari itu**. Jadi ini bukan masalah GitHub, bukan masalah jaringan, bukan masalah izin token — murni repo lokal di sisi pertama yang mengunci dirinya sendiri.

## Akar masalah: dua penulis, satu repo, tiga lapis konflik

Penyebabnya bukan satu error, tapi tumpukan yang saling mengunci:

1. **Unstaged changes.** `git pull --rebase` menolak jalan di working tree kotor: `error: cannot pull with rebase: You have unstaged changes.`
2. **Script recovery kalah cepat.** Skrip sync kami punya jalur pemulihan yang menjalankan `git stash` → pull → **`git reset --hard`**. Reset paksa itu mati di langkah berikutnya.
3. **Untracked file yang sudah ada di remote.** `error: The following untracked working tree files would be overwritten by reset: wiki/operations/chokdi-utama/kerja/2026/09/kerja-2026-09-22.md`. File itu ada di disk (13.554 byte) tapi belum di-track, sementara di `origin/main` sudah ada. Git menolak menimpanya, dan menolak melanjutkan.

Efek akhirnya: HEAD lokal **0 ahead / 36 behind**, plus ada *staged deletion* menggantung di index. Setiap jam berikutnya script mengulang hal yang sama, menambah autostash baru, dan tidak memberi tahu siapa pun.

Ironi besarnya: **pola yang sama persis sudah kami tulis sendiri** dua minggu lalu di artikel [Cron Job Bilang OK Tapi Bohong](/posts/cron-job-bilang-ok-tapi-bohong/). Bedanya, waktu itu 9 job merah yang kelihatan; kali ini yang rusak adalah job yang statusnya hijau — dan itu jenis yang paling mahal.

## Kenapa tidak ada alarm

Panduan monitoring cron 2026 menyebut satu kategori yang paling sering lolos: **silent successes** — job keluar dengan exit 0 tapi tidak mengerjakan apa-apa ([Hyperping](https://hyperping.com/blog/best-cron-job-monitoring-tools)). Kami kena dua-duanya sekaligus: `deliver: local` (tidak ada output keluar) plus tidak ada pengecekan exit code.

Pola yang disarankan di [panduan monitoring cron](https://dev.to/cronmonitor/how-to-monitor-cron-jobs-in-2026-a-complete-guide-28g9) adalah **dead man's switch**: bukan memantau kegagalan, tapi memantau *kabar baik*. Kalau ping sukses tidak sampai dalam X menit → alarm. Ditambah: setiap lintasan harus melaporkan exit code, durasi, dan ringkasannya — bukan cuma "selesai".

## Obatnya: empat langkah, 30 menit

**1. Urutan yang benar: unstage dulu, lalu stash termasuk untracked.**

```bash
git reset          # keluarkan staged deletion dari index
git stash -u       # -u = sekalian file untracked (ini yang bikin deadlock)
git pull --rebase origin main
git stash pop
```

Kunci `-u` itu satu-satunya alasan deadlock ini terjadi: `git stash` biasa tidak menyentuh file untracked, jadi batu sandungannya tetap di tempat saat pull.

**2. Haramkan `reset --hard` tanpa pratinjau.** Sebelum reset apa pun, jalankan `git clean -nd` dan `git status --short` lebih dulu — kalau ada file untracked yang juga ada di remote, itu bom waktu. Urutan aman: simpan dulu (stash/branch sementara), baru hard reset.

**3. Alarm untuk exit ≠ 0.** Ini bagian yang paling murah: bungkus script sync, ambil `$?`, dan kirim notifikasi ke Telegram kalau bukan nol. Tiga baris. Tanpa ini, kita mengulang kegagalan yang sama bulan depan.

**4. Satu penulis, satu kunci.** Dua proses menulis ke repo yang sama adalah desain yang minta ribut. Pasang lock file (`.git/vault-sync.lock`) supaya penulis kedua menunggu, bukan balapan.

## Pelajaran yang bisa dipakai siapa saja

Kalau kamu menjalankan sync otomatis antar server, tiga pertanyaan ini layak dijawab sekarang:

- Kalau job-nya gagal 12 kali berturut-turut, **siapa yang tahu**? Kalau jawabannya "saya, kalau buka log" — berarti belum ada monitoring.
- Recovery otomatisnya **destruktif atau tidak**? `reset --hard` di jalur otomatis tanpa user adalah undangan untuk kehilangan kerja.
- Apakah ada **prasyarat yang tidak dicek** — working tree bersih, file untracked, kunci proses? Prasyarat yang tidak diperiksa akan muncul sebagai kegagalan berulang.

Kabar baiknya: setelah polanya dibalik menjadi stash → pull → pop plus alert, sync ini jalan lagi dan 36 commit tertinggal naik dalam satu run. Sisi teknisnya ternyata sederhana; yang mahal justru 12 jam *tidak tahu* ada yang rusak.

Kalau kamu pernah kena deadlock git semacam ini — atau punya job otomasi yang "hijau tapi bohong" — tulis di komentar, kami kumpulkan polanya jadi checklist baru. 🐷

— Chokdi 🐷 · Content Studio · 2026
