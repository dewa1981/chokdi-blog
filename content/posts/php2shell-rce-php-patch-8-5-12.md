---
title: "PHP2Shell: 2 CVE 9.2, Deadline 29 Oktober, dan CVE Ketiga yang Masih Terbuka"
date: 2026-10-28T17:10:00+07:00
draft: false
tags: ["Keamanan", "PHP", "CVE", "WordPress", "Server"]
---

Tanggal 21 Oktober 2026 PHP merilis patch darurat untuk dua lubang yang bisa dieksekusi tanpa login. Tanggal 26 Oktober CISA memasukkan keduanya ke katalog *Known Exploited Vulnerabilities* — dan **deadline-nya 29 Oktober**, alias besok. Kalau kamu pegang WordPress, panel hosting, atau situs PHP apa pun yang menerima uang, ini bukan bahan bacaan, ini kerjaan hari ini.

PHP dipakai sekitar **70% website dunia** (data W3Techs yang dikutip Cloudflare). Artinya lubang di runtime PHP bukan masalah satu CMS — ini masalah setengah internet.

## 🚨 Apa yang sebenarnya bocor

Namanya PHP2Shell. Dua CVE, dua-duanya *unauthenticated remote code execution*, dan yang kena adalah **semua instalasi PHP 5.4 ke atas yang melayani request web**.

| CVE | Yang salah | CVSS 4.0 (PHP) | CVSS 3.1 (NVD) |
|---|---|---|---|
| CVE-2026-109618 | Request kehabisan memori, PHP diinterupsi sebelum data internal selesai diinisialisasi; saat cleanup data setengah jadi itu dipakai seolah valid | 9,2 | **9,8** |
| CVE-2026-109619 | Fatal error meninggalkan referensi ke memori yang sudah dilepas; request berikutnya di proses yang sama menyentuh memori basi itu | 9,2 | 8,1 |

NVD mencatat keduanya **published 21 Oktober 2026 14:17 UTC**, status `Analyzed` (saya cek langsung ke API NVD hari ini). Penemuannya kerja bareng: Calif.io, Wiz, OpenAI, dan Quarkslab.

Poin yang paling sering salah dipahami: ini **bukan bug plugin, tema, atau kode aplikasi**. Update plugin tidak menyembuhkan apa pun. Yang harus diganti adalah biner PHP yang jalan di server.

Risiko tertinggi ada di **Apache `mod_php`**, karena exploit sudah bisa jalan sebelum kode aplikasi dieksekusi. Tapi PHP-FPM, `php-cgi`, FrankenPHP, dan **LiteSpeed** juga masuk daftar — dan LiteSpeed itu yang paling banyak dipakai hosting Indonesia.

## 🔧 Angka versi yang sudah benar

Patch rilis 21 Oktober 2026 pukul 13:30 UTC (CERT-EU). Cek versi kamu dan bandingkan:

| Cabang | Versi aman minimum |
|---|---|
| PHP 8.5 | **8.5.12** |
| PHP 8.4 | **8.4.27** |
| PHP 8.3 | **8.3.36** |
| PHP 8.2 | **8.2.35** |

Untuk 7.4, 8.0, dan 8.1 ada backport source di repo php-src, tapi ketiga cabang itu sudah EOL — jangan jadi solusi permanen. Kalau PHP diurus provider shared hosting, tiket ke mereka hari ini, jangan tunggu pengumuman.

## ⏰ Kenapa deadline-nya mendesak

Begitu masuk katalog KEV, statusnya bukan lagi "kerentanan teoretis". Datanya:

- Ditambahkan **26 Oktober 2026**, `dueDate` **29 Oktober 2026**
- `forensicTriage: Yes` — artinya setelah patch, kamu diwajibkan memeriksa jejak, bukan cuma menambal
- Katalog KEV versi `2026.10.27` berisi **1.760 entri** (saya unduh feed resminya, bukan kutip berita)

Dari sisi penyerang, gerakannya cepat. Cloudflare mulai memblokir trafik eksploitasi **21 Oktober 03:02 UTC — sekitar 9 jam sebelum disclosure resmi**. Mereka juga melihat penyerang **memutasi payload** untuk mencoba melewati aturan WAF. Jadi ini bukan skenario "nanti kalau ada waktu".

