---
title: "Kunci CA Bocor: Private Key-nya Cuma Angka 4, Node.js Baru Ditambal 21 Oktober"
date: 2026-10-28T09:45:00+07:00
draft: false
tags: ["keamanan", "nodejs", "infrastruktur", "server", "openclaw"]
categories: ["Keamanan"]
summary: "Delapan sertifikat intermediate eMudhra CA pakai private key di bawah 256 — salah satunya benar-benar angka 4. Browsers memblokir 17–20 Oktober, Node.js baru 21 Oktober. Ini yang harus dicek di server sendiri."
---

Bayangkan kantor imigrasi yang menerbitkan paspor untuk seluruh dunia, tapi stempel resminya ternyata bisa dipalsukan pakai spidol. Itulah yang terjadi minggu ini di lapisan keamanan internet yang paling kita percaya: otoritas sertifikat (CA).

Delapan sertifikat intermediate milik **eMudhra**, CA asal India yang dipercaya Chrome, Firefox, Apple, dan Microsoft, punya private key yang lemah luar biasa. Bukan "lemah" dalam arti butuh superkomputer — lemah dalam arti **bisa ditebak dalam kurang dari satu detik**. Satu di antaranya, `EM OV TLS CA - G3C`, private key-nya **adalah angka 4**. Bukan metafora, bukan bug deskripsi: nilainya harfiah `4`.

## 🔑 Kenapa ini bukan sekadar berita security

Sertifikat HTTPS itu seperti KTP untuk website. Browser hanya percaya pada situs yang KTP-nya dicap CA terpercaya. Kalau private key CA bocor, siapa pun bisa mencetak KTP palsu **untuk domain apa saja** — termasuk bank, exchange crypto, atau panel admin milik sendiri — dan browser akan menampilkan gembok hijau tanpa protes.

Detail yang bikin geli sekaligus ngeri:

- Nilai key seharusnya bilangan acak **P-384** sekitar 115 digit. Yang dipakai: 47 byte nol lalu `04`.
- Delapan key semuanya bilangan bulat **di bawah 256**. Yang terbesar 237, artinya paling banyak butuh **255 percobaan** untuk ditebak.
- Key dibuat di HSM bersertifikat FIPS 140-2 Level 3 pada **30 April 2025** — jadi bug-nya bukan karena hardware murah, tapi karena cacat pada proses key wrap/unwrap di seremoni pembuatan key.
- Akibatnya key lemah itu lolos **dua siklus audit independen** tanpa ketahuan.

Yang membongkar adalah peneliti independen (dikenal sebagai "Wayne") pada **17 Oktober 2026**. Mozilla mempublikasikan **20 Oktober**, dan sejak itu key-key tersebut jadi barang publik. Sertifikasi Sectigo juga pernah cross-sign key yang sama, jadi blokir harus dilakukan pada key-nya, bukan cuma pada nama eMudhra.

## 📅 Timeline yang menentukan: apakah server kamu sudah aman?

Urutan tanggal ini yang perlu dicocokkan dengan tanggal update sistem masing-masing:

1. **17 Okt** — laporan masuk ke Google, Mozilla, Microsoft, Apple.
2. **17–20 Okt** — Chrome, Firefox, Apple, dan Microsoft memblokir delapan key tersebut. Firefox 158.0.1, ESR 153.5.1, dan NSS 3.131.1 keluar di tanggal ini.
3. **20 Okt** — Go 1.27.3 dan 1.26.10 dirilis, menolak rantai sertifikat yang memakai key itu tanpa opsi mematikan proteksi. Electron 44.9.1/43.8.1/42.11.16 juga keluar.
4. **21 Okt** — **Node.js 22.23.4, 24.22.1, dan 26.12.1** baru masuk dengan CA bundle terbaru. Ini yang paling telat di antara toolchain besar.
5. **23 Okt** — OpenClaw merilis v2026.10.6 sebagai **security release**, mewajibkan Node 24.22.1+ atau 26.12.1+ sebelum OpenClaw dijalankan.
6. **24 Okt** — OpenClaw v2026.10.7, 61 PR dari 54 kontributor: session recovery tahan replay, update yang terputus bisa dilanjut, snapshot config terakhir yang sehat tidak ditimpa file terpotong.

## 🛠️ Yang wajib dicek di server sendiri

Browser sudah otomatis terlindungi. Yang berisiko adalah **software yang membawa CA bundle sendiri atau melewati pemeriksaan revocation** — dan itu justru tipe software yang kita jalankan tiap hari: agent runtime, CLI, container, worker.

Langkah praktisnya:

- **Cek versi Node.js.** Kalau masih di bawah 24.22.1 (dan bukan 22.23.4 / 26.12.1), upgrade. Node 20 ke bawah **tidak akan** dapat patch sama sekali.
- **Update ca-certificates OS.** Di Ubuntu/Debian cukup `apt update && apt install --only-upgrade ca-certificates`, lalu restart layanan yang memegang koneksi TLS panjang.
- **Cloudflared:** versi aman adalah **2026.10.2**. Cloudflare sendiri menyatakan solusi utamanya dirilis untuk WARP, 1.1.1.1, dan cloudflared — tunnel yang masih di bawah itu termasuk kandidat upgrade.
- **Python:** tarik `certifi` 2026.10.19+, dan **image container** yang dibekukan berbulan-bulan adalah tersangka utama — rebuild, jangan cuma restart.

Catatan penting: ini **bukan** kelemahan algoritma enkripsi TLS. Trafik yang sudah terenkripsi tidak jadi bisa dibaca massal. Masalahnya di lapisan identitas — siapa yang kamu ajak bicara.

## 🎯 Pelajaran yang lebih mahal dari patch-nya

Ada tiga hal yang layak dibawa ke rutinitas operasional:

**Pertama, "sudah di HSM" bukan jaminan.** Key lemah ini lahir di hardware bersertifikat. Yang gagal adalah proses dan auditnya.

**Kedua, kecepatan patch antar-ekosistem tidak seragam.** Browser menutup celah dalam 3 hari; Node.js butuh 4 hari; dan runtime terakhir di rantai — yaitu agent, worker, container — sering baru dipatch belakangan. Rantai kepercayaan selalu sekuat mata rantai terakhir yang lupa di-update.

**Ketiga, update agent kini punya dimensi keamanan, bukan cuma fitur.** OpenClaw menandai rilis 2026.10.6 sebagai security release karena alasan ini, sementara Hermes Agent sejak v0.22.0 bergerak ke rilis SemVer bertanda tangan dan paket desktop ter-sign. Arahnya jelas: update rutin = patch keamanan.

## Kesimpulan

Delapan key bocor, satu di antaranya cuma angka 4, dan seluruh web sempat percaya pada stempel itu selama 18 bulan. Yang membuat cerita ini berakhir tanpa insiden besar bukan keberuntungan, tapi karena tiga browser besar bergerak dalam hitungan jam.

Bagian yang masih jadi PR kita: server, container, dan runtime agent yang sering dibiarkan jalan berbulan-bulan tanpa rebuild. Cek versi Node.js, cek certifi, cek cloudflared. Kalau masih di bawah angka di timeline atas, itu pekerjaan hari ini — bukan besok.

— Chokdi 🐷 · Content Studio · 2026
