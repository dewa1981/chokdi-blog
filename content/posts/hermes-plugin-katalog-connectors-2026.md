---
title: "Hermes Agent Plugin: Pasang dari Katalog, Langsung Aktif Tanpa Restart Gateway"
date: 2026-09-27T01:06:00+07:00
draft: false
tags: ["Hermes Agent", "Plugin", "AI Agent", "MCP", "Self-Hosted", "Update"]
---

Sampai minggu ini, cerita paling sering di grup operator bot itu sama: plugin sudah ke-install, tool-nya sudah ada di katalog, tapi tetap "tidak kelihatan" di chat. Penyebabnya satu — **gateway belum di-restart**. Hermes Agent memutuskan itu bukan cara yang benar. Sejak rilis **v0.21.4 (21 September)** dan **v0.21.5 (24 September 2026)**, tool dan skill dari plugin yang baru dipasang **langsung hidup di semua chat yang sedang terbuka**. 🐷

Bagi yang belum tahu, Hermes Agent adalah agent AI open source buatan Nous Research — open source penuh, bisa di-host sendiri, sekarang sudah 249 ribu bintang di GitHub. Artikel ini khusus soal lapisan yang paling sering bikin orang nyerah: **plugin dan connector**.

## 🔌 Connectors: Tab MCP Lama Diganti Halaman dengan Tombol "Connect Now"

Kalau kamu pernah menghabiskan satu jam lebih cuma untuk menyusun `config.yaml` supaya satu MCP server mau nyala, bagian ini obatnya.

- Plugin yang baru di-install sekarang punya tombol **"Connect now"** langsung untuk MCP server bawaannya.
- Tools dan skills dari plugin yang terpasang **langsung aktif di semua chat yang sedang terbuka** — tanpa restart gateway.
- Di proses onboarding, katalog plugin ditawarkan **berdampingan dengan connectors**, jadi kamu tidak lagi harus tahu dulu istilah "plugin" versus "MCP" sebelum bisa mulai.

Efek nyatanya sederhana tapi besar: jumlah restart gateway yang harus kamu lakukan untuk mencoba satu tool baru turun dari "beberapa kali" jadi **nol**.

## 🧠 Kenapa Restart Gateway Itu Musuh Besar Operator Bot

Ini bagian yang jarang dijelaskan, padahal inilah kenapa fitur di atas penting.

Hermes memisahkan **agent loop** (proses yang mengerjakan tugas) dari **gateway** (proses yang nyambungin ke Telegram, LINE, LAN, atau WebUI). Gateway-nya yang memegang koneksi ke banyak platform sekaligus dan menyimpan status sesi per percakapan.

Artinya: setiap kali kamu restart gateway untuk "menyalakan" plugin baru, kamu memutus semua koneksi platform yang sedang jalan. Kalau kebetulan ada pesan masuk di detik itu, pesan itu bisa nyangkut. Di server yang jalan 24 jam dengan belasan profil agent, restart itu bukan langkah sepele — dia risiko.

Dengan plugin yang aktif hot, **restart tidak lagi jadi bagian dari alur pemasangan plugin**. Kamu pasang, tekan Connect, dan tool-nya sudah ada di chat yang sedang dibuka.

## 🖥️ Desktop Plugin SDK: Plugin Jadi Berkas Tunggal, Bukan Fork Aplikasi

Rilis yang sama juga membuka gelombang **Desktop plugin SDK** (`@hermes/plugin-sdk`) yang serius. Modelnya diambil dari VS Code: plugin adalah **satu berkas ESM** yang default-export sebuah objek `HermesPlugin`, dan cuma boleh meng-import satu modul SDK — plus `react` dan `react/jsx-runtime`.

Alur pasangnya sesederhana menaruh berkas:

- Simpan di `$HERMES_HOME/desktop-plugins/<id>/plugin.js` (nama folder harus sama dengan `id` plugin).
- Aplikasi Desktop memantau folder itu, memuatnya dalam hitungan detik, dan **hot-reload setiap kali kamu simpan**.
- Tidak ada clone repo, tidak ada `npm run build`, tidak ada patch ke source aplikasi.

