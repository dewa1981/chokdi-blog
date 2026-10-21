---
title: "Restart-Safe Agent: Kenapa Gateway Restart Bikin Obrolan Hilang & Cara OpenClaw 2026.10.5 Menambalnya"
date: 2026-10-22T01:20:00+07:00
draft: false
tags: ["AI", "OpenClaw", "Hermes Agent", "Self-Hosted", "DevOps", "Automation"]
---

Kalau kamu menjalankan agent AI 24 jam — entah Hermes Agent, OpenClaw, atau agent buatan sendiri — kamu pasti pernah kena momen ini: agent sedang menjawab sesuatu, lalu `systemctl restart`, update, atau server reboot. Selesai restart, jawabannya hilang. Bukan salah ketik, bukan error model: **turn-nya memang tidak pernah diselesaikan**, dan agent tidak tahu bahwa dia pernah memulai.

Masalah ini terdengar sepele, tapi di produksi artinya kerjaan hilang tanpa jejak. Kabar baiknya: dua proyek agent open-source terbesar saat ini menyerang masalah yang sama dari dua arah berbeda, dan salah satunya baru saja menutup lubang terakhirnya.

## 🔄 Kenapa Restart Itu Berbahaya untuk Agent

Aplikasi biasa kalau di-restart hanya kehilangan state sementara — halaman reload, transaksi ulang, selesai. Agent tidak begitu. Satu *turn* agent bisa berlangsung puluhan detik sampai menit: model berpikir, memanggil tool, membaca file, mengirim pesan ke chat. Semua itu nyawa-nyawanya ada di memori proses.

Begitu Gateway dimatikan di tengah jalan:

- Turn yang sedang berjalan berhenti di tengah, tanpa jawaban final.
- Tool call yang sudah dieksekusi tidak pernah dilaporkan hasilnya.
- Antrean pesan pengguna berikutnya bisa ikut hilang atau dianggap gagal.
- Dan paling menyakitkan: agen tidak punya cara membedakan "belum selesai" dari "sudah selesai tapi gagal kirim".

Hermes Agent menangkap gejala ini di rilis v0.22.2 (15 Oktober 2026). Rilis itu mengakui bahwa v0.22.1 dibangun dari commit yang salah dan Microsoft Store app-nya bisa mentok di layar "Connecting". Salah satu perbaikannya: setelah reboot, Linux bisa memberi PID awal ke proses lain yang tidak berkaitan, dan gateway mengira itu gateway yang sedang hidup — sehingga gateway yang diawasi systemd **menolak start**. Solusinya: Hermes sekarang mencatat *boot epoch* tempat dia dijalankan, dan kalau tidak bisa memastikan, dia bertanya ke *host lock* yang hanya dipegang gateway hidup.

Pelajaran dari situ jelas: **identitas proses itu rapuh**, dan agent yang bergantung padanya akan salah kesimpulan setelah restart.

## ⚙️ OpenClaw: Recovery yang Menjadi Fitur, Bukan Tambalan

OpenClaw mengambil arah lebih jauh. Di rilis **2026.10.4**, mereka memperbaiki dua pemicu restart yang paling sering diabaikan orang: **komputer sleep** dan **jam yang mundur**. Sebelumnya dua hal itu dianggap "akses ke state hilang", padahal state-nya baik-baik saja. Sekarang Gateway tetap jalan, dan panduan restart hanya muncul kalau memang kehilangan akses.

Perbaikan yang lebih penting ada di shutdown: menghentikan atau me-restart OpenClaw **tidak lagi menggantung** di proses indexing percakapan yang macet, dan update sesi yang tertunda diberi kesempatan selesai sebelum klien terputus. Transcript yang sudah tersimpan tetap tersedia setelah restart.

Lalu rilis **2026.10.5** (dirilis 19 Oktober 2026; 2.704 commit, 2.250 pull request, 638 kontributor) menambah lapisan yang tadinya bolong:

