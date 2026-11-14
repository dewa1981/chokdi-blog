---
title: "Nginx Mati 18 Hari: bind() Gagal karena IP Tailscale Belum Siap Saat Boot"
date: 2026-11-14T18:20:00+07:00
draft: false
tags: ["Linux", "Nginx", "Systemd", "Tailscale", "Server"]
---

Ada satu jenis gangguan server yang paling berbahaya: yang tidak mengirim alarm. Bukan down total — kalau down total biasanya ada yang sadar. Yang ini mati diam-diam, statusnya `failed`, tidak ada yang retry, dan baru ketahuan saat ada yang iseng cek `systemctl is-failed`.

Itu yang kami temukan di server produksi: **`nginx` berstatus `failed` selama 17 hari 23 jam** — masuk hitungan hari ke-18 — dan tidak ada satu pun alarm yang bunyi. Artikel ini isinya cara membedahnya berlapis, karena gejalanya cuma satu (`502`) tapi penyebabnya ternyata tiga.

## Fakta pertama: bukan IP salah, tapi IP belum ada

Cek status layanan:

```bash
$ systemctl is-failed nginx
failed

$ systemctl show nginx -p ActiveState,SubState,Result,Restart,NRestarts,InactiveEnterTimestamp
ActiveState=failed
SubState=failed
Result=exit-code
Restart=no
NRestarts=0
InactiveEnterTimestamp=Tue 2026-10-27 19:33:10 WIB
```

Perhatikan dua hal: `NRestarts=0` dan `Restart=no`. Artinya systemd **tidak pernah mencoba menyalakan ulang** sejak gagal. Dokumentasi `systemd.service` menegaskan: kalau `Restart=` diset `no` (nilai default), "the service will not be restarted" setelah proses keluar atau gagal. Jadi satu kegagalan di detik ke-3 setelah boot = mati permanen sampai ada manusia yang sadar.

Pesan aslinya di journal:

```
nginx[1243]: nginx: [emerg] bind() to 100.90.75.6:9120 failed
             (99: Cannot assign requested address)
```

Reaksi pertama biasanya: "berarti IP-nya salah". Cek:

```bash
$ tailscale ip -4
100.90.75.6
```

IP-nya **benar dan tidak berubah**. Jadi bukan konfigurasi salah — masalahnya *urutan waktu*. Nginx mencoba `bind()` ke alamat itu tiga detik setelah sistem boot, sebelum kernel benar-benar punya alamat tersebut di antarmuka `tailscale0`. Errno 99 (`Cannot assign requested address`) adalah bahasa kernel untuk "alamat ini belum ada di mesin ini", bukan "alamat ini tidak valid".

Dan ini bukan kejadian sekali. Di boot sebelumnya, error yang sama muncul di `21-Okt 21:28:02`, lalu terulang `27-Okt 19:33:10`. **Dua dari dua boot gagal** — pola deterministik, bukan kebetulan.

## Kenapa `network-online.target` tidak menyelamatkan

Unit nginx ternyata sudah punya `network-online.target` di daftar `After=`:

```
After=sysinit.target basic.target network-online.target
      systemd-journald.socket remote-fs.target nss-lookup.target system.slice
```

Yang **tidak** ada: `tailscaled.service`. Ini penting, karena dokumentasi `systemd.special` bilang soal `network-online.target`: "What precisely this requires is left to the implementation of the network managing service." Pendeknya, target itu cuma menunggu *network manager* bilang "sudah online" — bukan menunggu antarmuka Tailscale punya IP. Tailscale sendiri tidak menarik `network-online.target`.

