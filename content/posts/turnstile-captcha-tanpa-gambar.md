---
title: "Captcha Gambar Sudah Kalah: Pasang Cloudflare Turnstile Tanpa Bikin Pengunjung Kabur"
date: 2026-11-18T11:50:00+07:00
draft: false
tags: ["Cloudflare", "Turnstile", "Keamanan", "Bot", "Web Development"]
---

Kalau kamu masih pakai captcha gambar — "pilih semua lampu lalu lintas" — kamu sedang membayar dua kali: sekali ke Google, sekali dengan kehilangan pengunjung yang malas. Sejak Turnstile jadi standar di 2026, pertanyaan yang beredar bukan lagi "captcha mana yang paling kuat", tapi "kenapa masih ada yang pakai captcha gambar".

Artikel ini bukan ringkasan dokumentasi. Ini urutan pasang yang benar, plus lima jebakan yang bikin Turnstile **kelihatan tidak berfungsi** padahal salahnya di implementasi.

## Dua Langkah, Bukan Satu

Turnstile bekerja dalam dua tahap yang wajib lengkap dua-duanya:

1. **Client-side** — widget JavaScript jalan di browser pengunjung, menyelesaikan challenge, lalu menghasilkan *token* (string sampai 2.048 karakter).
2. **Server-side** — server-mu mengirim token itu ke `https://challenges.cloudflare.com/turnstile/v0/siteverify` untuk dipastikan asli dan belum dipakai.

Dokumentasi Cloudflare menyebut eksplisit: **validasi server-side itu wajib**. Token bisa kedaluwarsa, tidak valid, atau sudah pernah dipakai. Kalau kamu cuma menaruh widget di HTML lalu percaya begitu saja, kamu tidak punya proteksi apa pun — kamu cuma punya hiasan.

## Fakta Token yang Sering Kelewat

Dua angka ini yang paling sering jadi sumber bug:

- **Umur token 300 detik (5 menit).** Pengunjung yang membuka form, lalu pergi minum kopi, balik lagi dan klik submit → token sudah mati. Hasilnya: form ditolak, pengunjung bingung, kamu menyalahkan Cloudflare.
- **Token sekali pakai.** Satu token = satu validasi. Kalau pengunjung klik submit dua kali, atau form-mu retry otomatis karena jaringan jelek, percobaan kedua **pasti gagal**. Solusinya `turnstile.reset()` di setiap akhir submit, bukan berharap token bisa dipakai ulang.

Ada satu nuansa tambahan: Cloudflare menyebut token bersifat sekali pakai "subject to network convergence" — dalam praktik, replika validasi bisa butuh waktu singkat untuk sinkron. Artinya jangan mendesain sistem yang bergantung pada penolakan instan token duplikat sebagai satu-satunya lapisan keamanan. Tetap pasang rate limit di endpoint-mu.

## Tiga Mode, Pilih Sesuai Konteks

| Mode | Tampilan | Cocok untuk |
|---|---|---|
| **Managed** (disarankan) | Kadang muncul kotak centang, tanpa gambar/teks | Form publik: daftar, login, komentar |
| **Non-Interactive** | Widget dengan spinner, tanpa interaksi | Checkout, form panjang yang tidak boleh terputus |
| **Invisible** | Tidak terlihat sama sekali | Halaman marketing, proteksi API internal |

Managed dipilih Cloudflare sendiri berdasarkan sinyal risiko pengunjung: pengunjung normal sering **tidak melihat apa pun**, sementara klien aneh dapat kotak centang. Itu sebabnya mode ini jadi default yang aman.

## Jebakan 1: Error 110200 "Domain not authorized"

Ini error client-side nomor satu yang dilaporkan. Artinya domain yang membuka widget **tidak ada di Hostname Management** milik widget tersebut. Dua penyebab umum:

- Kamu pasang widget di `staging.domain.com` tapi yang didaftarkan cuma `domain.com`.
- Kamu baru menambah hostname dan langsung tes. Di komunitas Cloudflare ada laporan jelas: hostname baru **tidak selalu langsung terverifikasi**, request pertama masih 110200 walau konfigurasi sudah benar. Tunggu propagasi, jangan buru-buru bikin widget baru.

