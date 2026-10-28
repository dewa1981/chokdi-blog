---
title: "Dragon Tiger: Satu Kartu, Tiga Aturan, Selisihnya 0% vs 7,47%"
date: 2026-10-29T00:12:00+07:00
draft: false
tags: ["Kasino", "Dragon Tiger", "House Edge", "Probabilitas"]
---

Dragon Tiger kelihatan seperti game paling polos di meja kasino: dua kartu dibuka, satu untuk Dragon satu untuk Tiger, kita cuma menebak mana yang lebih tinggi. Tidak ada Hit, tidak ada Stand, tidak ada strategi. Justru karena sesederhana itu, semua keputusan yang tersisa ada di **aturan mejanya** — dan di situ selisihnya besar sekali.

Artikel ini menghitung sendiri seluruh kombinasinya, bukan mengutip brosur. Hasilnya: taruhan utama yang sama bisa punya house edge **0%** atau **7,47%** tergantung dua hal — jumlah deck dan apa yang terjadi saat *tie*.

## Cara main dalam 30 detik

- Kartu diurutkan dari As (terendah) sampai King (tertinggi): A, 2, 3, …, 10, J, Q, K.
- Satu kartu untuk Dragon, satu kartu untuk Tiger. Tidak ada kartu tambahan.
- Pilihan taruhan: **Dragon**, **Tiger**, atau **Tie**. Bayaran Dragon/Tiger 1:1, Tie biasanya 8:1 (vendor lain 10:1 atau 11:1).
- Pragmatic Play dan SA Gaming memakai **8 deck**; Deltin menulis 6–8 deck.

Selesai. Tidak ada yang bisa dianalisis dari kartu sebelumnya karena tiap ronde hanya dua kartu. Jadi satu-satunya yang menentukan apakah kita rugi banyak atau sedikit adalah lembar aturan yang tercetak kecil di meja.

## Tiga aturan tie, tiga house edge berbeda

Ini inti artikelnya. Saat kartu Dragon dan Tiger sama nilainya (*tie*), tiap meja punya kebijakan berbeda, dan kebijakan itu langsung mengubah matematika taruhan Dragon/Tiger.

| Aturan saat tie | House edge 8 deck | House edge 1 deck |
|---|---|---|
| Stake kembali (push) | **0,00000%** | 0,00000% |
| Setengah stake hangus (paling umum) | **−3,73494%** | −2,94118% |
| Stake hangus penuh | **−7,46988%** | −5,88235% |

Angka di atas bukan perkiraan. Saya enumerasi seluruh pasangan kartu terurut:

- **8 deck** = 416 kartu → 172.640 pasangan; 12.896 di antaranya tie. Peluang tie **7,46988%**, peluang menang **46,26506%**.
- **1 deck** = 52 kartu → 2.652 pasangan; 156 tie. Peluang tie **5,88235%**, peluang menang **47,05882%**.

Kalau dicek ke tabel kombinasi Michael Shackleford (Wizard of Odds) untuk 8 deck: menang 39.936, tie 6.448, kalah 39.936 dari 86.320 kombinasi tak berurut — persis sama dengan hitungan saya (86.320 = 172.640 ÷ 2). Return totalnya −0,037349, alias house edge 3,73%.

**Bacaan praktisnya:** kalau meja menulis "tie = setengah stake hangus", RTP-nya **96,27%**. Kalau meja membalikkan stake utuh saat tie (jarang, tapi ada), RTP-nya 100% — dan kasino tidak akan lama membiarkan meja itu hidup. Kalau tie menghanguskan seluruh stake, RTP-nya jatuh ke **92,53%**, lebih buruk dari [roulette Eropa yang cuma −2,70%](/posts/roulette-house-edge-martingale/).

## Taruhan Tie: jebakan dengan angka paling terang

Taruhan Tie adalah tempat kasino mengambil paling banyak, dan anehnya paling sering dipromosikan di meja. Dengan 8 deck, peluang tie hanya 7,46988%. Artinya **fair odds**-nya 12,39:1. Begini perbandingannya kalau bayarannya berubah:

| Bayaran Tie | House edge (8 deck) |
|---|---|
| 12:1 | −2,89% |
| 11:1 (Pragmatic Play) | −10,36% |
| 10:1 (Deltin) | −17,83% |
| 9:1 | −25,30% |
| 8:1 (SA Gaming) | **−32,77%** |

Perhatikan satu hal yang sering terlewat: **semakin sedikit deck, taruhan Tie semakin buruk**, karena tie jadi lebih jarang. Di meja 1 deck, peluang tie cuma 5,88% sehingga fair odds-nya **16:1**, bukan 12,39:1. Bayaran 8:1 di meja 1 deck = house edge **−47,06%** — hampir separuh uang hangus dalam jangka panjang.

Jadi ada trade-off yang berlawanan arah dan hampir tidak pernah dijelaskan ke pemain:

- **Taruhan Dragon/Tiger lebih baik di deck sedikit** (−2,94% vs −3,73%).
- **Taruhan Tie jauh lebih buruk di deck sedikit** (−47,06% vs −32,77%).

Satu meja, dua kesimpulan berlawanan. Karena itu bertanya "Dragon Tiger bagus atau tidak?" tanpa menyebut jumlah deck dan aturan tie adalah pertanyaan yang tidak bisa dijawab.

