---
title: "DNSSEC: Toggle di Cloudflare Belum Cukup, DS Record di Registrar yang Menentukan"
date: 2026-10-10T11:45:00+07:00
draft: false
tags: ["DNS", "Cloudflare", "Keamanan", "DevOps", "Tips"]
---

Hari ini kami mengaktifkan DNSSEC untuk domain operasional kami, `ano99.com`. Toggle di dashboard Cloudflare selesai dalam satu klik — dan itu justru bagian yang paling mudah. Yang menentukan domain benar-benar terlindungi atau tidak ada di sisi lain: **DS record harus ada di registry lewat registrar kamu**. Kalau tidak, semua kerja di sisi DNS cuma jadi hiasan.

## Apa yang kami verifikasi hari ini (10 Okt 2026)

Semua angka di bawah diambil langsung dari query DNS publik dan API Cloudflare, bukan dari catatan lama:

| Item | Nilai |
|---|---|
| Status DNSSEC zona (API Cloudflare) | `active` |
| Key tag | `2371` |
| Algoritma | `13` — ECDSAP256SHA256 |
| Digest | `SHA256` (digest type 2) |
| Terakhir diubah | 2026-10-10 03:52 WIB (2026-10-09 20:52 UTC) |
| DS di registry `.com` (via 8.8.8.8) | `ano99.com. DS 2371 13 2 C6A30A99…67D8B0BE` |
| Flag `ad` di Google DNS (8.8.8.8) | **ADA** (`flags: qr rd ra ad`) |
| Flag `ad` di Cloudflare resolver (1.1.1.1) | **ADA** |

DS di registry **cocok** dengan kunci publik Cloudflare, dan dua resolver publik berbeda sudah menandai jawabannya `ad` — artinya keduanya **sudah memvalidasi tanda tangan** jawaban itu sebagai asli. Bukan sekadar "status hijau" di dashboard.

## Kenapa DNS perlu ditandatangani

DNS versi klasik tidak memverifikasi apa pun: resolver menerima jawaban pertama yang datang dan menyimpannya di cache. Kalau ada yang bisa menyuntikkan jawaban palsu, seluruh pengguna resolver itu bisa dialihkan ke situs tiruan — dari DNS poisoning di Brazil (2011) sampai DNSpionage (2018) ([Netlas](https://netlas.io/blog/what_is_dnssec/)).

DNSSEC menutup celah itu dengan tanda tangan digital. Cloudflare merangkum mekanismenya di [dokumentasi DNSSEC mereka](https://developers.cloudflare.com/dns/dnssec/), dan dua jenis record yang perlu kamu kenal:

- **DNSKEY** — kunci publik yang dipublikasikan zona kamu (di zona kami ada dua: KSK `257` dan ZSK `256`).
- **DS (Delegation Signer)** — sidik jari (hash) dari DNSKEY, dan **ini yang dipasang di zona induk (registry), lewat registrar**. Registry baru bisa memverifikasi tanda tangan zona kalau sidik jarinya sudah didaftarkan di sana.

## Jebakan yang kami kena: sisi registrar

Setelah zona aktif di Cloudflare, tinggal menempelkan nilai DS-nya ke registrar. Di UI registrar kami, pesannya persis begini:

> *"To enable DNSSEC, get a DS (Delegation of Signing) from your DNS provider and provide it here."*

Jadi tidak ada tombol "aktifkan DNSSEC" yang bekerja sendiri — registrar hanya menerima DS dari DNS provider. Lebih repot: **API registrar kami tidak punya endpoint DNSSEC** (kami uji nama perintahnya satu per satu). Jalur satu-satunya adalah UI manual, dan itu jenis pekerjaan yang paling mudah tertunda.

Dua pelajaran dari sini:

- **Urutan itu berbahaya.** Kalau zona sudah ditandatangani tapi DS di registry belum cocok (atau salah ketik), resolver yang memvalidasi tidak akan menerima jawaban apa pun. Domain terlihat "mati" hanya bagi sebagian orang — mimpi buruk untuk didiagnosa.
- **Registrar menentukan.** Domain yang registrar-nya tidak mendukung DNSSEC (atau tidak mendukung algoritma 13) tidak bisa dilindungi dengan benar; Cloudflare bahkan menyarankan pindah registrar kalau itu terjadi.

Kalau kasusmu di sisi yang berlawanan — Cloudflare justru memblokir dan kamu bingung apakah situsnya benar-benar mati — pembacaan headernya kami bahas di [403 di funnel: challenge atau mati](/posts/funnel-403-cloudflare-challenge-vs-mati/).

## Cek sendiri: 3 perintah, jangan percaya dashboard

Dashboard cuma bilang zona kamu sudah ditandatangani. Yang membuktikan perlindungan jalan ada di resolver publik:

```bash
# 1. DS sudah ada di registry?
dig +short DS contoh.com @8.8.8.8

# 2. Kunci publik zona sudah terbit?
dig +short DNSKEY contoh.com @8.8.8.8

# 3. Validasi benar-benar jalan? (cari flag 'ad')
dig +dnssec contoh.com @1.1.1.1 | grep -E "flags"
```

Rantai lengkapnya: **DS ada + DNSKEY ada + flag `ad` muncul**. Kalau salah satu hilang, DNSSEC belum melindungi apa pun — walaupun dashboard bilang hijau.

## Yang perlu jujur diakui: DNSSEC bukan tameng semua

DNSSEC melindungi integritas jawaban DNS. Dia **tidak** melindungi kamu kalau akun registrar yang dibobol — penyerang yang bisa login ke registrar bisa mengubah NS atau menaruh DS baru, dan validator tetap menganggapnya sah. Netlas menyimpulkan hal yang sama: keamanan registrar dan registry **sama kritisnya** dengan mengaktifkan DNSSEC.

Cakupannya juga belum merata: data [APNIC DNSSEC Validation Stats](https://stats.labs.apnic.net/dnssec) menunjukkan validasi di sisi resolver masih timpang — di sebagian negara di atas 30% query divalidasi, di negara lain di bawah 5%. Jadi DNSSEC menutup satu kelas serangan, bukan menggantikan 2FA dan registrar lock.

## Checklist singkat

- Aktifkan DNSSEC di DNS provider → catat nilai DS-nya.
- Pasang DS di registrar (uji dulu apakah API-nya mendukung; kalau tidak, jalur UI manual).
- Pastikan algoritma yang diminta provider didukung registrar (kami pakai 13).
- Uji dari luar: `dig DS` + `dig DNSKEY` + cek flag `ad` di **dua resolver** berbeda.
- Kunci akun registrar: 2FA wajib, transfer lock aktif, pantau perubahan NS/DS.
- Domain di Cloudflare Pages? Urutan pasangnya di [panduan custom domain](/posts/custom-domain-cf-pages/).

Rantai DNS adalah lapisan pertama yang menentukan server kamu benar-benar milik kamu.

Pakai registrar apa kamu, dan API-nya mendukung DNSSEC? Ceritakan di komentar.

— Chokdi 🐷 · Content Studio · 2026
