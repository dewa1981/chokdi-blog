---
title: "Hermes Agent v0.21.1: Plugin Lama Mati 14 September, Cek Sekarang"
date: 2026-09-12T00:15:00+07:00
draft: false
tags: ["Hermes Agent", "Plugin", "Update", "AI Agent"]
---

Kalau kamu menjalankan Hermes Agent dan punya plugin eksternal, ada satu tanggal yang harus kamu lingkari: **14 September 2026**. Mulai hari itu, plugin yang masih meng-import dari path lama tidak lagi sekadar memunculkan peringatan — dia **otomatis dimatikan**. Kabar baiknya: kamu masih punya dua hari, dan alat pengeceknya sudah resmi tersedia.

Ini konsekuensi dari pemecahan modul besar Hermes Agent di September 2026 — dan cara paling aman menghadapinya adalah mengecek plugin malam ini, bukan tanggal 15 September.

## Apa yang Sebenarnya Terjadi

Di PR #102117, tim Hermes memecah modul-modul besar Hermes Agent menjadi file-file kecil yang fokus. Sampai situ semua normal. Masalahnya di satu baris kebijakan yang sering bikin plugin komunitas tumbang: **internal import path bukan API yang stabil**.

Artinya, kalau plugin kamu melakukan sesuatu seperti ini:

```python
from prompt_builder import build_prompt
```

…maka setelah pemecahan modul, nama itu tidak lagi hidup di tempat yang sama (di tag terbaru, `prompt_builder.py` sudah pindah ke `agent/prompt_builder.py`).

Supaya author plugin punya waktu perbaikan, semua nama lama masih bisa di-import lewat blok `PLUGIN-COMPAT` yang ditempel sementara ke modul lama. Sifat lapisan ini dijelaskan gamblang di manifest resminya:

> "This layer is temporary and removed on 2026-09-14."

Skalanya besar. Manifest mencatat **2.125 nama** lama yang dipetakan ulang: 1.148 `moved-lazy`, 592 `import`, 290 `restored-def`, 41 `restored-helper`, 17 `restored-import`, 3 `module-stub`, dan 34 `unrestorable`. Kalau plugin kamu menyentuh salah satu nama itu, kamu termasuk yang kena.

## Timeline: Apa yang Terjadi ke Plugin Kamu

| Waktu | Yang kamu lihat di terminal/desktop | Nasib plugin |
|---|---|---|
| Sebelum 14 Sep 2026 | Banner kuning + `hermes doctor` + modal sekali di desktop | Tetap dimuat; tiap resolusi path lama memunculkan `HermesPluginCompatWarning` (sekali per nama per proses) |
| Mulai 14 Sep 2026 | Banner merah: plugin **DISABLED** | **Tidak dimuat**; `hermes plugins list` menampilkan alasannya |
| Setelah revert mendarat | Sama seperti di atas | Tidak dimuat — path lamanya sudah benar-benar hilang |

Poin pentingnya: fase "banner kuning" itu **masa tenggang, bukan status aman**. Kalau diabaikan, plugin kamu bisa hilang dari daftar tool begitu tanggal 14 tiba.

## Cara Cek Plugin Kamu (2 Menit)

Update dulu, baru periksa:

```bash
hermes update                      # ke v0.21.1 (tag v2026.9.7)
hermes plugins compat <path-ke-plugin>
hermes plugins compat <path-ke-plugin> --json   # kalau mau diolah script/CI
```

Outputnya memetakan setiap temuan: `file:line`, path lama → path baru. Selama masih ada yang belum dipindahkan, perintah ini **exit code 1** — jadi cocok dipasang di CI plugin kamu.

Satu catatan yang kami temukan sendiri: subcommand `hermes plugins compat` **baru ada di v0.21.1**. Server Chokdi kami masih jalan di v0.21.0 (tag `v2026.8.31` plus patch lokal LINE/Weixin), dan `hermes plugins compat` belum terdaftar di sana — jadi langkah pertamanya memang `hermes update`, bukan `compat`. Selama belum update, jalur manualnya: grep nama modul lama (misalnya `prompt_builder`) di folder plugin kamu.

## Kalau Plugin Kamu Terkena: Tiga Opsi

1. **Perbaiki import-nya (paling benar).** Pindahkan ke kolom *new location* yang ditunjukkan manifest. Warning hilang permanen, plugin aman selamanya.
2. **Pakai escape hatch sementara.** Tambahkan ini di `config.yaml`:

   ```yaml
   plugins:
     allow_deprecated_imports: true
   ```

   Ini membuat plugin tetap dimuat setelah tanggal 14, sampai revert benar-benar menghapus path lama. Baca: perpanjangan waktu, bukan solusi.
3. **Matikan atau ganti plugin-nya** kalau author-nya sudah tidak aktif. Lebih baik kehilangan satu plugin daripada menunggu crash saat kerja penting.

Kalau warning-nya mengganggu selama migrasi, warning-nya bisa dibungkam tanpa mematikan plugin:

```bash
python -W ignore::hermes_cli.plugin_compat.HermesPluginCompatWarning
```

Batas cakupannya: hanya **nama publik** yang di-restore. Nama privat (`_foo`, `_TG_NAME_LIMIT`, dan sejenisnya) tidak dipulihkan, dan seam monkeypatch untuk test juga tidak dipertahankan. Kalau plugin kamu menyentuh yang privat, jalan satu-satunya adalah pindah ke modul baru atau ekuivalen publiknya.

## Bonus: v0.21.1 Bukan Cuma Soal Compat

Patch ini kelihatan sepele di judul, tapi angkanya tidak masuk akal untuk sekadar "patch": **5.139 non-merge commit**, 4.364 file berubah, **632 pull request** digabung, dengan +601.014 baris ditambah dan −768.419 baris dibuang.

Enam area yang diklaim berubah: modularisasi kode, performa file-operation dan startup, pembaruan provider/model, perbaikan otorisasi MCP, perbaikan cron scheduling & delivery, dan reliabilitas delegation. Kalau kerja harianmu bergantung pada cron job atau MCP server, tiga area terakhir itu alasan paling kuat untuk segera menjalankan `hermes update` (fresh install: script resmi di repo). Kalau kamu baru mulai memakai Hermes untuk otomatisasi bot, lihat juga catatan kami di [Bot Mode dan multi-agent](/posts/hermes-agent-bot-mode-multi-agent/) serta [patch besar v0.20.6 di sini](/posts/hermes-agent-v0206-patch-besar/).

## Kesimpulan

Deadline-nya nyata, terdokumentasi, dan tinggal dua hari:

- Jalankan `hermes update` ke v0.21.1 (tag `v2026.9.7`).
- Jalankan `hermes plugins compat <path-ke-plugin>` — exit code 1 berarti masih ada yang harus diperbaiki.
- Perbaiki import ke lokasi baru, atau pasang `plugins.allow_deprecated_imports: true` sebagai penambal sementara.

Referensi resmi: [release v0.21.1](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.9.7), file [`COMPAT_MANIFEST.md`](https://github.com/NousResearch/hermes-agent/blob/v2026.9.7/COMPAT_MANIFEST.md), dan [CLI commands reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands).

Plugin mana yang paling kamu takutkan kena tanggal 14? Tulis di komentar.

— Chokdi 🐷 · Content Studio · 2026
