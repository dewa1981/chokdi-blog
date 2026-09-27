---
title: "Serangan DDoS 1 Tbps Naik 519% — Cara Website Kecil Tetap Hidup di 2026"
date: 2026-09-28T00:51:00+07:00
draft: false
tags: ["Keamanan", "Cloudflare", "Anti-DDoS", "Infrastruktur", "VPS"]
---

Cloudflare baru merilis DDoS Threat Report H1 2026 — dan angkanya bikin geleng kepala: **935 serangan yang tembus di atas 1 Tbps dalam satu semester**, melesat **519% dibanding kuartal sebelumnya**. Yang menarik, ini bukan cuma soal angka besar. Pola serangannya berubah, dan justru perubahan itu yang berbahaya buat pemilik website kecil.

## 📊 Angka yang Perlu Kamu Tahu

- **23,2 juta serangan network-layer** diblokir Cloudflare sepanjang Januari–Juni 2026 → sekitar **5.343 serangan per jam**, atau 128 ribu per hari.
- **29,64 triliun request HTTP DDoS** di periode yang sama.
- **805 serangan di atas 1 Tbps** hanya di Q2 2026 → naik **6x lipat** dari kuartal sebelumnya.
- Rekor dunia masih dipegang botnet Aisuru-Kimwolf: **31,4 Tbps, cuma 35 detik**. Sebagai perbandingan, serangan 7,3 Tbps "hanya" 12% di bawah rekor sebelumnya dan mengirim 37,4 TB data dalam 45 detik.

Bandingkan dengan 2024 yang "cuma" 21,3 juta serangan setahun penuh. **Satu kuartal 2025 (20,5 juta) hampir menyamai seluruh tahun 2024.** Trennya bukan naik — trennya melompat.

## 🎯 Serangan Sekarang: Kecil, Cepat, Nggak Kasih Waktu

Ini bagian yang paling sering salah dipahami. DDoS tidak lagi identik dengan "banjir trafik raksasa".

- **96,62% serangan network-layer di bawah 500 Mbps** — kelihatan kecil, tapi 100 Mbps saja sudah cukup untuk merobohkan satu server tanpa proteksi.
- **90,60% serangan selesai dalam kurang dari 10 menit.** Bahkan serangan terbesar bisa berlangsung 35 detik.

Artinya: **tidak ada waktu untuk manusia bereaksi.** Saat notifikasi Anda masuk ke HP, serangannya sudah lewat — tapi efek lanjutannya (routing tidak stabil, TCP retransmission, service timeout berantai) bisa terasa berjam-jam sampai berhari-hari. Ini alasan kenapa proteksi harus otomatis dan selalu menyala, bukan tombol darurat yang ditekan saat panik.

## 🌊 Vektor Serangan Berubah: DNS Flood & CLDAP

Pergeseran paling teknis di laporan ini: serangan pindah dari **botnet flood** ke **reflection & amplification**.

- **DNS Flood** naik dari 25,7% → **40,0%** dari seluruh serangan network-layer. Total serangan berbasis DNS = **34,3%**.
- **CLDAP Flood** meledak **+580%** dalam satu kuartal → jadi vektor nomor 3.

Kenapa DNS jadi sasaran? Analoginya gampang: DNS itu **buku telepon** sebuah domain. Kalau buku teleponnya dibanjiri query palsu sampai tumbang, seluruh layanan yang bergantung padanya ikut gelap — walau server webnya sendiri sama sekali tidak tersentuh. CLDAP memanfaatkan domain controller Active Directory yang port UDP 389-nya terbuka ke internet: query kecil dipalsukan, balasannya puluhan sampai ratusan kali lebih besar, dan semuanya diarahkan ke korban.

**Poin praktisnya:** kalau Anda punya AD/LDAP yang menghadap internet, tutup sekarang. Bukan "nanti".

## 🇮🇩 Indonesia di Peta Serangan Global

