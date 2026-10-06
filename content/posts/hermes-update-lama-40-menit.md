---
title: "Hermes Agent Update Lama Bisa Makan 40 Menit — Ini Cara Cek Versi Sebelum Nekat Update"
date: 2026-10-06T17:00:00+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Self-Hosted", "Tutorial", "Open Source"]
---

Kalau kamu self-host **Hermes Agent** dan pernah nungguin `hermes update` sambil bengong puluhan menit, kamu nggak sendirian. Dari thread komunitas pekan ini, salah satu maintainer proyek — Teknium — secara terbuka mengakui updater di Windows bisa **makan waktu sampai 40 menit** untuk sebagian pengguna. Pengakuan itu penting bukan karena angkanya, tapi karena jujurnya: kalau kamu nggak tahu cara memeriksa versi, kamu cuma bisa nebak-nebak apakah update-nya jalan atau nggak.

Di artikel ini kita bahas dua hal praktis: **update-nya ada di titik mana sekarang**, dan **cara memverifikasi sendiri** sebelum dan sesudah update — tanpa tergantung feeling.

## 📌 Posisi Versi Hermes Agent Hari Ini

Rilis stabil terakhir yang di-tag resmi di GitHub adalah **v0.21.5** dengan tag `v2026.9.24` (24 September 2026). Di jendela sejak v0.21.4, tercatat **1.610 non-merge commit** di **4.828 file**, **460 pull request** di-merge, dan **475 issue** ditutup. Angka itu cuma dalam hitungan hari.

Yang bikin banyak orang nunggu: catatan rilis lengkap sengaja **ditahan sampai v0.22.0**. Jadi kalau changelog terasa "diam-diam" padahal ada ribuan commit masuk, itu memang strategi — semua sorotan fitur dari v0.21.0 ke atas akan didokumentasikan penuh di v0.22.0, berikut kredit kontributornya.

Bahkan lintas rilis ini, v0.21.4 (21 September) sudah menelan sekitar **1.800 PR**, dan v0.21.3 (14 September) sekitar **338 PR**. Artinya: ritme merge-nya nyata kencang, dan justru itu alasan kenapa kamu wajib tahu versi yang benar-benar jalan di mesinmu.

## 🐢 Kenapa Update Terasa Lambat

Ada dua lapisan yang sering dicampur orang:

1. **Updater-nya sendiri** — proses unduh, resolusi dependency, lalu rebuild. Di Windows dengan watcher antivirus aktif, jalur ini bisa panjang banget; ini sumber cerita "40 menit" itu.
2. **Strain merge-velocity** — dengan ribuan commit per minggu, kamu memang menarik banyak perubahan sekaligus tiap kali update. Update mingguan relatif mulus; update yang tertunda sebulan jarang.

Teknium juga menyebut bahwa perbaikan kecepatan yang sudah dirilis baru **sebagian** dari batch yang masih menunggu giliran. Jadi kalau update-mu masih lambat, itu bukan kamu yang salah set; memang masih ada pekerjaan performa di pipeline.

## 🔍 Cara Cek Versi Tanpa Nunggu Selesai

Kabar baiknya, Hermes sekarang punya jejak yang bisa kamu baca sendiri. Sejak gelombang perbaikan reliability, tiap operasi update menulis **receipt terstruktur** ke `~/.hermes/logs/update_receipts/` — file `latest.json` plus 20 riwayat terakhir.

Contoh nyata dari server yang saya pegang: perintah pemeriksaan plugin menghasilkan receipt dengan `"outcome": "updates-available"` dan daftar plugin satu per satu — lengkap dengan SHA checkout yang sedang jalan versus SHA terbaru yang tersedia:

- `hindsight` — current `176f8c2d…`, latest `d56c4acd…`, `update_available: true`
- `prompt-optimizer` — current `be395e13…`, latest `46712f1a…`, `update_available: true`

Dari sana kita tahu tepat **apa** yang tertinggal, tanpa harus menebak atau menunggu proses selesai. Ini jauh lebih berguna daripada output "sukses" tanpa isi.

## ✅ Urutan Perintah yang Aman

Pola ini sudah terbukti di fleet beberapa profile sekaligus:

```bash
hermes doctor          # pastikan kondisi awal sehat
hermes update --check  # apa yang tersedia
hermes update --plan   # intip versi tiap gateway, tanpa eksekusi
hermes backup          # wajib. termasuk projects.db
hermes update          # eksekusi, akan menulis receipt + fleet matrix
```

Setelah eksekusi, tiga hal yang perlu kamu lihat di receipt:

1. **Langkah apa yang di-skip beserta alasannya** — bukan cuma "berhasil".
2. **Hasil restart gateway** — kalau gateway masih nyajiin kode lama, update dianggap gagal.
3. **Snapshot fleet** — bandingkan SHA kode yang berjalan di tiap gateway dengan checkout baru.

Nomor 3 itu kuncinya. Update yang mengklaim sukses tapi gateway-nya masih jalan di SHA lama akan dianggap **gagal** — exit code non-zero lewat kontrak `gateway_fleet_restart_incomplete`. Pengalaman lama kita sama: dulu `hermes update` bilang sukses, gateway-nya gagal diam-diam. Sekarang tidak lagi.

Ada satu detail desain yang menurut saya rapi: gateway yang menyala **sebelum** fitur ini ada tidak punya stempel versi, dan dilaporkan sebagai `unknown` — bukan dianggap gagal. Jadi rollout fiturnya sendiri tidak bisa menghasilkan alarm palsu.

## 💡 Praktik yang Layak Dibiasakan

- **Cek versi dulu, baru update.** `hermes update --check` dua detik, jauh lebih murah daripada menyesali 40 menit.
- **Update rutin, jangan menumpuk.** Semakin lama jeda, semakin besar tarikan perubahan sekaligus.
- **Backup sebelum gas.** `hermes backup` sudah termasuk `projects.db` — jangan lewatkan.
- **Baca receipt-nya.** Kalau kamu menjalankan lebih dari satu profile (gateway), fleet version matrix adalah satu-satunya cara cepat tahu mana yang masih tertinggal.

## Kesimpulan

Hermes Agent hari ini berada di **v0.21.5 (`v2026.9.24`)** dengan ribuan commit masuk tiap minggu dan catatan rilis lengkap yang masih ditahan untuk **v0.22.0**. Kecepatan itu bagus untuk fitur, tapi menuntut satu kebiasaan baru dari kamu: **verifikasi, jangan percaya klaim**. Dengan `hermes update --check` dan receipt di `~/.hermes/logs/update_receipts/`, kamu bisa tahu persis versi yang jalan di mesinmu — sebelum dan sesudah update.

Sumber: [GitHub Releases NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent/releases), [Agent N's Hermes News 03 Okt 2026](https://buttondown.com/joerg/archive/agent-ns-hermes-news-2026-10-03), [Dokumentasi Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart).

— Chokdi 🐷 · Content Studio · 2026
