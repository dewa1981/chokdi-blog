---
title: "Server Hidup tapi Internet Mati: Jebakan Exit Node Tailscale Tanpa IP Masquerading"
date: 2026-09-26T00:06:00+07:00
draft: false
tags: ["Jaringan", "Tailscale", "DevOps", "Tutorial"]
---

Ada jenis gangguan yang paling menipu di dunia server: **mesinnya hidup, prosesnya jalan, tapi tidak bisa keluar ke internet sama sekali.** Ping dari luar gagal, port SSH ketutup, dan monitor berteriak "SERVER DOWN" — padahal servernya baik-baik saja, yang rusak cuma jalannya. Kami kena persis kasus ini dan butuh 86 menit untuk membongkarnya.

## Gejala: Seperti Server Mati, Tapi Bukan

Semuanya mulai dari alert yang diulang-ulang: health check balas `HTTP 000`, host tidak bisa dijangkau. Kalau dipercaya mentah-mentah, kesimpulannya "server mati". Tiga pemeriksaan pertama langsung membantah itu:

- `ping` ke IP publik server → **100% packet loss**
- Port SSH `22022` → **CLOSED**
- `curl` ke endpoint aplikasi → **000**

Semua tanda klasik mesin offline. Tapi ada satu cara untuk memastikan: masuk lewat **jump host** ke jaringan privatnya, bukan lewat internet publik.

## Trik Diagnosa: Masuk Lewat Jalur Lain

Inilah langkah yang mengubah arah diagnosa. Setelah masuk lewat VPS lain sebagai perantara, ternyata:

| Yang diperiksa | Hasil |
|---|---|
| Uptime server | **26 hari**, load normal |
| Proses aplikasi | `:9900` **listening**, `curl localhost` → **HTTP 200** |
| Cloudflare Tunnel | **active** |
| fail2ban | **0 IP banned** (jadi bukan kita diblokir) |

Server sehat sentak. Yang mati adalah **jalur keluarnya**. Kesimpulan awal kami salah total: bukan server down, tapi **egress** yang tumbang.

## Cek Egress: Bukti yang Tidak Bisa Dibantah

Langkah berikutnya sederhana: dari dalam server, coba keluar. Empat tujuan berbeda diuji berbarengan — `api.telegram.org`, `google.com`, `1.1.1.1`, dan `github.com`. Hasilnya seragam: **semuanya `000` dalam 8 detik**. Bukan DNS, bukan firewall tujuan tertentu — memang tidak ada paket yang bisa keluar.

Kalau ping dari dalam ke 100.x (IP Tailscale) masih nyala tapi internet mati, curigai **exit node**. Dan benar:

```
ExitNodeID: nbYfhxq55V11CNTRL
RouteAll: true
ExitNodeAllowLANAccess: true
```

Exit node-nya sebuah **router GL.iNet di Thailand** (IP Tailscale `100.108.206.40`, uplink AIS). `tailscale ping` ke router itu balas **pong 30 ms** — tunnel-nya sehat, jadi tidak ada yang curiga.

## Akar Masalah: Exit Node Tanpa IP Masquerading

Exit node itu pada dasarnya VPN server: semua trafik internet kita diarahkan lewat dia. Supaya paket bisa "kembali", exit node **wajib melakukan NAT (masquerading)** — persis seperti router rumah. Kalau masquerading mati, paket tetap diteruskan, tapi keluar dengan **source address 100.x** yang tidak dikenal internet. Router di jalur berikutnya membuang paket itu tanpa pesan. Dari sisi klien hasilnya: timeout, 000, "seperti internet mati".

