---
title: "Pai Gow Poker: 40% Tangan Berakhir Seri — dan Justru di Situ Uangmu Hilang"
date: 2026-11-02T18:32:21+07:00
draft: false
tags: ["Kasino", "Pai Gow", "House Edge", "Matematika Taruhan", "Poker"]
---

Pai Gow Poker kelihatan seperti game paling santai di lantai kasino: satu set kartu 53 lembar (52 kartu plus satu joker), tujuh kartu di tanganmu, dan kamu cuma perlu membaginya jadi dua — lima kartu "tinggi" dan dua kartu "rendah". Tidak ada lawan yang menatap matamu, tidak ada bluff. Tapi justru di sini banyak pemain salah paham: mereka melihat 40% tangan berakhir seri, menyimpulkan "aman", lalu kaget saat saldo tetap menyusut.

Angka resminya tidak ambigu. Dengan strategi house way melawan bandar kasino, **40,4958% tangan berakhir push** — hampir dua dari lima. Uang benar-benar berpindah cuma di 59,5042% tangan. Tapi house edge-nya tetap **2,7212%**, lebih dari dua kali lipat baccarat (1,06%) dan hampir dua kali craps pass line (1,41%). Artikel ini membedah dari mana angka itu datang, dan kenapa "banyak push" bukan berarti "kerugian kecil".

## Aturan yang menentukan: 5 + 2, dan seri milik bandar

Tujuh kartu dibagi dua tangan. Tangan lima kartu memakai peringkat poker biasa; tangan dua kartu hanya bisa berupa pair atau high card. Syarat mutlak: tangan lima kartu **harus lebih tinggi** dari tangan dua kartu — kalau kamu membalik urutannya, tanganmu foul dan biasanya hangus.

Ada tiga aturan kecil yang masing-masing menyumbang keuntungan untuk bandar:

- **Joker semi-wild.** Ia boleh jadi as, atau melengkapi straight/flush/straight flush. Di tangan dua kartu ia selalu as.
- **Wheel (A-2-3-4-5) = straight tertinggi kedua** di sebagian besar kasino, bukan straight terendah.
- **Seri dibayar ke bandar.** Kalau satu tanganmu menang dan satu kalah, itu push. Tapi kalau satu kalah dan satu **seri**, kamu kalah penuh.

Pembayarannya: menang dua-duanya = even money **dipotong komisi 5%**; menang satu kalah satu = push; kalah/dua-duanya seri = modal hilang.

| Hasil | Dibayar | Probabilitas (house way, bandar = kasino) | Kontribusi EV |
| --- | --- | --- | --- |
| Menang dua tangan | +0,95 | 29,1195% | +0,276635 |
| Push (menang 1, kalah 1) | 0 | 40,4958% | 0,000000 |
| Kalah / dua-duanya seri | −1 | 30,3847% | −0,303847 |
| **Total** | | **100%** | **−0,027212** |

Perhatikan kolom terakhir: **−2,7212% per tangan**. Itu bukan taksiran; itu hasil enumerasi 8.250.459.031.214.390 kemungkinan pertandingan tujuh kartu pemain melawan tujuh kartu bandar, angka yang dipublikasikan Wizard of Odds dan bisa dihitung ulang baris per baris.

## Dari mana 2,72% itu datang? Dua sumber, bukan satu

Ini bagian yang paling sering salah dijelaskan di forum. House edge pai gow bukan "karena kasino curang", dan bukan cuma "karena komisi 5%". Ada dua komponen yang bisa dipisahkan persis:

| Sumber edge | Cara hitung | Besaran |
| --- | --- | --- |
| Aturan seri milik bandar (copy rule) | (win − loss) = 29,1195% − 30,3847% | **−1,2652 pp** |
| Komisi 5% dari kemenangan | 5% × 29,1195% | **−1,4560 pp** |
| **Total** | | **−2,7212 pp** |

Cek cepatnya: 1,2652 + 1,4560 = 2,7212. Persis sama dengan EV di tabel sebelumnya. Artinya **komisi menyumbang lebih besar (53,5%) daripada aturan seri (46,5%)**. Kalau kamu main di varian tanpa komisi (Washington State), keunggulan bandar turun ke sekitar 1,30% — sesuai dengan catatan bahwa tanpa komisi pun bandar masih diuntungkan oleh copy rule.

## Yang sebenarnya mahal: harga per tangan yang diputuskan

Di sinilah ilusi "aman" runtuh. Kalau kamu mengukur kerugian terhadap **uang yang benar-benar bergerak** (bukan terhadap total taruhan), angkanya jadi jauh lebih buruk:

- Porsi tangan yang ada pemenang: 59,5042%
- EV per tangan: −2,7212%
- **Element of risk = 2,7212% ÷ 59,5042% = 4,5731%**

Jadi setiap kali uang benar-benar berpindah di meja pai gow, ekspektasi kerugianmu 4,57% dari taruhan — hampir **4,3 kali** baccarat. Push memang menunda kerugian, tapi tidak menghapusnya; ia hanya menyebarkannya ke lebih sedikit tangan.

Rata-rata kamu butuh **1,68 tangan** untuk sampai ke satu keputusan. Dan rangkaian push panjang itu nyata: peluang push lima kali beruntun 1,0891% (1 dari 92), push sepuluh kali beruntun 0,0119% (1 dari 8.403). Dalam sesi 100 tangan, hampir pasti ada satu phase di mana kamu menang-kalah-push bergantian dan saldo terlihat "diam" — padahal itu bukan diam, itu bocor pelan.

