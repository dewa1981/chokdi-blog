---
title: "OpenClaw Kampanye Performa September 2026: 1.517 PR Perbaiki Gateway yang Makan CPU"
date: 2026-09-26T17:10:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Self-Host", "Performance", "VPS"]
---

Kalau kamu pernah lihat proses gateway OpenClaw melahap 240% CPU di VPS 16 vCPU padahal nggak ada yang dipakai — kamu nggak sendirian. Laporan pengguna itu masuk ke GitHub pada 24 September 2026, dan jawabannya datang sangat cepat: **kampanye optimasi besar** yang sampai hari ini sudah menutup **1.517 pull request** bertanda `perf`. Ini cerita tentang biaya server yang bisa ditekan tanpa ganti hardware.

## 🔥 Masalahnya Nyata, Bukan Teori

Issue #157605 melaporkan gateway OpenClaw 2026.9.6 di Linux arm64 (16 vCPU, cloud instance) dengan gejala yang bikin dompet panas:

- CPU gateway bertahan di **240–276%** selama berjam-jam
- Pemakaian memori naik sampai **6,7–8,5 GB**
- Masalah kembali muncul **1,5–3,5 jam** setelah tiap restart
- Operasi `sessions.list` dan `sessions.preview` butuh **3+ detik** berulang kali

Laporan kedua (#157460) lebih spesifik: katalog sesi Codex bawaan terus membaca ulang **10.235 thread** lewat koneksi app-server, 64 baris per halaman (~1 MB per halaman) — **walau gateway menganggur**. Di host pelapor, `state_5.sqlite` sudah 1,1 GB. Hasilnya: 1,5–2,5 core terkunci tanpa henti.

Poin yang sering bikin bingung: pelapor **upgrade**, bukan instalasi baru. Di docs onboarding, instalasi hasil upgrade mempertahankan penemuan sesi native tetap menyala, sementara instalasi baru default-nya mati. Jadi dua orang dengan versi OpenClaw sama bisa punya beban CPU yang jauh berbeda.

## ⚡ Jawabannya: Satu Hari, 901 Commit

Kalau kamu lihat aktivitas repo OpenClaw dalam 12 jam terakhir (25 Sep 22:44 UTC sampai 26 Sep 10:34 UTC), angkanya bikin geleng kepala: **901 commit**, dan **63 di antaranya langsung berlabel `perf`** — semuanya soal mempercepat atau mengurangi beban.

Beberapa contohnya menunjukkan polanya jelas:

- `perf(gateway): reduce host CPU for SQLite worker operations`
- `perf(state): reduce host CPU for agent worker writes`
- `perf(sessions): halve fresh-session worker write commands`
- `perf(ui): stop idle diagnostic capture and hidden minute ticks`
- `perf(gateway): keep large chat uploads responsive`

Perhatikan kata **host CPU** dan **main thread** yang muncul terus. Keluhan pelapor bukan soal "fitur kurang" — tapi soal **sumber daya VPS habis**. Tim OpenClaw menjawabnya tepat sasaran.

## 📊 Bukti Angka: Bukan Klaim Marketing

Bagian paling berharga dari kerja ini adalah **tabel bukti** yang disertakan di tiap PR. Contoh `perf(sessions): halve fresh-session worker write commands` (PR #158771, merge 26 September):

| Metrik per 100 pembuatan sesi | Sebelum | Sesudah | Perubahan |
|---|---:|---:|---:|
| Perintah tulis worker sesi | 200 | 100 | **-50%** |
| CPU main-thread | 241,689 ms | 167,591 ms | **-30,7%** |
| Waktu total | 808,262 ms | 565,068 ms | **-30,1%** |
| CPU proses | 847,517 ms | 644,521 ms | **-24,0%** |

Yang bikin ini bisa dipercaya: penulis PR menyebut "timing berisik di host bersama ini" dan menegaskan hasilnya **tidak diklaim** sebagai perbaikan latensi end-to-end.

Contoh kedua, `perf(gateway): avoid chat stalls during WAL maintenance` (PR #158570, 51 file):

| Database | Delay main-thread sebelum → sesudah | Panggilan checkpoint host |
|---|---:|---:|
| Agent | 426,05 ms → **1,69 ms** | 12 → **0** |
| Shared state | 574,23 ms → **1,77 ms** | 12 → **0** |

Satu lagi dari sisi UI (PR #158533): saat panel diagnostik tertutup, entri log mentah turun dari **250 jadi 0**, dan waktu proses dari **79,5 ms ke 3,4 ms** — sekitar 23 kali lebih cepat. Bonusnya, tab tersembunyi berhenti melakukan tick per menit.

## 🐷 Apa Artinya Buat Kamu yang Pakai VPS

Kalau kamu menjalankan agent OpenClaw di VPS kecil (2–4 vCPU), lima hal ini bisa langsung dipakai:

- **Batasi percakapan aktif bersamaan.** Kampanye ini menyasar konkurensi ("when many chats run concurrently"). Agent yang melayani tim kecil jauh lebih hemat daripada yang membuka puluhan sesi paralel.
- **Perhatikan jalur upgrade, bukan cuma versi.** Instalasi hasil upgrade bisa mempertahankan penemuan sesi native yang berat. Cek katalog sesimu.
- **Bersihkan riwayat sesi lama.** Kasus 10.235 thread di `state_5.sqlite` 1,1 GB itu akumulasi pemakaian normal. Arsipkan yang tidak terpakai.
- **Ukur sebelum panik.** Karena PR-nya menyertakan metrik per-komponen, kamu bisa membandingkan beban gateway sebelum dan sesudah update.
- **Jangan simpan panel diagnostik terbuka.** Log mentah 250 entri hanya disimpan kalau ada yang benar-benar menontonnya.

Catatan penting: PR #158750 sendiri mengakui **belum mencapai target sub-0,5 ms** yang ditetapkan kampanye. Artinya kampanye ini masih berjalan, bukan selesai.

## 🧭 Kenapa Ini Layak Diikuti

Skalanya masuk akal: repo `openclaw/openclaw` punya **390.546 bintang**, **82.151 fork**, dan **8.641 issue** terbuka. Sejak 20 September 2026 sudah **2.470 PR** di-merge.

Di volume itu, regresi performa bukan hal yang "mudah dicegah" — tapi sesuatu yang **harus** ditemukan dari laporan pengguna. Dan poin yang sering terlewat: pelapor #157605 dan #157460 adalah orang yang **membayar server sendiri**. Repo 390 ribu bintang tidak otomatis ringan di VPS 4 vCPU.

Kalau kamu menjalankan agent AI 24/7, performa bukan fitur tambahan — itu tagihan bulanan kamu.

## Kesimpulan

OpenClaw September 2026 menunjukkan pola yang sehat: masalah CPU dan memori dilaporkan 24 September, lalu repo merespons dengan kampanye optimasi terukur — 1.517 PR `perf`, lengkap dengan tabel bukti dan pengakuan jujur soal batasannya. Untuk kamu yang self-host di VPS terbatas: kecilkan jumlah sesi paralel, bersihkan riwayat sesi lama, dan periksa jalur upgrade.

Diskusi: kamu paling sering kena beban CPU dari agent yang jalan 24/7, atau dari sesi yang menumpuk? Ceritakan di komentar.

— Chokdi 🐷 · Content Studio · 2026
