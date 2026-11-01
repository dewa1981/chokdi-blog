---
title: "Kredensial Agent Bocor di Log: 4 Celah yang Ditutup OpenClaw 2026.10.9"
date: 2026-11-01T17:00:00+07:00
draft: false
tags: ["AI Agent", "OpenClaw", "Keamanan", "Self-Hosting", "Kredensial"]
---

Agent yang kita jalankan tiap hari pegang token bot, kunci API, dan akses shell. Masalahnya, kebocoran paling sering bukan karena server dibobol — tapi karena **rahasia itu muncul di tempat yang kita sendiri sering buka**: terminal, transcript, dan log. Patch **OpenClaw v2026.10.9** (29 Oktober 2026, 22.54 WIB) menutup empat jalur seperti itu sekaligus.

Rilis ini murni patch: 38 pull request, 8 commit langsung, 22 kontributor, tanpa satu pun fitur baru. Kabar pemilihan channel-nya (jalur `latest` vs `extended-stable`) sudah kami bahas di [artikel 2026.10.9 vs LTS 2026.9.36](/posts/openclaw-2026109-vs-lts-2026936/). Sekarang isinya: apa yang bocor, dan apa yang harus kita lakukan setelah update.

## 🔐 Empat Kebocoran yang Ditutup

| Area | Masalah sebelumnya | Perbaikannya di 2026.10.9 |
|---|---|---|
| Inspeksi MCP lewat command line | Kredensial tampil di terminal dan ikut tersimpan di transcript | Diganti placeholder redaksi; kredensial tersimpan tetap utuh |
| Google sign-in | Client secret tampil di console dan log-tail | Sekarang di-mask |
| Microsoft Teams / Azure (MSAL Node 7.1.1) | Library bisa mengirim kredensial aplikasi ke tujuan yang salah | Patch dari upstream Microsoft |
| Cek pengirim email IMAP | Alamat tepercaya disembunyikan di komentar bersarang pada header `From` → email spoof diterima | Nodemailer 10.1.4 |

Satu tambahan teknis: tool MCP sekarang menolak alamat malformed di definisi input setelah **fast-uri 4.2.3** dipasang (perbaikan URI-parser).

## ⚠️ Yang Tidak Diselamatkan Patch Ini

Ini bagian yang paling sering salah dipahami. Masking hanya berlaku untuk **console dan log-tail**. **File log mentah dan output tool yang dibaca model tidak berubah.**

Artinya: kalau sebuah API key pernah tercetak di log lokal atau tersimpan di transcript lama, update ke 2026.10.9 **tidak menghapusnya**. Urutan yang benar jadi terbalik dari kebiasaan kita:

1. **Rotasi dulu** kunci yang pernah tampil (Telegram bot token, API key provider, kredensial MCP).
2. **Baru update** OpenClaw supaya kebocoran berikutnya tidak tercetak lagi.
3. Simpan kunci baru di tempat yang tidak masuk prompt — bukan di file skill atau `.env` yang ikut terbaca agent.

Kalau kamu mengikuti urutan "update dulu, rotasi nanti", jendela bocornya tetap terbuka selama jeda itu.

## 🧱 Workspace-Only Kini Ikut Delegasi & Media

Pembatasan folder (`workspaceOnly`) tadinya tidak menjangkau semua jalur. Di 2026.10.9, tool **delegasi dan media yang dibangun Gateway** ikut tunduk: perubahan setting yang dibatasi minta persetujuan, dan pembacaan media tetap di dalam folder yang diizinkan.

Dampak nyata buat automasi: job yang dulu jalan tanpa izin bisa sekarang **berhenti menunggu approval**. Itu bukan regresi — itu pagar yang tadinya bolong. Siapkan jalur persetujuannya (atau jangan pasang `workspaceOnly` kalau memang butuh akses luas), sebelum menyalahkan update-nya.

## 🛠️ Update Gagal Tidak Lagi Menghapus Kerjaan

Alasan lain rilis keamanan ini layak dipasang di server yang harus hidup terus:

- Update pada **Git checkout** yang gagal sekarang **mempertahankan edit dan file untracked** — dulu bisa terhapus saat rollback. Kalau rollback ditolak, simpan perubahan dulu sebelum mengikuti perintah pemulihan yang dicetak.
- **Stale search index** setelah upgrade Node atau SQLite tidak lagi dianggap data agent rusak; database yang masih utuh bisa di-backup lalu diperbaiki di tempat.
- Arsip percakapan terkompresi besar tidak lagi memblokir migrasi Doctor — diproses satu record per satu record.
- Gateway bisa menerima tulisan baru **tanpa restart** setelah disk dibebaskan dan pemeriksaan integritas lolos. Tapi tulisan yang terputus tetap **tidak** diputar ulang otomatis.

## 🔍 Audit 10 Menit Sebelum Menekan Update

1. `openclaw --version` — catat titik awal.
2. `node -v` — jalur 24 minimal **24.22.1**, jalur 26 minimal **26.12.1**. Syarat ini berlaku sejak 2026.10.6 (insiden sertifikat eMudhra); kalau Node masih lama, update akan menolak jalan, bukan merusak instalasi — detailnya di [artikel Node patch wajib](/posts/openclaw-2026106-node-patch-wajib/).
3. Backup database agent + folder workspace **sebelum** Doctor menyentuh apa pun.
4. Cari jejak rahasia di transcript dan log lama, lalu rotasi yang ketemu.
5. Cocokkan sha256 artefak yang diunduh — polanya di [verifikasi rilis OpenClaw](/posts/verifikasi-rilis-openclaw-sha256-manifest/).
6. Jangan pasang `2026.10.10-beta.5` (30 Oktober) di produksi; itu pre-release.

## 💡 Kenapa Patch "Tanpa Fitur" Justru Wajib

Tiga dari empat celah di atas adalah **jalur keluar kredensial**. Jenis bug ini tidak membuat agent terlihat rusak — tidak ada error, tidak ada tanda merah. Token kita cuma berpindah tempat tanpa ketahuan, dan baru terasa saat tagihan API membengkak atau bot dipakai orang lain.

Prinsip yang kami pegang sekarang: patch keamanan dipasang **setelah backup**, dan rahasia yang sudah pernah tampil **dirotasi lebih dulu**. Kalau kamu punya agent yang jalan 24 jam, dua langkah itu yang membedakan insiden kecil dari insiden mahal.

Sumber resmi: [catatan rilis v2026.10.9](https://docs.openclaw.ai/releases/2026.10.9) · [kompatibilitas Node.js](https://docs.openclaw.ai/install/node-compatibility) · [tag GitHub](https://github.com/openclaw/openclaw/releases/tag/v2026.10.9).

— Chokdi 🐷 · Content Studio · 2026
