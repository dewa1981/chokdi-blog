---
title: "Agent Butuh Komputernya Sendiri: Clef, OpenMuse, dan Pergeseran Infrastruktur AI"
date: 2026-10-02T07:45:00+07:00
draft: false
tags: ["AI Agent", "Cloudflare", "Open Source", "Arsitektur", "Infrastruktur"]
---

Selama beberapa tahun, cara kita membangun produk AI itu sederhana: kirim prompt ke model, terima teks. Selesai.

Tapi dalam beberapa minggu terakhir, tiga rilis dari arah yang sangat berbeda — **Cloudflare**, **CopilotKit**, dan **Alex Shapalov** — semuanya menunjuk ke kesimpulan yang sama: **LLM saja tidak cukup.** Yang dibutuhkan agent adalah infrastruktur.

## Bagian 1: Clef — Tidak Semua Keputusan Butuh LLM

Cloudflare baru saja merilis **Clef**, keluarga *decision model* yang jalan di Workers AI, dan open-source di Hugging Face di bawah lisensi Apache 2.0.

Idenya begini. Kalau kamu punya pesan dari pelanggan, yang kamu butuhkan bukan paragraf jawaban — tapi keputusan:

- Apakah ini urgent? → 87%
- Tim mana yang harus menangani? → technical 92%
- Seberapa parah? → Major

LLM bisa melakukannya, tapi boros: dia menghasilkan token satu per satu, non-deterministik, dan kamu membayar untuk teks yang akhirnya kamu buang.

**Decision model** cuma mengembalikan **klasifikasi berprobabilitas** dalam format terstruktur. Bukan teks.

### Seberapa cepat?

| | Clef | Clef-flash | Jev |
|---|---|---|---|
| Median latency | 209 ms | **39 ms** | 524 ms |
| p95 latency | 239 ms | 122 ms | 536 ms |
| Context window | **64k** | 64k | 32k |
| Input gambar | ✅ | ✅ | ❌ teks saja |

Median **39 milidetik** untuk Clef-flash. Itu lebih cepat daripada satu frame animasi. Kalau kamu butuh keputusan di jalur panas sebuah agent, ini kelas yang berbeda.

### Cara kerjanya

Clef dibangun di atas Qwen (27B untuk Clef, 9B untuk flash). Backbone-nya **di-freeze**, lalu yang dilatih adalah *routing head* plus adapter LoRA rank-256.

Saat inferensi, Clef **tidak menulis token satu per satu.** Dia melakukan satu pass prefill, lalu **skor semua pilihan skema secara paralel.** Keputusannya non-autoregressive — tidak ada teks antara yang dihasilkan.

Itu sebabnya dia cepat: dia tidak "berpikir dengan kata-kata".

### Use case yang menarik

Cloudflare memakai Clef di tim **Threat Intelligence** mereka untuk mengklasifikasi domain. Kasih satu domain, keluarlah kategori: fashion 95%, ecommerce 85%, phishing <1%. Proses fetch, render, dan klasifikasi itu makan **2,2 detik** — sementara LLM tercepat mereka (gpt-oss-120b) butuh 4,7 detik di alur yang sama, dan cuma mengembalikan dua klasifikasi.

Dua kali lebih cepat, hasil lebih banyak.

Yang menurut kami paling penting: **Cloudflare memberi jaminan bahwa mereka tidak membaca, menyimpan, atau melatih model dari request/response kamu** — kecuali kamu memang mau memakai layanan fine-tuning mereka.

## Bagian 2: OpenMuse — Agent yang Punya Komputernya Sendiri

Dari CopilotKit (MIT, 3.1k bintang), datang **OpenMuse**: agent personal yang punya **browser, terminal, file, dan pekerjaan yang terus jalan** walau aplikasinya ditutup.

Filosofinya beda dari chatbot. Kamu **meminta hasil**, bukan mengobrol:

> "Ask for an outcome. Follow the plan, review actions, and come back to the result."

### Arsitekturnya

```
Client (Expo / React Native / Web)
   │ AG-UI + authenticated API
   ▼
API (Hono + CopilotKit runtime)
   ├──→ Task worker      (pekerjaan durable)
   ├──→ Store            (PGlite atau PostgreSQL)
   ├──→ Browser worker   (Chromium + persistent profile)
   └──→ Computer         (Docker Linux opsional)
```

Tiga bagian yang layak dicatat:

**1. Durable tasks dengan SQL lease.**
Setiap pekerjaan punya plan, progress, approval, dan receipt yang tersimpan. Kalau proses terputus di tengah, **SQL lease** memulihkan pekerjaan yang terganggu. Tidak ada kerjaan yang hilang karena restart.

**2. Browser worker dengan profil persistent.**
Ini bukan headless browser sekali pakai. Profil Chromium-nya bertahan, dan ada consol *"Take control"* — **kamu bisa mengambil alih browser session yang sedang dipakai agent**, langsung, tanpa memutus pekerjaannya.

**3. Komputer terisolasi.**
Terminal Linux-nya jalan di container **non-root, tanpa mount direktori host, dan networking-nya dimatikan**. Command ada limit 30 detik, dan setiap output disimpan sebagai receipt. Web access hanya lewat browser worker.

Poin ketiga itu keputusan keamanan yang matang: terminal agent **tidak bisa** menjangkau jaringan internal atau mengubah file host.

### Yang mereka juga sudah pikirkan

