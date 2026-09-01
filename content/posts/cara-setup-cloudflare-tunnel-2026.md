---
title: "Cara Setup Cloudflare Tunnel 2026: 12 Langkah Tanpa Buka Port"
date: 2026-09-01T11:40:00+07:00
draft: false
tags: ["Cloudflare", "Tunnel", "Tutorial", "Self-Hosted", "Keamanan"]
---

Buka port di router = buka pintu buat semua orang, bukan cuma buat kamu sendiri. Itu trade-off lama yang harus diterima setiap admin self-hosted: forward port 443, arahkan DNS ke IP rumah, dan berharap firewall-nya kuat. **Cloudflare Tunnel menghapus trade-off itu sepenuhnya** — koneksi outbound-only dari server ke edge Cloudflare, jadi tidak ada satu pun perangkat di jaringan kita yang mendengarkan traffic inbound dari internet.

Panduan ini membahas setup Cloudflare Tunnel lengkap tahun 2026, dari instalasi bersih sampai deployment production yang di-hardening dengan Zero Trust Access policies. 12 langkah, sekitar 45 menit, **nol port inbound terbuka**. Artikel ini juga menjawab pertanyaan yang sering muncul: sebenarnya apa maksud "hardening" itu? Kita bedah tuntas di bawah.

## Apa yang Sebenarnya Dilakukan Cloudflare Tunnel

Cloudflare Tunnel menjalankan daemon kecil bernama `cloudflared` di server. Daemon ini membuka koneksi **outbound** ke data center Cloudflare terdekat dan mendaftarkan dirinya ke tunnel bernama di akun kita. Ketika request masuk ke hostname, Cloudflare merutekannya lewat koneksi yang sudah ada ke origin server.

**Model keamanannya dalam satu kalimat:** tidak ada yang menerima koneksi inbound yang tidak diminta — selama-lamanya, berapa pun hostname atau service yang kita route.

Ini juga kenapa tunnel tetap jalan saat IP berubah, ISP bermasalah, atau server pindah jaringan total: identitas tunnel ada di file kredensial, bukan di alamat jaringan.

### Beda Tunnel vs Warp (sering ketuker)

- **Warp** = client-side agent yang merutekan traffic *perangkat* lewat Cloudflare — seperti VPN client biasa.
- **Cloudflare Tunnel** = sisi server: mengekspos *service* yang kita jalankan, bukan perangkat yang kita bawa.

Di deployment Zero Trust penuh, keduanya sering dipakai bareng — tapi untuk setup dasar tunnel, kita fokus ke sisi server saja.

## Prasyarat (semua gratis)

| Kebutuhan | Versi/Catatan |
|---|---|
| Akun Cloudflare | Plan Free cukup, domain nameserver diarahkan ke Cloudflare |
| `cloudflared` | 2026.8.2 (latest stable per 14-Agu-2026) |
| Server/VM | Linux (Debian/Ubuntu dipakai di sini), macOS, atau Windows |
| Docker Engine | Opsional, hanya untuk jalur Docker Compose |
| Domain di Cloudflare | TLD apa saja |

Tidak butuh static IP, tidak butuh sentuh panel router, tidak butuh plan berbayar.

## Step 1-2: Install & Login cloudflared

```bash
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' | sudo tee /etc/apt/sources.list.d/cloudflared.list

sudo apt-get update && sudo apt-get install cloudflared
cloudflared --version   # → cloudflared version 2026.8.2
```

Lalu autentikasi CLI (buka browser / URL untuk headless box):

```bash
cloudflared tunnel login
```

Login sukses menaruh sertifikat di `~/.cloudflared/cert.pem`. Ini kredensial penting — jangan commit ke repo publik, jangan salin ke mesin yang tidak kita kontrol.

## Step 3-4: Buat Tunnel & Config Ingress

```bash
cloudflared tunnel create homelab-tunnel
# → Tunnel credentials written to ~/.cloudflared/<TUNNEL-ID>.json
```

File JSON itu terikat ke tunnel spesifik. Kalau pindah host, **wajib ikut menyalin file ini** — lupa menyalinnya adalah penyebab paling umum kegagalan autentikasi di mesin baru.

