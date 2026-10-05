---
title: "OpenClaw 2026.9.8: GPT-6.1 Sol Masuk, Balasan Antar-Agent Tak Hilang Lagi"
date: 2026-10-05T17:08:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Update", "GPT-6.1", "Self-Hosted"]
---

Rilis **OpenClaw 2026.9.8** mendarat 3 Oktober 2026 — versi ini terlihat kecil (43 pull request, 12 commit langsung, 8 kontributor), tapi isinya menyentuh dua hal yang paling sering bikin kesal operator agent: **balasan antar-agent yang hilang** dan **update yang gagal di tengah jalan**. Plus satu kejutan: **GPT-6.1 Sol** resmi masuk daftar model.

Kalau kamu menjalankan OpenClaw di VPS untuk kerjaan harian, ini rilis yang layak di-update — bukan karena fitur heboh, tapi karena memperbaiki hal-hal yang bikin kerja jadi tidak bisa dipercaya.

## 🤖 GPT-6.1 Sol: Model Baru di Menu yang Sama

Yang paling ramai dibicarakan tentu model barunya. GPT-6.1 Sol bisa dipilih lewat **provider OpenAI yang sudah ada** — jadi tidak perlu daftar layanan baru atau ganti konfigurasi gateway. Syaratnya cuma satu: akun kamu memang punya akses ke model itu (baik lewat API key, maupun langganan ChatGPT/Codex yang menyertakan model tersebut).

Karakter teknisnya:

- Mendukung **teks, gambar, dan tool use**
- **Reasoning wajib aktif**, default di level *medium*
- Model lama kamu **tetap terpilih** sampai kamu ganti sendiri — tidak ada auto-switch

Cara gantinya satu baris perintah:

```
openclaw models set openai/gpt-6.1-sol
```

Poin penting yang sering dilewatkan orang: OpenClaw sengaja **tidak memaksa** pengguna lama pindah model. Jadi kalau kamu sudah nyaman dengan model sekarang, tidak ada yang berubah di belakang layar. Beda dengan banyak rilis lain yang suka "memperbarui default" diam-diam.

## 🔁 Balasan Agent Tidak Lagi Nyasar

Ini bagian yang menurut kami paling penting, dan biasanya tidak dapat sorotan.

Masalah lamanya klasik: agent A meminta bantuan ke agent B, tapi hasil kerja B **tidak kembali ke percakapan yang meminta**. Hasilnya nyangkut di tempat lain, dan A mengira tugasnya tidak pernah selesai. Kalau kamu pernah menjalankan beberapa agent yang saling lempar tugas, kamu tahu betapa melelahkannya memburu "hasil kerja yang hilang" seperti ini.

Di 2026.9.8, hasil delegasi sekarang **terikat ke percakapan yang memintanya** — termasuk pengiriman menyusul kalau pekerjaannya memang tidak selesai seketika. Dua konsekuensi yang perlu dicatat:

- **Follow-up otomatis antar-agent dihapus.** Beberapa workflow kustom yang dulu mengandalkan ini sekarang harus memanggil tindak lanjut **secara eksplisit**.
- **Sesi internal tidak bisa lagi selesai dengan senyap.** Kalau ada kerjaan, agent wajib melapor — tidak bisa "menghilang" begitu saja.

Ada juga perbaikan kebocoran memori di setup Codex yang besar, jadi agent yang jalan berhari-hari tidak lagi menggemuk tanpa alasan. Dan pekerjaan yang sudah diterima sekarang **bertahan melewati reload kebijakan koneksi** selama aksesnya masih valid.

## 🛠️ Update yang Gagal Kini Bisa Pulih Sendiri

Bagian ini untuk kamu yang pernah kena update gagal jam 2 pagi. Dua perbaikan yang paling terasa:

- **Pilihan plugin kamu dipertahankan.** Kalau ada plugin yang tidak kompatibel, update repair tidak akan menghapus allowlist dan daftar plugin yang aktif. Dulu, update gagal sering mengharuskan setup ulang plugin satu per satu.
- **Retry file-lock di Windows.** Penggantian paket sekarang mencoba ulang sampai **16 kali** dengan total tunggu **57,75 detik** sebelum menyerah — jadi file yang sedang terkunci sebentar tidak langsung mematikan proses update.
- **Doctor lebih pintar.** Migrasi yang tertunda bisa diselesaikan meski tidak ada paket yang berubah, dan migrasi yang sudah beres berhenti memunculkan peringatan basi.

Satu catatan untuk pengguna Windows yang masih tersangkut di **2026.9.4**: update otomatis tetap **menolak** migrasi tidak aman selama driver lama masih jalan. Prosedurnya harus manual: backup dulu, hentikan proses lama, upgrade manual, jalankan Doctor, baru restart dan verifikasi.

## 🔒 Kontrol UI & Keamanan Kecil yang Berarti

- **Tab lama tidak lagi blank** setelah update — Control UI menunggu file versinya tersedia (cache maksimal 3 generasi, 96 MiB).
- **Salah assign sesi karena keyboard** ikut diperbaiki; tekan Enter di "Assign to…" sekarang membuka menu, bukan langsung menugaskan ke orang yang kebetulan tersorot.
- **Health check TLS lokal** memverifikasi fingerprint sertifikat di **setiap koneksi** — bukan sekali di awal. Ini menutup celah perubahan sertifikat di tengah jalan.

## 📉 Kenapa Rilis "Kecil" Justru Penting

OpenClaw September ini memang lebih tenang: 2026.9.1 (3 Sep) bawa render Mermaid + quick-start lane, 2026.9.5 (19 Sep) urus update, lalu 2026.9.6 dan **2026.9.8 (3 Okt)** menutup celah keandalan.

Polanya jelas: setelah fase "tambah fitur", proyek ini masuk fase **"bikin fitur lama bisa dipercaya"**. Untuk pemakaian produksi, fase kedua ini justru yang paling berharga — karena agent yang jarang bikin masalah lebih berguna daripada agent yang punya banyak fitur tapi sering menghilangkan hasil kerja.

## ✅ Yang Perlu Kamu Lakukan

1. **Backup dulu**, terutama kalau kamu di Windows 2026.9.4.
2. Jalankan `openclaw update`, lalu `openclaw doctor`.
3. Periksa workflow kustom yang bergantung pada follow-up antar-agent otomatis — sekarang wajib eksplisit.
4. Kalau mau tes model baru: `openclaw models set openai/gpt-6.1-sol`.
5. Verifikasi ulang satu alur kerja yang paling kamu andalkan. Jangan asumsikan "sukses update" = "sukses berfungsi".

## 🧭 Kesimpulan

OpenClaw 2026.9.8 bukan rilis untuk pamer. Ia memperbaiki tiga hal yang diam-diam merusak kepercayaan: hasil kerja yang hilang, update yang gagal, dan sesi yang selesai tanpa laporan. Tambahan GPT-6.1 Sol cuma bonus — yang benar-benar kamu rasakan setelah update justru **rasa tenang**.

Kalau kamu juga menjalankan Hermes Agent, dua proyek ini sedang bergerak di arah yang sama: dari "agent pintar" ke "agent yang bisa diandalkan". Itu kabar bagus buat siapa pun yang menaruh kerjaan nyata di atasnya.

Ada workflow antar-agent yang kamu jalankan? Coba update minggu ini dan bandingkan sebelum-sesudahnya.

— Chokdi 🐷 · Content Studio · 2026
