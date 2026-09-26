---
title: "Komari: Monitor Server Ringan 6.255 Bintang, Tapi Agent-nya Juga Remote Shell"
date: 2026-09-26T18:05:00+07:00
draft: false
tags: ["Server", "Monitoring", "Self-Hosted", "Keamanan"]
---

Kalau kamu punya lebih dari tiga VPS, dashboard monitoring bukan lagi barang mewah — tapi nebeng layanan pihak ketiga bikin data server kita numpang di tempat orang. Komari muncul jadi jawaban: panel monitoring self-hosted, satu binary Go, agent super ringan. Sampai September 2026 repo-nya sudah **6.255 bintang dan 764 fork**, dengan rilis terbaru **1.5.1 (24 September 2026)** dan cuma **1 open issue** — angka yang jarang dimiliki proyek satu orang. Tapi ada satu hal yang wajib kamu tahu sebelum pasang: agent Komari bukan cuma pelapor metrik, dia juga **eksekutor perintah**.

## Kenapa Komari Naik Cepat

| Data | Nilai |
|---|---|
| Bahasa | Go (binary tunggal) |
| Lisensi | MIT |
| Bintang / Fork | 6.255 / 764 |
| Rilis terbaru | 1.5.1 — 24 Sep 2026 |
| Issue terbuka | 1 |

Yang bikin betah bukan angkanya, tapi alurnya:

- **Interval 1 detik** — CPU, RAM, disk, network, ping kelihatan hampir real-time.
- **Agent ringan** — proses kecil, cocok buat VPS 1 GB yang dipakai proxy atau bot.
- **Auto-discovery** — puluhan node bisa masuk tanpa isi token satu-satu.
- **Tema & plugin** — tampilan bisa diganti, API-nya terbuka buat integrasi sendiri.
- **Jalan di Linux dan Windows** — termasuk server yang bukan cuma buat web.

## Jebakan 1: Agent-nya Adalah Control Channel Dua Arah

Ini bagian yang wajib dibaca dua kali. Riset Huntress (April 2026) menemukan Komari dipakai di intrusi nyata sebagai command-and-control. Bukan karena di-*weaponise*, tapi karena **kemampuannya aktif dari default**: agent membuka WebSocket persisten ke server, lalu menerima tiga jenis event dari server — `exec` (jalankan perintah PowerShell/sh), `terminal` (reverse shell PTY interaktif di browser), dan `ping` (ICMP/TCP/HTTP). Flag `--disable-web-ssh` sifatnya **opt-in**, jadi kalau tidak dipasang, remote shell-nya hidup.

Di kasus itu, penyerang memasang agent Komari sebagai Windows service bernama "Windows Update Service" lewat NSSM, dan installer-nya diambil langsung dari repo resmi GitHub — pola yang oleh Huntress disebut *"C2 living off the trust of GitHub"*. Tidak perlu infrastruktur penyerang sendiri; cukup percaya pada GitHub.

Kalau kamu pakai Komari untuk diri sendiri, tiga hal ini murah dan bukan opsional: pasang agent dengan `--disable-web-ssh`, jangan pernah expose panel ke internet tanpa auth (pakai reverse proxy + OAuth/WAF), dan perlakukan token agent seperti password root — bocor satu token, satu server ikut.

## Jebakan 2: Cloudflare Nge-cache WebSocket → Dashboard Blank

Ini jebakan yang bikin kami sendiri berjam-jam salah diagnosa. Gejalanya khas: **semua card 0% dan offline selamanya**, padahal `docker logs` penuh `200 POST /api/clients/v2/rpc` dan jumlah baris di `metrics.db` terus naik. Server sehat, agent sehat, dashboard bodoh.

Akar masalahnya bukan aplikasi, tapi edge. Saat panel dipasang di belakang Cloudflare, respons `/api/rpc` ikut **di-cache 4 jam** (`cache-control: max-age=14400`). Browser membuka `new WebSocket(...)` ke path itu, tapi yang diterima balik bukan `101 Switching Protocols` — melainkan 200 hasil cache. Socket tidak pernah jadi, jadi UI tidak pernah dapat data live.

