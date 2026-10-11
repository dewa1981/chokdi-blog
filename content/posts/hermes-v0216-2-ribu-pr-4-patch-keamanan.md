---
title: "Hermes Agent v0.21.6: 2.106 PR dalam 2 Minggu — dan 4 Lubang Keamanan yang Ditambal"
date: 2026-10-11T17:16:00+07:00
draft: false
tags: ["AI", "Hermes Agent", "Open Source", "Keamanan", "Agent AI"]
---

Nous Research menandai **Hermes Agent v0.21.6** pada 8 Oktober 2026. Sekilas ini cuma "patch release" biasa — tapi angka di dalamnya bikin melongo: **2.106 pull request di-merge**, **3.027 issue ditutup**, dan **8.867 commit non-merge** dalam satu jendela rilis. Yang lebih penting buat kita: empat lubang keamanan serius ikut ditambal di rilis ini.

## 📊 Skala Rilis: Angka yang Bicara

Diukur pada commit `818c13be`, jendela sejak v0.21.5 berisi:

- **2.106 PR merged** dan **3.027 issue ditutup**
- **8.867 non-merge commit** di **8.342 file** berubah
- **+772.490 baris** ditambah, **−225.600 baris** dibuang

Sebagai pembanding, v0.21.5 (24 September) "hanya" 460 PR, dan v0.21.4 (21 September) sekitar 1.800 PR. Jadi kecepatan tim Nous bukan cuma stabil — makin cepat.

Yang menarik: catatan rilis lengkap sengaja **ditahan untuk v0.22.0**. Semua fitur dari v0.21.0 ke atas baru akan didokumentasikan penuh di rilis berikutnya, lengkap dengan kredit kontributor. Artinya v0.21.6 ini adalah "titik aman" — stabil untuk dipakai, tapi cerita lengkapnya menyusul.

## 🏭 Yang Baru: Pipeline Rilis Stabil

Ini perubahan yang paling sering dilewatkan, padahal dampaknya besar:

> "This is the first release cut by the new stable release pipeline: one attempt ref, a tested Docker image, and a receipt tag at publish."

Sebelumnya, kalau kamu pakai Docker atau Hermes Cloud, agak sulit memastikan tag rilis itu benar-benar sudah teruji. Sekarang setiap rilis lewat pipeline yang sama: satu ref percobaan, image Docker yang **sudah dites**, dan tag "resi" saat dipublikasikan. Buat yang deploy di server sendiri, ini mengurangi drama "update ternyata rusak".

## 🔐 Empat Lubang Keamanan yang Ditambal (Bagian Terpenting)

Ini bagian yang wajib kamu baca kalau menjalankan Hermes dengan dashboard yang bisa diakses dari luar. Semua empat temuan datang dari **Tenable Research** (TRA-725 sampai TRA-728):

- **Spoofing header `X-Forwarded-For`** bisa mereset rate limit login dan menembus batas percobaan sign-in per IP (#133367)
- **Request login tanpa autentikasi** bisa menulis nilai tak terbatas ke auth audit log — alias bisa bikin log meledak, celah klasik buat menguras disk (#133369)
- **Route `/auth/` publik tidak punya batas ukuran body request** (#133370)
- **Sign-in native bisa mengirim kode login ke redirect non-loopback** — ini yang paling berbahaya, karena berujung **session takeover** (#130685)

Ada juga dua tambalan di luar dashboard:

- **Hardening git filter repository.** Panggilan git otomatis (snapshot workspace sesi, worktree subagent, kanban, `hermes -w`) dulu bisa menjalankan program filter `clean`/`smudge`/`process` yang didefinisikan oleh config repo yang **tidak dipercaya** — sebelum prompt pertama kamu jalan (#130661). Jadi cuma dengan berada di folder repo jahat, kode mereka bisa jalan.
- **Hardening sender email gateway.** Display name berkutip di header `From` (contoh `"Victim <victim@example.com>" <attacker@evil.test>`) dulu bisa membuat pesan penyerang lolos allowlist email — alias bisa menyamar sebagai orang yang kamu izinkan.

## 🧰 Fitur yang Diam-diam Ikut Masuk

Release body menyebut beberapa hal "undocumented here on purpose" yang tetap menarik buat pemakaian harian:

- **Transkripsi langsung saat kamu bicara** di CLI, TUI, dan Desktop (`stt.streaming`) — subtitle real-time sebelum kalimatmu selesai
- **Voice chat punya model sendiri** (`auxiliary.voice_chat`), reasoning dimatikan secara default biar balasan suara tidak lambat
- **Plugin pihak ketiga jalan di plugin host terpisah per profil** (`plugins.isolation: host`) — satu plugin bermasalah tidak merobohkan seluruh agent
- **Model lokal masuk `hermes model`**, plus **llama.cpp CUDA di Linux x64 dan arm64** — buat yang punya GPU, jalan lokal makin praktis
- **`hermes status` mode ringkas** (`--short`, `--full`) untuk cek kondisi tanpa scroll panjang
- Peringatan cron/doctor kalau **cron store tidak bisa ditulis** — penyebab nomor satu cron "jalan tapi tidak kelihatan hasilnya"

## ⚙️ Cara Update

- **Docker / Hermes Cloud:** pakai `nousresearch/hermes-agent:stable`
- **Install via git:** jalankan `hermes update`, atau ulang installer one-liner
- **Desktop & Termux:** **tidak berubah** di rilis ini; keduanya ikut di rilis bundled berikutnya

## 🎯 Kenapa Ini Relevan Buat Kita

Pelajaran yang bisa diambil: kelas bug yang paling berbahaya di agent AI **bukan** bug fitur — tapi bug di lapisan autentikasi dan input tepercaya. Empat temuan Tenable semuanya soal mempercayai header dan input yang datang dari luar. Buat kamu yang jalanin agent dengan dashboard atau gateway yang menghadap internet, tiga kebiasaan ini murah dan menyelamatkan:

1. **Jangan pernah taruh dashboard agent langsung terbuka ke internet** — taruh di belakang Cloudflare Tunnel atau Tailscale, dan pastikan header seperti `X-Forwarded-For` ditulis oleh proxy, bukan diteruskan mentah dari klien.
2. **Update ke tag stabil terbaru**, jangan nyaman di versi lama "karena aman". Lubang rate-limit dan session takeover itu justru ada di versi lama.
3. **Hati-hati membuka folder repo asing** di mesin yang sama dengan agent-mu. Hardening v0.21.6 menutup celah git filter itu, tapi tetap saja menjalankan agent dengan hak akses berlebih di laptop kerja adalah risiko yang tidak perlu.

## ✅ Kesimpulan

Hermes Agent v0.21.6 adalah bukti bahwa proyek yang cepat rilis belum tentu ceroboh: 2.106 PR digabung **sekaligus** lubang keamanan dari laporan pihak ketiga ditutup transparan dengan kredit lengkap. Pipeline rilis stabil barunya juga menjawab keluhan lama soal update Docker yang sulit diprediksi. Kalau kamu jalanin Hermes buat kerjaan harian, rilis ini layak di-update hari ini — bukan karena fitur barunya, tapi karena empat tambalan itu.

Catatan lengkap v0.22.0 masih ditunggu. Sampai saat itu, v0.21.6 adalah versi paling aman untuk dipakai.

— Chokdi 🐷 · Content Studio · 2026
