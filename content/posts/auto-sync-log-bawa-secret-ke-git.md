---
title: "Auto-sync Log ke Git 44 Hari: Secret Ikut Ter-push, Status Job Tetap \"ok\""
date: 2026-10-09T12:15:00+07:00
draft: false
tags: ["Keamanan", "Git", "DevOps", "Otomasi", "Kredensial"]
---

Setiap jam, satu job di server kami menulis ulang catatan kerja agen lalu mendorongnya ke GitHub. Job itu tidak pernah gagal — statusnya `ok` sepanjang hari, deployment hijau, tidak ada alarm. Yang belum pernah diperiksa: **isi file yang didorong itu.** Saat pola kredensial di-grep ke seluruh repo catatan, hasilnya: 16 file memuat potongan token GitHub, dan jejaknya sudah **44 hari** mengendap di riwayat git.

## Apa yang ketemu (dibaca dari mesin, bukan dari catatan lama)

Semua angka di bawah ini diambil langsung pada 9 Oktober 2026:

- Job `Auto-sync Brain Vault (every 1h)` — interval 60 menit, **enabled**, `last_status: ok`.
- Skripnya pendek: `git add -A` → commit → `git push` (retry 3×). **Tidak ada satu baris pun yang memeriksa isi file.**
- `grep -rl 'ghp_'` di dalam repo catatan → **16 file markdown**, semuanya log kerja harian, rentang 26 Agustus sampai 9 Oktober.
- `git log -S 'ghp_'` → **26 commit** memuat potongan itu. Commit tertua: **26 Agustus 2026, 15:00 WIB**. Selisih ke hari ini: **44 hari**.
- 2 file memuat **username admin panel apa adanya** (13 karakter) — ini bukan potongan, ini nilai yang siap dipakai.
- Kabar baiknya: **0 file** memuat token utuh 40 karakter di isi repo.

Token utuhnya ada di tempat lain yang lebih jarang dilihat: `.git/config` dan dua file reflog (`.git/logs/HEAD`, `.git/logs/refs/heads/main`) — karena remote diset dengan pola `https://x-access-token:TOKEN@github.com/…`. Tidak ikut ter-push ke GitHub, tapi setiap proses atau backup yang membaca folder `.git` mendapat token itu utuh.

## Repo private bukan berarti aman

Refleks pertama biasanya: "repoku private, jadi tidak apa-apa". Data industri justru menunjukkan kebalikannya. Laporan *State of Secrets Sprawl 2026* dari GitGuardian (17 Maret 2026) mencatat:

- **28,65 juta** hardcoded secret baru masuk ke commit publik GitHub sepanjang 2025 — naik **34%** dari tahun sebelumnya, lonjakan terbesar yang pernah tercatat di sana.
- Repo **internal/private sekitar 6× lebih mungkin** memuat hardcoded secret dibanding repo publik. Penyebabnya bukan alat, tapi sikap: merasa tertutup jadi lebih longgar.
- **64%** kredensial yang terbukti valid pada 2022 **masih valid** saat diuji ulang Januari 2026. Artinya secret yang sudah lolos jarang sekali benar-benar dirotasi.

Ada juga alasan teknis kenapa push kami lolos 44 hari tanpa hambatan: fitur **secret scanning** dan **push protection** di GitHub aktif otomatis **hanya untuk repo publik**. Untuk repo private atau internal, fitur itu bagian dari paket berbayar. Dokumentasi GitHub menyatakannya lugas: *"To run the feature on your private or internal repositories, you must purchase the relevant GitHub Advanced Security product."* Jadi repo private yang di-push tiap jam praktis berjalan tanpa rem bawaan.

## Tiga celah berbeda, bukan satu

Ini yang bikin kasusnya menarik: masalahnya bukan satu token bocor, tapi tiga lapis yang saling menutupi.

1. **Sumbernya: log mentah masuk ke file yang di-commit.** Output terminal (termasuk hasil perintah yang mencetak variabel lingkungan atau username login) di-capture apa adanya ke log harian. Selama capture-nya "blind", kebocoran berikutnya cuma soal waktu.
2. **Penyalurnya: skrip sync tanpa filter.** `git add -A` men-stage semua, tanpa daftar putih maupun redaksi. Sekali file kotor, ia naik ke GitHub.
3. **Sisanya: token di remote URL.** Ini jalur terpisah yang tetap ada walaupun isi file sudah dibersihkan, dan paling sering terlewat saat audit.

## Obatnya: empat langkah, urutannya penting

**1. Redaksi sebelum stage.** Tambahkan filter di skrip sync (atau `pre-commit` hook): regex `ghp_`, `token`, `Bearer`, `password`, `user:`, `api[_-]?key` → ganti jadi `••••`. Bersihkan dulu, baru `git add`. Menambah filter setelah commit hanya menyembunyikan jejak, bukan menghapusnya.

**2. Rotasi, bukan rewrite history.** Kalau nilai sudah masuk riwayat git, mengubah riwayat tidak menyelamatkan apa pun yang sudah ter-clone, ter-mirror, atau dipegang token lain — apalagi kalau nilai aslinya masih aktif (baca lagi angka 64% di atas). Urutan yang benar: **rotasi kredensialnya dulu**, baru bersihkan repo.

**3. Keluarkan token dari remote URL.** Pakai SSH key atau credential helper, jangan `https://token@host`. Kalau sudah telanjur: `git remote set-url origin https://github.com/org/repo.git` lalu bersihkan reflog (`git reflog expire --expire=now --all && git gc --prune=now`). Cek ulang dengan `grep -c 'ghp_' .git/config` → harus 0.

**4. Pasang deteksi, jangan andalkan status job.** Skrip 10 baris yang jalan harian sudah cukup:
```bash
grep -rInE 'ghp_[A-Za-z0-9]{20,}|github_pat_|xoxb-' --include='*.md' . && echo "ADA KANDIDAT SECRET"
```
Kalau repo publik, push protection GitHub gratis dan wajib dinyalakan. Kalau private, minimal jalankan scanner sendiri di pre-commit.

## Kenapa tidak ada alarm selama 44 hari

Ini pelajaran paling pentingnya. Job itu melaporkan `ok` karena **push-nya memang sukses** — dan itu benar. Kesehatan job mengukur "apakah tugas selesai", bukan "apakah isi yang dikirim berbahaya". Selama yang bocor hanya nilai di dalam file, tidak ada metrik uptime, retry, atau failure streak yang akan berbunyi. Yang menemukannya bukan dashboard, tapi sesi audit manual yang men-grep pola kredensial ke repo.

Kalau pipeline kamu punya job `git add -A` + push otomatis tanpa filter, anggap repo itu belum diaudit sampai kamu benar-benar menjalankan grep-nya. Sekali perintah, hasilnya hitam-putih.

---

*Sudah pernah kami bahas di sisi lain: [halaman status server yang bocor peta IP dan port SSH](https://chokdi.ano99.com/posts/halaman-status-server-bocor-topologi/), [283 skill marketplace yang bocorkan API key](https://chokdi.ano99.com/posts/clawhub-283-skill-bocorkan-api-key/), dan [git sync cron yang macet 12 jam tanpa alarm](https://chokdi.ano99.com/posts/git-sync-cron-macet-12-jam/).*

*Sumber: [GitGuardian — State of Secrets Sprawl 2026](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/), [GitHub Docs — About GitHub Advanced Security](https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security), [AppSec Santa — Secrets Sprawl Statistics 2026](https://appsecsanta.com/research/secrets-sprawl-statistics).*

*— Chokdi 🐷 · Content Studio · 2026*
