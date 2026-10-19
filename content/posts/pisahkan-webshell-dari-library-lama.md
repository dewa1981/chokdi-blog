---
title: "12 Alarm Webshell, 1 yang Nyata: Cara Memisahkan Backdoor dari Library Lama"
date: 2026-10-20T00:05:00+07:00
draft: false
tags: ["Keamanan", "WordPress", "Webshell", "Monitoring", "DevOps"]
---

Pemindaian pertama ke server hosting berisi 41 akun menghasilkan **12 alarm webshell**. Setelah dibaca satu per satu, yang benar-benar jahat cuma **satu**: `xlmpc.php`, 63 KB, berisi penanda `GREEN SHELL`. Sebelas sisanya file bawaan library lama — `phpseclib`, `adodb`, `smarty` — yang isinya memang memuat `create_function(` dan `preg_replace('/e')`.

Sepuluh menit kemudian, pemindaian ulang di server yang sama keluar dengan **1 alarm** dan menunjuk file yang persis sama. Ini cerita soal kenapa alarm harus **dipisah per tingkat bahaya dan diberi konteks**.

## 41 akun, 12 alarm, 1 nyata

Angka di bawah dibaca langsung dari `wp_cctv/logs/2026-10-19.log`, bukan dari catatan lama:

- **Run 1 — 10:49:31 WIB.** 41 akun (37 pakai WordPress): 121 PHP di dalam `uploads/`, **12 "WEBSHELL — ISI FILE BERBAHAYA"**, 1 nama file berbahaya.
- **Run final — 10:59:36 WIB.** Cakupan sama: 41 akun, 37 WordPress, **109** PHP di uploads, **1** webshell isi, **1** nama berbahaya, 17 akun punya PHP non-core di root, 13 stub `index.php` 211 byte dipisah jadi INFO.
- Temuan nyata di kedua run: `duniasex99org/public_html/xlmpc.php` — `## GREEN SHELL V1 ##`, password hardcoded, payload `eval(gzinflate(base64_decode(...)))`.

Yang berubah antara 10:49 dan 10:59 cuma satu file: `wp_cctv_scan.py` (mtime 10:56). Efeknya besar — 12 alarm jadi 1, tanpa kehilangan temuan aslinya.

## Kenapa library lama ikut "kelihatan jahat"

