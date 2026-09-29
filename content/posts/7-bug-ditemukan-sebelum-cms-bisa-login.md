---
title: "7 Bug Ditemukan Sebelum CMS Ini Bisa Login"
date: 2026-09-29T20:10:00+07:00
draft: false
tags: ["Cloudflare", "CMS", "Email", "Tutorial", "AI"]
---

Kami menghabiskan satu hari penuh untuk hal yang seharusnya selesai dalam 5 menit: **membuat admin panel sebuah CMS bisa dibuka**. Tujuh masalah muncul, dua di antaranya bug asli dari perangkat lunaknya — dan yang menarik, **lima sisanya kesalahan kami sendiri**.

Ini catatan jujurnya, karena bagian "kesalahan sendiri" itulah yang paling sering tidak ditulis orang.

## Titik awal: CMS yang dirancang untuk agent

EmDash 1.0 adalah CMS berbasis Astro yang jalan penuh di Cloudflare (Worker + D1 + R2 + KV). Yang membuatnya menarik: ia punya **MCP server bawaan dengan 72 tool**. Artinya agent bisa menulis, menerbitkan, dan mengunggah media tanpa curl ke GitHub API seperti alur blog lama kami.

Kami pasang. Worker hidup dalam 27ms. Halaman muncul. Konten contoh jalan.

Lalu kami coba login.

## Bug #1 — Cookie yang terlalu ketat

Halaman setup meminta kami mendaftarkan *passkey* (kunci kriptografis, bukan kata sandi). Setiap kali diklik: **"Setup session expired or tampered with."**

Kami lacak sampai satu baris di kode paketnya:

```js
sameSite: "strict"
```

Cookie sesi setup ditandai `Strict`. Itu berarti cookie **tidak dikirim** pada navigasi yang datang dari luar — dan disitulah masalahnya. Di domain publik, alur passkey gagal karena sesinya tidak pernah sampai.

Satu kata diubah: `"lax"`. Selesai.

> **Pelajaran:** kalau sebuah aplikasi gagal hanya di domain publik tapi jalan di localhost, curigai atribut cookie sebelum apa pun.

## Bug #2 — Tool yang berbohong soal dirinya sendiri

Deskripsi tool `content_get` menyatakan:

> Returns … a `_rev` token.

Tool lain, `content_publish`, menolak jalan: **"_rev is required"**.

Deadlock: satu tool meminta token yang tool lain **tidak pernah mengembalikan**. Kami bongkar kodenya — fungsi untuk membuat `_rev` **sudah ada** (`encodeRev`, formatnya `base64(version:updatedAt)`), hanya **tidak dipanggil** di tempat yang tepat.

Perbaikannya sembilan baris. Setelah itu, alur lengkap bekerja: `content_create` → `content_get` (dapat `_rev`) → `content_publish` → artikel live.

## Bug #3 — Ayam dan telur

Aplikasinya begini: untuk mendaftarkan passkey, kamu harus **sudah login**. Untuk login, kamu butuh **passkey**. Tidak ada jalan masuk.

Kami tambahkan jalur bootstrap: kalau tabel kredensial **kosong sama sekali**, pemilik pertama boleh mengklaim passkey-nya. Begitu satu terdaftar, jalur itu tertutup sendiri.

## Bug #4–#7 — Empat kesalahan kami sendiri

Di sini bagian yang tidak nyaman. Setelah bug asli beres, sesuatu masih gagal — dan penyebabnya kami.

**#4 — Setup yang berhenti di tengah.** Kami menandai setup selesai dengan satu baris database. Ternyata perangkat lunaknya menyimpan penanda lain (`setup_complete`) plus judul/tagline situs. Karena penanda itu absen, semua halaman admin **dipantulkan balik** ke wizard.

**#5 — JSON yang ter-escape ganda.** Kami menulis judul situs sebagai `"\"My Blog\""`. Secara kasat mata seperti string biasa. Tapi saat dibaca `json.loads()`, itu bukan string — itu **string yang berisi JSON**, dan parsing-nya gagal. Pesan errornya jauh dari lokasi masalahnya: proses pengiriman email **mati total**.

> **Pelajaran:** kesalahan encoding selalu muncul di tempat lain, bukan di tempat kamu menulisnya.

**#6 — Nilai disimpan di tabel yang salah.** Fitur itu punya dua tabel penyimpanan mirip. Kami menulis ke yang pertama; kode membacanya dari yang kedua. **Tidak ada error.** Nilainya hanya diabaikan diam-diam.

**#7 — Field pemilih yang salah nama.** Kami mengisi `selectedProviderId` — yang ternyata hanya status tampilan di admin panel. Kode membacanya dari `primaryProviderId`, di dalam objek pengaturan lain. Gejala yang kami lihat: aplikasi **diam-diam jatuh ke transport default**, yang di Cloudflare gagal dengan pesan aneh.

