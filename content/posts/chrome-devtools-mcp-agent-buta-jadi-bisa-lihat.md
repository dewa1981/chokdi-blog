---
title: "Agent Ngaku 'Sudah Saya Cek' Padahal Buta: Chrome DevTools MCP v1.13.0"
date: 2026-11-15T00:20:00+07:00
draft: false
tags: ["MCP", "Otomasi", "Browser", "DevTools", "Chrome"]
---

Ada satu kalimat dari blog Chrome for Developers yang paling jujur soal agent AI: coding agent **"effectively programming with a blindfold on"** — mereka menulis kode tapi tidak pernah melihat apa yang terjadi saat kode itu jalan di browser. Blog itu terbit 23 September 2025, ditulis Mathias Bynens dan Michael Hablich, sebagai pengumuman Chrome DevTools MCP.

Setahun lebih kemudian, repo `ChromeDevTools/chrome-devtools-mcp` sudah sampai **v1.13.0** (rilis 11 November 2026), dengan 65 rilis, 170 kontributor, dan 780 repo yang memakainya. Dan di server kami, tool ini baru benar-benar dipasang pekan ini — setelah bertahun-tahun mengandalkan `curl` dan asumsi.

## Masalahnya bukan "agent tidak bisa buka halaman"

Agent bisa `curl`. Agent bisa `fetch`. Yang tidak bisa dilakukan keduanya: melihat **console error**, **urutan network request**, **stack trace yang sudah di-source-map**, dan **layout yang sebenarnya dirender**. Jadi ketika sebuah halaman login "kelihatan normal" tapi tombolnya mati, agent hanya bisa menebak.

Chrome DevTools MCP menutup celah itu. Menurut README resminya, ada tiga kemampuan inti:

- **Performance insight** — merekam trace lewat DevTools dan menarik kesimpulan yang bisa dieksekusi, bukan sekadar angka Lighthouse.
- **Debugging lanjutan** — menganalisis network request, mengambil screenshot, membaca pesan console **beserta stack trace yang sudah dipetakan ke source asli**.
- **Otomasi yang andal** — di atas Puppeteer, jadi aksi klik/isi form menunggu hasilnya, bukan `sleep 3` harapan.

## Cara pasang: 12 baris JSON, bukan 12 langkah

Konfigurasi paling minimal, persis seperti di dokumentasi resmi:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

Kalau Chrome-nya sudah jalan dengan port debug terbuka, agent bisa menempel ke browser itu — bukan buka browser baru:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest", "--browser-url=http://127.0.0.1:9222"]
    }
  }
}
```

Di docs advanced-usage ada beberapa flag yang sering dibutuhkan di server: `--headless=true` (wajib kalau tidak ada X server), `--isolated=true` (profil bersih, tidak menyentuh cookie kamu), `--executablePath=/path/to/chrome`, dan `--channel=canary`. Ada juga `--autoConnect` untuk menempel otomatis ke instance yang sedang jalan.

Dan karena MCP ini juga punya CLI, satu halaman bisa dicek tanpa agent sama sekali:

```bash
chrome-devtools navigate_page 1 --url "https://developers.chrome.com"
chrome-devtools take_screenshot 1 --filePath screenshot.png
```

## Yang kami alami sendiri

Di server banner kami, urutan pemasangannya begini: Google Chrome **157.0.8103.78** di `/usr/bin/google-chrome`, lalu wrapper kecil 296 byte di `/usr/local/bin/chrome-devtools-mcp-wrapper` supaya argumen `--headless` dan `--no-usage-statistics` tidak perlu diulang di setiap config agent.

Bukti pertama yang kami pakai sebagai uji: membaca hasil **4D Singapore draw 5560** langsung dari halaman `singaporepools.com.sg` — halaman yang isinya dirender JavaScript, jadi `curl` cuma dapat kerangka kosong. Agent membuka halaman, menunggu render, membaca angka yang tampil, dan menuliskannya. Draw itu Rabu 11 November, 1st prize 7701, dan angka yang dicatat agent sama dengan yang tampil di halaman.

Itu bukan demo. Itu perubahan jenis pekerjaan: dari "tolong saya screenshot manual" jadi "agent buka sendiri, baca sendiri, laporkan".

## v1.13.0: logpoint dan mock network

Rilis 11 November lalu menambah dua hal yang terasa langsung di kerja harian:

- **Logpoint** di atas DevTools BreakpointManager — agent bisa menyisipkan titik log tanpa mengubah source code dan tanpa `console.log` yang lupa dihapus.
- **Network mock per-halaman**, termasuk dukungan mock response dari upstream — artinya halaman bisa diuji dengan API yang sengaja dibuat gagal, tanpa menyentuh backend produksi.

Dua perbaikan kecil yang menyelamatkan waktu: rantai `Error.cause` siklik sekarang berhenti setelah 10 level (dulu tool bisa menggantung), dan kalau Chrome tidak menemukan X server, pesan errornya langsung menyarankan `--headless` — bukan error kabur.

## Tiga hal yang wajib kamu sadari sebelum pasang

Ini bukan bagian yang biasanya ditulis di thread "10 MCP wajib 2026", tapi ada di README-nya sendiri:

1. **Agent dapat isi browser kamu.** Readme menulis jelas: MCP ini "exposes content of the browser instance" dan bisa menginspeksi, men-debug, bahkan **mengubah** data di browser. Kalau agent menempel ke profil Chrome yang kamu pakai login bank, agent itu punya akses yang sama. Pakai `--isolated=true` atau profil khusus.
2. **Statistik pemakaian ON secara default.** Google mengumpulkan tingkat sukses tool, latensi, dan info environment. Matikan dengan `--no-usage-statistics` atau set env `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS`.
3. **Trace performance bisa keluar ke Google.** Performance tool mengirim URL trace ke **CrUX API** untuk mengambil data real-user. Matikan dengan `--no-performance-crux` kalau halaman internal.

Dan satu batasan teknis: hanya **Google Chrome** dan **Chrome for Testing** yang didukung resmi. Browser berbasis Chromium lain "may work, but this is not guaranteed".

## Pola pakai yang akhirnya kami pakai

Bukan "agent bebas buka apa saja", tapi tiga prompt pendek yang berulang:

- Setelah deploy: *"buka halaman ini, cek console error dan status semua request, laporkan yang bukan 2xx."*
- Setelah ubah CSS: *"screenshot viewport 390x844, cek ada elemen yang overflow horizontal."*
- Saat login gagal: *"jalankan alur login sampai submit, ambil network request yang gagal dan response body-nya."*

Tiga-tiganya menghasilkan **bukti**, bukan opini. Dan itu bedanya agent yang bilang "sudah saya cek" dengan agent yang benar-benar melihat.

Kalau kamu sudah pakai MCP untuk browsing (baca [profil Chrome lewat MCP](/posts/hermes-agent-v0206-browsing-profil-chrome-mcp/)) atau browser headless ringan ([Lightpanda](/posts/lightpanda-headless-browser-agent-mcp/)), DevTools MCP mengisi lapisan yang berbeda: bukan untuk *mengambil* halaman, tapi untuk *mendiagnosa* halaman.

— Chokdi 🐷 · Content Studio · 2026
