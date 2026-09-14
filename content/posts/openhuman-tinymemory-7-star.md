---
title: "OpenHuman 39.774 Star, Tapi Mesin Memori TinyMemory Cuma 7 Star"
date: 2026-09-14T18:10:00+07:00
draft: false
tags: ["AI", "Agent", "Open Source", "Riset"]
---

OpenHuman mendadak jadi bahan obrolan di mana-mana: agent harness open source yang katanya punya "mesin memori revolusioner". Kami cek langsung ke kode dan API GitHub-nya — dan hasilnya jauh lebih menarik daripada klaimnya. Angka bintangnya luar biasa, tapi mesin memori yang digadang-gadang ternyata nyaris nggak punya penonton.

## 39.774 star dalam 7 bulan

Per 14 September 2026, repo `tinyhumansai/openhuman` sudah mengumpulkan **39.774 star** dan **3.922 fork**, dengan 186 issue terbuka. Repo ini baru dibuat 18 Februari 2026, ditulis dengan Rust, dan masih aktif di-push — commit terakhir hari ini juga. Di Product Hunt mereka menang Product of the Week.

Untuk ukuran proyek 7 bulan, itu pertumbuhan yang gila. Wajar kalau banyak orang langsung menyimpulkan: "ini masa depan agent lokal".

Tapi satu kebiasaan yang selalu kami pakai sebelum percaya: **buka repo-nya, jangan cuma baca thread**.

## Mesin memorinya cuma 7 star

OpenHuman bukan monolit. Ada tiga repo terpisah di organisasi yang sama. Kami tarik angkanya langsung dari GitHub API hari ini:

| Repo | Fungsi | Star | Fork | Bahasa | Lisensi |
|---|---|---|---|---|---|
| `openhuman` | Agent harness + aplikasi desktop | **39.774** | 3.922 | Rust | GPL-3.0 |
| `tinycortex` | Engine memori ("Fastest AI Memory Model") | **253** | 39 | Rust | GPL-3.0 |
| `tinymemory` | Memory engine utama | **7** | 13 | Rust | GPL-3.0 |

Perhatikan barisan terakhir. Yang punya 39 ribu star adalah **aplikasi desktop**-nya — maskot, UI, integrasi, pengalaman pakai. Yang disebut-sebut sebagai mesin memori canggih justru baru dibuat 10 Agustus 2026 dan punya **7 star**.

Ini bukan berarti kodenya jelek. Justru sebaliknya: pemisahan modul `tinymemory` rapi sekali — ada lapisan kontrak (`tinymemory-api`) yang bebas dependensi, bus tipe, core, sampai lapisan engine TinyCortex. Host bisa ganti engine memori tanpa recompile. Itu desain yang matang.

Masalahnya cuma satu: **popularitas aplikasi bukan bukti kualitas mesin di dalamnya**.

## Apa yang benar-benar ada (dan yang cuma klaim video)

Situs resmi OpenHuman cukup jujur soal ini. Mereka menulis: *"OpenHuman's memory engine decides what to keep, how to compress it, and what surfaces when an agent needs context."* Di README-nya, memori OpenHuman digambarkan sebagai **Memory Tree + Obsidian vault**, dengan opsi backend `agentmemory` — artinya memorinya bisa dibaca manusia sebagai file Markdown biasa.

Yang klaimnya perlu disaring adalah angka-angka di video review. Kami sudah membedah kode `tinymemory-core` untuk beberapa klaim populer:

- **"4 tier memori: hot/warm/cool/cold"** → tidak ditemukan. Yang ada hanya fungsi `recency_score()` — skor sederhana berdasarkan kebaruan data.
- **"Knowledge graph skala miliar token"** → graph-nya ada, tapi `tree/graph/` hanya sekitar **156 baris**. Itu traversal BFS ringan, bukan database graph raksasa.
- **"1000x lebih cepat, $1 per 5 juta token"** → angka ini bukan dari website resmi maupun dokumentasi; tidak bisa diverifikasi dari sumber publik.
- **"Neocortex"** → di situs resmi nama itu muncul sebagai **nama model LLM** (`neocortex-mk1`) untuk backend cloud mereka, bukan sebagai mesin memori.

Yang **benar** dan layak diakui: proyeknya nyata dan serius, arsitekturnya modular, integrasinya luas (118+ koneksi, klaim dukungan sampai 100 apps / 10.000 MCP / 90.000 skills), dan aktivitas maintainernya konsisten.

## Kenapa ini penting kalau kamu mau self-host

Ada satu detail yang sering dilewatkan saat orang membahas "agent gratis": **lisensi**. Ketiga repo OpenHuman memakai **GPL-3.0**. Kalau kamu memakai, memodifikasi, lalu mendistribusikan produk turunannya (termasuk versi yang dipakai klien atau dijual), kamu terikat kewajiban GPL — termasuk membuka kode turunanmu.

Bandingkan dengan Hermes Agent yang kami pakai sehari-hari di [setup self-host di VPS](/posts/hermes-vs-openclaw-selfhost-vps/): lisensi MIT, memori self-learning, dan backend memorinya bisa ditukar — kami jalan dengan [Hindsight dan Mnemosyne](/posts/hermes-true-memory-mnemosyne-hindsight/). Untuk kebutuhan bisnis, perbedaan MIT vs GPL-3 ini bukan detail kecil.

Kalau kamu memang ingin pola "memori yang bisa dibaca sendiri", pendekatan ala [second brain untuk AI agent](/posts/second-brain-ai-agent/) sebenarnya bisa ditiru tanpa pindah platform: simpan memori sebagai Markdown, tambahkan graph entitas, lalu pakai skor kebaruan. Persis konsep yang dipakai TinyMemory — hanya tanpa harus mengganti seluruh stack.

## Pelajaran: bintang bukan bukti

Tiga hal yang kami bawa pulang dari riset ini:

1. **Pisahkan popularitas aplikasi dari kualitas komponennya.** 39.774 star bisa berarti UI-nya enak, bukan mesinnya hebat.
2. **Cek lisensi sebelum cek fitur** kalau proyeknya akan dipakai untuk kerjaan klien.
3. **Verifikasi klaim angka di kode, bukan di video.** Satu `grep` sering lebih jujur daripada satu jam menonton review.

Kalau kamu tertarik membandingkan arsitektur memori agent — atau punya pengalaman pakai OpenHuman langsung — tulis di komentar. Kami senang diuji balik.

Sumber: [repo openhuman](https://github.com/tinyhumansai/openhuman), [repo tinymemory](https://github.com/tinyhumansai/tinymemory), dan [situs resmi tinyhumans.ai](https://tinyhumans.ai/openhuman).

— Chokdi 🐷 · Content Studio · 2026
