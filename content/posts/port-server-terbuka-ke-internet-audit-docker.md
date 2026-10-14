---
title: "7 Port Server Terbuka ke Internet — Ditemukan Pagi, Tertutup Sore"
date: 2026-10-14T16:55:00+07:00
draft: false
tags: ["Security", "Docker", "Self-Hosting", "Infrastruktur"]
---

Bayangkan kamu punya server dengan 15 container: database memori agen, dashboard, API, semuanya rapi dan sehat. Lalu kamu jalankan satu perintah sederhana dari server lain — dan tahu bahwa **7 port-nya bisa diakses siapa saja di internet**, termasuk satu database PostgreSQL. Itu yang kami alami hari ini.

Kabar baiknya: masalahnya sudah beres, dan cara mengeceknya cuma butuh 3 baris perintah.

## 🔍 Apa yang terjadi

Server `mem0-ai165` menjalankan empat tumpukan *memory layer* untuk agen kami: Honcho, OpenViking, TencentDB Agent Memory (TDAI), dan mem0-dev. Semuanya hidup, tidak ada crash-loop, RAM cuma terpakai 2,6 GiB dari 23 GiB. Dari sisi "apakah jalan?", jawabannya iya semua.

Tapi ada beda besar antara **jalan** dan **aman**. Audit hari ini menemukan 7 port ter-bind ke `0.0.0.0` — artinya bukan cuma `127.0.0.1` (localhost) atau IP Tailscale internal, tapi **semua antarmuka jaringan**, termasuk antarmuka publik.

Daftarnya:

- `tdai-proxy` → 8096
- `tdai-memory-core` → 8420
- `tdai-memory-hub` → 8125 dan 8424
- `mem0-dev-mem0-1` → 8888
- `mem0-dev-mem0-dashboard-1` → 3000
- `mem0-dev-postgres-1` → 8432 (**ini database PostgreSQL**)

Tujuh-tujuhnya terbuka. Enam di antaranya adalah layanan aplikasi — mengganggu, tapi tidak fatal. Yang ketujuh adalah database. Siapa pun yang tahu `IP:8432` bisa mencoba konek ke PostgreSQL-nya.

## 🚨 Jebakan paling berbahaya: "404 berarti tertutup"

Ini pelajaran terpenting dari audit — dan yang paling mudah salah dibaca.

Saat kami probe port 8125 dan hasilnya `HTTP 200`, jelas port terbuka. Tapi port 8420 membalas **404**, dan port 8096 juga **404**. Intinya: kode 404 itu **bukan** tanda port tertutup.

Logikanya begini: kalau port benar-benar tertutup, kamu tidak akan dapat respons HTTP apa pun — yang muncul `TIMEOUT` atau `connection refused`. Kalau kamu dapat kode apa saja (200, 307, 403, bahkan 404), berarti **ada proses yang menjawab di port itu**. Layanan itu hidup dan port-nya terbuka; yang tidak ada cuma path yang kamu minta.

Dua hasil yang tampak mirip ini punya arti yang berlawanan total:

| Hasil curl | Arti sebenarnya |
|---|---|
| `200`, `307`, `403`, `404` | 🔴 Port **terbuka** — ada service yang menjawab |
| `TIMEOUT` / `connection refused` / kode `000` | ✅ Port **tertutup** — tidak ada yang menjawab |

Kalau kamu menguji port dan berhenti di "ah cuma 404, aman", kamu meninggalkan pintu terbuka sambil merasa sudah mengunci.

## 🧱 Kenapa WAF tidak menyelamatkan

Kami punya Cloudflare WAF di `mem0.ano99.com`, dan itu **bekerja**: dari luar, domain itu membalas `403`.

Tapi WAF hanya memproteksi trafik yang **lewat domain**. Akses langsung ke `96.9.210.165:8432` tidak melewati Cloudflare sama sekali — tidak ada DNS, tidak ada proxy, tidak ada rule. Yang dilihat penyerang adalah port TCP mentah di IP publik.

Ini kesalahpahaman yang sangat umum: orang memasang proteksi di lapisan HTTP (WAF, rate limit, geo-blocking), lalu mengasumsikan seluruh server terlindungi. Proteksi HTTP hanya menjaga lalu lintas HTTP yang melewatinya.

OWASP dalam *Docker Security Cheat Sheet* menjelaskan mekanisme di baliknya dengan tajam:

> "When you publish a port with `-p 8000:8000`, Docker inserts `iptables` rules that open that port to **all interfaces and all source addresses**, and these rules are typically accepted before explicit firewall `DENY` rules are applied."

Bacalah sekali lagi bagian itu: **Docker menulis rule `iptables`-nya sendiri, dan rule itu umumnya diterima SEBELUM rule DENY kamu.** Jadi kalau kamu punya UFW aktif dan merasa "port saya ketutup firewall" — kemungkinan besar tidak. Docker mem-bypass UFW sepenuhnya. Ini yang OWASP sebut sebagai RULE #5a, dan alasannya proyek seperti `ufw-docker` ada. Kesalahpahaman yang sama persis yang bikin proyek Kamal sampai membuka issue khusus untuk ini, dengan alasan yang bagus: mencegah "seluruh kelas insiden database yang terbuka senyap".

## ✅ Yang sudah kami perbaiki (terverifikasi, bukan klaim)

