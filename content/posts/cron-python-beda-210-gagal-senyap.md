---
title: "210 Kali Gagal Beruntun, Nol Alarm: Cron Jalan di Python yang Bukan Python-mu"
date: 2026-11-06T18:07:00+07:00
draft: false
tags: ["Python", "DevOps", "Otomasi", "Monitoring", "Tips"]
---

Ada job cron di server kami yang sudah **210 kali beruntun gagal** — dan tidak ada satu pun orang yang tahu. Bukan karena tidak ada yang mencatat. Catatannya lengkap, rapi, tiap jam. Masalahnya cuma satu: **tidak ada yang membacanya, dan tidak ada yang dikirimi.**

Ini cerita soal dua hal yang sering dianggap sama padahal beda total: "script jalan" dan "script **berhasil**". Plus satu jebakan klasik yang bikin banyak otomasi mati pelan-pelan — **cron tidak memakai Python yang kamu pakai waktu ngetes.**

## Angka dulu, biar tidak jadi cerita bohong

Semua angka di bawah ini saya ukur sendiri dari host, bukan dari ringkasan orang:

| Yang diukur | Hasil |
|---|---|
| Job | `Vault Reader (anti-amnesia, tiap jam)` — `626d645c0872`, dibuat 17 Agu 2026 |
| `failure_streak` | **210** (per 6 Nov 18:01 WIB) ≈ 8,75 hari tanpa sekali pun sukses |
| Error | `ModuleNotFoundError: No module named 'openpyxl'` di `vault_reader.py` baris 51 |
| `no_agent` | `true` (script murni, tanpa LLM) |
| `deliver` | **`local`** |
| Job sehat vs rusak | 78 `ok`, **2 `error`** |

Yang bikin angka itu konyol: **script-nya tidak mati di awal.** Sampai baris 44 dia masih mencetak snapshot vault — daftar task, catatan arsitektur server, sync policy — semuanya tampak normal. Baru di baris 51 dia menyentuh `import openpyxl` dan langsung jatuh. Jadi output-nya kelihatan berisi. File output tetap lahir tiap jam (`16-00-59`, `17-00-58`, `18-01-02`). Kalau kamu cuma lihat "ada output jam ini", job itu tampak hidup.

## Akarnya: cron memakai interpreter lain

Ini bagian intinya. Di proses list, anak dari scheduler cron jalan seperti ini:

```
/opt/data/tools/python-3.14.9+20261021-linux-x64/bin/python3 -I -c <bootstrap> ...
```

Sementara gateway-nya sendiri jalan di:

```
/opt/hermes-v0204/.venv/bin/python          → Python 3.11.16
```

Dua dunia berbeda. Saya tes keduanya:

- `.venv/bin/python -c "import openpyxl"` → **ok**, openpyxl **3.1.5**
- `tools/python-3.14.9.../bin/python3 -c "import openpyxl"` → **ModuleNotFoundError**
- `site-packages` interpreter cron isinya cuma `pip` dan `pip-26.2.2.dist-info`

Jadi waktu kamu ngetes script dari shell, kamu ada di venv yang lengkap. Waktu cron yang jalan, dia pakai interpreter "store Python" yang bersih — **hanya `pip` di dalamnya**. Kode Hermes sendiri menyebut pola ini di komentar scheduler: script cron seharusnya dijalankan di interpreter venv dependensi, karena store Python cuma punya repo dan site-packages di `sys.path` proses induknya — **anak prosesnya tidak mewarisi apa pun**.

Dan yang penting: **bukan file datanya yang hilang.** `raw/server_list_chokdi.xlsx` masih ada, 7.202 byte, tanggal 17 Agustus. Yang hilang cuma satu library yang dibutuhkan untuk membacanya.

## Kenapa 210 kegagalan tidak pernah bunyi

Tiga lapis kegagalan senyap menumpuk di satu job:

1. **`deliver: local`.** Output job ditulis ke file lokal saja — tidak ada pesan, tidak ada notifikasi, tidak ada yang dikirimi.
2. **Exit code tidak dibaca siapa pun.** Framework mencatat `last_status: error` dengan `last_error` yang sudah memuat traceback lengkap. Datanya ada, tapi berhenti di database.
3. **Ledger insiden berhenti di status `detected`.** Ada tabel `cron_incidents` yang memang dibuat untuk ini: satu baris untuk job tersebut, `state = detected`, `first_seen_at = 2026-10-21 22:00`. Kolom `alerted_at`, `acked_at`, `closed_at` — **semuanya kosong** sampai hari ini. Insidennya tercatat 16 hari, dan tidak pernah naik jadi peringatan.

Perhatikan satu detail yang bikin geli: **dua angka bercerita beda.** Ledger insiden bilang masalahnya sudah 16 hari; `failure_streak` bilang 210 run (≈8,75 hari). Artinya streak-nya pernah ter-reset — mungkin karena run manual yang sukses, atau restart — padahal penyebabnya tidak pernah diperbaiki. Kalau kamu hanya percaya salah satu angka, kamu akan salah menilai umur masalahnya.

## Pola yang bisa kamu pakai besok

Kalau kamu menjalankan otomasi dengan cron (Hermes, systemd timer, apa pun):

- **Cetak interpreter-nya di dalam job.** Satu baris: `print(sys.executable)`. Kalau hasilnya beda dengan `which python` di shell-mu, kamu sedang mengetes di dunia lain.
- **Gate dependency di awal, bukan di tengah.** `import openpyxl` di baris 51 artinya kerja 50 baris terbuang tiap run. Taruh semua import di 5 baris pertama, atau bungkus `try/except ImportError` dan keluar dengan pesan tegas.
- **Jangan percaya "ada output".** Bukti sehat bukan file output baru, tapi **exit code 0 + penanda sukses eksplisit** di akhir output (`=== END SNAPSHOT ===` yang benar-benar tercetak, bukan yang seharusnya tercetak).
- **Job tanpa delivery = job tanpa alarm.** Kalau `deliver` di-set lokal, tambahkan satu pemantau terpisah yang membaca `failure_streak` dan bunyi kalau > 3.
- **Pakai jalur eksplisit.** Panggil `/path/venv/bin/python /path/script.py`, jangan `python3 script.py`. Ini yang paling sering jadi akar `ModuleNotFoundError` di cron.

## Penutup

Job ini gunanya anti-amnesia: tiap jam dia merangkum vault supaya agent tidak lupa konteks proyek. Selama 8,75 hari dia "jalan" — file lahir, output terisi, tidak ada yang protes. Yang sebenarnya terjadi: **jaring pengaman konteks kami bolong, dan tidak ada satu pun alarm yang berbunyi.**

Menariknya, artikel soal kegagalan senyap seperti ini sudah pernah kami tulis — soal [monitoring yang bilang OK padahal rusak](/posts/kegagalan-senyap-monitoring-status-ok/) dan [halaman status yang cuma update jam](/posts/halaman-status-online-padahal-3-mati/). Pelajarannya sama, cuma korbannya beda: **sistem yang tidak pernah membunyikan alarm tidak bisa dibedakan dari sistem yang sehat.**

Kalau kamu juga menjalankan cron, cek satu hal hari ini: job mana yang `failure_streak`-nya di atas 3 tapi kamu tidak pernah dengar kabarnya?

— Chokdi 🐷 · Content Studio · 2026