Yang bisa disumbang plugin juga bukan cuma tombol kecil di pojok: **panel**, **halaman penuh**, **item sidebar**, **status bar**, **title bar**, **entri palet ⌘K**, **keybind**, sampai **tema**. Semuanya masuk ke satu registry yang sama — core Hermes mendaftarkan tampilannya lewat jalur yang persis sama, jadi tidak ada perbedaan perlakuan antara plugin pihak ketiga dan fitur bawaan.

Ada tiga mode pengiriman: **disk** (paling direkomendasikan, untuk user dan agent), **unified package** (plugin yang juga membawa kode sisi agent), dan **bundled** (ikut build aplikasi). Ketiganya pakai kontrak yang sama dan muncul di **Capabilities → Plugins**, bisa dinyalakan/dimatikan secara live.

## 🧩 Contoh Nyata: 2.473 Baris Jadi Beberapa Baris Konfigurasi

Kalau kamu belum pernah menulis plugin Hermes, contoh berikut paling gampang dibayangkan. Ini plugin "hello" yang menaruh panel di kanan dan satu chip di status bar:

```js
import { host, haptic, useValue } from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'

function HelloPane() {
  const gateway = useValue(host.state.gateway)
  return jsxs('div', {
    className: 'flex h-full flex-col gap-2 p-3 text-sm',
    children: [
      jsx('div', { className: 'font-medium', children: 'Hello, Hermes' }),
      jsx('div', { children: `gateway: ${gateway}` })
    ]
  })
}

export default {
  id: 'hello',            // harus sama dengan nama folder
  name: 'Hello',
  register(ctx) {
    ctx.register({
      id: 'pane', area: 'panes', title: 'hello',
      data: { placement: 'right', width: '260px' },
      render: () => jsx(HelloPane, {})
    })
    ctx.register({
      id: 'chip', area: 'statusBar.right', order: 130,
      render: () => jsx('button', {
        type: 'button',
        onClick: () => { haptic('tap'); host.notify({ kind: 'info', message: 'Hello from my plugin!' }) }
      })
    })
  }
}
```

Catatan teknis yang wajib diingat: berkas disk dimuat **tanpa dikompilasi**, jadi **sintaks JSX tidak akan di-parse**. Tulis UI pakai panggilan `jsx()` / `jsxs()` dari `react/jsx-runtime`. Batas import sengaja ketat — hanya SDK, `react`, dan `react/jsx-runtime`. Kalau kamu import yang lain, error-nya jelas: *unsupported import*.

Aturan lain: nama folder **harus sama** dengan `id` plugin, dan plugin Desktop itu **level aplikasi** — satu root untuk semua profil, gateway, atau mesin remote yang tersambung ke jendela itu. Kalau plugin gagal load, akan muncul toast yang menyebut errornya; perbaiki, simpan, dan dia reload sendiri.

## 🛠️ Plugin Resmi yang Menjawab Keluhan Lama: Claude Subscription

Satu contoh paling relevan buat kamu yang sudah bayar langganan Claude: **claude-subscription-directsdk**, plugin tier resmi dari NousResearch, masuk katalog **20 September 2026** (di-pin ulang ke commit terverifikasi 22 September), versi v0.3.0, lisensi MIT, label **Experimental**.

Masalah yang dia selesaikan: dulu langganan Claude dan API Claude itu seperti **dua pintu satu gedung**. Kamu sudah bayar membership, tapi begitu mau bot kamu bicara lewat Claude, muncul card reader kedua — akun API terpisah dengan tagihan per token. Plugin ini menutup pintu kedua itu: **Claude Code CLI yang tidak dimodifikasi** dipakai sebagai provider model, jadi semua request jalan di langganan yang sudah kamu bayar.

Syaratnya tiga: **Hermes Agent 0.21.4+**, **Python 3.10+**, dan **Claude Code CLI** sudah masuk login. Alurnya:

1. Install & login Claude Code (`npm install -g @anthropic-ai/claude-code`, lalu `claude auth login`).
2. Update Hermes ke 0.21.4 atau lebih baru.
3. `hermes plugins install claude-subscription-directsdk`.
4. `hermes model` → pilih **Claude Subscription DirectSDK (Experimental)** → `hermes profile create claude opus`.

Model yang tersedia lewat plugin ini: **Sonnet 5 (1M)**, **Haiku 4.5 (200K)**, **Opus 5 (1M)**, **Opus 4.8 (1M)**, dan **Fable 5.1 (1M)** dengan short name `sonnet`, `haiku`, `opus`, `fable`.

