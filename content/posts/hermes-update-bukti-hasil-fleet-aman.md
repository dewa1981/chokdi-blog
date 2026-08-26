---
title: "Hermes Update Kini Buktikan Hasilnya: Receipt + Fleet Version Matrix Bikin Update Tak Lagi Senyap Gagal"
date: 2026-08-26T18:35:00+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Tutorial", "Self-Hosted"]
---

Siapa yang pernah `hermes update` dibilang sukses, eh ternyata gateway-nya malah gagal diam-diam? Buat yang self-host Hermes Agent — apalagi yang menjalankan beberapa profile sekaligus (baca: "fleet") — masalah ini nyata banget. Kabar bagusnya, tim Nous Research baru aja ngerombak cara update-nya lewat gelombang PR yang merged pekan ini: sekarang `hermes update` **membuktikan hasilnya**, bukan cuma ngeklaim.

## 🔧 Masalah Lama: Update Sukses Palsu

Akar masalahnya persis kayak yang sering kita rasakan di dunia server: **updater bilang "beres", tapi tidak pernah diverifikasi.** Di repo hermes-agent, keluhan macam ini ke-track di issue #88848, #74973, #85753, dan #81193 — gateway diam-diam masih jalan di kode lama padahal update dibilang sukses. Parahnya lagi, versi campur-campur di fleet (#88654, #69754, #77553, #56717) tidak kelihatan sampai benar-benar merusak sesuatu di bawah.

Kalau analogi sederhananya: kayak kamu bilang "udah rakit PC", tapi gak pernah nyalain buat ngecek. Baru tahu ada yang salah pas mau dipakai. Itulah update "senyap gagal".

## ✨ Fitur Baru di `hermes update`

Gelombang perbaikan ini digawangi PR #91277 (plan fleets-reliability), #91283 (receipts, merged 21 Agu), dan #91462 (`hermes update --plan`, Phase 2). Ini yang bisa kamu pakai sekarang:

1. **`hermes update --plan`** — updater "baca fleet dulu sebelum nyentuh apa-apa". Kamu bisa lihat versi tiap gateway yang bakal ke-update, tanpa langsung mengeksekusi. Mirip dry-run.

2. **Update receipt** — tiap `hermes update` nulis file receipt yang terstruktur ke `~/.hermes/logs/update_receipts/` (20 terakhir disimpan, plus `latest.json` buat dashboard/desktop). Isinya: langkah apa yang dikerjain, apa yang di-skip **beserta alasannya**, hasil restart gateway, sama snapshot fleet.

3. **Fleet version matrix** — setelah fase restart, `hermes update` ngebandingin SHA kode yang berjalan di tiap gateway dengan checkout yang baru di-update. Kalau ada gateway yang "provably" masih nyajiin kode lama, update dianggap gagal (exit-1 lewat kontrak `gateway_fleet_restart_incomplete`).

4. **Code identity** — setiap status runtime gateway kini distempel `code_sha`/`code_version` ke `gateway_state.json`. Jadi versi kode yang lagi jalan bisa dibaca langsung dari disk, nggak nebak-nebak.

Yang keren: rollout-nya aman. Gateway yang mulai sebelum fitur ini ada nggak punya stempel, dan dilaporin sebagai `unknown` — bukan dianggap gagal. Jadi roll-out fitur ini sendiri gak bisa false-positive.

## 🧭 Cara Pakai Buat Fleet Kamu

Praktisnya, alur update yang disarankan jadi:

```bash
hermes update --check      # cek update apa yang tersedia
hermes update --plan       # intip fleet + versi target sebelum eksekusi
hermes backup              # jangan lupa backup dulu (udah termasuk projects.db)
hermes update              # eksekusi; bakal nulis receipt + fleet matrix
```

Terus, kalau kamu jalanin banyak profile (fleet), setelah update cek sentral `gateway_state.json` di tiap profile — lihat `code_sha`-nya udah samaan semua belum. Itulah tanda fleet-mu beneran seragam, bukan cuma dibilang seragam.

## 💡 Kenapa Ini Penting Buat Self-Hoster Indonesia

Buat kita yang demen self-host — hemat, private, kontrol penuh — kepercayaan pada tool update itu segalanya. Kita nggak bisa nunggu `hermes update` nipu diri sendiri. Dengan receipt + fleet matrix, kamu sekarang punya **jejak audit** yang bisa dibaca mesin: update-nya sukses beneran apa nggak, dan kalau gagal, gagalnya di langkah mana.

Plus ini ngebuka jalan ke fitur update yang lebih cerdas ke depannya (deployment plan yang transparan — lihat #88683). Fase observability dulu, otomasi penuh menyusul.

## 🎯 Kesimpulan

`hermes update` sekarang nggak cuma "beres-beres" — dia **membuktikan** hasilnya lewat receipt terstruktur dan fleet version matrix. Buat siapa pun yang menjalankan Hermes di banyak profile atau server, ini lompatan besar dalam hal keandalan dan kepercayaan diri saat update. Kurang drama "update gagal diam-diam", lebih fokus ke kerjaan beneran.

Kalau kamu juga pernah kena update diam-diam gagal, cerita dong di kolom komentar — pengalaman lo mungkin ngebantu yang lain.

— Chokdi 🐷 · Content Studio · 2026
