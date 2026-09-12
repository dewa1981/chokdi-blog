---
title: "Hermes Agent: Satu Gateway untuk Semua Profil Bot — `hermes gateway migrate --multiplex`"
date: 2026-09-12T18:20:00+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Self-Hosted", "Update", "Multi-Agent"]
---

Kalau kamu menjalankan Hermes Agent dengan lebih dari satu profil — bot pribadi, bot kerja, bot cron laporan, bot staff — sampai pekan ini tiap profil itu punya **proses gateway sendiri**: satu unit systemd sendiri, satu PID file, sering satu port sendiri. Di VPS kecil, menjalankan tujuh profil berarti tujuh hal yang harus kamu start, monitor, dan restart satu per satu.

Pull request **#108928** yang merge pada 12 September 2026 mengubah aturan mainnya: sekarang ada perintah resmi untuk memindahkan instalasi multi-profil ke **satu gateway multiplex** — dan `hermes update` bisa melakukannya otomatis. Berikut bedah lengkapnya.

## Apa yang sebenarnya baru?

Sebenarnya mode multiplex (`gateway.multiplex_profiles: true`) sudah ada di Hermes Agent sebelumnya. Yang baru adalah **jalur migrasinya** — dulu kamu harus mematikan gateway tiap profil secara manual, menghapus service, lalu menyalakan flag sendiri. Sekarang ada dua perintah:

```bash
hermes gateway migrate --multiplex --dry-run   # lihat rencana, nol perubahan
hermes gateway migrate --multiplex --yes       # eksekusi
hermes gateway migrate --standalone            # rollback dari manifest
```

Perintahnya idempoten: kalau instalasimu sudah pakai multiplex, dia menolak dengan pesan "already multiplexing" tanpa menyentuh apa pun.

Bagian yang paling penting buat yang males ribet: `hermes update` sekarang **memigrasi otomatis** kalau tidak ada penghalang. Syaratnya tiga: minimal dua profil, minimal satu gateway per-profil yang jalan, dan multiplex masih mati. Kalau terhalang, dia tidak memaksa — dia mencetak blok peringatan berisi apa yang harus dibetulkan plus perintah satu baris untuk menjalankannya manual. Aman untuk server headless karena jalur ini tidak pernah bertanya interaktif.

## Apa yang dikerjakan saat migrasi

Coba lihat contoh dry-run di PR-nya:

```text
Migration plan (dry run — nothing changed)
  profile      gateway pid   service
  default      -             none
  coder        531712        systemd (user)
  ops          531713        systemd (user)

  Steps:
  - coder: stop pid 531712 + uninstall systemd (user)
  - ops: stop pid 531713 + uninstall systemd (user)
  - default: set gateway.multiplex_profiles: true
  - default: start the gateway via systemd, verify it serves 3 profiles
  - record removed services in <home>/gateway_migration.json
```

Tiga hal yang perlu dicatat:

1. Service tiap profil sekunder **dihentikan dan di-uninstall**, tapi dicatat di manifest `gateway_migration.json` — jadi rollback (`--standalone`) bisa memasang kembali service dan menyalakannya persis seperti sebelumnya.
2. Flag ditulis lewat config API, bukan mengedit YAML manual.
3. Gateway default dinyalakan di **service manager yang sama** dengan yang dipakai profil sekunder, lalu diverifikasi lewat `served_profiles` di `gateway_state.json` — jadi kita tahu semua profil benar-benar terlayani, bukan cuma "kelihatannya jalan".

## Dua hal yang bisa memblokir migrasi

Migrasi dirancang menolak dengan bersih kalau berisiko. Ada dua blocker (tidak ada yang berubah kalau kena):

| Blocker | Kenapa berbahaya | Perbaikan |
|---|---|---|
| Kredensial `(platform, credential)` yang sama dipakai dua profil | Dua profil memperebutkan bot token yang sama → pesan bisa nyasar | Hapus token dari salah satu profil, atau simpan di default dan routing chat-nya pakai `profile_routes` |
| Profil sekunder menyalakan platform port-binding tanpa ingress `/p/<profile>/` | Listener bisa bentrok / profil terlewat | Pindahkan konfigurasi platform itu ke profil default saja |

Platform port-binding yang dimaksud: `webhook`, `api_server`, `msgraph_webhook`, `feishu`, `wecom_callback`, `bluebubbles`, `sms`, `whatsapp_cloud`, `line`, dan `teams`. Kalau profil sekunder menyalakan salah satunya, seluruh profil itu **di-skip** (profil lain tetap jalan) dengan pesan yang menyebut profil dan platform yang bermasalah.

## HTTP inbound kini lewat `/p/<profile>/`

Ini perubahan konsekuensi yang paling terasa buat yang punya webhook atau API server. Alih-alih port kedua, traffic profil sekunder masuk ke listener default dengan prefix:

```text
POST http://host:8644/webhooks/<route>            # default
POST http://host:8644/p/coder/webhooks/<route>    # profil "coder"
```

Autentikasi mengikuti profil di URL: request ke `/p/coder/...` harus memakai `API_SERVER_KEY` dari `~/.hermes/profiles/coder/.env`, dan key listener default akan ditolak. Prefix profil yang tidak dikenal mengembalikan `404`. Route webhook tanpa `profile:` tetap jadi route default dan tidak bisa diakses lewat prefix profil — jadi isolasi antar profil tetap ketat. Ini nyambung dengan penguatan isolasi multi-profil yang masuk di [v0.21.2 patch state.db](/posts/hermes-agent-v0212-patch-state-db/).

## Multiplex atau tetap satu proses per profil?

| Pilih multiplex kalau… | Tetap satu proses per profil kalau… |
|---|---|
| Banyak profil low-traffic di satu VPS/container | Butuh isolasi level proses (memori, crash domain) |
| Males kelola N unit systemd, N port, N PID file | Mau restart satu profil tanpa menyentuh yang lain |
| Mau satu hal untuk di-start, dipantau, dan di-restart | Profil itu menangani traffic besar |

Gateway per-profil mandiri **tetap didukung** — ada flag `--force` untuk sengaja menjalankannya. Jadi ini jalur migrasi, bukan penghapusan fitur.

## Dashboard dan yang belum didukung

Dashboard Hermes dapat endpoint `GET /api/gateway/migrate/plan` (bentuk JSON-nya sama dengan plan CLI) dan `POST /api/gateway/migrate` yang menjalankan CLI-nya detached plus log `gateway-migrate.log`. Halaman System → kartu Gateway hanya menampilkan tombol "Migrate to a single multiplexed gateway" untuk instalasi multi-profil yang eligible, dan tombolnya nonaktif sambil menampilkan daftar blocker kalau tidak.

Yang belum dicakup otomatis: container **s6** dan **Windows Scheduled Tasks** — keduanya ditolak dengan panduan, bukan dipaksa.

## Kesimpulan

Ini contoh khas rilis Hermes Agent belakangan ini: bukan fitur yang bikin heboh di timeline, tapi menghapus kerja manual yang paling bikin capek — mengelola fleet bot. Kalau kamu punya dua profil atau lebih di satu mesin, jalankan `hermes gateway migrate --multiplex --dry-run` dulu, baca plannya, baru eksekusi. Rollback-nya satu perintah, jadi risikonya kecil.

Detail lengkapnya ada di [PR #108928](https://github.com/NousResearch/hermes-agent/pull/108928) dan [dokumentasi multi-profile gateways](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways). Kalau kamu menjalankan fleet agent sendiri, berapa profil yang kamu kelola sekarang? Tulis di komentar, ya.

— Chokdi 🐷 · Content Studio · 2026
