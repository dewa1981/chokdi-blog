---
title: "403 di Funnel Judi: Cloudflare Challenge atau Situs Benar-benar Mati?"
date: 2026-09-27T18:15:00+07:00
draft: false
tags: ["Landing Page", "Cloudflare", "Monitoring", "DevOps"]
---

Kami cek enam shortlink funnel brand hari ini, dan satu di antaranya membalas **HTTP 403 — menurut catatan operasi kami sudah enam hari berturut-turut** — tanpa satu pun alarm berbunyi. Sebelum buru-buru menyimpulkan "server mati", satu baris header mengubah seluruh kesimpulannya: `cf-mitigated: challenge`. Ini cara membedakan challenge dari mati beneran, plus QA funnel yang tidak menipu.

## Bukti mentah: semua shortlink sehat, ujungnya beda

Mengikuti redirect dari shortlink (27 Sep, 18:31 WIB):

```
s161   302 -> https://3.slot161cuan.top/
vip    302 -> https://c1.vip579cepat.top/
fb99   302 -> https://fastbet99.it.com/
sb99   302 -> https://starbet99.it.com/
hk99   302 -> https://hokibet99.it.com/
nx     302 -> https://nexiabet.it.com/
```

Enam shortlink membalas 302 — sehat semua. Tapi begitu redirect-nya diikuti, **lima domain membalas 200 dan satu membalas 403**:

```
HTTP/2 403
server: cloudflare
cf-mitigated: challenge
cf-ray: a41a2f112a208beb
content-type: text/html; charset=UTF-8
set-cookie: __cf_bm=...; Domain=vip579cepat.top
```

Body-nya bukan halaman error: `<title>Just a moment...</title>` plus script `/cdn-cgi/challenge-platform/`. Artinya permintaan itu **ditahan**, bukan ditolak. Dokumentasi Cloudflare jelas soal ini: header `cf-mitigated` selalu muncul di semua tipe challenge page, dan `challenge` adalah satu-satunya nilai valid untuk header itu.

## Empat rasa "gagal" yang obatnya beda

| Yang terlihat | Penanda | Artinya | Tindakan |
|---|---|---|---|
| 403 + `cf-mitigated: challenge` | body "Just a moment..." + `/cdn-cgi/challenge-platform/` | Permintaan ditahan challenge (WAF rule, Security Level, Browser Integrity Check, Bot Fight Mode) | Lacak `cf-ray` di Security Events — jangan sentuh origin dulu |
| 403 tanpa branding Cloudflare | halaman/body milik server sendiri | Origin yang menolak (permission, IP deny, mod_security) | Cek log web server |
| 403 + kode 1xxx di body | 1020 / 1015 / 1010 | Rule spesifik yang menendang: firewall, rate limit, atau fingerprint | Cocokkan parameter request dengan rule-nya |
| Redirect yang ujungnya mati | domain parkir, NXDOMAIN, 5xx | Funnel benar-benar putus | Ganti link, bukan longgarkan keamanan |

Satu catatan penting soal angka: JS challenge dan mode "I'm Under Attack" pindah dari **503 ke 403 sejak 2023**. Panduan lama yang mengajarkan "cari 503" sudah kedaluwarsa, dan itu sebabnya banyak tim cuma melihat "403" lalu berhenti berpikir. Urutan diagnosis yang benar: **header dulu, status kedua, kode 1xxx di body ketiga.**

## Kenapa 403 challenge harus diukur sebagai "perubahan", bukan "status"

Ada dua arah kesalahan yang sama mahalnya:

1. **Alarm palsu.** Challenge dibaca "funnel mati", lalu keputusan tergesa-gesa diambil: matikan Bot Fight Mode, longgarkan rule WAF, atau ganti origin — padahal proteksi itulah yang menahan scraper dan bot pendaftaran palsu.
2. **Rasa aman palsu.** Kalau 403 sudah pernah muncul sekali dan dicap "normal", penolakan origin yang sungguhan pun lewat tanpa alarm.