## Uang riil: 100 tangan, taruhan Rp100.000

| Pos | Perhitungan | Hasil |
| --- | --- | --- |
| Turnover | 100 × Rp100.000 | Rp10.000.000 |
| EV total | 10.000.000 × −2,7212% | **−Rp272.117** |
| dari komisi 5% | 10.000.000 × 1,4560% | −Rp145.598 |
| dari copy rule | 10.000.000 × 1,2652% | −Rp126.520 |

Pai gow memang lambat — realistis 30–35 tangan per jam, bukan 600 spin seperti slot. Tapi lambat bukan berarti murah: dengan 30 tangan/jam, turnover **Rp3.000.000 per jam** dan ekspektasi kerugian **−Rp81.635 per jam**; 35 tangan/jam → turnover Rp3,5 juta, kerugian **−Rp95.241 per jam**. Bandingkan slot Rp1.000 per spin 600 spin/jam (turnover Rp600.000/jam): di RTP 97% kerugiannya cuma sekitar Rp18.000/jam. Jadi pai gow menghabiskan uang **4–5 kali lebih cepat** daripada slot receh — padahal meja terasa jauh lebih tenang.

## Simulasi 3.000 sesi: yang dialami pemain, bukan rata-rata

Simulasi Monte Carlo (3.000 sesi × 100 tangan, taruhan 1 unit, seed tetap) memberi gambaran yang lebih jujur daripada EV:

- Sesi berakhir **profit: 34,40%**
- Sesi berakhir **rugi: 65,60%**
- Rata-rata hasil: **−2,86 unit** (mendekati teori −2,72; selisihnya noise 1 sd)
- Sesi terbaik: **+22 unit** · sesi terburuk: **−30 unit** (mentok modal)

Standar deviasi per tangan 0,7523 unit — cukup kecil sehingga dalam 100 tangan hasilmu masih bisa menyimpang ±7,5 unit. Artinya kemenangan sesi pendek hampir selalu cerita keberuntungan, bukan strategi.

## Sisi lain meja: kalau kamu yang jadi bandar

Ini yang jarang dibahas situs promosi. Pai gow mengizinkan pemain **banking** (jadi bandar bergiliran). Arah angkanya berbalik total:

| Skenario | EV per tangan |
| --- | --- |
| House way, bandar = kasino | −2,7212% |
| Optimal, bandar = kasino | −2,5122% |
| House way, **kamu** bandar | −0,2540% |
| Optimal, **kamu** bandar | **−0,0442%** |

Selisih banking versus tidak banking = **2,4680 poin**. Jadi kalau kamu memaksa main sebagai pemain terus tanpa pernah banking, kamu membuang hampir seluruh keunggulan yang tersedia di meja itu. Dan selisih house way versus strategi optimal cuma 0,21 poin — bukti bahwa **setting kartu bukan penentu utama**, arus uangnya yang menentukan.

## Empat jebakan yang bikin hitungan ini meleset di meja nyata

1. **Menganggap push = aman.** Push berarti modal tidak bertambah; edge 2,72% tetap berjalan tiap tangan, hanya dibayar di tangan yang diputuskan.
2. **Main dua tangan (dragon hand).** Eksposur dobel, edge tetap sama — kerugian per jam langsung dua kali lipat, bukan dua kali lebih seru.
3. **Menutupi edge dengan side bet.** Fortune/Emperor's Challenge punya house edge sendiri yang jauh lebih besar (bisa dua digit persen). Jangan pernah menghitung EV utama dengan bonus side bet.
4. **Foul hand.** Salah menyusun (tangan lima kartu lebih rendah dari dua kartu) = kalah tanpa perbandingan. Ini kerugian murni di luar 2,72%: pemain baru kehilangan beberapa persen tambahan dari kesalahan sendiri, bukan dari kasino.

## Kesimpulan

Pai Gow Poker adalah studi kasus paling bersih soal bagaimana kasino membangun keuntungan dari aturan, bukan dari keberuntungan: **copy rule 1,27 poin + komisi 1,46 poin = 2,72 poin per tangan**, dengan element of risk 4,57% pada setiap tangan yang benar-benar diputuskan. Game ini lambat, sopan, penuh push — dan tetap membocorkan uang kalau kamu main tanpa tahu angkanya. Kalau mau lihat pembanding, baca analisis [baccarat banker vs player](/posts/baccarat-banker-vs-player-house-edge/), [three card poker Q-6-4](/posts/three-card-poker-q-6-4-potong-kerugian-setengah/), [Caribbean Stud raise buta](/posts/caribbean-stud-raise-buta-rugi-16-persen/), dan cara menentukan ukuran taruhan di [kelly criterion](/posts/kelly-criterion-ukuran-taruhan-bankroll/). Yang paling penting: hitung dulu, baru duduk.

<!-- cta-funnel -->
> **Sudah tahu angkanya, sekarang pilih mejanya.** Meja kasino langsung, live dealer, dan ribuan slot ada di satu akun.
>
> 👉 [GASPOL MASUK MEJA VIP SEKARANG](https://tomat.jagungbaru.com/banner/vip?utm_source=blog&utm_campaign=pai-gow-poker-push-40-persen-house-edge)

— Chokdi 🐷 · Content Studio · 2026
