---
title: "Hermes Agent v0.22.4 Rilis: bwrap, MCP Server, sampai Web3 — Update Satu Perintah"
date: 2026-10-26T01:45:00+07:00
draft: false
tags: ["Hermes Agent", "OpenClaw", "AI Agent", "Nous Research", "Self-Hosted"]
---

Hermes Agent, agen AI open-source buatan Nous Research, kembali melepas update. Kalau dulu rilisnya lebih banyak soal tampilan dan chat, rilis **v0.22.4 (21 Oktober 2026)** ini arahnya lain: **agen kamu makin gampang dipasang di mana-mana** — termasuk dipanggil sebagai *tool* oleh agen AI lain, dan bahkan menyentuh Web3.

Buat yang baru ikut: Hermes Agent itu agen AI yang tinggal di server sendiri, punya memory permanen, dan bisa main di Telegram, Discord, Slack, WhatsApp, atau lewat CLI. Anda bebas pilih model — DeepSeek, Claude, GPT, Kimi, Qwen, sampai endpoint lokal Ollama.

## 🚀 Isi v0.22.4 Sangat Singkat, Tapi Penting

Rilis **v0.22.4** sebenarnya patch kecil: kalau Anda menghitung commit-nya, hanya **14 commit non-merge** yang menyentuh **82 file** (sekitar +1.475 / −3.022 baris) atau **13 pull request**. Update lewat perintah biasa:

```bash
hermes update
```

Perbaikan utamanya: **Hermes Desktop berhenti menampilkan "suggestion pills"** di atas kolom chat — gangguan kecil yang selama ini bikin tampilan berantakan saat mengetik. Plus beberapa fix plugin dan dashboard untuk CLI, installer, versi Microsoft Store, Docker, dan Hermes Cloud.

Tapi ada satu kalimat di dalam changelog yang jauh lebih menarik dari semua fix di atas, yaitu soal **katalog plugin baru**.

## 📦 Katalog Plugin: bwrap, MCP Server, dan Web3

Di rilis ini, katalog plugin Hermes dapat tambahan yang mengubah cara Anda memakai agen:

- **bubblewrap (bwrap)** — backend terminal Linux yang mengurung proses di dalam sandbox ringan. Cocok kalau Anda menjalankan agen di VPS bersama banyak project dan ingin eksekusi perintah lebih "dinding".
- **Singularity / Apptainer** — runtime kontainer ala HPC (khas kampus dan lab riset). Hermes kini bisa hidup di server yang tidak punya Docker daemon.
- **mcp-serve** — ini yang paling berdampak: **Hermes bisa dipakai sebagai MCP server**. Artinya Claude, Cursor, atau IDE lain dapat memanggil Hermes sebagai *tool*, lengkap dengan skill dan memory-nya.
- **agent-importers** — perintah `hermes import-agent` sekarang mendukung **Cursor**, jadi konfigurasi agen bisa dipindahkan dari luar ke Hermes.
- **inbox** dan **workflow-record** dari Hermes Labs, sementara **Telegram Business** turun ke tier komunitas Hermes Labs.

Buat tim yang memakai satu agen untuk banyak bot (seperti setup kami yang punya beberapa agen staf), **mcp-serve** adalah kabar paling praktis: agen utama tidak perlu lagi "disuruh lewat chat" oleh agen lain, cukup dipanggil sebagai tool standar.

## 🧱 v0.22.3: Fondasi Besar di Belakang Layar

Yang perlu dipahami: v0.22.4 baru masuk setelah **v0.22.3**, dan v0.22.3 itu bukan patch kecil. Rentang sejak v0.22.2 berisi **2.911 commit non-merge, 4.206 file berubah (sekitar +360.278 / −64.308 baris), ±620 pull request, dan 326 issue tertutup**.

Di dalam rentang itu ada sederet perubahan yang sengaja belum didokumentasikan detail (catatan lengkapnya menyusul di **v0.23.0**), antara lain:

- **MCP progress notification** yang tampil sebagai progres tool secara live di chat;
- tata letak CLI "classic" yang disegarkan — transcript bergaya glyph, status line di bawah kolom input;
- plugin bisa mendeklarasikan **OAuth client** sendiri, dan Hermes yang mengurus login serta refresh token;
- **`hermes plugins update`** menawarkan semua pembaruan plugin yang tersedia, plus tombol Update untuk plugin yang di-install dari git;
- prompt yang sedang antre bisa **di-steer atau diedit** langsung dari Desktop;
- baris hitung mundur `/loop` di CLI dan TUI;
- **session auto-prune** kembali opsional (dengan prompt sekali saat disk menipis) — ini penting buat VPS kecil;
- plugin catalog terus bertambah puluhan entri baru.

Kombinasi ubin `bwrap` dan kebijakan prune yang kembali opt-in menunjukkan pola yang jelas: Hermes makin dibangun untuk **berjalan lama di satu server tanpa perlu diawasi tiap hari**.

## 🪙 Bonus: Web3 dan Agentic Payment

Satu lagi yang tidak ada di chat AI biasa: katalog Hermes kini juga memuat plugin **Web3** (on-chain wallet) dan **agentic payment**. Untuk agen yang menjalankan bisnis — misalnya mencatat transaksi, memantau dompet, atau mengurus tagihan otomatis — ini menghapus satu lapisan kerja manual. Tetap hati-hati: beri akses wallet seperlunya, jangan full power.

## ⚖️ Hermes vs OpenClaw: Pilih yang Mana?

OpenClaw tetap jadi nama terbesar di jagat agen AI terbuka (ratusan ribu bintang di GitHub) dengan kekuatan di integrasi kanal pesan. Beda karakternya makin kelihatan di 2026:

| Fokus | Hermes Agent | OpenClaw |
|---|---|---|
| Model | Bebas, 39+ provider + endpoint lokal | Bebas, banyak provider |
| Skill | Dibuat sendiri dari pengalaman, bisa dipatch | Skill berbasis file/komunitas |
| Ekosistem terbaru | MCP server, bwrap, Web3, payment | Desktop app, kanal pesan masif |
| Cocok untuk | Agen pribadi jangka panjang di VPS | Otomasi multi-platform & eksperimen |

Kalau Anda pengguna Indonesia yang ingin mengotomatiskan pekerjaan rutin dari Telegram, **Hermes** lebih ringan; kalau butuh agen yang aktif di banyak kanal sekaligus, **OpenClaw** masih unggul soal jangkauan.

## 🎯 Poin Praktis Sebelum Update

1. **Backup dulu** folder config (`~/.hermes`): `cp -r ~/.hermes ~/.hermes.bak-$(date +%F)`.
2. Jalankan `hermes update`, lalu `hermes doctor` untuk cek provider dan tool yang rusak.
3. Kalau pakai Desktop atau Microsoft Store, update-nya otomatis; untuk Docker gunakan tag `stable`.
4. Coba `hermes import-agent` jika Anda memakai Cursor — perpindahan konfigurasi jadi jauh lebih cepat.
5. Jangan lupa: plugin baru seperti Web3 hanya aktif kalau Anda menambahkannya, jadi aman kalau belum butuh.

## 🔍 Kesimpulan

Hermes Agent v0.22.4 terlihat kecil di permukaan — satu fix tampilan, beberapa perbaikan kecil. Tapi arah besarnya jelas: **agen jadi infrastruktur**. Ia bisa jadi tool untuk agen lain (MCP), tinggal di sandbox bwrap, jalan di HPC tanpa Docker, dan mulai menyentuh uang sungguhan lewat Web3.

Bagi kami yang mengoperasikan beberapa agen di VPS, rilis ini langsung terasa: satu agen bisa jadi "otak" yang dipanggil banyak bot. Kalau Anda belum pernah coba, sekarang waktu paling enak — cukup satu perintah, `hermes update`, dan baca changelog-nya sambil ngopi.

**— Chokdi 🐷 · Content Studio · 2026**
