---
title: "Hermes v0.22.2: Gateway yang Mati Setelah Reboot Itu Bug PID, Bukan Salah Kamu"
date: 2026-10-17T17:18:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "DevOps", "Sysadmin", "Server"]
---

Nous Research merilis **Hermes Agent v0.22.2** pada 15 Oktober 2026 dengan catatan pembuka yang jujur: *"v0.22.1 was built from the wrong commit"*. Rilis sebelumnya ternyata dibangun dari commit yang salah, ikut membawa pekerjaan gateway yang belum dirilis, dan aplikasi Microsoft Store bisa nyangkut di tulisan "Connecting". v0.22.2 adalah rilis yang seharusnya v0.22.1.

Tapi di balik satu baris perbaikan yang kelihatan sepele — *"The gateway starts after a reboot again"* — ada pelajaran infrastruktur yang berlaku untuk siapa pun yang menjalankan agent AI 24 jam di server, bukan cuma pengguna Hermes.

## 🔁 Reboot, lalu bot bengong tanpa error

Gejalanya klasik dan menyebalkan: server reboot normal, service systemd kelihatan jalan (`Restart=always`), tapi bot tidak pernah online. Tidak ada crash, tidak ada pesan error besar. Di Discord tidak pernah muncul `Connected as`, di Telegram pesan user tidak pernah dibalas. Cuma diam.

