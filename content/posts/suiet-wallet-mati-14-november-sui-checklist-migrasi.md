---
title: "Suiet Mati 14 November: Koin SUI Kamu Tidak Hilang, tapi Bisa Jadi Tidak Terlihat"
date: 2026-11-14T17:34:00+07:00
draft: false
tags: ["Crypto", "Sui", "Wallet", "Self-Custody", "Keamanan"]
---

Hari ini, **14 November 2026**, API Suiet berhenti. Suiet adalah dompet ekstensi browser self-custody untuk jaringan Sui. Timnya sudah menghentikan pengembangan dan perawatan, lalu menahan layanan API tetap hidup sampai tanggal ini supaya orang sempat memindahkan akunnya.

Yang perlu kamu tahu dulu, sebelum panik: **koin SUI kamu tidak hilang, tidak dibekukan, dan tidak dipindahkan.** Tidak ada yang berubah di blockchain. Yang mati adalah jendela untuk melihat dan memakai koin itu.

## 🕒 Apa yang Benar-Benar Mati Hari Ini

Suiet bergantung pada backend-nya sendiri untuk membaca rantai Sui. Begitu API-nya padam, tiga hal praktis ikut padam:

- **Saldo dan riwayat transaksi bisa gagal dimuat.** Ekstensi bisa menampilkan angka kosong atau data lama, padahal di rantai tidak ada yang berubah.
- **Kirim transaksi dan koneksi ke dApp bisa gagal.** Tanda tangan dan siaran transaksi lewat layanan yang sama.
- **Tidak ada aplikasi cadangan.** Suiet tidak pernah merilis aplikasi mobile, dan listing Chrome Web Store-nya sedang dicabut — jadi tidak ada klien Suiet kedua untuk pindah.

Pengumuman resmi akun Sui pada 11 November meminta pengguna **segera mencadangkan recovery phrase atau private key setiap akun**, dan tidak membagikannya ke siapa pun. Satu hal yang sering terlewat: kalau kamu punya beberapa akun di dalam satu ekstensi Suiet, **setiap akun punya frasa sendiri**. Mencadangkan satu akun tidak menyelamatkan akun lain.

## ⛓️ Dompet Hilang Bukan Koin Hilang

Analogi paling gampang: dompet fisik dan uang di dalamnya. Kalau dompet kulitmu rusak, uangnya tidak ikut musnah — kamu tinggal ambil uangnya dan taruh di dompet lain. Bedanya, di kripto "uang" itu benar-benar ada di rantai, dan "dompet" cuma alat untuk memegang kunci.

Karena itu, langkah pemulihannya sederhana secara konsep: **pulihkan alamat yang sama di dompet Sui lain** memakai frasa pemulihan yang sudah kamu cadangkan. Alamatnya tetap sama, isinya tetap sama. Yang berubah hanya aplikasi yang membukanya.

## ✅ Checklist Migrasi (Kerjakan Hari Ini)

1. **Buka Suiet sekarang** selama API-nya masih merespons, lalu buka menu pengaturan dan ekspor recovery phrase/private key tiap akun.
2. **Tulis di kertas, jangan difoto.** Screenshot frasa 12/24 kata adalah kebiasaan paling berbahaya — galeri foto ikut tersinkron ke cloud.
3. **Jangan pernah mengetik frasa itu ke halaman web mana pun**, termasuk yang tampilannya mirip situs resmi. Frasa hanya dimasukkan ke aplikasi dompet yang kamu pasang sendiri dari sumber resmi.
4. **Pasang dompet Sui lain** dari kanal resmi (situs proyek atau toko ekstensi resmi), lalu pilih "import wallet" dan masukkan frasa tadi.
5. **Cocokkan alamatnya.** Alamat baru harus **persis sama** dengan alamat lama di Suiet. Kalau beda, berarti frasanya salah atau beda akun — jangan lanjut, ulangi dari langkah 1.
6. **Uji dengan nominal kecil dulu**, kirim sedikit SUI ke alamat lain, baru anggap migrasi selesai. Setelah itu pertimbangkan memindahkan aset ke dompet yang timnya masih aktif.

## 🚨 Jebakan yang Paling Mahal: Portal Migrasi Palsu

Momen seperti ini adalah panen raya untuk penipu. Pola yang muncul: iklan "migrasi resmi Suiet" di mesin pencari, grup Telegram yang menawarkan "bantuan migrasi", atau situs yang meminta kamu menempelkan frasa pemulihan untuk "verifikasi".

Aturannya cuma satu dan tidak ada pengecualian: **tidak ada layanan migrasi yang sah yang butuh frasa pemulihanmu.** Migrasi dilakukan olehmu, di dompetmu sendiri, secara offline dari sisi server. Siapa pun yang meminta frasa itu adalah pencuri.

## 📉 Pola yang Lebih Besar dari Suiet

Suiet bukan yang pertama. Pada 10 November 2026 proyek dompet hardware Sui, **Suiball**, mengumumkan penutupan. Sebelumnya, **Phantom mengakhiri dukungan Sui pada September 2026**. Harga SUI sendiri sedang tertekan, di kisaran **US$ 0,77** saat artikel ini ditulis.

Yang penting dibedakan: itu semua adalah **tim produk yang pergi**, bukan jaringan Sui yang rusak. Rantai Sui tetap berjalan, dan aset on-chain tetap utuh. Tapi pelajarannya jelas — di ekosistem yang lebih kecil, dompet pihak ketiga bisa mati lebih cepat daripada jaringan yang mereka layani.

## 🧠 Pelajaran yang Bisa Dibawa ke Dompet Lain

Self-custody artinya kunci, bukan aplikasi. Selama kamu memegang frasa pemulihan, matinya satu dompet cuma gangguan sehari. Sebaliknya, kalau frasanya hilang atau cuma tersimpan sebagai screenshot di ponsel, dompet yang paling canggih pun tidak menolong.

Kebiasaan yang layak dipasang sekarang, bukan saat panik: cek frasa pemulihan setiap dompet yang kamu pakai, simpan di dua tempat fisik yang terpisah, dan anggap setiap dompet pihak ketiga punya tanggal kedaluwarsa.

**Baca juga:** [Harmony Matikan Blockchain-nya: Rantai Pertama yang Menyerah pada AI Agents, ONE Migrasi ke Ethereum](https://chokdi.ano99.com/posts/harmony-sunset-one-migrasi-ethereum/) · [Reorg 1 Blok Ethereum Bikin THORChain Setop Swap 10 Jaringan — 10 ETH Cukup Lumpuhkan Protokol](https://chokdi.ano99.com/posts/thorchain-setop-swap-reorg-10-eth/) · [Patch Sudah Ada Tapi Belum Dirilis: Pelajaran dari Hack US$319 Juta Liquid Network](https://chokdi.ano99.com/posts/patch-tertinggal-hack-liquid-network-319-juta/)

— Chokdi 🐷 · Content Studio · 2026