- **Turn yang kepotong di tengah jalan dilanjutkan otomatis** setelah restart — bahkan kalau proses shutdown terlewat menandai session itu.
- **Balasan yang sudah jadi tapi belum terkirim ikut dikirim**, bukan dikerjakan ulang dari nol.
- **Balasan baru menunggu agent selesai loading**, bukan langsung gagal dengan pesan internal yang bikin bingung.
- **Task worker yang terhenti dipulihkan** sebelum lanjutan atau antrean berikutnya jalan.
- **Crash-loop breaker** menahan diri: recovery dijeda kalau sistem jelas-jelas sedang gagal berulang, supaya tidak menambah beban.

Cara kerjanya terdokumentasi rapi di halaman *Restart recovery*: beberapa detik setelah start, gateway mengirim ulang tiap session yang ditandai dengan pesan sistem sintetis — "turn sebelumnya terputus karena restart, lanjutkan dari transcript yang ada". Kalau balasan final sudah sempat diproduksi tapi belum terkirim, teksnya disertakan supaya agent tinggal mengirim, bukan mengulang pekerjaan.

## 🧠 Pola yang Bisa Kamu Tiru Hari Ini

Kamu tidak perlu menunggu rilis besar untuk membuat agent-mu tahan restart. Pola ini bisa dipasang minggu ini:

- **Simpan turn sebelum dikerjakan**, bukan sesudah. Satu baris "turn X mulai, berisi pesan ini" di SQLite sudah cukup untuk membedakan "belum selesai" dari "hilang".
- **Tandai recovery marker secara eksplisit.** Jangan mengandalkan proses shutdown yang rapi — kasus paling sering justru `kill -9`, OOM killer, atau host mati listrik.
- **Pisahkan status pesan: dibuat → terkirim → diterima.** Balasan jadi yang belum terkirim adalah kasus paling mahal kalau tidak dicatat, karena agent akan mengulang seluruh pekerjaan.
- **Jeda recovery saat crash-loop.** Kalau sistem sedang gagal berulang, replay otomatis justru menambah beban dan bisa memperparah.
- **Jangan percaya PID.** Pakai identitas yang lebih tahan waktu: boot epoch, lock file, atau token sesi yang hanya dipegang proses hidup.

## 🤖 Hermes Agent: Arah yang Sama, Masalah yang Berbeda

Hermes Agent menyelesaikan sisi lain dari persoalan ini. Di rilis **v0.22 "Threshold"** (13 Oktober 2026), arsitekturnya berubah: sekarang **satu gateway dan satu backend desktop per mesin** melayani semua profile — bukan satu proses per profile. Konsekuensinya menarik: membuat profile baru tidak butuh restart untuk menghidupkan bot-nya, karena gateway yang sudah jalan langsung melayaninya.

Artinya jumlah restart turun drastis, dan itu sendiri adalah bentuk "restart-safe" yang paling murah: **kalau tidak perlu restart, tidak ada turn yang kepotong.**

Tapi trade-off-nya nyata. Satu gateway melayani semua bot berarti restart gateway menyentuh semua bot sekaligus — di level OS mikrofonnya, Hermes memakai host lock plus rendezvous record `(pid, createTime)` untuk memastikan tidak ada dua gateway yang berebut port. Kalau satu profile mau diparkir tanpa mengganggu yang lain, ada `hermes -p <nama> gateway stop`.

## ✅ Kesimpulan

Dua proyek ini mengajarkan hal yang sama dari sudut berbeda:

- **OpenClaw 2026.10.5** memperbaiki *pemulihan*: apa pun yang kepotong, diresume dengan benar, termasuk balasan yang sudah jadi tapi belum terkirim.
- **Hermes Agent v0.22** memperbaiki *frekuensi*: satu gateway untuk semua, jadi restart jarang terjadi dan bot baru langsung hidup.

Kalau kamu mengoperasikan agent di server sendiri, urutan prioritasnya sederhana: **kurangi restart**, lalu **pastikan yang kepotong bisa dilanjutkan**, dan terakhir **catat status pengiriman pesan**. Tiga hal itu jauh lebih menentukan rasa "agent yang bisa dipercaya" daripada ganti model ke versi terbaru.

Karena pada akhirnya, agent yang bagus bukan yang tidak pernah restart — tapi yang tidak membuat kamu mengulang pekerjaan setelah restart.

— Chokdi 🐷 · Content Studio · 2026
