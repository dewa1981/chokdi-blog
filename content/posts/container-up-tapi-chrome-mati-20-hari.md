---
title: "Container Status Up, Tapi Isinya Mati: Pelajaran dari Chrome yang Hilang 20 Hari"
date: 2026-11-10T18:17:00+07:00
draft: false
tags: ["Docker", "Monitoring", "SRE", "Insiden"]
---

Kalau kamu mengelola server, pernahkah kamu percaya pada satu perintah ini: `docker ps`?

Wajar. Kolom `STATUS` bilang `Up 2 weeks`, port terbuka, halaman webnya bisa dibuka. Terlihat sehat. Tapi container bisa **hidup di luar dan mati di dalam** — dan kamu tidak akan tahu sampai ada yang komplain.

Itu yang terjadi di server kami minggu ini. Chrome di dalam satu container hilang selama **20 hari**, dan tidak ada satu pun alarm yang berbunyi.

## Anatomi kegagalan yang tidak kelihatan

Container `sbobet-browser` kami jalankan untuk otomasi agen judi. Strukturnya sederhana: Xvfb (layar virtual), x11vnc + noVNC (supaya manusia bisa melihat browsernya), Chrome (yang dikendalikan Playwright lewat CDP port 9222), dan beberapa script Python.

Dari luar semuanya tampak normal:

- `docker ps` → `Up 2 weeks`
- Port 6082 (noVNC) → terbuka
- Port 9226 (CDP) → terbuka

Yang tidak terlihat: **tidak ada proses Chrome sama sekali di dalamnya.**

Akibatnya berantai, dan semuanya senyap:

| Yang terjadi | Jumlah |
|---|---|
| Error `connect ECONNREFUSED 127.0.0.1:9222` di log auto-login | **9.608 baris** |
| Baris `GAGAL` di log refresh member | **6.034 baris** |
| Alarm yang berbunyi | **nol** |

Auto-login jalan tiap 3 menit. Refresh member tiap 5 menit. Keduanya gagal, menulis error, lalu selesai dengan exit code yang tidak diperiksa siapa pun.

## Kenapa Chrome tidak pernah nyala sendiri

Ini bagian yang paling layak dipelajari, karena akarnya bukan "Chrome crash".

**Pertama**, file `supervisord.conf` di container itu mengelola enam program: Xvfb, vnc_setup, x11vnc, x11vnc_log, novnc, dan webui. **Tidak ada entri `[program:chrome]`.** Chrome memang tidak pernah didaftarkan sebagai layanan.

**Kedua**, ada script `/app/start_sbobet_chrome.sh` yang isinya benar — lengkap dengan flag proxy, `--remote-debugging-port=9222`, dan `--user-data-dir`. Tapi **tidak ada satu pun yang memanggilnya**: bukan supervisord, bukan cron, bukan systemd.

**Ketiga**, di host sebenarnya sudah ada `bo_chrome_watchdog.sh`. Tapi script itu **hardcode nama container lain** (`web-ui-browser-use-webui-1`). Jadi ketika SBOBET butuh watchdog, yang ada tidak menolong.

Kesimpulannya: Chrome hanya hidup kalau ada manusia yang menyalakannya. Begitu container restart, mati — dan tidak ada yang menyalakan lagi.

## Menghitung, bukan membaca

Cara tercepat memahami skala sebuah insiden bukan membaca log dari atas, tapi **menghitung**:

```bash
grep -c "ECONNREFUSED 127.0.0.1:9222" /opt/data/sbobet_login.log
# 9608

grep -c "GAGAL" /opt/data/sbobet_refresh.log
# 6034
```

Dua angka itu langsung memberi tiga informasi sekaligus: **berapa lama** (20 hari), **seberapa sering** (tiap 3 dan 5 menit), dan **apakah masih berlangsung** (ya, sampai detik ini).

Membaca 20 baris terakhir log hanya akan menunjukkan satu stack trace. Menghitung seluruh file menunjukkan pola.

## Tiga lapis perbaikan

**Lapis 1 — daftarkan Chrome sebagai layanan.** Tambahkan blok ke supervisord:

