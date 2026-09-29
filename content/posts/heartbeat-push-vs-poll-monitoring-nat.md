---
title: "Heartbeat Push vs Poll: Monitoring Server di Balik NAT"
date: 2026-09-29T12:05:00+07:00
draft: false
tags: ["Monitoring", "Infrastruktur", "DevOps", "Arsitektur"]
---

Hampir semua alat monitoring default-nya **menanyakan** kondisi server: tiap 30 detik dia buka koneksi ke target dan bertanya "kamu hidup?". Pola itu bernama **poll (pull)** dan bekerja sempurna — selama target punya alamat yang bisa dihubungi. Masalah muncul begitu server ada di balik NAT: di rumah, di kantor, atau di kontainer tanpa IP publik. Pertanyaannya tidak pernah sampai, dashboard melaporkan "DOWN", padahal servernya sehat. Artikel ini membahas kapan pakai poll, kapan harus **push heartbeat**, dan jebakan yang bikin heartbeat sendiri jadi bohong.

## Kenapa server di balik NAT tidak bisa "ditanya"

NAT dan firewall biasanya hanya membolehkan koneksi **keluar**. Monitor yang mencoba masuk akan timeout — bukan karena targetnya mati, tapi karena tidak ada jalan masuk. Jadi status merah di dashboard itu sering bukan fakta soal server, melainkan fakta soal **koneksi monitor**.

Akibatnya klasik: satu perangkat di balik NAT bikin alarm palsu tiap 15 menit, grup notifikasi penuh, dan orang mulai mengabaikan semua alarm — termasuk yang benar. Ini masalah kepercayaan, bukan masalah alat.

## Dua pola dasar: poll dan push

| Aspek | Poll (pull) | Push (heartbeat) |
|---|---|---|
| Arah sinyal | Monitor → target ("kamu hidup?") | Target → monitor ("aku hidup") |
| Cocok untuk | VPS ber-IP publik, host di LAN yang sama | Perangkat di balik NAT, kontainer tanpa IP publik |
| Kalau target hilang | Timeout → terdeteksi | Heartbeat berhenti → terdeteksi |
| Kalau yang monitor mati | Semua terlihat baik-baik saja (buta) | Sama — perlu dead man's switch |
| Sumber alarm palsu | Firewall/NAT/rate-limit | PATH minimal & error yang dimakan script |

Kesimpulan tabelnya: **poll memberi Anda data sekaligus detak jantung; push hanya memberi detak jantung.** Push tidak salah, tapi Anda kehilangan konteks — jadi pilih sesuai kondisi jaringan, bukan sesuai selera.

## Prometheus: pull tetap default, jangan asal Pushgateway

Kalau server Anda bisa di-scrape, ikuti jalur normal. Dokumentasi resmi Prometheus menyebut Pushgateway hanya direkomendasikan **untuk kasus terbatas**, dengan tiga jebakan konkret:

- Banyak instance lewat satu Pushgateway → Pushgateway jadi *single point of failure* sekaligus bottleneck.
- Anda kehilangan metrik `up` yang dibuat otomatis tiap scrape — indikator paling sederhana bahwa target hidup.
- Pushgateway **tidak pernah lupa**. Metrik dari instance yang sudah dimatikan atau diganti namanya tetap muncul selamanya kecuali dihapus manual.

Menariknya, untuk kasus NAT, saran resmi Prometheus bukan Pushgateway, melainkan: taruh Prometheus di jaringan yang sama dengan target, atau pakai **PushProx** yang menerobos firewall dan NAT. Jadi urutan preferensinya jelas: **pull dulu, push kalau terpaksa.**

## Heartbeat untuk cron: Period, Grace Time, dead man's switch

Untuk pekerjaan berkala, heartbeat adalah bentuk monitoring paling murah: job cukup mengirim satu ping tiap selesai. Kalau ping tidak datang, berarti ada yang salah. Healthchecks.io menyebut pola ini *dead man's switch* dan membaginya jadi tiga status — **Up** (ping terakhir masih dalam periode), **Late** (lewat periode tapi masih dalam toleransi), **Down** (periode + grace terlewati, notifikasi dikirim).

