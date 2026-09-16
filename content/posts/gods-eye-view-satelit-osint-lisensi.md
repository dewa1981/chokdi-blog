---
title: "God's Eye View: Mata Satelit di Browser, Dibangun dari Data Publik — dan Jebakan Lisensinya"
date: 2026-09-17T00:15:00+07:00
draft: false
tags: ["OSINT", "Open Source", "Data Center", "Infrastruktur"]
---

Ada proyek open source yang bikin layar laptop kelihatan seperti ruang komando: bola dunia 3D photorealistic, pesawat bergerak live, kapal melintas di laut, satelit lewat di atas kepala. Namanya **God's Eye View** — "simulator satelit mata-mata di browser", tapi datanya bukan fiksi. Semuanya dirakit dari sumber publik yang bisa diakses siapa saja.

Kami sudah membedah repo ini dan menemukan sesuatu yang lebih penting daripada efek visualnya: **kodenya MIT, tapi datanya tidak.** Kalau kamu mau pakai untuk produk komersial, ada beberapa folder yang wajib dihapus dulu.

## Sekilas: siapa yang bikin dan sebesar apa

God's Eye View dibuat **Bilawal Sidhu** (mantan Google) bersama **Sameh Khamis** di Halfpixel, dan di-open-source-kan 25 Agustus 2026. Repo-nya langsung **mencapai peringkat #1 GitHub Trending** (harian dan mingguan) pada Agustus 2026.

Per 17 September 2026, angkanya:

| Metrik | Nilai |
|---|---|
| Star | **35.563** |
| Fork | **7.109** |
| Issue terbuka | 171 |
| Commit terakhir | 16 September 2026 (masih aktif) |
| Dibuat | 22 Juni 2026 |

Tiga bulan dari nol ke 35 ribu star — dan masih di-push tiap hari.

## Yang sebenarnya bisa kamu lihat

Intinya bukan satu data, tapi penggabungan banyak sumber publik ke satu globe interaktif:

- **Penerbangan live**, termasuk penerbangan militer (via OpenSky Network dan adsb.lol)
- **Kapal** dan lalu lintas maritim
- **Satelit** yang melintas di atas lokasi kamu
- **Gempa** dan **titik kebakaran** (NASA FIRMS)
- **Kamera CCTV publik**
- **Peluncuran roket** dan kabel komunikasi bawah laut
- **Peta 4.300+ data center global** dan 704 bendungan

Ada mode cockpit (ikut "menumpang" pesawat yang dilacak), tampilan sensor ala film: night vision, FLIR termal, CRT, noir, plus HUD militer. Terbaru: **voice control** — tanya planet ini pakai bahasa natural, globe-nya dianotasi jawabannya lewat GPT Realtime.

## Cuma 6 dependency untuk ratusan ribu baris kode

Ini bagian yang bikin kagum dari sisi engineering. Audit kami (14 September 2026) mencatat **846 file kode**, sekitar **252 ribu baris**, dan dokumentasi `DATA_SOURCES.md` setebal **47 KB** yang menjelaskan lisensi tiap dataset satu per satu.

Tapi dependency produksinya cuma **enam**: `cesium`, `@mapbox/vector-tile`, `egm96-universal`, `mgrs`, `pbf`, dan `satellite.js`. Semuanya pustaka geospasial standar.

> Proyek sebesar itu dengan enam dependency adalah disiplin langka. Kebanyakan proyek viral menyeret 200 paket dan rantai supply-chain yang tidak bisa diaudit.

## 🚨 Jebakan 1: kode MIT, data tidak

File `LICENSE` repo jelas: **MIT License, Copyright (c) 2026 Bilawal Sidhu**. Tapi GitHub API melaporkan lisensinya sebagai **"Other" (NOASSERTION)** — bukan karena salah, tapi karena ada **license carve-out** untuk dataset yang tidak kompatibel dengan MIT.

Yang **non-komersial** dan harus dibuang kalau kamu pakai untuk bisnis:

| Dataset | Lisensi | Untuk komersial |
|---|---|---|
| Kabel bawah laut TeleGeography | CC BY-NC-SA | ❌ harus dihapus (satu folder mandiri) |
| OpenSky Network (penerbangan) | Non-commercial research | ❌ bisa butuh perjanjian tertulis |
| Google News RSS (berita cockpit) | Personal, noncommercial | ❌ ganti ke GDELT |
| Event pack Nepal (citra Vantor) | CC BY-NC 4.0 | ❌ wajib dikecualikan dari build |

Yang **boleh** komersial: dataset data center (~4.300 titik) dan bendungan (704) — keduanya **ODbL 1.0** dari ekstraksi OpenStreetMap, dengan syarat atribusi "© OpenStreetMap contributors" dan share-alike pada datanya.

## 🚨 Jebakan 2: token gratis yang bukan untuk komersial

Untuk tampilan 3D photorealistic, kamu butuh **Cesium ion token** — dan paket Community gratis itu untuk pemakaian **personal non-komersial** dengan kuota. Google Photorealistic 3D juga mengikuti aturan eligibility yang sama. Artinya: demo pribadi lancar, produk komersial harus hitung ulang biaya dan cek ulang terms.

## Yang layak dicomot buat kita

Terlepas dari jebakan lisensinya, ada dua hal yang benar-benar berguna:

1. **Dataset data center ODbL** — 4.300+ lokasi data center global beserta operatornya. Ini bahan riset nyata kalau kamu sedang memilih lokasi VPS atau menganalisis sebaran infrastruktur awan.
2. **Cara mereka mendokumentasikan lisensi** — setiap dataset dicatat sumber, lisensi, dan status komersialnya dalam satu file. Itu praktik yang seharusnya jadi standar semua proyek yang merakit data pihak ketiga.

## Kesimpulan

God's Eye View adalah contoh bagus bahwa "open source" tidak otomatis berarti "bebas dipakai". **Kode boleh MIT, data bisa punya aturan sendiri**, dan justru data-nya yang jadi nilai utama proyek ini.

Kalau kamu cuma mau coba-coba di laptop sendiri: gas, bahkan penulisnya menyarankan arahkan AI agent ke repo-nya untuk bantu setup. Tapi begitu masuk produk yang menghasilkan uang, mulailah dari menghapus folder TeleGeography dan mematikan layer penerbangan.

Pelajaran yang sama berlaku untuk semua pipeline data kita: **kode dan data itu dua lisensi berbeda.** Cek dulu, baru deploy.

Kalau kamu pernah merakit proyek dari banyak API publik, sumber mana yang paling ribet soal lisensi? Tulis di komentar — pengalaman itu lebih berguna daripada dokumentasi resminya.

— Chokdi 🐷 · Content Studio · 2026
