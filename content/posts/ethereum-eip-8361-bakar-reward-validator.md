---
title: "EIP-8361: Ethereum Bakar Reward Validator, Issuance Bisa Nol Jika Staking Tembus 50%"
date: 2026-08-30T18:35:00+07:00
draft: false
tags: ["Crypto", "Ethereum"]
---

# EIP-8361: Ethereum Bakar Reward Validator, Issuance Bisa Nol Jika Staking Tembus 50%

Ethereum lagi ramai — bukan cuma karena harga, tapi karena proposal kontroversial bernama **EIP-8361**. Enam peneliti ternama, termasuk Justin Drake dari Ethereum Foundation, mengusulkan agar reward validator dibakar makin banyak seiring naiknya rasio staking, sampai issuance baru benar-benar nol ketika 50% supply ETH terkunci di staking. Buat pemegang ETH, ini kabar baik di jangka panjang (aset makin langka); buat staker, yield bisa tergerus habis.

## Apa Itu EIP-8361?

EIP-8361 alias *tapered issuance burn* mengubah kebijakan moneter Ethereum secara fundamental. Mekanismenya sederhana tapi berani:

- Setiap validator kena **potongan reward** yang naik seiring rasio staking.
- Pada angka saturasi **60,25 juta ETH** (sekitar setengah supply), potongan mencapai **100%** — reward staking bersih jadi nol.
- Yang dibakar hanya ETH hasil issuance baru; **fee transaksi dan tips tetap utuh**.
- Hanya menyentuh *consensus layer* — klien Prysm sudah punya implementasi draft sekitar 300 baris.

Besar potongan mengikuti rumus rasio staking pangkat 1,5, dan penerapannya bertahap selama 18 bulan (total sekitar 2 tahun termasuk *lead time* fork). Tujuannya satu: mematikan insentif staking yang selama ini tidak pernah berhenti.

## Kenapa Proposal Ini Muncul Sekarang?

Kurva issuance Ethereum sekarang punya masalah: yield hanya turun sebesar akar kuadrat dari rasio staking, dengan lantai sekitar **1,5%** berapa pun ETH yang di-stake. Artinya, selama yield masih di atas premi risiko, orang akan terus stake — tanpa batas.

- Rasio staking Ethereum sudah melewati **sepertiga supply** sejak April 2026.
- Antrean validator penuh terus di *maximum churn*.
- Salah satu penulis, Jérôme de Tychey, memperingatkan skenario terburuk: **lebih dari 70 juta ETH** (55%+ supply) bisa terkunci pada Januari 2028. "The window is closing," tulisnya.

Alasan lain: yield tinggi membuat ETH mengalir ke exchange dan staking provider besar, memicu sentralisasi, melemahkan kredibilitas *social slashing*, dan mengusir solo staker. Yang tidak stake juga kena dilusi — dan token staking likuid (LST) perlahan menggantikan ETH mentah sebagai alat bayar di ekosistem.

## Dampaknya ke Staker dan Harga ETH

| Rasio Staking | Potongan Reward | Kondisi |
|---|---|---|
| Di bawah 20% | Minim | Issuance puncak (~0,5% supply/tahun) |
| 33% (kondisi sekarang) | Mulai naik bertahap | Yield ~2,6%, turun perlahan |
| 50% (~60,25 juta ETH) | 100% | Issuance nol, reward bersih nol |

Yang paling kena adalah operator besar: karena potongan naik lebih cepat dari pertumbuhan stake, operator yang pegang setengah stake sudah tidak diuntungkan tumbuh lagi di rasio ~31%. Konsensus issuance hari ini menyumbang **minimal 93%** dari total yield staking — jadi kalau ini mati, ya mati total.

Di sisi lain, issuance nol berarti ETH **tidak lagi terdilusi** — kandidat kuat jadi aset deflasi, sejalan dengan narasi [bitcoin makin mirip emas](https://chokdi.ano99.com/posts/bitcoin-makin-mirip-emas-korelasi-50-persen/) yang sedang tren di pasar.

## Kontroversi: Lido vs Penulis

Tidak butuh sehari, proposal ini langsung dapat tentangan. Isidoros Passadis, Chief of Staking di Lido, menyebut risetnya "terlalu teoretis" dan memperingatkan kurva ini bisa menciptakan keseimbangan macet di 50% staked dengan yield nol — yang dia sebut *death-knell* bagi keamanan jaringan. Menurutnya, membatasi staking cuma memindahkan masalah *too-big-to-fail* ke tempat lain.

Penulis membalas lebih dulu: "Nobody needs to protect solo stakers from this EIP" — justru solo staker yang perlu dilindungi dari kurva dilusi tanpa saklar mati seperti sekarang. Timing-nya juga panas: EIP ini muncul dua hari sebelum deadline inklusi upgrade Hegotá, dan kemungkinan besar **tidak masuk** upgrade tersebut.

## Kesimpulan

EIP-8361 masih draft dan proses inklusinya panjang, tapi arah kebijakan moneter Ethereum mulai jelas: dari "staking = sumber penghasilan" bergeser ke "staking = jaga keamanan jaringan". Kalau jadi, ETH bakal makin langka dan deflasi — kabar bagus untuk harga jangka panjang, tapi pahit untuk para staker. Perdebatan ini baru mulai, dan hasilnya bakal menentukan nasib ETH sebagai uang. Setuju atau nggak dengan proposal ini? Tulis pendapatmu di kolom komentar!

*Artikel ini ditulis oleh Chokdi 🐷 · Content Studio · 2026. Bukan saran investasi — riset dulu sebelum ambil keputusan.*
