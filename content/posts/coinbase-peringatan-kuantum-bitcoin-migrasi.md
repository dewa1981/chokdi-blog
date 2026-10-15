---
title: "Coinbase Peringatkan Ancaman Kuantum ke Bitcoin: Migrasi Butuh Bertahun-tahun, 5% Supply BTC Ada di Tangan Mereka"
date: 2026-10-15T17:10:00+07:00
draft: false
tags: ["Crypto", "Bitcoin", "Quantum", "Coinbase", "Keamanan"]
---

Coinbase baru saja menerbitkan roadmap teknis untuk menyiapkan Bitcoin menghadapi komputer kuantum — dan mereka jujur: prosesnya **butuh bertahun-tahun, bukan berbulan-bulan**. Buat kamu yang pegang BTC, ini bukan berita panik, tapi berita penting: masalahnya nyata, solusinya sudah mulai dirancang, dan yang paling menentukan justru hal-hal kecil yang bisa kamu cek sendiri hari ini.

## 🚨 Apa yang Sebenarnya Terjadi?

Pada 13 Oktober 2026, Coinbase mempublikasikan posisi teknis berjudul *"Working Together on Bitcoin's Post-Quantum Readiness"* lewat blog resmi mereka. Penulisnya Shashank Agrawal, dan yang bikin ini berbobot: Coinbase adalah salah satu kustodian kripto terbesar di dunia yang **memegang sekitar 5% dari seluruh Bitcoin yang ada** — termasuk di balik beberapa ETF Bitcoin spot AS.

Inti pesannya sederhana. Bitcoin sekarang diamankan oleh tanda tangan digital ECDSA dan Schnorr. Komputer kuantum yang cukup kuat — istilah teknisnya CRQC (*cryptographically relevant quantum computer*) — secara teori bisa menurunkan **kunci privat dari kunci publik** yang sudah terekspos. Kalau itu terjadi, dana di alamat tersebut bisa diambil orang lain.

Belum ada mesin seperti itu hari ini. Tapi menurut Coinbase, justru itulah saatnya mulai — karena perubahan aturan konsensus Bitcoin dan migrasi dompet butuh waktu lama.

## ⚠️ Risiko Sebenarnya Bukan "Semua Bitcoin"

Ini bagian yang sering salah dipahami. Tidak semua Bitcoin sama rentannya.

- **Alamat yang belum pernah dipakai** menyimpan kunci publik dalam bentuk hash. Komputer kuantum tidak diperkirakan mudah membalik hash ini — relatif aman.
- **Alamat yang sudah pernah spending** sudah membuka kunci publiknya ke blockchain. Ini yang jadi sasaran.
- **Alamat lama (P2PK) dan Taproot (P2TR, sejak 2021)** memperlihatkan kunci publik sejak awal.

Riset yang dirujuk media kripto menemukan sekitar **20.000 alamat Bitcoin** yang masing-masing menampung minimal 50 BTC dengan kunci publik sudah terbuka. Risiko ekstra muncul kalau alamat itu **dipakai berulang** — bukan sekali lalu kosong.

Artinya: kebiasaan lama "satu alamat buat selamanya" itu justru celah yang paling gampang ditutup, dan tidak perlu menunggu upgrade protokol apa pun.

## 🛠️ Apa yang Coinbase Usulkan?

Roadmap ini bukan instruksi, tapi masukan untuk diskusi terbuka. Ada tujuh poin utama, dan tiga yang paling praktis buat dipahami:

**1. Siapkan sebelum pasti.** Jangan tunggu pengumuman mesin kuantum muncul baru gerak. Perubahan Bitcoin itu lambat karena harus lewat konsensus developer, miner, dan pemegang node.

**2. Pisahkan "wadah" dari tanda tangan.** Pilih desain output type yang bisa mengganti atau menambah skema tanda tangan post-quantum **tanpa merombak seluruh sistem**. Coinbase menyebut dua kandidat: **P2MR (BIP-360)** dan **P2TRv2**.

**3. Perlindungan bertahap.** Dompet aktif bisa pakai konstruksi hybrid dulu. Salah satu desain transisi yang diusulkan: **1-of-2** — dana yang sama punya dua jalur pengeluaran, satu pakai kunci klasik (ECDSA/Schnorr), satu pakai kunci post-quantum.

Coinbase juga menyoroti hal teknis yang sering dilewatkan: skema tanda tangan *stateful* bisa lebih kecil dan cepat, tapi berisiko tinggi karena salah kelola state bisa berujung pemalsuan tanda tangan. Jadi opsinya harus tetap terbuka.

## 📦 Tantangan yang Belum Selesai

Jangan bayangkan ini bakal mulus. Tanda tangan post-quantum ukurannya **jauh lebih besar** dari yang sekarang. Bitcoin sengaja membatasi ruang blok — kalau tanda tangan membengkak, transaksi per blok berkurang dan **biaya transaksi bisa naik**.

Ada juga syarat yang tidak bisa ditawar: verifikasi harus tetap bisa dilakukan siapa saja dengan **full node** sendiri, tanpa bergantung pihak ketiga. Kalau solusinya terlalu berat, node kecil tersingkir dan desentralisasi Bitcoin melemah.

Belum lagi pertanyaan paling pelik: bagaimana dengan **koin yang sudah tidak bisa diakses** — kunci hilang, pemilik meninggal, atau alamat era Satoshi yang sudah bertahun-tahun diam? Coinbase ingin diskusi itu jalan berbarengan, jangan sampai menahan pekerjaan teknisnya.

Untuk konteks: Google menargetkan migrasi infrastruktur mereka ke kriptografi post-quantum sekitar **2029**, dan sejumlah estimasi menempatkan komputer kuantum yang relevan secara kriptografis di rentang **2029–2035**. Tidak mendesak besok, tapi juga tidak cukup waktu kalau nunggu sampai kejadian.

## ✅ Yang Bisa Kamu Lakukan Sekarang

Tidak ada yang perlu dijual, tidak ada yang perlu panik. Tapi ada langkah berbiaya nol:

- **Berhenti pakai ulang alamat.** Terima di alamat baru setiap kali, jangan menumpuk saldo di alamat yang sudah pernah spending.
- **Simpan kunci privat dengan benar** — backup berlapis, jangan satu titik kegagalan.
- **Jangan SMMA (spend from the same address) besar-besaran** dari alamat lama.
- **Pantau BIP-360 dan BIP-361.** Dua proposal inilah yang nanti jadi dasar output type post-quantum dan aturan sunset tanda tangan lama.
- **Bedakan ancaman kuantum dari risiko harian.** Kebocoran seed phrase, phishing, dan malware jauh lebih sering bikin orang kehilangan koin daripada kuantum.

## Kesimpulan

Coinbase tidak bilang Bitcoin dalam bahaya hari ini — mereka bilang Bitcoin **butuh mulai bersiap**, dan migrasinya tidak bisa diburu-buru. Yang menarik: masalahnya sudah punya jalur konkret (BIP-360, hybrid 1-of-2, evaluasi ML-DSA/SLH-DSA), bukan cuma kecemasan. Buat pemegang BTC, waktu paling murah untuk memperbaiki kebiasaan dompet adalah sekarang — sebelum ada alasan untuk buru-buru.

Kamu sendiri gimana — masih pakai satu alamat buat semua transaksi, atau sudah rutin rotasi alamat? Cerita di komentar, ya.

---

*Sumber: blog resmi Coinbase (13 Okt 2026), The Quantum Insider, 24/7 Wall St., proposal BIP-360 & BIP-361.*

— Chokdi 🐷 · Content Studio · 2026
