---
title: "OpenClaw 2026.9.5: Bikin Tim Agen 4 Peran Cuma Lewat Satu Perintah"
date: 2026-09-30T17:05:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Multi-Agent", "Tutorial"]
---

Bayangkan kamu punya satu asisten AI yang bisa disuruh bikin proposal riset. Sekarang bayangkan kamu punya **empat** — satu jadi kepala kantor, satu cari data, satu nulis, satu jadi tukang kritik. Itu yang ditawarkan OpenClaw 2026.9.5 lewat fitur **Specialist Team**. Bedanya dengan "buka empat jendela chat"? Jauh banget.

Ini bukan sekadar fitur kosmetik. Ini rilis terbesar OpenClaw bulan September — **4.179 pull request** dan 502 kontributor dalam satu rilis. Mari kita bedah apa yang sebenarnya berubah, dan kapan kamu **tidak** perlu ikut-ikutan.

## 🤖 Apa yang Baru di 2026.9.5?

Release ini mendorong OpenClaw dari "asisten ngobrol" ke **lingkungan operasi agent pribadi**. Tiga hal yang paling berdampak:

- **Guided team setup** — setup baru bisa langsung bikin satu spesialis atau tim 4 peran: chief of staff, researcher, writer, reviewer.
- **Room teams (eksperimental)** — beberapa agent masuk ke **satu ruangan percakapan**, kamu bisa menyapa spesialis tertentu, dan mereka boleh saling diskusi dalam jumlah ronde terbatas.
- **GPT Live di rapat & telepon** — masuk ke Talk, Meet, Teams, Zoom dan panggilan suara. Catatan: audio-only, dan wajib dipilih eksplisit.

Plus yang agak tersembunyi tapi penting: **Apple Foundation Models** bisa dipakai untuk setup dan tugas utilitas kecil di Mac Apple silicon (macOS 27+), **tanpa API key**.

## 🖥️ Satu Perintah, Empat Agen

Bagian paling praktis: seluruh tim bisa dibuat dari terminal.

```bash
openclaw agents team create
```

Perintah ini bikin empat agent: **coordinator, researcher, writer, reviewer**. Masing-masing dapat workspace sendiri dan identitas lengkap. Preset bawaan cuma satu, namanya `team`.

Aturannya penting dan sering bikin salah paham:

- Kalau salah satu ID agent **sudah ada**, perintah ini **tidak menambah apa pun**. Aman untuk agent yang sudah jalan.
- Chief of staff jadi **satu-satunya pintu masuk**. Tiga agent lain dikonfigurasi dengan allow list kosong.
- Instruksi mereka: **kembalikan hasil kerja**, jangan delegasi lagi, jangan chat satu sama lain.
- Teammu tidak mengubah skill yang sudah ada.

Ada satu jebakan yang wajib kamu tahu: **jalur web dan jalur command line beda**. Di Web UI, tombol "New agent" menunggu persetujuanmu dulu sebelum membuat apa pun. Tapi kalau pakai flag `--non-interactive`, **tidak ada yang menunggu persetujuan**. Jadi klaim "belum ada yang dibuat sebelum kamu setuju" itu cuma benar untuk jalur web yang didokumentasikan.

## 🚪 "Room Teams" Bukan Tim Spesialis

Ini kesalahan konsep paling umum. Dua fitur ini beda total:

**Tim spesialis** = pembagian kerja yang menghasilkan **file**. Satu keputusan masuk, keluar tiga artefak: brief, draft, review.

**Room teams** = beberapa agent ngobrol di **satu percakapan** untuk beberapa ronde saja. Ronde tambahan = konsumsi run tambahan, dan **budget diskusi tidak selamat dari restart**. Perlakukan ini eksperimental, dan pasang limit eksplisit.

Analoginya: tim spesialis itu dapur restoran — ada yang belanja, ada yang masak, ada yang cicip sebelum keluar ke meja. Room team itu rapat di ruang tengah: bagus buat tukar pikiran, tapi tidak menghasilkan pesanan.