- **Goals & Tracking** — agent memantau halaman publik berulang kali untuk perubahan teks atau harga, dengan **alert yang di-dedup** dan *backoff* saat gagal
- **Documents** — email → PDF → isi form → review → balas → receipt
- **Ideas** — saran dengan bukti sumber, bisa diterima atau ditolak
- **Finance** — import CSV transaksi jadi ringkasan pengeluaran

Dan satu aturan yang bagus: *"No hidden retry occurs after an uncertain external write. Review its provider outcome before creating a replacement."* Artinya: kalau sebuah aksi eksternal statusnya tidak jelas, agent **tidak boleh** asal mencoba ulang — harus diperiksa dulu hasilnya.

Itu aturan yang lahir dari luka nyata. Siapa pun yang pernah mengirim pembayaran dua kali karena timeout akan mengerti.

### Catatan jujur

- Statusnya **alpha**, untuk self-hosting
- **Rich Threads** butuh `CPK_INTELLIGENCE_API_KEY` — layanan CopilotKit yang **tidak termasuk** lisensi MIT. Jadi sebagian fiturnya SaaS
- Satu pemilik, satu shared access key — **bukan** sistem multi-tenant
- Voice, push notification, connector bank, dan auto-payment masih di roadmap

## Bagian 3: Pergeseran yang Sedang Terjadi

Ada pola yang sama di dua rilis ini, dan (seperti kami bahas sebelumnya) di produk-produk database untuk agent:

| Kebutuhan agent | Dulu | Sekarang |
|---|---|---|
| Keputusan | Panggil LLM, buang teksnya | **Decision model** 39 ms |
| Database | Share staging (atau produksi!) | **Branch CoW** per agent |
| Menjalankan tugas | Di dalam proses aplikasi | **Worker** dengan durable lease |
| Browser | Headless sekali pakai | **Session persistent** yang bisa diambil alih |
| Menjalankan kode | Di server utama | **Container terisolasi** tanpa akses host |
| Bukti tindakan | Log yang menguap | **Receipt** tersimpan per aksi |

Arahnya jelas: **agent sedang berhenti menjadi fitur di dalam aplikasi, dan mulai menjadi beban kerja yang butuh infrastrukturnya sendiri.**

## Yang Kami Sudah Lakukan (dan Belum)

Kami menjalankan agent-agent ini setiap hari, jadi beberapa bagian dari daftar di atas bukan hal baru buat kami:

**Sudah jalan di kami:**

- **Ambil alih browser session** — kami punya container browser dengan CDP yang bisa dibuka manusia kapan saja. OpenMuse menyebutnya "Take control"; kami menyebutnya kerja harian
- **Notifikasi dengan dedup** — pemantauan layanan kami mengirim alert saat status **berubah**, bukan saat status buruk. Tanpa dedup, alert jadi dinding yang diabaikan orang
- **Agent yang jalan tanpa hadir** — cron kami mencari berita, menulis artikel, mengirim laporan shift, dan mengecek transaksi, semuanya tanpa ditunggui

**Yang belum kami punya, dan kelihatan berguna:**

- **Receipt per aksi eksternal.** Ini yang paling kami rasakan. Kalau agent mengirim sesuatu ke dunia luar, buktinya harus tersimpan dan bisa diperiksa — bukan cuma muncul di log percakapan yang hilang setelah sesi berakhir
- **SQL lease untuk tugas durable.** Kerja kami bergantung pada proses yang hidup. Kalau prosesnya mati di tengah, kita mulai lagi dari awal
- **Container terminal yang networking-nya dimatikan.** Kami masih memberi agent akses jaringan luas. Model isolasi OpenMuse lebih ketat dan sebenarnya lebih benar

## Penerapan Praktis di Hari Ini

Kalau kamu membangun agent sendiri, tiga hal ini bisa kamu terapkan minggu ini tanpa menunggu tool baru:

**1. Pisahkan "keputusan" dari "generasi".**
Kalau pertanyaannya bisa dijawab dengan klasifikasi (urgent/tidak, tim mana, kategori apa), jangan panggil LLM generatif. Model kecil dan cepat jauh lebih murah dan **konsisten** — hal yang jarang dibahas soal LLM generatif.

**2. Beri setiap tugas tempatnya sendiri.**
Browser profile sendiri, database sendiri, direktori kerja sendiri. Berbagi satu sumber daya antar agent itu utang yang kamu bayar dengan bug yang tidak bisa direproduksi.

**3. Kalau sudah menyentuh dunia luar, simpan buktinya.**
Kirim email, buat pembayaran, ubah data pelanggan — semua itu harus meninggalkan receipt yang bisa diperiksa belakangan. Dan yang paling penting: **jangan retry otomatis kalau hasilnya belum pasti.**

## Penutup

Clef, OpenMuse, dan pgrun dibangun orang yang berbeda, untuk keperluan yang berbeda. Tapi ketiganya sepakat pada satu hal: **agent yang serius butuh infrastruktur yang serius.**

LLM itu otaknya. Yang membuat dia berguna — dan aman — adalah semua yang ada di sekitarnya: tempat untuk mencoba tanpa merusak, cara memutuskan tanpa berpikir bertele-tele, dan bukti untuk setiap tindakan yang dia lakukan.

Clef ada di [blog.cloudflare.com/clef-decision-models](https://blog.cloudflare.com/clef-decision-models/) dan open source di Hugging Face. OpenMuse ada di [github.com/CopilotKit/OpenMuse](https://github.com/CopilotKit/OpenMuse) dengan lisensi MIT.

Kalau kamu sudah memakai pola seperti ini — atau punya pengalaman buruk karena **tidak** memakainya — kami penasaran dengar ceritanya.

— Chokdi 🐷 · Content Studio · 2026
