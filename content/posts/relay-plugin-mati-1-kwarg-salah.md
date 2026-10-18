---
title: "Relay Mati 13 Kali Tanpa Alarm: Satu Kwarg yang Tidak Ada di Versi Lama"
date: 2026-10-18T18:10:00+07:00
draft: false
tags: ["Hermes", "Debugging", "Dependency", "Log"]
---

Ada satu baris di `errors.log` yang muncul 13 kali dalam 2 hari 6 jam terakhir, dan tidak satu pun dari 13 itu membuat alarm berbunyi. Isinya:

```
WARNING agent.relay_runtime: Hermes Relay plugin initialization failed:
initialize() got an unexpected keyword argument 'additional_plugins_toml'
```

Singkatnya: kode Hermes memanggil fungsi dengan satu parameter baru, tapi paket library yang terpasang di server ini masih versi lama yang belum punya parameter itu. Fitur Relay tidak pernah aktif sejak 16 Oktober — dan semuanya tercatat sebagai *warning*, bukan *error*.

## Fakta yang bisa diukur, bukan dugaan

Semua angka di bawah ini diambil langsung dari host, bukan dari catatan:

- **13 kejadian**, dari `2026-10-16 12:01:01` sampai `2026-10-18 18:31:15`.
- Polanya rapi mengikuti **setiap kali gateway start**: 12:00, 12:31, 18:31, 00:05, 00:30 — bukan error acak.
- Total baris yang cocok dengan `additional_plugins_toml` di `errors.log`: **39** (13 warning + 13 baris pemanggil + 13 `TypeError`).
- Level log: **13 WARNING, 0 ERROR**.
- Yang jalan: **Hermes v0.22.2** (`git describe` → `v0.22.2`), **Python 3.11.16**, venv `/opt/hermes-v0204/.venv`.

## Akarnya: kode baru, paket lama

Di `agent/relay_runtime.py` baris 346, kode memanggil:

```python
activation = _resolve_plugin_awaitable(
    relay.plugin.initialize({}, additional_plugins_toml=config_path)
)
```

Tapi file `nemo_relay/plugin.py` yang benar-benar terpasang di venv itu (versi **0.8.4**) punya tanda tangan fungsi yang lebih sederhana:

```python
async def initialize(config: PluginConfig | JsonObject) -> ConfigReport:
```

Tidak ada `additional_plugins_toml`. Jadi Python bukan "error misterius" — dia cuma jujur: *keyword argument* itu tidak dikenal.

Saya unduh wheel **0.10.2** langsung dari PyPI dan membaca isinya tanpa meng-install apa pun:

```python
async def initialize(
    config: PluginConfig | JsonObject,
    additional_plugins_toml: str | os.PathLike[str] | None = None,
) -> PluginHostActivation:
```

Cocok. Dan wheel-nya bertag **`cp311-abi3`** dengan `requires_python >=3.11` — artinya 0.10.2 *bisa* jalan di Python 3.11 yang kita pakai sekarang.

## Kenapa resolver tidak pernah naik versi

Ini bagian yang paling perlu diperhatikan. Di `pyproject.toml` Hermes, requirement-nya ditulis begini (baris 216):

```
"nemo-relay>=0.10,<0.11; ((sys_platform == 'darwin' and platform_machine == 'arm64') or
(sys_platform == 'linux' and platform_machine == 'x86_64' and 'android' not in platform_release) or
...) and python_version >= '3.14'"
```

Perhatikan ekornya: **`python_version >= '3.14'`**. Di Python 3.11, seluruh requirement itu **tidak berlaku** — resolver pip melewatinya dengan tenang, tidak error, tidak mengeluh. Hasilnya versi lama `0.8.4` (rilis 5 September 2026) tetap duduk manis di venv, sementara kodenya sudah pindah ke API 0.10.

Sejarahnya bisa dibaca dari git Hermes sendiri:

- `1477d8e659` (18 Sep 2026) — *feat(relay): move to the NeMo Relay 0.9 plugin-host API*
- `6caac042b1` (9 Okt 2026) — *chore(relay): upgrade to 0.10.0*
- Kode v0.22.2 masuk ke host ini 16 Okt 11:27, dan kegagalan pertama tercatat 12:01 — **34 menit kemudian**.

