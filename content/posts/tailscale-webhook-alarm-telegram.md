---
title: "Tailscale Webhook ke Telegram: Alarm Tailnet + Jebakan HMAC yang Bikin Signature Valid Ditolak"
date: 2026-09-21T18:25:00+07:00
draft: false
tags: ["Tailscale", "Tutorial", "Monitoring", "Keamanan", "Otomasi"]
---

Jam 3 pagi, satu device baru join ke tailnet. Tidak ada yang tahu. Baru ketahuan tiga hari kemudian saat audit mesin di console. Masalahnya bukan Tailscale-nya — masalahnya **tidak ada yang memberi tahu kita**. Ini catatan cara ngepasang alarm tailnet ke Telegram lewat Tailscale Webhook, lengkap dengan satu jebakan HMAC yang bikin signature **valid** tetap ditolak.

## Kenapa Webhook, Bukan Polling

Tailscale menyediakan webhook resmi: kita kasih satu endpoint HTTPS, lalu Tailscale kirim `POST` JSON setiap ada event di tailnet — biasanya dalam beberapa detik setelah kejadian ([dokumentasi resmi](https://tailscale.com/docs/features/webhooks)). Bandingkan dengan polling API tiap 5 menit: lebih boros, lebih lambat, dan tetap bisa kelewat.

Tiga syarat yang sering dilupakan:

1. Endpoint **wajib HTTPS** dan hanya boleh lewat port **80 atau 443**. Port 8899 mentah tidak bisa dipakai langsung — perlu reverse proxy.
2. Cuma role **Owner, Admin, Network admin, atau IT admin** yang bisa bikin/hapus webhook.
3. **Webhook secret hanya bisa dicopy sekali** saat endpoint dibuat, dan sifatnya *case-sensitive*. Kalau popup-nya sudah ditutup tanpa dicopy: hapus endpoint, bikin ulang.

## Event yang Layak Dipantau

Dari daftar event resmi, ini yang paling berguna buat alarm keamanan:

| Kategori | Event | Artinya |
|---|---|---|
| Tailnet management | `nodeCreated` | device baru masuk tailnet |
| Tailnet management | `nodeNeedsApproval` | device minta approval — sinyal device asing |
| Tailnet management | `nodeKeyExpiringInOneDay` | key node mau expire < 1 hari |
| Tailnet management | `nodeKeyExpired` | key sudah expired (koneksi bisa putus) |
| Tailnet management | `nodeDeleted` | device dihapus (termasuk node ephemeral) |
| Tailnet management | `policyUpdate` | **policy file tailnet diubah** — ini kritis |
| Device misconfiguration | `exitNodeIPForwardingNotEnabled` | exit node salah konfigurasi |
| Device misconfiguration | `subnetIPForwardingNotEnabled` | subnet router salah konfigurasi |

`policyUpdate` dan `nodeNeedsApproval` yang paling layak dikirim ke HP: dua-duanya bisa berarti "ada orang mengubah aturan akses", bukan sekadar device baru.

## Alurnya

```text
Event Tailnet
  ↓ POST JSON + header X-Tailscale-Webhook-Signature (HMAC sha256)
Endpoint HTTPS (nginx :443)  ← route /webhook/...
  ↓ proxy
Webhook runner (adnanh/webhook :9000)
  ↓ hook id → script
Script: verifikasi HMAC → parse type/message → kirim Telegram
```

Semua bagian di tengah cuma alat; yang menentukan hidup-mati alarm adalah **langkah verifikasi**.

## Jebakan #1 — HMAC Mismatch pada Body yang Di-serialize Ulang

Header-nya begini:

```text
Tailscale-Webhook-Signature: t=1663781880,v1=0123abcd...64-hex
```

Cara verifikasi menurut Tailscale: bentuk string `t + "." + body` (body asli request, bukan isi header), lalu HMAC-SHA256 dengan webhook secret sebagai key, dan bandingkan dengan `v1` pakai fungsi compare khusus HMAC. Sekilas gampang — sampai request body lewat parser.

Di kasus kami, runner `adnanh/webhook` v2.8.3 **me-parse body JSON lalu me-remarshal-nya** (key diurut alfabet + compact) saat hook diminta menerima `entire-payload`. Akibatnya byte yang kami-HMAC bukan byte yang dikirim Tailscale → **signature yang asli-pun ditolak**. Ini pola umum, bukan bug eksklusif kami: parser body yang jalan sebelum verifikasi membuat `JSON.stringify(JSON.parse(body))` tidak selalu identik dengan isi asli — beda whitespace, urutan key, escaped unicode (`\uXXXX` vs UTF-8), sampai format angka ([Code With Karani](https://www.codewithkarani.com/blog/webhook-signature-verification-body-parser-order)).

Poin pentingnya: HMAC dari JSON "hampir sama" **bukan** hash yang "hampir sama" — hash tidak kenal nilai separuh. Dan rotasi secret tidak akan menolong, karena secret-nya tidak pernah salah.

Ada dua fix yang terbukti:

- Verifikasi langsung atas **raw body** sebelum parser apa pun menyentuh request (paling bersih).
- Kalau runner-nya di luar kendali (kasus kami): verifikasi **tolerant** — cek HMAC atas body as-is **dan** atas versi sorted-compact. Tetap aman: dua-duanya butuh secret buat dipalsukan.

## Jebakan #2 — Replay Attack dan Payload Berbentuk Array

Dua hal lagi dari `dokumentasi` yang sering kelewat:

- **Replay**: nilai `t` adalah timestamp. Bandingkan dengan waktu sekarang — kalau selisihnya lebih dari 5 menit, perlakukan sebagai kemungkinan replay.
- **Root payload SELALU array**, bahkan kalau isinya cuma satu event. Parser yang berasumsi "satu object per request" akan gagal persis di saat Tailscale menggabung beberapa event jadi satu kiriman (yang memang dilakukan untuk hemat overhead).

## Verifikasi yang Jujur

Alarm baru boleh disebut "live" kalau sudah diuji dua arah:

- Kirim **test event** dari admin console → script harus lolos verifikasi dan pesan masuk Telegram.
- Kirim body dengan **signature palsu** → harus ditolak, keluar exit code ≠ 0, dan **tidak** diteruskan ke Telegram.
- Setelah edit `hooks.json`: `systemctl restart` — runner membacanya saat start, tanpa hot-reload.
- Event asli Tailscale hanya datang saat kejadian nyata (device join, key expire). Sebelum itu, jangan klaim sudah terbukti — cek bukti di `journalctl -u webhook-restart | grep tailscale`.

Kalau semua langkah ini dilewat, jangan heran alarm-nya bergabung dengan alarm lain yang diabaikan orang — pola yang sudah kami bahas di [alarm palsu bikin alarm asli diabaikan](/posts/alarm-palsu-bikin-alarm-asli-diabaikan/). Dan kalau masih bingung beda Tailscale dengan Cloudflare Tunnel untuk kasus seperti ini, ada di [sini](/posts/tailscale-vs-cloudflare-tunnel/).

## Penutup

Webhook Tailscale itu alat murah dan cepat — satu endpoint, pilih event, dapat notif detik itu juga. Kompleksitasnya ada di verifikasi signature; kunci satu kalimat: **verifikasi byte yang dikirim, bukan byte yang kamu pikir dikirim**. Kamu pernah kena HMAC mismatch karena body parser? Tulis di komentar — atau cek dulu runner-mu, mungkin sedang menyembunyikan bug yang sama.

— Chokdi 🐷 · Content Studio · 2026
