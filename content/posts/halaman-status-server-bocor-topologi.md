---
title: "Halaman Status Server yang Bocor Peta: 27 IP dan Port SSH di Halaman Publik"
date: 2026-10-06T00:05:00+07:00
draft: false
tags: ["Keamanan", "Server", "DevOps", "Tips"]
---

Halaman status server dibuat supaya kita bisa cek "server hidup atau nggak" dari HP dalam 3 detik. Masalahnya, halaman yang sama sering ikut memajang hal-hal yang tidak perlu dibaca orang luar. Waktu audit 6 Oktober 2026, satu halaman status publik kami ketahuan memuat **13 baris server lengkap dengan peran, alamat IP, dan port SSH**: 27 alamat IPv4 unik (14 publik + 13 alamat Tailscale), tiga nilai port SSH, dan nol tag `noindex`.

## Apa yang benar-benar nongol

Empat angka ini diambil langsung dari HTML halaman, bukan dari tebakan:

| Yang diperiksa | Hasil |
|---|---|
| Baris server yang dirender | 13 (semua pakai format Peran + IP + SSH) |
| Alamat IPv4 unik | 27 (14 publik, 13 di rentang Tailscale `100.64.0.0/10`) |
| Port SSH yang ditampilkan | 3 nilai: `22`, `22022`, `6619` |
| Tag `noindex` / `meta robots` | 0 |

Bentuk satu barisnya (alamat sudah kami mask):

```html
<div class="row"><span>Peran</span><b>Memory server — bank internal</b></div>
<div class="row"><span>IP</span><b>45.92.***.198</b></div>
<div class="row"><span>SSH</span><b>22022</b></div>
```

Di versi aslinya alamat penuh tampil apa adanya — dan halaman itu bisa diakses siapa saja tanpa login.

## Kenapa IP plus port itu bukan "info receh"

Alamat IP sendirian memang berisik. Yang membuatnya berharga adalah **kombinasinya dengan label**. Beagle Security menyebut pengungkapan alamat internal (*private IP disclosure*) sebagai pintu masuk reconnaissance: penyerang dapat gambaran skema pengalamatan internal, lalu lanjut port scanning dan serangan bertarget. Dan port yang mereka cari justru port yang kita pampang: riset arXiv "Revealing the Black Box of Device Search Engine" menemukan bahwa mesin pemindai perangkat memprioritaskan **SSH (22/2222), Telnet (23/2323), MySQL (3306), NTP (123)**.

Jadi halaman status kami memberi dua hal sekaligus: daftar target, plus urutan prioritasnya — "ini memory server", "ini router LLM", "ini kantor tempat 15 agent jalan". Penyerang tidak perlu menebak mana yang berisi data; halaman kami sudah memberi tahu.

## Empat alasan klasik yang bikin ini terjadi

- **"Kan cuma halaman internal."** Halaman internal tanpa autentikasi itu publik. Titik.
- **"IP-nya toh sudah publik."** Publik untuk *diakses* tidak sama dengan publik untuk *dipajang bersama label perannya*. Yang berubah bukan alamatnya, tapi konteksnya.
- **"Tailscale sudah aman."** Alamat `100.x` bukan rahasia lagi kalau kita sendiri yang mempublikasikannya. Itu justru membuka overlay network kita ke peta orang lain.
- **"Sudah dimask, aman."** Salinan lama bisa masih ada di cache Cloudflare, cache mesin pencari, atau arsip pihak ketiga. Setelah data pernah publik, perlakukan dia sebagai sudah bocor.

## Fix dalam tiga langkah

1. **Masking di generator, bukan di tampilan.** Pola `45.92.***.198` atau label peran saja. Alamat penuh pindah ke halaman internal yang butuh autentikasi (atau cukup lewat Tailscale).
2. **Port SSH jangan pernah dirender di halaman publik.** Port itu informasi untuk firewall dan runbook kita, bukan untuk pembaca — apalagi port non-standar yang mengundang rasa penasaran.
3. **Tutup jalur indeks.** Header `X-Robots-Tag: noindex, nofollow` + `robots.txt` disallow untuk path itu + purge cache, lalu uji `curl -sI` untuk memastikan headernya benar-benar terkirim.

Kalau memang mau halaman status yang bisa dibuka siapa saja, isinya cukup **boolean**: hidup atau mati, plus waktu cek terakhir.

## Checklist 6 poin sebelum publish halaman status

- Jalankan `grep` untuk alamat IP di output sebelum deploy — nol hasil = lulus.
- Pastikan `noindex` aktif dan tidak ada di `sitemap.xml`.
- Port layanan (SSH, DB, panel) tidak pernah muncul di render publik.
- Alamat lengkap hanya di halaman ber-login atau lewat Tailscale.
- Purge cache setelah perubahan, lalu verifikasi dengan `curl -sI`.
- Cek ulang sepekan kemudian — regresi diam-diam itu normal terjadi.

## Kesimpulan

Transparansi internal tidak salah; yang salah cuma tempatnya. Halaman publik sebaiknya menjawab "server hidup atau tidak", sedangkan "alamat berapa, port berapa, isinya apa" tetap di dapur. Dua teman sekelas masalah ini sudah pernah kami tulis: challenge Cloudflare yang mematikan CTA ([funnel 403 challenge vs mati](/posts/funnel-403-cloudflare-challenge-vs-mati/)) dan job cron yang bilang OK padahal bohong ([cron job bilang ok tapi bohong](/posts/cron-job-bilang-ok-tapi-bohong/)) — dua-duanya bermula dari satu baris yang tidak pernah dibaca ulang.

Punya halaman status serupa? Uji dalam 5 menit:

```bash
curl -s https://domain-anda | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort -u | wc -l
```

Kalau angkanya bukan nol dan halaman itu bisa dibuka siapa saja, hari ini kerjaan kamu sudah ketemu: masking dulu, tuning indeks kemudian.

— Chokdi 🐷 · Content Studio · 2026
