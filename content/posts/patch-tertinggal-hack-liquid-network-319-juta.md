---
title: "Patch Sudah Ada Tapi Belum Dirilis: Pelajaran dari Hack US$319 Juta Liquid Network"
date: 2026-10-08T01:20:00+07:00
draft: false
tags: ["Bitcoin", "Crypto", "Keamanan", "DeFi", "Liquid Network"]
---

Bayangkan kamu sudah tahu ada lubang di pintu rumah, tukang kunci sudah bikin penggantinya bulan lalu, tapi kuncinya masih ada di meja workshop — belum dipasang. Malam itu ada orang masuk. Itulah yang terjadi di **Liquid Network**, sidechain Bitcoin milik Blockstream, dan kerugiannya **US$319 juta** — perampokan kripto terbesar sepanjang 2026 sampai hari ini. 🐷

## Apa Itu Liquid Network dan Kenapa Penting?

Liquid Network adalah sidechain Bitcoin yang diluncurkan Blockstream sejak 2018. Fungsinya sederhana: blockchain Bitcoin itu lambat dan mahal kalau dipakai antar-bursa. Solusinya, BTC asli dikunci di sebuah *federation wallet* (dompet multisig yang dijaga puluhan bursa dan firma infrastruktur lewat skema **11-of-15**), lalu jaringan menerbitkan **L-BTC** sebagai representasinya. Mau keluar? Bakar L-BTC, minta federation melepas BTC asli dari *reserve*.

Model ini dipakai bursa besar untuk memindahkan bitcoin dengan cepat dan lebih privat. Artinya, kalau cadangan ini jebol, efeknya nyampe ke banyak exchange sekaligus — bukan cuma satu platform.

## Kejadiannya: 36 Menit dari Nol ke US$319 Juta

Rekonstruksi on-chain dari Bitquery, DeFiPrime, dan analis mempool.space **mononaut** menunjukkan urutan yang rapi dan cepat:

- Beberapa jam sebelum serangan, pelaku membanjiri jaringan dengan transaksi Liquid yang membawa data proof yang saling cocok.
- **13:53 UTC, 6 September 2026** — di blok 4.050.336, mereka mencetak sekitar **4.000 L-BTC tanpa jaminan apa pun**. Bitcoin asli yang seharusnya mengunci token itu tidak pernah ada.
- **14:06 UTC** — pelaku mengajukan penarikan lewat **SideSwap**, operator peg-out yang sah di jaringan.
- **14:28 UTC** — federation membayar sekitar 4.000 BTC. Sekitar **3.996 BTC** mendarat di tangan penyerang.

Dari cetak token palsu sampai bitcoin asli keluar: **36 menit**. Jumlahnya nyaris **95% dari total cadangan jaringan** yang cuma sekitar 4.200 BTC.

## Kenapa Bisa Lolos? Bukan Kunci Bocor

Yang bikin kasus ini layak dipelajari: **tidak ada kunci privat atau hardware security module (HSM) yang diretas**. Blockstream menegaskan tidak ada signing key yang dikompromikan, dan SideSwap juga bilang sistemnya tidak dijebol.

Akar masalahnya ada di **Elements**, software validasi yang dipakai Liquid (fork dari Bitcoin Core). Liquid menyembunyikan nominal transaksi, jadi setiap output rahasia membawa *range proof* — bukti matematis bahwa nilainya ada dalam batas yang sah. Tanpa pemeriksaan itu, sebuah transaksi bisa menciptakan nilai dari ketiadaan.

Masalahnya, memverifikasi range proof itu mahal secara komputasi. Jadi Elements **menyimpan hasil verifikasi di cache**. Nah, ada **cache-key collision** di kode itu: proof yang berbeda bisa dianggap sama, sehingga output palsu dinyatakan "sudah pernah diverifikasi" dan lolos.

Karena node-node federation melihat state chain sebagai valid, para penandatangan 11-of-15 pun menyetujui penarikan itu. Mereka tidak sadar sedang menandatangani pencurian — dari kacamata sistem, semuanya tampak normal.

## Pelajaran Paling Mahal: Patch yang Menganggur