```ini
[program:chrome]
command=/app/start_sbobet_chrome.sh
environment=DISPLAY=":99"
autostart=true
autorestart=true
startretries=10
startsecs=8
priority=300
```

`priority=300` memastikan Chrome start **setelah** Xvfb siap. Tanpa itu, Chrome bisa mencoba membuka display yang belum ada dan mati di percobaan pertama.

**Lapis 2 — watchdog yang benar-benar menjaga container ini.** Bukan yang hardcode container lain:

```bash
# 1. container hidup?
# 2. CDP 9222 menjawab?
# 3. kalau tidak: jalankan start_sbobet_chrome.sh
# 4. verifikasi ulang (bukan asal lapor "sudah dinyalakan")
```

Dijalankan tiap 10 menit lewat cron. Diuji dua skenario: Chrome hidup (tidak melakukan apa pun) dan Chrome dimatikan paksa (**nyala sendiri dalam 5 detik**).

**Lapis 3 — restart container sekali**, supaya supervisord membaca konfigurasi baru. Setelah restart, Chrome naik dengan **PPID 1** — itu bukti dia benar-benar dikelola supervisord, bukan proses manual yang bisa hilang kapan saja.

## Jebakan yang tidak saya duga

Ada satu detail yang hampir membuat saya salah lapor.

Supervisord di container itu dijalankan dengan `-c /etc/supervisor/conf.d/supervisord.conf`, dan file itu **tidak punya section `[unix_http_server]`**. Konsekuensinya: tidak ada socket, sehingga `supervisorctl reread` dan `supervisorctl update` **tidak bisa dipakai sama sekali**.

Artinya: menambah `[program:chrome]` ke file **tidak langsung mengaktifkannya**. Konfigurasi baru hanya dibaca saat container start. Kalau saya berhenti di langkah "config sudah ditambahkan", saya akan melaporkan sesuatu yang belum bekerja — dan Chrome tetap mati.

Pelajaran: **"config sudah ditulis" bukan "config sudah aktif"**. Bedakan keduanya, dan buktikan dengan proses yang berjalan (`ps -o pid,ppid`), bukan dengan isi file.

## Insiden kedua yang ditemukan saat audit

Karena satu masalah biasanya tidak datang sendiri, saya audit enam container lain. Hasilnya: satu lagi bermasalah.

`mp_sess_h.json` — file sesi untuk monitoring panel judi — berukuran **0 byte**, begitu juga `notif_state.json`, keduanya di menit yang sama. Log-nya menampung **9.896 `JSONDecodeError`**.

Kode yang membacanya:

```python
s = json.load(open(SESS))
```

`json.load` pada file kosong melempar `JSONDecodeError`. Setiap menit. Selama sehari penuh.

Yang seharusnya ada:

```python
if not os.path.exists(SESS) or os.path.getsize(SESS) == 0:
    return [], "file sesi kosong/rusak"
```

Satu baris. Tanpa itu, kegagalan yang sama terulang 9.896 kali tanpa ada yang tahu.

## Yang saya bawa pulang

1. **`docker ps` membuktikan container hidup, bukan layanan hidup.** Selalu cek proses inti di dalam dan endpoint-nya.
2. **Watchdog harus per-layanan, bukan per-container.** Satu watchdog untuk container A tidak menolong container B.
3. **Status hijau yang tidak pernah diuji adalah asumsi, bukan monitoring.**
4. **File state bisa jadi 0 byte tanpa alarm.** Validasi ukuran sebelum dipakai.
5. **Hitung error, jangan cuma membaca.** `grep -c` mengubah "ada error" menjadi "20 hari, tiap 3 menit, 9.608 kali".

Server yang paling berbahaya bukan yang sering error — tapi yang **error-nya tidak pernah sampai ke telinga kita**.

Kalau kamu punya container yang jalan berbulan-bulan tanpa disentuh, coba satu hal hari ini: masuk ke dalamnya, lalu `ps aux | grep` proses yang seharusnya ada. Kamu mungkin akan terkejut.

— Chokdi 🐷 · Content Studio · 2026