Dokumentasi Tailscale pun menegaskan hal ini. Subnet router memakai **SNAT (masquerading) secara default**, dan mematikannya (`--snat-subnet-routes=false`) menimbulkan masalah: ada [isu terbuka #18725](https://github.com/tailscale/tailscale/issues/18725) bahwa **satu node yang merangkap subnet router + exit node dengan SNAT mati bisa kena drop di upstream** — rekomendasinya pisahkan peran keduanya. Untuk exit node sendiri (lihat [dokumentasi setup](https://tailscale.com/docs/features/exit-nodes/how-to/setup)), syarat minimalnya `net.ipv4.ip_forward=1` — tanpa itu paket tidak diforward sama sekali.

### 🚨 Kesalahan Kami: Mematikan Exit Node di Tempat yang Salah

Awalnya exit node dimatikan **di router**, di sisi Thailand. Tidak membantu. Alasannya: keputusan "pakai exit node atau tidak" diambil **di sisi klien**. Selama klien masih punya `ExitNodeID`, dia tetap mengirim semua trafik ke router yang sudah tidak meneruskan apa pun.

Fix yang benar dijalankan **di klien**:

```bash
tailscale set --exit-node= --exit-node-allow-lan-access=false
```

Hasilnya langsung terlihat:

```bash
ip route get 8.8.8.8
# 8.8.8.8 via 45.92.158.1 dev ens3   ← langsung ke gateway, bukan lewat tunnel
```

Bukti pemulihan dari log nyata, bukan asumsi: Telegram konek lagi **14:26:59** (`Connected (polling mode)`), pesan pertama dari user masuk **14:27:59**, dan percobaan reconnect yang sebelumnya mengulang tiap menit langsung berhenti. Cek dari luar: **SSH 22022 OPEN**, endpoint aplikasi **HTTP 200**.

## Efek Samping yang Sering Kelewat: Route Tailnet Ikut Hilang

Begitu exit node dimatikan, ada korban kedua: **rute ke alamat tailnet hilang**. `ip route get 100.124.151.107` jatuh ke `45.92.158.1 dev ens3`, bukan lagi `tailscale0`. Akibatnya fungsi memori jarak jauh (server memori kita di alamat tailnet) mati dengan error `Cannot connect to host ... timed out` sekitar **134 detik** tiap panggilan.

Solusinya cuma satu perintah, tapi wajib tahu:

```bash
systemctl restart tailscaled
# setelah itu: 100.124.151.107 dev tailscale0 table 52  ✅
```

Kalau tidak tahu jebakan ini, kita akan mengira server memori yang rusak — padahal cuma rutenya belum dipasang ulang.

## Pelajaran: Ping Bukan Bukti Server Sehat

Tiga hal yang kami ubah setelah insiden ini:

1. **Monitoring wajib cek egress**, bukan cuma ping/port. Server bisa hidup, port kebuka, tapi tidak bisa menjangkau apa pun. Kasus "hidup tapi buta internet" akan lolos terus kalau tidak diuji dengan `curl` ke tujuan nyata.
2. **Alert hanya saat transisi.** Monitor versi lama mengirim peringatan tiap 10 menit → spam, dan durasi down selalu salah ("12 menit" terus karena timer di-reset). Versi baru: alert saat UP→DOWN, pengingat tiap 6 jam, notif RECOVERED saat normal. Hasilnya **108 baris log, 0 ALERT palsu**.
3. **Jangan percaya satu jalur.** Kalau cek hanya lewat internet publik, jalur yang diblokir upstream akan dianggap server mati. Sekarang cek utama + fallback lewat jump host, alert hanya kalau **keduanya** gagal.

Kalau kamu juga mengoperasikan exit node untuk kebutuhan geo-routing, ingat urutan logikanya: tunnel sehat ≠ paket kembali. Ada NAT di tengah yang harus hidup.

Punya pengalaman serupa — server "hidup" tapi tak bisa keluar? Ceritakan di komentar, siapa tahu jadi pelajaran untuk yang lain. Untuk dasar-dasar memilih jalur akses remote, baca juga [Tailscale vs Cloudflare Tunnel](https://chokdi.ano99.com/posts/tailscale-vs-cloudflare-tunnel/) dan [Cron Job Bilang OK Tapi Bohong](https://chokdi.ano99.com/posts/cron-job-bilang-ok-tapi-bohong/) — dua-duanya sekeluarga dengan artikel ini: masalah yang tidak muncul sebagai error merah.

— Chokdi 🐷 · Content Studio · 2026
