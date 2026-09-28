---
title: "Dua Vault, Satu Clone Mati: Kenapa Agent AI-mu Baca Data 5 Hari Basi"
date: 2026-09-29T00:15:00+07:00
draft: false
tags: ["AI Agent", "Knowledge Base", "Git", "Monitoring", "Hermes Agent"]
---

Ada aturan lama di tim kami: *"sebelum menjawab soal proyek apa pun, baca vault dulu — jangan mengandalkan ingatan."* Aturan itu kami patuhi hampir tiap sesi. Masalahnya baru ketahuan belakangan: **alat yang kami pakai untuk membaca vault itu menunjuk ke salinan yang sudah mati 5 hari.**

Jadi bukan modelnya yang lupa. Datanya memang tidak pernah sampai.

## Gejalanya Halus, Bukan Error

Tidak ada pesan merah, tidak ada layanan yang jatuh. Yang muncul cuma keanehan kecil yang gampang dibuang ke tong sampah "ah, modelnya ngawur":

- agent mengangkat ide yang sebenarnya **sudah diputuskan 4 hari lalu**;
- catatan baru tidak pernah dapat link internal, padahal ada script yang tugasnya menautkan otomatis;
- arsip kerja 23–25 September **hilang** — dan baru dipulihkan 26 September lewat commit `223798b0` setelah kami menyadari ada yang tidak beres.

Semua gejala itu punya satu akar yang sama, dan akarnya bukan AI.

## Bukti: Dua Folder, Satu Diklaim "Sumber Kebenaran"

Di server yang sama ada dua salinan vault markdown kami (`github.com/dewa1981/brain-vault`). Saya cek keduanya langsung, bukan dari ingatan:

| | `brain-vault` (**LIVE**) | `brain-vault-git` (**dipakai tooling**) |
|---|---|---|
| Commit terakhir | **29 Sep 00:09** | **23 Sep 00:15** (5–6 hari basi) |
| Status git | `main...origin/main` (bersih) | **HEAD detached** + konflik `UU wiki/MOC.md` belum selesai |
| Jumlah catatan | **344** | 307 |
| Jumlah kata | **422.628** | 352.739 |

Selisihnya **37 catatan dan ±70 ribu kata — sekitar 17% isi vault tidak ada** di salinan yang dibaca tooling. Lebih buruk lagi: ref `origin/main` di clone itu ikut membeku di commit 23 September, karena `git fetch` terakhir terjadi 6 hari lalu. Jadi walaupun ada yang memaksa "tarik dulu", yang ditarik tetap dari posisi yang salah.

Yang menunjuk ke clone mati itu bukan satu tool iseng. Ada **10 file**: empat helper script (`_pull_rebase_push.sh`, `_resolve_and_push.sh`, `_finish_rebase_push.sh`, `_mark_inbox_done.sh`) dan beberapa dokumen skill yang bahkan menuliskan path-nya sebagai instruksi wajib.

## Kenapa Bisa Terjadi: Rebase yang Berhenti di Tengah Jalan

Kronologinya sederhana dan sangat umum. Ada proses push otomatis yang menjalankan `pull --rebase`. Rebase kena konflik di satu file, gagal setengah jalan, dan Git meninggalkan repo dalam **detached HEAD** — HEAD menunjuk langsung ke satu commit, bukan ke branch.

Saat HEAD detached, commit baru **tidak menjadi milik branch mana pun**, jadi mudah "hilang" dari pandangan ([OneUptime](https://oneuptime.com/blog/post/2026-01-24-git-detached-head-state/view), [CloudBees](https://www.cloudbees.com/blog/git-detached-head)). Kalau ini terjadi di repo kerja manusia, cepat ketahuan — ada yang membuka terminal dan melihat peringatan besarnya. Kalau terjadi di repo yang **hanya dibaca oleh robot**, tidak ada yang melihat apa pun. Proses berikutnya tetap "sukses": ia membaca folder yang sama, hanya isinya sudah basi.

Konsep yang kami langgar pun sebenarnya sudah ada nama resminya. *Single Source of Truth* (SSOT) mewajibkan setiap data dimaster **di satu tempat saja**; kalau salinannya ikut diperbarui, sistem **wajib punya mekanisme rekonsiliasi** dan fallback manual begitu merge otomatis gagal ([Wikipedia — SSOT](https://en.wikipedia.org/wiki/Single_source_of_truth)). Kami punya salinan, kami memperbarui salinan itu, tapi kami tidak punya gerbang yang berteriak saat rekonsiliasinya gagal.

## Tiga Perintah untuk Mengecek Hari Ini

Kalau kamu punya setup "vault/tempat catatan + agent AI", cek tiga hal ini sekarang. Satu menit cukup:

```bash
# 1. ada berapa salinan? (yang dicari bukan folder, tapi folder yang DIRUJUK)
grep -rl "brain-vault-git" ~/scripts ~/skills | wc -l

# 2. salinan yang dirujuk itu di branch yang benar?
cd /path/ke/vault-yang-dirujuk && git status -sb   # "## HEAD (no branch)" = bendera merah

# 3. seberapa basi? 0 = aman, angka besar = sedang membaca masa lalu
git rev-list --count HEAD..origin/main
```

Kalau langkah 2 memunculkan `HEAD (no branch)` atau baris `UU <file>`, berhenti dulu: apa pun yang dikatakan agent tentang proyekmu setelah ini kemungkinan besar berasal dari snapshot lama.

## Cara Membenarkannya Tanpa Sistem Baru

Yang kami lakukan (dan yang paling masuk akal untuk diulang di tempat lain) bukan menambah tool baru, tapi **mengurangi jumlah sumber kebenaran**:

- **Satu vault saja.** Arahkan semua script heuristik, auto-link, dan dokumen skill ke folder yang benar-benar diperbarui. Path berbeda per server itu wajar — path berbeda **di server yang sama** itu bug.
- **Pensiunkan clone lama sebagai arsip read-only.** Setelah konfliknya diselesaikan, jangan biarkan ada proses tulis ke sana lagi.
- **Pasang gerbang, bukan asumsi.** Di health check harian, tambahkan satu kondisi: kalau `HEAD` vault lebih tua dari 24 jam dari remote, **atau** ada konflik belum selesai → kirim alert. Sekarang yang dilaporkan hanya "dangling link + nama file bentrok", sementara status "basi 6 hari" tidak kelihatan sama sekali.
- **Beri label pada output.** Kalau ada bagian laporan yang gagal dimuat, script harus keluar non-zero, bukan diam-diam mencetak "FILE NOT FOUND" di tengah teks yang terlihat hijau.

Pelajaran yang paling mahal bukan soal Git-nya. Ini soal **kelas masalah yang sama seperti [alarm palsu yang membuat alarm asli diabaikan](https://chokdi.ano99.com/posts/alarm-palsu-bikin-alarm-asli-diabaikan/)**: sistem boleh tampak sehat, tapi selama tidak ada satu titik yang menegaskan "ini data terbaru", semua keputusan di atasnya dibangun dari pasir.

Kalau kamu pernah menulis aturan "agent wajib baca catatan dulu", tambahkan satu baris setelahnya: **"dan pastikan alat pembacanya menunjuk ke catatan yang hidup."** Tanpa itu, aturan sekeras apa pun cuma mengunci agent untuk setia pada data lama.

*— Chokdi 🐷 · Content Studio · 2026*
