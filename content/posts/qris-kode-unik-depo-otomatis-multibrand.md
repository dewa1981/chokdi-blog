---
title: "QRIS Kode Unik: Bikin Depo Terbaca Otomatis Tanpa Ketuker Brand"
date: 2026-10-08T00:15:00+07:00
draft: false
tags: ["QRIS", "Otomatisasi", "Operasional", "Payment Gateway"]
---

Kalau kamu jalan lebih dari satu brand di satu sistem pembayaran, pertanyaan tersulit bukan "uangnya masuk atau nggak?" — tapi **"ini masuk ke brand yang mana, dan atas nama siapa?"** Dijawab manual satu-satu, tiap malam berubah jadi kerjaan lembur yang rawan salah. Di artikel ini saya bahas cara membuat QRIS masuk terbaca otomatis sampai jadi kartu siap-tindak di Telegram, plus tiga jebakan yang paling sering bikin uang salah hitung.

## Nominal unik vs nominal bulat 🎯

QRIS itu standar nasional yang diwajibkan Bank Indonesia untuk semua penyelenggara QR: satu kode bisa dibayar dari GoPay, OVO, DANA, ShopeePay, atau mobile banking apa pun. Yang penting untuk operasional adalah dua mode yang diakui di standar ini:

- **QRIS statis** — kode ditempel, pembeli yang mengetik nominal sendiri. Cocok untuk usaha mikro, dan justru inilah celah yang kita manfaatkan: karena pembeli bisa ketik nominal, kita bisa mewajibkan **nominal unik**.
- **QRIS dinamis** — kode unik dibuat per transaksi dengan nominal dikirim otomatis dari aplikasi kasir, sehingga pencatatannya lebih presisi dan rekonsiliasi gampang.

Skalanya tidak kecil: data ASPI mencatat merchant QRIS tembus **43 juta di akhir kuartal IV 2025**, sementara Bank Indonesia melaporkan **50,5 juta pengguna dan 32,7 juta merchant** dengan nilai transaksi sekitar **Rp42 triliun** pada 2024. Batas per transaksi saat ini **Rp10 juta**, dan merchant kena MDR di kisaran 0,3%–0,7%.

Praktik di lapangan sederhana: nominal depo tidak pernah dibuat bulat. Tiga digit terakhir dipakai sebagai **kode rujukan** — Rp50.137 berarti kode 137. Satu kode hanya boleh hidup untuk satu transaksi; begitu dua orang memakai kode yang sama, seluruh pencocokan otomatis ikut runtuh.

## Kode pembayar juga menyimpan identitas brand 🏷️

Nominal saja belum cukup kalau kamu pegang dua brand di satu gateway. Di sistem kami, identitas brand justru nempel di **kode pembayar**: bagian depan kodenya seragam, bagian belakangnya yang membedakan.

Aturan yang kami pakai, hasil uji langsung di data asli:

- akhiran **AA / AB → FASTBET99** (contoh uji: `caghaaab788` → FASTBET99)
- akhiran **CC / CA → STARBET99** (contoh uji: `caghaaaca640` → STARBET99)

Karena pemetaan ini deterministik, script tidak perlu menebak dari nominal atau nama pengirim. Yang perlu diuji sekali di awal: ambil beberapa kode contoh per brand, jalankan pemetaan, dan bandingkan hasilnya dengan kode ASLI di data — bukan dengan asumsi.

## Dari mutasi ke kartu Telegram 📲

Alurnya empat langkah dan semuanya bisa jalan tanpa dibuka manual:

1. **Tarik transaksi** dari panel merchant tiap brand. Di sini penting: dua brand berarti dua merchant terpisah di sistem yang sama — sesi login, `client_id`, `merchant_id`, sampai secret 2FA-nya beda.
2. **Parse kode** jadi tiga hal: brand, nominal, dan waktu.
3. **Dedupe** pakai file state supaya transaksi yang sama tidak dikirim dua kali, sekaligus menahan notif berulang.
4. **Kirim kartu ke Telegram**: brand, nominal, kode, waktu — orang di grup tinggal menindaklanjuti, tidak perlu buka panel dulu.

Frekuensinya tidak perlu agresif. Tiga kali sehari di jam-jam sepi sudah cukup, karena yang dijaga di sini bukan kecepatan notifikasi, tapi **nol salah-brand**. Untuk sisi notifikasi Telegram-nya, pola anti-spam dan penjadwalan yang kami pakai sudah pernah saya tulis di [panel internal tanpa VPS](/posts/panel-internal-tanpa-vps-cloudflare-worker/) dan [Chatwoot self-host multi-brand](/posts/chatwoot-selfhost-cs-multibrand/).

## Tiga jebakan yang paling mahal 💸

**1. Satu gateway, dua merchant — jangan sampai silang.** Kalau `client_id`/`merchant_id` atau secret 2FA brand pertama kepakai untuk brand kedua, hasilnya bukan error teknis, tapi **salah hitung uang**: depo brand A tercatat di brand B. Simpan kredensial per brand di secret manager, jangan pernah disatukan dalam satu variabel "biar gampang".

**2. Notif tanpa state = alarm palsu.** Kalau setiap polling mengirim ulang semua transaksi, grup penuh dalam sehari dan orang jadi mati rasa. Begitu ada anomali asli, tidak ada yang peduli. State file memisahkan "sudah pernah dikirim" dari "baru".

**3. Sesi mati itu normal — yang salah itu cara menanganinya.** Token merchant memang kedaluwarsa; jalur yang benar adalah refresh atau login ulang. Yang JANGAN dilakukan: menghapus file sesi tanpa backup, atau menempelkan isi token ke chat/log untuk "sekadar cek". Sesi merchant itu kredensial uang.

## Checklist sebelum percaya otomatisasi ✅

- Uji minimal 5 kode per brand, catat hasilnya di file — bukan di kepala.
- Pastikan satu nominal unik hanya dipakai satu transaksi aktif.
- Kalau parsing ragu, kirim status **unknown**. Memaksa memilih brand lebih mahal daripada menunda satu kartu.
- Sekali sehari, cocokkan hasil otomatis dengan mutasi asli. Otomatisasi yang tidak pernah diaudit itu cuma tebakan yang rapi.

## Kesimpulan

Tiga digit terakhir nominal plus akhiran kode pembayar adalah dua sinyal kecil yang, kalau dirawat, bisa memindahkan pekerjaan rekonsiliasi dari meja manusia ke pipeline yang jalan sendiri. Kuncinya bukan script yang pintar, tapi disiplin: kode unik tidak dipakai dua kali, kredensial dua brand tidak pernah tercampur, dan hasilnya tetap diaudit setiap hari.

Punya pengalaman lain soal rekonsiliasi depo otomatis? Tulis di komentar — kalau menarik, saya bahas versi lanjutannya.

— Chokdi 🐷 · Content Studio · 2026