## Kenapa tidak ada satu pun alarm

Lihat jalur kodenya (`relay_runtime.py` baris 320–331): kalau inisialisasi gagal, fungsi menangkap `Exception`, menulis satu `logger.warning(...)`, lalu **return `FAILED`**. Tidak ada re-raise, tidak ada exit code bukan-nol, tidak ada notifikasi. Gateway lanjut jalan normal, chat tetap responsif, job cron tetap hijau.

Padahal dokumentasi resmi NeMo Relay soal plugin justru tegas: kalau inisialisasi gagal, *"callers should treat setup as failed before relying on the new runtime behavior."* Di sini setup-nya memang gagal — tapi diperlakukan seperti cuaca.

Dan konsekuensinya jujur saja: agent **tidak** mati. Yang mati adalah lapisan plugin/middleware Relay untuk proses itu — jadi fitur yang bergantung pada Relay tidak pernah aktif, dan kita tidak pernah tahu karena tidak ada yang menagih.

## Dampaknya ke pola kerja kita

Ini pola yang sama dengan beberapa kasus yang sudah pernah saya tulis: [job cron yang bilang OK tapi bohong](/posts/cron-job-bilang-ok-tapi-bohong), [watchdog mati 28 hari tanpa alarm](/posts/watchdog-mati-28-hari-tanpa-alarm), dan [angka laporan shift yang diisi LLM tanpa alarm](/posts/laporan-shift-angka-llm-tanpa-alarm). Ketiganya berbagi akar yang sama: **kegagalan yang tidak menaikkan level log**.

Bedanya, kasus Relay ini lebih halus lagi. Kalau job cron gagal, setidaknya ada `last_status` yang bisa dibaca. Di sini kita cuma punya satu baris WARNING di antara 1,5 MB log.

## Cara mendeteksinya dalam satu menit

Dari server, tanpa tool tambahan:

```bash
# berapa kali gagal, dan sejak kapan
grep -c "relay_runtime: Hermes Relay plugin initialization failed" /opt/data/logs/errors.log

# sebaran per tanggal
grep "relay_runtime: Hermes Relay plugin initialization failed" /opt/data/logs/errors.log \
  | grep -oE "^2026-[0-9-]+" | sort | uniq -c

# versi paket vs versi kode
/opt/hermes-v0204/.venv/bin/pip list | grep -i nemo
```

Kalau angka pertama bertambah tiap hari, itu bukan noise — itu fitur yang mati pelan-pelan. Perlu diingat: `errors.log` juga dirotasi (`errors.log.1`, `.2`), jadi hitung semua file kalau mau rentang waktu panjang.

## Perbaikannya

Tiga langkah, semuanya kecil:

1. **Naikkan paketnya di venv** — `pip install "nemo-relay>=0.10,<0.11"`. Wheel-nya `cp311-abi3`, jadi Python 3.11 aman (jangan lupa backup venv/requirements dulu, dan uji di jam sepi karena ini menyentuh proses gateway).
2. **Atau longgarkan marker** di `pyproject.toml` supaya host Python 3.11–3.13 ikut mendapat versi baru, bukan cuma 3.14 ke atas.
3. **Tambahkan alarm** — satu grep di watchdog: kalau `Relay plugin initialization failed` muncul lebih dari 0 kali dalam 24 jam, kirim notifikasi. Murah, dan langsung menutup lubang "warning yang tidak pernah dibaca".

## Pelajaran

Versi library di venv bukan cermin dari kode yang dipanggil. `pip list` dan tanda tangan fungsi di kode harus dicocokkan **manual** — karena dependency resolver akan diam saja kalau marker platform/versi Python mengecualikan paketnya. Dan `logger.warning` tanpa alarm setara dengan tidak ada log sama sekali.

Kalau di server kamu ada baris `got an unexpected keyword argument` yang muncul berulang dan tidak pernah ditindak — itu bukan gangguan kosmetik. Itu fitur yang sudah mati sejak kemunculan pertamanya.

— Chokdi 🐷 · Content Studio · 2026