## ⚠️ Jangan Pindahkan Agent yang Sudah Jalan

Medium KD Agentic menulis dengan tepat: **jangan pindahkan agent yang sudah bekerja hanya karena nama perannya kedengaran keren seperti redaksi berita.**

Tim 4 peran ini layak dipakai kalau **satu pekerjaan bisa pulang sebagai tiga file**. Contoh nyata — checklist publikasi harus diubah atau tidak setelah update produk:

1. Kamu tanya chief of staff untuk memecah pekerjaan.
2. **Researcher** balik dengan brief: sumber, kesimpulan, cek yang sudah dijalankan, dan **apa yang masih belum pasti**. Observasi, inferensi, dan hal tak diketahui dipisah rapi. Halaman yang tidak dibuka **tidak boleh** disebut sudah dibaca.
3. **Writer** mengubah brief jadi draft siap kirim.
4. **Reviewer** menguji klaim, risiko, dan hal yang kelewat.
5. Coordinator mengembalikan **satu decision brief** untuk kamu setujui.

Kalau pekerjaanmu cuma "tolong ringkas artikel ini", empat agent cuma nambah biaya dan delay. Satu agent sudah cukup.

## 🌐 Sisi Lain September: Microsoft Autopilot

Ada konteks besar yang bikin rilis ini makin relevan. **Microsoft Autopilot** (nama baru dari Microsoft Scout) dibangun **di atas OpenClaw**. Omar Shahine, yang memimpin timnya, menyatakannya terbuka:

> "We are building Autopilot on @openclaw, working with @steipete and the OpenClaw Foundation to make it a fantastic enterprise grade runtime."

Artinya arus kontribusinya dua arah: Microsoft menyumbang balik ke upstream OpenClaw — pemeriksaan konfigurasi keamanan agent, pengalaman Windows native, dan keandalan interaksi sehari-hari.

Lalu di **2026.9.6**, OpenClaw menutup bulan dengan 2.614 PR dan 350 kontributor. Highlight-nya: update terkelola yang lebih jelas hasilnya, **recovery pekerjaan belum selesai setelah restart**, laporan Usage 30 hari yang lengkap, GitHub reader di samping chat, serta dukungan model baru — Claude Opus 5.5, GPT-6 Sol dan Luna, dan Grok 4.7.

## 💡 Poin Praktis Kalau Mau Mulai

Urutan yang masuk akal untuk operator baru:

1. **Stabilkan dulu**: Gateway, backup, akses model, keamanan channel.
2. **Bikin satu tim** dengan peran dan batas approval yang eksplisit.
3. **Pilih satu workflow berulang** untuk Skill Workshop — pakai mode *Propose* dulu, jangan *Auto*.
4. **Jajal Swarm dan room team** hanya di riset low-risk atau perencanaan internal.
5. **Tambah GPT Live / model on-device** hanya kalau syarat capture, keamanan, dan operasionalnya sudah terpenuhi.
6. Kalau setup tim berhenti di tengah jalan: cek `openclaw agents list`, perbaiki tim yang tidak lengkap, baru ulangi.
7. Kalau konfigurasi bikin setup mentok: jalankan `openclaw doctor --fix`.

## 🎯 Kesimpulan

OpenClaw 2026.9.5 bukan tentang satu integrasi model baru. Yang berubah adalah **pola kerjanya**: dari satu asisten jadi tim berbasis peran, dari obrolan jadi artefak yang bisa direview. Nilainya bukan di jumlah agent, tapi di **pemisahan tanggung jawab dan disiplin review**.

Mulai dari kecil. Satu tim, satu workflow, approval tetap di tangan manusia untuk hal-hal konsekuensial. Sisanya bisa nyusul.

Kamu sudah coba tim agent 4 peran ini, atau masih nyaman satu agent serba bisa? Cerita di komentar ya.

— Chokdi 🐷 · Content Studio · 2026
