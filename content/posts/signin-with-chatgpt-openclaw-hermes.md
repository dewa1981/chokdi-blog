---
title: "Sign in with ChatGPT: OpenAI Buka Langganan ChatGPT ke OpenClaw & Hermes Agent"
date: 2026-09-30T09:20:00+07:00
draft: false
tags: ["AI", "OpenClaw", "Hermes Agent", "OpenAI", "ChatGPT"]
---

Selama ini ada tembok tak terlihat antara **langganan ChatGPT** dan **API OpenAI**. Kamu bayar ChatGPT Plus atau Pro tiap bulan, tapi begitu mau dipakai di agent AI seperti OpenClaw atau Hermes Agent, kamu tetap harus bikin API key dan bayar lagi per token. Dua tagihan, satu otak.

Sejak **29 September 2026**, tembok itu dibongkar. OpenAI resmi mengumumkan **Sign in with ChatGPT** — sebuah cara untuk memakai langganan ChatGPT-mu di aplikasi pihak ketiga, **tanpa API key, tanpa tagihan token terpisah**. Dan yang menarik untuk kita: **OpenClaw ada di daftar mitra resminya**.

## 🤝 Apa Itu Sign in with ChatGPT?

Sederhananya, ini **OAuth untuk langganan ChatGPT**. Alurnya:

1. Buka aplikasi yang mendukung (misal OpenClaw)
2. Pilih **Sign in with ChatGPT** atau **Continue with ChatGPT**
3. Login pakai akun ChatGPT-mu
4. Tinjau izin yang diminta, lalu **pilih apakah aplikasi boleh memakai kuota langgananmu**

Poin pentingnya: **login dan pemakaian kuota itu dua izin terpisah**. Kamu bisa login ke aplikasi (biar akun ke-link) tapi TIDAK membiarkannya makan kuota ChatGPT-mu. Kamu juga tidak perlu membuat atau menyerahkan API key OpenAI sama sekali.

Kalau kamu izinkan pemakaian kuota, **request AI yang eligible akan dihitung ke jatah ChatGPT Work dan Codex** yang sudah termasuk di langgananmu.

## 📊 Plus dan Pro Boleh, Tapi Ada Syaratnya

Ini bagian yang sering disalahpahami. Menurut dokumentasi resmi OpenAI:

- **Siapa pun** bisa login dengan ChatGPT ke aplikasi mitra — ini murni soal identitas
- **Hanya pengguna Plus dan Pro** yang boleh memakai **kuota langganannya** di aplikasi pihak ketiga
- Aplikasi mitra juga bisa membatasi fitur ini hanya untuk paket tertentu

Ada juga batas tambahan dari sisi aplikasi: dokumentasi OpenClaw menyebut bahwa Sign in with ChatGPT memakai **jatah Codex** dengan *usage tracking* dan **limit token tersendiri**. Jadi kuota yang "dibawa" ke agent tidak identik dengan kuota chat biasa.

## 🛡️ Kontrolnya Ada di Tangan Kamu

Yang bikin ini terasa matang: OpenAI membangun kontrolnya di **Settings > Usage** ChatGPT. Kamu bisa:

- **Lihat** berapa banyak pemakaian ChatGPT yang berasal dari tiap aplikasi
- **Set limit mingguan per aplikasi** dalam bentuk persentase dari total kuota mingguanmu
- **Putuskan koneksi** kapan saja lewat *Settings > Security and login > Sign in with ChatGPT*

Dua catatan teknis yang wajib dicatat:

- **Limit aplikasi adalah CAP, bukan kolam terpisah.** Ia membatasi porsi yang boleh dimakan satu aplikasi — ia tidak menambah kuota dan tidak "memesan" jatah.
- Aplikasi bisa kena limit-nya sendiri **walaupun kuota ChatGPT-mu masih sisa**. Jadi kalau agent tiba-tiba berhenti, cek limit aplikasi dulu sebelum panik.
- Kalau kuota habis, aplikasi **berhenti** — ia tidak otomatis berpindah ke billing-nya sendiri atau memakai credit, kecuali kamu secara eksplisit mengizinkan.

Soal privasi, ini yang penting: **memakai kuota tidak memberi aplikasi akses ke percakapan atau memori ChatGPT-mu**. Yang dibagikan hanya info akun dasar: nama, email, foto profil. Dan yang dibagikan bukan API key.

## 🐾 OpenClaw Sudah Ada di Daftar — Hermes Agent Belum

Ini bagian yang paling relevan buat kita. Di halaman resmi ChatGPT Learn, OpenAI membagi mitranya jadi tiga kategori:

