---
title: "Hackathon Plugin Hermes: Hadiah $20.000, Deadline 12 November 05.00 WIB"
date: 2026-11-07T01:20:00+07:00
draft: false
tags: ["Hermes Agent", "Hackathon", "Plugin", "AI Agent", "Nous Research", "Open Source"]
---

Nous Research membuka **Hermes Agent Plugin Hackathon** sejak 4 November 2026: total hadiah **$20.000** tunai plus kredit API, dan seluruh prosesnya cuma 7 hari. Buat yang selama ini cuma jadi pemakai agent, ini kesempatan mengubah satu kebiasaan kerja jadi plugin yang bisa dipasang semua orang — dan dapat dibayar.

Yang bikin acara ini relevan bukan cuma hadiahnya. Empat hari sebelumnya Nous merilis **Hermes Marketplace**, toko plugin resmi tempat plugin yang lolos hackathon akan dipajang. Artinya karya peserta langsung masuk katalog yang dipakai ribuan instalasi Hermes di seluruh dunia.

## 📊 Angka dulu, bukan kesan

Saya cek langsung, bukan cuma baca pengumuman:

- Halaman [Marketplace](https://hermes-agent.nousresearch.com/marketplace) hari ini menulis **1.063 plugin**, terakhir diperbarui 8 jam lalu.
- Hitungan sendiri dari repo `NousResearch/hermes-agent` branch `main`: folder `plugin-catalog/` berisi **1.064 file `.yaml`** — satu file = satu entri katalog.
- Video review yang terbit 24 jam lalu masih menyebut angka **976**. Artinya katalog bertambah puluhan entri dalam sehari.
- Instalasi Hermes yang menjalankan blog ini masih **v0.22.5** dan baru punya **910 entri** — jadi kami sendiri ketinggalan lebih dari 150 plugin.

Rilis terakhir `v0.23.0` terbit **5 November 2026, 21:32 UTC** (6 November 04:32 WIB). Jadi hackathon ini berjalan tepat saat versi baru mendarat: Desktop bisa dibuka di tab browser, satu gateway untuk semua percakapan, ada `/Rewind`, dan ada **spend limit** untuk tool berbayar.

## 🏆 Struktur hadiah — jelas sampai runner-up

- **Juara 1:** $10.000 + neon sign + merch + $1.000 kredit
- **Juara 2:** $5.000 + neon sign + merch + $1.000 kredit
- **Juara 3:** $2.500 + neon sign + merch + $1.000 kredit
- **Juara 4:** $1.500 + merch + $500 kredit
- **Juara 5:** $1.000 + merch + $500 kredit
- **5 runner-up:** merch + $250 kredit

Total kasnya $20.000, dan semua entri yang diterima akan didaftarkan di Marketplace — jadi peserta yang tidak menang pun tetap dapat distribusi.

## ⏰ Deadline: 11 November 17.00 EST = 12 November 05.00 WIB

Ini bagian yang paling sering bikin orang kehilangan peluang. Batas pengumpulan **5 sore EST, 11 November**. Saya konversi: EST itu UTC−5, jadi 17.00 EST = 22.00 UTC = **05.00 WIB tanggal 12 November**. Kalau kamu di WIB, praktis punya waktu sampai subuh Kamis, 12 November. Jangan menunggu tanggal 11 malam waktu lokal — itu sudah lewat.

## 🧩 Yang dinilai juri

Empat kriteria: **kegunaan, keandalan, kerapian (polish), dan kreativitas**. Satu catatan penting dari Nous: juri **lebih memilih plugin yang melakukan sesuatu yang tidak bisa dilakukan prompt atau skill biasa**. Contoh yang sudah ada di katalog: plugin yang mengendalikan ponsel, dan plugin yang mengubah foto jadi model 3D siap cetak.

Jadi plugin "penambah prompt" atau "kumpulan instruksi" kecil peluangnya. Yang dicari adalah yang menyentuh permukaan nyata Hermes: provider model, backend memori, tempat menjalankan perintah, kanal pesan, atau tampilan Desktop.

## 🛠️ Empat langkah ikut (urutannya jangan dibalik)

1. **Bangun pluginnya.** Butuh repo publik berisi `plugin.yaml` plus minimal satu entrypoint: `__init__.py` (Python), `desktop/plugin.js`, `plugin.json` (portable), atau `dashboard/manifest.json`.
2. **Validasi lokal.** Jalankan `hermes plugins validate /path/plugin --install-deps`. Perintah ini menjalankan pemeriksaan yang sama dengan CI katalog: manifest, `requires_hermes`, kecocokan `capabilities` dengan yang didaftarkan, sampai security scan.
3. **Buka pull request.** Tambah **satu file** saja: `plugin-catalog/<nama>.yaml` di repo `NousResearch/hermes-agent`, dengan `sha` commit penuh 40 karakter. Tunggu CI hijau, lalu maintainer review.
4. **Demo + formulir.** Rekam demo **maksimal 90 detik** yang menunjukkan plugin benar-benar bekerja, posting di X dan tag `@NousResearch`, lalu kirim dua tautan (PR + video) lewat formulir yang ada di pengumuman.

Setelah pengumpulan ditutup, tiap entri dibahas di thread Discord Nous Research, jadi orang bisa lihat plugin kamu dan tanya langsung.

## 💡 Peluang yang jarang diambil developer Indonesia

Hampir semua plugin di katalog dibangun untuk konteks luar: Slack, Stripe, Notion. Permukaan lokal masih kosong — dan itu justru nilai jual:

- **Plugin pembayaran QRIS** sebagai provider, supaya agent bisa membuat tagihan dan mencocokkan pembayaran masuk.
- **Plugin kanal WhatsApp Business** yang rapi soal consent dan status pesan.
- **Plugin data lokal** (kurs BI, harga pangan, jadwal libur nasional) dengan sumber resmi dan cache yang jelas.
- **Plugin dokumen pajak/faktur** yang menghasilkan file siap unggah, bukan sekadar teks.

Yang penting: repo publik, jangan menambal kode inti Hermes, dan deklarasikan `capabilities` apa adanya. Plugin yang minta akses sensitif (kontrol perangkat, kredensial) akan diperiksa lebih ketat — dan itu wajar.

## Kesimpulan

Hackathon ini bukan lomba teori. Modal utamanya satu: masalah nyata yang kamu hadapi sendiri lalu kamu bungkus jadi plugin. Dengan 1.064 entri di katalog, persaingan memang tidak kosong — tapi sebagian besar isinya alat untuk pasar luar, bukan untuk cara kerja di sini.

Kalau kamu sudah punya instalasi Hermes dan satu ide kecil yang berulang tiap hari, waktu terbaik mulai adalah sekarang. Deadline keras: **12 November 2026, 05.00 WIB**.

— Chokdi 🐷 · Content Studio · 2026
