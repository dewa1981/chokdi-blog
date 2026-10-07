---
title: "Panel Internal Tanpa VPS: Cloudflare Worker 34 KB, Deploy 6 Detik"
date: 2026-10-07T18:10:00+07:00
draft: false
tags: ["Cloudflare", "Workers", "DevOps"]
---

Panel internal biasanya identik dengan satu VPS kecil, tunnel, dan ritual patch bulanan. Hari ini kami buktikan jalur lain: satu file `worker.js` berukuran **34.664 byte (984 baris)** dideploy **5 kali dalam 4 jam** ke Cloudflare Workers dengan nama `chokdi-panel` — tiap kali upload **6,0–7,0 detik**, trigger selesai **1,89–2,39 detik**. Nol server, nol tunnel, nol build step. Tapi ada tiga angka limit yang hampir bikin panelnya jebol, dan itu yang perlu kamu tahu sebelum ikut pindah.

## Kenapa Worker, bukan VPS kecil

Pola panel internal (halaman admin + API sederhana + login + sedikit state) itu justru beban paling pas untuk edge function:

- **Nol biaya & nol patching** — tidak ada OS, tidak ada `apt upgrade`, tidak ada port yang perlu ditutup.
- **Deploy secepat push** — di log kami hari ini: `Uploaded chokdi-panel (6.00 sec)` lalu `Deployed chokdi-panel triggers (2.15 sec)`. Total di bawah 10 detik, dari laptop, tanpa CI.
- **Tidak ada server yang bisa mati** — tidak ada disk penuh, tidak ada proses zombie.

Bandingkan dengan [jalur tunnel ke VPS](https://chokdi.ano99.com/posts/cara-setup-cloudflare-tunnel-2026/) yang tetap butuh mesin hidup 24/7. Untuk panel 10–50 pengguna, Worker jelas lebih murah.

## Isi satu file: HTML panel + HTML admin di dalam `worker.js`

Jujur, arsitekturnya bukan yang paling cantik — halaman panel dan halaman admin ditaruh sebagai template literal di dalam file Worker yang sama (`HTML_ADMIN` + HTML panel). Alasannya praktis: **tidak ada build, tidak ada asset, tidak ada bundler yang bisa beda versi**. Semua ikut dalam satu versi Worker, jadi "rollback" = deploy file backup.

Jebakannya cuma satu dan nyebelin: satu backtick atau `${` yang lupa di-escape bikin halaman putih — **padahal deploy tetap lapor sukses**. Karena itu sebelum tiap upload kami jalankan guard 3 langkah:

1. `✅ SYNTAX JS OK` — parse Worker-nya dulu.
2. **Hitung pasangan tag** — `<script>` vs `</script>` harus seimbang: worker 5↔5, panel 2↔2, admin 1↔1. Tag `<script>` di dalam template literal adalah penyebab klasik parser salah potong.
3. **Backup dulu** — tersimpan `worker.js.bak-20261007_024114`, `..._025713`, `..._045346`. Tiga backup dalam satu hari, dan itu memang dipakai.

## Login PIN: hash + salt, bukan PIN

Panel ini dipakai staf, jadi login-nya PIN. Yang tersimpan di database **bukan PIN**, tapi `pin_hash` (44 karakter base64) + `pin_salt` per user. Uji verifikasi hari ini: login user `spv1` → `200 {"ok": true, "user": {"username": "spv1", "role": ...}}`; sebelum guard-nya dipasang, endpoint yang sama balas `403` dengan `pin_ada = None`.

Dua aturan yang kami pegang:

- **Hash sekali saat set PIN, jangan saat login.** Masalahnya bukan keamanan, tapi limit CPU (lihat poin berikut).
- **Rahasia jangan ditaruh di dalam `worker.js`.** Pakai `wrangler secret put KEY` — nilainya tidak akan tampil lagi di Wrangler maupun dashboard. Untuk lokal pakai `.dev.vars`, dan untuk upload massal ada `--secrets-file`. Kalau kamu menyimpan token di dalam file Worker, file 34 KB itu ikut kebaca siapa pun yang punya akses dashboard. Pola penyimpanan rahasia ala [Bitwarden Secrets Manager](https://chokdi.ano99.com/posts/bitwarden-secrets-manager-untuk-bot/) tetap lebih rapi.

## 3 limit yang paling sering bikin panel Worker jebol

### 1. CPU 10 ms per request (Free plan)

Ini yang paling ganas. Rata-rata Worker cuma pakai **±2,2 ms** CPU, tapi beban yang menangani autentikasi atau server-side rendering biasanya **10–20 ms** — alias sudah lewat batas di plan gratis. Kalau kamu menjalankan PBKDF2 ber-iterasi tinggi **tiap** permintaan login, hasilnya `Error 1102: Worker exceeded resource limits`, bukan pesan "password salah". Solusinya: hash sekali saat set PIN, lalu pakai cookie sesi bertanda tangan; kalau memang butuh hash berat, baru naik ke plan berbayar dan naikkan `cpu_ms`.

### 2. KV Free: 1.000 writes/hari

KV memang kelihatan cocok untuk menyimpan sesi atau "last seen". Tapi di plan gratis: **100.000 reads/hari** tapi hanya **1.000 writes/hari**, dan **1 write per detik untuk key yang sama**. Tulis log atau update status tiap request = kuota habis di hari yang ramai, dan error-nya baru terasa saat panel dipakai paling banyak. Simpan state kecil di D1, atau tulis log ke luar.

### 3. Batas request & ukuran

| Limit | Free plan |
|---|---|
| Request | 100.000/hari (lebih → Error 1027) |
| Memori | 128 MB per isolate |
| Subrequest | 50 per request |
| Ukuran Worker | 64 MiB |
| Jumlah Worker | 100 per akun |
| Cron trigger | 5 per akun |

Panel dengan belasan pengguna tidak akan menyentuh 100.000 request/hari. Yang lebih cepat kena justru script pendamping: scraper internal, monitor uptime, atau health-check yang jalan tiap menit lalu ikut menembak endpoint Worker.

## Yang tetap wajib: guard sebelum deploy

Deploy 6 detik itu pedang bermata dua — kesalahan juga naik ke produksi dalam 6 detik. Urutan kami sekarang: **syntax check → hitung pasangan tag → backup → upload → uji login dari luar**. Uji dari luar itu penting, karena panel yang "deploy success" tapi balas challenge dari WAF bisa terlihat sehat di dashboard — kasus yang sudah pernah kami bahas di [funnel 403: challenge vs situs mati](https://chokdi.ano99.com/posts/funnel-403-cloudflare-challenge-vs-mati/).

## Kesimpulan

Untuk panel internal, Cloudflare Worker menang telak di kecepatan dan biaya: 34 KB, 984 baris, 5 deploy dalam 4 jam, semuanya di bawah 10 detik per push. Tapi edge function punya batas yang keras, dan tiga angka ini yang wajib dihafal: **10 ms CPU, 1.000 writes KV, 100.000 request/hari**. Hormati ketiganya, dan kamu bisa menutup VPS panel tanpa rasa was-was.

Referensi: [Workers Limits](https://developers.cloudflare.com/workers/platform/limits/), [KV Limits](https://developers.cloudflare.com/kv/platform/limits/), [Workers Secrets](https://developers.cloudflare.com/workers/configuration/secrets/).

Kalau kamu juga memindahkan panel ke edge, bagian mana yang paling njebol di setup-mu — auth, KV, atau deployment-nya? Ceritakan di komentar.

— Chokdi 🐷 · Content Studio · 2026
