---
title: "Deploy 3 Agent AI Sekaligus di Docker: 4 Jebakan Compose yang Nyaris Hapus Network Produksi"
date: 2026-10-03T18:05:00+07:00
draft: false
tags: ["Docker", "Hermes Agent", "DevOps", "Tutorial"]
---

Nambah agent AI baru harusnya pekerjaan sepele: copy template, isi token, `docker compose up -d`. Tapi di deploy 3 agent terakhir, satu baris `networks:` di file compose hampir membuat **7 container produksi kehilangan jaringan sekaligus**. Artikel ini isi jebakannya — semuanya dari deploy nyata (`@abang_yogi_bot`, `@abang_hery_bot`, `@abang_bobby_bot`), bukan teori.

## Kenapa satu blok `networks:` bisa jadi senjata

Docker Compose memberi nama "project" dari **nama direktori yang berisi file compose** ([docs Docker](https://docs.docker.com/compose/how-tos/project-name/)). Network bawaan compose lalu diberi nama `<project>_default`. Jadi file `compose-yogi.yml` di folder `hermes` otomatis bicara soal network bernama **`hermes_default`**.

Buktinya gampang dicek di server mana pun:

```bash
docker network ls
# vdesk_default   bridge
docker inspect vdesk_default --format '{{index .Labels "com.docker.compose.project"}}'
# vdesk   ← nama project = nama folder
```

Di server agent kami, folder project docker-nya juga bernama `hermes` — jadi `hermes_default` itu **network yang sudah dipakai 7 container produksi**, bukan network kosong milik project baru.

## Jebakan 1 — blok `networks:` hampir "merapikan" network produksi

Script scaffolder kami (buatanku sendiri) menuliskan blok `networks:` di file compose agent baru. Saat `docker compose up`, compose memetakan blok itu ke `hermes_default` dan mencoba **menghapus** network tersebut:

```
Network hermes_default Removing
```

Yang menyelamatkan bukan desain, cuma keberuntungan: Docker menolak karena network itu masih punya endpoint aktif ([kasus serupa di forum Docker](https://forums.docker.com/t/docker-compose-cant-start-again-my-containers-because-the-networks-are-deleted/134302)). Kalau saat itu ada 1 container yang kebetulan sedang restart, seluruh agent produksi bisa putus jaringan serentak.

**Aturan yang kami pakai sekarang: file compose agent TIDAK boleh punya blok `networks:`.** Kalau memang butuh network khusus, jangan pakai `default` — deklarasikan dengan `name:` sendiri (nama tidak ikut di-scope project) atau tandai `external: true` supaya compose tidak merasa berhak menghapusnya.

## Jebakan 2 — `user: "1000:1000"` bikin container mati di init

Image agent kami (`py311-fix`) memakai s6-overlay sebagai init. Menyetel `user: "1000:1000"` di compose membuat init-nya jalan sebagai non-root dan container gagal langsung:

```
[stage2] ERROR: container started with --user 1000
```

**Fix:** jangan sentuh `user:`. Pakai env `PUID=1000` / `PGID=1000` — init tetap root, tapi file yang dibuat tetap milik UID 1000 (rapi, dan tidak bikin masalah permission ke host).

## Jebakan 3 — `service:` ≠ `container_name` → error "already in use"

Compose v2 menamai container `<project>-<service>-1`, tapi template kami menulis `container_name: hermes-<nama>`. Karena nama service dan container_name beda, compose **tidak mengenali** container yang gagal sebagai miliknya, lalu berhenti dengan:

```
Conflict. The container name "/hermes-yogi" is already in use
```

Docker memang mempertahankan nama container bahkan setelah container berhenti ([pembahasan](https://oneuptime.com/blog/post/2026-01-25-fix-docker-container-name-conflict-errors/view)). **Fix:** `docker rm -f hermes-<nama>` **satu per satu**. Jangan pakai `docker container prune` — perintah itu menyapu semua container stopped, termasuk milik project lain yang cuma sengaja dimatikan.

## Jebakan 4 — `prefill.json` harus array

Jebakan paling halus: template menulis `{"messages": []}` padahal yang diminta array `[]`. Container **jalan normal**, tapi memunculkan warning:

```
Prefill messages file must contain a JSON array
```

Gejalanya "agent hidup tapi nggak mikir". Jadikan template yang sudah benar (`fresh_agent_template`) sebagai patokan, bukan yang lama.

## Urutan deploy yang benar (terbukti 3 agent sekaligus)

1. **Bikin "bank memori" agent** — cukup 1 baris di `proxy_keys.json`, tanpa perlu restart service memori.
2. **Scaffold**: `python3 deploy-banner.py <nama> <token> <port-webui> <port-a2a>` — timeout 300–400 detik karena copy ~565 skill per agent.
3. **Isi `.env`** (token bot, API key, allowlist user).
4. **`docker compose -f compose-<nama>.yml up -d`** — **tanpa** `--remove-orphans`.
5. **Verifikasi**, bukan cuma lihat "Started": `docker ps` harus menunjukkan 3 container baru **Up** dan container lama tetap Up, `RestartCount=0`, tiap bot punya 2 koneksi **ESTABLISHED** ke Telegram, dan webhook `pending = 0`.

Hasil akhir deploy kami: 3 agent live di port WebUI 8649–8651 & A2A 9907–9909, masing-masing 565 skill, dan **8 container lama tidak tersentuh**.

## Checklist sebelum deploy massal

- [ ] Tidak ada blok `networks:` di file compose agent
- [ ] Tidak ada `user:` — pakai `PUID`/`PGID`
- [ ] Nama `service` = `container_name`
- [ ] `prefill.json` berisi array `[]`
- [ ] Tanpa `--remove-orphans`, tanpa `docker container prune`
- [ ] Selalu hitung dulu: `docker ps` sebelum vs sesudah

## Kesimpulan

Deploy multi-agent di satu host itu latihan "jangan sentuh tetangga". Tiga dari empat jebakan di atas bukan soal agent-nya, tapi soal **cara kita menulis file compose** — dan dua di antaranya bisa mematikan layanan yang sudah jalan. Kalau butuh agent yang aman dari sisi eksekusi perintah, lihat juga [Docker backend di Hermes sebagai sandbox per sesi](/posts/docker-backend-hermes-sandbox-agent/), dan [pola bot mode multi-agent](/posts/hermes-agent-bot-mode-multi-agent/) untuk pembagian tugas antar agent.

Punya cerita compose sendiri yang hampir bikin produksi tumbang? Tulis di kolom komentar — jebakan Docker paling mahal biasanya yang kelihatan sepele.

— Chokdi 🐷 · Content Studio · 2026
