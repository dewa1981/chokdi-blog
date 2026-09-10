---
title: "Riset Baru: Serangan Quantum ke Bitcoin Turun 50%, AI Bantu Pecahkan Rekor Google"
date: 2026-09-11T00:20:00+07:00
draft: false
tags: ["Crypto", "Bitcoin", "Ethereum", "Quantum", "AI Agent"]
---

Ancaman komputer kuantum ke Bitcoin dan Ethereum baru saja naik satu tingkat — tapi bukan karena mesinnya makin canggih. Justru sebaliknya: **biaya serangan yang dibutuhkan turun drastis**, dan kali ini manusia dibantu AI agent yang bikin kerjanya makin cepat. Paper baru yang dibagikan ke CoinDesk (10 Sep 2026) menunjukkan estimasi sumber daya untuk satu langkah kunci serangan quantum ke crypto **turun lebih dari 50%** dibanding tolok ukur yang dipublikasikan Google Quantum AI pada Maret 2026.

Kalau kamu pegang BTC atau ETH jangka panjang, ini kabar yang perlu dipahami — bukan buat panik, tapi buat tahu kenapa topik "post-quantum" mulai serius dibicarakan di ruang developer.

## Apa Sih yang Baru Dipecahkan?

Penelitian ini menyasar **ECDSA**, skema tanda tangan yang melindungi dompet Bitcoin dan Ethereum (keduanya pakai kurva `secp256k1`). Kalau kriptografi ini jebol, kunci publik yang terekspos bisa diturunkan jadi kunci privat — dan penyerang bisa menandatangani transaksi seolah-olah dia pemilik dompet.

Yang dioptimalkan peneliti bukan serangan utuhnya, tapi satu perhitungan di dalam **algoritma Shor** yang dipakai berulang kali: *point addition*.

Hasilnya, dalam angka yang gampang dicerna:

| Metrik | Google (Maret 2026) | Paper baru (Sep 2026) |
|---|---|---|
| Skor total (qubit × gate) | ± 3 miliar | **± 1,5 miliar** |
| Logical qubit | < 1.200 | **1.151** |
| Toffoli gate | 90 juta (varian 1) | **± 1,3 juta** (langkah teroptimasi) |
| Versi adaptasi algoritma Shor | — | ± 1,96 miliar (tetap di bawah Google) |

Peta jalannya tetap: angka ini belum serangan penuh. Sirkuit baru mencakup satu perhitungan besar, belum termasuk koreksi error fisik, perhitungan Shor lengkap, dan biaya hardware riil. Tapi angkanya terus melorot — paper itu pakai batas data Juli 2026, dan desain yang lebih baru di dalamnya sudah menyentuh **± 1,26 miliar**, bahkan ada varian yang menurunkan kebutuhan mesin ke **813 logical qubit** (dengan konsekuensi komputasi jauh lebih besar).

## Yang Bikin Kali Ini Beda: AI Agent Ikut Ngoprek

Ini bagian paling menarik buat kita yang ngoprek agent AI sehari-hari. Perbaikan itu datang dari **ECDSA.Fail**, tantangan terbuka buatan Eigen Labs. Lebih dari **100 peserta** plus **AI coding agent** menghabiskan sekitar **delapan minggu** menyerang masalah yang sama, menghasilkan **400+ submission** yang diterima.

Pola kerjanya jelas kalau dibaca dari paper:

- **Manusia** memilih arah riset dan membuat perubahan desain besar.
- **AI agent** dipakai berat untuk implementasi, pengujian berulang, dan optimasi-optimasi kecil.
- Paper-nya sendiri tidak memisahkan berapa persen kontribusi manusia vs AI.

Efeknya penting: **hardware kuantum tidak harus makin maju supaya serangan makin dekat.** Selama matematikanya bisa dioptimasi, kebutuhan mesinnya turun. Pola yang sama baru kita lihat di dunia matematika — 10.000 AI agent OpenAI ngoprek masalah jutaan dolar ([ceritanya di sini](/posts/openai-10-ribu-agent-navier-stokes/)).

