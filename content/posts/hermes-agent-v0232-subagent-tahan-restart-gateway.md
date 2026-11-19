---
title: "Hermes Agent v0.23.2: Subagent yang Mati Saat Gateway Restart Kini Bisa Dibangunkan"
date: 2026-11-19T17:21:24+07:00
draft: false
tags: ["Hermes Agent", "Nous Research", "Subagent", "Delegation", "AI Agent", "Update"]
---

Nous Research merilis **Hermes Agent v0.23.2** pada 16 November 2026, dan judul rilisnya sendiri jujur: ini bukan rilis fitur, cuma tag rollup untuk **1.989 PR** yang di-merge sejak v0.23.1. Tapi di dalam window itu ada satu perubahan yang terasa langsung buat siapa pun yang menjalankan agent 24 jam: **subagent sekarang punya catatan permanen di `state.db`**, jadi pekerjaan yang terpotong restart gateway atau crash tidak lagi lenyap jadi "outcome unknown".

## 🧨 Masalah lama: 40 menit kerja hilang karena `hermes update`

Skenario yang sering kejadian: bot Telegram melempar tugas riset ke satu subagent, anak itu bekerja 30-40 menit, lalu `hermes update` jalan atau gateway restart karena OOM. Anaknya mati, hasilnya tidak pernah kembali — yang kamu lihat cuma kegagalan tanpa jejak.

Changelog-nya menyebut versi lama bisa membuat bot diam **sampai 30 menit** lalu mematikan apa pun yang sedang jalan; sekarang update normal menunggu pekerjaan selesai.

## 🗂️ Yang berubah: satu baris `resumable_subagents` per anak

Setiap subagent kini menulis satu baris di `state.db` profilnya: waktu mulai, *heartbeat checkpoint*, alasan berhenti, dan penanda pemulihan kalau proses pemiliknya mati. Efeknya: **`continue` tetap bekerja setelah gateway restart, hard kill, atau PC crash** — bukan cuma selama proses masih ingat.

```python
delegate_task(action='continue',
              subagent_id='sa-0-1a2b3c4d',
              message='lanjutkan dari langkah 3')
```

Anak dibangun ulang di route yang sama (model, provider, profil) dan worktree yang sama; transkripnya dimuat, `message` jadi turn berikutnya. Kalau route berubah — misalnya provider diganti sejak anak itu jalan — `continue` **ditolak**. Sengaja: lebih baik gagal terang-terangan daripada anak yang sama berpikir dengan otak berbeda.

## 🧭 Lima `resume_mode`: tidak semua bisa dibangunkan

Tiap anak yang berhenti membawa `resume_mode`, dan artinya beda-beda:

| `resume_mode` | Penyebab khas | Yang dibutuhkan untuk lanjut |
| --- | --- | --- |
| `AUTO_AT` | kena limit/rate limit dengan waktu reset | tunggu `failure_resets_at` lewat |
| `AUTO_ON_BOOT` | gateway shutdown, crash, hard kill | tidak ada; cek git state & tool terakhir |
| `ON_FIX` | kredit habis, auth, model tidak ada, diblokir kebijakan | kamu perbaiki dulu penyebabnya |
| `REPAIR_THEN_CONTINUE` | transkrip tidak muat, part gambar/reasoning ditolak | transkrip harus diperbaiki dulu |
| `HANDOFF` | provider menolak percakapan ini (safety) | model lain, atau parent ambil alih |

Jadi kalau anak mati karena **kredit habis**, membangunkan ulang tanpa isi saldo cuma mengulang kegagalan yang sama.

## ⚙️ Cara menyalakan otomatis (default-nya MATI)

Tidak ada yang bangun sendiri kecuali kamu memilihnya. Di `config.yaml`:

```yaml
delegation:
  resumable_ttl_hours: 48          # berapa lama anak yang berhenti tetap bisa dilanjutkan
  max_resumable: 32                # maksimal record resumable per profil
  auto_resume: false               # opt-in: gateway membangunkan sendiri (belanja token tanpa ditunggu)
  auto_resume_deadline_minutes: 360 # menyerah 6 jam setelah stop pertama
```

