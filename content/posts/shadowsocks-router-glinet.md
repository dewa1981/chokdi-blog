---
title: "Shadowsocks di Router GL.iNet: 1 Proxy SOCKS5 untuk Seluruh LAN 🛰️"
date: 2026-09-23T00:10:00+07:00
draft: false
tags: ["Jaringan", "OpenWrt", "Proxy", "Tutorial", "GL.iNet"]
---

Router GL.iNet itu OpenWrt yang sudah dipoles. Artinya kamu bisa menyuruh **router-nya sendiri** jadi proxy SOCKS5 — lalu semua device di LAN (laptop, HP, TV, browser kerja) bisa numpang lewat situ. Satu config, satu titik kontrol, tidak perlu pasang aplikasi proxy di tiap device.

Catatan lengkapnya sudah kami buktikan di dua router beda chipset: GL-BE9300 (Qualcomm) dan GL-MT6000 Flint 2 (MediaTek). Ini resepnya.

## Kenapa ditaruh di router, bukan di tiap device?

| Pendekatan | Kelebihan | Kekurangan |
|---|---|---|
| Aplikasi proxy per device | Gampang, tanpa sentuh router | Setup berulang, config tersebar, gampang lupa |
| Proxy di router (SOCKS5) | Sekali pasang, semua device dapat | Perlu akses SSH + bikin init script sendiri |

Yang penting: kita pakai mode **ss-local** — router jadi *klien* Shadowsocks yang membuka port SOCKS5 lokal, bukan mode transparent proxy. Mode ini jauh lebih tahan banting, terutama di board Qualcomm.

## Yang perlu disiapkan

- Router GL.iNet yang sudah bisa di-SSH (`ssh root@<ip-router>`).
- Akun server Shadowsocks (server, port, method, password).
- Firmware yang punya feed opkg — di GL-MT6000 (GL.iNet 4.9.1, base OpenWrt 21.02) paket `shadowsocks-libev-ss-local` tersedia langsung.
- **Backup dulu — wajib, bukan opsional.** `tar czf /tmp/backup-pre.tar.gz -C /etc config` plus `uci export`.

## Resep instalasi (5 langkah)

```bash
# 1. Backup
uci export > /tmp/uci-pre.txt
opkg list-installed > /tmp/pkgs-pre.txt

# 2. Install mesinnya saja (JANGAN luci-app-*)
opkg install shadowsocks-libev-ss-local

# 3. Upload init script sendiri (lihat bagian bawah), chmod 755
#    Tidak ada binary base64 di OpenWrt -> pakai openssl!
B64=$(base64 -w0 ss-custom)
ssh root@<ip-router> "echo '$B64' | openssl base64 -d -A > /etc/init.d/ss-custom; chmod 755 /etc/init.d/ss-custom"

# 4. Enable + start
/etc/init.d/ss-custom enable
/etc/init.d/ss-custom start
```

Langkah 3 itu intinya. Init bawaan paket GL.iNet **tidak bisa dipakai** untuk kasus ini (alasannya di bagian jebakan), jadi kita tulis service procd sendiri.

## Init script `ss-custom` (procd)

Ini yang mengontrol proxy dan auto-start saat boot:

```sh
#!/bin/sh /etc/rc.common
START=95
STOP=10
USE_PROCD=1
SS_BIN="/usr/bin/ss-local"

start_instance() {
	local name="$1" server="$2" port="$3" pass="$4" method="$5" lport="$6"
	procd_open_instance "$name"
	procd_set_param command "$SS_BIN" \
		-s "$server" -p "$port" -k "$pass" -m "$method" \
		-l "$lport" -b 0.0.0.0 -u -t 60
	procd_set_param respawn 3600 5 5
	procd_set_param stdout 1
	procd_set_param stderr 1
	procd_close_instance
}

start_service() {
	start_instance "sg" "sg.contoh.com" "443" "RAHASIA" "xchacha20-ietf-poly1305" "1080"
	start_instance "id" "id.contoh.com" "443" "RAHASIA" "xchacha20-ietf-poly1305" "1081"
}

stop_service() { : }
reload_service() { stop; start }
```

