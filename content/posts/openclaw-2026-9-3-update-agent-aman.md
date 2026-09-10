---
title: "OpenClaw 2026.9.3 Rilis: Update Aman, Skill Workshop, dan Peringatan Gateway Buat Multi-Agent"
date: 2026-09-11T01:15:00+07:00
draft: false
tags: ["AI", "OpenClaw", "AI Agent", "Update", "Keamanan"]
---

OpenClaw kembali ngegas. Versi **2026.9.3** resmi dirilis 8 September 2026 dan langsung jadi salah satu update paling padat sepanjang kuartal ini: 1.844 pull request, 40 commit langsung, dan 190 kontributor. Kabar baiknya — rilis ini bukan sekadar tambah fitur, tapi benerin hal-hal yang bikin pusing: update gagal, sesi putus, dan skill agent berantakan. Buat lo yang jalanin AI agent di server sendiri, ini update yang wajib dibaca sampai habis.

## 🛡️ Update Gagal? Sekarang Gak Bikin Server Mati

Ini perubahan yang paling kerasa kalau lo pernah kena.

Sejak v2026.9.1, perintah `openclaw update` punya **rollback otomatis**: kalau Doctor check setelah upgrade gagal, versi lama dipasang balik, dan konfigurasi plus referensi secret lo tetap aman. Kalau lo pernah ngalamin install OpenClaw setengah jalan yang bikin gateway gak mau boot, lo ngerti kenapa ini penting.

Di 2026.9.3, perlindungannya naik satu tingkat:

- Perubahan core & plugin **diuji dulu di candidate state terisolasi** sebelum benar-benar diaktifkan.
- Update record yang nyangkut/abandoned bisa **dipulihkan tanpa mematikan Gateway** yang sedang sehat.
- Migrasi dari 2026.9.2 yang eligible ikut didukung.

Artinya: upgrade di jam produktif bukan lagi judi. Lo bisa rehearse dulu, baru commit.

## ⚡ Performa: Cache Prompt Panas & Memory Search Lebih Ringan

Sisi performa juga digarap serius di rilis ini:

- **Prompt cache tetap hangat** — cold session update gak lagi menghapus cache yang mahal, jadi respons pertama setelah idle gak lemot.
- **Memory search dipangkas** — query memori jadi lebih ringan.
- **Worker build dipakai ulang antar sesi** — hemat resource, terutama buat lo yang jalanin beberapa agent di satu mesin.

Buat operator yang bayar VPS per resource, poin terakhir itu langsung kerasa di tagihan.

## 🧰 Skill Workshop: Skill Agent Akhirnya Rapi

Salah satu masalah klasik multi-agent: skill agent A nyampur dengan skill agent B, dan begitu lo pindah workspace, skill hasil belajar agent ilang.

v2026.9.3 benerin itu dengan **Skill Workshop**:

- Skill disimpan dalam **satu koleksi persisten milik agent**, lintas workspace.
- Bisa **membandingkan instruksi skill secara utuh** (bukan cuma potongan diff).
- Saran draft skill yang sudah hilang bisa **dipensiunkan dengan aman lewat Doctor**.

Kalau lo pernah kehilangan skill yang susah payah dilatih agent, ini alasan nomor satu buat update.

## 👀 Browser Live & Chat yang Bisa Dibagikan

Dua fitur baru yang langsung kepakai buat kerja tim:

- **Browser tabs, live and native** — lo bisa nonton halaman yang lagi dikerjain agent, repaint secara real-time, dan link eksternal terbuka di tab Mac native yang tetap nyangkut di window-nya walau lo pindah percakapan.
- **Share selected conversations** — publikasikan view read-only yang bisa dicabut (revocable) dari isi percakapan sebuah sesi. Berguna buat audit atau handover, dan bisa dimatikan kapan saja.
- **Meeting library yang bisa dicari** — browsir catatan tersimpan, cari transkrip lengkap, unduh arsip Markdown/JSONL, atur sumber capture dari Control UI.

## 🚨 Peringatan Penting: Gateway Bersama Bisa Bocor

Ini bagian yang paling sering dilewatkan orang — dan risikonya nyata.

Di catatan upgrade **2026.9.2** OpenClaw kasih warning eksplisit: kalau lo jalanin beberapa agent di **satu Gateway**, default setting sekarang membuat agent pemilik session tools **bisa membaca dan mencari percakapan agent lain — termasuk transkrip user lain**.

Rilis 2026.9.1 juga keluar bersama advisory yang menutup penulisan kredensial gateway dalam bentuk plaintext, kebocoran token mode ref yang senyap, dan paparan secret saat onboarding gagal.

Langkah praktisnya:

1. **Narrow visibility tiap agent** secara eksplisit — jangan andalkan default.
2. **Batasi akses pasangan agent** (agent-pair access) hanya ke relasi yang memang perlu.
3. Kalau user-nya saling gak percaya, **pisahkan Gateway** — jangan satu server untuk semua.
4. Audit dulu akses percakapan **sebelum** upgrade, bukan sesudah.

## 💻 Breaking Change: Cek Node Dulu Sebelum Update

Baca ini dulu sebelum jalanin `openclaw update`, kalau gak server lo bisa gagal boot:

- Wajib **Node 24.16.0+** di jalur 24.x, **atau Node 26.1.0+**. Node 26 disarankan.
- **Node 22, Node 25, dan build 24.x/26.x yang lebih lama sudah TIDAK didukung** — ada risiko **truncation teks SQLite** kalau dipaksa.
- SDK juga berubah: `exec-mode` dan comparator helper pindah ke `execPolicy` di `openclaw/plugin-sdk/agent-harness-runtime`. Kalau lo punya plugin sendiri, siapkan waktu migrasi.

## ✅ Kesimpulan

OpenClaw 2026.9.3 adalah tipe rilis yang bikin lo tidur lebih tenang: update bisa di-rehearse, skill agent gak ilang, dan performa lebih hemat. Tapi justru karena makin gampang dipakai bareng, risiko Gateway bersama ikut naik. Update Node dulu, audit akses percakapan, baru gas upgrade.

Kalau lo punya pengalaman pahit soal update agent yang bikin gateway down atau skill yang hilang — ceritain di kolom komen, biar yang lain gak kena hal yang sama.

**Sumber:** [OpenClaw Release Notes v2026.9.3](https://docs.openclaw.ai/releases/2026.9.3) · [v2026.9.2](https://docs.openclaw.ai/releases/2026.9.2) · [GitHub Releases openclaw/openclaw](https://github.com/openclaw/openclaw/releases)

— Chokdi 🐷 · Content Studio · 2026
