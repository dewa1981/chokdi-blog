---
title: "DDoS 1 Tbps Naik 519%: Cara Website Kecil Tetap Hidup Tanpa IP Publik"
date: 2026-09-28T09:20:00+07:00
draft: false
tags: ["Cloudflare", "Keamanan", "VPS", "Self-Hosted", "Infrastruktur"]
---

Cloudflare baru merilis **DDoS Threat Report H1 2026** — dan angkanya bikin merinding: **935 serangan DDoS di atas 1 Tbps** berhasil diredam cuma dalam enam bulan pertama 2026. Artinya lonjakan **+519% antar kuartal**. Pertanyaan besarnya untuk kita yang cuma punya VPS kecil: apa masih ada harapan?

Jawabannya: ada. Dan kabar baiknya, triknya **gratis** dan bisa dipasang malam ini.

## 📊 Angka yang Perlu Kamu Tahu

Mari lihat skala sebenarnya dari laporan resmi Cloudforce One (organisasi threat intelligence-nya Cloudflare):

- **23,2 juta** serangan network-layer dan **29,64 triliun** request HTTP di-redam sepanjang Januari–Juni 2026
- Kalau dirata-rata: **~5.343 serangan per jam**, atau **~128.000 per hari**
- April 2026 jadi bulan terpadat: **165 petabyte** trafik dalam sebulan
- Di Q2 saja, Cloudflare meredam **805 serangan di atas 1 Tbps** — naik **lebih dari 6x lipat** dari kuartal sebelumnya
- Rekor sepanjang masa masih dipegang serangan **31,4 Tbps** (November 2025) yang cuma berlangsung **35 detik**

Dua angka terakhir itu penting sekali, dan alasannya bukan yang kamu duga.

## ⚡ Masalahnya Bukan Besarnya — Tapi CEPATNYA

Ini bagian yang paling sering salah dipahami. Rata-rata serangan itu sebenarnya **kecil dan singkat**:

- **96,62%** serangan network-layer di bawah **500 Mbps**
- **90,60%** selesai dalam **kurang dari 10 menit**
- Bahkan serangan rekor 31,4 Tbps itu hanya bertahan **35 detik**

Sekarang renungkan: kalau serangannya cuma **100 Mbps** dan bertahan **5 menit**, apa yang terjadi pada VPS-mu?

VPS murah umumnya punya bandwidth 100 Mbps–1 Gbps. Serangan 100 Mbps saja sudah **cukup untuk melumpuhkan** server dan website. Dan karena semua selesai dalam hitungan detik sampai menit, **tidak ada waktu untuk intervensi manusia**. Saat notifikasi alert sampai ke HP-mu, serangannya sudah kelar — yang tersisa cuma layanan yang sudah mati dan butuh jam-jaman untuk pulih.

Kesimpulan pahitnya: **mitigasi manual dan solusi on-demand itu terlalu lambat.** Titik. Mau sekuat apa pun kamu jaga server, kalau masih mikir "nanti kalau kena baru saya blokir" — kamu sudah kalah sebelum mulai.

## 🛡️ Kenapa "Sembunyikan IP" Bukan Solusi

Banyak yang mikir solusinya adalah menyembunyikan IP atau pasang firewall ketat. Dua-duanya membantu, tapi keduanya punya lubang besar.

Firewall (ufw/iptables) memang memblokir port — tapi begitu kamu buka **port 80/443 untuk publik**, IP-mu terekspos. Dan IP yang terekspos bisa di-flood **langsung di level jaringan**. Firewall VPS-mu bekerja di kernel, tapi kernel tetap harus menerima paket itu dulu. Kalau bandwidth uplink-nya sudah habis dipakai paket sampah, berapa pun banyaknya rule iptables, **port-nya tetap tidak bisa diakses**.

Titik lemahnya bukan konfigurasi — tapi **IP publik itu sendiri**.

## 🔑 Solusinya: Cloudflare Tunnel (dan Kenapa Bekerja)

Di sinilah **Cloudflare Tunnel** masuk. Idenya sederhana tapi elegan: **jangan pernah buka port ke internet.**

```text
(INTERNET)                    CLOUDFLARE EDGE
 user → domain ─────────────► https + WAF + redam DDoS
                                  │  tunnel (outbound)
                                  ▼
                     cloudflared ──► service di 127.0.0.1
                     (VPS: TIDAK ada port terbuka)
```

Cara kerjanya:

1. `cloudflared` di VPS-mu buka koneksi **outbound** ke edge Cloudflare — tidak ada satu pun port inbound yang dibuka
2. Trafik user masuk ke Cloudflare Edge, bukan ke VPS-mu
3. Edge menyaring, menantang, dan meredam serangan **sebelum** menyentuh servermu
4. Cuma request yang valid yang diteruskan lewat tunnel ke service di `127.0.0.1`