## Jam Kuantum Crypto Makin Sinkron ke 2029

Kabar riset ini datang bareng gebrakan dari arah lain. Departemen Perdagangan AS menuntaskan penghargaan CHIPS Act senilai masing-masing **hingga US$100 juta** untuk Rigetti, D-Wave, dan Quantinuum — plus ambil saham minoritas di ketiganya. Dananya diarahkan ke mesin *fault-tolerant* yang justru jadi syarat serangan quantum nyata.

Di sisi jaringan:

- **Ethereum** memasang target sendiri: base layer tahan quantum (execution, consensus, data) pada **Desember 2029**.
- **Bitcoin** belum punya deadline jaringan, tapi geraknya kencang lewat **BIP-360** (tipe output post-quantum) dan **BIP-361** (migrasi bertahap dari ECDSA dan Schnorr).

Yang bikin keduanya terasa mendesak: migrasi dompet dan kunci publik yang sudah terekspos itu butuh **bertahun-tahun**, dan tidak bisa dilakukan surut ke belakang.

> "None of this is urgent because an attack is imminent. It is urgent because the remedy takes years and cannot be applied retroactively."
> — **Jieyi Long**, lead author paper sekaligus CTO Theta Labs

Terjemahan bebasnya: bukan karena serangannya besok, tapi karena obatnya lama dan tidak bisa retroaktif.

## Jadi Harus Apa Sekarang?

Poin penting yang jangan dilewatkan: **tidak ada komputer quantum hari ini yang bisa memakai hasil riset ini untuk membobol Bitcoin atau Ethereum.** Ini masih riset estimasi sumber daya.

Langkah praktis yang masuk akal buat pemegang koin:

1. **Jangan pindahkan koin ke alamat baru berulang-ulang** yang bikin kunci publik kamu terekspos di chain tanpa perlu.
2. **Pantau BIP-360 dan BIP-361** — ini jalur resmi migrasi Bitcoin, bukan proyek pinggiran.
3. **Ikuti perkembangan Ethereum** soal target quantum-resistant Desember 2029.
4. **Belajar dari yang sudah nyata**, bukan cuma teori — StarkWare sudah mengeksekusi transaksi Bitcoin quantum-resistant pertama di mainnet ([rekam jejaknya di sini](/posts/bitcoin-transaksi-quantum-resistant-pertama/)).

Kesimpulannya sederhana: keamanan crypto bukan garis lurus antara "aman" dan "jebol". Ada ruang di tengah yang bisa digerakkan dari dua sisi — hardware dan matematika. Dan untuk pertama kalinya, sisi matematika digerakkan ratusan orang dibantu AI agent dalam waktu kurang dari dua bulan.

Menurut kamu, 2029 itu realistis atau cuma angka biar komunitas bergerak lebih cepat? Tulis di kolom komentar ya.

---

**Sumber:**
- [CoinDesk — Crypto researchers cut Bitcoin and Ethereum quantum attack estimate by 50%](https://www.coindesk.com/tech/2026/09/10/crypto-researchers-cut-bitcoin-and-ethereum-quantum-attack-estimate-by-50)
- [CoinDesk — Bitcoin and Ethereum race quantum clock as U.S. backs $300 million hardware push](https://www.coindesk.com/tech/2026/09/09/bitcoin-and-ethereum-race-quantum-clock-as-u-s-backs-usd300-million-hardware-push)
- [Google Research — Safeguarding cryptocurrency by disclosing quantum vulnerabilities responsibly](https://research.google/blog/safeguarding-cryptocurrency-by-disclosing-quantum-vulnerabilities-responsibly/)
- [NIST — Department of Commerce announces finalization of CHIPS R&D award](https://www.nist.gov/news-events/news/2026/09/department-commerce-announces-finalization-chips-rd-award-d-wave)

— Chokdi 🐷 · Content Studio · 2026
