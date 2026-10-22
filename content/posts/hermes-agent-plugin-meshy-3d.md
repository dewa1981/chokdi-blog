---
title: "Hermes Agent Dapat Plugin 3D Resmi: Foto Gelas Jadi Model Siap Print"
date: 2026-10-22T17:10:00+07:00
draft: false
tags: ["hermes-agent", "meshy", "ai-3d", "plugin", "openclaw", "3d-printing"]
---

Bayangkan kamu lagi duduk santai, buka Telegram, kirim satu foto mug kesayangan ke agent AI, lalu 30 detik kemudian balik kiriman file 3D yang tinggal masuk printer. Itu bukan demo tahun depan. Mulai **22 Oktober 2026**, skenario ini resmi jalan di Hermes Agent.

Nous Research baru saja merilis **plugin Meshy resmi** untuk Hermes Agent. Announcement-nya langsung dibanjiri 66 ribu lebih views, dan bukan tanpa alasan: ini pertama kalinya agent open source bisa bikin aset 3D beneran — bukan sekadar gambar atau script Blender setengah jadi.

## 🆕 Apa yang Baru, Singkat Saja

Plugin `meshy` adalah **plugin resmi v0.4.0** di katalog Hermes Agent. Isinya satu paket portable berisi MCP server milik Meshy sendiri (di-pin di `@meshy-ai/meshy-mcp-server@0.6.4`) plus satu skill kerja `meshy-3d`, dan satu perintah install:

```
hermes plugins install meshy
hermes plugins enable meshy
```

Yang bisa dilakukan setelah install:

- **Text to 3D** — "bikin peti harta low-poly buat Godot"
- **Image to 3D & multi-view** — foto produk, konsep art, atau beberapa sudut sekaligus
- **AI Texturing & retexturing** — nempelin tekstur PBR ke model yang sudah ada
- **Remesh** — turunin jumlah poligon sesuai budget game
- **UV unwrap, auto-rigging, animation** — karakter humanoid bisa langsung jalan
- **3D print prep** — cek bisa dicetak atau nggak, repair, 3MF multicolor, auto split, sampai handoff ke slicer

Ekspornya juga lengkap: **FBX, OBJ, GLB, STL, USDZ, 3MF**. Jadi mau masuk Unity, Godot, Blender, atau langsung ke Bambu Studio, semuanya kebuka.

## 📸 Bukti Nyata: Foto Mug ke Model Print

Ini bagian yang paling menarik buat kita yang bukan 3D artist.

Di Hermes Desktop, begitu model jadi, hasilnya **di-render langsung di dalam chat** — bisa diputar, ada menu download & convert, plus gallery semua generasi terakhir dengan riwayat "Made from" (dari gambar mana model itu lahir). Di aplikasi chat seperti Telegram, Hermes mengirim preview video pendek supaya tetap kelihatan hasilnya walau kamu lagi di HP.

Contoh nyata dari tim Meshy sendiri: mereka minta peti kayu bergaya game dengan trim emas. Hasilnya keluar dengan **565.188 triangle** — jauh terlalu berat untuk game. Mereka lalu bilang: *"bikin versi game-ready di bawah 10.000 triangle"*. Hermes bikin remesh, minta approval, dan menyimpan file kedua dengan **8.165 triangle**, ketiga texture map masih utuh. Verifikasi angka segitiga ini dikerjakan agent sendiri, bukan dikira-kira.

Untuk jalur cetak, Meshy mengklaim **97% slicer pass rate** dari internal test mereka. Model yang lolos analisis bisa langsung di-scale ke ukuran nyata — misal "bikin tinggi 80 mm" — lalu diserahkan ke slicer yang terpasang.

## 💳 Soal Kredit: Ini yang Harus Kamu Tahu

Jangan sampai kaget tagihan. Semua tool Meshy yang menghabiskan kredit (5–62 kredit per call) **dilewatkan approval prompt** di Hermes dengan estimasi biaya:

- **Allow once** → sekali ini saja
- **Allow for this session** → sesi ini saja
- **Deny** → batal

Selain itu ada **limit 200 kredit per chat**, jadi kalau mau ngebut banyak model, Hermes akan tanya ulang. Tool read-only seperti cek saldo, status task, library animasi, dan deteksi slicer jalan tanpa prompt.

Harga dasarnya (per dokumentasi Meshy): **Text/Image to 3D 20 kredit**, Ultra Mode 25 kredit, AI Texturing 10 kredit, sementara **remesh, rigging, dan animasi gratis**. Free plan dapat 100 kredit per bulan — cukup buat sekitar 5 generasi. Buat pemakaian serius, plan Pro sekitar 1.000 kredit per bulan.

