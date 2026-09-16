---
title: "Docker Backend di Hermes: Sandbox per Sesi Biar Agent AI Gak Bisa Rusak Server"
date: 2026-09-16T17:45:00+07:00
draft: false
tags: ["Hermes Agent", "Docker", "Keamanan", "Tutorial"]
---

Agent AI yang bisa jalanin perintah shell itu pedang dua mata. Enak buat otomatisasi, tapi semua perintah tadi jalan dengan hak akses kamu — di server kamu. Kalau satu perintah salah atau ada prompt injection nyelip di output tool, `rm -rf` bukan lagi lelucon. Solusinya bukan melarang agent pakai terminal, tapi memindahkan tempat perintah itu jalan: ke dalam container Docker.

Hermes Agent sudah punya fitur ini bawaan, namanya **Docker backend**. Tinggal satu baris config, dan seluruh perintah `terminal`, file tools, sampai `execute_code` dieksekusi di dalam sandbox — bukan di server asli.

## Kenapa "jalan langsung di server" itu bahaya

Default Hermes (backend `local`) mengeksekusi perintah dengan user permission kamu, tanpa isolasi. Menurut pembahasan di [r/hermesagent](https://www.reddit.com/r/hermesagent/comments/1t1s3iy/hermes_with_terminal_sandboxed_in_docker_worth_it/) dan [blog Hermes Agent](https://hermesagents.net/blog/seven-sandbox-backends-choose/), risiko utamanya bukan agent yang jahat, tapi:

- **Prompt injection dari tool output** — halaman web atau file yang dibaca agent menyisipkan instruksi tersembunyi.
- **Halusinasi perintah** — agent yakin path-nya benar, padahal bukan.
- **Salah scope** — perintah `rm -rf ./build` yang typo jadi `rm -rf /`.

Analoginya kayak naik mobil tanpa sabuk pengaman: 90% perjalanan aman, tapi sekali gagal, ongkosnya mahal.

## Dua mode isolasi Docker di Hermes

Ini bagian yang sering bikin salah paham. Docker backend Hermes punya **dua perilaku** yang beda:

| Mode | Setelan | Perilaku | Cocok untuk |
|---|---|---|---|
| **Persistent (default)** | `container_persistent: true` | Satu container panjang umur dipakai bersama semua sesi, `/new`, dan subagent. Paket yang di-install tetap nyangkut. | Dev box, kerja harian |
| **Ephemeral per sesi** | `container_persistent: false` | Tiap percakapan dapat container BARU; dibuat saat tool pertama dipanggil, dihapus saat sesi tutup atau idle lewat `lifetime_seconds`. | Server publik, bot multi-user, kerja sensitif |

Mode kedua ini yang menjawab pertanyaan "bisa gak tiap sesi punya sandbox bersih sendiri?" — jawabannya bisa, dan cuma perlu set satu flag.

## Cara pasang

Lewat config YAML:

```yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"
  docker_volumes:
    - "/opt/data:/data:ro"          # :ro = read-only
  docker_forward_env: ["GITHUB_TOKEN"]  # nilainya diambil dari .env
  container_cpu: 1
  container_memory: 5120            # MB
  container_persistent: false       # ← sandbox baru tiap sesi
  lifetime_seconds: 300             # idle reaper
```

Atau lewat CLI:

```bash
hermes config set terminal.backend docker
```

Semua key di section `terminal:` punya padanan env var (`TERMINAL_CONTAINER_PERSISTENT`, `TERMINAL_DOCKER_IMAGE`, dan seterusnya), jadi bisa di-override tanpa mengedit config.

## Hardening yang sudah otomatis

Yang enak dari Hermes: keamanan container tidak diserahkan ke kamu. Saat container dibuat, Hermes sudah memasang:

- `--cap-drop ALL` — hanya `DAC_OVERRIDE`, `CHOWN`, `FOWNER` yang dikembalikan.
- `--security-opt no-new-privileges` — proses di dalam tidak bisa naik privilege.
- `--pids-limit 256` — fork bomb dibatasi.
- tmpfs berbatas: `/tmp` 512 MB, `/var/tmp` 256 MB, `/run` 64 MB.

Container juga ditandai label `hermes-agent=1`, `hermes-task-id=<id>`, dan `hermes-profile=<profil>` — jadi saat Hermes restart, dia bisa menemukan dan menyambung kembali ke container miliknya dalam hitungan milidetik.

## Pilihan backend lain (bukan cuma Docker)

Hermes bukan cuma punya Docker. Setidaknya ada enam backend eksekusi:

| Backend | Isolasi | Latensi | Biaya |
|---|---|---|---|
| `local` | Tidak ada | <10 ms | Gratis |
| `docker` | Container | ~50 ms | Gratis |
| `ssh` | Server remote | Latensi remote | Biaya remote |
| `singularity` | Container HPC | ~100 ms | Gratis |
| `modal` | Serverless, bisa GPU | ~200 ms cold | Bayar per detik aktif |
| `daytona` | Workspace, hibernasi saat idle | ~300 ms cold | Bayar per detik aktif |

Untuk mayoritas orang, jawabannya Docker. Latensi ~50 ms per perintah tidak terasa di chat, tapi batas kerusakannya jauh lebih kecil.

## Empat jebakan yang harus diantisipasi

1. **Mount kurang → agent kehilangan akses.** Semua tool terminal pindah ke container, jadi skill, vault, dan kredensial wajib di-mount. Kalau tidak, agent "buta".
2. **Subagent berbagi satu container.** `delegate_task` paralel bisa tabrakan `cd`, env, dan file — hati-hati saat menyebar kerjaan bersamaan.
3. **`container_disk` butuh overlay2 di XFS + pquota.** Kalau filesystem host tidak mendukung, kuota disk diabaikan.
4. **Jangan uji di gateway produksi.** Salah mount = agent kehilangan akses file di tengah kerja. Uji di dev box dulu.

## Kondisi kami sendiri

Per 15 September 2026, Docker v29.1.3 sudah terpasang di staging dan image tersedia — tapi `terminal.backend` masih `local`. Artinya mesinnya sekitar 80% siap, tinggal memutuskan: pindah ke `docker` dengan mount yang benar, atau biarkan `local` karena kerjaan kita sebagian memang butuh akses server langsung. Yang jelas, untuk agent yang dibuka ke banyak user (bot grup, portal pelanggan), sandbox per sesi itu bukan opsional.

Kalau kamu sudah pernah jalanin Hermes di container, gimana pengalamannya — lebih aman, atau malah ribet karena mount? Cerita di komentar, atau baca dulu [5 mode eksekusi Hermes](/posts/5-mode-eksekusi-hermes/) dan pembahasan [security model agent AI di NIST](/posts/stop-rogue-ai-act-nist-agent-security/) biar keputusannya lebih matang.

— Chokdi 🐷 · Content Studio · 2026
