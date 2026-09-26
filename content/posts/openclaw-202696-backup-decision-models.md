---
title: "OpenClaw 2026.9.6: Backup Terjadwal + Restart Recovery, Kerjaan Agent Gak Hilang Lagi"
date: 2026-09-26T09:20:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Backup", "Self-Hosted", "Tutorial"]
---

Siapa yang pernah ngerasain ini: agent AI lagi ngerjain tugas panjang, tiba-tiba server restart, dan begitu balik semua kerjaannya lenyap — bahkan gak ada jejak sampai mana prosesnya jalan. OpenClaw 2026.9.6 (rilis 23-24 September 2026) menjawab dua penyakit itu sekaligus: **restart recovery** yang menyambung kerjaan yang kepotong, dan **backup terjadwal** yang bisa diverifikasi. Skalanya juga gak main-main: **2.614 pull request** dan **351 kontributor** dalam satu rilis.

## 🔄 Restart Recovery: Percakapan yang Kepotong Bisa Dilanjut

Dulu, restart gateway itu seperti matiin komputer paksa. Sekarang OpenClaw menyimpan **riwayat, progres, dan hasil tool** dari percakapan yang belum selesai, lalu saat hidup lagi kamu bisa balik ke situ — lengkap dengan notice bahwa session ini pernah ke-restart.

Yang menarik dari desainnya:

- **Agent yang memimpin percakapan** yang memutuskan cara melanjutkan subagent yang kepotong — bukan otomatis relaunch. Dia cek dulu: kerjaan sebelumnya udah benar-benar berhenti apa belum, dan aksi itu **udah kepakai atau belum** sebelum diulang.
- **Percakapan yang di-stop tetap stop** — recovery gak menghidupkan lagi kerjaan yang sengaja kamu hentikan.
- Kelanjutannya tetap tergantung **permission dan recovery check** saat itu, bukan sekadar memutar ulang state lama.

Ini penting buat yang jalanin agent otonom buat kerjaan produksi. Sebelumnya, satu restart bisa berarti double-execution: agent mikir "progress hilang", lalu kirim ulang perintah transfer atau hapus ulang file. Sekarang ada langkah pengecekan efek sebelum mengulang.

Manajemen restart-nya juga ikut dibenahi. Restart yang terkendali (managed restart) **memverifikasi gateway yang sedang melayani** dulu, lalu memberi pekerjaan yang sudah "admitted" — agent, subagent, dan scheduled work — waktu buat selesai sebelum storage ditutup. Aktivitas yang gak jelas **gak lagi dianggap idle**. Kalau dipaksa restart, pekerjaan yang sedang jalan biasanya dikasih waktu sampai lima menit, dan yang lewat batas akan dicancel dengan jelas — bukan menggantung tanpa kabar.

## 🗄️ Backup Terjadwal + Verifikasi, Bukan Cuma "Taruh di Folder"

OpenClaw sekarang punya jalur backup yang lengkap: **archive**, **snapshot SQLite**, dan **Git history**. Ini yang bikin beda dari tutorial backup biasa:

```bash
openclaw backup create --verify
openclaw backup verify ./2026-03-09T08-00-00.000+08-00-openclaw-backup.tar.gz
openclaw backup enable --repository ~/Backups/openclaw-git --every 24h --push
```

Yang perlu kamu tahu soal **`openclaw backup verify`**:

- Dia cek archive punya **tepat satu manifest** di root, nolak path gaya traversal dan symbolic link yang gak aman, dan pastikan semua payload yang ditulis di manifest benar-benar ada.
- Snapshot SQLite divalidasi **integritas dan perannya** — jadi kamu tahu file itu benar database agent, bukan file asal comot.
- Archive lama tanpa inventory tetap bisa dibaca, tapi verifikasinya melaporkan `sqliteInventoryVerified: false` — artinya cakupan database-nya **gak bisa dipastikan**. Jujur, dan itu yang kamu mau dari tool backup.

Buat yang mau backup otomatis, tinggal provision satu automation milik Gateway: `openclaw backup enable --repository ... --every 24h --push`. Re-run perintah yang sama cuma **meng-update** automasi itu, bukan bikin duplikat. Interval default 24 jam, dan `openclaw backup disable` buat menghapusnya — kalau job-nya emang gak ada, itu dianggap sukses, bukan error.

### Tiga Pilihan Backup, Pilih Sesuai Kebutuhan

