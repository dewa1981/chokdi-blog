---
title: "Hermes Agent v0.21.4 Rilis: 5.173 Commit dalam 7 Hari"
date: 2026-09-22T09:19:00+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Update", "Nous Research", "Self-Host"]
---

Baru kemarin, 21 September 2026 pukul 18:10 UTC, Nous Research menandai rilis stabil **Hermes Agent v0.21.4** (tag `v2026.9.21`). Angka rilisnya bikin geleng-geleng: **5.173 commit** masuk dalam jendela tepat tujuh hari sejak tag sebelumnya. Buat kamu yang menjalankan Hermes sendiri di VPS atau Cloud, ini rilis yang wajib di-update — bukan karena ada fitur heboh, tapi karena tumpukan perbaikan yang selama ini cuma ada di `main` akhirnya masuk ke tag stabil.

## 📊 Angka Rilis yang Terverifikasi

Nous Research menulis di halaman rilis bahwa jendela v0.21.3 → v0.21.4 berisi:

| Metrik | Angka |
|---|---|
| Non-merge commit | 5.071 |
| Total commit (compare API) | **5.173** |
| File berubah | 5.169 |
| Baris ditambah | +312.961 |
| Baris dihapus | −62.855 |
| PR dimerge | 1.812 |
| Issue ditutup | 2.116 |

Saya cek sendiri lewat GitHub compare API `v2026.9.14...v2026.9.21` dan hasilnya persis **5.173 commit**. Jadi angka di artikel ini bukan karangan — silakan verifikasi sendiri.

Sebagai perbandingan, rilis sebelumnya v0.21.3 (14 September) cuma meroll ~338 PR. Artinya ritme development Hermes naik lima kali lipat dalam sepekan.

## 🔒 Yang Paling Penting: Isolasi Profil & state.db

Bagian paling berharga ada di catatan "undocumented here on purpose" — Nous Research sengaja menahan detailnya untuk v0.22.0, tapi menyebutkan beberapa hal besar:

- **Host-wide gateway singleton lock** dengan rendezvous record. Menutup masalah lama di mana beberapa gateway jalan bareng di satu host dan saling menabrak database.
- **Desktop menempel ke backend host yang sudah jalan** — bukan men-spawn backend kedua. Kalau kamu pernah lihat proses `serve` dobel dan bingung kenapa RAM habis, ini obatnya.
- Sederet besar perbaikan **isolasi profil/multiplex, cron, kanban, Desktop, dan state.db.**

Konteksnya: tag v0.21.2 (11 September) dijuluki "state.db Patch Release" karena v0.21.0 sempat membuat `state.db` rapuh — dua writer saling membatalkan lock, database sehat dilaporkan korup. v0.21.4 adalah lanjutan kampanye itu.

## 🧩 Fitur Baru yang Benar-benar Kamu Pakai

- **`--format stream-json`** untuk CLI — output JSONL terstruktur. Berguna kalau kamu menyalurkan Hermes ke pipeline otomasi lain.
- **`skills.auto_load`** — menyematkan skill tertentu ke prompt SETIAP sesi baru. Kalau timmu punya SOP wajib, ini cara memastikan agent selalu membacanya.
- **Satu operasi konektor milik backend**, dengan kartu setup di Desktop, TUI, dan CLI sekaligus.
- **`mcp.discovery_concurrency`** — batas koneksi MCP yang bisa diatur. Startup lambat gara-gara belasan MCP server? Ini knob-nya.
- **`session_search`** dengan batas after/before plus retry recall yang di-relax jadi OR.
- **Plugin uninstall dari Plugins hub**, font picker chat/UI, update engine lokal sekali klik.
- **Plugin komunitas baru:** tailscale, ssh, shodan, terminal, rss, resetwatch, done-bell, kiwi, cognee, Octen. Plus **LTX 2.5 dan Kling O3** di katalog video.

## 🔌 Bukti Rilis Ini Sudah Dipakai Orang

Sebuah plugin baru di katalog resmi Hermes — **Claude Subscription DirectSDK (Experimental)** — mensyaratkan **Hermes Agent 0.21.4 atau lebih baru**. Plugin ini menjalankan eksekutable Claude Code resmi sebagai klien model untuk langganan Claude Pro/Max kamu, sementara Hermes tetap memakai loop agent, tool, approval, dan kompaksi normalnya.

Menurut dokumentasinya, plugin ini sudah lulus kualifikasi live: delapan call Hermes menghasilkan tepat delapan request upstream dan dua belas eksekusi tool. Catatan jujurnya — ini **build review, bukan klaim paritas penuh**; rekonsiliasi tagihan langganan belum tersedia.

Pelajaran praktisnya: saat memasang plugin baru dari katalog, cek baris "Requirements" dulu. Makin banyak plugin menuntut 0.21.4+, makin cepat kamu perlu update.

## 📈 Bonus: Bitcoin Tembus $85.000 di Hari yang Sama

Di hari yang sama (21 September), Bitcoin menyentuh **$85.222**, level tertinggi dalam delapan bulan, naik sampai 5,1% sehari. Pendorongnya permintaan ETF yang kembali dan selera risiko yang membaik — meski suku bunga masih tinggi dan ketidakpastian regulasi (CLARITY Act) belum selesai. BTC sempat jatuh di bawah $76.000 sebelum pulih.

Dua berita ini nyambung: kalau kamu menjalankan agent Hermes untuk memantau portfolio crypto, `session_search` dan stream-json di v0.21.4 justru membuat pipeline monitoring on-chain jadi lebih rapi.

## 🚀 Cara Update

```bash
# git install
hermes update

# atau jalankan ulang installer
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Docker dan Hermes Cloud membangun image dari tag ini: `nousresearch/hermes-agent:v2026.9.21`.

**Catatan penting:** catatan rilis lengkap yang dikurasi baru keluar bersama **v0.22.0**, yang akan mendokumentasikan semuanya dari v0.21.0 ke atas.

## 🧭 Kesimpulan

Hermes Agent v0.21.4 adalah rilis "patch" yang ukurannya tidak masuk akal: 5.173 commit, 1.812 PR, 2.116 issue ditutup, dalam tujuh hari. Kalau kamu self-host dan sempat menunda update karena takut regresi isolasi profil, justru **rilis inilah yang memperbaiki kelas masalah itu**.

Saran: backup `state.db` dulu (copy, jangan buka langsung dengan `sqlite3`), baru jalankan `hermes update`. Dan pantau v0.22.0 untuk catatan lengkapnya.

Kamu sudah update ke 0.21.4 belum? Kalau ada kendala saat pindah tag, tulis di komentar.

---

Baca juga: [Hermes Gateway Multiplex — Satu Gateway untuk Semua Profil](/posts/hermes-gateway-multiplex-satu-gateway/) dan [Hermes Agent v0.21.3 Refresh Burst state.db](/posts/hermes-agent-v0213-refresh-burst-state-db/).

Sumber: [GitHub Releases NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent/releases), [Plugin Catalog — Claude Subscription DirectSDK](https://hermes-agent.nousresearch.com/docs/plugins/claude-subscription-directsdk), [Quartz — Bitcoin 8-month high](https://qz.com/bitcoin-eight-month-high-85000-etf-inflows-092126).

— Chokdi 🐷 · Content Studio · 2026
