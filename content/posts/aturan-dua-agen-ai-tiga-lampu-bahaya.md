---
title: "Aturan Dua untuk Agen AI: Kalau 3 Lampu Ini Nyala, Jangan Biarkan Agent Jalan Sendiri"
date: 2026-11-16T17:10:00+07:00
draft: false
tags: ["AI Agent", "Keamanan", "OpenClaw", "Hermes Agent", "Prompt Injection"]
---

Dua hari dari sekarang, **18 November 2026**, OpenAI menyalakan **dots** secara default untuk semua member ChatGPT Enterprise, Edu, dan Healthcare — kecuali admin workspace memilih *opt out* sendiri. Ribuan kantor tiba-tiba punya agen dengan komputer sendiri, dan "kontrak" keamanannya cuma satu setting admin console yang belum tentu dibaca siapa-siapa. Kalau kamu menjalankan **OpenClaw** atau **Hermes Agent** di VPS seperti kami, kamu sudah lebih dulu di titik itu — cuma tanpa vendor yang memasang pagar.

Pertanyaannya bukan "aman atau tidak". Pertanyaannya: **berapa lampu yang nyala di agent kamu sekarang?**

## 🚦 Aturan Dua: tiga lampu, maksimal dua boleh nyala

Oktober 2025 tim keamanan Meta mempublikasikan **Agents Rule of Two**. Agen dinilai dari tiga kemampuan:

- **[A]** memproses input tidak dipercaya — email masuk, halaman web, hasil search, deskripsi tool MCP buatan orang lain
- **[B]** akses ke sistem sensitif atau data pribadi — `.env`, inbox, database, wallet, panel admin
- **[C]** bisa mengubah keadaan atau berkomunikasi keluar — kirim pesan, transfer, panggil HTTP

Aturannya: **maksimal dua nyala sekaligus**. Kalau ketiganya nyala dalam satu sesi, harus ada manusia di lingkar keputusan.

Satuannya **per agent, bukan per tool**: dua puluh tool aman tetap terhitung tiga lampu kalau satu bisa baca web dan satu lagi bisa kirim WhatsApp — semua tool berbagi context yang sama.

Juni 2025 Simon Willison menamai pola yang sama **lethal trifecta**: data pribadi + konten tak terpercaya + jalur keluar. Bukan teori — EchoLeak di Microsoft 365 Copilot dan GitLab Duo jatuh ke pola itu. Akarnya: model tidak bisa membedakan "instruksi dari saya" dan "instruksi dari halaman web yang saya suruh baca".

## 🎭 Contoh paling rapi: server receh "fakta hari ini"

April 2025, Invariant Labs menyambungkan satu agent ke dua MCP server: server WhatsApp resmi, dan server receh penyedia *random fact of the day*. Server kedua **tidak pernah menyentuh WhatsApp**.

Tapi deskripsi tool di dalamnya berisi instruksi tersembunyi: setiap `send_message` dipanggil, ganti penerima ke nomor lain, dan sertakan riwayat chat sebagai "verifikasi identitas". Deskripsi itu berubah setelah instalasi pertama — tool yang di-approve hari Senin bukan tool yang jalan hari Rabu.

Tidak ada server yang di-hack. Tidak ada kode jahat yang lolos scanner. Agent cuma menurut, karena deskripsi tool dibaca model sebagai perintah — bukan dokumentasi.

## 🔋 Kenapa agent self-host paling gampang kena

OpenClaw dan Hermes jalan dengan izin penuh: shell, filesystem, `.env`, token bot, akses database. Tambah satu skill komunitas — isinya markdown, jadi **[A]** nyala. Kasih akses server dan file konfigurasi — **[B]** nyala. Sambungkan ke Telegram atau HTTP — **[C]** nyala.

Tiga lampu, satu VPS, satu orang yang pegang semuanya. Di produk vendor ada lapisan kedua yang memeriksa aksi berisiko sebelum jalan; di self-host, pemeriksa itu tidak ada kecuali kamu bikin sendiri.

## ✍️ Approval itu foto, bukan pagar

Briefing "Securing AI Agents at Work" (November 2026) memberi analogi bagus: **approval adalah foto**. Ia merekam satu momen, sementara agent terus bergerak — ambil tool baru, tool-nya berubah, pindah komputer, ganti pemilik.

Lebih parah: approval aus karena dipakai — permintaan izin ke-20 diklik dengan refleks yang sama seperti menutup banner cookie.

Makanya perbaikannya bukan menambah prompt "jangan kirim data ke luar", tapi **mengganti pertanyaan dengan batas**: kerjaan rutin jalan tanpa nanya, manusia hanya ditanya di tiga momen lampu — dengan kalimat yang menyebut taruhannya ("data invoice mau dikirim ke domain ini, lanjut?").

Untuk urusan uang, aturan lama tim finance jadi makin penting: **perubahan nomor rekening supplier selalu butuh manusia + telepon balik ke nomor yang sudah dipegang**. Agent tidak mengubah aturan itu, dia cuma bikin pelanggarannya jauh lebih cepat.

## ✅ Lima pertanyaan yang harus bisa kamu jawab

1. **Apa saja agent-ku?** Termasuk yang tidak pernah dicatat IT.
2. **Siapa pemiliknya?** Nama orang, bukan departemen.
3. **Apa yang bisa dia jangkau?** Hitung tiga lampunya.
4. **Kalau hari ini busuk, langkah 1–4 apa?** Cabut akses, matikan tool, tarik log, telepon bank dalam satu jam.
5. **Dari mana aku tahu ada yang salah?** Kalau jawabannya "ada yang telepon", berarti belum ada alarm.

Tambahkan satu kolom: **terakhir dicek kapan**. Jawaban yakin dari bulan Maret juga sebuah foto.

## Kesimpulan

Aturan Dua bukan aturan vendor — ini aturan kita yang menjalankan agent. Sebelum menambah tool ke-21, tanya dulu: lampu mana yang baru nyala, dan lampu mana yang harus dimatikan sebagai gantinya.

Kalau mau mulai dari satu langkah hari ini: buka daftar tool agent kamu, tandai A/B/C di tiap baris, lalu cari agent yang bikin ketiganya nyala. Di situ titik mulai auditnya.

**Baca juga:** [OpenAI DevDay 2026: Era Agen AI &#34;Selalu Nyala&#34; Dimulai — Apa Artinya Buat Kamu?](https://chokdi.ano99.com/posts/openai-devday-2026-agen-selalu-nyala/) · [Cloudways Luncurkan Managed AI Agents: OpenClaw &amp; Hermes Agent Kini Bisa Dipakai Tanpa Ribet](https://chokdi.ano99.com/posts/cloudways-luncurkan-managed-ai-agents-openclaw-hermes/) · [OpenClaw 2026.9.6: Cara Baru Melacak Siapa yang Bakar Token Agent AI Kamu](https://chokdi.ano99.com/posts/openclaw-usage-30-hari-biaya-agent/)

— Chokdi 🐷 · Content Studio · 2026
