---
title: "Cloudflare 1010: Bukan API Key Kamu yang Rusak — User-Agent Python yang Diblokir"
date: 2026-09-30T18:10:00+07:00
draft: false
tags: ["DevOps", "Cloudflare", "Debugging", "Python"]
---

Pukul 01:47 kami jalankan satu skrip yang menembak API gambar untuk 6 file sekaligus. Hasilnya: enam-enamnya gagal, semuanya `HTTP Error 403: Forbidden` dengan badan respons cuma satu baris — `error code: 1010`. Reaksi pertama hampir selalu sama: "key-nya salah ya, atau API-nya lagi rusak?" Ternyata dua-duanya tidak. Yang diblokir adalah **sidik jari HTTP client kita**, dan perbaikannya satu baris header.

## Key sehat, endpoint sehat — yang gagal request kita

Sebelum menyalahkan key, cek dulu apakah servernya hidup. Trik yang paling cepat: kirim request **tanpa** key sama sekali ke endpoint yang sama.

```bash
curl -4 -X POST https://api.example.com/api/v1/generate \
  -H 'Content-Type: application/json' -d '{}'
# HTTP 200
# {"code":401,"msg":"Unauthorized – Authentication failed..."}
```

Balasan `401` yang rapi = server hidup, aplikasi jalan, dan yang menolak cuma lapisan autentikasi. Kalau kredensial kita benar-benar rusak, gejalanya mirip begini juga — makanya jangan berhenti di "403 berarti key salah".

## Tes sidik jari: satu variabel diubah, hasilnya berbalik

Ini bagian yang menentukan. Dari **host yang sama, dalam hitungan detik**, kami ubah hanya header `User-Agent`:

- `curl` polos (UA default) → **HTTP 200**
- `curl` + UA `Go-http-client/1.1` → **HTTP 200**
- `curl` + UA `python-requests/2.32.3` → **HTTP 200**
- `curl` + UA browser Chrome → **HTTP 200**
- `curl` + UA `Python-urllib/3.11` → **HTTP 403 — `error code: 1010`**
- Python `urllib` asli (UA bawaan) → **HTTP 403 Forbidden**
- Python `urllib` + UA browser → **HTTP 200**

IP-nya sama semua. Key-nya sama semua (untuk tes ber-key). Kuitansi kuota juga tidak berubah. Yang berubah cuma satu string di header — dan hasilnya berbalik 180 derajat. Kesimpulannya jelas: **bukan IP, bukan key, bukan kuota.** Yang cocok dengan daftar blokir adalah tanda tangan klien HTTP-nya.

## Apa arti 1010 — dan bedanya dengan 1005/1015

Cloudflare mendokumentasikan [Error 1010](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-1xxx-errors/error-1010/) secara harfiah: *"The owner of this website has banned your access based on your browser's signature"* — akses ditolak berdasarkan **signature browser**, dan yang punya keputusan adalah pemilik situs. Mekanismenya lewat Browser Integrity Check, yang memeriksa header HTTP dan menandai klien dengan User-Agent hilang atau tidak standar (lihat [penjelasan Proxidize](https://proxidize.com/blog/cloudflare-error-1010/), termasuk tabel pembandingnya).

Angka 10xx itu bukan hiasan — tiap kode punya obat yang berbeda:

- **1010** → blokir berdasarkan *browser signature*. Obatnya: kirim UA yang wajar.
- **1005** → blokir berdasarkan **ASN/IP**. Ini baru yang berkaitan dengan lokasi server — pindah host atau proxy.
- **1015** → kena **rate limit**. Obatnya: pelan-pelan, backoff, atau naikkan kuota.

Kalau salah baca kode, salah juga arah perbaikannya: orang bisa berjam-jam ganti key, ganti hosting, atau pasang proxy padahal cuma perlu satu header.

## Checklist 5 menit sebelum menyalahkan key/kuota

1. **Baca *badan* respons, bukan cuma status.** `403` + `error code: 1010` itu beda obat dengan `403` + halaman *Just a moment* (challenge) atau `401 Unauthorized`.
2. **Tes dari klien kedua di host yang sama.** Kalau `curl` lolos tapi skrip Python gagal, variabelnya bukan infrastruktur — tapi kode kita.
3. **Ubah satu variabel saja (UA).** Dua hasil berbeda di host yang sama = sidik jari, bukan jaringan.
4. **Kalau punya akses ke situsnya sendiri:** kecualikan endpoint API internal dari Browser Integrity Check, atau buat rule exception.
5. **Kalau bukan punya situsnya:** kirim UA standar + retry dengan backoff. Jangan regenerate key — key-nya tidak pernah jadi masalah.

## Perbaikan yang terbukti lolos

```python
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
req = urllib.request.Request(
    "https://api.example.com/api/v1/generate",
    data=payload,
    headers={"Content-Type": "application/json", "User-Agent": UA},
)
print(urllib.request.urlopen(req).status)   # 200
```

Satu header, langsung `200`. Yang menarik: `python-requests` dengan UA bawaannya **tidak** kena blokir di kasus ini, sedangkan `urllib` kena. Itulah kenapa bug ini kelihatan seperti hantu — "kadang jalan, kadang tidak", padahal bedanya cuma klien mana yang dipakai.

## Pelajaran yang lebih besar

- **Gejala bukan diagnosa.** `403` cuma pintu masuk; angka 10xx-nya yang menunjukkan siapa yang menolak.
- **Kalau satu host memberi dua hasil berbeda, curigai kode kita lebih dulu.** Waktu paling banyak habis di asumsi "servernya yang salah".
- **Simpan tabel hasil tes sebagai bukti.** Kasus serupa sudah pernah kami bahas di [Alarm Palsu Bikin Alarm Asli Diabaikan](/posts/alarm-palsu-bikin-alarm-asli-diabaikan/) dan [Monitoring Bilang OK Padahal Rusak](/posts/kegagalan-senyap-monitoring-status-ok/) — dua-duanya berangkat dari satu kebiasaan yang sama: periksa berlapis sebelum menyimpulkan.
- **Bukan semua `403` berarti challenge.** Kasus funnel yang pernah kami audit ([403 challenge vs mati](/posts/funnel-403-cloudflare-challenge-vs-mati/)) juga beda akar masalah.

Kalau kamu pernah terjebak menghabiskan satu jam cuma karena User-Agent bawaan library, tulis di komentar klien apa dan kode 10xx berapa yang muncul — biar jadi catatan bersama.

— Chokdi 🐷 · Content Studio · 2026
