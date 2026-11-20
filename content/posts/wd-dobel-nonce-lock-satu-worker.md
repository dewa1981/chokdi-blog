---
title: "Kenapa WD Bisa Dobel: Nonce, Kunci, dan Aturan Satu Worker di Pembayaran Otomatis"
date: 2026-11-21T00:20:00+07:00
draft: false
tags: ["Sistem Pembayaran", "Crypto", "Engineering"]
---

WD dobel hampir tidak pernah karena "bandar nakal". Hampir selalu karena **dua request membaca angka yang sama pada waktu yang sama** — lalu sistem salah menyimpulkan bahwa pembayaran pertama gagal. Artikel ini membedah satu kasus nyata di sistem pembayaran otomatis berbasis USDT: dari nonce yang bentrok, prefix `0x` dobel yang bikin broadcast ditolak setelah ditandatangani, sampai alasan kenapa app-nya **wajib** jalan dengan satu worker.

Semua angka di bawah diambil dari uji produksi, bukan perkiraan.

## Dua tombol, satu nonce

Sistem pembayaran otomatis yang menandatangani transaksi sendiri (bukan lewat node wallet) harus mengambil nonce akun lebih dulu. Cara paling naif — dan paling sering dipakai — adalah `eth_getTransactionCount(alamat, "latest")`.

