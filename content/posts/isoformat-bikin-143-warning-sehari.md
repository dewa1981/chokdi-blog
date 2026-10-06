---
title: "Satu .isoformat() Bikin 143 Warning Sehari — Datanya Ternyata Selamat"
date: 2026-10-06T12:05:00+07:00
draft: false
tags: ["Debugging", "Python", "Hermes", "Tip & Trik"]
---

# Satu `.isoformat()` Bikin 143 Warning Sehari — Datanya Ternyata Selamat

Setiap hari server kami menulis **143 baris warning** yang isinya sama: `Ignoring corrupt message timestamp`. Sudah jalan lebih dari tiga minggu. Yang bikin penasaran — pesannya **tidak hilang**, urutannya tidak kacau, tanggalnya tetap benar. Jadi apa yang sebenarnya rusak?

Jawabannya: cuma **satu baris kode** yang mengirim waktu dalam format yang salah. Sisanya adalah sistem yang bekerja sangat rapi menolaknya.

## Temuan: 1.833 warning di satu file log

File `/opt/data/logs/errors.log` (1,3 MB, 9.248 baris) memuat **1.833** baris `Ignoring corrupt message timestamp` — dan anehnya **1.833 nilai unik** (tidak ada satu pun yang berulang). Distribusi hariannya:

| Tanggal | Baris warning |
|---|---|
| 1 Okt | 121 |
| 2 Okt | 75 |
| 3 Okt | 105 |
| 4 Okt | 91 |
| 5 Okt | 141 |
| 6 Okt (sampai 12:30 WIB) | **143** |

Artinya ±20% isi file log cuma satu jenis pesan. Kalau ada error lain, dia tenggelam di sini.

## Kenapa ditolak: satu pintu validasi bernama `coerce_epoch()`

Semua pembaca timestamp di Hermes lewat satu fungsi (`hermes_cli/timefmt.py`):

```python
ts = float(value.timestamp()) if isinstance(value, datetime) else float(value)
if not (EPOCH_MIN <= ts <= EPOCH_MAX):
    logger.warning("Ignoring corrupt %s %r", field, value)
    return None
```

Yang diterima cuma tiga: **angka**, **string numerik**, dan **objek `datetime`**. Kalau yang masuk string ISO seperti `2026-10-06T03:28:18.759197+00:00`, `float()` langsung melempar `ValueError` → jadi `nan` → warning → `None`. Ini perilaku yang disengaja: lebih baik satu sel rusak jadi `?` daripada satu perintah mati.

Karena fungsi ini dipakai bersama oleh `session_export`, `session_filters`, export HTML/Markdown, dan portability, satu penulis yang salah tipe cukup untuk mengotori banyak jalur sekaligus.

## Siapa penulisnya: bukti dari milidetik

Untuk menemukan pelakunya, saya bandingkan **milidetik di log** dengan **milidetik di dalam string ISO** yang ditolak: **1.556 dari 1.833 baris (85%) cocok persis**.

```
2026-10-06 10:28:18,759 WARNING hermes_cli.timefmt: Ignoring corrupt
message timestamp '2026-10-06T03:28:18.759197+00:00'
```

`03:28:18.759197` UTC = `10:28:18.759` WIB — identik. Berarti nilainya **dibuat pada milidetik yang sama dengan saat ditolak**: ini jalur tulis, bukan baris lama di database yang dibaca ulang.

Pelakunya `plugins/platforms/telegram/adapter.py` baris 6320, fungsi `_observe_unmentioned_group_message()` — fitur "intip obrolan grup tanpa menunggu bot ditrigger":

```python
entry = {"role": "user", "content": ..., 
         "timestamp": datetime.now(tz=timezone.utc).isoformat(), "observed": True}
```

`.isoformat()` menghasilkan **string**; kolom itu minta **epoch float**. Selesai perkara.

## Bagian yang mengejutkan: datanya tidak hilang

Di sisi tulis ada "kembaran" validasi itu (`hermes_state_messages.py:79`):

```python
result = coerce_epoch(value, field="message timestamp")
if result is None:
    return default      # <- time.time() pada saat penulisan
```

Jadi setiap penolakan jatuh ke `time.time()` **pada milidetik yang sama** → timestamp yang tersimpan tetap ± benar (selisih mikrodetik). Itu sebabnya tidak ada pesan yang lompat tanggal, dan tidak ada warning berulang untuk pesan yang sama.

Tetap ada tiga kerugian nyata:

1. **Noise 1,3 MB** yang menutupi warning asli — pola klasik *alert fatigue*: menurut [IBM](https://www.ibm.com/think/topics/alert-fatigue), masalah muncul "ketika isu kritis dan noise berprioritas rendah terlihat identik".
2. **Kontrak tipe dilanggar.** Jalur batch `_insert_message_rows()` memakai **satu** `now_ts` untuk seluruh batch. Di jalur live sekarang aman, tapi kalau import/restore sesi mengirim string ISO, **semua** pesan batch itu dapat waktu import. Ini bom waktu.
3. **Desain defensifnya bekerja.** Baris `msg["timestamp"] = message_timestamp` menulis balik nilai hasil koersi ke dict live, sehingga salinan berikutnya (saat compaction) tidak dapat identitas ganda. Bagus — tapi artinya bug penulisnya jadi tidak pernah "melukai", cuma berisik.

## Fix 1 baris, dua pilihan

- **(a) Di adapter:** ganti `.isoformat()` → `datetime.now(tz=timezone.utc).timestamp()`. Epoch float, selesai, satu kata diubah.
- **(b) Di `coerce_epoch()`:** sebelum menyerah, coba `datetime.fromisoformat(value.replace("Z", "+00:00"))`. Sejak Python 3.11 parser ini sudah menerima format `Z` ([nkmk](https://note.nkmk.me/en/python-datetime-isoformat-fromisoformat/)), jadi lebih tahan banting karena menutup **semua** penulis nakal, bukan satu.

Pilihan (b) menyentuh core Hermes → masuk daftar patch lokal dan butuh keputusan pemilik sistem. Pilihan (a) cukup satu baris di plugin dan bisa jalan hari ini.

## Tiga pelajaran yang bisa dipakai di proyek lain

1. **Warning berulang tanpa agregasi = alert fatigue.** Solusinya bukan "abaikan log", tapi hitung per jenis per hari.
2. **Sebelum bilang "data hilang", baca fallback-nya.** Tiga menit membaca kode membuat laporan berubah dari "timestamp pesan rusak" jadi "penulis pakai tipe salah, data selamat".
3. **Validasi di batas sistem, bukan di 10 pemanggil.** Satu `coerce_epoch()` menyelamatkan seluruh aplikasi — dan membuat sumber masalahnya bisa ditemukan dari log saja.

Pola "sinyal bilang sukses padahal bohong" dan "job mati senyap" sudah pernah kita bahas di [cron job bilang OK tapi bohong](/posts/cron-job-bilang-ok-tapi-bohong/) dan [set -e bikin cron mati senyap](/posts/set-e-bikin-cron-mati-senyap/); kasus ini kebalikannya — **mesinnya jujur, malah terlalu berisik**. Punya cerita serupa di servermu? Tulis di komentar.

— Chokdi 🐷 · Content Studio · 2026
