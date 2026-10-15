---
title: "Funnel VIP 403 Selama 24 Hari: Alarm yang Tidak Pernah Berbunyi"
date: 2026-10-15T18:20:00+07:00
draft: false
tags: ["Landing Page", "Monitoring", "Cloudflare", "DevOps"]
---

Enam shortlink funnel brand kami periksa sore ini (15 Okt, 18:31 WIB) — **semuanya balas HTTP 302**, kelihatan sehat semua. Tapi begitu redirect-nya diikuti, satu ujungnya sudah **403 sejak 21 September: 24 hari** — dan tidak ada satu pun alarm yang berbunyi. Artikel ini soal kenapa itu bisa terjadi, dan cara mendeteksinya dengan satu perintah.

## Enam shortlink, satu ujung pincang

Semua shortlink balas 302 (artinya redirector kami sendiri sehat):

```
vip   302 -> https://c1.vip579cepat.top/
s161  302 -> https://4.slot161cuan.top/
fb99  302 -> https://fastbet99pusat.com/
```

Ujungnya yang beda jauh:

- `c1.vip579cepat.top` → **403** (`cf-mitigated: challenge`)
- `s1.vip579maju.top` (host VIP lain) → **403**
- `4.slot161cuan.top` → **200** (judul halaman: "SLOT161 : Daftar Situs Slot88 Resmi…")
- `fastbet99pusat.com` → **200**
- `vip579.net/register` → **200** (judul: "VIP579")

Perhatikan: brand lain sehat, jadi ini bukan soal infrastruktur kami rusak. Yang pincang cuma jalur VIP — dan jalurnya sudah pincang tiga minggu lebih.

## 302 bukan bukti apa pun

Kesalahan paling umum: kita mengukur **shortlink**-nya, bukan **hasil akhirnya**. Shortlink itu redirector milik kami sendiri — dia balas 302 walau tujuan akhirnya mati atau menampilkan halaman kosong. Status 302 hanya bilang "redirect diterima", **bukan** "calon pendaftar sampai ke halaman daftar".

Urutan yang benar: **shortlink → header `Location` → status tujuan → judul halaman tujuan**. Empat langkah, bukan satu.

### Bedakan "challenge" dari "mati" — satu baris header

403 di belakang Cloudflare ada dua rasa, dan obatnya beda:

```
$ curl -s -4 -D - -o /dev/null https://c1.vip579cepat.top/ | head -3
HTTP/2 403
cf-mitigated: challenge
```