Cara membuktikan dalam satu perintah:

```bash
curl -s -i --http2 \
  -H 'Upgrade: websocket' -H 'Connection: Upgrade' \
  -H 'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==' \
  -H 'Sec-WebSocket-Version: 13' https://panel-kamu.domain/api/rpc
```

Kalau hasilnya `HTTP/2 200` (bukan 101) **dan** ada `cf-cache-status: HIT`, itu cache — bukan bug Komari.

Perbaikannya ada di **Caching → Cache Rules**, hostname panel + URI path starts with `/api` → **Bypass cache**, lalu Purge Everything. Yang bikin banyak orang tersesat: kalau "bypass"-nya dibuat di **Security → WAF** dengan action *Skip*, **cache-nya tidak ikut di-bypass** — rule-nya tercatat aktif tapi match-nya nol. WAF dan cache itu dua fase yang berbeda.

## Jebakan 3: WAF Memblokir Agent, Bukan Cuma Browser

Agent mengirim data dari IP datacenter — persis tipe trafik yang paling dicurigai Cloudflare. Hasilnya 403 challenge dan node tampak offline. Perlu satu custom rule WAF dengan action **Skip** untuk path `/api` dan `/report`. Kalau `/login` juga 403 padahal `curl http://127.0.0.1:<port>/login` dari server sendiri balas 200, lebarkan rule-nya ke semua path host itu — jangan sentuh aplikasinya dulu.

## Jebakan 4: Protokol Agent dan Key Auto-Discovery

Dua hal kecil yang bikin kamu begadang:

1. **Protokol v1 vs v2.** Komari 1.4.2 hanya melayani WebSocket v1, sementara agent baru default-nya v2. Gejalanya: agent melapor 200, tapi data tidak pernah masuk. Di seri 1.5.x protokol sudah bisa ditukar, tapi kalau kamu masih di versi lama, paksa `--protocol-version 1` di service file agent.
2. **Key auto-discovery harus JSON-quoted.** Value-nya disimpan di tabel `configs` dan wajib berbentuk `"AD-xxxxx"` **termasuk tanda kutip**. Tanpa kutip, agent balas 500 dan bilang kunci tidak valid.

## Kebiasaan yang Bikin Bisa Tidur

- Backup **dua** database (`komari.db` + `metrics.db`) sebelum update apa pun — ini aturan yang paling sering dilanggar saat panik.
- **Jangan edit SQLite saat container hidup.** Update kecil kadang lolos, tapi insert/DDL gampang bikin skema korup dan dashboard blank.
- Kalau dashboard blank, restart container dulu — jangan langsung bongkar database.
- Satu instance untuk satu kepemilikan. Jangan campur node project pribadi dengan node kerjaan; sekali tercampur, izin aksesnya ikut tercampur.
- Update hanya kalau ada kebutuhan. Monitoring yang jalan dan membosankan lebih berharga daripada monitoring versi terbaru yang rusak.

## Kesimpulan

Komari layak dicoba: ringan, self-hosted, dan datanya milik sendiri. Tapi dia bukan alat pasif. Perbedaan antara "alat monitoring" dan "pintu belakang" di sini cuma satu flag yang sengaja tidak dinyalakan secara default — jadi nyalakan sendiri. Pasang di belakang proxy ber-auth, matikan web terminal, dan taruh cache rule di tempat yang benar.

Kalau kamu pernah kena dashboard monitoring yang diam-diam kosong, baca juga [penyebab website down yang sering salah didiagnosa](/posts/5-penyebab-website-down/) dan [kenapa alarm palsu bikin alarm asli diabaikan](/posts/alarm-palsu-bikin-alarm-asli-diabaikan/). Sumber: [repo Komari](https://github.com/komari-monitor/komari), [dokumentasi Komari](https://www.komari.wiki/), dan [riset Huntress tentang penyalahgunaan agent Komari](https://www.huntress.com/blog/komari-c2-agent-abuse). Ada cerita monitoring sendiri? Tulis di komentar.

— Chokdi 🐷 · Content Studio · 2026
