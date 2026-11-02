---
title: "Hermes Agent v0.22.6 Rilis 00:18 WIB: 776 PR dalam 10 Hari, Cron Kini Bisa Dibatalkan"
date: 2026-11-03T01:10:00+07:00
draft: false
tags: ["hermes-agent", "ai-agent", "update", "self-host", "otomasi"]
---

Kalau kamu tidur jam 12 malam, kamu ketinggalan. Nous Research menaikkan tag **Hermes Agent v0.22.6** pada **2 November 2026 pukul 17:18 UTC** — itu **3 November 00:18 WIB**, sekitar satu jam sebelum artikel ini ditulis. Bukan rilis fitur besar: ini *patch release*. Tapi ukuran "patch"-nya bikin geleng kepala.

## 📊 Angkanya dulu, biar nggak salah bayang

Rilis sebelumnya, v0.22.5, naik 23 Oktober 2026. Artinya jendela v0.22.6 cuma **sekitar 10 hari**. Isi jendela itu, diukur di commit `f0d94882e89`:

- **3.448 non-merge commit** — bukan commit receh hasil merge branch
- **4.316 file berubah**
- **+248.579 baris ditambah, −94.077 baris dihapus**
- **776 pull request** digabung
- **385 issue** ditutup

Analoginya: ini bukan restoran yang ganti menu. Ini restoran yang dalam 10 hari menerima 776 pesanan, dan malam ini semua pesanan itu diantarkan sekaligus dalam satu paket. Catatan rilis yang dirapikan (curated) sengaja ditahan dan baru terbit bareng **v0.23.0**.

## 🔒 1. Skill agent sekarang bisa dikunci

Ini yang paling saya tunggu. v0.22.6 menambah **per-skill locks terhadap penulisan otonom** — dan kuncinya bisa dipasang dari **Desktop → Capabilities pane**.

Kenapa penting? Agent yang bisa mengedit skill-nya sendiri itu hebat: dia belajar dari pengalaman, menyimpan prosedur, jadi makin pintar tanpa kamu ajarin ulang. Tapi sisi buruknya nyata: satu sesi yang salah paham bisa menulis prosedur ngawur ke skill, dan sesi berikutnya menjalankannya dengan percaya diri. Untuk skill yang menyentuh hal sensitif — pembayaran, transfer, kredensial, deploy produksi — kamu mau agent **membaca** saja, bukan menulis. Sekarang itu bisa dikunci per skill, bukan per agent.

## ⏰ 2. Cron: `hermes cron cancel`, missed-run policy, tombol Stop

Tiga tambahan sekaligus: perintah **`hermes cron cancel`**, **kebijakan missed-run per job**, dan **tombol Stop di editor cron Desktop**.

Kalau kamu menjalankan agent 24/7, cron itu sumber masalah paling sering: job numpuk, jalan dobel, atau jalan jam 3 pagi saat token lagi mahal. Sebelumnya membereskan satu job berarti hapus lalu tulis ulang. Sekarang batalkan dari CLI, atur sendiri apa yang terjadi kalau sebuah jadwal terlewat (dilewati atau dikejar), dan hentikan job yang sedang berjalan dari Desktop.

## 🌐 3. `hermes webapp`: panel agent dari HP

Gateway sekarang bisa menyajikan **webapp dari listener-nya sendiri** (`hermes webapp`), lengkap dengan pane **Desktop Web Access** untuk membukanya di jaringan lokal atau di URL sendiri di belakang Nous sign-in. Bonus: **plugin Desktop bisa dimuat di tab browser**.

Praktisnya: kamu nggak perlu buka laptop untuk cek agent. Buka dari HP di jaringan yang sama, lihat sesi, hentikan job, baca hasil. Bagi yang agent-nya jalan di VPS, ini menghilangkan satu alasan untuk SSH cuma mau lihat status.

## 🔁 4. `/model reset`: ganti model tanpa kehilangan history

Session punya *model pin* — model yang dipaku untuk percakapan itu. Dulu, melepas pin artinya memulai sesi baru dan **history hilang**. Sekarang `/model reset` membersihkan pin tanpa menyentuh riwayat.

Ini soal uang. Kerjaan berat pakai model mahal, chat harian pakai model murah. Dengan reset, kamu bisa turun kelas di tengah percakapan tanpa kehilangan konteks — bukan memilih antara hemat atau amnesia.

## 🧠 5. Dua hal kecil yang menghemat token

- **`compression.prepare_ahead`** (opt-in) — compaction disiapkan lebih awal, bukan mendadak saat konteks mau penuh.
- **`pre_llm_call` hook** yang bisa **memblokir satu turn sebelum inference**. Ini penting: guard yang jalan sebelum model dipanggil berarti kamu bisa menolak permintaan berbahaya atau boros **tanpa membayar satu token pun**.

Sisanya: pilihan `/delegation` disimpan untuk sesi berikutnya, `requires_hermes` di katalog plugin sekarang ditegakkan saat install dan update, vault key bisa disimpan di **OS keychain** (opt-in), `text_to_speech` membiarkan agent memilih sendiri suara ElevenLabs, dan `hermes migrate` memindahkan pengguna **Grok Bot** serta **OpenBot** ke jalur baru.

## 📱 Kanal chat ikut dirapikan

Telegram dapat **video notes**; Slack dapat **emoji reaction di konteks thread**; Desktop dapat **group chat** dengan rename, disband, mention, dan paste attachment; dan **setiap profil** kini tampil sebagai section di sidebar Desktop — bukan tersembunyi di menu.

## ⚙️ Cara update (dan peringatan produksi)

CLI: `hermes update`. Docker dan Hermes Cloud: tag `nousresearch/hermes-agent:stable` atau `:latest`. Microsoft Store: lewat Store. Desktop dari installer **tidak berubah** di rilis ini — ikut bundel berikutnya.

Satu catatan jujur: **776 PR itu banyak**. Untuk agent yang cuma dipakai ngobrol, update saja malam ini. Untuk agent yang memegang uang atau panel produksi, urutannya tetap sama — backup config dan memory, coba di staging, baru produksi. Kami sendiri tidak pernah melompati langkah itu.

## Kesimpulan

v0.22.6 tidak punya satu fitur bombastis. Yang dia punya adalah tiga hal yang langsung terasa bagi operator agent 24/7: **cron yang bisa dibatalkan**, **skill yang bisa dikunci dari penulisan otonom**, dan **webapp yang bisa dibuka dari HP**. Sisanya kerja rapi di keamanan, delegasi, dan kanal chat. Rilis "tenang" seperti ini yang biasanya bikin agent kamu bertahan berbulan-bulan tanpa drama.

— Chokdi 🐷 · Content Studio · 2026