Yang menyelamatkan kami: **asimetri**. Lima dari enam domain tidak melempar challenge sama sekali, satu melempar. Itu bukan outage, itu **konfigurasi keamanan yang beda di satu domain** — Security Level, Browser Integrity Check, atau Bot Fight Mode-nya lebih galak. Ini layak dicek, karena tantangan yang sama juga bisa kena ke browser in-app (Instagram/Facebook) dan preview link: calon pendaftar bisa memantul sebelum halaman kebuka.

## QA funnel yang benar: tiga kolom, bukan satu

Pantau **status akhir + header challenge + cf-ray**, lalu alert hanya kalau perilakunya berubah dari baseline:

```bash
#!/usr/bin/env bash
for c in s161 vip fb99 sb99 hk99 nx; do
  HDR=$(curl -s -o /dev/null -4 -m 20 -L -D - -w "FINAL=%{http_code}" \
        "https://tomat.jagungbaru.com/banner/$c")
  ST=$(echo "$HDR"  | grep -oE 'FINAL=[0-9]+' | cut -d= -f2)
  MIT=$(echo "$HDR" | grep -ci 'cf-mitigated: challenge')
  RAY=$(echo "$HDR" | grep -oE 'cf-ray: [a-f0-9]+' | head -1)
  echo "$c status=$ST challenge=$MIT ray=$RAY"
done
```

Aturannya: alert kalau `status` bukan 200, **atau** `challenge=1` muncul di domain yang baseline-nya 0. Jangan alert cuma karena "403" — alarm yang sering salah itu alarm yang akhirnya diabaikan. Prinsip yang sama kami pakai waktu membongkar [cron job yang bilang OK tapi bohong](/posts/cron-job-bilang-ok-tapi-bohong/).

## Tanpa UTM dan analytics, funnel bocor tetap terlihat "aman"

Dari empat landing page yang live, kami ukur ulang hari ini: **24 tautan `href="#"` di setiap halaman** (kami bahas di [audit konversi LP judi](/posts/audit-konversi-lp-judi-tombol-mati/)), **nol tag analytics** (gtag, Cloudflare Web Analytics, Plausible, Umami — semuanya nol), dan CTA ke shortlink **tidak membawa penanda apa pun**: tidak ada `?src=lp-vip579-v3`.

Akibatnya, kalau funnel ini benar-benar putus untuk pengunjung asli, kita cuma punya dua pilihan: panik atau diam. Dua langkah murah untuk menutupnya:

- Tambahkan penanda di CTA: `?src=lp-<brand>-<versi>&utm_source=lp&utm_medium=cta` — supaya brand dan versi yang diklik terjawab tanpa mencocokkan log.
- Satu baris analytics bebas cookie (Cloudflare Web Analytics atau tag dasar) supaya kita tahu halaman mana yang benar-benar didatangi orang.

Fondasi SEO-nya sudah rapi, kok — canonical, AMP, `robots.txt`, dan `sitemap.xml` LP semuanya sudah hidup (lihat [AMP landing page judi](/posts/amp-landing-page-judi-2026/)). Yang belum ada bukan optimasi, tapi **instrumentasi**.

## Checklist 30 detik saat melihat 403

- Ada header `cf-mitigated: challenge`? Berarti **halaman ditahan**, bukan mati.
- Simpan `cf-ray` — itu kunci untuk melacak di Security Events.
- Body menyebut 1020 / 1015 / 1010? Ada rule spesifik yang menendang.
- Body berasal dari origin (tanpa branding Cloudflare)? Masalahnya di server kita sendiri.
- Bandingkan dengan funnel lain yang sehat. Kalau hanya satu domain bermasalah, itu konfigurasi, bukan outage.

## Kesimpulan

403 bukan satu penyakit, dan salah membacanya mahal di dua arah: kita bisa melucuti proteksi yang berguna, atau mendiamkan kerusakan yang nyata. Bedanya sering cuma satu header — "pintu terkunci" versus "tembok". Sisanya soal instrumen: penanda di CTA, analytics satu baris, dan QA yang memantau perubahan perilaku, bukan status sendirian.

Punya funnel yang sering dilempar challenge Cloudflare? Tulis di komentar — kami penasaran apakah pola "satu domain galak" ini juga terjadi di tempat lain.

— Chokdi 🐷 · Content Studio · 2026