Masalahnya: `latest` hanya menghitung transaksi yang **sudah masuk blok**. Penjelasan di [Ethereum Stack Exchange](https://ethereum.stackexchange.com/questions/39790/concurrency-patterns-for-account-nonce) menyebut nonce justru satu-satunya elemen yang memaksa transaksi sebuah akun berjalan berurutan, sehingga saat aplikasi menandatangani beberapa transaksi paralel, "hanya satu yang akan berhasil" kecuali hitungannya dimanipulasi dengan benar.

Akibat praktisnya di panel depo/WD:

- Dua klik "Bayar" dalam detik yang sama membaca nonce **yang sama**.
- Transaksi kedua dianggap *replacement* transaksi pertama — di mempool, aturan penggantian memang berbasis pengirim + nonce yang sama ([onfinality](https://onfinality.io/en/learn/eth-sendrawtransaction-replacement-underpriced) menulis "same sender + same nonce = replacement attempt").
- Uang bisa hilang (satu tx tertimpa) atau, kalau admin menekan bayar lagi setelah status ambigu, **terkirim dua kali**.

Peringatan dari dokumentasi yang sama layak ditempel di dashboard: memakai nonce **baru** padahal seharusnya nonce yang sama disebut sebagai "kesalahan paling merusak" — karena yang terjadi berikutnya adalah lubang nonce dan transaksi menggantung.

## Perbaikan 1: antrean nonce, bukan tebak-tebakan

Perbaikannya bukan "tambah `sleep`", tapi membuat nonce keluar dari satu pintu:

1. Sumber nonce = `max(nonce "pending" on-chain, counter lokal persisten)`. `pending` sudah memasukkan tx di mempool; counter lokal menutup celah saat dua kiriman beruntun terjadi sebelum node melihat tx pertama.
2. Seluruh urutan **baca nonce → tanda tangan → broadcast → catat** dibungkus satu kunci.
3. Counter ditulis atomik: file sementara → `fsync` → `os.replace`.
4. Kunci harus berlaku **antarproses**, bukan cuma antar-thread — `fcntl.flock` pada file lock.

Bukti uji: 20 thread bersamaan menghasilkan nonce **5..24**, semuanya unik dan berurutan; simulasi restart melanjutkan dari counter file; dan `flock` antarproses terukur **menunggu 4,0 detik**. Di produksi, dua kiriman **0,01 USDT bersamaan** lolos keduanya — dua txid unik, `status 0x1`, blok 134.557.873, nonce **1264 dan 1265**, biaya total 0,02 USDT.

## Perbaikan 2: prefix `0x` dobel = broadcast ditolak setelah tanda tangan

Ini bug yang paling berbahaya karena **tidak memunculkan error di UI**. Kode memanggil:

```
rpc("eth_sendRawTransaction", ["0x" + raw])
```

Padahal `raw` dari library penandatangan **sudah** ber-prefix `0x`. Node menjawab:

```
Invalid params: invalid value string "0x0xf8ab…"
```

Artinya: transaksi **sudah ditandatangani, sudah dipotong biayanya secara mental, tapi ditolak jaringan**. Aplikasi menerima `ok: false` tanpa txid — dan menyimpulkan "pasti belum terkirim", membuka baris untuk dibayar ulang. Persis di situ pembayaran dobel lahir. Di log, dua kiriman terbukti ditolak node dengan pola ini.

Tiga aturan yang menutup celahnya:

- **txid dihitung sebelum broadcast** (`keccak256` dari raw tx), bukan menunggu balasan node.
- Kalau broadcast ditolak setelah tanda tangan, tetap balas **txid** + penanda `broadcast_ditolak: true`. Aplikasi tidak boleh menganggap "gagal total".
- **Counter nonce tidak dinaikkan** saat broadcast ditolak — supaya tidak terjadi lubang nonce yang membuat semua transaksi berikutnya macet.

Aturan operasionalnya satu kalimat: **ada txid = status `cek`, tidak pernah `tolak`.** Toleransi verifikasi juga dinaikkan (24 → 120 detik di sisi API, 90 → 240 detik di sisi app) karena transaksi BSC bisa masuk blok lebih lambat dari jendela tunggu lama.

## Perbaikan 3: kenapa wajib satu worker

App pembayaran tadi dipindah dari server Flask pengembangan ke gunicorn. Konfigurasinya justru **tidak** mengikuti saran umum "2 × CPU + 1":

```
gunicorn -w 1 --threads 8 --timeout 180
```

Alasannya ada di arsitektur gunicorn sendiri: modelnya *pre-fork*, tiap worker adalah **proses terpisah**. Kontributor gunicorn menyatakannya lugas di [diskusi resmi #3017](https://github.com/benoitc/gunicorn/discussions/3017): *"Gunicorn workers are designed to share nothing."* Di [halaman design](https://gunicorn.org/design/) pun ditulis singkat — **threads share memory, workers isolate failures**.

Karena kunci anti-dobel app itu (`PAY_LOCK`, `CLAIM_LOCK`) disimpan di memori proses, menaikkan `-w 4` berarti **empat kunci berbeda** untuk empat worker. Dua request bisa masuk ke dua worker, sama-sama menganggap dirinya pemegang kunci, dan sama-sama membayar. `--threads 8` tetap aman karena thread berada dalam satu proses dan berbagi memori.

Kalau suatu hari butuh lebih dari satu worker, kuncinya harus pindah keluar: Redis `SETNX`, `SELECT ... FOR UPDATE` di database, atau advisory lock. Sampai itu ada, `-w 1` bukan kemunduran performa — itu syarat keselamatan uang. Catatan ini sengaja ditulis di dokumen review supaya tidak ada yang "optimasi performa" lalu mematahkan anti-dobel.

## Checklist untuk sistem depo/WD sendiri

- Hitung txid **sebelum** broadcast, simpan ke baris transaksi.
- Satu sumber nonce (`pending` + counter lokal), satu kunci yang berlaku antarproses.
- Status ambigu → `cek`, jangan `tolak`. Baris `proses` yang menggantung harus punya *expiry* dan tidak boleh dibayar ulang otomatis.
- Satu worker, atau kunci eksternal kalau worker lebih dari satu.
- Rekonsiliasi terakhir selalu **on-chain** (status `0x1` + event Transfer cocok), bukan dari tampilan UI.

Baca juga: [Terima Pembayaran USDT Otomatis: Alur yang Aman](/posts/terima-pembayaran-usdt-otomatis/), soal [kode unik depo otomatis multi-brand](/posts/qris-kode-unik-depo-otomatis-multibrand/), dan kenapa [WD jam 23:00 baru masuk pagi](/posts/wd-jam-cut-off-skn-rtgs-kenapa-dana-masuk-besok/).

## Penutup

Pembayaran dobel jarang lahir dari niat jahat; ia lahir dari dua baris kode yang membaca angka sama tanpa antrean, dan dari satu status "gagal" yang sebenarnya "belum jelas". Dua-duanya bisa ditutup tanpa menambah server: hitung txid lebih dulu, kunci urutannya, dan jangan pernah menaikkan jumlah worker pada app yang kuncinya hidup di memori.

Punya kasus serupa di sistem pembayaranmu? Ceritakan di kolom komentar — atau uji sendiri dengan nominal 0,01 USDT dulu sebelum menyentuh nominal besar.

— Chokdi 🐷 · Content Studio · 2026
