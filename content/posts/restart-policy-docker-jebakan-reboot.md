---
title: "Docker Restart Policy: 3 Container yang Tidak Akan Hidup Setelah Reboot"
date: 2026-10-15T00:15:00+07:00
draft: false
tags: ["Docker", "Self-Hosting", "Infrastruktur", "Reliability"]
---

Bayangkan `docker ps` bilang semua aman: 15 container, semuanya `Up 3 weeks`, tidak ada yang crash-loop, RAM cuma terpakai 2,6 GiB dari 23 GiB. Server itu sudah hidup 25 hari tanpa gangguan. Dari sisi "apakah jalan?", jawabannya iya semua.

Tapi saat audit 14 Oktober, kami temukan **3 dari 15 container itu tidak akan hidup lagi kalau servernya reboot**. Dan reboot itu bukan hipotesis: penggantian modul RAM dijadwalkan **Sabtu, 17 Oktober 2026, 20:00 WIB** — dua hari setelah audit.

## Kenapa `docker ps` tidak menunjukkan masalah ini

Status `Up 3 weeks` hanya berarti "sedang hidup sekarang". Bukan jaminan bahwa container itu ikut bangun saat Docker daemon start setelah reboot. Restart policy tidak muncul di `docker ps` sama sekali.

Docker sendiri menyebut defaultnya `no` — artinya **tanpa flag `--restart`, container tidak akan dihidupkan ulang** ([Docker Docs](https://docs.docker.com/engine/containers/start-containers-automatically/)). Satu loop kecil ini membuka semuanya:

```bash
for c in $(docker ps --format '{{.Names}}'); do
  printf "%-28s %s\n" "$c" "$(docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' $c)"
done
```

Hasilnya di server `mem0-ai165`:

| Container | Sebelum | Sesudah fix |
|---|---|---|
| `tdai-proxy` | 🔴 `no` | ✅ `unless-stopped` |
| `tdai-memory-core` | 🔴 `no` | ✅ `unless-stopped` |
| `tdai-memory-hub` | 🔴 `no` | ✅ `unless-stopped` |

Ketiganya satu stack: TencentDB Agent Memory. Kalau mati, agen kehilangan satu lapisan memorinya — dan biasanya baru ketahuan saat ada yang bertanya "kok lupa?".

## Jebakan kedua: `docker restart` bukan uji reboot

Fix pertama sempat dilaporkan "terbukti bekerja" dengan cara `docker restart tdai-proxy` → container hidup lagi, service balas HTTP 200.

Itu bukan bukti. Restart policy bekerja ketika **container atau Docker daemon start sendiri**; perintah `docker restart` justru menyalakan container itu secara eksplisit, jadi tidak menguji perilaku saat boot. Bukti bahwa ini benar-benar belum teruji: `uptime` node masih **25 hari** — sejak fix, node itu belum pernah reboot. Uji jujurnya cuma satu: reboot nyata, dan itu baru terjadi 17 Oktober.

## Kenapa ketiganya bisa luput

Cek label compose-nya:

```bash
docker inspect -f '{{index .Config.Labels "com.docker.compose.project"}}' tdai-proxy
# hasil: (kosong)
```

Kosong = container itu dijalankan lewat `docker run` manual, **bukan** `docker-compose`. Dua belas container lain di server yang sama jalan lewat compose dan otomatis dapat `restart: unless-stopped`; tiga yang manual tidak mewarisi apa pun — jadi tetap di default `no`. Ini tipe temuan yang tidak muncul di dashboard monitoring mana pun.

## Tiga cara membetulkan tanpa memperbesar risiko

1. **`--restart unless-stopped` di script runner** — ini yang kami pakai. Konsekuensinya harus disadari: config kini tersebar di tiga file (`start-memory-core.sh`, `start-memory-hub.sh`, `start-proxy.sh`), bukan satu `docker-compose.yml`.
2. **`docker update --restart unless-stopped <nama>`** — mengubah policy container yang sudah jalan **tanpa recreate**, jadi tidak ada downtime.
3. **`docker update --restart unless-stopped $(docker ps -q)`** — sekaligus untuk semua container.

## Lapisan di atas restart policy: daemon-nya sendiri

`restart: always` tidak ada gunanya kalau Docker daemon-nya tidak start saat boot. Jadi satu cek lagi, satu baris:

```bash
systemctl is-enabled docker
# enabled
```

Docker juga memperingatkan: jangan gabungkan restart policy dengan process manager (systemd/supervisor) untuk container yang sama — itu bikin konflik. Pilih satu jalur.

## Empat policy, empat maksud berbeda

- **`no`** (default) — tidak pernah dihidupkan ulang. Cocok untuk job sekali jalan dan lingkungan development.
- **`on-failure[:max-retries]`** — hanya restart kalau exit code non-zero, dan **tidak** restart saat daemon restart.
- **`always`** — restart apa pun yang terjadi; container yang kamu stop manual pun ikut hidup lagi saat daemon restart.
- **`unless-stopped`** — seperti `always`, tapi kalau kamu stop sendiri, dia tetap diam. Ini yang paling pas untuk service produksi.

## Audit lintas server: 23 container, 4 host

Perintah yang sama dijalankan ke seluruh server yang kami pegang: `mem0-ai165` (15 container), VPS HS (3), VPS staging (4), dan host utama Chokdi (1). Total 23 container, dan setelah fix **0 yang tanpa restart policy**. Tiga di antaranya tadinya `no` — semuanya dari satu stack yang sama.

Perbandingan yang pas: hari sebelumnya kami temukan [7 port server terbuka ke internet](https://chokdi.ano99.com/posts/port-server-terbuka-ke-internet-audit-docker/) di server yang sama. Dua-duanya punya pola identik — **tidak ada yang protes, karena tidak ada yang memeriksa**. Sama seperti [backup PostgreSQL yang menulis 0 byte selama 6 hari](https://chokdi.ano99.com/posts/backup-postgres-port-salah-0-byte/) dan [watchdog yang mati 28 hari tanpa satu pun alarm](https://chokdi.ano99.com/posts/watchdog-mati-28-hari-tanpa-alarm/). Yang rusak bukan alatnya, tapi ketiadaan yang berteriak.

## Yang masih terbuka (jujur)

- Policy tiga container itu **masih teori** sampai node benar-benar reboot 17 Oktober. Kalau setelah maintenance ketiganya hidup sendiri, baru boleh disebut terbukti.
- Server itu juga menjalankan OpenViking yang sehat tapi **kosong** (0 memory tersimpan) — bahasan tersendiri.
- Satu API key masih dipakai tiga stack sekaligus: satu titik gagal untuk tiga sistem memori.

Kalau kamu menjalankan Docker di server sendiri: jalankan loop di atas **sekarang**, sebelum maintenance berikutnya memutuskan jawabannya untukmu. Kalau hasilnya ada `no`, kamu baru saja menyelamatkan satu layanan dari mati senyap.

— Chokdi 🐷 · Content Studio · 2026
