---
title: "Hermes Agent Berhenti Ikut `main` — Update Sekarang Ikut Rilis Bertag"
date: 2026-10-16T09:25:00+07:00
draft: false
tags: ["Hermes Agent", "Update", "AI Agent", "DevOps", "Nous Research"]
---

Kalau kamu pernah `hermes update` lalu tiba-tiba bot produksi kelakuan aneh, penyebabnya bukan botmu — penyebabnya kamu diam-diam ikut `main`. Selama ini `hermes update` mengambil **setiap commit terbaru** dari branch `main`, bukan rilis stabil. Sejak **Hermes Agent v0.21.7 (11 Oktober 2026)**, default itu berubah: source install sekarang **hanya ikut rilis bertag `vX.Y.Z`**. Ini kabar bagus buat siapa pun yang jalanin Hermes dengan kredensial asli.

## 📌 Apa yang sebenarnya berubah di v0.21.7

Satu baris di release notes yang penting banget: *"Updates now follow tagged releases."*

Artinya:

- `hermes update` pada source checkout resmi → pindah ke **rilis `vX.Y.Z` terbaru secara persis**, bukan commit per commit.
- Install yang **sudah lebih baru** dari rilis terakhir → **tidak digeser mundur**. Dia cuma menunggu rilis berikutnya.
- **Fork dan mirror tetap ikut `main`**, karena mereka tidak dapat rilis resmi.
- Store, MSIX, dan desktop bundled **tidak terpengaruh** — channel-nya sudah dipanggang di paket.

Menurut release notes resmi, patch ini menggulung **~204 PR** ke rilis stabil untuk desktop (macOS Apple Silicon, Windows), Microsoft Store dan MSIX, installer, Docker, dan Hermes Cloud — di window itu terukur **740 non-merge commit** di **4.156 file** (+86.775 / −26.980) plus **69 issue ditutup**.

## 🔢 Kenapa ini penting: 8.867 commit dalam 2 minggu

Komparasinya bikin merinding. Di window **v0.21.6** saja (rilis 8 Oktober 2026), rentang sejak v0.21.5 berisi:

- **8.867 non-merge commit**
- **8.342 file berubah** (+772.490 / −225.600)
- **2.106 PR** di-merge, **3.027 issue** ditutup

Jadi kalau kamu `hermes update` di periode itu, kamu bukan "update" — kamu **ganti generasi kode setiap kali kamu panggil**. Untuk agent yang cuma buat main-main, itu seru. Untuk agent yang megang token GitHub, kunci API, dan dompet kripto, itu risiko yang tidak perlu. Satu commit setengah matang yang lolos, dan kamu yang bangun jam 3 pagi.

## 🛠️ Cara pakai channel — 4 perintah

Semua ini dari dokumentasi resmi dan bersifat per-install:

- `hermes update` → **channel stabil (default baru)**: ikut rilis bertag saja.
- `hermes update --set-channel main` → kembali ke perilaku lama: ikut **setiap commit** di `main`.
- `hermes update --set-channel stable` → balik ke rilis saja. Ini sekaligus **pin ke commit rilis tertentu** (kalau checkout-mu lebih baru, ini terasa seperti rollback).
- `hermes update --channel main` → **sekali jalan** saja ikut `main`, tidak disimpan.

Pilihannya tersimpan per install di `update.installs` dalam `config.yaml`. Di **Desktop app**, ada switch **Settings ▸ About ▸ Updates** (Stable releases / Every commit), dan dialog update sekarang menampilkan channel mana yang kamu pakai.

## 🧩 Jejak yang hampir kelewat: install ber-patch lokal

Ini bagian yang paling relevan buat tim yang jalanin Hermes dengan **patch lokal** (misal patch LINE/Weixin di atas `main`, seperti yang kami pakai di server sendiri). Dokumentasi resmi menutup celah ini secara eksplisit: kalau kamu sengaja menjalankan branch kustom dengan patch di atas `main`, set:

```yaml
updates:
  parked_branch_strategy: update_in_place
```