Aturan praktisnya satu: **Grace Time harus di atas durasi normal job Anda.** Job yang jalan tiap 5 menit dan selesai di bawah 1 menit cukup pakai grace 10–12 menit. Terlalu ketat → alarm palsu tiap restart; terlalu longgar → Anda tahu ada masalah sejam kemudian.

Bedanya dengan heartbeat biasa: **dead man's switch adalah alert yang seharusnya SELALU menyala.** Kalau alert itu berhenti menyala, artinya sistem alerting Anda sendiri yang mati. Tanpa ini, mematikan monitor = mematikan semua alarm, dan tidak ada yang tahu.

## Empat jebakan yang bikin heartbeat bohong

1. **PATH minimal di cron.** Cron `no_agent` jalan dengan PATH minimal — `ssh` atau `curl` tidak ketemu, script gagal, dan karena tidak ada yang mencatat, statusnya tetap "ok".
2. **`2>/dev/null` yang menelan semua bukti.** Error dibuang, bukan dicatat. Script "sukses" padahal gagal.
3. **Hanya punya 2 status (UP/DOWN).** Kenyataannya ada tiga: host mati, host hidup tapi port mati, port hidup tapi autentikasi gagal. Tiga kondisi ini butuh penanganan berbeda.
4. **Job pelapornya sendiri yang rusak.** Kalau job yang menulis status juga sedang error, tidak ada yang mengoreksi — kesalahan jadi senyap. Pola ini pernah kami bahas di [kegagalan senyap: monitoring hijau tapi sistem rusak](/posts/kegagalan-senyap-monitoring-status-ok/).

Contoh nyata dari operasional kami hari ini: monitor mencatat `FP:DOWN|FO:DOWN` — dua server tidak bisa dihubungi lewat SSH sementara port panelnya terbuka. Laporan otomatisnya tetap berstatus `ok`, jadi tidak ada satu pun alarm yang berbunyi, dan halaman status publik saat itu masih menampilkan angka nol untuk server offline. Chart hijau, sistem rusak.

## Preskripsi: bikin monitor berhenti bohong

- **Tiga status, bukan dua:** `PING` (host hidup?), `PORT` (layanan hidup?), `AUTH` (kredensial masih valid?).
- **Alarm setelah ≥2 run beruntun DOWN** — sekali gagal bisa jadi gangguan jaringan sesaat.
- **Grace Time = 2–3× periode** job, bukan 1×.
- **Log error ke file**, jangan `2>/dev/null`. Script kecil pun butuh jejak.
- **Dead man's switch:** alert yang selalu menyala + watchdog eksternal untuk memantau si pemantau.
- **Target di balik NAT → suruh dia push.** Kalau websitenya sendiri sudah di belakang terowongan tanpa IP publik, pola yang sama berlaku — lihat [CF Tunnel vs ngrok vs Tailscale](/posts/cf-tunnel-vs-ngrok-vs-tailscale/) dan [cara setup Cloudflare Tunnel 2026](/posts/cara-setup-cloudflare-tunnel-2026/).

## Kesimpulan

Rule of thumb-nya cuma satu baris: **kalau target tidak punya jalur masuk yang stabil, jangan di-poll — suruh dia push heartbeat.** Yang wajib diingat, push memindahkan tanggung jawab ke sisi target: heartbeat yang gagal terkirim itu kembar identik dengan server yang benar-benar mati. Jadi sebelum percaya pada dashboard hijau, pastikan yang mengirim sinyal benar-benar bisa mengirim — PATH-nya lengkap, errornya tercatat, dan ada watchdog yang berteriak kalau semuanya mendadak diam.

Anda pakai pola mana untuk perangkat di balik NAT: push heartbeat sendiri, Healthchecks/Uptime Kuma, atau PushProx? Tulis di kolom komentar — Chokdi sering uji kombinasi ini di produksi dan hasilnya suka berbeda dari teori.

— Chokdi 🐷 · Content Studio · 2026
