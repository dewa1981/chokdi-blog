---
title: "IP-KVM: Jalur Terakhir Saat Server Hang Total"
date: 2026-10-06T17:55:00+07:00
draft: false
tags: ["IP-KVM", "Tailscale", "Homelab", "Remote Access", "Tips"]
---

SSH timeout, ping mati, dashboard balas kosong — padahal mesinnya masih menyala dan lampu power tetap hijau. Di titik itu tidak ada satu pun tool jaringan yang bisa menolong: **yang tersisa hanya IP-KVM**. Perangkat kecil yang ditancapkan ke HDMI + USB mesin target, lalu memberi kita layar, keyboard, dan mouse — sampai ke level BIOS.

Artikel ini merangkum pelajaran nyata dari unit yang kami pakai (GL.iNet Comet Pro / GL-RM10) supaya kalau versi Anda kena masalah, perbaikannya tidak perlu 2 jam.

## Kenapa SSH Tidak Pernah Cukup

SSH hanya berguna kalau **OS berhasil boot dan jaringan hidup**. Tiga skenario ini bikin SSH mustahil dipakai:

- Kernel panic atau boot loader rusak — OS tidak pernah nyala.
- Disk penuh sampai service jaringan gagal start.
- Perlu masuk BIOS/UEFI: ganti urutan boot, nyalakan virtualisasi, atau flash BIOS.

IP-KVM bekerja di lapisan yang lebih dalam: dia cuma butuh **listrik + kabel HDMI**. Kita bisa melihat POST screen, masuk BIOS, memilih boot device, atau menjalankan `fsck` dari live USB — seolah-olah tangan kita ada di depan mesin. Karena itu posisinya di **ujung rantai ketersediaan**: kalau perangkat ini juga rusak, mesinnya benar-benar harus disentuh fisik.

## Comet Pro: Akses Level Hardware Lewat Tailscale

Unit kami adalah **GL.iNet Comet Pro (GL-RM10)**. Yang membuatnya praktis: perangkat ini punya node **Tailscale sendiri**, jadi kita tidak perlu membuka port publik atau lewat aplikasi cloud vendor — cukup buka IP Tailscale-nya di browser.

Di console-nya ada beberapa mode transfer video, dan ini yang sering bikin bingung saat kualitas gambar jelek:

| Mode | Kapan dipakai |
|---|---|
| WebRTC | Seimbang: video lancar + audio jalan |
| WebRTC (FEC) | Jaringan tidak stabil — paket hilang ditambal data redundan |
| WebRTC (Native) | Library WebRTC Google, ada sejak firmware v1.10.0 |
| Direct | Latensi paling rendah, kualitas lossless, **tanpa audio** |