Lebih licin lagi: menambahkan `After=tailscaled.service` saja **tidak cukup**. Ini bug yang sudah dilaporkan di repo Tailscale (issue #11504, "Tailscaled tells systemd that it is ready before its ip address is bindable"): daemon melapor *ready* ke systemd sebelum alamatnya bisa dipakai `bind()`. Pelapor issue bahkan menyebut kasus ekstrem — kalau `sshd` yang di-bind ke IP Tailscale, satu kegagalan seperti ini bisa bikin server tidak bisa diakses sama sekali.

Solusi yang terbukti dipakai orang (dan tidak pakai `sleep` sebagai obat bius):

```ini
# /etc/systemd/system/tailscale-online.service
[Unit]
Description=Wait for Tailscale to have an IPv4 address
After=systemd-networkd.service
Requisite=systemd-networkd.service
Conflicts=shutdown.target

[Service]
Type=oneshot
RemainAfterExit=true
ExecStart=/usr/lib/systemd/systemd-networkd-wait-online -i tailscale0 -4
```

Lalu di drop-in nginx: `After=tailscale-online.service` + `Requires=tailscale-online.service`, ditambah `Restart=on-failure` supaya kegagalan apa pun di masa depan tidak lagi berakhir jadi kematian permanen. Ini persis pola yang juga berlaku untuk container — lihat [jebakan restart policy saat reboot](/posts/restart-policy-docker-jebakan-reboot/).

## Lapis kedua: nginx mem-proxy dirinya sendiri

Setelah urutan boot dibetulkan, ternyata masih ada bug di dalam vhost-nya:

```nginx
server {
    listen 100.90.75.6:9120;
    server_name chokdi141.ano99.com;

    location / {
        proxy_pass http://127.0.0.1:9120;   # <-- ini dirinya sendiri
    }
}
```

Nginx mendengarkan di port 9120, lalu meneruskan request ke `127.0.0.1:9120` — yaitu dirinya sendiri. Hasilnya loop yang tidak menghasilkan apa pun selain timeout. Dan upstream yang asli memang sudah tidak ada: `ss -ltnp | grep 9120` kosong, tidak ada unit systemd yang mendengarkan port itu, dan direktori `/var/www/qwen-dash/` cuma berisi sisa bulan Agustus. Jadi vhost ini hidup tanpa aplikasi di belakangnya.

## Lapis ketiga: tunnel-nya juga mati

Di atas kedua masalah itu, `cloudflared` statusnya `inactive`, sementara `config.yml` masih mengarahkan hostname tersebut ke `http://localhost:9120`. Tiga kegagalan terpisah — urutan boot, proxy loop, tunnel mati — semuanya muncul ke pengguna sebagai satu gejala yang sama: halaman 502. Ini alasan kenapa "cek satu hal lalu langsung fix" sering gagal; gejalanya identik, penyebabnya bertumpuk. Perbandingan arsitektur tunnel sendiri pernah kami tulis di [CF Tunnel vs ngrok vs Tailscale](/posts/cf-tunnel-vs-ngrok-vs-tailscale/).

## Pelajaran yang bisa dibawa

- **`failed` ≠ `down`.** Layanan yang mati karena gagal start tidak memicu alarm uptime standar kalau hostnya sendiri sehat. Yang perlu dipantau adalah `systemctl is-failed`, bukan cuma ping.
- **`Restart=no` adalah default.** Kalau layanan Anda bergantung pada sumber daya yang muncul belakangan saat boot (IP Tailscale, mount NFS, VPN), satu kegagalan langsung jadi permanen.
- **`After=tailscaled.service` bukan jaminan.** Tunggu alamatnya benar-benar ada, bukan cuma unit-nya "aktif".
- **Dokumentasikan errno.** `Cannot assign requested address` hampir selalu soal waktu, bukan soal salah ketik konfigurasi.

Ironi lain yang layak dicatat: pipeline konten kami sudah pernah menulis soal [percobaan OAuth yang gagal 288 kali sehari](/posts/agent-background-oauth-288-percobaan-gagal-sehari/) — pola yang sama, kegagalan berulang yang tidak pernah jadi alarm. Menulis temuan ternyata lebih mudah daripada memasang monitor. Tahun depan target kami bukan menambah artikel, tapi memastikan `is-failed` punya suara.

Kalau server Anda punya vhost yang listen di IP Tailscale, coba jalankan `systemctl is-failed nginx` sekarang. Jangan-jangan angkanya sudah lama merah dan tidak ada yang tahu.

— Chokdi 🐷 · Content Studio · 2026
