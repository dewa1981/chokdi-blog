---
title: "Incredible ($59/bulan) vs Record-Replay Gratis: Cara AI Belajar dari Menonton Kamu Kerja"
date: 2026-10-07T14:10:00+07:00
draft: false
tags: ["AI", "AI Agent", "Computer Use", "Open Source", "Automasi", "Record Replay"]
---

# Incredible ($59/bulan) vs Record-Replay Gratis: Cara AI Belajar dari Menonton Kamu Kerja

Ada satu masalah yang menghantui semua orang yang pakai AI agent: **kamu harus menjelaskan semuanya dari nol, setiap kali.**

"Klik tombol itu di kiri atas." "Isi kolom ini pakai angka dari file Excel." "Kalau muncul popup, tekan OK." Ribet, ya? Kamu tahu caranya, tapi AI-nya tidak — dan menjelaskannya makan waktu lebih lama daripada mengerjakannya sendiri.

Nah, **7 Oktober 2026** sebuah startup meluncurkan produk yang katanya menjawab masalah itu: **Incredible**. Konsepnya sederhana tapi menggoda — **AI yang belajar dengan menonton kamu bekerja**. Tahan tombol, ucapkan tugasnya pakai kata-katamu sendiri, dan AI itu akan mengklik serta mengetik di aplikasi dan browser yang sudah kamu pakai.

Artikel ini membedah produknya: berapa harganya, apa yang bisa dan tidak bisa, **dan** — bagian yang paling menarik untuk kita — **konsep "record & replay" ini bisa kamu bangun sendiri, gratis, di server sendiri.** Kita buktikan.

## 🎬 Apa Itu Incredible?

Dari landing page resminya (`incredible.one`):

> *"Incredible clicks and types in your browser, files and apps, exactly like you do. The busywork gets done while you do something else."*

**Cara kerjanya menurut mereka:**

| Aspek | Detail |
|---|---|
| Bentuk | **Desktop app** (macOS & Windows) |
| Trigger | Tahan tombol **`fn`** → ucapkan tugasnya (**voice**, bukan prompt) |
| Kemampuan | Klik, ketik, navigasi, copy-paste, ganti tab, cari, kirim |
| Browser | Pakai website seperti kamu, **termasuk yang sudah kamu login** |
| File | Baca/ubah Excel, Word, PDF, PowerPoint di komputermu |
| Integrasi | **3.000+ aplikasi** (Gmail, Slack, Notion, HubSpot, Salesforce, Teams, dsb) |
| Keamanan | SOC 2 Type 2 (audit Sensiba), GDPR, **tanpa training dengan datamu** |
| Pendanaan | **$2,7 juta pre-seed** |

Pendekatan mereka berbeda dari chatbot konvensional. Sebuah chatbot cuma **menuliskan jawaban** — kamu masih harus menempelkan jawaban itu ke setiap aplikasi sendiri. Incredible melompat satu langkah: **ia menaruh jawabannya di sana untuk kamu.**

## 💰 Harganya: $59/User/Bulan (dan Naik Sampai $209)

Ini bagian yang jarang disorot promo, jadi biar kita tegas:

| Paket | Harga | Isi |
|---|---|---|
| **Incredible** | **$59 / user / bulan** | Voice assistant penuh, semua kemampuan |
| **Incredible Max** | **$209 / user / bulan** | Semua fitur Incredible |

Dalam rupiah ($59 ≈ Rp 16.000), itu sekitar **Rp 950 ribu per orang per bulan**. Untuk tim 5 orang: **± Rp 4,7 juta per bulan**. Setahun: **± Rp 57 juta.**

Dan ada satu catatan penting yang menentukan apakah ini cocok untukmu atau tidak.

## ❌ Kenapa Tidak Bisa Di-Self-Host

Ini fakta yang perlu kamu tahu sebelum berharap bisa "pasang sendiri di server":

```
Incredible = aplikasi desktop CLOSED-SOURCE
    ↓
• Hanya untuk Mac & Windows (app desktop)
• TIDAK ada versi Linux, server, atau Docker
• Engine-nya milik mereka — bukan open source
```

Artinya:

1. **Harus jalan di laptop/PC kamu.** Kalau laptopnya kamu tutup, agent-nya berhenti.
2. **Data kamu lewat server mereka** (walau mereka mengklaim SOC 2 + GDPR + tanpa training).
3. **Tidak bisa dikustomisasi** untuk alur kerja khusus, aplikasi internal, atau panel perusahaan sendiri.
4. **Bayar per orang, tiap bulan** — dan biaya naik kalau timnya bertambah.

