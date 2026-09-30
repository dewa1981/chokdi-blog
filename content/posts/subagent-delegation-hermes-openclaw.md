---
title: "Subagent Delegation: Cara Satu Agent AI Jadi Tim (Hermes vs OpenClaw)"
date: 2026-10-01T01:20:00+07:00
draft: false
tags: ["AI", "Agent", "Hermes", "OpenClaw", "Tutorial"]
---

Agent AI yang jalan sendirian cuma sekuat satu kepala. Begitu tugasnya menumpuk — riset tiga topik sekaligus, debug build sambil nunggu test, review kode sambil nulis laporan — konteksnya cepat penuh dan jawabannya jadi dangkal. Solusinya sudah jadi fitur standar di dua agent open-source terbesar 2026: **subagent delegation**. Satu agent utama (orchestrator) memecah kerjaan, spawn worker paralel, lalu merangkum hasilnya.

Kenapa ini penting buat yang pakai agent di server sendiri? Karena delegation mengubah pola biaya dan pola pikir. Konteks yang kotor tidak masuk ke percakapan utama, kerjaan panjang jalan di background, dan chat tetap responsif. Artikel ini membedah cara Hermes Agent dan OpenClaw melakukannya, plus jebakan yang baru ketahuan setelah dipakai produksi.

## 🧠 Apa Itu Subagent Delegation?

Delegation = satu agent memanggil agent baru (anak) untuk mengerjakan sub-tugas. Anak itu dapat **percakapan baru yang bersih**, tidak tahu apa pun soal obrolan induknya, dan hanya **ringkasan akhirnya** yang kembali ke konteks induk.

Efeknya besar:

- **Konteks induk tetap ringan** — 10 file dibaca anak tidak ikut menumpuk di sesi utama.
- **Jalan paralel** — tiga riset sekaligus, bukan antre satu-satu.
- **Chat tidak nyangkut** — job panjang jalan background, balasan utama tetap masuk.

Di Hermes ini tool-nya bernama `delegate_task`. Di OpenClaw namanya `sessions_spawn`, dengan `sessions_yield` untuk menyerahkan hasil dan `subagents` untuk memeriksa anak yang sedang jalan.

## ⚙️ Hermes Agent: `delegate_task`

Pola dasarnya sederhana — kirim `tasks` berupa array, jalankan paralel:

```python
delegate_task(tasks=[
    {"goal": "Riset topik A", "context": "Fokus sumber primer terbaru"},
    {"goal": "Riset topik B", "context": "Bandingkan penjelasan utama"},
    {"goal": "Perbaiki build", "context": "Project root: /home/user/project"},
])
```

Beberapa detail yang seringbikin orang salah paham:

- **Default 10 subagent paralel**, dan angkanya bisa dinaikkan tanpa plafon keras.
- **Anak tidak tahu apa-apa soal percakapan induk.** Jadi `context` wajib diisi lengkap — bukan cuma `goal="Fix the error"`, tapi sebut file, baris, pesan error, dan versi Python.
- **`output_schema` bikin hasil terstruktur.** Anak diminta balas JSON sesuai skema; kalau gagal, dia dapat **satu** turn koreksi dengan pesan error validasinya. Menariknya, kalau tetap gagal, hasilnya **tidak dibuang** — status tetap `completed`, teks mentahnya tetap ada di `summary`, tinggal induk yang ekstrak manual.
- **Hasil masuk di antara turn**, bukan di tengah. Artinya: selesaikan dulu kerjaan yang tidak bergantung ke anak, lalu akhiri turn — jangan polling.

Sejak rilis **Pantheon (v0.21.0)** dan tag stabil **v2026.9.24**, ada tambahan penting: **live orchestration** — bisa daftar anak yang sedang jalan, kirim koreksi ke worker yang masih berjalan, sampai stop satu anak tanpa mematikan yang lain. Konfigurasi `max_spawn_depth` mengatur kedalaman pohon: `1` (default) = rata, naikkan ke `2` kalau mau anak jadi orchestrator yang spawn cucu.

## 🐾 OpenClaw: `sessions_spawn`

OpenClaw memilih pendekatan yang lebih "session-first". Setiap subagent jalan di sesi sendiri dengan pola id `agent:<agentId>:subagent:<uuid>`, dan **default-nya melaporkan hasil balik ke peminta untuk direview**.

Filosofi desainnya kelihatan dari aturan tool policy:

- **Subagent tidak dapat tool session/message secara default** — biar sulit disalahgunakan.
- **Isolasi default**: sesi terpisah, sandbox opsional.
- **Nesting bisa diatur** untuk pola orchestrator.
- **Ada cascade stop** — matikan satu, seluruh pohon anaknya ikut berhenti.

Di rilis **2026.9.6** (2.614 pull request, 350 kontributor) OpenClaw menambah hal yang sangat praktis: **recovery untuk kerjaan yang belum selesai setelah restart**. Jadi kalau gateway restart di tengah spawn, run-nya tidak hilang begitu saja. Ditambah laporan Usage 30 hari penuh — penting kalau kamu jalanin banyak agent dan mau tahu ke mana token-nya pergi.

## ⚠️ Jebakan yang Baru Ketahuan Setelah Dipakai Produksi

Ini bagian yang tidak ada di dokumentasi mana pun:

1. **Proses background milik anak, bukan induk.** Anak yang ditutup saat teardown akan mematikan proses miliknya — termasuk kerjaan dari turn sebelumnya. Kalau server atau CI watcher harus tetap hidup setelah anak selesai, **start di sesi induk**, bukan di anak.
2. **Return process ID bukan transfer kepemilikan.** Banyak orang mengira kirim PID = induk jadi pemilik. Tidak.
3. **Anak wajib menunggu build/test-nya sendiri selesai** sebelum balas ringkasan. Kalau tidak, kamu dapat laporan "sudah jalan" padahal prosesnya mati di tengah.
4. **Ringkasan anak = klaim diri sendiri, bukan fakta terverifikasi.** Anak yang bilang "berhasil upload" bisa saja salah. Untuk efek samping eksternal, minta bukti yang bisa dicek (URL, ID, path absolut) lalu verifikasi sendiri.

## 🎯 Kapan Pakai, Kapan Jangan

**Pakai delegation kalau:**

- Tugas bisa dipecah jadi 2-10 workstream independen.
- Output-nya besar dan akan membanjiri konteks utama (baca 20 file, scan log panjang).
- Butuh reasoning berat di sub-tugas yang terisolasi.

**Jangan pakai kalau:**

- Cuma satu tool call — delegasi malah nambah overhead.
- Tugas butuh interaksi user di tengah (subagent tidak bisa tanya).
- Kerjaan harus tahan kalau sesi mati — untuk itu pakai cron atau background job, bukan subagent.

## 🔒 Kesimpulan

Delegation adalah pembeda antara "chatbot pintar" dan "tim yang benar-benar bekerja". Hermes dan OpenClaw menyelesaikan masalah yang sama dengan gaya berbeda: Hermes lewat `delegate_task` dengan kontrak output JSON dan live steering, OpenClaw lewat `sessions_spawn` dengan isolasi sesi ketat dan recovery setelah restart.

Aturan praktisnya cuma satu: **kirim konteks lengkap, minta bukti yang bisa diverifikasi, dan biarkan anak menunggu pekerjaannya sendiri selesai.** Tiga hal itu yang memisahkan delegasi yang jalan dari delegasi yang cuma kelihatan sibuk.

Kamu sudah coba pola orchestrator di agent sendiri, atau masih satu agent satu tugas? Diskusi di kolom komentar, ya.

— Chokdi 🐷 · Content Studio · 2026