Dua catatan jujur sebelum kamu sambungkan akun. **Pertama**, plugin-nya sendiri masih bereksperimen, dan angka biaya yang dia tampilkan di sesi adalah **ekuivalen harga list**, bukan tagihan langganan yang terverifikasi — pandang sebagai estimasi, bukan struk. **Kedua**, soal aturan pemakaian: plugin ini secara teknis rapi (menjalankan CLI resmi tanpa modifikasi, tidak menyimpan kredensial sama sekali), tapi **rekayasa yang rapi bukan keputusan soal ToS**. Cek dulu ketentuan layanan dan dokumentasi paket kamu sendiri sebelum menyambungkan akun. Ada juga detail plan yang gampang bikin kaget: per aturan yang didokumentasikan Anthropic, model **Fable** di paket **Pro** menagih ke **kredit usage pay-as-you-go sejak request pertama**, sementara di paket **Max** masih termasuk sampai 50% dari limit mingguan.

## 💰 Plugin Itu Bukan Semua Wajib — Tapi Ada 3 yang Layak Duluan

Ini bagian yang paling sering bikin orang salah langkah: install sepuluh plugin sekaligus, lalu bingung kenapa Hermes jadi lambat dan berisik.

Urutan yang masuk akal untuk operator di Indonesia:

- **disk-cleanup** — agent menumpuk berkas sementara (skrip tes, profil browser, log, artefak). Ada slash command `/disk-cleanup dry-run` supaya kamu lihat daftarnya **dulu** sebelum ada yang dihapus. Ini yang bikin VPS 60 GB tidak penuh dalam sebulan.
- **langfuse observability** — supaya kamu bisa jawab "tadi agent ngapain, dan abis berapa?". Butuh `pip install langfuse`, lalu key di `~/.hermes/.env`. Kalau kamu bayar model per token, plugin ini membayar dirinya sendiri di minggu pertama. Bisa self-host kalau tidak mau trace keluar.
- **kanban dashboard** — buat kerja multi-agent yang harus selamat dari restart. Task disimpan di SQLite, ada drag-and-drop board, run history, worker log, dan update WebSocket. Kalau kamu mengurus lebih dari satu agent, transcript chat bukan tempat melacak progres.

Baru setelah itu pikirkan yang lebih "berat": connectors ke SaaS, provider memori, dan search tambahan. Perlu jujur juga: kompleksitas itu pindah tempat, bukan hilang. Menambah plugin berarti menambah rate limit dan titik gagal baru. Plugin yang boros adalah plugin yang **dipakai setiap hari**, bukan yang terdengar paling canggih.

## ✅ Kesimpulan

Rilis 21-24 September ini menutup satu kelas frustrasi yang sangat praktis: **plugin baru tidak lagi butuh restart gateway untuk kelihatan**. Untuk kamu yang menjalankan bot 24 jam di VPS — Telegram, LINE, WebUI, gateway — itu berarti memasang tool baru berhenti jadi operasi berisiko dan mulai jadi hal sepele.

Langkah paling aman kalau kamu mau ikut naik: **backup dulu, copy `state.db`** (jangan buka langsung dengan `sqlite3` di database yang hidup), baru jalankan `hermes update`. Untuk instalasi git cukup `hermes update`; Docker dan Hermes Cloud membangun image dari tag `nousresearch/hermes-agent:v2026.9.24`.

Kalau kamu sudah pakai Hermes: plugin apa yang paling pengaruh buat alur kerjamu? Tulis di komentar — dan kalau kamu baru mau mulai, justru onboarding-nya sedang dipermudah sekarang.

## 🔗 Sumber

- [Desktop Plugin SDK — Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk)
- [Hermes Agent v0.21.5 Release Notes — GitHub](https://github.com/NousResearch/hermes-agent/releases)
- [Best Hermes Agent Tools and Plugins 2026 — Composio](https://composio.dev/content/best-hermes-plugins)
- [Hermes Agent With Claude Code Subscription — AI Profit Boardroom](https://aiprofitboardroom.com/blog/hermes-agent-with-claude-code-subscription/)
- [Hermes Agent Full Tutorial for Beginners — Tech With Tim (YouTube)](https://www.youtube.com/watch?v=1ve4Atbqmoo)

— Chokdi 🐷 · Content Studio · 2026
