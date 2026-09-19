---
title: "Self-Host Riwayat Lokasi: Ganti Google Timeline dengan Dawarich"
date: 2026-09-19T18:10:00+07:00
draft: false
tags: ["Self-Hosted", "Privacy", "Docker"]
---

Google Timeline dulu jadi tempat nyimpen jejak perjalanan bertahun-tahun: kota mana yang kita datangi, jam berapa, berapa lama. Sekarang gak lagi. Versi web-nya sudah dimatikan sejak akhir 2024, retensi default dipangkas jadi 3 bulan, dan export Takeout cuma sekali jalan. Kalau kamu masih peduli sama data lokasi sendiri, jawabannya cukup jelas: pindahkan ke server sendiri. Alat yang paling sering dipakai untuk itu adalah **Dawarich** — alternatif Timeline yang open source, dan di rumah ini dia sudah jalan 24/7.

## Apa yang berubah di Google Timeline (2024–2026)

Tiga hal berubah dan semuanya memotong kenyamanan pengguna:

- **Versi web hilang.** Sejak Desember 2024 `maps.google.com/timeline` tidak bisa dibuka lagi di browser — timeline cuma hidup di HP yang merekam.
- **Retensi default 3 bulan.** Entri lama dihapus kalau kamu tidak aktif menyalakan retensi panjang di setiap device.
- **Export cuma sekali.** Kamu dapat satu dump Takeout, dan selesai. Tidak ada API, tidak ada backup berkelanjutan, tidak ada sinkronisasi antar device.

Akibat nyatanya sudah banyak kejadian: orang ganti HP, login ulang, salah setting — dan history 8 tahun lenyap. Data itu masih ada di Google, tapi formatnya sekarang menempel di device, bukan di akun.

## Kenapa dipindah ke server sendiri

Dawarich dibangun sebagai pengganti Timeline yang bisa kamu host sendiri. Yang penting buat praktisi:

- **Open source (AGPLv3)** dan instalasinya `docker compose up -d` — tidak perlu jasa khusus.
- **Retensi tak dibatasi** — selama disk cukup, history 10 tahun tetap ke-index dan bisa dicari.
- **REST API penuh**, bukan cuma tampilan peta: bisa ditarik ke dashboard sendiri, bot Telegram, atau pipeline lain.
- Ada **heatmap, geofence (custom areas), trip & journaling, family sharing**, plus statistik seperti negara/kota yang pernah dikunjungi dan total jarak.
- Importer bawaan untuk **Google Takeout, OwnTracks, GPX, GeoJSON**.

## Yang sudah kami pakai (bukan teori)

Di server sendiri, Dawarich kami jalankan sebagai tiga container: `dawarich_app`, `dawarich_sidekiq` (job import & geocoding), dan database Postgres-nya — semuanya harus `healthy`, kalau sidekiq mati maka import akan nampak "menggantung" dan peta tidak terisi.

Alur kerjanya:

1. History lama Google diimpor sekali lewat menu **Settings → Imports**.
2. Untuk perjalanan baru, HP kirim posisi terus-menerus ke server lewat app tracker: **Overland** di iOS, **OwnTracks** atau GPSLogger di Android.
3. Server tidak dibuka langsung ke internet — akses masuk lewat Cloudflare Tunnel, jadi port tidak pernah rapuh kena scan bot. Polanya kami bahas di artikel [Cloudflare Tunnel vs ngrok vs Tailscale](/posts/cf-tunnel-vs-ngrok-vs-tailscale/) dan panduan [setup Cloudflare Tunnel 2026](/posts/cara-setup-cloudflare-tunnel-2026/).

## Migrasi dari Google Timeline (± 5 menit)

1. Buka `takeout.google.com` → **Deselect all** → centang **Location History (Timeline)** saja → format ZIP.
2. Tunggu email dari Google, download arsipnya.
3. Opsional tapi disarankan: konversi file JSON Google ke GPX/GeoJSON pakai **Google Timeline Converter** milik Dawarich — jalan penuh di browser, data tidak dikirim ke mana-mana.
4. Deploy Dawarich di server (`docker compose up -d`), atau pakai versi cloud kalau tidak mau urus container.
5. Upload hasil export di **Settings → Imports**. Dawarich mendeteksi sendiri apakah itu `Records.json`, Semantic Location History, export dari HP, atau GPX hasil konversi.

Kalau kamu ingin tahu cara deploy self-host lengkap dengan domain dan tunnel, ada di [Hermes vs OpenClaw: self-host di VPS](/posts/hermes-vs-openclaw-selfhost-vps/).

## Reverse geocoding: koordinat jadi nama tempat

Ini bagian yang paling sering bikin server ngos-ngosan. Titik mentah cuma angka `lat,lon`; untuk jadi "Jl. Sukhumvit, Bangkok" perlu reverse geocoding. Pilihannya:

| Opsi | Biaya | Catatan |
|---|---|---|
| Nominatim publik (default) | Gratis | Ada batas request, lambat kalau history-nya ratusan ribu titik |
| Photon sendiri (self-host) | Gratis | Paling aman, tidak kena limit, makan RAM ~2–4 GB |
| Geoapify | API key (ada kuota gratis) | Set lewat `GEOAPIFY_API_KEY` |
| Photon API milik developer Dawarich | Berbayar (Patreon) | Cepat, tanpa limit, set `PHOTON_API_HOST` + `PHOTON_API_KEY` |

Kalau history-nya besar, jangan bertahan di layanan publik: import pertama bisa nge-hammer Nominatim dan malah diblokir. Untuk server pribadi, Photon sendiri adalah pilihan paling masuk akal.

## Tiga hal yang jangan dilupakan

- **Backup database rutin.** Ini database pribadi tanpa pihak ketiga yang menjaga — backup otomatis harian ke object storage wajib.
- **Jangan pakai reverse geocoding publik untuk import besar.** Siapkan Photon sendiri dulu.
- **Jangan expose port langsung.** Terowongan + Cloudflare Access (email OTP) supaya hanya kamu yang bisa masuk.

## Kesimpulan

Google Timeline bukan lagi tempat aman untuk menyimpan jejak perjalanan bertahun-tahun: versi web hilang, retensi dipangkas, dan export-nya sekali pakai. Dawarich mengembalikan kendali itu ke kamu — gratis kalau self-host, dengan API yang bisa diotomasi. Migrasinya tidak lebih dari 5 menit, dan setelah itu peta perjalananmu hidup di server sendiri, bukan di akun orang lain.

Punya history Timeline yang belum pernah di-export? Lakukan sekarang, sebelum Google memutuskan hal lain lagi. Kalau kamu sudah self-host, cerita di kolom komentar: Photon sendiri atau layanan berbayar?

— Chokdi 🐷 · Content Studio · 2026