Update-nya lalu **merge `origin/main` ke branch kamu**, bukan pindah keluar dari branch. Checkout tidak bergerak, commit kamu selamat, tapi kode yang berjalan tetap maju. Fast-forward kalau bisa; kalau divergen, hasilnya merge sungguhan di bawah safety tag `pre-update-<stamp>`, dan **berhenti bersih (tidak ada yang berubah) kalau konflik**.

Kalau kamu tidak set ini? Updater akan **un-pin install kamu** — perilaku bawaan `main` di era lama justru memaksa checkout yang dipin ke sebuah tag untuk ikut `main` lagi.

## ⚠️ Update ≠ bisa mundur seenaknya

Satu jebakan yang harus kamu tahu sebelum norak mutar balik: **rilis lama tidak bisa jalan di atas `state.db` yang sudah ditulis runtime gateway baru**. Tempat-tempat yang bisa melakukannya **menolak**, bukan merusak riwayat — lengkap dengan pesan seperti `Refused to delete a session that has gateway runtime history`.

Kalau memang harus balik: **restore state dari sebelum update**, jangan jalankan rilis lama di database hasil upgrade. Pola amannya:

1. `hermes gateway stop`
2. `/snapshot restore <id>` (atau `hermes import <backup.zip>` kalau kamu punya backup penuh)
3. Baru jalankan versi lama

Catatan penting: sesi dan pesan yang lahir **setelah** update tidak ada di snapshot itu.

## 🕒 Downtime update: drain-first, bukan dipotong

Buat yang jalanin bot 24/7, update tetap **mematikan gateway** di Linux/macOS tepat sebelum checkout berubah, lalu menyalakannya lagi setelah dependency siap. Bedanya, restart-nya sekarang **drain-first**: gateway menolak turn baru, lalu menunggu pekerjaan yang sedang jalan (chat turn, cron job, API run) selesai — dibatasi `agent.restart_after_turn_timeout` (**default 30 menit**).

Selama menunggu, updater mencetak tiap 30 detik apa yang masih ditahan, contohnya:

```
→ hermes-gateway: draining (up to 1875s)...
⏳ still draining — 1560s left before the forced restart
waiting on 1 active work unit(s):
• cron job 6ba19dab68df (nightly-scout) ... running 6m40s
```

Artinya: job cron panjang kamu **tidak dipotong di tengah jalan** — tapi juga berarti update bisa terasa "menggantung" sampai job itu kelar. Mau langsung paksa? Turunkan `agent.restart_after_turn_timeout` (nilai `0` = langsung drain paksa).

## 🐳 Satu lagi: install Docker menolak, dengan sopan

Kalau install-mu image-managed (Docker), `hermes update` **menolak secara bersih (exit code 2)**, mencetak perintah yang benar (`docker pull nousresearch/hermes-agent:latest`), dan menulis receipt `refused` supaya tooling fleet bisa melihat percobaan itu terjadi. Marker di `/etc/hermes/image-provenance.json` yang jadi penentu — bahkan kalau source checkout di-bind-mount ke dalam container, penolakannya tetap jalan. Fail-closed: marker rusak pun tetap menolak.

## 🎯 Kesimpulan

v0.21.7 bukan rilis fitur — ini **rilis kebijakan**, dan justru karena itu dampaknya besar. `hermes update` berhenti jadi roda roulette commit dan berubah jadi langkah antar-rilis yang bisa diaudit. Buat kami, ini menutup satu kelas masalah: dulu "versi Hermes kami" adalah momen-momen acak dari `main`; sekarang itu titik yang bisa disebut dengan nama.

Tiga hal yang bisa kamu lakukan hari ini:

1. **Cek channelmu** — `hermes update --check`; kalau kamu tidak sengaja berada di `main`, `hermes update --set-channel stable`.
2. **Punya patch lokal?** Set `updates.parked_branch_strategy: update_in_place` sebelum update berikutnya, biar patchmu tidak ditinggal.
3. **Backup dulu** — `updates.pre_update_backup` default `false` di banyak install. Nyalakan, karena rollback tanpa snapshot bukan rollback.

Kamu tim `stable` atau tim `main`? Kalau kamu sengaja ikut `main` demi fitur terbaru, boleh share alasanmu — kami penasaran seberapa banyak yang rela jadi canary.

— Chokdi 🐷 · Content Studio · 2026
