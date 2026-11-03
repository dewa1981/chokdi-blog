---
title: "Casino War: Edge 2,88% dari Satu Kartu — dan Tie Bet 10:1 yang Bocor 18,65%"
date: 2026-11-03T12:10:00+07:00
draft: false
tags: ["Kasino", "Casino War", "House Edge", "Matematika Taruhan", "Tie Bet"]
---

Casino War adalah game kartu paling sederhana di lantai kasino: kamu dan bandar masing-masing dapat satu kartu, yang lebih tinggi menang. Tidak ada keputusan, tidak ada strategi, tidak ada hitungan kartu. Karena kelihatan "cuma lempar koin", banyak pemain menganggap edge-nya tipis. Kenyataannya **2,88%** — hampir tiga kali lipat baccarat (1,06%) dan dua kali craps pass line (1,41%). Dan yang paling mahal justru taruhan sampingannya: **tie bet 10:1 dengan house edge 18,65%**.

Artikel ini membedah angkanya sampai ke tabel probabilitas, bukan cuma mengutip brosur.

## Aturan dalam 30 detik

Main pakai **enam deck**, peringkat kartu seperti poker, **as selalu tinggi**, jenis kartu (suit) tidak berpengaruh.

1. Kamu dan bandar masing-masing dapat satu kartu.
2. Kartumu lebih tinggi → menang even money. Lebih rendah → modal hilang.
3. **Seri (tie)** → dua pilihan: **menyerah** (kehilangan setengah taruhan) atau **perang** (menambah taruhan sebesar taruhan awal, lalu masing-masing dapat satu kartu lagi).
4. Kalau perang dimenangkan (kartu kedua sama atau lebih tinggi): taruhan tambahan menang even money, taruhan awal **push** (kembali utuh). Kalau kalah: **dua-duanya hangus**.

Perhatikan poin 4. Di sinilah seluruh keuntungan bandar bersembunyi.

## Dari mana angka 2,88% datang

Tabel hasil untuk enam deck, aturan standar ("stingy": tidak ada bonus kalau seri dua kali), dengan asumsi pemain selalu memilih perang:

| Kejadian | Dibayar | Probabilitas | Kontribusi EV |
| --- | --- | --- | --- |
| Menang | +1 | 0,502735 | +0,502735 |
| Kalah taruhan awal | −1 | 0,463023 | −0,463023 |
| Kalah setelah perang | −2 | 0,034242 | −0,068484 |
| **Total** | | **1,000000** | **−0,028772** |

Totalnya **−2,8772%**. Itu house edge-nya.

Sebelum perang diputuskan, peluangnya persis seimbang: kartu pemain lebih tinggi **46,3023%**, bandar lebih tinggi **46,3023%**, seri **7,3955%**. Tanpa aturan perang, game ini adil. Yang membalikkan keadaan adalah rumus pembayaran perang: **kamu mempertaruhkan dua unit untuk memenangkan satu unit**. Kemenangan perang cuma membayar taruhan tambahan, sementara kekalahan perang menyapu taruhan awal sekaligus tambahannya. Asimetri 2-untuk-1 itulah mesin cetak uangnya.

## Element of risk: 2,68%, bukan 2,88%

Kasino sering mengutip angka yang lebih "ramah": **element of risk 2,68%**. Ini bukan pemasaran kosong, tapi cara hitung yang berbeda. Karena perang hanya terjadi saat seri (7,3955%), rata-rata uang yang kamu pertaruhkan per tangan bukan 1 unit, melainkan:

**1 + 0,073955 = 1,07395 unit**

Maka 2,8772% ÷ 1,07395 = **2,679%** dari total aksi. Dua-duanya benar — bedanya cuma penyebut. Yang penting: jangan tertipu membaca "2,68%" sebagai lebih murah, karena modal yang berputar juga lebih besar.

## Menyerah justru lebih rugi, dan ini bisa dibuktikan

Naluri bilang: kalau seri, mending menyerah, kehilangan setengah saja. Matematikanya bilang sebaliknya. Kalau menyerah, kerugian per tangan = 0,5 × peluang seri:

**0,5 × 7,3955% = 3,698%**

Itu persis house edge aturan surrender di tabel Wizard of Odds: **3,70%** untuk enam deck. Jadi menyerah menambah kerugian dari 2,88% menjadi 3,70% — sekitar 28% lebih boros. Selalu pilih perang. (Kalau kamu main di meja dengan aturan "liberal" — bonus sebesar taruhan awal saat seri dua kali — edge turun ke **2,33%**; varian super liberal dengan bonus 3× ante menyentuh **1,24%**.)

## Tie bet: 18,65% adalah lubang paling dalam di meja

Taruhan sampingan "kartu pertama seri" membayar **10:1** dan kelihatan menggoda. Peluang sebenarnya cuma **7,3955%**.

EV = (0,073955 × 10) − (1 − 0,073955) = **−18,649%**

Bahkan kalau kasino membayar 11:1 (software Habanero), edge-nya masih **−11,25%**. Bandingkan dengan taruhan utama 2,88%: tie bet **enam kali lebih mahal**. Ini taruhan yang secara matematis tidak pernah layak, seberapa pun "feeling" kamu soal kartu kembar.

Untuk skala nyata: dengan ante Rp100.000 dan 1.000 tangan, ekspektasi kerugian di taruhan utama ≈ **Rp2.877.000** (asumsi kamu tidak menyentuh tie bet dan selalu memilih perang saat seri).

## Posisi Casino War di rak game

Dari daftar house edge standar: blackjack strategi dasar ±0,5%, baccarat 1,06%, craps pass line 1,41%, Casino War 2,88%, roulette Eropa 2,70%, American roulette 5,26%, keno bisa 25–30%. Artinya Casino War bukan game terburuk — dia di tengah. Yang membuatnya berbahaya bukan angkanya, tapi **kecepatannya**: satu tangan selesai dalam hitungan detik, tanpa jeda berpikir. Rumah tangga 2,88% per tangan, dimainkan 300–500 tangan per jam, terasa jauh lebih mahal daripada baccarat 1,06% yang ritmenya lebih lambat.

Kesimpulan praktis: kalau mau main, main di taruhan utama saja, selalu perang saat seri, jangan pernah sentuh tie bet, dan hitung kerugian yang diharapkan dari **jumlah tangan**, bukan dari durasi duduk.

**Sumber:**
- Wizard of Odds — [Casino War](https://wizardofodds.com/games/casino-war/) (tabel analisis & house edge per jumlah deck, Michael Shackleford)
- Wizard of Odds — [House Edge Comparison](https://wizardofodds.com/gambling/house-edge/)
- Cache Creek Casino Resort — [Casino War Odds](https://www.cachecreek.com/casino-war-odds)

— Chokdi 🐷 · Content Studio · 2026
