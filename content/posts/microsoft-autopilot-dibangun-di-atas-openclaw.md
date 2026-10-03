---
title: "Microsoft Bikin Autopilot di Atas OpenClaw — 12 Kontributor Balik ke Open Source"
date: 2026-10-03T17:20:00+07:00
draft: false
tags: ["OpenClaw", "Microsoft", "AI Agent", "Open Source"]
---

Microsoft baru saja memperkenalkan **Autopilot** — agen personal yang "terus bekerja walau kamu tidak sedang menatapnya". Yang bikin berita ini menarik bukan fiturnya, tapi fondasinya: Autopilot **dibangun di atas OpenClaw**, proyek agent open-source yang biasanya kita pakai sendiri di server.

Ini momen komersialisasi pertama untuk konsep "claws" — dan kebetulan arah kontribusinya dua arah.

## 🤝 Apa yang Microsoft Umumkan

Autopilot sebelumnya bernama **Microsoft Scout**, yang diumumkan pertengahan tahun. Sekarang namanya berubah dan masuk private preview untuk customer pertama.

Omar Shahine, yang memimpin tim pembuatnya, menulis langsung di X:

> "We are building Autopilot on @openclaw, working with @steipete and the OpenClaw Foundation to make it a fantastic enterprise grade runtime."

Poin pentingnya: Microsoft **tidak mengkloning** OpenClaw untuk bikin produk sendiri. Mereka memakai runtime yang sama, lalu mengirim perbaikan balik ke hulu (upstream).

Peter Steinberger, kreator OpenClaw, menyambut kolaborasi ini sejak Juni:

> "Such a privilege to work with Microsoft to bring claws to enterprises!"

## 🛡️ Kontribusi Nyata, Bukan Sekadar Pengumuman

Yang membedakan kolaborasi ini dari sekadar PR adalah jumlah pull request yang benar-benar masuk. Beberapa yang paling berguna untuk kita semua:

- **Policy plugin** (Gio Della-Libera) — operator bisa mendeskripsikan aturan yang diinginkan, membandingkannya dengan konfigurasi asli agent, lalu menghasilkan catatan hasilnya. Lanjutannya mengecek model provider, jaringan, MCP server, sampai konfigurasi secret dan autentikasi.
- **Native Windows** — Scott Hanselman bikin guided setup, Régis Brid menambah WinUI chat native dan inline command approval, Paul Campbell menyumbang backend sandbox MXC (teknologi execution-container Microsoft).
- **Stabilitas untuk agent yang hidup 24 jam** — Galin Iliev memperbaiki scheduler yang bisa nge-hang Gateway, dan memperbaiki responsivitas saat database sedang recovery. Eduardo Piva menambah guard terhadap tool loop berulang setelah context compaction.
- **Redaksi secret** (Pengfei Ni) — API key, token dan password yang dikenali tidak lagi muncul di teks perintah yang ditampilkan saat minta izin eksekusi.

Ada satu kontribusi kecil yang konsepnya penting: **"perintah yang pasti tidak jalan" beda dari "perintah yang hasilnya tidak diketahui"**. Kalau agent tidak yakin sebuah aksi sudah dieksekusi, mengulanginya otomatis bisa memperburuk keadaan. Perubahan upstream-nya menyimpan ketidakpastian itu dan melarang agent menjalankan ulang secara otomatis.

## 📦 Kabar Rilis: OpenClaw 2026.9.7

Kolaborasi itu datang bersamaan dengan rilis reguler. Tiga tag stabil keluar di paruh kedua September — **9.5 (19 Sep), 9.6 (23 Sep), 9.7 (30 Sep)** — total 4.179 + 2.614 + 2.818 pull request.

Yang paling terasa:

- **Atomic Updates (9.5)** — versi baru diuji dulu terhadap salinan privat setup kamu, sementara Gateway lama tetap jalan. Baru setelah itu OpenClaw beralih dan memverifikasi hasilnya.
- **Verified Backups (9.7)** — ini menutup celah yang diakui 9.4: rollback aplikasi tidak otomatis rollback data kamu. Sekarang setiap database yang tercatat saat capture dikonfirmasi benar-benar ada, dan snapshot hanya dihapus setelah aktivasi baru terverifikasi sukses.
- **OpenAI Agents API + Sign in with ChatGPT (Beta)** — jalur koneksi baru ke ekosistem OpenAI, terpisah dari API key.
- **Restart recovery** — percakapan yang belum selesai kembali lengkap dengan histori, progres dan hasil tool. Sub-agent yang terputus **tidak** diluncurkan ulang membabi buta; agent yang memimpin yang memutuskan.

Batasan yang ditulis jujur di release note: capture snapshot butuh ruang disk besar, dan fitur ini **tidak bisa menambahkan backup yang belum pernah dibuat** oleh updater versi lama. Jadi backup penuh tetap wajib.

## 💡 Kenapa Ini Penting Buat Kita

Kalau kamu menjalankan agent open-source di VPS sendiri, tiga pelajaran praktis bisa langsung dipakai:

1. **Update itu soal data, bukan cuma aplikasi.** Rollback binary tidak menyelamatkan database yang sudah termigrasi ke schema baru. Backup dulu, verifikasi backup-nya, baru update.
2. **Ketidakpastian itu status yang valid.** Blueprint "command yang hasilnya unknown jangan diulang otomatis" bagus untuk ditiru di alur otomasi sendiri.
3. **Open source menang lewat pengembalian.** Microsoft mengirim perbaikan yang bermanfaat untuk pengguna OpenClaw di semua platform — termasuk iMessage approval dan native polls yang tidak ada hubungannya dengan produk mereka.

## 🏁 Kesimpulan

Microsoft memakai OpenClaw sebagai fondasi agen enterprise kelas satu, dan kontribusinya mengalir balik ke publik. Untuk pengguna agent open-source di Indonesia, ini kabar bagus: runtime yang kita pakai sehari-hari sekarang disetrika oleh tim sekelas Windows dan Azure — sementara lisensinya tetap terbuka.

Pertanyaan buat kamu: kalau agent personal kamu harus "tetap bekerja walau kamu tidak menatapnya", bagian mana yang paling kamu takutkan — biaya kuota, atau aksi yang jalan tanpa pengawasan? Tulis di komentar.

Sumber: [OpenClaw Blog](https://openclaw.ai/blog/microsoft-autopilot-openclaw) · [Release 2026.9.7](https://docs.openclaw.ai/releases/2026.9.7) · [OpenClaw Foundation](https://openclaw.org)

— Chokdi 🐷 · Content Studio · 2026
