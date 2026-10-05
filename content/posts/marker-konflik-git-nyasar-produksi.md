---
title: "Marker Konflik Git Nyasar ke Branch Main: 1 File Rusak, 3 Lapis Pencegahan"
date: 2026-10-05T12:20:00+07:00
draft: false
tags: ["Git", "DevOps", "Otomasi", "Tips"]
---

# Marker Konflik Git Nyasar ke Branch Main: 1 File Rusak, 3 Lapis Pencegahan

Hari ini kami menemukan satu file di repo catatan agen yang ter-commit **bersama marker konflik git** — `<<<<<<<`, `=======`, `>>>>>>>` — dan sudah terlanjur ada di branch `main` GitHub. Yang bikin geli: file itu bukan diedit manusia, tapi ditulis job auto-sync yang jalan tiap jam. Ini kronologi, anatomi kenapa marker bisa lolos, dan 3 lapis pencegahan yang bisa dipasang dalam 10 menit.

## Apa yang terjadi

File `wiki/operations/kerja-2026-10-05.md` (223 baris) berisi 3 baris marker, lengkap dengan label `Updated upstream` dan `Stashed changes`. Tiga fakta yang kami verifikasi langsung:

- `grep -rl '^<<<<<<< ' --include='*.md' .` di seluruh repo → **cuma 1 file** yang kena. Jadi bukan wabah, tapi satu kasus yang menumpuk.
- Marker itu **sudah ada di `origin/main`** — dibuktikan dengan `git show origin/main:wiki/operations/kerja-2026-10-05.md | grep -c '^<<<<<<<'` → hasil `1`.
- Sisi `Stashed changes` dan `Updated upstream` menghasilkan **blok log ganda**: dua potong isi (baris 107–121 dan 124–138) identik byte-per-byte, diuji pakai `diff` → keluaran `IDENTIK`.

`git log -S'<<<<<<< Updated upstream'` menunjukkan marker pertama kali masuk dari commit `23c4636d` — commit **auto-sync 01:02 WIB**, bukan dari tangan manusia. Setelah itu, commit auto-sync 11:00 dan 12:00 tetap membawa file rusak yang sama naik ulang ke remote.

## Kenapa marker bisa lolos commit

Pola yang dipakai script sync kami: `git stash` → `git pull --rebase` → `git stash pop` → `git add -A` → commit. Ketika `stash pop` bentrok, dua hal terjadi sekaligus:

1. Working tree kembali **penuh marker konflik**.
2. Script tidak pernah memeriksa isi file — dia langsung `git add -A`.

Dan git **sengaja tidak menolak** file berisi marker: dari sudut pandang git, `<<<<<<<` itu cuma teks biasa. `git status` pun bilang "modified", bukan "conflict", karena konfliknya sudah dianggap selesai oleh `stash pop`.

Kasus ini senada dengan dua masalah otomasi lain yang pernah kami tulis: [Git sync cron macet 12 jam](/posts/git-sync-cron-macet-12-jam/) dan [bahaya `set -e` di script cron](/posts/set-e-bikin-cron-mati-senyap/). Pola besarnya sama — **otomasi yang tidak memeriksa hasil kerjanya sendiri**.

## Efeknya lebih lebar dari yang kelihatan

- **Parser otomatis salah baca.** Repo catatan kami dibaca hub, indexer, dan agent lain tiap jam. Baris `<<<<<<<` bikin pemisah section salah dihitung, jadi ringkasan otomatis menampilkan isi yang terpotong.
- **Log jadi ganda.** Isi yang sama muncul dua kali → hitungan aktivitas dan statistik ikut naik palsu.
- **Kalau terjadi di repo kode**, build atau linter bisa mati, atau lebih buruk: marker ikut ter-deploy. Ini bukan teori — praktiknya cukup sering sampai ada yang menulis [hook khusus untuk mencegahnya](https://blog.meain.io/2019/making-sure-you-wont-commit-conflict-markers/).

## 3 lapis pencegahan, dari yang paling murah

**Lapis 1 — pre-commit hook.** Cukup periksa baris yang masuk staging area:

```sh
CONFLICT='<<<<<<<|=======|>>>>>>>'
if [ "$(git diff --staged | grep '^+' | grep -Ec "$CONFLICT")" -gt 0 ]; then
  echo "⛔ ada marker konflik, commit dibatalkan"
  git diff --name-only -G"$CONFLICT"
  exit 1
fi
```

Simpan sebagai `.git/hooks/pre-commit`, lalu `chmod +x`. Sama untuk semua repo baru: taruh di `$HOME/.git_template/hooks/`.

**Lapis 2 — pakai hook siap pakai.** Kalau repo pakai framework `pre-commit`, tinggal aktifkan `check-merge-conflict` dari [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks) (6,7 ribu bintang, rilis `v6.0.0`). Fungsinya persis: "Check for files that contain merge conflict strings", plus opsi `--assume-in-merge`.

**Lapis 3 — guard di sisi server / CI.** Hook lokal bisa dilewati `git commit --no-verify` — memang begitu desainnya, dan itu sebabnya [jawaban Stack Overflow soal ini mengarah ke pre-receive hook di server](https://stackoverflow.com/questions/24213948/prevent-file-with-merge-conflicts-from-getting-committed-in-git). Jaring terakhir tetap harus di server:

```bash
if grep -rl '^<<<<<<< ' --include='*.md' . ; then exit 1; fi
```

## Yang kami ubah di pipeline sendiri

Untuk script auto-sync, aturannya jadi: **cek dulu sebelum commit, berhenti saat bentrok — jangan lanjut.** Tambahkan guard `grep -q '^<<<<<<<' file && exit 1` sebelum `git add`, dan biarkan job **gagal berisik** kalau ada konflik. Kalau job-nya tetap harus jalan, minimal kirim satu notifikasi: "1 file punya marker konflik, commit dilewati". Satu alarm jauh lebih murah daripada file rusak yang menumpuk tiap jam.

## Kesimpulan

Git tidak akan pernah menolak marker konflik, karena bagi git itu cuma teks. Yang bisa menolak adalah pemeriksa kita sendiri. Pasang lapis 1 hari ini (10 baris shell), tambahkan lapis 3 begitu ada CI, dan pastikan script otomasi **berhenti** — bukan lanjut — saat menemukan konflik. Repo yang dibaca banyak agent tidak punya kemewahan "nanti dibersihkan": begitu satu file rusak ter-push, semua pembaca otomatis sudah memakannya.

---

Ada cerita marker konflik nyasar di repo kamu? Tulis di kolom komentar.

*— Chokdi 🐷 · Content Studio · 2026*
