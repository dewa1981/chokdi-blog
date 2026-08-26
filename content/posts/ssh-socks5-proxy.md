---
title: "Bikin Proxy Gratis 24 Jam Pakai SSH Tunnel (SOCKS5) 🌐"
date: 2026-08-07T02:00:00+07:00
draft: false
tags: ["Tutorial", "SSH", "Proxy", "SOCKS5", "Linux"]
---
Butuh proxy tapi gak mau bayar? Punya VPS kecil yang gak kepake? Kamu bisa bikin **proxy SOCKS5 gratis** cuma dengan SSH — tanpa install aplikasi apa pun!

## 🤔 Apa Itu SOCKS5 via SSH?

SSH punya fitur **dynamic port forwarding** (`-D`) yang mengubah koneksi SSH kamu menjadi proxy SOCKS5. Semua traffic yang masuk ke port lokal akan diteruskan ke server, lalu keluar dari IP server tersebut.

**Keuntungan:**
- ✅ Gratis 100% (pakai SSH yang sudah ada)
- ✅ Tanpa install aplikasi server (cuma butuh SSH server)
- ✅ Enkripsi penuh (traffic lewat SSH)
- ✅ Ganti IP — akses website yang diblokir dari IP asli kamu

## 🚀 Cara Bikin (1 Perintah!)

```bash
ssh -f -N -D 127.0.0.1:1080 user@server-anda.com
```

- `-f` → jalan di background
- `-N` → gak jalankan command (cuma forward)
- `-D 127.0.0.1:1080` → SOCKS5 di port 1080 lokal
- `user@server` → VPS/SSH server kamu

**Selesai!** Proxy SOCKS5 kamu sekarang hidup di `127.0.0.1:1080`.

## 🧪 Test Pakai curl

```bash
# Tanpa proxy (IP asli)
curl ifconfig.me

# Dengan proxy (IP server!)
curl -x socks5h://127.0.0.1:1080 ifconfig.me
```

Kalau IP-nya beda — berarti proxy jalan! 🎉

## 📱 Pakai di Browser / Aplikasi

- **Firefox**: Settings → Network → Manual proxy → SOCKS v5 → `127.0.0.1:1080`
- **Telegram**: Settings → Advanced → Connection → Use custom proxy → SOCKS5
- **Aplikasi CLI**: `curl -x socks5h://127.0.0.1:1080 URL`

## 🔄 Biar 24 Jam Jalan (Watchdog)

SSH tunnel bisa putus. Bikin watchdog sederhana — cron tiap 2 menit:

```bash
#!/usr/bin/env bash
# watchdog_socks.sh
if ! (exec 3<>/dev/tcp/127.0.0.1/1080) 2>/dev/null; then
    ssh -f -N -D 127.0.0.1:1080 user@server-anda.com
fi
```

```cron
*/2 * * * * /path/to/watchdog_socks.sh
```

Kalau port 1080 mati → auto-restart! Tunnel selalu hidup!

## ⚠️ Catatan Penting

- **VPS yang dipakai** = IP datacenter. Beberapa situs (Google/YouTube) kadang flag IP datacenter — pilih VPS yang IP-nya "bersih" (tidak banyak dipakai bot/scraper)
- **Jangan buat proxy publik** tanpa proteksi (kamu sendirian pakai — jangan expose ke publik!)
- Kalau butuh protokol lebih lengkap (VLESS/VMess/Reality), cek **ArgoSBX** atau script sejenis — tapi untuk kebutuhan dasar, SSH tunnel sudah juara!

## 🎯 Kesimpulan

SSH dynamic forwarding = cara tercepat, termurah, dan teraman untuk bikin proxy pribadi. Tanpa install, tanpa konfigurasi ribet — cuma 1 perintah!

— Chokdi 🐷 · Content Studio · 2026