Kalau `delegation.auto_resume: true`, gateway memeriksa tiap profil **setiap 15 detik** dan melanjutkan anak `AUTO_AT`/`AUTO_ON_BOOT` di percakapan dan worktree-nya sendiri. Batasnya: **2 percobaan otomatis**, lalu satu pesan kegagalan final ke parent. Selama menunggu, anak tampil di `delegate_task(action='list')` sebagai `waiting_to_resume` dengan catatan seperti *"waiting to resume at 14:05 (attempt 1 of 2); gives up at 19:40"* — tidak ada tebak-tebakan.

## ⚠️ Empat jebakan yang perlu kamu tahu sebelum menyalakannya

1. **Worktree-nya dipin.** Selama record hidup (default 48 jam, maksimal 32 per profil), worktree anak ditahan dari pembersihan otomatis. Lewat cap itu, yang paling tua kehilangan pin: tree-nya diarsipkan ke `refs/hermes/archive/` lalu dihapus. Di VPS kecil ini soal disk.
2. **Side effect tidak diputar ulang.** Anak yang dibangunkan harus memeriksa tool terakhirnya; kalau tidak ada hasil tercatat dan dia tidak bisa memastikan panggilan itu jalan, dia **wajib berhenti dengan `BLOCKED:`** alih-alih mengulang — jadi kamu tetap harus memeriksa sendiri.
3. **Ini bukan durable execution.** Untuk kerja yang harus tahan apa pun, tetap pakai `cronjob` atau `terminal(background=True)` — subagent yang bisa dilanjutkan ≠ proses yang tidak bisa mati.
4. **`auto_resume` membelanjakan token tanpa ditunggu.** Dua percobaan otomatis × anak yang bisa berjalan lama = tagihan tanpa kamu minta. Nyalakan hanya kalau kamu sudah paham membaca `waiting_to_resume`.

## 🇮🇩 Kenapa ini relevan buat yang menjalankan bot di VPS

Pola paling umum di sini: satu VPS, gateway systemd, beberapa profil bot, cron tiap jam, dan update Hermes hampir tiap minggu. Dulu jadwal update dan jadwal kerja agent selalu bertabrakan — sekarang tidak wajib. `hermes update --force` (berhenti segera) menandai anak yang sedang jalan sebagai resumable; update biasa (drain) menunggu kerja selesai dulu.

## Kesimpulan

v0.23.2 membosankan kalau dibaca dari judul — 1.989 PR, catatan kurasi lengkap menyusul di v0.24.0. Tapi isinya satu perubahan yang mengubah cara kita memperlakukan restart: **kerja agent berhenti jadi barang sekali pakai**. Saran praktis: biarkan `auto_resume` mati dulu satu-dua minggu, pakai `continue` manual, rasakan mode mana yang muncul di bot kamu — baru nyalakan setelah paham biayanya.

Pernah kena kerja subagent hilang gara-gara restart? Ceritakan di komentar.

**Baca juga:** [Hermes Agent v0.23.0 &#39;The Hearth&#39;: Desktop Pindah ke Tab Browser, 10 Tool Browser Lama Dihapus](https://chokdi.ano99.com/posts/hermes-agent-v0230-hearth-desktop-di-browser/) · [Hermes v0.22.2: Gateway yang Mati Setelah Reboot Itu Bug PID, Bukan Salah Kamu](https://chokdi.ano99.com/posts/hermes-v0222-gateway-pid-recycle/) · [Hermes Agent v0.23.1: Bug 2 MB yang Bikin `hermes plugins install` Gagal Tanpa Error](https://chokdi.ano99.com/posts/hermes-agent-v0231-plugin-catalog-2mb-gagal-senyap/)

— Chokdi 🐷 · Content Studio · 2026
