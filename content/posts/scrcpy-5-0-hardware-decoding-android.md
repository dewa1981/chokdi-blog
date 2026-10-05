---
title: "scrcpy 5.0: Mirror Android ke PC, CPU Turun 10x Berkat Hardware Decoding"
date: 2026-10-05T18:20:00+07:00
draft: false
tags: ["Android", "Tutorial", "Open Source"]
---

Kalau kamu perlu melihat **dan** mengendalikan layar HP Android langsung dari laptop atau server Linux — tanpa install apa pun di HP-nya — jawabannya sudah lama satu: **scrcpy**. Dan kabar bagusnya, scrcpy **5.0 rilis 5 Oktober 2026 pukul 10:30 UTC (17:30 WIB)**, dengan satu fitur yang langsung terasa: **hardware decoding**.

Artikel ini isi apa yang baru di 5.0, cara pakainya, plus jebakan yang sudah kami kena sendiri.

## scrcpy itu apa (dan kenapa beda dari aplikasi mirror biasa)

scrcpy mem-mirror layar Android lewat USB atau TCP/IP, lalu mengizinkan kontrol pakai keyboard dan mouse komputer. Yang membuatnya beda:

| Aspek | Angka |
|---|---|
| Frame rate | 30–120 fps (tergantung HP) |
| Kualitas | 1920×1080 atau lebih |
| Latensi | 35–70 ms |
| Waktu tampil gambar pertama | ~1 detik |
| Sisa instalasi di HP | tidak ada (server di-push sementara) |

Bonusnya: **tanpa root**, **tanpa akun**, **tanpa iklan**, dan **tanpa internet**. Lisensinya Apache-2.0, repo-nya sudah dikutip **151 ribu bintang** dan 13,9 ribu fork (penulis: Romain Vimont). Syarat minimum HP: Android 5.0 (API 21) + USB debugging aktif.

## Yang baru di scrcpy 5.0

Perubahan terbesarnya bukan sekadar perbaikan kecil:

| Perubahan | Dampak nyata |
|---|---|
| **Hardware decoding (default)** | CPU turun sampai **10×**, daya lebih hemat |
| Video buffering diperbaiki | tayangan lebih stabil |
| Build Windows ARM64 | jalan native di laptop ARM |
| adb 37.0.1, FFmpeg 9.0.2, SDL 3.4.18, dav1d 1.5.4 | pondasi lebih baru |
| `ANDROID_SERIAL` berlaku di mode OTG | multi-HP lebih rapi |
| Perbaikan keyboard UHID + AltGr | tombol tidak lagi ada yang hilang |

Hardware decoding aktif otomatis. Kalau mau memaksa atau memilih dekoder tertentu:

```bash
scrcpy --hwdec=auto          # default: pakai HW kalau bisa
scrcpy --hwdec=disabled      # paksa software
scrcpy --hwdec=vaapi         # VA-API, Linux saja
scrcpy --hwdec=d3d11va       # D3D11VA, Windows saja
scrcpy --hwdec=videotoolbox  # VideoToolbox, macOS saja
```

Catatan Linux: VA-API butuh driver GPU (`va-driver-all` di Debian/Ubuntu). Kalau hardware decoder tidak sanggup, scrcpy otomatis jatuh ke software decoding — jadi aman dibiarkan default.

## Lepas kabel: mode nirkabel

Dua jalan, pilih sesuai kenyamanan.

- **Otomatis** — sambungkan sekali via USB, lalu: `scrcpy --tcpip` (scrcpy cari IP dan port adb-nya sendiri, aktifkan mode TCP/IP, lalu connect). Kalau HP sudah listen di port 5555: `scrcpy --tcpip=192.168.1.1`.
- **Manual** — `adb tcpip 5555` → cabut kabel → `adb connect IP_HP:5555` → `scrcpy`.

Sejak Android 11 ada **wireless debugging** yang membolehkan pairing tanpa pernah menancapkan kabel. Kalau ada lebih dari satu HP tersambung, pilih targetnya: `--serial=<id>` (atau `-s`), `-d` untuk USB, `-e` untuk TCP/IP, atau set environment `ANDROID_SERIAL`.

## Layar virtual: satu HP, dua layar

Fitur dari seri 3.x ini yang paling sering kami pakai. Virtual display bikin HP menjalankan layar tambahan yang **tidak mengganggu layar aslinya**:

```bash
scrcpy --new-display=1920x1080 --start-app=org.videolan.vlc
```

Sejak 3.3.1 ada `--no-vd-destroy-content`: saat virtual display ditutup, aplikasi dipindah ke layar utama, bukan dimatikan — kerjaan tidak hilang kalau koneksi putus mendadak.

## Tiga jebakan yang benar-benar bikin macet

1. **Xiaomi dan pesan `INJECT_EVENTS`.** Muncul error *"Injecting input events requires the caller... to have the INJECT_EVENTS permission"*. Solusinya: aktifkan **"USB debugging (Security Settings)"** — ini item yang **berbeda** dari "USB debugging" biasa — lalu reboot HP.
2. **Download dari situs sembarangan.** Repo resmi hanya **GitHub Genymobile/scrcpy**. Ini bukan teori: saat riset artikel ini, situs pihak ketiga yang mengaku menyediakan changelog scrcpy masih menulis **v3.3.4** sebagai versi terakhir, padahal **v5.0 sudah rilis di repo resmi**. Kalau percaya sumber itu, kamu ketinggalan tiga versi besar.
3. **HP kelas bawah ngos-ngosan.** Turunkan beban: `scrcpy -m1024` atau batasi `--max-fps=30`.

## Kami pakai untuk apa saja

- **Uji tampilan landing page di HP asli** — bukan cuma resize window browser.
- **Rekam klip promo** dari layar HP langsung dari server Linux (lihat juga [cara bikin video promosi dengan AI](/posts/video-promosi-ai/)).
- **Satu PC mengendalikan beberapa HP uji** — keyboard & mouse PC jadi input HP lewat simulasi HID.
- **Pendamping kerja agent** yang butuh "mata" di perangkat mobile, senada dengan [agent browser yang bekerja tanpa screenshot](/posts/jev-ultrafast-browser-agent-tanpa-screenshot/).

Kalau koneksinya sudah mantap, ini rangkaian opsi yang sering dipakai untuk kualitas tinggi sekaligus hemat CPU:

```bash
scrcpy --video-codec=h265 -m1920 --max-fps=60 --no-audio -K
```

## Kesimpulan

scrcpy 5.0 menutup satu-satunya kelemahan seriusnya: beban CPU. Dengan hardware decoding yang **aktif secara default**, mem-mirror Android kini murah — cocok untuk memantau HP uji 24 jam, merekam konten, atau mengubah HP bekas jadi layar kedua. Kalau kamu punya HP Android nganggur di laci, rilis ini alasan yang tepat untuk menariknya keluar.

Sumber resmi:
- Repo: [github.com/Genymobile/scrcpy](https://github.com/Genymobile/scrcpy)
- Rilis v5.0: [github.com/Genymobile/scrcpy/releases/tag/v5.0](https://github.com/Genymobile/scrcpy/releases/tag/v5.0)

Kamu sudah pernah coba scrcpy untuk kasus apa? Tulis di komentar — kalau ada yang macet di langkah nirkabel, biasanya cuma soal pairing Android 11+.

— Chokdi 🐷 · Content Studio · 2026
