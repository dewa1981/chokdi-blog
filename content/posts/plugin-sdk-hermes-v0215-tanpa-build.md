---
title: "Plugin SDK Hermes v0.21.5: Bikin Plugin Desktop Tanpa Build, Tanpa Clone Repo"
date: 2026-10-07T17:24:00+07:00
draft: false
tags: ["Hermes Agent", "AI", "Nous Research", "Plugin", "Developer", "Open Source"]
---

Bayangkan kamu mau nambah fitur di aplikasi agent AI kamu — satu panel kecil, satu tombol di status bar, satu halaman baru. Cara lama: clone repo, baca 40 file, `npm run build`, lalu berdoa semoga patch-nya tidak bentrok saat update berikutnya. Cara baru di **Hermes Agent v0.21.5**: tulis **satu file JavaScript**, simpan, selesai.

Nous Research menandai rilis **Hermes Agent v0.21.5** dengan tag `v2026.9.24` pada 24 September 2026. Ini patch release, tapi bobotnya berat: **~460 pull request** digabung dari v0.21.4, dan salah satu isi terpentingnya adalah **Desktop plugin SDK wave** — gelombang API yang mengubah Hermes Desktop dari aplikasi biasa jadi **platform yang bisa diperluas**.

## 🧩 Apa Itu Desktop Plugin SDK?

Menurut [dokumentasi resmi Hermes](https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk), desktop plugin itu **satu file ESM** yang mengekspor objek `HermesPlugin`. File itu cuma mengimpor **satu modul** — `@hermes/plugin-sdk` — dan langsung dapat semuanya:

- **Live state aplikasi** (sesi aktif, turn-busy, cwd, status socket gateway, model, profil, viewport)
- **Gateway JSON-RPC door** — jalur yang dipakai aplikasi sendiri buat akses sesi, config, skills, dan cron
- **Namespace backend REST/socket sendiri** (lewat `/api/plugins/` kalau kamu bawa `plugin_api.py`)
- **React Query + UI kit bawaan aplikasi**, jadi tampilan plugin kamu otomatis senada dengan UI asli

Yang paling enak: **tidak ada repo clone, tidak ada `npm run build`, tidak ada patching source aplikasi**. Cukup taruh file di:

```
~/.hermes/desktop-plugins/hello/plugin.js
```

Aplikasi memantau folder itu, memuat file dalam beberapa detik, dan **hot-reload setiap kali kamu simpan**. Kalau gagal, muncul toast yang menyebut error-nya — perbaiki, simpan, jalan lagi. Nama folder **harus sama** dengan `id` plugin.

## 🛠️ Plugin Pertama dalam 10 Baris

Ini contoh minimal dari dokumentasi resmi — satu panel di sisi kanan plus satu chip di status bar:

```js
import { host, haptic, useValue } from '@hermes/plugin-sdk'
export default {
  id: 'hello',
  name: 'Hello',
  register(ctx) {
    ctx.register({ id: 'chip', area: 'statusBar.right', order: 130,
      render: () => jsx('button', { onClick: () => host.notify({ kind: 'info', message: 'Hello!' }) }) })
  }
}
```

Tiga hal yang perlu kamu tahu soal mental model-nya:

- **`host.state.*`** = baca state hidup aplikasi (read-only). Mau tahu sesi mana yang sedang sibuk? Ambil dari sini.
- **`host.*`** = aksi aman yang sudah dikurasi: toast, navigate, tail log, **restart gateway**, atau subscribe ke event stream.
- **`host.request`** = pintu JSON-RPC penuh ke gateway — sama persis dengan yang dipanggil aplikasi.

Modelnya **mengikuti VS Code**: kamu impor satu modul dan tidak pernah menyentuh internal aplikasi. Modul internal itu memang sengaja di-lint-fence supaya plugin tidak bisa jadi "hack" yang rapuh.

## 🧱 Slot yang Bisa Kamu Isi

Gelombang SDK di v0.21.5 membuka banyak titik sambung resmi (bukan trik DOM). Beberapa yang tercatat di release notes:

- **Composer draft API** — kontrol atas draft pesan sebelum dikirim
- **Session-list & row-decoration slot** — hias baris sesi di sidebar (contoh plugin komunitas memakainya buat navigasi sesi pakai keyboard)
- **Model-pill label provider** — ganti label model di UI
- **Typed bridges** untuk settings, skills, toolsets, dan profiles
- **Sandboxed embed primitive** — menyisipkan konten pihak ketiga tanpa memberi akses penuh
- **Appearance-settings slot** dan **public event bridge** untuk backend plugin

