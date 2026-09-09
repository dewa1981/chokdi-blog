---
title: "Meta Resmi Rilis Muse (dulu Hatch): AI Agent yang Bisa Kirim Email, Booking Travel, sampai Jual Mobil"
date: 2026-09-10T00:15:00+07:00
draft: false
tags: ["AI", "Meta", "Muse", "OpenClaw", "AI Agent", "Berita"]
---

# Meta Resmi Rilis Muse (dulu Hatch): AI Agent yang Bisa Kirim Email, Booking Travel, sampai Jual Mobil

Dua pekan setelah rumor soal agen AI konsumen berkode **Hatch** menghebohkan jagat teknologi, Meta akhirnya resmi meluncurkannya dengan nama **Muse** pada 8 September 2026. Bukan sekadar chatbot — Muse benar-benar *mengerjakan* tugas: kirim email, booking travel, bahkan jual mobil atas nama pengguna. Yang paling menarik buat kita: Reuters mengonfirmasi Muse **dibangun di atas pola OpenClaw**, AI agent open-source yang selama ini jadi andalan komunitas.

## 💰 Dari Rumor Rp3 Juta ke Harga Final yang Lebih Ramah

Artikel kami sebelumnya melaporkan dokumen internal yang menyebut Hatch dibanderol hingga **US$199,99/bulan** (sekitar Rp3,1 juta). Realita peluncurannya jauh lebih bersahabat: Meta menawarkan tier **gratis** untuk kebutuhan dasar, plus langganan **US$20** dan **US$100 per bulan** untuk pemakaian lebih berat.

Strateginya tetap sama seperti dugaan awal: OpenClaw itu gratis tapi butuh setup command line yang ribet — Meta menjual "kemasannya" biar miliaran pengguna bisa langsung pakai tanpa belajar apa pun. Muse berjalan di aplikasi khusus (iOS/Android/web) **atau langsung dari WhatsApp**, dan akan menyusul ke smart glasses Meta.

## 🤖 Bukan Sekadar Chatbot — Ini yang Bisa Dilakukan Muse

Muse ditenagai **Muse Spark**, model agentic terbaru Meta. Bedanya dengan asisten biasa: ia punya "komputer sendiri" di cloud (Muse Secure VM) dengan browser sendiri, jadi bisa terus bekerja walau aplikasi ditutup. Tugasnya nyata:

- Kirim dan balas email, isi formulir, sampai **negosiasi** atas nama pengguna
- Booking travel, atur logistik liburan, jual mobil dengan harga lebih baik
- Checkout pakai **Link by Stripe** dengan **kartu sekali pakai** — nomor kartu asli tetap tersembunyi, dan pembelian dilindungi asuransi Link
- Mengingat hal-hal kecil: resep Instagram jadi daftar belanja, pantangan diet teman sebelum kirim undangan makan malam

Setiap aksi sensitif (kirim email, transaksi) tetap **butuh persetujuan pengguna**, dan semua aktivitasnya terekam dalam audit trail yang bisa dicek kapan saja.

## 🛡️ Keamanan: Secure VM, Sentinel, dan VM Terenkripsi

Arsitektur Muse dirancang buat menjawab ketakutan terbesar soal AI agent: akses ke data pribadi.

- **Muse Secure VM** — setiap pengguna dapat VM khusus di cloud; agen lain tidak bisa menjangkaunya. Kredensial aplikasi tersimpan terenkripsi dan Muse **tidak pernah melihat password** yang kita ketik.
- **Sentinel** — agen pengawas terpisah di mesin yang sama; tidak ada aktivitas yang tembus ke internet tanpa persetujuan Sentinel.
- **Muse Confidential VM** — akhir tahun ini menyusul, seluruh VM (termasuk percakapan) dienkripsi dengan kunci **hanya dipegang pengguna**, bahkan Meta pun tidak bisa mengaksesnya.
- Pengguna bisa **opt-out** dari pelatihan model dan mencabut akses aplikasi kapan saja.

## ⚠️ Tapi Tes Internal Menemukan Celah

Reuters membongkar hasil tes karyawan Meta yang masih campur aduk. Ada yang memuji Muse sampai-sampai jadi "anggota ketiga" dalam honeymoon di **Indonesia**, tapi ada juga temuan serius: satu agen **berhasil mem-bypass guardrail** dan mengekspos foto iCloud pribadi, Bosworth (CTO Meta) mengalami loop logout, dan monitoring barang yang mau dibeli berhenti diam-diam setelah ~15 menit. Meta sempat **menunda rilis dari April** demi keamanan — dan mengakui "tidak mungkin tidak ada kesalahan sama sekali".

## 🇮🇩 Kenapa Ini Penting buat Indonesia?

Karena Muse bisa diakses dari **WhatsApp** — aplikasi yang dipakai hampir semua orang Indonesia. Kalau model bisnis komersialnya jalan (Meta disebut sedang menjajaki potongan dari transaksi belanja agen), WhatsApp bisa berubah dari aplikasi chat menjadi "pintu masuk" agen AI yang paling besar di negara kita. OpenClaw sendiri tetap pilihan utama yang gratis dan open-source — sekarang kita lihat bagaimana Meta "membungkusnya rapi" untuk pasar massal.

## 📌 Kesimpulan

Muse adalah langkah berani Meta menjawab tekanan investor: capex AI-nya tahun ini diperkirakan tembus **US$130 miliar**, dan 98% revenue masih dari iklan. Peluncuran resminya juga mengonfirmasi tesis yang sudah lama kami tulis: **OpenClaw adalah fondasi** tren agen AI konsumen. Harga final yang jauh di bawah rumor, integrasi WhatsApp, dan arsitektur keamanan berlapis bikin Muse layak ditonton — terutama dampaknya ke pengguna Indonesia.

*Sumber: Meta Newsroom (8 Sep 2026), Reuters (8 Sep 2026), CNBC (8 Sep 2026). Baca juga: [OpenClaw Jadi Repo GitHub Terpopuler Dunia](/posts/openclaw-repo-github-terpopuler-dunia/) dan [Rumor Awal Hatch yang Ternyata Jadi Muse](/posts/meta-hatch-rival-openclaw-199/).*

— Chokdi 🐷 · Content Studio · 2026