**Jadi bukan pilihan buruk** — untuk pemakaian pribadi/produktivitas kantor biasa, produk seperti ini masuk akal. Tapi begitu kebutuhannya adalah **berjalan 24 jam**, **data internal sensitif**, atau **integrasi ke sistem sendiri** (kita menyebutnya: panel transaksi, API internal, database), model desktop-berlangganan ini langsung macet.

> Analoginya: Incredible itu seperti **tukang yang datang ke rumah** — pintar, tapi cuma hadir selama kamu di rumah dan bayar per kunjungan. Kalau kamu butuh sesuatu yang **tinggal di dalam rumah dan kerja sepanjang malam**, kamu butuh jenis yang berbeda.

## 🎁 Kabar Baiknya: Konsep "Record & Replay" BISA Kamu Bangun Sendiri

Nah, bagian ini yang menarik. **Ide "belajar dengan menonton" itu bukan teknologi eksklusif Incredible.** Konsepnya sudah ada jauh sebelum produk ini, dan versi open-source-nya sudah siap dipakai hari ini.

Konsepnya bernama **trajectory recording & replay**:

```
1. REKAM    → setiap aksi (klik, ketik, scroll) dicatat lengkap
2. SIMPAN   → tiap langkah = satu folder berisi: aksi + kondisi SEBELUM + kondisi SESUDAH
3. PUTAR    → aksi yang sama dijalankan ulang, dengan jeda yang bisa diatur
```

Yang bikin ini istimewa bukan cuma "memutar ulang" — tapi **bukti visualnya**. Setiap langkah menyimpan:

| File | Isi |
|---|---|
| `action.json` | nama tool, argumen lengkap, hasil, titik klik, timestamp |
| `before.png` / `after.png` | tangkapan layar **sebelum** dan **sesudah** aksi |
| `before_state.json` / `after_state.json` | struktur elemen aplikasi (accessibility tree) |
| `click.png` | tangkapan layar dengan **tanda merah** di titik klik |
| `evidence.json` | status tangkapan tiap fase |
| `recording.mp4` | **video layar** (H.264/30fps) sepanjang sesi |

Artinya: kamu bisa **lihat sendiri** apa yang AI lihat dan lakukan — per langkah. Itu bukan cuma demo keren; itu **jejak audit**.

## 🖥️ Sudah Ada di Server Kami: cua-driver

