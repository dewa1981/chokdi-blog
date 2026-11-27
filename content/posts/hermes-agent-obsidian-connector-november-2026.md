---
title: "Hermes Agent Sekarang Bisa Baca-Tulis Vault Obsidian — Catatan Tetap di Laptop Kamu"
description: "Obsidian merilis konektor resmi untuk para agent pada 25 November, dan Hermes masuk gelombang pertama. Ini isi paketnya, cara install, dan arti 'lokal' yang perlu dipahami sebelum memberi akses."
date: 2026-11-28T01:10:00+07:00
draft: false
tags: ["Hermes Agent", "Obsidian", "AI Agent", "Plugin", "Produktivitas"]
---

Rabu malam, 25 November 2026 pukul 21.19 UTC, akun resmi Obsidian menulis satu kalimat yang langsung menyebar: **"Obsidian now has official connectors for every agent."** Dalam sehari, unggahan itu dilihat lebih dari 1,1 juta kali (catatan CellCog). Sehari kemudian, Nous Research mengonfirmasi: **Hermes Agent resmi bisa mengendalikan vault Obsidian** lewat konektor resmi yang sama.

Bagi yang memakai Obsidian sebagai second brain, ini bukan sekadar plugin baru. Catatan selama ini hanya bisa dibaca manusia; sekarang agent bisa mencari, membaca, menulis, dan merapikannya — tanpa memindahkan file ke cloud.

## 📜 Apa yang sebenarnya diumumkan

- Obsidian membuat konektor resmi untuk banyak agent sekaligus. Nama yang disebut saat peluncuran: Claude, ChatGPT, Grok Bot, dan **Hermes**. Di balasan, akun Obsidian menambahkan OpenClaw, Mistral, Dots, dan Duet; dokumentasinya juga mencantumkan Cursor, GitHub Copilot, Kiro, dan OpenCode.
- Isinya bukan aplikasi baru, tapi **skill dan instruksi**: cara kerja Obsidian Flavored Markdown, Bases, JSON Canvas, template, dan link — diperbarui mengikuti fitur Obsidian terbaru.
- Untuk Hermes, pemasangannya satu baris: `hermes plugins install obsidian`.

## 🧩 Isi paket: tujuh skill

Di Hermes Marketplace, plugin `obsidian` berstatus **Verified**, dibuat langsung oleh Obsidian (v1.2.3). Tujuh skill di dalamnya:

- **obsidian-cli** — cari, baca, buat, dan kelola catatan lewat aplikasi Obsidian yang sedang berjalan.
- **obsidian-headless** — sync dan publish vault tanpa aplikasi (butuh Node.js 22+ dan langganan Sync/Publish).
- **obsidian-markdown** — link, properties, callout, embed.
- **obsidian-bases** — file Bases: view, filter, formula, summary.
- **json-canvas** — Canvas: node, edge, group.
- **defuddle** — ambil teks bersih dari halaman web.
- **knap** — render template dari data terstruktur (butuh Node.js 20+).

Penting: paket ini **instruksi saja** — tanpa MCP server, hook, atau proses latar. Defuddle, Knap, dan Headless tidak dibundel; skill akan minta izin dulu sebelum memasangnya dari npm.

## ⚠️ "Lokal" bukan berarti model tidak membaca

Obsidian tetap tanpa AI bawaan, tanpa akun, tanpa analytics, dan tidak bisa mengakses data pengguna. File tetap di perangkat, dalam format terbuka. Tapi halaman marketplace Hermes menulis nuansa yang jarang dikutip: **isi vault yang kamu tanyakan masuk ke percakapan dan diproses model AI yang kamu pakai**, bukan hanya di komputer kamu.

Selain itu, `obsidian-cli` bisa membaca, menulis, memindahkan, **dan menghapus** catatan. Izinnya penuh, bukan read-only. Dua hal ini yang perlu dipahami sebelum mengetik "rapikan semua catatanku".

## 🛡️ Cara mulai yang aman

1. **Backup vault dulu.** Git atau zip, lima menit. Ini bukan formalitas — agent punya izin hapus.
2. **Satu folder per agent.** Misalnya `Agent/Hermes/`, supaya catatan lama tidak tersentuh.
3. **Mulai dari membaca.** Minta ringkasan atau daftar link dulu; baru naik ke tugas menulis.
4. **Minta log perubahan.** Satu file `Agent-Log.md` berisi apa yang diubah setiap sesi.
5. **Matikan kalau selesai.** Plugin bisa di-disable; akses tidak harus permanen.

## 🚀 Kenapa ini relevan buat pengguna Hermes di Indonesia

Kombinasinya menarik karena dua-duanya bisa jalan tanpa langganan cloud: Obsidian gratis dan lokal, Hermes open-source dan bisa di-host di VPS sendiri. Untuk kerja harian, gunanya konkret: ringkas catatan rapat jadi poin aksi, ubah catatan proyek jadi draft artikel, cari kaitan antar catatan, atau isi template dokumen dari data yang sudah ada.

Konteksnya juga pas. Hermes v0.23.4 (23 November) menggulung **229 PR** sejak v0.23.3, dan marketplace-nya kini berisi **2.684 plugin**. Sehari setelah rilis, NVIDIA mengirim Vera CPU DevKit untuk menguji "swarm" Hermes dalam jumlah besar. Arahnya jelas: kemampuan agent tumbuh lewat plugin, bukan menunggu rilis inti.

## Kesimpulan

Konektor Obsidian mengubah catatan dari arsip pasif menjadi memori kerja yang bisa dipakai agent. Yang perlu dipegang: file tetap milik kamu, tapi begitu agent membaca, isinya masuk ke model — jadi atur izin dan backup sebelum bereksperimen. Mulai kecil: satu folder, satu tugas, satu log.

*Catatan: fitur dan harga bisa berubah. Cek `help.obsidian.md/connectors` dan halaman marketplace Hermes untuk versi terbaru.*

**Baca juga:** [Hermes Agent v0.20.1 Resmi Rilis: AI Agent Open Source yang Paling Banyak Dipakai di Dunia](https://chokdi.ano99.com/posts/hermes-agent-v0201-ai-agent-paling-dipakai-di-dunia/) · [Hermes Agent v0.20.2 Resmi Rilis: Update Agustus 2026 untuk AI Agent Lokal](https://chokdi.ano99.com/posts/hermes-agent-v0202-update-agustus-2026/) · [Hermes Agent: AI Agent Open-Source Terpopuler di Dunia 2026](https://chokdi.ano99.com/posts/hermes-agent-ai-terpopuler-dunia-2026/)

— Chokdi 🐷 · Content Studio · 2026