Satu catatan penting: **cron dan eksekusi tanpa approver tidak bisa bayar kredit otomatis** — paid call akan ditolak. Jadi jangan berharap pipeline 3D jalan sendiri jam 3 pagi tanpa ada manusia yang klik Approve.

## ⚙️ Syarat & Jebakan yang Bikin Gagal

Ini bagian yang paling sering bikin orang frustrasi di jam pertama:

1. **Node.js 18+ (disarankan 22.12+) dan npx harus ada di PATH.** Plugin pertama kali jalan akan download paket pinned ke cache npm.
2. **Butuh `MESHY_API_KEY`.** Ambil dari meshy.ai → Settings → API. **API key butuh plan Pro ke atas.** Untuk jalur skill (bukan plugin) bisa pakai device sign-in browser, kode sekali pakai, expired 10 menit — cocok buat server remote.
3. **Jangan install skill pihak ketiga bernama `meshyai`.** Itu bukan punya Meshy. Yang resmi hanya dari author `meshy-dev`.
4. **Kalau Hermes tidak memakai skill-nya**, mulai sesi baru setelah install, atau sebut kata "Meshy" di permintaanmu.

Bonus yang jarang dibahas: Hermes menjalankan **self-improvement review** setelah job pertama dan menambahkan catatan ke salinan lokal skill-nya — contohnya, selalu cek jumlah triangle sebelum menyebut model "game-ready". Jadi agent-nya makin pintar tiap kali kamu pakai.

## 🥊 Hermes vs OpenClaw untuk 3D

Keduanya bisa menjalankan workflow Meshy yang sama, jadi pilih yang sudah kamu pakai sehari-hari. Bedanya praktis:

- **Skill**: Hermes punya dua (generation + printing, printing bisa install sendiri); OpenClaw satu skill gabungan.
- **Cara install**: Hermes bisa lewat Skills Hub atau satu pesan di chat; OpenClaw satu pesan atau satu command.
- **Approval biaya**: Hermes pakai kartu pilihan dengan tombol Approve & Confirm; OpenClaw tanya di chat.
- **Hasil**: Hermes kasih preview + file card dengan tombol Open; OpenClaw preview + link file.

Kalau kamu di tim yang butuh audit jejak biaya rapi, kartu approval Hermes lebih enak dibuktikan ke atasan. Kalau butuh cepat dan sudah nyaman di dashboard browser, OpenClaw tidak kalah.

## 🎯 Buat Apa Aja di Indonesia?

Tiga use case yang paling masuk akal buat kreator dan UMKM kita:

1. **Aset game & Roblox.** Props, potion, senjata, environment low-poly. Minta langsung dengan budget triangle di prompt — "di bawah 1.500 triangle" — dan agent akan cek angka aslinya.
2. **Visual produk UMKM.** Foto kerajinan, kopi, atau souvenir → model 3D bertekstur → embed di landing page pakai `<model-viewer>`. Konversi naik karena pembeli bisa muter produk 360°.
3. **Print on demand.** Figurin, gantungan kunci, fridge magnet, lampu hias. Jalur printing-nya sudah termasuk cek printability, jadi kamu tidak buang filament buat model bolong.

Yang **belum** cocok: karakter hero dengan close-up detail tinggi, komponen dengan toleransi dimensi presisi, dan modular kit yang harus punya topologi konsisten. AI 3D 2026 masih paling kuat untuk konsep, graybox, props statis, dan base produksi. Turntable cantik ≠ aset siap rilis.

## ✅ Kesimpulan

Plugin Meshy resmi menutup celah terbesar Hermes Agent: sebelumnya kamu minta model 3D dan dapatnya teks atau script, sekarang dapatnya file. Kombinasi katalog 600+ plugin dari rilis v0.22 dan plugin 3D ini bikin Hermes berubah dari "asisten yang ngobrol" jadi "rekan produksi yang ngasih aset".

Kalau kamu punya printer 3D nganggur atau lagi bikin game indie, malam ini juga bisa coba: install plugin, siapkan API key Pro, lalu kirim satu foto barang di meja kamu. Dua menit kemudian kamu sudah pegang file GLB.

Yang penting diingat: approval kredit itu fitur, bukan gangguan. Baca estimasinya, baru klik Approve.

— Chokdi 🐷 · Content Studio · 2026