Hasilnya: penyerang **tidak tahu IP-mu**, dan tidak ada pintu untuk ditendang. Serangan 1 Tbps berhenti di jaringan Cloudflare yang punya **kapasitas 500 Tbps di 330+ kota** — bukan di VPS 4 GB punya kamu.

## ⚙️ 5 Langkah Praktis (Terbukti di Lapangan)

Ini yang kami pakai sendiri untuk host panel, blog, dan landing page kami:

1. **Bind semua service ke `127.0.0.1`**, jangan `0.0.0.0`. Kalau aplikasinya bind ke semua interface, dia tetap bisa dijangkau dari dalam — dan kalau ada salah konfigurasi, dari luar juga.
2. **Install `cloudflared`** dan buat tunnel dari dashboard Cloudflare (config remote). **Pakai config remote**, jangan bikin dua konfigurasi lokal yang saling bertabrakan dengan unit `cloudflared` yang sudah jalan.
3. **Buka HANYA SSH untuk admin** — dan kalau bisa jangan port 22 publik. Pakai port non-standar (mis. `22022`) yang dibatasi hanya dari IP admin atau jaringan private seperti Tailscale.
4. **Jangan pernah aktifkan port forward 80/443** di router atau firewall VPS. Kalau `ufw` masih membuka 80/443 publik, tunnel-nya jadi tidak ada gunanya.
5. **Firewall tetap nyala** sebagai lapisan kedua: default deny inbound, izinkan cuma SSH terbatas + egress yang dibutuhkan (`cloudflared` butuh TCP 443 dan UDP 7844 keluar).

## 🧩 Bonus: Cloudflare Workers sebagai Perisai Tambahan

Kalau mau lebih aman lagi, **Cloudflare Workers** bisa jadi lapisan depan sebelum trafik masuk ke origin kamu:

- **Filter bot** di edge — cek User-Agent, header, dan pola request sebelum diteruskan
- **Rate limiting** per IP supaya satu klien tidak bisa menyerbu berulang
- **Redirect terkontrol** — domain publik menunjuk ke Worker, Worker yang meneruskan ke origin lewat tunnel, jadi struktur aslinya tersembunyi
- **WAF Rules** — blokir pola serangan yang jelas sampah di level edge, hemat bandwidth dan CPU origin

Ini pola yang kami pakai berlapis: **Cloudflare Edge → Worker → Tunnel → service loopback**. Tiga lapisan yang semuanya gratis di tier basic.

## ⚠️ Tiga Jebakan yang Sering Kena

Berdasarkan pengalaman langsung, ini yang paling sering bikin setup tunnel gagal:

- **Domain "nyangkut" challenge.** Kalau situsmu balas `403` dengan header `cf-mitigated: challenge`, itu **bukan tanda situsmu mati** — itu Cloudflare sedang menantang bot. Sering salah diagnosis jadi "server down" padahal cuma curl dari IP datacenter yang ditantang. Cek header dulu sebelum panik.
- **Lupa bedakan "block" vs "challenge".** Bot challenge dan IP block punya gejala mirip tapi penyebab beda total. Untuk automation, jangan andalkan browser — pakai fetch lewat Worker atau search API.
- **Menyembunyikan IP tapi tetap buka port 80/443.** Ini kesalahan paling fatal. Kalau port-nya terbuka, penyerang tinggal scan dan tembak langsung, tunnel-mu jadi hiasan.

## 💡 Kesimpulan

Laporan H1 2026 itu pesannya jelas: **hyper-volumetric DDoS bukan lagi ancaman perusahaan besar.** Lonjakan +519% dan rekor 935 serangan di atas 1 Tbps per semester artinya ini sudah jadi "cuaca normal" di internet.

Tapi kabar baiknya, kamu tidak perlu kapasitas 500 Tbps untuk bertahan. Yang kamu butuhkan cuma **berhenti membuka pintu**. Cloudflare Tunnel + bind ke loopback + firewall ketat = kombinasi gratis yang membuat VPS 4 GB-mu setangguh infra besar — karena serangan tidak pernah sampai ke pintunya.

**Mulai dari mana?** Cek dulu VPS-mu: apakah port 80/443 masih terbuka ke publik? Kalau ya, itu pekerjaan rumah pertama malam ini.

Kalau kamu sudah pakai tunnel buat self-hosting, gimana pengalamanmu — ada masalah dengan IPv6 atau WebSocket? Tulis di komentar, kita bahas.

## 📚 Sumber

- [Cloudflare DDoS Threat Report H1 2026](https://blog.cloudflare.com/ddos-threat-report-2026-h1/)
- [Cloudflare 2025 Q4 Report — rekor 31,4 Tbps](https://blog.cloudflare.com/ddos-threat-report-2025-q4/)
- [Help Net Security — analisis tren H1 2026](https://www.helpnetsecurity.com/2026/08/13/cloudflare-h1-2026-ddos-trends-report/)

— Chokdi 🐷 · Content Studio · 2026
