---
title: "OpenClaw 2026.11.10: 7.671 PR, Deep Research Bawaan, Memori Knowledge, dan Browser Handoff"
date: 2026-11-26T01:10:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Deep Research", "Memori", "Rilis"]
---

OpenClaw kembali dengan rilis besar. Versi **2026.11.10** keluar 25 November 2026 dan langsung jadi rilis terbaru di repo resminya: **8.309 commit, 7.671 pull request, dan 349 kontributor** dalam satu paket. Ini bukan patch harian biasa seperti 2026.11.1 sampai 2026.11.9 yang isinya perbaikan tanpa fitur baru — ini rilis fitur, dan tiga di antaranya langsung menyentuh cara agent bekerja sehari-hari.

## 🚀 7.671 PR dalam satu rilis: apa artinya

Angka 349 kontributor itu yang paling menarik. Artinya rilis ini bukan hasil satu tim kecil yang menambal bug, tapi tumpukan kerja komunitas yang baru digabung sekarang. Efek praktisnya dua: kamu dapat fitur baru, tapi juga mewarisi ratusan perbaikan kecil yang tidak pernah kamu baca changelog-nya. Jadi sebelum upgrade, backup config dan catat versi lama dulu — bukan karena rilisnya berbahaya, tapi karena permukaan perubahannya luas.

## 🔎 Deep Research: sekarang bawaan, bukan eksperimen

Dulu riset multi-sumber di OpenClaw itu kerjaan manual: suruh agent search, buka halaman, lalu rangkum sendiri. Sekarang Deep Research ikut sebagai plugin bawaan (`deep_research`) dan **aktif secara default**. Kamu cukup minta di chat, tanpa install apa pun.

Cara kerjanya rapi: pertanyaan dipecah jadi sub-pertanyaan, sumber dicari dan diambil, lalu setiap temuan dicocokkan dengan kutipan persis dari teks yang benar-benar terbaca. Kalau ada sumber yang bertentangan, keduanya ditampilkan berdampingan; kalau bukti kurang, muncul bagian **Unresolved** alih-alih jawaban yang dikarang.

Ada dua mesin. `portable` (default) memakai model dan tool web yang sudah kamu punya. `google` harus dinyalakan sendiri dan memakai layanan Deep Research milik Google (`deep-research-preview-04-2026`) — perlu profil API key Google, dan biaya serta penyimpanannya ikut provider.

Batasnya juga jelas, dan ini penting buat menghitung biaya. Default-nya **8 panggilan model, 6 pencarian, 12 fetch, 2 fetch paralel, dengan deadline 180 detik**. Maksimalnya 30 panggilan model, 20 pencarian, 40 fetch, 4 paralel, dan 900 detik. Korpus sumber dibatasi 60.000 byte, tiap respons model maksimal 4.096 token output. Hasil disimpan **7 hari**, maksimal 32 job per percakapan, dan job yang kepotong tetap lanjut setelah gateway restart.

Kalau kamu kasih dokumen sendiri, pencarian web otomatis mati kecuali kamu set `sources.web: true`. Dan `allowDomains`/`denyDomains` berguna kalau mau riset dibatasi ke domain tepercaya saja.

## 🧠 Knowledge: memori jadi vault Markdown yang bisa dibaca manusia

Fitur kedua adalah sistem memori baru bernama **Knowledge**. Statusnya opt-in: nyalakan lewat `plugins.slots.memory` diisi `"knowledge"`, atau pilih Knowledge sebagai provider memori di Settings. Enaknya, perubahan ini hot-reload tanpa restart gateway, dan data `memory-core` lama tidak disentuh.

Hasilnya berupa vault Markdown lokal berisi orang, proyek, keputusan, plus kutipan pendukungnya. Semua bisa dibuka di explorer Control UI, ditelusuri lewat Timeline proyek, dan dicari berdasarkan kata kunci, alias, atau tanggal. Ada "scribe" bawaan yang bisa menelan percakapan OpenClaw, catatan meeting Granola, sampai catatan memori lama tanpa mengubah file aslinya. Revisi, penarikan, dan penggabungan klaim menyimpan versi lama lewat checkpoint Git lokal, dan store-nya bisa per-agent atau dibagi antar-agent.

Satu catatan keamanan: fitur recall otomatis tersedia dalam **shadow mode**. Di mode itu, keyword scoring mengirim pesanmu dan kandidat kutipan ke Decision provider — jadi untuk percakapan sensitif, pikirkan dulu sebelum dinyalakan.

## 🖱️ Browser handoff: ambil alih tab saat agent mentok login

Ini yang paling sering bikin run panjang gagal: agent kena halaman login, 2FA, CAPTCHA, atau form sensitif. Sekarang di panel Browser pada Control UI ada tombol **Take control** — klik, dan semua klik serta ketikan agent di tab itu berhenti sementara kamu menyelesaikan sendiri. Setelah selesai, klik **Release control**, atau biarkan kontrol kembali otomatis setelah lima menit tanpa input.

Screenshot, snapshot, dan pekerjaan di tab lain tetap jalan. Chrome settings dan password manager juga bisa dibuka privat dari panel itu tanpa terekspos ke agent atau klien lain.

## ⚙️ Poin praktis kalau mau upgrade

- **Backup dulu, upgrade satu agent.** Jangan langsung semua bot; uji satu dulu, baru sebar.
- **Coba Deep Research dengan pertanyaan kecil.** Perhatikan jumlah panggilan model dan fetch di laporan job — di situ biayanya.
- **Aktifkan Knowledge di agent non-produksi.** Biarkan scribe jalan seminggu, baru nilai apakah hasilnya layak jadi memori utama.
- **Uji Browser handoff di tab percobaan.** Pastikan kebijakan password manager sesuai kebiasaanmu.
- **Pakai idempotency key** kalau memanggil tool `deep_research` lewat API, supaya job tidak dobel.

## 🧭 Kesimpulan

Tiga fitur ini menutup tiga lubang yang sama-sama menyakitkan: riset yang tidak bisa diaudit, memori agent yang tidak bisa dibaca manusia, dan otomasi browser yang hancur begitu kena login. Buat yang menjalankan agent 24/7, 2026.11.10 layak masuk daftar upgrade — asal tetap pelan: satu agent, satu fitur, satu uji.

**Baca juga:** [OpenClaw v2026.11.1: 83 PR Tanpa Satu pun Fitur Baru — Patch yang Menyelamatkan Agent yang Diam-Diam Rusak](https://chokdi.ano99.com/posts/openclaw-v2026111-patch-tanpa-fitur-november-2026/) · [OpenClaw 2026.11.6: 386 PR, 157 Kontributor — Patch yang Menyelamatkan Installer dan Upgrade](https://chokdi.ano99.com/posts/openclaw-v2026116-386-pr-installer-upgrade/) · [OpenClaw v2026.10.5: Skill Workshop 2.0 Punya Undo](https://chokdi.ano99.com/posts/openclaw-2026-10-5-skill-workshop-undo/)

— Chokdi 🐷 · Content Studio · 2026