Satu hal yang bisa kamu verifikasi sendiri: buka akun Cloudflare-mu, lihat *Managed Free Ruleset* (`77454fe2d30c4220b5701f6fdfb893ba`). Di akun kami, ruleset itu versi **60**, update terakhir **23 Oktober 15:07 UTC**, dan **7 dari 39 rule** di dalamnya menyebut pasangan CVE ini. Proteksi WAF nyala otomatis di paket Free maupun berbayar — tapi WAF cuma tambahan, bukan pengganti patch.

## 🐷 Jebakan: 8.5.12 pun belum bersih total

Di sinilah banyak orang berhenti terlalu cepat. Tanggal 23 Oktober PHP menerbitkan advisory untuk **CVE-2026-115560**, lubang di fitur *session upload progress*, dan yang kena justru versi yang **sudah di-patch penuh, termasuk 8.5.12**. Fix-nya baru menyusul di rilis reguler berikutnya.

Dua konsekuensi praktis:

1. Rule WAF nomor 6 memang sudah mencakup CVE ini, **tapi hanya kalau `session.upload_progress.name` masih memakai nama default**. Kalau di aplikasimu nama field itu diganti, kamu tidak tercakup.
2. Per 28 Oktober, CVE-2026-115560 **belum ada di NVD** — saya query API-nya, hasilnya nol. Jadi jangan pakai "belum ada di NVD" sebagai alasan merasa aman.

## ✅ Checklist yang bisa dieksekusi sekarang

1. **Cek versi yang benar-benar melayani web**, bukan versi CLI. `php -v` di terminal bisa beda dengan PHP-FPM yang dipakai situs. Pakai PHP Selector di panel (cPanel/aaPanel/SPanel), atau lihat folder `lsphp*` kalau LiteSpeed.
2. **Jangan percaya header.** Saya tes 9 domain publik kami sendiri: semuanya balas `server: cloudflare`, versi PHP tidak terlihat dari luar. Audit header itu bukan bukti, hanya kebetulan yang menenangkan.
3. **Patch ke angka di tabel** di atas, lalu restart FPM/web server.
4. **Jangan matikan WAF** saat proses patch. Cloudflare bilang proteksinya *stopgap* — tapi stopgap yang jalan lebih baik daripada kontrol yang cuma ada di slide.
5. **Setelah patch: berburu, jangan berhenti.** Cari file PHP yang berubah setelah 21 Oktober, akun admin baru yang tidak kamu buat, dan file aneh di folder upload. Pesan Kraken CSO Nick Percoco jelas: menutup lubang tidak otomatis mengeluarkan penyerang yang sudah masuk.

## 🪙 Sambungannya ke crypto

Kraken dan Ledger termasuk yang paling keras bersuara — dan keduanya tidak melaporkan kebobolan. Per 24 Oktober **belum ada exchange atau wallet yang mengaku rugi** karena PHP2Shell. Logikanya sederhana: yang bisa diserang adalah *web front-end* (halaman klaim, blog WordPress, portal deposit), bukan blockchain-nya.

Yang paling sering luput: **router, NAS, firewall, control panel, dan appliance vendor yang punya PHP tertanam**. Semuanya bergantung pada update firmware pabrik, dan sebagian mungkin tidak akan pernah dapat. Barengan dengan itu ada patch Node.js (26.12.1, 24.22.1, 22.23.4) dan kasus sertifikat eMudhra yang sudah kami tulis di [artikel sebelumnya](/posts/emudhra-ca-bocor-key-4-nodejs-patch-agent/). Pola WAF darurat seperti ini juga pernah kami bahas di [catatan CVE September](/posts/waf-cloudflare-emergency-cve-september-2026/), dan soal CVE yang lolos dari perhatian ada di [kasus LiteLLM](/posts/litellm-cve-2026-59822-mcp-auth-bypass/).

## Kesimpulan

Tiga angka yang perlu kamu ingat: **9,2** (skor keparahan), **29 Oktober** (deadline KEV), dan **7** (rule WAF yang sudah aktif). Satu temuan yang jarang disebut media: **CVE-2026-115560 masih terbuka walau kamu sudah pakai 8.5.12**.

Kalau server itu yang memegang deposit dan withdraw, "nanti saja sore" adalah keputusan bisnis, bukan keputusan teknis. Cek versi dulu — 30 detik — baru putuskan.

Kalau kamu punya checklist patch sendiri yang lebih rapi, tulis di kolom komentar. Kita semua belajar dari versi yang lebih cepat.

— Chokdi 🐷 · Content Studio · 2026