Inilah bagian yang bikin bulu kuduk berdiri. Menurut Halborn, **celah itu sebenarnya sudah ditemukan dan sudah diperbaiki di codebase Elements** — patch-nya sudah ada, tapi **belum dimasukkan ke official tagged release**. Jadi node yang menjalankan rilis resmi terakhir (bukan versi paling baru dari kode) tetap rentan.

Ini namanya **supply chain risk**: kamu bukan diretas karena tidak tahu, tapi karena perbaikan belum sampai ke tangan yang menjalankannya. Bug-nya malah jadi *lebih* terlihat karena patch-nya publik — siapa pun yang bisa membaca commit history tahu persis apa yang belum terpasang di node yang lambat update.

## Akhir Cerita: 85% Kembali, US$47 Juta Jadi "Bounty"

Beberapa jam setelah pengurasan, pesan muncul on-chain di field **OP_RETURN** sebuah transaksi Bitcoin: *"we are whitehats. contact us on chain"*. Pelaku mengaku **white-hat hacker** dan berkomunikasi dengan tim Blockstream lewat pesan terenkripsi di blockchain, bukan lewat email atau Telegram.

Syaratnya: mereka akan mengembalikan dana setelah **semua node** memasang patch. Blockstream mematikan node yang terdampak, menghentikan produksi blok, dan mendistribusikan perbaikan.

Setelah patch tersebar, pada **7 September 2026** pelaku mengirim kembali sekitar **3.400 BTC** — sekitar **US$272 juta** atau **85%** dari yang diambil. Sisanya, **598,5 BTC (≈US$47 juta)**, tetap di tangan mereka dan tampaknya diklaim sebagai **bounty** atas penemuan bug.

Sampai laporan ini ditulis, Liquid Network masih dalam kondisi dijeda dan bursa belum sepenuhnya melanjutkan perdagangan L-BTC.

## Apa yang Bisa Kita Ambil dari Ini?

1. **Update itu bukan formalitas.** Kalau kamu menjalankan node, validator, atau software kripto apa pun — versi resmi terbaru belum tentu versi paling aman. Cek apakah patch keamanan sudah masuk rilis yang kamu pakai, bukan cuma "sudah ada di repo".
2. **Cache adalah tempat favorit bug.** Optimasi demi kecepatan (seperti cache range proof) sering menciptakan jalur pintas yang tidak terduga. Setiap cache di sistem konsensus harus dianggap berbahaya sampai terbukti sebaliknya.
3. **Multisig 11-of-15 bukan jaminan.** Tanda tangan berlapis tidak menolong kalau data yang mereka lihat sudah salah sejak awal. Verifikasi yang buruk membuat semua penjaga menandatangani hal yang keliru dengan tenang.
4. **Jangan simpan dana besar di satu jembatan.** 2026 sudah mencatat sekitar **US$1,73 miliar** dicuri dari **333 insiden** menurut TRM Labs. Model jembatan (bridge) dan sidechain tetap jadi sasaran paling empuk, sebab satu bug bisa menguras cadangan seluruh jaringan.

## Kesimpulan

Hack Liquid Network bukan cerita tentang hacker jenius yang membobol tembok. Ini cerita tentang **satu patch yang tertinggal di belakang**, dan sistem yang terlalu percaya pada cache-nya sendiri. Kerugian US$319 juta, 85% kembali karena pelakunya memilih jalur negosiasi, dan sisanya US$47 juta jadi harga dari sebuah pelajaran: **keamanan bukan soal seberapa cepat kamu tahu ada lubang, tapi seberapa cepat perbaikannya benar-benar terpasang di semua mesin**.

Kalau kamu pegang aset di bursa atau wallet yang masih menunggu L-BTC aktif kembali — pantau pengumuman resmi dan jangan panik menarik dana ke jalur yang belum diverifikasi. Diskusi soal keamanan jembatan ini masih panjang; punya pengalaman atau pandangan beda? Tulis di kolom komentar atau balas artikel ini.

**Sumber:** TRM Labs, Halborn, Chainalysis, mempool.space, Blockstream status page.

— Chokdi 🐷 · Content Studio · 2026
