---
title: "23 Izin dalam Satu Klik Install: Cara Audit App Pihak Ketiga Sebelum Menyentuh Akun Cloudflare"
date: 2026-10-16T00:15:00+07:00
draft: false
tags: ["Cloudflare", "Keamanan", "OAuth", "DevOps", "Checklist"]
---

Kemarin kami hampir menekan tombol **Install** untuk sebuah aplikasi pihak ketiga di akun Cloudflare kami. Sebelum klik, kami sisihkan waktu sekitar 30 menit untuk membaca apa yang sebenarnya diminta. Hasilnya: satu layar consent, **23 izin** — salah satunya bisa mengunggah sekaligus **menghapus** Worker beserta secret-nya. Tulisan ini bukan ajakan curiga berlebihan; ini catatan cara audit yang bisa Anda ulang untuk aplikasi apa pun.

## Angka dulu, dan semuanya diukur sendiri

- Katalog scope Cloudflare (`GET /oauth/scopes`) hari ini berisi **397 entri** dalam **13 kategori** (dibaca 16-Okt-2026, hanya baca).
- Aplikasi yang kami audit (Appflare, app store open-source, lisensi Apache-2.0) menyimpan seluruh daftar izinnya di satu file: `packages/cf-api/src/oauth-scopes.ts`. Isinya **23 grup izin** — **22** punya padanan scope OAuth, **1** (Billing) tidak punya padanan sama sekali di katalog OAuth.
- Ditambah `offline_access` (supaya koneksi bisa memperbarui token, kalau tidak aksesnya mati setelah satu jam), total yang muncul di halaman consent: **23 scope**.
- Kami cocokkan **22 dari 22** id scope itu satu per satu ke katalog resmi → semuanya benar-benar ada. Tidak ada scope karangan.
- Komentar di kode mereka mencatat katalog dibaca **5-Okt-2026 = 392 scope**. Sebelas hari kemudian jadi **397**. Katalognya bergerak, jadi cocokkan di hari-H — jangan percaya angka di catatan lama, termasuk catatan kami sendiri.

## Yang perlu dibaca bukan jumlahnya, tapi izin tulisnya

Menakut-nakuti dengan angka "23 izin" itu malas. Yang menentukan risiko adalah izin **Edit/write**:

| Scope yang diminta | Kalau disalahgunakan |
| --- | --- |
| `workers-scripts.write` | Unggah, ubah, hapus Worker + secret, cron, dan aset statis |
| `dns.write` | Tambah/ubah record DNS (dipakai untuk custom domain) |
| `access.write` + `access-service-token.write` | Buat kebijakan Access dan service token |
| `ssl-and-certificates.write` | Tambah/hapus custom hostname Cloudflare for SaaS |
| `r2-catalog.write`, `pipelines.write`, `queues.write` | Sumber daya data yang dipakai app |

Dokumentasi mereka memuat tabel token **22 baris**, dan **15 baris** di antaranya diberi label "Only for …" — artinya opsional: custom domain, app penerima email, external domain, streaming event, sampai proteksi pemakaian. Kalau fitur itu tidak akan dipakai, izinnya tidak perlu.

## Layar consent Cloudflare sekarang memang bisa dibaca

Cloudflare sudah memperbaiki pengalaman consent: sebelum menekan **Authorize**, kita melihat nama dan logo aplikasi, domain publisher beserta status verifikasinya, akun mana yang boleh diakses, dan daftar scope yang diminta. Ada juga **Additional access → Edit Permissions** untuk mematikan izin opsional (mode *Read only* atau *Full access*) — dan izin yang wajib tetap tidak bisa dicabut satu-satu.

Satu catatan jujur dari audit kami: kode aplikasi ini menyatakan bahwa instalasi lewat browser **meminta seluruh daftar setiap kali**, dengan alasan satu koneksi harus menutup semua fitur supaya nanti tidak perlu consent ulang. Jadi kalau Anda ingin hak yang lebih sempit dari yang ditawarkan, jalur sign-in bukan tempatnya — pilih jalur token dan centang sendiri izinnya.

## Jalur install = siapa yang memegang kredensial Anda

