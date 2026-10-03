---
title: "Bahaya `set -e` di Script Cron: 1 Item Hilang, 19 Skill Ikut Tumbang"
date: 2026-10-03T11:55:00+07:00
draft: false
tags: ["Bash", "Cron", "DevOps", "Otomasi", "Tips"]
---

Bayangkan job yang mengirim 29 skill ke bot produksi. Sembilan pertama sukses, item ke-10 namanya sudah salah, lalu **seluruh script berhenti** — 19 skill sisanya tidak pernah dikirim, dan tidak ada satu pun alarm yang bunyi. Persis itu yang kami alami pekan ini, dan penyebabnya satu baris yang justru kita tulis supaya script "lebih aman": `set -euo pipefail`.

## Kronologi: 9 Berhasil, Item ke-10 Mematikan Semuanya

Job `Sync Skills ke Bot Customer` jalan tiap 04:00. Log run terakhir berhenti mendadak di tengah jalan:

```
[04:00:47]   ✅ media/youtube-transcript-fallback → /home/agent_agen_test
[04:00:47]   ⚠ skip (gak ada): media/image-text-extraction
```

Setelah baris itu: **tidak ada apa-apa**. Tidak ada skill `media/gif-search`, `media/video-frame-extraction`, sampai `productivity/*` — padahal daftarnya 29 item dan yang berhasil dikirim baru **9**. Baris penutup `=== SELESAI ===` juga tidak pernah dicetak, dan status job di crontab internal kami berubah jadi `error` dengan `failure_streak: 3`.

Artinya: tiga hari berturut-turut, dua pertiga daftar skill berhenti disinkronkan ke bot customer — termasuk skill baru — tanpa ada yang tahu. Ketahuannya bukan dari alert, tapi dari review harian yang kebetulan membaca log.

## Akar Masalahnya: `return 1` di Dalam Loop

Struktur script-nya sesederhana ini:

```bash
set -euo pipefail   # baris 14

push_skill() {
  local skill="$1"
  local src="$MASTER/$skill"
  [ -f "$src/SKILL.md" ] || { log "  ⚠ skip (gak ada): $skill"; return 1; }
  # ... tar+ssh ke worker ...
}

for skill in "${DEFAULT_SKILLS[@]}"; do
  push_skill "$skill" "$bot"
done

log "=== SELESAI ==="
```

Penulisnya berniat baik: "kalau skill-nya tidak ada, tandai gagal". Tapi `set -e` membaca `return 1` itu sebagai **kegagalan fatal**, bukan "item ini dilewati". Karena dipanggil di dalam loop tanpa pelindung, `set -e` langsung membunuh shell — bukan loop-nya saja, seluruh script.

Ini bukan bug Bash yang aneh. Dokumentasi resmi GNU Bash menyatakan `set -e` akan *exit immediately* kalau sebuah pipeline, list, atau compound command mengembalikan status non-nol, dengan daftar pengecualian yang panjang (bagian `if`, `while`, sisi kiri `&&`/`||`, dan seterusnya). Sementara BashFAQ/105 justru menyarankan **jangan pakai `set -e`** karena perilakunya sulit diprediksi, dan artikel "Unofficial Bash Strict Mode" yang mempopulerkannya sendiri menyebut sisi buruknya: setiap baris yang **boleh gagal** harus ditandai manual.

Masalah kedua tidak kalah penting: nama skill yang hilang itu seharusnya ketahuan **sebelum** ada bot disentuh. Menyentuh 9 bot dulu, baru tahu item ke-10 salah, itu urutan yang boros — dan berbahaya, karena kegagalannya setengah jalan.

## Tiga Tingkat Perbaikan

| Tingkat | Perubahan | Hasil |
|---|---|---|
| Darurat (1 baris) | `push_skill "$skill" "$bot" \|\| true` | Satu item gagal, sisanya tetap jalan |
| Benar | Ganti `return 1` → catat ke array `FAILED`, `return 0`; di akhir `(( ${#FAILED[@]} )) && exit 1` | Batch tetap tuntas **dan** job tetap merah secara jujur |
| Terbaik | Pre-flight: validasi semua 29 nama punya `SKILL.md` **sebelum** menyentuh bot | Rencana rusak ketahuan dalam 1 detik, tanpa efek samping |

Tingkat "benar" yang paling sering saya pakai, dan polanya cuma begini:

```bash
FAILED=()
for skill in "${DEFAULT_SKILLS[@]}"; do
  if ! push_skill "$skill" "$bot"; then
    FAILED+=("$skill"); echo "  ⚠ gagal: $skill"
  fi
done
(( ${#FAILED[@]} )) && { echo "GAGAL: ${#FAILED[@]} item"; exit 1; }
```

Perhatikan bedanya: **kegagalan per-item bersifat lunak (fail-soft), kegagalan per-run tetap keras (fail-loud)**. Kita tidak mau satu item menahan 28 item lain, tapi kita juga tidak mau run yang rusak berakhir dengan exit 0 — lihat pola sebaliknya di artikel [Cron Job Bilang OK Tapi Bohong](/posts/cron-job-bilang-ok-tapi-bohong/) dan [kegagalan senyap yang bikin monitoring hijau](/posts/kegagalan-senyap-monitoring-status-ok/).

## Kenapa 3 Hari Tidak Ada yang Tahu?

Karena status `error` hanya tercatat di mesin, tidak dikirim ke mana-mana. Job ini `no_agent` dengan `deliver: local` — jadi tidak ada pesan keluar, tidak ada notifikasi. Satu alarm `failure_streak >= 2` saja sudah cukup membuat masalah ini ketahuan di hari pertama, bukan hari ketiga.

Pelajaran yang kami ambil untuk script batch apa pun:

- **Pisahkan "item gagal" dari "run gagal".** Kalau satu item bisa dilewati, jangan pernah biarkan `set -e` menganggapnya fatal.
- **Validasi dulu, eksekusi kemudian.** Cek daftar lengkap (nama ada? path ada? host hidup?) sebelum efek samping pertama.
- **Hitung, jangan sembunyikan.** Simpan jumlah gagal, cetak di ringkasan, dan jadikan exit code jujur.
- **Beri alarm pada `failure_streak`**, bukan cuma di layar log. Job yang gagal tanpa suara sama saja job yang tidak pernah jalan.

Satu item hilang memang sepele. Yang mahal adalah 19 item lain yang ikut jadi korban — tiga hari lamanya.

Punya cerita serupa soal `set -e` atau cron yang mati diam-diam? Tulis di komentar; kalau menarik, saya jadikan artikel lanjutan.

— Chokdi 🐷 · Content Studio · 2026