Aturan aman: **satu widget per environment** (dev / staging / produksi) dengan daftar hostname masing-masing. Kalau satu widget dipakai di semua environment, kamu akan dapat 110200 setiap kali pindah domain.

## Jebakan 2: CSP memblokir script

Kalau situsmu pakai Content Security Policy, Turnstile tidak akan jalan sampai `challenges.cloudflare.com` diizinkan di `script-src`, `frame-src`, dan `connect-src`. Gejalanya bukan error 110200 — widgetnya hanya **tidak muncul**, dan konsol browser yang memberi tahu, bukan dashboard Cloudflare.

## Jebakan 3: Retry yang tidak dibedakan

Cloudflare mengelompokkan error client-side per keluarga kode:

- **100-an** → masalah jaringan/jendela, cukup minta pengunjung refresh.
- **110-an** → **salah konfigurasi**, jangan retry; retry 10x hasilnya tetap sama. Tampilkan pesan "hubungi support".
- **300/600-an** → challenge gagal; tawarkan ganti browser atau mode incognito.

Retry buta di semua kode = pengunjung menunggu selamanya di halaman yang tidak akan pernah lolos.

## Jebakan 4: Gagal-terbuka saat siteverify down

Endpoint validasi bisa timeout. Kalau kodemu berbunyi `try { validasi } catch { izinkan }`, kamu baru saja membuat pintu belakang: matikan koneksi ke Cloudflare, dan semua bot lewat. Pola yang benar adalah **fail closed** — anggap gagal, tolak request, log kejadiannya:

```python
try:
    r = requests.post(SITEVERIFY, data={"secret": SECRET, "response": token}, timeout=10)
    return bool(r.json().get("success"))
except requests.RequestException:
    return False   # bukan True
```

Sekalian: kirim parameter `remoteip` dari header asli (`CF-Connecting-IP` bila di belakang Cloudflare) supaya token terikat konteks jaringan pengunjung, bukan bisa dipindah-pindah.

## Jebakan 5: Kunci bocor di frontend

`sitekey` memang publik. `secret key` **tidak boleh** pernah menyentuh HTML, bundle JS, atau repo. Simpan di environment variable, dan rotasi berkala lewat dashboard atau API. Pola paling umum: developer menaruh secret di file config frontend karena "biar gampang tes" — lalu lupa menghapusnya saat produksi.

## Soal Biaya

Turnstile gratis di tier standar. Laporan pihak ketiga 2026 menyebut plafon praktisnya sekitar **20 widget, 10 hostname per widget, dan 7 hari retensi analytics** — angka ini bergerak, jadi cocokkan sendiri di halaman *Plans* Cloudflare sebelum mendesain arsitektur multi-tenant.

## Checklist Sebelum Anggap "Sudah Beres"

1. Widget terpisah untuk dev, staging, produksi.
2. Semua hostname terdaftar, termasuk subdomain.
3. CSP mengizinkan `challenges.cloudflare.com`.
4. Server memanggil siteverify — bukan hanya mengecek field kosong.
5. `success` **dan** `action` **dan** `hostname` diperiksa, bukan hanya `success`.
6. Token di-reset setelah setiap submit.
7. Error 110-an tidak di-retry; 100/300/600-an boleh.
8. Uji dengan token palsu: harus ditolak. Uji dengan token yang sama dua kali: percobaan kedua harus ditolak.

Turnstile bukan sihir — dia hanya mengganti teka-teki gambar dengan sinyal risiko yang lebih jujur. Yang menentukan aman atau tidaknya tetap implementasi di sisi server: apakah kamu benar-benar memvalidasi, atau cuma menempel widget supaya kelihatan aman.

**Sumber:** Cloudflare Turnstile Docs (Get started, Validate the token, Turnstile widgets, Client-side error codes), Cloudflare Turnstile Plans, Cloudflare Community (laporan 110200 pada hostname baru & workers.dev).
