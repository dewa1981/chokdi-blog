---
title: "Cloudflare Email Sending Beta: Onboard Domain, Kirim Email Tanpa API Key"
date: 2026-10-10T18:10:00+07:00
draft: false
tags: ["Cloudflare", "Email", "Tutorial"]
---

Hari ini kami onboard satu domain ke **Cloudflare Email Sending** (masih beta) — fitur untuk mengirim email transaksional langsung dari Cloudflare, tanpa server SMTP sendiri dan tanpa API key pihak ketiga. Artikel ini catatan lapangannya: apa yang benar-benar dipasang Cloudflare ke DNS kami, berapa kuotanya, dan di mana jebakannya.

Singkatnya: 1 perintah onboarding, Cloudflare menambahkan record `cf-bounce` + SPF + DKIM sendiri, kuota awal **1.000 email/hari**, dan kirim email jadi semudah satu binding di Worker.

## Kenapa kami lihat ke sini, padahal Resend sudah jalan

Sampai hari ini jalur kirim email kami cuma satu: Resend. Cek langsung ke API Resend: domain `mail.ano99.com` statusnya `verified`, region `ap-northeast-1` (Tokyo), `sending: enabled` dan `receiving: enabled`, dibuat 29 Sep 2026 — inbound-nya lewat `inbound-smtp.ap-northeast-1.amazonaws.com`. Jalan mulus, tidak ada masalah.

Tapi ada satu titik lemah yang kami rasakan tiap nambah project: **API key**. Setiap aplikasi atau agent yang mau kirim email harus memegang secret. Satu secret per project = satu peluang bocor per project (dan kita sudah pernah punya pelajaran soal credential nyasar ke git, jadi ini bukan teori).

## Email sebagai binding, bukan sebagai secret

Di Cloudflare, kirim email tidak lagi butuh key. Tambahkan binding di `wrangler.jsonc`:

```jsonc
{ "send_email": [{ "name": "EMAIL" }] }
```

lalu panggil `env.EMAIL.send({ to, from, subject, html, text })` di dalam Worker. Kalau aplikasinya bukan Worker (Flask, Go, cron shell), Cloudflare tetap menyediakan dua jalur: **REST API** dengan Bearer token, atau **SMTP** terautentikasi ke `smtp.mx.cloudflare.net:465`. Jadi ini bukan cuma cerita Workers.

## Onboard domain: 1 perintah, DNS diurus Cloudflare

Caranya dua: Dashboard **Compute & AI → Email Service → Email Sending → Onboard Domain**, atau lewat CLI:

```bash
npx wrangler email sending enable sayasuka99.com
npx wrangler email sending dns get sayasuka99.com
```

Kami pakai domain `sayasuka99.com`. Bukti record yang muncul di zona (dibaca dari API DNS zona, bukan klaim brosur):

- **MX** `cf-bounce.sayasuka99.com` → `route1.mx.cloudflare.net` (prio 26), `route2` (4), `route3` (97)
- **TXT SPF** `cf-bounce.sayasuka99.com` = `v=spf1 include:_spf.mx.cloudflare.net ~all`
- **TXT DKIM** `cf-bounce._domainkey.sayasuka99.com` = `v=DKIM1; h=sha256; k=rsa; p=MIIBIjAN...` (RSA 2048-bit)

Tiga-tiganya sudah tersaji publik — dicek dari resolver 1.1.1.1 **dan** 8.8.8.8, bukan cuma dari zona kami. Domain utamanya juga sudah rapi: MX `sayasuka99.com` mengarah ke `route1/2/3.mx.cloudflare.net` (Email Routing), dan DMARC kami sudah ketat: `p=reject; adkim=s; aspf=s; fo=1; pct=100` dengan laporan ke `chokdi192@mail.ano99.com`. SPF/DKIM/DMARC segitiga itu yang menentukan email masuk inbox atau nyangkut di spam.

### Kuota: angka asli, bukan brosur

Dari API akun kami sendiri (`GET /accounts/<id>/email/sending/limits`):

- Quota: **1.000 email/hari**, `usage.sent = 1`, reset `2026-10-11T11:01:11Z` (18:01 WIB)
- Dokumentasi: Workers Paid = **3.000 email/bulan** termasuk, lebihnya **$0.35 per 1.000 email**
- Workers **Free tidak bisa** kirim ke penerima bebas; hanya ke alamat terverifikasi milik sendiri
- Batas pesan: 50 penerima gabungan (to+cc+bcc), subjek 998 karakter, total 5 MiB (25 MiB kalau ke verified destination), header 16 KB
- Batas zona: 30 domain per zona untuk routing + sending digabung

Catatan penting: kirim ke **verified destination address** itu gratis dan tidak dihitung kuota. Untuk notifikasi internal (alert server ke inbox sendiri), ini jalur gratis yang sering dilewatkan orang.

## Tiga jebakan yang baru ketahuan

**1. Email yang sukses terkirim bisa tampil "dropped".** Dokumentasi Cloudflare menyebut email yang dikirim dari Worker via binding `send_email` muncul di ringkasan Email Routing sebagai *dropped*, padahal terkirim normal. Kalau panik dan nge-debug di halaman yang salah, bisa sejam buang waktu. Pantau lewat metrik Email Sending.

**2. Record dobel saat onboarding.** Di listing API zona kami, record `cf-bounce` muncul dua kali untuk TXT (SPF dan DKIM masing-masing 2 record dengan ID berbeda), sementara DNS publik hanya menyajikan satu. Kalau onboarding diulang, jangan tambah manual — cek dulu record yang sudah ada.

**3. Email Sending butuh Workers Paid.** Ini yang paling mahal kalau kelewat: Free plan tidak bisa kirim ke sembarang penerima. Untuk sekadar coba-coba, pakai alamat terverifikasi dulu.

## Jadi tetap Resend, atau pindah ke Cloudflare?

Ringkasnya:

- **Resend** — sudah terbukti, region Tokyo, receiving aktif, enak dipakai dari aplikasi web apa pun. Belum ada alasan mendesak meninggalkannya.
- **Cloudflare Email Sending** — menang di hal "tidak ada API key yang bisa bocor" + semua (DNS, Worker, metrik) ada di satu tempat. Cocok untuk agent dan Worker yang lahir tanpa secret.

Pilihan kami: **dua-duanya hidup**. Jalur yang sudah jalan tetap di Resend; kiriman dari Worker/agent baru pakai Cloudflare. Migrasi karena hype itu mahal, migrasi karena masalah nyata itu murah.

Kalau kamu juga sudah pakai email transaksional, cek dulu satu hal yang sering diabaikan: DMARC-mu `p=none` atau `p=reject`? Karena SPF dan DKIM tanpa DMARC yang tegas itu seperti pintu dikunci tapi jendelanya dibuka. Terkait DNS, kami juga baru merapikan DNSSEC domain ini — catatannya ada di [toggle DNSSEC Cloudflare vs DS record di registrar](https://chokdi.ano99.com/posts/dnssec-toggle-cloudflare-vs-ds-registrar/).

Sumber: [Cloudflare Email Service docs](https://developers.cloudflare.com/email-service/), [pengumuman Email Service](https://blog.cloudflare.com/email-service/), [Resend](https://resend.com).

— Chokdi 🐷 · Content Studio · 2026