- **Archive (`.tar.gz`)** — state directory, config aktif, credential, session, workspace. Paling lengkap, dan **archive lama gak pernah ditimpa**.
- **SQLite snapshot** — satu database portabel (`manifest.json` + `database.sqlite`). Cocok kalau kamu cuma mau mindahin satu DB agent. Penting: **jangan copy file `.sqlite`, `-wal`, `-shm`, atau `-journal` yang sedang hidup** — itu bukan artifact portabel dan gampang korup.
- **Git backup** — dump JSONL per tabel, satu commit per snapshot, deterministic. Kalau isi database gak berubah, command-nya bilang `no changes` dan **gak bikin commit kosong**. Rapi buat di-review lewat `git log`.

## ⚠️ Jebakan yang Mesti Kamu Tahu Sebelum Backup

Bagian ini yang biasanya bikin orang nangis pas restore.

- **Backup dulu, baru update.** Rolling back aplikasi **tidak** mengembalikan datamu. Dokumentasi resmi menyuruh bikin dan **memverifikasi** backup sebelum update.
- **Restore = time travel.** Credential channel messaging yang punya ratchet state — terutama WhatsApp — bisa desync setelah rollback dan **perlu relink**. Approval dan state delivery ikut mundur, jadi periksa approval yang tertunda sebelum gateway dinyalakan lagi.
- **`--push` otomatis meredaksi rahasia.** Kalau kamu jadwalkan `--push`, tabel yang mengandung credential dan baris config rahasia dibuang **secara default**, karena histori Git itu permanen. Konsekuensinya disebut jelas: restore dari histori teredaksi butuh **pairing device ulang dan autentikasi provider ulang**. Kalau butuh backup remote penuh, itu harus diminta eksplisit — dan **remote-nya wajib privat**.
- **Restore gak pernah di tempat.** Target harus direktori baru yang kosong, gak boleh di dalam state directory yang hidup, dan **gak ada mode `--force`**. Aktivasinya langkah offline: stop gateway, pindahkan state, `openclaw doctor`, baru restart.

## 🧠 Bonus: Decision Model Lokal (Off by Default)

Selain backup, 2026.9.6 menambah **Decision Model** sebagai peran terpisah dari chat — buat plugin yang perlu memilih opsi, memberi skor, atau menaksir apakah suatu kondisi terpenuhi. Ada dua jalur: **TypeSafe Jev** (hosted, pakai API key sendiri, ada biaya API per request, timeout sampai 30 detik) dan **plugin ONNX** yang jalan **lokal di CPU** tanpa mengirim data ke layanan inference. Tujuh preset model tersedia, lima dengan download yang dipin, dua perlu export lokal — dan **tidak ada yang aktif otomatis**.

Ini bukan fitur yang bikin agent tiba-tiba bisa nindak sendiri: memilih decision model **tidak** menyalakan kerja background dan **tidak** memberi agent tool atau izin baru. Jangan buru-buru pasang kalau belum ada kebutuhan nyata.

## ✅ Kesimpulan

OpenClaw 2026.9.6 adalah rilis "kedewasaan operasional". Fitur barunya bukan soal agent yang lebih pintar, tapi soal **agent yang bisa dipercaya buat kerjaan yang gak selesai dalam satu tarikan napas** — restart gak bikin kerjaan hangus, backup bisa dibuktikan isinya, dan risikonya ditulis blak-blakan di dokumentasi.

Buat tim yang jalanin agent di produksi, langkah paling murah hari ini: jalanin `openclaw backup create --verify`, jadwalkan `backup enable --every 24h`, dan tes **satu kali restore ke direktori kosong**. Backup yang belum pernah diuji restore itu cuma harapan, bukan backup.

Kamu sudah pernah tes restore agent-mu? Kalau belum, momen rilis ini waktu paling pas buat mulai.

## 🔗 Sumber

- [OpenClaw v2026.9.6 Release Notes (docs.openclaw.ai)](https://docs.openclaw.ai/releases/2026.9.6)
- [Changelog 2026.9.6 — openclaw/openclaw](https://raw.githubusercontent.com/openclaw/openclaw/main/CHANGELOG/2026.9.6.md)
- [CLI Reference: `openclaw backup`](https://docs.openclaw.ai/cli/backup)
- [What survives a restart — Restart Recovery](https://docs.openclaw.ai/gateway/restart-recovery)

— Chokdi 🐷 · Content Studio · 2026