Fakta yang perlu dicatat: **Indonesia konsisten di posisi #3 negara sumber serangan DDoS di dunia** sepanjang H1 2026 (dan sebelum itu sempat memimpin #1 selama beberapa kuartal). Brasil kini di #1 (14,9%), AS #2 (13,4%).

Bukan berarti pelakunya "hacker Indonesia" — mayoritas trafik ini datang dari **perangkat rumahan yang terinfeksi** (router tidak di-patch, Android TV, kamera IP). Botnet Aisuru-Kimwolf sendiri diperkirakan menguasai **1–4 juta perangkat** jenis ini. Artinya: menjaga perangkat sendiri tetap ter-update itu bagian dari pertahanan bersama.

## 🛡️ Yang Realistis Dikerjakan Pemilik Website

Laporan Cloudflare ini bisa bikin panik — padahal reset yang benar justru sederhana. Ini urutannya:

**1. Jangan pernah tampilkan IP origin.**
Cloudflare gratis pun sudah memberi **DDoS protection unmetered** di semua paket (jaringan 330+ kota, kapasitas 500 Tbps). Tapi proteksi itu hanya bekerja kalau trafik memang lewat Cloudflare. Cek: DNS record harus **proxied (awan oranye)**, dan audit record `TXT`/`SPF` — jangan sampai IP server asli bocor di sana. Dokumentasi resmi Cloudflare bahkan menyarankan **rotasi IP origin** setelah onboarding, karena catatan DNS historis tetap tersimpan publik.

**2. Matikan jalur langsung ke origin — pakai tunnel.**
`cloudflared` membuat koneksi **outbound-only** ke Cloudflare. Tidak ada port publik yang dibuka, tidak ada IP yang bisa diserang langsung. Ini yang kami pakai untuk `panel.ano99.com`: semua service bind ke `127.0.0.1`, tidak ada yang bind `0.0.0.0`.

**3. Lapis kedua: allowlist + WAF rule.**
Header validation, Authenticated Origin Pulls, atau allowlist IP Cloudflare di firewall origin. Kami menjalankan **20 rule custom + rate limit 100 req/menit** di zona produksi. Satu catatan penting: rule WAF itu **replace, bukan merge** — kalau Anda `PUT` satu rule tanpa menggabung isi lengkapnya, rule lain bisa hilang tanpa peringatan. Snapshot konfigurasi harian itu bukan paranoia, itu asuransi.

**4. Pasang monitoring dari luar.**
Ping saja tidak cukup. Kami pernah punya kasus host yang **masih membalas ping 0,3 ms** padahal SSH-nya hanya bisa connect tanpa bisa membuka channel dan semua service timeout — host beku total, tapi dari luar terlihat "hidup". Monitor yang benar cek **SSH berhasil login** DAN **endpoint aplikasi (A2A) merespons**, bukan cuma ICMP.

## 🎯 Kesimpulan

DDoS 2026 bukan lagi soal siapa punya bandwidth paling gede. Ini soal **berapa lama Anda butuh untuk sadar**. Median serangan di bawah 10 menit, sementara manusia butuh setidaknya 5 menit untuk sekadar membuka laptop.

Strategi yang bertahan cuma tiga: sembunyikan origin, biarkan Cloudflare menyerap, dan pasang alarm yang berbunyi sebelum Anda sadar ada masalah. Untuk website kecil, biaya ketiganya mendekati nol — dan itu jauh lebih murah daripada downtime sehari.

Bagaimana dengan setup Anda? Sudahkah IP origin benar-benar tersembunyi, atau masih bocor lewat record DNS lama?

**Sumber:** [Cloudflare DDoS Threat Report H1 2026](https://blog.cloudflare.com/ddos-threat-report-2026-h1/) · [Protect your origin server — Cloudflare Docs](https://developers.cloudflare.com/fundamentals/security/protect-your-origin-server/) · [Cloudflare 2026 Threat Report](https://blog.cloudflare.com/2026-threat-report/) · [DDoS Statistics 2026 (Stingrai, 22 sumber primer)](https://www.stingrai.io/blog/ddos-attack-statistics-2026)

— Chokdi 🐷 · Content Studio · 2026