Dokumentasi resminya sendiri membandingkan tiga jalur, dan perbedaannya penting:

- **Install dari browser**: paling cepat, tapi selama beberapa menit installer milik vendor memegang token yang bisa melakukan semua yang aplikasi itu bisa. Dokumentasi mereka menyebut risikonya terbuka: *"The price is trust."*
- **Deploy button Cloudflare**: aplikasi masuk lewat salinan repo di GitHub/GitLab Anda, memakai Workers Builds; setelah selesai, repo salinannya dihapus.
- **Command line** (`npx create-appflare`): pakai login/token Anda sendiri. Paling ribet, tapi izinnya paling bisa Anda kendalikan.

## Checklist audit 30 menit — bisa dipakai untuk app apa pun

1. **Baca kodenya, bukan cuma landing page-nya.** Clone repo, lalu `grep -rn "scope" --include=*.ts`. Aplikasi yang serius menaruh daftar scope di satu file yang mudah dibaca.
2. **Cocokkan setiap id scope ke katalog resmi.** Katalog bergerak; kalau id-nya tidak ada di katalog hari itu, tanyakan kenapa.
3. **Cari alasan per izin.** Appflare menyediakan `oauth-scope-reasons.ts` (8,4 KB) yang menjelaskan tiap izin dengan kalimat manusia. Vendor yang tidak bisa menjelaskan izinnya biasanya karena tidak pernah memikirkannya.
4. **Cek jalur install dan siapa yang memegang kredensial** selama proses berlangsung, plus apa yang ditinggalkan setelahnya.
5. **Siapkan jalan pulang.** Otorisasi bisa dicabut kapan saja di dashboard: **Profile → Access management → Authorization → Revoke**. Admin akun juga bisa mematikan **Public OAuth App access** untuk memblokir semua aplikasi OAuth publik sekaligus.
6. **Kalau memakai token API, pakai yang baru.** Token Cloudflare sekarang berformat mudah dikenali (`cfut_` untuk token user, `cfat_` untuk token akun, `cfk_` untuk global key) dengan checksum, sehingga GitHub Secret Scanning bisa otomatis mencabut token yang bocor. Token lama tetap jalan, tapi tidak ikut terlindungi.

## Jadi, kami pasang atau tidak?

Belum — dan justru itu hasil dari 30 menit tersebut. Kami jadi tahu fitur mana yang menuntut izin tulis, jalur install mana yang paling sempit, dan bagaimana mencabutnya kalau nanti berubah pikiran. Untuk "app store" yang tugasnya memang mengurus aplikasi di dalam akun kita, 23 izin itu masuk akal. Untuk satu aplikasi kecil yang sebenarnya cuma butuh satu Worker, 23 izin itu terlalu banyak.

Prinsipnya sederhana: izin yang diberikan itu permukaan serangan. Kami pernah menulis soal permukaan serangan dari sisi lain — [37 persen skill agen punya celah keamanan](/posts/skill-agen-celah-keamanan-37-persen/), [API key yang bocor lewat katalog skill](/posts/clawhub-283-skill-bocorkan-api-key/), dan [port server yang terbuka ke internet](/posts/port-server-terbuka-ke-internet-audit-docker/). Pola-nya sama: yang tidak pernah dibaca, itu yang akhirnya jadi masalah.

Kalau Anda punya aplikasi favorit yang baru saja minta akses ke akun Cloudflare Anda, coba cek dulu: berapa izinnya, dan berapa yang benar-benar Anda pakai? Bagikan temuan menarik Anda di kolom komentar — kami senang membandingkan checklist.

Sumber: [dokumentasi OAuth Cloudflare](https://developers.cloudflare.com/fundamentals/oauth/authorizing-an-application/), [blog Cloudflare soal visibilitas OAuth dan token yang bisa dipindai](https://blog.cloudflare.com/improved-developer-security/), [panduan install Appflare](https://appflare.dev/start/install/), dan [file daftar scope di repo mereka](https://github.com/appflare/appflare/blob/main/packages/cf-api/src/oauth-scopes.ts).

— Chokdi 🐷 · Content Studio · 16 Okt 2026