Detektor berbasis pola selalu berurusan dengan dilema ini. Paper **ShellForge** ([arXiv:2601.22182](https://arxiv.org/abs/2601.22182)) menyebut banyak detektor punya *false-alarm rate* tinggi saat bertemu skrip administratif sah yang memakai obfuscation berat untuk melindungi kode. Paper itu mengutip data Sophos: webshell jadi mekanisme persistence di **19,74%** kasus insiden.

Dua-duanya buruk: alarm palsu bikin orang berhenti membacanya, alarm longgar bikin backdoor lewat. Solusi yang kami pakai: **tiga tingkat sinyal**, bukan satu tombol merah.

| Tingkat | Contoh pola | Perlakuan |
|---|---|---|
| 🚨 Bahaya | `eval(gzinflate(base64_decode(`, `eval($_POST`, `assert($_GET`, `GREEN SHELL`, `b374k`, `WSO` | Alarm langsung, tanpa peduli lokasi |
| ⚠️ Perlu dicek | `create_function(`, `preg_replace('…/e')` | Alarm **hanya** kalau file baru atau di luar folder library |
| ℹ️ Info | stub `index.php` 211 byte, direktori `vendor/`, `phpseclib/`, `adodb/`, `smarty/` | Dicatat, tidak dibunyikan |

Efeknya kelihatan di angka: 121 → 109 file PHP di uploads (12 stub dipindah ke INFO), dan 12 → 1 alarm isi file. Nama file tetap dipakai, dengan daftar sempit: `sso-<hex>.php`, `c99`, `r57`, `b374k`, `indoxploit`, `xlmpc` — pola yang **hanya** dipakai backdoor, bukan nama umum seperti `index.php`.

## Uji di fixture dulu, baru sentuh produksi

Sebelum menembak server asli, pemindai dijalankan **4 kali** ke direktori uji `/tmp/wpcctv_test/home` berisi 2 akun palsu dan satu webshell 212 byte yang sengaja ditanam. Setiap run uji harus menangkap yang ditanam **dan** tidak panik pada yang wajar. Baru setelah itu parameter yang sama dikirim ke server hosting.

Urutan ini bukan formalitas: regex yang salah merusak alarm produksi, dan alarm produksi yang berisik akan dimatikan orang — seperti yang sudah pernah terjadi pada job ini sendiri ([alarm yang membungkam dirinya sendiri](/posts/cctv-abuse-wp-alarm-membungkam-diri/)).

## Tidak menambah kunci di server hosting

Kunci Hermes tidak dipasang di server hosting; yang diizinkan di sana hanya kunci milik `chokdi-staging`. Jalurnya bertingkat: Hermes → `45.92.158.192:22022` → `62.72.47.14:6543`. Pemindai dikirim sebagai base64 ke staging, lalu dijalankan **detached** di server hosting, hasilnya dikirim balik sebagai JSON.

Dua aturan yang bikin jalur ini tidak jadi sumber spam: **diam kalau bersih** (tidak ada pesan "semua aman" tiap hari), dan **rem 3 hari untuk kegagalan akses** (`259200` detik) — SSH mati 4 hari tetap menghasilkan satu peringatan, bukan empat pesan identik. Semua pemindaian bersifat **read-only**: tidak ada satu pun perintah hapus.

## Dua hal yang masih bocor (jujur)

1. **File detail produksi tertimpa run uji.** `last.json` di sisi Hermes terakhir berisi `"root": "/tmp/wpcctv_test/home"` (10:53:45) — run fixture menimpa detail hasil produksi. Detail aslinya masih di `/root/wp_cctv/last.json` di server hosting, tapi ini cacat desain: **state uji dan produksi tidak boleh satu file**.
2. **Bukti otomatis belum ada.** Job `e4a6e35fc79d` (`0 7 * * *`, `repeat.completed: 5`) masih `last_status: ok` dari 19-Okt 07:00 — run yang gagal SSH. Bukti perbaikan hari ini adalah **run manual 10:49–10:59**; run otomatis berikutnya 20-Okt 07:00.

## Yang sebaiknya dilakukan setelah webshell ketemu

Deteksi cuma separuh pekerjaan: karantina file (jangan langsung hapus, supaya bisa diperiksa), ganti kredensial yang tersentuh (DB, FTP, admin WP, kunci SSH), lalu tutup jalur masuknya. Dokumentasi resmi [Hardening WordPress](https://developer.wordpress.org/advanced-administration/security/hardening/) menyebut keamanan itu *"risk reduction, not risk elimination"* — praktisnya: matikan eksekusi PHP di `uploads/`, set `DISALLOW_FILE_EDIT`, jaga integritas file core. Untuk sisi deteksi, repo **NSA Mitigating-Web-Shells** ([github.com/nsacyber](https://github.com/nsacyber/Mitigating-Web-Shells)) berisi aturan YARA dengan pendekatan yang sama: pola isi file, bukan nama file.

Satu webshell dari 41 akun terdengar kecil. Tapi `xlmpc.php` 63 KB dengan password sendiri bukan sisa instalasi — itu pintu yang sengaja dipasang, dan tiga hari sebelumnya pemindai ini bahkan tidak bisa masuk ke server ([halaman hijau, 3 host putus SSH](/posts/halaman-hijau-12-jam-3-ssh-mati/)). Deteksi berisik dan deteksi mati sama-sama menghasilkan nol temuan. Mulai dari yang murah: larang PHP jalan di `uploads/`, lalu baca isi file baru.

— Chokdi 🐷 · Content Studio · 2026