- **App dengan pemakaian kuota ChatGPT** (Plus/Pro): daftar mitra utama
- **App sign-in saja** (login tanpa pakai kuota): Airtable, Canva, GitLab, HubSpot, Supabase
- **Integrasi open-source**: **OpenClaw**, OpenCode, Pi, T3

**OpenClaw masuk kategori open-source integration**. Dokumentasinya pun sudah memisahkan tiga jalur autentikasi: **Codex OAuth**, **Sign in with ChatGPT**, dan **API key biasa**.

Menariknya, buat OpenClaw bisa dibilang ini bukan hal baru sepenuhnya. Sejak **Mei 2026**, OpenClaw sudah mengumumkan bahwa user bisa menjalankan turn agent OpenAI memakai langganan ChatGPT yang ada, lewat rute autentikasi Codex — yang mereka sebut *"subscription-backed Codex auth profile"*. Yang diumumkan 29 September ini adalah **generalisasinya**: sekarang jadi program resmi OpenAI, dengan visibilitas dan kontrol langsung di setting ChatGPT.

Setup-nya lewat CLI:

```bash
openclaw onboard --auth-choice openai
```

Atau untuk server headless:

```bash
openclaw models auth login --provider openai --device-code
```

Untuk **Hermes Agent**, sampai artikel ini ditulis, **Nous Portal** sudah lebih dulu menjalin kerja sama dengan OpenAI (diumumkan 29 September 2026 juga) — lewat **"Sign in with ChatGPT" di Nous Portal**, sehingga kamu bisa memakai plan ChatGPT-mu di Hermes Agent. Jalur registrasinya ada di *Account Settings > Linked Accounts* di Portal. Jadi dua agent open-source populer sekarang punya jalur resmi ke langganan ChatGPT — dengan cara pendaftaran yang berbeda.

## 💡 Kenapa Ini Penting Buat Kamu

Bagi yang menjalankan agent AI 24/7 di VPS, ini mengubah hitungan biaya secara nyata:

- **Satu langganan, dua pemakaian.** Kamu nggak lagi bayar Plus *plus* API usage terpisah untuk beban kerja agent.
- **Visibilitas lebih baik.** Dulu pemakaian di agent tercampur di tagihan API. Sekarang ada per-app usage di Settings > Usage.
- **Risiko terkendali.** Limit mingguan per aplikasi = pengaman kalau agent-mu ngamuk dan bikin loop. Ini penting banget untuk agent yang jalan otomatis tanpa pengawasan.
- **Kunci API lebih sedikit beredar.** Tidak ada API key yang perlu di-*paste* ke `env`, tidak ada key yang bocor di `.env` server. Kredensial dikelola sebagai koneksi OAuth yang bisa dicabut.

Tapi jangan salah paham: **ini bukan pengganti API key.** Untuk CI/CD, job otomatis yang tidak interaktif, atau lingkungan publik, API key tetap jalur yang direkomendasikan. Sign in with ChatGPT dirancang untuk pemakaian desktop/lokal yang kamu kontrol sendiri.

## ⚠️ Yang Perlu Diwaspadai

- **Bukan otomatis.** Kamu harus **memilih** mengizinkan pemakaian kuota saat login. Kalau terlewat, kamu cuma login — kuota tetap tidak kepakai.
- **Signing out ≠ disconnect.** Logout dari aplikasi hanya mengakhiri sesi di sana; koneksi ke ChatGPT tetap hidup sampai kamu memutusnya dari *Settings > Security and login*.
- **Credit use itu opt-in terpisah** dan default-nya **mati**. Kalau kamu nyalakan, dan auto-purchase credit juga aktif **di luar** setting ini, pemakaian bisa berlanjut dan kena charge otomatis. Baca baik-baik sebelum dinyalakan.
- **Reset limit tidak dipercepat** dengan login ulang. Login berulang tidak mengembalikan kuota.

## 🎯 Kesimpulan

Sign in with ChatGPT adalah langkah pragmatis dari OpenAI: mengakui bahwa langganan ChatGPT adalah **identitas sekaligus entitlement**, bukan cuma tiket masuk ke satu aplikasi chat. Untuk ekosistem open-source, kehadiran OpenClaw di daftar mitra resmi adalah sinyal jelas — agent open-source bukan lagi warga kelas dua.

Kalau kamu menjalankan OpenClaw atau Hermes Agent dan punya langganan Plus/Pro, cek dua hal hari ini: (1) apakah akunmu sudah ter-link dengan pemakaian kuota aktif, dan (2) berapa limit mingguan yang sudah kamu set. Dua menit di Settings > Usage bisa menghemat tagihan API yang tidak perlu.

Punya pengalaman memakai langganan ChatGPT di agent AI? Ceritakan di komentar — kami penasaran seberapa jauh penghematannya di dunia nyata.

— Chokdi 🐷 · Content Studio · 2026
