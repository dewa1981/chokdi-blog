---
title: "Notion Webhook ke Telegram 1 Detik: 4 Bug yang Bikin Notifikasi Hilang Diam-diam"
date: 2026-10-19T00:15:00+07:00
draft: false
tags: ["Notion", "Webhook", "Cloudflare Workers", "Otomasi"]
---

Pindah dari *polling* ke *webhook* kelihatan seperti pekerjaan setengah jam: bikin endpoint, terima POST, kirim pesan. Kenyataannya kami butuh empat kali perbaikan sebelum notifikasi Notion benar-benar sampai ke Telegram — dan tiga di antaranya gagal **tanpa error yang kelihatan**. Artikel ini isi jeroannya: arsitektur yang akhirnya jalan, empat bug yang bikin notifikasi hilang, plus cara membuktikan tanda tangan HMAC-nya memang menyala.

## Kenapa webhook, bukan polling

Dokumentasi Notion menjelaskan webhook sebagai kebalikan dari polling: "Instead of repeatedly polling the Notion API to check if anything has changed, Notion will tell you the moment something important happens." Satu POST dikirim ke endpoint kita setiap ada perubahan halaman atau database.

Yang perlu diingat sejak awal: **event `page.content_updated` itu diagregasi**. Notion sengaja menahan sebentar supaya banyak edit cepat (ngetik, format, pindah blok) jadi satu event saja. Jadi kalau kamu mengetes dan menunggu 2 detik lalu menyimpulkan "webhook mati", kamu salah tes. Pakai event non-agregat seperti `comment.created` kalau mau bukti instan.

## Alur yang akhirnya jalan

```
Notion Task Board
   │  webhook subscription (8/8 event halaman)
   ▼
notion-hook.ano99.com   (Cloudflare Worker)
   ├─ verifikasi HMAC-SHA256 dari RAW body
   ├─ dedupe per halaman di KV (TTL 600 detik)
   ├─ ambil detail kartu → Notion API
   ├─ ringkas → Telegram DM
   └─ POST ke endpoint pemicu → 202, kerja lanjut async
```

Angka yang kami ukur setelah semua bug dibereskan: webhook sampai Telegram **± 1 detik**, panggilan Worker ke endpoint pemicu **0,096 detik** (balas `202` lebih dulu, kerja di belakang), dan agen otomatis bangun **≤ 2 menit** setelah kartu masuk status *Review*. Tidak ada satu pun polling di jalur ini.

## Empat bug, tiga di antaranya senyap

### 1. WAF Cloudflare memblokir Notion → 403

Endpoint kami di belakang Cloudflare. Request dari IP datacenter Notion kena aturan keamanan, jadi yang diterima bukan event, tapi halaman challenge. Di log Worker: tidak ada apa-apa — request-nya tidak pernah sampai.

Fix-nya bukan mematikan WAF, tapi **skip rule** yang sempit: hanya path webhook, hanya method `POST`, hanya pada hostname itu. Dokumentasi Cloudflare menyediakan aksi *Skip* untuk custom rule; kuncinya sesempit mungkin, jangan "matikan semua security untuk domain ini".

Catatan penting yang bikin banyak orang gila: pada paket Free, **Bot Fight Mode tidak bisa di-skip lewat WAF Custom Rules**. Kalau kasusmu begitu, urutannya: lihat Security Events, pastikan yang menahan request itu managed rule atau bot fight, baru tentukan jalur.

### 2. HMAC dihitung dari `JSON.stringify` → selalu 401

Ini bug paling mahal. Setiap request Notion membawa header `X-Notion-Signature` berisi HMAC-SHA256 dari **body mentah**, ditandatangani pakai `verification_token` yang dikirim sekali saat verifikasi langganan.

Kode kami melakukan `JSON.parse` lalu `JSON.stringify` ulang untuk menghitung tanda tangan. Hasilnya selalu beda — urutan kunci, spasi, dan karakter escape berubah, byte-nya tidak sama lagi. Dokumentasi Notion menyebutnya eksplisit: *"Pass the raw request body exactly as it arrived (re-serialized JSON produces different bytes and fails verification)."*

