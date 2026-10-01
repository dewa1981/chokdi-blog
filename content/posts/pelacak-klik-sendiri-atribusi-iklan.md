---
title: "Pelacak Klik Sendiri: Atribusi Iklan Tanpa Vendor (Panduan 2026)"
date: 2026-10-02T00:05:00+07:00
draft: false
tags: ["Atribusi", "Marketing", "Telegram", "Landing Page"]
---

# Pelacak Klik Sendiri: Atribusi Iklan Tanpa Vendor (Panduan 2026)

Iklan jalan di mana-mana: Facebook, Google, TikTok, forum, sampai spanduk. Orang klik, chat masuk, deposit masuk. Tapi begitu ditanya **"klik dari mana yang menghasilkan closing?"** — jawabannya cuma tebakan. Budget diarahkan pakai feeling, dan sumber yang boncos ikut dibiayai terus.

Masalahnya bukan kurang data. Masalahnya data itu **milik platform iklan**, bukan milik kita — dan untuk brand judi, pintu itu mayoritas tertutup. Artikel ini membedah cara membangun pelacak klik sendiri: 20 baris JavaScript di landing page, satu tabel di VPS sendiri, dan satu view SQL yang langsung menjawab "sumber mana yang beneran ngasih duit".

## Kenapa Atribusi Pihak Ketiga Tidak Bisa Diandalkan

Dua hal yang jarang dihitung orang:

1. **Click ID milik platform, bukan milik kita.** Google menempel `gclid`, Meta menempel `fbclid`, TikTok menempel `ttclid`. Nilainya opaque — tidak bisa didekode, dan gunanya cuma kalau dikirim balik ke platform yang menerbitkannya. Kalau platform menolak bisnis kita, ID itu jadi hiasan.
2. **Apple memangkas sebagian di jalur tertentu.** Di Mail, Messages, dan Private Browsing, identifier seperti `gclid`, `fbclid`, `msclkid`, `dclid`, `twclid`, dan `mc_eid` dihapus default — sementara parameter UTM tetap selamat. Artinya pengukuran yang bergantung 100% pada click ID punya lubang yang tidak bisa ditambal dari sisi kita.

Untuk brand judi, lapisan kedua masalahnya lebih keras: akun iklan bisa hilang kapan saja, dan begitu hilang, riwayat atribusinya ikut hilang. Maka satu-satunya lapisan yang benar-benar kita kendalikan adalah **pencocokan internal** — tahu klik mana yang berujung deposit, tanpa izin siapa pun.

## Dua Lapisan yang Harus Ditangkap Bersamaan

Jangan pilih salah satu, ambil keduanya:

- **UTM** (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`) — milik kita, bisa dibaca manusia, portabel ke alat analitik apa pun.
- **Click ID** (`gclid`, `fbclid`, `ttclid`, `yclid`, dll) — milik platform, opaque, masa hidup berbeda-beda.

Masa hidup itu penting kalau mau menyimpan lama. Ringkasnya: `gclid` 90 hari untuk upload offline, `fbclid` 90 hari sebagai `_fbc`, `msclkid` 90 hari, `yclid` 21 hari, dan `ttclid` **7 hari** default (diatur di level ad group). Platform rutin merevisi angka ini, jadi cek ulang sebelum membangun strategi persistensi.

## Tiga Komponen, Nol Belanja

Bahannya sudah ada di hampir semua setup afiliasi: landing page di Cloudflare Pages/Netlify, shortlink 302 seperti `tomat.jagungbaru.com/banner/<kode>`, bot Telegram, LiveChat, dan satu VPS.

### 1. Penangkap klik (±20 baris JS di LP)

Saat halaman dibuka:

- baca `fbclid` / `gclid` / `ttclid` dari URL (atau cookie `_fbc` / `_fbp` yang sudah ada),
- baca semua UTM,
- buat kode pendek unik, misal `K-7XQ2M`,
- simpan di `localStorage` **dan** kirim ke server sendiri: `POST /tr {kode, click_id, utm, ts, referrer}`,
- tambahkan `?k=K-7XQ2M` ke setiap tautan keluar (tombol Telegram/WA).

Poin terakhir itu yang sering dilupakan: kalau cuma disimpan di browser, hilang begitu user ganti device atau bersihkan storage.

### 2. Penyambung (penerima kode)

Jalur paling rapi adalah Telegram. Tombol di LP diarahkan ke `https://t.me/<bot>?start=K-7XQ2M`, dan bot menerima payload itu di `/start` → kirim `POST /tr/link {kode, telegram_user_id}`.

**Batas teknis yang wajib diingat:** parameter `start` Telegram hanya menerima `A-Z a-z 0-9 _ -` dan **maksimal 64 karakter** — rekomendasi resminya pakai base64url, yang berarti budget praktisnya sekitar 48 byte setelah encoding. Jadi jangan pernah menaruh seluruh URL iklan di sana; simpan detailnya di server, dan bawa **kode pendek** saja.

Untuk jalur WhatsApp/LiveChat, polanya beda: kode ditempel di pesan pembuka — *"Halo, saya mau daftar [K-7XQ2M]"* — lalu CS atau webhook LiveChat membacanya dengan regex sederhana.

### 3. Pencocok + atribusi (di VPS sendiri)

```sql
CREATE TABLE clicks (
  kode      TEXT PRIMARY KEY,
  click_id  TEXT,
  utm       TEXT,
  referrer  TEXT,
  created   TEXT
);
CREATE TABLE leads (
  kode      TEXT,
  channel   TEXT,      -- telegram / wa / livechat
  user_ref  TEXT,
  status    TEXT,      -- lead / chat / daftar / depo / closing
  amount    REAL,
  updated   TEXT
);
CREATE VIEW v_source AS
  SELECT c.utm, count(*) AS n_klik,
         sum(CASE WHEN l.status='depo'    THEN 1 ELSE 0 END) AS n_depo,
         sum(CASE WHEN l.status='closing' THEN 1 ELSE 0 END) AS n_closing,
         sum(CASE WHEN l.status='closing' THEN l.amount ELSE 0 END) AS revenue
  FROM clicks c LEFT JOIN leads l ON l.kode = c.kode
  GROUP BY c.utm;
```

Satu view itu cukup untuk menjawab pertanyaan paling mahal di bisnis ini: **sumber mana yang untung, sumber mana yang cuma rame**. Tambahkan cron harian yang mengirim hasilnya ke grup internal — laporan yang datang sendiri tidak akan dilewatkan.

## Pitfall yang Mahal Kalau Diabaikan

- **Kode bukan dasar pembayaran.** Kode cuma penanda asal; verifikasi closing tetap dari panel (deposit benar-benar masuk). Kalau tidak, atribusi jadi ajang klaim palsu.
- **Storage sisi klien tidak bisa dipercaya.** Mode privat dan browser bersih menghapus `localStorage`, karena itu `POST /tr` wajib dikirim saat klik pertama.
- **Shortlink harus meneruskan parameter**, bukan membuangnya. Uji `curl -I` dan pastikan `?k=` masih ada di header `Location`.
- **Jangan simpan data pribadi berlebihan.** Kode + click ID + status sudah cukup; kalau memang harus menyimpan nomor/email, hash dulu (SHA-256) sebelum masuk tabel.

## Kesimpulan

Atribusi bukan soal punya alat paling mahal, tapi soal punya **tempat menyimpan yang tidak bisa dimatikan orang lain**. Tiga komponen di atas — penangkap klik, penyambung kode, satu tabel di VPS — menjawab pertanyaan "klik mana yang bayar" tanpa Meta, tanpa vendor, tanpa biaya langganan.

Kalau [CS multi-brand sudah jalan](https://chokdi.ano99.com/posts/chatwoot-selfhost-cs-multibrand/) dan [halaman pre-chat sudah menanyakan jenis transaksi](https://chokdi.ano99.com/posts/audit-konversi-lp-judi-tombol-mati/), langkah lanjutannya jelas: sambungkan field itu ke tabel `leads`. Dari situ, jalur dari klik sampai closing bisa dilihat utuh — dan keputusan budget berhenti jadi tebakan.

Baca juga: [Landing page judi modern tanpa JavaScript](https://chokdi.ano99.com/posts/landing-page-judi-modern-tanpa-js/) — kenapa halaman yang ringan justru lebih banyak mengonversi.

**Sudah coba bikin pelacak sendiri, atau masih bergantung pada angka dari platform iklan?** Tulis di kolom komentar.

— Chokdi 🐷 · Content Studio · 2026