Sumber: dokumentasi resmi [GL.iNet KVM Console Guide](https://docs.gl-inet.com/kvm/en/user_guide/gl-rm10/console_guide/). Kalau Anda cuma butuh kecepatan respons keyboard, `Direct` sering lebih nyaman daripada mengejar kualitas gambar.

## Pelajaran 1: Buildroot, Bukan OpenWrt

Jangan berasumsi perangkat KVM GL.iNet sama dengan router GL.iNet. Di unit kami, `cat /etc/os-release` menjawab `ID=buildroot` — bukan OpenWrt. Konsekuensinya:

- **Tidak ada `opkg`**, jadi tidak ada jalur install paket seperti di router.
- **Tidak ada updater in-place**; update firmware hanya lewat channel resmi GL.iNet (upload image).
- Tailscale client yang dibundel **tidak aman di-upgrade sendiri** — build-nya custom.

Jebakan yang paling sering muncul: panel admin Tailscale bilang *"client outdated"*. Di unit kami itu bukan masalah nyata — perangkatnya memang berjalan di firmware beta yang membawa build Tailscale versi dev. Salah fix-nya justru berisiko: mengganti client secara manual bisa merusak jalur akses darurat satu-satunya.

## Pelajaran 2: SSH-nya OpenSSH, Bukan Dropbear

Ini trap klasik yang bikin orang menyerah: sudah menaruh public key di file `authorized_keys`, tapi login tetap `Permission denied`. Di unit kami penyebabnya sederhana — file `authorized_keys` ala **dropbear** memang ada, tapi daemon yang benar-benar listening adalah **OpenSSH sshd**. Key yang ditulis ke file dropbear tidak pernah dibaca.

Urutan diagnosa yang benar:

```bash
ps w | grep -E 'sshd|dropbear'      # daemon mana yang jalan?
grep AuthorizedKeysFile /etc/ssh/sshd_config
```

OpenSSH default membaca `/root/.ssh/authorized_keys`. Dan ingat bedanya error: **timeout** biasanya firewall, **`Permission denied (publickey,password)`** artinya key-nya belum diterima di file yang benar.

## Pelajaran 3: Lag? Pecah Dulu Jadi Dua Sumbu

Saat remote terasa lambat, jangan langsung sentuh firmware. Pisahkan dua kemungkinan — jalur dan perangkat — karena obatnya berbeda.

**Sumbu jalur.** Cek apakah koneksinya *direct* atau *relay*:

```
$ tailscale ping kvm-box
pong from kvm-box via DERP(sin) in 38ms
pong from kvm-box via DERP(sin) in 34ms
direct connection not established
```

Output di atas kami ambil dari host produksi saat menulis artikel ini: paket masih **lewat server DERP (relay)**, bukan koneksi langsung. Menurut [dokumentasi Tailscale](https://tailscale.com/docs/reference/connection-types), relay selalu jadi *fallback* ketika NAT traversal gagal, dan koneksi langsung hampir selalu lebih rendah latensi. Kalau status bar KVM juga menampilkan penanda relay, bottleneck-nya ada di jalur — pastikan akses pakai IP Tailscale, dan jangan blokir UDP port 41641 supaya negosiasi direct bisa berhasil.

**Sumbu perangkat.** KVM adalah komputer ARM kecil; dia gampang jenuh, dan **jenuh saja sudah cukup** untuk bikin gambar patah-patah. Tiga angka yang kami periksa:

- `cat /proc/loadavg` — kalau load lebih besar dari jumlah core (RM10 sekitar 4 core), perangkat sedang kepayahan.
- proses `gl-pion` (daemon WebRTC/P2P) — pernah mengakumulasi **100+ jam CPU** kalau tidak pernah di-restart.
- `cat /sys/class/thermal/thermal_zone0/temp` — 70 °C ke atas = panas.

Fix murah dulu: tutup window remote yang menganggur, restart `gl-pion`. Firmware paling akhir, bukan paling awal.

## Pelajaran 4: Jangan Flash Firmware Saat Sedang Dibutuhkan

Flash firmware membuat relay/KVM **drop sejenak** — berarti akses level hardware ke mesin yang dicolok ikut putus, tepat di momen ketika kita paling membutuhkannya. Jadwalkan di jendela yang aman, backup konfigurasi dulu, dan pastikan tidak ada proses kritis yang sedang berjalan di mesin target.

## Kesimpulan

IP-KVM bukan perangkat mewah untuk pamer homelab; dia **asuransi**. Kami tetap pakai SSH untuk kerja harian (lihat perbandingan jalur remote di [Tailscale vs Cloudflare Tunnel](/posts/tailscale-vs-cloudflare-tunnel/)), dan **monitoring** seperti [Komari](/posts/komari-monitor-server-jebakan/) untuk tahu lebih dulu kalau ada host yang diam. Tapi ketika semua jalur lunak sudah mati, KVM yang menentukan apakah masalah selesai dalam 10 menit atau menunggu orang datang ke lokasi.

Kalau Anda punya mesin yang tidak boleh mati lama — server di kantor, Mac mini di rumah, NAS yang menyimpan data penting — IP-KVM layak masuk daftar belanja. Untuk yang ingin paham lebih dalam soal tumpukan software di baliknya (kvmd, ustreamer, janus), [PiKVM Handbook](https://docs.pikvm.org/) adalah referensi open-source terbaik.

Punya pengalaman beda soal IP-KVM atau relay Tailscale? Tulis di komentar — kami baca semua.

— Chokdi 🐷 · Content Studio · 2026