## Side bet: semuanya di atas 5%

Meja Dragon Tiger modern menempelkan banyak taruhan sampingan. Semua sudah dihitung Shackleford untuk 8 deck:

- **Suited Tie** (nilai dan jenis kartu sama) 50:1 → house edge **−13,98%**. Peluangnya 1,6867% (1.456 dari 86.320).
- **Big/Small** (kartu di atas atau di bawah 7; angka 7 kalah) 1:1 → **−7,69%** (192 menang dari 416 kartu).
- **Odd/Even** 1:1 → **−7,69%**, karena 6 dari 13 rank menang dan 7 kalah. Versi SA Gaming sedikit berbeda: Even 1,05:1 → −5,38%, Odd 0,75:1 → −5,77%.

Pola yang konsisten: taruhan utama paling murah, taruhan sampingan paling mahal. Ini sama seperti yang terjadi di [sicbo, di mana dua kotak berlabel "6:1" bisa beda 6 poin house edge](/posts/sicbo-216-kombinasi-house-edge/).

## Dalam rupiah: 1.000 tangan × Rp100.000

Turnover Rp100 juta. Semua angka dihitung dari persentase di atas, bukan dikira-kira:

| Skenario | Hasil yang diharapkan |
|---|---|
| Tie = push (stake kembali) | **Rp0** |
| Tie = setengah hangus, 8 deck | **−Rp3.734.940** |
| Tie = stake hangus penuh, 8 deck | **−Rp7.469.880** |
| Tie = setengah hangus, 1 deck | −Rp2.941.180 |
| Semua ke taruhan Tie 8:1 (8 deck) | **−Rp32.771.080** |
| Semua ke taruhan Tie 11:1 (8 deck) | −Rp10.361.450 |

Per tangan, taruhan Dragon/Tiger di meja 8 deck standar memakan sekitar **Rp3.735** dari setiap Rp100.000 yang dipasang. Kelihatan kecil per ronde, tapi 1.000 ronde bukan durasi yang aneh untuk satu sesi meja live.

Dan jangan tertipu pola. Peluang kalah 10 kali beruntun pada taruhan Dragon di 8 deck adalah **0,200709%** — sekitar 1 dari 498 urutan 10 tangan. Itu berarti dalam 1.000 tangan, rangkaian kalah 10 kali beruntun hampir pasti muncul setidaknya sekali. Ini alasan yang sama kenapa [martingale di roulette tidak menyelamatkan apa pun](/posts/roulette-house-edge-martingale/), dan kenapa ukuran taruhan sebaiknya ditentukan sebelum duduk, bukan setelah kalah — lihat [kelly criterion untuk batas taruhan yang masuk akal](/posts/kelly-criterion-ukuran-taruhan-bankroll/).

## Checklist sebelum duduk

1. **Cari tahu jumlah deck-nya.** 8 deck = standar. Kalau tertulis 6 deck, house edge taruhan Tie berubah (10:1 di 6 deck = −18,65%, bukan −17,83%).
2. **Baca aturan tie di lembar meja.** "Setengah hangus" = 3,73%. "Hangus penuh" = 7,47%. Ini beda 2× dan tertulis kecil sekali.
3. **Cek bayaran Tie sebelum menyentuhnya.** 11:1 masih −10,36%; 8:1 sudah −32,77%. Tidak ada versi Tie yang menguntungkan pemain.
4. **Hindari side bet kalau tujuannya menang lama.** Suited Tie, Big/Small, Odd/Even semuanya 5% ke atas.
5. **Bandingkan dengan meja lain.** Banker baccarat 1,06% dan Player 1,24% lebih murah dari Dragon/Tiger 3,73% — perbandingan lengkapnya ada di [baccarat: banker vs player](/posts/baccarat-banker-vs-player-house-edge/).

## Kesimpulan

Dragon Tiger bukan game "50:50 yang adil". Dia game 50:50 **yang dipotong**, dan besar potongannya ditentukan oleh dua baris aturan yang jarang dibaca orang: jumlah deck dan perlakuan saat tie. Di meja terbaik, potongannya 2,94%; di meja terburuk, 7,47%. Taruhan utamanya masih salah satu yang termurah di lantai kasino — tapi seluruh taruhan sampingannya adalah tempat uang mengalir keluar.

Kalau mau main dengan aturan yang jelas dan meja yang sudah dikurasi, funnel live casino kami ada di sini:

<!-- cta-funnel -->
> **Mau coba meja Dragon Tiger dengan aturan tie yang transparan?**
> Cek meja live casino VIP — RTP dan aturan tie ditulis terbuka sebelum Anda pasang kartu pertama.
> 👉 **[MASUK MEJA VIP SEKARANG](https://tomat.jagungbaru.com/banner/vip?utm_source=blog&utm_campaign=dragon-tiger-satu-kartu-tiga-aturan)**

Sumber angka: [Wizard of Odds — Dragon Tiger](https://wizardofodds.com/games/dragon-tiger/) (diperbarui 2 Okt 2026), aturan resmi Pragmatic Play dan SA Gaming. Semua persentase dihitung ulang dari enumerasi kombinasi, bukan dikutip mentah — kalau ada yang mau saya hitung ulang untuk jumlah deck tertentu, tulis di komentar.

— Chokdi 🐷 · Content Studio · 2026
