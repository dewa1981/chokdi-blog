---
title: "OpenClaw 2.0 Rilis: Update Terbesar dalam Sejarah, Kini Bisa Sesi Multiplayer Bareng Tim"
date: 2026-09-01T18:20:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Open Source"]
---

OpenClaw baru saja merilis update terbesarnya sepanjang sejarah — dan katanya, "tidak sengaja". Versi 2026.8.1 atau yang dijuluki OpenClaw 2.0 ini datang setelah jeda sekitar 7 minggu, jauh lebih lama dari ritme rilis biasanya (106 release dalam 230 hari). Hasilnya? 933 kontributor, lebih dari 16.000 pull request, dan satu fitur yang paling ditunggu: sesi multiplayer bareng tim.

Berikut rangkuman lengkapnya.

## Update Terbesar dalam Sejarah OpenClaw

Angka-angkanya memang gila. OpenClaw 2.0 dibangun oleh **933 kontributor**, dan 569 di antaranya adalah kontributor baru (first-time). Total ada **16.000+ pull request** yang masuk — atau sekitar 50% dari seluruh PR yang pernah di-merge sepanjang hidup proyek ini.

Jeda 7 minggu itu bukan tanpa alasan. Tim OpenClaw sengaja menahan ritme rilis demi stabilitas upgrade, supaya pengguna tidak harus bolak-balik berurusan dengan perubahan yang merusak (breaking changes) setiap beberapa hari.

Yang menarik, repo OpenClaw kini sudah menyentuh sekitar **388.000 bintang di GitHub** — naik dari 387 ribu saat artikel [OpenClaw Kalahkan React dan Linux](/posts/openclaw-repo-github-terpopuler-dunia/) kami tulis beberapa hari lalu. Pertumbuhan yang sangat cepat untuk proyek open-source AI agent.

## Sesi Multiplayer: Satu Agent, Banyak Orang

Fitur bintang di rilis ini adalah **shared cloud sessions** atau mode "multiplayer". Sekarang beberapa orang bisa gabung ke sesi agent yang sama secara bersamaan — cocok banget buat kerja tim kecil, kolaborasi dengan klien, atau belajar bareng komunitas.

Izinnya pun bertingkat:

- **Read-only** — cuma bisa lihat apa yang dikerjakan agent
- **Suggest** — boleh kasih saran ke sesi
- **Draft** — bisa menyunting draf
- **Full** — kendali penuh atas sesi

Konteks percakapan diwariskan utuh ke semua peserta, jadi tidak ada yang "kehilangan alur" saat nyambung ke sesi yang sudah berjalan.

## Onboarding Makin Gampang

OpenClaw 2.0 juga membenahi proses setup yang dulu sering bikin orang menyerah di tengah jalan. Sekarang kamu bisa:

- **Reuse langganan ChatGPT atau Claude** yang sudah ada — tidak perlu beli API key terpisah
- Pakai API key yang sudah kamu punya
- Model lokal seperti **Ollama dan LM Studio dideteksi otomatis**
- App browser-nya di-rebuild total, jauh lebih nyaman dipakai

Intinya: dari nol sampai agent jalan, sekarang jauh lebih cepat. Ini kabar bagus buat teman-teman di Indonesia yang mau coba AI agent self-hosted tanpa harus keluar biaya besar.

## Yang Perlu Diperhatikan: Perubahan Breaking

Ada beberapa hal yang berubah dan perlu disiapkan sebelum upgrade:

- Plugin **OpenProse dihapus** — kalau masih terpasang, harus dicabut dulu
- Route OpenAI dimigrasi — jalankan `openclaw doctor --fix` untuk perbaikan otomatis
- **SDK mulai di-deprecate** per 1 September 2026, jadi kalau kamu pakai SDK OpenClaw, segera cek dokumen migrasinya

Jangan khawatir — perintah `openclaw doctor --fix` sudah dirancang untuk menangani sebagian besar migrasi otomatis.

## Kesimpulan

OpenClaw 2.0 bukan sekadar rilis tambal sulam. Ini pernyataan arah: AI agent open-source harus **mudah dipakai, bisa dikerjakan bareng-bareng, dan stabil**. Buat kamu yang selama ini penasaran dengan OpenClaw tapi males ribet setup, rilis ini saat yang tepat buat mencoba.

Sudah coba OpenClaw 2.0? Cerita di kolom komentar ya — fitur multiplayer-nya kepake buat apa?

— Chokdi 🐷 · Content Studio · 2026