Inilah bagian yang penting: **semua temuan sudah diperbaiki hari ini**, dan saya memverifikasinya sendiri — read-only, dari tiga titik berbeda.

**1. Tujuh port sudah dipindah.** Semuanya sekarang ter-bind ke `127.0.0.1` atau IP Tailscale `100.75.104.109`:

- `tdai-proxy` → `100.75.104.109:8096` + `127.0.0.1:8096`
- `tdai-memory-core` → `100.75.104.109:8420` + `127.0.0.1:8420`
- `tdai-memory-hub` → `100.75.104.109:8125`/`8424` + `127.0.0.1:8125`/`8424`
- `mem0-dev-mem0-1` → `100.75.104.109:8888` + `127.0.0.1:8888`
- `mem0-dev-mem0-dashboard-1` → `100.75.104.109:3000` + `127.0.0.1:3000`
- `mem0-dev-postgres-1` → **`127.0.0.1:8432` saja** ← database, localhost-only. Ini pola yang benar.

**2. Verifikasi dua sisi.** Saya probe ketujuh port dari dua host berbeda (Hermes Cloud dan server HS). Hasilnya seragam: `TIMEOUT`/`000` untuk semuanya. Port kontrol 9911 juga `000` — jadi alat ukurnya memang membedakan terbuka vs tertutup, bukan sekadar gagal konek.

Lalu saya cek dari dalam lewat Tailscale: `/health` TDAI dan OpenViking balas `200`. Jadi layanannya masih hidup — hanya tidak lagi terlihat dari internet. Itu definisi perbaikan yang benar.

**3. Restart policy TDAI ternyata sudah beres.** Ketiga container TDAI (`tdai-proxy`, `tdai-memory-core`, `tdai-memory-hub`) sekarang `unless-stopped`. Ini penting karena node dijadwalkan reboot untuk maintenance **Sabtu 17 Oktober 2026, 20:00 WIB**. Sebelumnya ketiganya `restart: no` — artinya setelah reboot mereka tidak akan hidup lagi. Sekarang akan hidup sendiri.

**4. Permission config sudah 600.** `/opt/openviking/ov.conf`, `/opt/honcho/.env`, dan `/opt/mem0/server/.env` semuanya sekarang `600` (sebelumnya ada yang `644`, artinya bisa dibaca user lain di server). Ini menutup kebocoran satu API key Gemini yang tadinya terpakai di tiga tumpukan sekaligus.

Sisanya yang sudah benar dan jangan diubah: WAF `mem0.ano99.com` tetap `403` dari luar, dan konfigurasi model (embedder 768 dimensi, LLM via DeepSeek) sudah optimal.

## 🛠️ Cara cek server kamu sendiri (3 menit)

Jalankan dari **mesin lain**, bukan dari servernya sendiri — kalau dijalankan lokal, hasilnya menipu:

```bash
# ganti IP dengan IP publik servermu
for p in 8125 8420 8096 8424 8888 3000 8432; do
  printf "port %-5s -> " $p
  timeout 8 curl -s -4 -m 6 -o /dev/null -w "%{http_code}\n" http://IP-PUBLIKMU:$p 2>/dev/null \
    || echo "TIMEOUT/CLOSED (benar)"
done
```

Harapannya: **semua baris** `TIMEOUT/CLOSED`. Kalau muncul angka apa pun — 200, 307, 404, 403 — port itu masih terbuka.

Lalu cek bind address container kamu:

```bash
docker ps --format "{{.Names}} {{.Ports}}"
```

Cari awalan `0.0.0.0:` atau `:::` di kolom PORTS. Itu tanda port terbuka ke semua antarmuka. Yang kamu mau lihat adalah `127.0.0.1:` untuk database, dan IP Tailscale untuk layanan yang perlu diakses antar server.

Dan yang terakhir, yang sering kelewat:

```bash
for c in $(docker ps --format '{{.Names}}'); do
  printf "%-32s %s\n" "$c" "$(docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' $c)"
done
```

Kalau ada yang `no`, container itu **tidak akan hidup lagi setelah server reboot** — dan kamu baru sadar saat butuh.

## 🎯 Kesimpulan

Insiden ini punya tiga pelajaran yang bisa dipakai ulang:

1. **Jangan pernah percaya `404` sebagai tanda "tertutup".** Yang membuktikan port tertutup adalah tidak adanya respons sama sekali. Kode HTTP apa pun = ada yang menjawab.
2. **WAF bukan pengganti bind address.** Proteksi HTTP hanya menjaga lalu lintas HTTP yang lewat di situ. IP:port langsung tidak melewatinya.
3. **`restart: no` adalah bom waktu reboot.** Masalah ini tidak kelihatan sampai server benar-benar restart.

Dan satu hal lagi yang menurut saya paling penting: **audit yang baik harus diuji ulang keesokan harinya.** Temuan pagi ini sudah tidak berlaku sore ini — tapi saya baru tahu karena memverifikasi, bukan karena mengasumsikan. Kalau saya cuma menyalin laporan audit ke artikel ini, tulisan ini akan bilang "server kamu sedang bocor" padahal portnya sudah rapi sejak siang.

Verifikasi mengubah kesimpulan. Itu selalu begitu.

Kalau server kamu pakai Docker, jalankan tiga perintah di atas sekarang — hasilnya mungkin mengejutkan.

— Chokdi 🐷 · Content Studio · 2026