Buat `~/.cloudflared/config.yml`:

```yaml
tunnel: homelab-tunnel
credentials-file: /home/user/.cloudflared/7f3a1c9e-....json

ingress:
  - hostname: app.example.com
    service: http://localhost:8080
  - hostname: grafana.example.com
    service: http://localhost:3000
  - service: http_status:404
```

⚠️ **Aturan emas:** ingress dievaluasi top-to-bottom, dan **rule terakhir WAJIB catch-all `http_status:404`**. Letakkan catch-all di atas hostname asli, dan semua request bakal ditelan sebelum sampai ke aplikasi.

## Step 5-6: Route DNS & Jalanin Pertama Kali

```bash
cloudflared tunnel route dns homelab-tunnel app.example.com
cloudflared tunnel route dns homelab-tunnel grafana.example.com
```

Ini membuat CNAME di DNS Cloudflare menunjuk ke `<TUNNEL-ID>.cfargotunnel.com` (otomatis proxy/orange cloud). **Tunnel tanpa DNS record itu tidak terlihat dunia luar** — langkah ini gampang dilewatkan dan jadi penyebab "kenapa domain gak resolve?"

Jalankan di foreground dulu:

```bash
cloudflared tunnel run homelab-tunnel
```

Startup sehat menampilkan 4 koneksi terdaftar (redundansi ke 4 edge location). Kalau `https://app.example.com` sudah nyampe ke `localhost:8080`, Ctrl+C dan lanjut ke persistent service.

## Step 7: Deploy Persistent (systemd / Docker Compose)

Jangan biarkan tunnel mati tiap SSH session ditutup. Dua opsi:

**Option A — Docker Compose:** app dan cloudflared dalam satu file, satu network Docker. ⚠️ Di dalam container, `localhost` mengacu ke container itu sendiri — pakai nama service Docker (`service: http://app:8080`), bukan localhost.

**Option B — systemd** (bare metal/VM), dengan hardening flags bawaan:

```ini
[Service]
User=cloudflared
Group=cloudflared
ExecStart=/usr/local/bin/cloudflared tunnel --config /etc/cloudflared/config.yml run
Restart=always
RestartSec=5
NoNewPrivileges=true
ProtectHome=true
ProtectSystem=full
```

Jalankan di bawah user sistem dedicated (`cloudflared`, shell `/usr/sbin/nologin`), bukan root. `NoNewPrivileges`, `ProtectHome`, `ProtectSystem=full` membatasi apa yang bisa diakses proses kalau sekalipun daemon dikompromikan.

## Apa Itu "Hardening"? (Riset Lebih Dalam)

Ini pertanyaan yang paling sering muncul — **hardening = proses mengunci sistem supaya tetap aman bukan cuma saat setup, tapi di kondisi terburuk sekalipun.** Kalau analogi: setup dasar itu kayak pasang pintu; hardening itu pasang gembok, alarm, CCTV, dan bikin SOP siapa yang boleh pegang kunci.

Di konteks Cloudflare Tunnel, hardening punya 5 lapisan:

### 1. Zero Trust Access Policies (paling penting)

Hostname publik tanpa access policy = port terbuka dengan bentuk berbeda. Cloudflare Access berdiri di depan tunnel dan **memaksa autentikasi sebelum request menyentuh origin**.

Di dashboard Zero Trust → Access → Applications, tambahkan self-hosted application per hostname internal (Grafana, admin panel, dll): atur session duration pendek, policy allow berdasarkan email domain / daftar email, identity provider built-in one-time PIN (atau Google/GitHub/SAML).

Tanpa ini, siapa pun bisa menemukan hostname lewat Certificate Transparency logs (publik by design) dan mengaksesnya. **Gate semua yang bukan untuk publik sebelum menyebut tunnel "selesai".**

### 2. Service Tokens (untuk machine-to-machine)

CI runner yang perlu hit API internal tidak bisa login via browser. Solusinya service token: pasangan Client ID + Secret di dashboard, dikirim sebagai header di request otomatis:

```bash
curl -H "CF-Access-Client-Id: <CLIENT_ID>.access" \
     -H "CF-Access-Client-Secret: <CLIENT_SECRET>" \
     https://internal-api.example.com/health
```

### 3. mTLS untuk yang sensitif

Untuk hal bener-bener sensitif (UI admin database), mTLS memaksa client certificate **di atas** Access policy — bukan cuma "siapa kamu" tapi "kamu punya sertifikat yang kita tanda tangani?"

### 4. Rotasi Kredensial

Jangan biarkan kredensial tunnel JSON dan service token statis selamanya. Rotasi terjadwal. Kalau laptop/server yang punya akses di-decommission, **revoke tunnel-nya dan buat ulang** — jangan coba ingat-ingat semua tempat file kredensial lama disalin.

### 5. Update cloudflared + WAF

Cek versi cloudflared berkala (cron bulanan pun lebih baik daripada lupa total) — binary outdated adalah sumber bug fix dan security patch yang terlewat. Untuk service yang pegang data user, pasangkan WAF rules di zone yang sama: Access menghentikan user tidak sah, WAF menghentikan request malformed/malicious **sebelum** sampai ke cloudflared.

### Checklist hardening sebelum "done"

- [ ] Catch-all `http_status:404` ada di baris paling bawah config.yml
- [ ] Semua hostname internal di belakang Access application dengan policy yang bekerja
- [ ] Tunnel jalan di systemd/Docker Compose (`Restart=always`), bukan foreground terminal
- [ ] Kredensial & config di-backup di luar server
- [ ] Versi cloudflared dicek berkala (cron)
- [ ] Service tokens dirotasi, tunnel yang tidak terpakai di-revoke

## 5 Pitfall Umum (dan Cara Hindari)

1. **Hilang file kredensial JSON saat pindah host** → salin bareng config.yml; jangan bikin tunnel baru (meninggalkan DNS yatim menunjuk ke tunnel ID mati).
2. **Catch-all ditaruh terlalu awal** → rule berjalan top-to-bottom, `404` di tengah menelan semua hostname setelahnya; gejalanya mirip origin rusak.
3. **Pakai localhost dari dalam container** → di Docker, localhost = container itu sendiri. Pakai nama service di shared network.
4. **Skip DNS route** → buat tunnel + ingress TIDAK otomatis bikin DNS record. Jalankan `tunnel route dns` per hostname.
5. **Lupa Access policy di tool internal** → tunnel tanpa Access = bisa diakses publik siapa pun yang nemu hostname-nya.

## Troubleshooting Singkat (8 Masalah Umum)

- **"could not read tunnel credentials"** → path `credentials-file` di config.yml tidak cocok dengan lokasi JSON asli.
- **Error 1033** → tunnel mati/putus; cek `cloudflared tunnel info`, restart kalau connection count = 0.
- **Semua route 404 walau origin sehat** → catch-all kepasang sebelum rule hostname; reorder + restart (config tidak hot-reload).
- **TLS error di log** → biasanya clock skew; cek NTP (`timedatectl`), handshake cloudflared sensitif waktu.
- **Loop restart di Docker** → `docker logs cloudflared`; paling sering config.yml mount salah atau kredensial tidak ikut ke volume.

## Kesimpulan

Cloudflare Tunnel adalah satu-satunya dari tiga solusi serupa (vs Tailscale Funnel vs ngrok) yang free tier-nya realistis buat produksi beneran: unlimited tunnel, unlimited hostname, Access policies untuk tim kecil, tanpa biaya per-gigabyte egress. Ditambah DNS, WAF, dan Zero Trust Access dalam satu platform — tanpa vendor tambahan.

Tapi ingat: **tunnel yang "udah jalan" tanpa hardening itu belum selesai.** Pasang Access policy untuk semua yang internal, rotasi kredensial, update cloudflared, dan backup config di luar server. 45 menit setup + 15 menit hardening = service yang aman, reachable dari mana saja, dan bertahan dari reboot tanpa dijagain.

Ada pengalaman setup tunnel sendiri atau pertanyaan soal Zero Trust Access? Tulis di komentar — kita diskusi bareng! — Chokdi 🐷 · Content Studio · 2026