Kami pakai **cua-driver** dari [trycua/cua](https://github.com/trycua/cua) — infrastruktur open-source untuk computer-use agent. Di server kami versi **0.21.0** sudah terpasang, dan perintah-perintahnya sudah nyata ada:

```
start_recording      → mulai rekam
stop_recording       → stop rekam
get_recording_state  → status rekaman
replay_trajectory    → putar ulang hasil rekaman
install_ffmpeg       → dukungan capture video
```

**Cara pakainya sesederhana ini:**

```bash
# 1. Mulai rekam
cua-driver recording start ~/cua-trajectories/isi-kredit
# … jalankan alur kerjanya …
cua-driver recording stop

# 2. Nanti, putar ulang
cua-driver replay_trajectory '{"dir":"~/cua-trajectories/isi-kredit","delay_ms":500}'
```

**Tiga kegunaan nyata:**

1. **Demo & screen recording** — putar folder-nya untuk menunjukkan persis apa yang agent lihat & lakukan.
2. **Regresi** — jalankan urutan yang sama di versi build berikutnya, lalu **bandingkan** trajectory-nya. Kalau ada yang berubah, kamu tahu.
3. **Data latih** — tiap turn adalah pasangan `(state, action, next_state)` yang siap dipakai untuk pembelajaran offline.

## ⚠️ Satu Jebakan yang Wajib Kamu Tahu (Pelajaran Mahal)

Kalau kamu tertarik mengadopsi ini, **jangan lewatkan satu detail teknis ini** — kami menemukannya langsung dari dokumentasinya:

> **`element_index` tidak bertahan antar sesi.**

Artinya begini: ketika AI mengklik tombol berdasarkan *indeks elemen* (mis. "elemen #14"), indeks itu **dibuat ulang setiap kali sistem memotret layar**. Indeks lama tidak berlaku di sesi berikutnya — karena nomor prosesnya berubah dan ID jendelanya selalu berubah.

**Akibatnya:**
- ❌ Rekaman yang mengandalkan indeks elemen → **gagal diputar ulang** keesokan harinya
- ✅ Rekaman berbasis **koordinat piksel** (`x, y`) + **keyboard** → **putar ulang mulus**

**Kesimpulan praktisnya:** kalau kamu mau trajectory yang benar-benar bisa di-replay, **susun dari primitif piksel + keyboard**, bukan dari indeks elemen. Kalau tidak, putar ulangmu akan berhenti dengan pesan `Invalid element_index` atau `No cached AX state`.

Ini persis jenis jebakan yang membedakan "kelihatan keren di demo" dan "benar-benar jalan di produksi" — dan dokumentasinya jujur menyebutkannya.

## 📊 Perbandingan Langsung

| Aspek | Incredible | Record-Replay Open Source |
|---|---|---|
| Biaya | **$59–209/user/bulan** | **$0** (software gratis) |
| Bisa self-host? | ❌ Tidak | ✅ Ya |
| Jalan 24 jam di server? | ❌ (butuh laptop nyala) | ✅ Ya |
| Data di infra sendiri? | ❌ Lewat server mereka | ✅ Ya |
| Bisa custom (internal/panel)? | ❌ Terbatas | ✅ Sepenuhnya |
| Voice control | ✅ (tombol `fn`) | ⚠️ Perlu disambung sendiri |
| Belajar dari demonstrasi | ✅ Ya | ✅ Ya (trajectory) |
| Jejak audit (bukti per langkah) | ⚠️ Tidak dijelaskan | ✅ Ya, lengkap |
| Video rekaman sesi | ⚠️ Tidak dijelaskan | ✅ Ya (`recording.mp4`) |
| Integrasi 3.000+ app | ✅ Ya (siap pakai) | ⚠️ Bikin sendiri |

**Bacanya begini:** Incredible menang di **kemudahan** (tinggal download, sudah sambung 3.000 aplikasi). Open-source menang di **kebebasan, biaya, dan kontrol**. Kalau kebutuhanmu "AI yang bantu kerjaan kantor di laptop" — Incredible layak. Kalau kebutuhanmu "agent yang jalan terus di server dan pegang sistem internal" — open source satu-satunya jalan.

## 🎯 Pelajaran yang Bisa Kamu Ambil

**1. "Belajar dengan menonton" itu pola, bukan produk.**
Jangan beli mahal-mahal kalau kebutuhanmu bisa dipenuhi pola yang sama dengan tools gratis. Cek dulu apa yang sudah kamu punya.

**2. Untuk kerjaan sensitif, rekam dulu — jangan langsung otomatis.**
Kalau alurnya menyentuh uang atau data penting (approve transaksi, isi saldo, ubah data pelanggan), pola **rekam → tinjau → baru otomatis** jauh lebih aman daripada langsung menyerahkan kendali. Rekaman per langkah itu jadi **bukti** kalau ada masalah di kemudian hari.

**3. Desktop app berlangganan vs server sendiri — pilih sesuai kebutuhan.**
Kalau agentnya harus kerja saat kamu tidur, datanya tidak boleh keluar, dan harus nyambung ke sistem internal — **server sendiri, open source**. Kalau cuma bantu kerjaan pribadi di laptop, produk jadi lebih cepat.

**4. Detail teknis menentukan.**
`element_index` yang tidak bertahan antar sesi itu contoh kecil yang berdampak besar. Baca dokumentasinya sampai habis sebelum menjanjikan sesuatu ke timmu.

## 🏁 Kesimpulan

Incredible adalah produk yang menarik dengan konsep yang **benar**: AI yang bertindak, bukan sekadar menjawab. Tapi **$59/user/bulan** dan **ketergantungan pada aplikasi desktop tertutup** membuatnya kurang cocok kalau kamu butuh agent yang berjalan 24 jam dengan data di infrastruktur sendiri.

Kabar baiknya: **konsep record & replay sudah tersedia open-source** dan bisa kamu pasang hari ini. Kalau kamu sudah punya server dan sedikit kemauan eksplorasi, kamu bisa dapat sebagian besar manfaatnya — **tanpa biaya langganan, tanpa data keluar dari servermu.**

Pertanyaan yang layak kamu tanyakan sebelum memutuskan: **agentmu perlu hadir saat kamu di depan laptop, atau perlu hadir saat kamu tidur?** Jawabannya menentukan pilihanmu.

---

*Sumber: [incredible.one](https://www.incredible.one) · [Software Advice](https://www.softwareadvice.com/product/560290-Incredible) · [trycua/cua](https://github.com/trycua/cua) — dokumentasi cua-driver (`RECORDING.md`, `BROWSER.md`) dan verifikasi langsung pada cua-driver 0.21.0.*

*Artikel ini disusun oleh chokdi_staging.*
