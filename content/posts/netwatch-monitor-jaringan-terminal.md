---
title: "NetWatch: Monitor Jaringan Real-Time di Terminal, Tanpa Config"
date: 2026-09-23T11:50:00+07:00
draft: false
tags: ["Networking", "Linux", "Tools", "Monitoring"]
---

Koneksi VPS melambat, upload jalan terus padahal tidak ada yang jalan, atau tiba-tiba ada trafik keluar ke IP asing. Untuk tahu *proses mana* yang bikin masalah, `iftop` dan `nload` tidak cukup — dua-duanya cuma kasih IP dan grafik, bukan jawaban. **NetWatch** mengisi celah itu: satu binary Rust, tanpa file config, langsung dipanggil dengan `sudo netwatch`, dan kamu dapat capture live, decode L7, atribusi proses, plus mesin diagnosa yang menutup sendiri temuan yang sudah beres.

## Apa itu NetWatch?

NetWatch adalah tool TUI (terminal user interface) untuk diagnosa jaringan real-time. Repo `matthart1983/netwatch` sudah **±3.292 bintang, 149 fork, lisensi MIT**, dan release terbarunya **v0.32.3 (20 September 2026)** — cadence rilisnya termasuk paling rajin di kategori tool terminal, bahkan masuk **Tool of The Week di Terminal Trove**.

Isinya 10 tab, semua diakses pakai tombol `1`–`0`:

| # | Tab | Isi |
|---|---|---|
| 1 | Dashboard | Latency, throughput mirrored, link aktif, koneksi per proses |
| 2 | Connections | Socket, PID, state, GeoIP, RTT, retransmit |
| 3 | Interfaces | Address, MTU, rate, error, drop |
| 4 | Packets | Decode live, dekripsi TLS 1.3, JA4, filter, export PCAP |
| 5 | Stats | Sebaran protokol + histogram timing handshake |
| 6 | Topology | Mesin, gateway, DNS, host teratas, traceroute |
| 7 | Timeline | Koneksi per TCP state + alert |
| 8 | Processes | Bandwidth per proses |
| 9 | Diagnose | Issue, penyebab, langkah fix, verified close |
| 0 | Egress | Tujuan yang sudah dikenal, policy, drift |

## Cara install

```bash
brew install netwatch                 # macOS / Linux
scoop install netwatch                # Windows (butuh Npcap)
cargo binstall netwatch-tui           # binary prebuilt, di mana saja
docker run --rm -it --net=host --pid=host --cap-add=NET_RAW \
  ghcr.io/matthart1983/netwatch
```

Untuk Debian/Ubuntu ada apt repository resmi, Fedora lewat COPR. Binary Linux-nya statis — tidak butuh dependensi tambahan.

Menjalankan tanpa sudo di Linux bisa, cukup sekali:

```bash
sudo setcap 'cap_net_raw,cap_bpf,cap_perfmon+eip' "$(which netwatch)"
```

## 4 fitur yang membuatnya beda

**1. Atribusi proses, bukan cuma IP.** Tab Connections dan Processes menempelkan tiap socket ke PID dan nama proses — persis yang kita butuh saat harus memutuskan "proses ini boleh dibunuh atau tidak". Untuk flow yang sangat pendek, atribusi bisa hilang atau basi; itu keterbatasan yang jujur diakui dokumennya.

**2. Dekripsi TLS 1.3 milik sendiri.** NetWatch memakai mekanisme `SSLKEYLOGFILE` yang sama dengan Wireshark: kalau kita yang pegang kuncinya, trafik itu bisa dibaca inline di tab Packets dan difilter pakai `decrypted:true`. Ini **bukan** intersepsi trafik orang lain — cuma membuka sesi milik kita sendiri.

**3. Diagnose engine yang menutup sendiri temuannya.** Tab 9 mempelajari baseline per metrik, lalu memakai katalog aturan untuk menyusun temuan: *issue*, penyebab terperingkat, langkah perbaikan. Kalau kondisi sehat bertahan, isu **tertutup otomatis**; kalau baseline rusak lagi, isu **terbuka otomatis**. Semua objeknya bisa diekspor jadi `report.md` — enak buat dilampirkan ke laporan.

**4. Egress linting.** Tab 0 mempelajari tujuan per proses (IP, ASN, SNI, port), lalu bisa di-*promote* (`P`) jadi `egress-policy.toml`. Selanjutnya tujuan baru muncul sebagai **drift**, bukan diblokir — modenya observe. File policy yang writable oleh grup/other akan ditolak tool, dan export NDJSON tersedia lewat tombol `e`.

Ada juga **Flight Recorder** yang membekukan rekaman saat alert kritis, plus sandbox Landlock di Linux.

## Tiga view, satu binary

- **Full** — 10 tab di atas.
- **`--lite`** — satu layar 80x24, pas untuk sesi SSH ke server kecil atau split tmux. Kalau kamu biasa kelola router atau proxy lewat SSH (lihat [Shadowsocks di router GL.iNet](/posts/shadowsocks-router-glinet/) dan [SSH SOCKS5 proxy](/posts/ssh-socks5-proxy/)), view ini yang paling sering dipakai.
- **`--view dense`** — 130x44+, empat kotak dengan grafik braille; unduh naik ke atas dari sumbu, unggah turun ke bawah.

View diganti pakai tombol `V` tanpa restart — collector tetap jalan.

## Kapan dipakai, kapan tidak

Pakai NetWatch kalau pertanyaannya "**siapa** yang bikin trafik ini, dan **kenapa** jadi lambat". Bandingkan dengan tetangganya: `bandwhich`/`iftop`/`nload` cuma rate; `tcpdump` + Wireshark paling lengkap tapi manual dan tanpa baseline. NetWatch menggabungkan keduanya dalam satu layar.

Yang perlu dicatat: proyeknya masih muda (dibuat Februari 2026) walau sangat aktif, butuh sudo atau `setcap`, atribusi proses bisa stale untuk flow sangat pendek, dan di Windows wajib Npcap. Untuk audit egress, dia **mengamati**, tidak memblokir — blokir tetap tugas firewall (misalnya pola tunnel di [Tailscale vs Cloudflare Tunnel](/posts/tailscale-vs-cloudflare-tunnel/)).

## Kesimpulan

NetWatch adalah jawaban untuk kasus klasik "server lambat, tidak tahu kenapa" tanpa harus merangkai tiga tool berbeda. Satu binary, `sudo netwatch`, dan tujuh puluh detik kemudian kamu sudah tahu proses, tujuan, dan penyebabnya.

Sudah pernah coba, atau masih setia `iftop`? Tulis di kolom komentar — saya penasaran tool apa yang kamu pakai untuk diagnosa jaringan sehari-hari.

**Sumber:**
- Repo resmi: [github.com/matthart1983/netwatch](https://github.com/matthart1983/netwatch)
- Halaman Terminal Trove: [terminaltrove.com/netwatch](https://terminaltrove.com/netwatch/)
- Registry crate: [crates.io/crates/netwatch-tui](https://crates.io/crates/netwatch-tui)

— Chokdi 🐷 · Content Studio · 2026
