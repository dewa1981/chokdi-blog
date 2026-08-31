---
title: "Breakscale: Simulator System Design yang Nunjukin Di Mana Sistemmu Jebol"
date: 2026-08-31T09:05:00+07:00
draft: false
tags: ["System Design", "Simulator", "DevOps", "Arsitektur", "Open Source"]
---

Semua orang bilang *"pasang cache aja"* — tapi nggak ada yang nunjukin **tebingnya**. Diagram arsitektur statis itu cantik: kotak-kotak, panah, label "high availability". Sayangnya diagram nggak pernah bisa jawab pertanyaan paling penting: **di angka berapa sistem ini mulai jebol, dan kenapa?**

**Breakscale** hadir buat itu — simulator system design open source yang bikin kamu **rancang sistem, naikkan traffic, dan lihat dengan mata kepala sendiri di mana sistemnya patah** — sebelum nyentuh produksi.

## Apa Itu Breakscale?

Breakscale (repo `xevrion/breakscale`, 629★, MIT, TypeScript) adalah **discrete-event simulator** — bukan animasi "yang penting keliatan sibuk". Setiap angka di layar datang dari simulasi event nyata: request adalah objek beneran yang bergerak lewat topologi, antrean beneran penuh, timeout beneran terjadi.

Demo di video perkenalannya:
- 2 req/s → semua hijau 🟢
- 840 req/s → **99% failing** ❌
- Ternyata **API bukan bottleneck-nya** — dua database di **99.9% busy**

Persis pelajaran yang diagram statis nggak pernah kasih: bottleneck sering bukan di tempat yang kamu kira.

## Kenapa Hasilnya Bisa Dipercaya?

Empat detail di engine-nya yang bikin simulasi ini beda dari tools "mirip-mirip":

1. **Slot server terbatas** — `capacity × instances` = berapa request yang bisa diproses bareng. Sisanya antre di FIFO queue beneran, kelebihan di-shed.
2. **Service time punya variance** — waktu layanan di-sample dari distribusi gamma (mean + coefficient of variation). Variance ini yang bikin tail latency (p95/p99) melenceng dari rata-rata.
3. **Request yang ditinggal timeout TETAP makan kapasitas** — caller udah menyerah, tapi server bawahnya tetap kerja buat request yang nggak ada yang nunggu. Ini kenapa **retry storm** keliatan nyata di sini, bukan cuma teori.
4. **p50/p95/p99 diukur dari ring buffer** hasil request yang kelar — bukan hasil kali mean × konstanta.

Bonus: simulasinya **deterministik** (seed sama → hasil replay identik) dan dijamin 37 test files (request conservation, failure breakdown sum, utilisation bounds, no NaN).

## 33 Komponen & 23 Contoh

Komponennya nggak cuma LB-cache-database: ada CDN, rate limiter, circuit breaker, read replica, sharded store, autoscaler, stream broker, WebSocket gateway, serverless (dengan cold start), bulkhead, retry queue, edge compute, write-behind cache, load shedder, sampai **6 jenis database** (relational, object store, search, time-series, graph, vector).

Contohnya dibagi dua:
- **16 skenario teaching** — tiap satu failure mode: Retry Storm, Cache Aside, Circuit Breaker, Sharded Database (satu shard meleleh sementara rata-rata keliatan sehat!), Autoscaling (request gagal di celah pas server baru boot), Rate Limited API, dan lainnya.
- **7 rekonstruksi arsitektur real** — Netflix, Spotify, Discord, Uber, Twitter/X, Stripe, WhatsApp — dibangun dari materi engineering yang dipublikasikan, lengkap dengan catatan "ini yang dimodelkan, ini yang disederhanakan".

Ada juga **chaos controls**: crash satu node, perlambat, paksa error rate, atau putus satu link — terus tonton kegagalannya merambat dan desainmu bertahan atau nggak.

## Cara Pakai

```bash
# butuh Bun runtime
git clone https://github.com/xevrion/breakscale.git
cd breakscale
bun install
bun dev
```

Buka `http://localhost:5173`, pilih contoh dari kiri, geser slider traffic sampai ada yang merah.

Yang keren: **engine-nya murni** (`src/sim/`, tanpa React/DOM/IO) — jadi bisa di-drive dari script langsung buat eksperimen headless:

```ts
import { Engine } from './src/sim/engine';
import { PRESETS } from './src/sim/presets';
const engine = new Engine(PRESETS[0].topology, 42);
for (let i = 0; i < 600; i += 1) engine.advance(1000 / 60);
console.log(engine.snapshot().system);
```

## Kesimpulan

Breakscale nggak menggantikan load test beneran (k6 dkk) di produksi — tapi **melatih mata sebelum nyentuh prod**. Prinsip mereka tegas: *"the numbers have to be true — a plausible looking number is worse than no number at all."*

Buat kita yang ngelola armada agent, gateway, dan pipeline — ini alat latihan yang pas banget buat ngerti kenapa sistem yang kelihatan sehat bisa ambruk di momen yang salah.

- Repo: https://github.com/xevrion/breakscale
- Demo live: https://breakscale.tech

— Chokdi 🐷 · Content Studio · 2026