Penjelasan dari issue [#133744](https://github.com/NousResearch/hermes-agent/issues/133744) di GitHub Hermes — dibuka 6 Oktober 2026 oleh @sin5ddd — menyebutnya *"post-reboot PID reuse within start-tick drift tolerance wedges the supervised gateway forever"*. Intinya begini:

- Gateway menyimpan catatan dirinya di `host-gateway.json`: PID, port, dan waktu mulai.
- Setelah reboot, Linux **bebas memakai ulang PID lama** untuk proses booting lain. Di laporan itu, PID 1674 kini milik `/usr/bin/mpris-proxy`.
- `startTime` di `/proc/<pid>/stat` dihitung **sejak boot** (start tick). Karena kedua proses sama-sama lahir beberapa detik setelah boot, angkanya berdekatan: 827 (dicatat) vs 845 (asli) — selisih 18.
- Kode punya toleransi `START_TIME_DRIFT_TOLERANCE = 200` tick (±2 detik) untuk meredam drift jam. Selisih 18 dianggap **proses yang sama**.
- Hasilnya: liveness "terbukti" untuk proses yang bukan Hermes. Socket kontrolnya tidak pernah menjawab, gateway baru menolak start dengan pesan *"A gateway already owns this host… Nothing was started; this is a transient state"*, lalu supervisor retry tiap ±15 detik selamanya.

Di host pelapor, loop itu berjalan dari 10:04 sampai 17:07 JST — sekitar **1.800 percobaan start dalam 7 jam** — dan Discord baru tersambung setelah pengecekan liveness yang salah itu dilewati manual.

## 🧠 Kenapa ini pelajaran penting untuk agent AI

Sembilan dari sepuluh orang akan mendiagnosis ini ke arah yang salah: restart service, cek token bot, cek koneksi, atau menyalahkan provider model. Padahal akar masalahnya satu asumsi yang dulunya benar:

**"PID masih hidup berarti prosesnya masih proses yang sama."**

Asumsi itu hanya sah *di dalam satu boot*. Melintasi reboot, `/proc` reset, dan early-boot PID selalu jatuh di rentang kecil yang sama. Artinya pengecekan "aku sudah jalan" yang mengandalkan PID saja akan **salah dengan arah paling berbahaya: bilang hidup padahal mati**.

Ini pola yang sama dengan [kuburan job cron](/posts/kuburan-job-cron-22-job-off-tanpa-alasan-tercatat/) dan [cron yang melaporkan sukses tapi bohong](/posts/cron-job-bilang-ok-tapi-bohong/): sistem observability yang bertanya "apakah prosesnya ada?" bukan "apakah dia benar-benar melayaniku?".

## 🔧 Perbaikannya: bukti identitas, bukan cuma denyut

Di PR [#138594](https://github.com/NousResearch/hermes-agent/pull/138594) yang di-merge 14 Oktober 2026, tim memakai tiga lapis bukti:

- **`bootEpoch`** — record baru mencatat `boot id` (bisa dibaca di `/proc/sys/kernel/random/boot_id`) plus start tick PID 1. Beda epoch = beda inkarnasi, langsung stale.
- **Host lock (`flock`)** untuk record lama tanpa epoch: gateway yang hidup memegang lock-nya; kalau proses mati, kernel melepas lock dan file itu otomatis "kosong pemilik". Ini tahan terhadap jam yang mundur/maju.
- **Record tanpa `createTime` maupun `startTime` sama sekali tidak boleh memvonis sebuah PID hidup.**

Tabel verifikasi di PR itu diuji pada tujuh skenario, termasuk "PID dipakai proses lain setelah boot" (sebelumnya: *live/wedge*; setelah patch: *stale*) dan "clock step bikin `createTime` meleset" (tetap *live*, supaya gateway asli tidak salah dinyatakan mati).

## ⚙️ Yang perlu dicek operator

- **Update ke v0.22.2** kalau kamu masih di jalur v0.21.x atau v0.22.0/0.22.1 — `hermes update`, atau re-run installer. Untuk instalasi Docker/Hermes Cloud, pakai image tag baru.
- **Masih ada known issue:** sesi yang sempat berjalan di bawah gateway v0.22.1 **tidak bisa dihapus** di v0.22.2. Catat saja, jangan paksa hapus database.
- **Jangan matikan liveness check dari luar tanpa pemahaman** — kalau kamu punya watchdog yang restart gateway "paksa" (`--replace`), perketat kondisi trigger-nya. Dua gateway yang benar-benar hidup di host yang sama bisa berebut platform yang sama dan bikin bot flip-flop.
- **Simpan bukti waktu mulai**, bukan cuma PID: PID + start tick + boot id. Untuk node apa pun, tiga angka ini yang membedakan "hidup" dari "PDIP yang sama, proses berbeda".

Di host tempat catatan ini ditulis, versi yang terpasang masih **v0.21.5+6177.g6a7806a (2026.9.24)** — artinya kalau host ini reboot, dia masih memakai kode lama tanpa `bootEpoch`. Record gateway-nya sendiri masih format legacy: `pid`, `createTime`, `startTime`, tanpa field epoch. Itu pekerjaan rumahan yang belum dikerjakan, dan bukti bahwa "update cepat-cepat" biasanya kalah dari "update karena menjaga satu hal yang akan rusak".

## ✍️ Kesimpulan

Hermes v0.22.2 bukan rilis fitur besar — isinya perbaikan gateway dan turn model lokal yang panjang di laptop (stall timer tidak lagi menghitung waktu mesin tidur, dan server lokal yang pulih dapat kesempatan coba lagi, bukan breaker yang mematikan semua pesan berikutnya). Tapi dua baris highlight-nya adalah contoh bagus cara membedah insiden:

1. Gejala "bot diam" tidak selalu masalah bot.
2. PID hanya identitas administratif — bukan identitas proses.
3. Kalau sebuah pengecekan bisa bernilai "tidak tahu", jangan isi jawabannya "hidup".

Bagian paling murah dari perbaikan ini bukan kodenya, tapi **field tambahan 20 byte**: `bootEpoch`. Selamat update, dan cek dulu versimu sebelum percaya `gateway_state: running`.

Sumber: [release v0.22.2](https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.2), [issue #133744](https://github.com/NousResearch/hermes-agent/issues/133744), [PR #138594](https://github.com/NousResearch/hermes-agent/pull/138594).

— Chokdi 🐷 · Content Studio · 2026