Dua hal kunci: `-b 0.0.0.0` (agar device LAN bisa akses, bukan cuma router sendiri) dan `respawn` (proxy hidup otomatis kalau mati). Pola `procd_open_instance` / `procd_set_param` ini memang cara resmi membuat service di OpenWrt — service harus jalan di foreground, procd yang mengurus background-nya ([dokumentasi procd OpenWrt](https://openwrt.org/docs/guide-developer/procd-init-scripts)).

## Verifikasi 2x — jangan cuma lihat "running"

Cek dari **dalam router** dan **dari device lain**:

```bash
ssh root@<ip-router>
ps w | grep ss-local                                  # harus 2 proses
netstat -tlnp | grep -E ':1080|:1081'                 # LISTEN di 0.0.0.0
curl -s --socks5-hostname 127.0.0.1:1080 https://api.ipify.org
```

Terakhir, dari laptop/server lain di LAN: `curl --socks5-hostname 192.168.8.1:1080 https://api.ipify.org`. Kalau exit IP-nya sudah IP negara tujuan, berarti beres.

Di client: set **type SOCKS5** (bukan HTTP), host = IP LAN router, port 1080/1081, tanpa username/password.

## Enam jebakan yang paling sering kena

| # | Masalah | Sebab & solusi |
|---|---|---|
| 1 | Device LAN tidak bisa pakai proxy | Init bawaan hardcode `-b 127.0.0.1` → pakai init sendiri |
| 2 | Chrome: `ERR_EMPTY_RESPONSE` | Type proxy di-set HTTP padahal port-nya SOCKS5 → ganti SOCKS5 |
| 3 | `scp` gagal, `base64: not found` | OpenWrt minim → `scp -O` dan `openssl base64 -d -A` |
| 4 | `nc -z` error | busybox nc terbatas → `ash -c "echo > /dev/tcp/IP/PORT"` |
| 5 | Transparent proxy diam-diam gagal | Offload NSS Qualcomm bypass netfilter → pakai ss-local per-device |
| 6 | IP router beda antar device | Setiap router punya subnet sendiri, jangan asal copas config |

Jebakan nomor 5 penting: kami pernah bangun TPROXY lengkap (ipset + dnsmasq + iptables) dan counter-nya naik, tapi paket tidak diteruskan di board Qualcomm. Di board MediaTek dengan mode SOCKS5, semuanya jalan normal.

## Kenapa tidak ada menu Shadowsocks di LuCI?

Pertanyaan yang sering muncul setelah instalasi: kok menu-nya tidak muncul? **Karena memang tidak dipasang — sengaja.**

Yang dipasang hanya mesinnya (`shadowsocks-libev-ss-local` + init `ss-custom` kita). `luci-app-shadowsocks-libev` tidak diinstall karena tiga alasan: bawa config UCI default di port 1080 yang **bentrok** dengan `ss-custom` kita, versi LuCI beda per feed (bisa bikin LuCI blank), dan setting proxy jarang diubah — edit satu file lebih jelas daripada form.

Satu catatan: `opkg install shadowsocks-libev-ss-local` menarik `shadowsocks-libev-config` yang otomatis meng-enable init bawaan (S99). Statusnya masih `active with no instances` alias tidak mengganggu, tapi kalau mau aman: `/etc/init.d/shadowsocks-libev disable` — `ss-custom` tidak terpengaruh.

## Kesimpulan

Router GL.iNet = OpenWrt = server kecil yang bisa kamu suruh apa saja, termasuk jadi proxy gateway satu rumah. Kuncinya cuma tiga: pakai mode `ss-local`, tulis init script procd sendiri, dan verifikasi dari luar router — bukan cuma dari dalam.

Kalau kamu lebih suka proxy yang digerakkan dari server/VPS, cara SSH SOCKS5 juga kami bahas di [artikel proxy SSH tunnel](/posts/ssh-socks5-proxy/). Dan kalau masih bingung memilih jalur akses remote yang aman, ada perbandingan [Tailscale vs Cloudflare Tunnel](/posts/tailscale-vs-cloudflare-tunnel/).

Punya router OpenWrt nganggur di lemari? Ini proyek sore yang berguna — coba dulu, nanti cerita di komentar.

— Chokdi 🐷 · Content Studio · 2026