Fix: baca body sebagai teks mentah, hitung HMAC dari teks itu, bandingkan dengan **constant-time compare**:

```js
const raw = await request.text();            // JANGAN parse dulu
const expected = "sha256=" + [...new Uint8Array(
  await crypto.subtle.sign("HMAC",
    await crypto.subtle.importKey("raw",
      new TextEncoder().encode(verificationToken),
      { name: "HMAC", hash: "SHA-256" }, false, ["sign"]),
    new TextEncoder().encode(raw)))
].map(b => b.toString(16).padStart(2, "0")).join("");

const sig = request.headers.get("x-notion-signature") || "";
let ok = expected.length === sig.length;
for (let i = 0; i < Math.min(expected.length, sig.length); i++) {
  if (expected[i] !== sig[i]) ok = false;    // jangan break: hindari bocor timing
}
if (!ok) return new Response("invalid signature", { status: 401 });
```

### 3. Event yang di-subscribe salah

Kartu di database Notion saat diedit memancarkan `page.content_updated`, **bukan** `page.created`. Kami berlangganan `page.created` di awal, jadi semua perubahan status kartu tidak pernah memicu apa pun. Ini jenis bug yang tidak meninggalkan jejak: 200 dikirim, log bersih, notifikasi tidak ada.

### 4. Secret Telegram belum dipasang → notif hilang diam-diam

`TG_BOT_TOKEN` dan `TG_CHAT_ID` belum di-`wrangler secret put`, tapi Worker tetap membalas 200. Artinya: Notion menganggap pengiriman sukses, tidak pernah retry, dan tidak ada satu pun alarm di sisi kami. Yang menyelamatkan hanya uji manual "kirim satu event, lihat HP".

Pelajaran umumnya: **kalau handler membalas 200, kamu tidak akan pernah tahu ada yang gagal.** Balas non-200 untuk kegagalan yang harus di-retry, dan simpan error-nya ke tempat yang bisa dibaca.

## Bukti HMAC-nya benar-benar menyala

Fix tanpa uji itu cuma niat baik. Uji tiga request ke endpoint produksi (19 Okt 2026, 00:35 WIB):

- `GET /` → **405** (hanya menerima POST, sesuai desain)
- `POST /` tanpa header `x-notion-signature` → **401**
- `POST /` dengan `x-notion-signature: sha256=deadbeef…` → **401**

Yang penting bukan angka 401-nya, tapi bahwa endpoint **menolak** request yang tidak bertanda tangan. Endpoint webhook yang membalas 200 untuk semua orang itu bukan otomasi, itu pintu terbuka: siapa pun bisa menyuruh agenmu bekerja.

## Checklist sebelum pasang di produksi

1. Skip rule WAF: path + method + hostname, sesempit mungkin.
2. Hitung HMAC dari **raw body**, bukan hasil parse-ulang.
3. Bandingkan tanda tangan dengan constant-time compare.
4. Subscribe ke event yang benar (`page.content_updated` untuk perubahan kartu).
5. Balas `2xx` **cepat**, kerja berat di belakang (async `202`) — Notion punya batas waktu tunggu.
6. Pasang semua secret dulu, lalu tes satu event nyata sampai masuk ke HP.

Kalau kamu punya job otomasi lain, dua artikel ini pas dibaca setelah ini: kenapa [cron bisa bilang OK padahal gagal](/posts/cron-job-bilang-ok-tapi-bohong/) dan pola [dead man switch untuk notifikasi yang gagal senyap](/posts/notifikasi-gagal-senyap-dead-man-switch/). Untuk yang belum punya server, [panel internal tanpa VPS pakai Cloudflare Worker](/posts/panel-internal-tanpa-vps-cloudflare-worker/) menjelaskan jalur yang kami pakai di sini.

**Sumber:** [Notion Webhooks reference](https://developers.notion.com/reference/webhooks) · [Cloudflare WAF — aksi Skip pada custom rule](https://developers.cloudflare.com/waf/custom-rules/skip/)

Punya webhook yang "sukses terus" tapi notifikasinya tidak pernah datang? Ceritakan di kolom komentar — biasanya jawabannya ada di satu header yang tidak pernah dicek.

— Chokdi 🐷 · Content Studio · 2026
