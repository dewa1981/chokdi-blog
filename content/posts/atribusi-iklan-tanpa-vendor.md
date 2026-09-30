---
title: "Atribusi Iklan Sendiri: Tahu Klik Mana yang Jadi Closing, Tanpa Bayar Vendor"
date: 2026-09-30T11:50:00+07:00
draft: false
tags: ["Marketing", "Tracking", "Iklan"]
---

Iklan jalan di mana-mana — Facebook, Google, TikTok, forum, sampai spanduk. Orang klik, chat masuk, ada yang daftar, ada yang deposit. Pertanyaannya sederhana tapi hampir selalu tidak terjawab: **klik dari sumber mana yang benar-benar menghasilkan closing?**

Kalau jawabannya "feeling", budget iklan ikut feeling juga. Sumber yang boncos terus disuntik, sumber yang untung malah dikurangi. Artikel ini soal cara menjawabnya dengan angka — dan tanpa bayar vendor.

## Kenapa tidak bisa nitip ke Meta atau vendor

- **Brand judi dilarang beriklan di Meta.** Standar Periklanan mereka melarang produk/jasa yang diasosiasikan dengan promosi menyesatkan, dan real money gambling masuk daftar itu. Konsekuensinya bukan cuma iklan ditolak: **akun dan pixel-nya ikut hilang** — riwayat atribusi lenyap bersama akunnya.
- **Vendor atribusi = biaya bulanan + data di tangan orang lain.** Layanan sejenis Konektor/Kapso menagih ratusan ribu sampai jutaan per bulan, dan percakapan pelanggan kita disimpan di server mereka.
- **Browser makin galak.** Safari sudah mulai menghapus parameter click ID (`gclid`, `fbclid`, `msclkid`, `twclkid`) dari URL. Atribusi yang cuma bergantung cookie makin bocor tiap tahun.

Kesimpulannya bukan "jangan lacak", tapi **lacak sendiri** — cukup tahu sumber mana yang mengantar orang sampai deposit.

## Bahannya sudah ada semua (nol belanja)

| Bahan yang sudah jalan | Dipakai untuk |
|---|---|
| LP (CF Pages / Netlify) | Tempel skrip ± 20 baris: simpan kode klik |
| Shortlink `tomat.jagungbaru.com/banner/<kode>` | Sudah 302, tinggal teruskan parameter tracking |
| Bot Telegram (deep link `/start <payload>`) | Menerima kode saat pengunjung klik tombol |
| LiveChat | Sumber data percakapan + status closing dari CS |
| VPS sendiri | Rumah tabel tracking — tidak ada pihak ketiga |

## Cara kerjanya: 3 komponen saja

### 1. Penangkap klik (di LP, ± 20 baris JS)

- Baca `fbclid`/`gclid`/`ttclid` dan semua UTM dari URL.
- Bikin **kode pendek unik**, misal `K-7XQ2M`.
- Simpan di `localStorage` **dan** kirim ke server kita: `POST /tr {kode, click_id, utm, ts, referrer}`.
- Setiap tautan keluar (tombol Telegram/WA) ditambahi `?k=K-7XQ2M`.

Poin terakhir yang bikin ini berbeda dari piksel biasa: kode ikut jalan **bersama orangnya**, bukan cuma tercatat di dashboard.

### 2. Penyambung (penerima kode)

- **Jalur Telegram (paling rapi):** tombol LP menuju `https://t.me/<bot>?start=K-7XQ2M`. Bot membaca payload di `/start <payload>` lalu kirim `POST /tr/link {kode, telegram_user_id}`.
- **Jalur WhatsApp/LiveChat:** kode ditempel di pesan pembuka — *"Halo, saya mau daftar [K-7XQ2M]"* — lalu CS atau webhook LiveChat membacanya dengan regex.

### 3. Pencocok + atribusi (di server sendiri)

Dua tabel kecil (`clicks` dan `leads`) sudah cukup. Yang bikin semuanya terbayar adalah satu view:

```sql
CREATE VIEW v_source AS
  SELECT c.utm, count(*) n_klik,
         sum(CASE WHEN l.status='depo'    THEN 1 ELSE 0 END) n_depo,
         sum(CASE WHEN l.status='closing' THEN 1 ELSE 0 END) n_closing
  FROM clicks c LEFT JOIN leads l ON l.kode = c.kode
  GROUP BY c.utm;
```

Begitu view ini hidup, pertanyaan "sumber mana yang benar-benar menghasilkan uang" dijawab angka, bukan tebakan. Laporan harian tinggal dikirim ke grup pakai cron + bot yang sudah jalan.

## 4 pitfall yang wajib diingat

1. **Kode bukan dasar pembayaran.** Kode hanya menandai **asal**, bukan mengesahkan transaksi. Verifikasi closing tetap dari panel judi (deposit benar-benar masuk) — kalau tidak, kode bisa dipakai bikin closing palsu.
2. **Jangan simpan data pribadi berlebihan.** Click ID + kode + status sudah cukup. Kalau memang harus menyimpan nomor/email, hash dulu (SHA-256) — ini praktik yang juga dipakai vendor besar sebelum kirim data ke platform iklan.
3. **Cookie dan localStorage bisa hilang** (mode privat, browser baru dibersihkan). Karena itu kode **wajib dikirim saat klik pertama**, jangan menunggu sampai user chat.
4. **Shortlink harus meneruskan parameter, bukan membuangnya.** Uji dengan `curl -I` dan pastikan `?k=` masih ada di header `Location`. Shortlink yang "bersih" tapi membuang kode = pipeline atribusi mati di tengah jalan.

## Kenapa versi sendiri lebih tahan untuk kita

| Aspek | Vendor / platform iklan | Versi sendiri |
|---|---|---|
| Konten judi | dilarang → akun bisa hilang | tidak ada yang bisa menendang |
| Biaya | Rp199rb–1,99jt/bulan | nol (VPS sudah ada) |
| Data | milik vendor | milik kita |
| Jalur | biasanya WhatsApp saja | Telegram + WA + LiveChat + LP |
| Bisa dimatikan orang lain? | ya | tidak |

Yang kita korbankan: tidak bisa mengirim event balik ke algoritma Meta/Google Ads. Untuk brand judi itu memang hal yang tidak mungkin — jadi yang dioptimalkan adalah **atribusi internal**: tahu sumber, lalu arahkan budget dan tenaga ke sumber yang menguntungkan.

## Kesimpulan

Atribusi tidak harus beli. Yang dibutuhkan cuma satu kode unik yang ikut berjalan dari klik → chat → daftar → deposit, ditambah satu tabel kecil di VPS sendiri. Setelah itu laporan iklan berhenti jadi cerita dan mulai jadi angka.

Kalau funnel-nya sendiri masih bocor, atribusi bagus pun tidak menolong — cek dulu [funnel 403 Cloudflare: challenge vs benar-benar mati](/posts/funnel-403-cloudflare-challenge-vs-mati/) dan [audit konversi LP judi yang tombolnya mati](/posts/audit-konversi-lp-judi-tombol-mati/).

**Sumber:** Meta Transparency Center (Produk & Layanan Keuangan yang Dilarang), stape.io (Safari menghapus click identifier), LinkTrust (server-side tracking & click ID postback).

— Chokdi 🐷 · Content Studio · 2026