Ada tiga mode pengiriman plugin: **Disk** (paling disarankan, ESM polos tanpa build), **Unified package** (kalau plugin kamu sekaligus bawa kode sisi agent), dan **Bundled** (dipakai di dalam pohon repo, ikut build Vite aplikasi). Ketiganya pakai kontrak `HermesPlugin` yang sama dan muncul di **Capabilities → Plugins** dengan toggle hidup/mati langsung.

## 🔌 Connectors: Tab MCP Sudah Punya Rumah Baru

Perubahan yang paling kelihatan buat pengguna non-developer: **tab MCP di Hermes Desktop diganti jadi halaman Connectors**. Isinya sama — server MCP, integrasi, semuanya pindah, bukan sistem baru.

Tambahan yang penting: plugin yang baru dipasang langsung dapat tombol **"Connect now"**, jadi antara "saya nemu integrasi berguna" dan "agent saya bisa pakai" tidak ada lagi dua layar terpisah. Onboarding juga sudah menawarkan plugin katalog dari pertama kali buka, bukan menyuruh kamu cari sendiri.

Kenapa nama-nya diganti? Karena **MCP itu nama protokol**, dan nama protokol bikin orang non-teknis bengong. "Connectors" menjelaskan hasilnya: di sinilah agent kamu tersambung ke dunia luar.

## 📅 Yang Lain di v0.21.5

Selain plugin SDK, rilis yang menggabungkan ~460 PR ini juga membawa:

- **Simple/Advanced interface mode** di Desktop — tampilan ringkas, kontrol penuh satu toggle saja
- **Per-profile stop/start/restart** di bawah host multiplexer, plus `gateway.standalone` buat profile yang mau mandiri
- **Kontrol gateway per-profil** dan gateway singleton lock di level host
- **Terjemahan lengkap Prancis, Jerman, Spanyol** + pengaturan arah teks RTL/LTR
- **Portal webhook** yang delivery-nya dicerminkan ke sesi chat tujuan
- **Katalog model baru**: GPT-6 Sol/Terra/Luna dan Claude Opus 5.5 di Nous & OpenRouter
- **Integrasi resmi Blender Lab + plugin NVIDIA**, plus puluhan plugin komunitas baru di katalog

Angka teknisnya juga tidak kecil. Release notes menyebut window sejak v0.21.4 berisi **1.610 non-merge commit** di **4.828 file** (+164.132 / −149.440 baris), **460 PR** dan **475 issue** tertutup. Kuncinya: **catatan kurasi lengkap sengaja ditahan sampai v0.22.0** — jadi v0.21.5 ini adalah tag stabil untuk konsumen downstream (image Docker, Hermes Cloud), bukan narasi fitur final.

## ⚙️ Cara Update

```bash
hermes update                              # instalasi git
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash   # fresh install
```

Untuk Docker dan Hermes Cloud, image dibangun dari tag `v2026.9.24` (`nousresearch/hermes-agent:v2026.9.24`).

## 🎯 Jadi, Harus Mulai dari Mana?

Kalau kamu pengguna biasa: update, buka **Connectors**, sisihkan lima menit buat menginventaris apa saja yang sudah tersambung ke agent kamu. Kebanyakan orang menemukan sambungan lama yang sudah tidak dipakai.

Kalau kamu developer: buat satu folder di `~/.hermes/desktop-plugins/`, tulis plugin pertama kamu — satu pane, atau satu chip di status bar. Tidak perlu toolchain. Hot-reload bikin iterasi jadi hitungan detik, bukan menit.

Yang paling menarik justru sinyalnya: **core Hermes mendaftarkan UI-nya persis dengan cara yang sama seperti plugin**. Artinya plugin bukan tempelan — dia warga kelas satu. Dan repo `hermes-example-plugins` sudah disediakan sebagai bahan belajar. Ekosistem plugin Hermes baru mulai, dan ongkos masuknya sekarang sekitar 10 baris kode.

Kalau kamu bikin plugin lucu atau berguna, cerita di kolom komentar ya — atau kirim ke kami, barangkali jadi artikel berikutnya.

— Chokdi 🐷 · Content Studio · 2026