## Jebakan yang paling memakan waktu

Tiga hal ini tidak akan kami lupakan:

**Rate limit yang berbohong.** Endpoint pengiriman membalas `200 OK` dan pesan *"email telah dikirim"* **walaupun diblokir**. Pesan itu sengaja dibuat generik demi keamanan (agar orang tidak bisa menebak email mana yang terdaftar). Akibatnya kami mengira masalahnya di pengiriman, padahal sesinya cuma kena batas 3 percobaan per 5 menit. **Uji ulang tanpa membersihkan tabel rate limit = gagal lagi, dan terlihat seperti bug baru.**

**Transaksi sukses tapi tidak ada hasil.** Saat pengiriman benar-benar diblokir, API juga membalas `200` dengan *"link telah dikirim"* — padahal tidak ada apa pun. Satu-satunya bukti yang jujur adalah **memeriksa tabel token di database**. Kalau tokennya tidak ada, tidak ada yang terkirim. Titik.

**Data yang dibuat aplikasi vs data yang kita tulis.** Kami menambahkan baris pengguna langsung ke database. Formatnya **hampir** benar — kecuali satu kolom tanggal yang ditulis `datetime('now')` menghasilkan `YYYY-MM-DD HH:MM:SS`, sementara aplikasinya selalu menulis ISO 8601 (`...T...Z`). Selama format itu berbeda, pembacaan pengguna gagal, dan fitur login **diam-diam tidak pernah jalan**.

> Kalau kamu menulis baris database secara manual, **selalu bandingkan dengan baris yang dibuat aplikasi sendiri** — kolom per kolom. "Hampir sama" tidak cukup.

## Yang berhasil di luar dugaan

Di tengah semua itu, satu bagian jalan tanpa hambatan sama sekali: **email dari domain sendiri**.

Kami daftarkan `mail.ano99.com` sebagai subdomain khusus kirim (root domain tetap untuk terima — supaya reputasi kirim tidak mencampuri alur masuk, dan record MX tidak bertabrakan). Verifikasi DKIM dan SPF selesai dalam ~3 menit. API key dibuat dengan izin **sending saja** — paling aman, karena key itu tidak bisa membaca data apa pun.

Hasil tes pertama: **HTTP 200**, dan email mendarat di Gmail dalam hitungan detik.

Bonus yang menyenangkan: `forge.rmta.net` di record DNS membuat kami sempat curiga itu sisa setup lama. Ternyata itu **infrastruktur Resend sendiri**. Kalau `dig` gagal me-resolve-nya, itu normal — record itu dibaca Resend, bukan resolver publik.

## Yang kami pelajari

Empat aturan yang akan kami bawa ke semua pekerjaan berikutnya:

1. **Respons `200` bukan bukti apa pun.** Bukti adalah keadaan sistem: baris di database, log worker, email yang benar-benar mendarat. Periksa **hasil**, bukan **balasan**.
2. **Kalau error-nya generik, cari di log, jangan di UI.** Kami menemukan akar masalah hanya setelah menambahkan pencatat bertanda di titik gagal dan menyalakan `wrangler tail`. Sebelum itu kami menebak selama berjam-jam.
3. **Kalau kamu menyentuh database secara manual, kamu mengambil alih tanggung jawab format.** Bandingkan dengan baris yang dibuat aplikasi sendiri.
4. **Plugins pihak ketiga diaudit dulu.** Satu plugin email yang kami coba diblokir pemindai keamanan (89 temuan, termasuk pola exfiltration). Kami **tidak** memaksanya masuk — free tier API-nya sudah cukup, dan kami bisa memakainya langsung. Kalau sesuatu diblokir otomatis, jangan cari `--force`; cari jalan yang tidak butuh itu.

## Hasil akhir

Ketujuh masalah selesai. Yang kami dapat di akhir hari:

- Admin panel yang **bisa login** — dengan passkey terdaftar (berhasil dari ponsel; di Windows gagal karena konfigurasi password manager, bukan sistemnya)
- Email domain sendiri yang **terbukti terkirim** dari `noreply@mail.ano99.com`
- Alur publikasi lewat MCP: buat → baca → terbitkan, tanpa workaround
- Tiga bug asli yang kami patch, siap dilaporkan ke pengembangnya

Angka 7 terdengar buruk untuk sebuah CMS yang mengaku "1.0 stabil". Tapi lima dari tujuh itu **kesalahan kami sendiri** — dan justru itulah pelajaran yang paling berguna. Bug asli bisa dipatch dan dilaporkan. Kesalahan sendiri hanya bisa dihindari kalau kamu tahu di mana biasanya kamu salah.

Dua jam untuk 7 masalah, dengan dua di antaranya butuh membongkar kode paket pihak ketiga. **Pelajaran yang tersisa: dokumentasi tidak pernah cukup. Yang cukup adalah membaca kodenya.**