Kalau `cf-mitigated: challenge` muncul, artinya permintaannya dihentikan **Challenge Page** Cloudflare — bukan origin mati. Menurut [dokumentasi resmi Cloudflare](https://developers.cloudflare.com/cloudflare-challenges/challenge-types/challenge-pages/detect-response/), header ini hadir untuk **semua tipe challenge** dan `challenge` adalah satu-satunya nilai yang sah. Cloudflare juga menyebut challenge [dirancang lewat otomatis oleh pengunjung asli](https://developers.cloudflare.com/cloudflare-challenges/).

Kejujuran penting: dari server (IP datacenter, `curl` polos) **kita tidak akan pernah lolos challenge**, jadi 403 dari sini **tidak otomatis berarti pengunjung manusia tertahan**. Yang terbukti: 24 hari statusnya non-200 untuk pemeriksaan otomatis, tak ada yang tahu, dan brand yang sama punya jalur daftar yang balas 200 (`vip579.net/register`). Memastikan sisi manusia = buka dari browser asli.

## Kenapa 24 hari tidak ada yang tahu

Tiga sebab, dan semuanya struktural — bukan karena orangnya malas:

1. **Tidak ada job yang memeriksa rantai ini.** Dari 81 job cron di server kami, **0** yang menyebut domain shortlink funnel (`grep -c` pada `jobs.json` = 0). Yang diperiksa robot: server hidup, disk, backup, gateway — bukan konversi iklan.
2. **Destinasi brand itu diputar-putar.** Bulan lalu `fb99` menunjuk `fastbet99.it.com`; sekarang `fastbet99pusat.com`. Rotasi domain itu normal — tapi artinya link lama bisa jadi **yatim** tanpa ada yang mencatat. Kalau pemantauan tidak menyimpan baseline tujuan, perubahan ini tak terlihat.
3. **Pemeriksaan hanya terjadi saat ada yang kebetulan membuka.** Ujung-ujungnya ditemukan oleh sesi review manual, bukan oleh sistem. Ini pola yang sama seperti [watchdog yang mati 28 hari](/posts/watchdog-mati-28-hari-tanpa-alarm/) dan [kegagalan senyap yang statusnya "OK"](/posts/kegagalan-senyap-monitoring-status-ok/).

## Cek rantai dengan satu perintah

Ini bentuk minimal yang layak dipasang sebagai cron harian. Simpan sebagai script, jalankan lewat pembungkus `.sh` (bukan inline panjang), dan tulis hasilnya ke file supaya bisa dibandingkan besok:

```bash
#!/bin/bash
# funnel_chain_check.sh — cek ujung redirect, bukan cuma shortlink
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36"
for K in vip s161 fb99 sb99 hk99 nx; do
  U="https://tomat.jagungbaru.com/banner/$K"
  CODE=$(curl -s -4 -o /dev/null -w "%{http_code}" -A "$UA" "$U")
  FINAL=$(curl -s -4 -o /dev/null -w "%{url_effective}" -L -A "$UA" "$U")
  END=$(curl -s -4 -o /dev/null -w "%{http_code}" -L -A "$UA" "$U")
  MIT=$(curl -s -4 -D - -o /dev/null -L -A "$UA" "$U" | grep -i '^cf-mitigated' | tr -d '\r')
  echo "$(date '+%F %T') $K shortlink=$CODE ujung=$END $MIT final=$FINAL"
  [ "$END" != "200" ] && echo "ALARM: funnel $K ujung $END ($MIT) -> $FINAL"
done
```

Catatan penting: **selalu pakai User-Agent browser** untuk jalur ini. `curl` polos dari IP server akan kena challenge lebih sering, dan alarm jadi palsu — dan [alarm palsu bikin alarm asli diabaikan](/posts/alarm-palsu-bikin-alarm-asli-diabaikan/).

## Tiga hal yang layak dipasang

1. **Baseline tujuan per brand.** Simpan `Location` + judul halaman tujuan tiap hari. Judul berubah dari "Slot88" ke "Domain for Sale" = alarm.
2. **Alarm non-200 > 15 menit** ke Telegram, satu pesan per kejadian (bukan 50). Tambahkan kolom `cf-mitigated` di laporan supaya triage-nya cepat: challenge atau origin mati.
3. **Verifikasi manusia 1× sehari** untuk brand yang ujungnya non-200 — buka dari browser, screenshot, simpan. Bot memang tidak bisa memutuskan "pengunjung asli tertahan atau tidak"; itu kerja manusia.

## Kesimpulan

Funnel yang mati tidak berteriak. Dia balas 302, terlihat sopan, dan menunggu tiga minggu sampai ada yang kebetulan memeriksanya. Yang membedakan tim yang tahu dari yang tidak bukan alat mahal — cuma satu kebiasaan: **selalu ikuti redirect sampai ujung, ukur halaman akhirnya, dan simpan baseline-nya**. Cara membedakan 403 challenge vs situs mati pernah kami tulis [di sini](/posts/funnel-403-cloudflare-challenge-vs-mati/) — sekarang tinggal dijalankan otomatis setiap hari.

Ada funnel lain di server kamu yang belum pernah diuji sampai ujung? Coba jalankan script di atas hari ini — hasilnya sering bikin kaget. 🐷

— Chokdi 🐷 · Content Studio · 2026
