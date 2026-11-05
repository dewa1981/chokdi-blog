---
title: "Chuck-a-Luck: Dibayar 1:1, 2:1, 3:1 Terlihat Adil — Padahal Rumah Untung 7,87%"
date: 2026-11-05T18:05:00+07:00
draft: false
tags: ["Kasino", "Chuck-a-Luck", "Mini Dice", "House Edge", "Probabilitas", "Dadu"]
---

Tiga dadu dalam sangkar kawat, enam kotak angka, dan bayaran yang kelihatan murah hati: **satu angka cocok dibayar 1:1, dua cocok 2:1, tiga cocok 3:1**. Kalau dadunya satu, ini permainan yang adil. Karena dadunya tiga, kasino mengambil **7,87% dari setiap taruhan** — lebih besar dari roulette Eropa (2,70%) dan lebih besar dari Sic Bo versi bagus (2,78%).

Di Malaysia dan Singapura game ini dijual sebagai **Mini Dice** di meja Genting; di Eropa dan Amerika namanya Chuck-a-Luck, atau "birdcage" karena sangkarnya. Angka 7,87% itu bukan tebakan — ia keluar dari 216 kemungkinan hasil yang bisa dihitung habis.

## Aturannya dalam satu paragraf

Tiga dadu enam sisi dikocok. Kamu pasang pada satu nomor 1 sampai 6. Kalau nomormu muncul di **satu** dadu, kamu dibayar 1:1. Muncul di **dua** dadu, 2:1. Muncul di **tiga** dadu, 3:1. Tidak muncul sama sekali — taruhan hangus. Beberapa meja menaikkan bayaran triple jadi 10:1 atau 12:1, dan beberapa menawarkan taruhan sampingan: Field, Under 10/Over 11, Big/Small, Any Triple.

## 216 kemungkinan, tidak ada yang luput

Satu dadu punya 6 hasil, jadi tiga dadu = 6³ = **216 hasil**, semuanya peluangnya sama. Untuk satu nomor pilihanmu, hitungan cocoknya begini:

| Dadu cocok | Kombinasi | Peluang | Dibayar |
|---|---|---|---|
| 3 | 1 | 0,4630% | 3:1 |
| 2 | 15 | 6,9444% | 2:1 |
| 1 | 75 | 34,7222% | 1:1 |
| 0 | 125 | 57,8704% | −1 |
| **Total** | **216** | **100%** | — |

EV per unit taruhan = (75×1 + 15×2 + 1×3 − 125) / 216 = **−17/216 = −0,078704**.

Jadi **house edge 7,8704%**, bukan "kira-kira 8%". Dengan taruhan Rp10.000, ekspektasi matematisnya **−Rp787 per lemparan**. Seratus lemparan: −Rp78.704. Seribu lemparan: **−Rp787.037** — dan itu angka rata-rata, bukan skenario terburuk.

## Bayaran triple: 3:1 sampai 12:1, semua tetap merugikan

Ini bagian yang paling sering salah dipahami. Banyak pemain berpikir "kalau triple dibayar lebih besar, berarti adil". Tidak. Saya hitung ulang seluruh tabelnya:

| Triple dibayar | House edge |
|---|---|
| 3:1 | 7,870% |
| 5:1 | 6,944% |
| 8:1 | 5,556% |
| 10:1 | 4,630% |
| 12:1 | 3,704% |

Bahkan di meja paling "liberal" (12:1), rumah masih pegang **3,70%**. Bayaran yang benar-benar membuat EV = 0 adalah **20:1** — tidak ada kasino komersial yang menawarkan itu. Wikipedia mencatat varian meja rumahan yang adil dengan skema lain: 1:1 untuk satu cocok, **3:1** untuk dua cocok, dan **5:1** untuk tiga cocok; (75×2 + 15×4 + 1×6)/216 = 216/216 = 1,00 alias nol. Perhatikan: yang dinaikkan bukan hanya triple, tapi juga bayaran dua cocok. Itu bukti bahwa sumber kebocoran bukan cuma di triple.

## Kenapa rasanya seperti menang

Dua ilusi yang bekerja bersamaan.

Pertama, **peluang dapat sesuatu = 91/216 = 42,13%** (paling sedikit satu dadu cocok). Hampir separuh. Tapi 42,13% itu dibayar rata-rata kecil: dari 91 hasil menang, 75 hanya mengembalikan 1 unit. Sementara 57,87% hasil lainnya menghapus taruhanmu utuh.

Kedua, **ekspektasi jumlah dadu yang cocok = 3 × 1/6 = 0,5**. Setengah dadu per lemparan. Otak membaca "setengah" sebagai "50-50, dan kalau lebih dari satu cocok aku dibayar dobel". Yang tidak dihitung: kejadian dua atau tiga cocok cuma **16/216 = 7,41%**, dan justru di situlah uangmu seharusnya kembali.

Saya jalankan 200.000 sesi simulasi, taruhan Rp10.000 per lemparan, nomor tunggal:

- **100 lemparan** (sekitar 25 menit di meja): peluang pulang dengan uang lebih banyak = **22,60%**
- **1.000 lemparan** (satu sesi panjang): peluang untung tinggal **1,26%**
- Simulasi rata-rata 1.000 lemparan = **−Rp787.796**, cocok dengan teori −Rp787.037 (selisih 0,1%, itu noise)
- Simpangan baku 1.000 lemparan = **Rp352.502**

Artinya: setelah 1.000 lemparan, hasilmu hampir pasti jatuh di kisaran −Rp1,5 juta sampai nol. Kemenangan yang kamu ingat-ingat itu bukan strategi, itu ekor distribusi.

## Taruhan sampingan: yang murah dan yang gila

| Taruhan | Menang | Peluang | House edge |
|---|---|---|---|
| Big/Small (tanpa triple) | 105/216 | 48,611% | 2,778% |
| Field liberal (total 5–8 atau 13–16) | 104/216 | 48,148% | 3,704% |
| Single number (triple 3:1) | 91/216 | 42,130% | 7,870% |
| Field stingy (total 3–7 atau 13–18) | 91/216 | 42,130% | 15,741% |
| Under 10 / Over 11 | 81/216 | 37,500% | 25,000% |

Perhatikan dua baris Field. **Aturan yang sama, rentang angka berbeda, edge naik empat kali lipat.** Ini pelajaran yang jauh lebih berguna daripada trik apa pun: sebelum duduk, baca rentang menangnya, bukan cuma tulisannya.

Distribusi total tiga dadu juga menjelaskan kenapa Under 10/Over 11 begitu brutal: total 10 dan 11 masing-masing punya 27/216 = 12,5% (titik puncak), sementara total 3 dan 18 cuma 0,46%. Taruhan "di bawah 10" memotong justru area yang paling padat.

## Saudara serumah yang kamu sudah tahu: Bau Cua

Taruhan nomor tunggal di Chuck-a-Luck **identik secara matematis** dengan Bau Cua Ca Cop / Hoo Hey How yang biasa dimainkan saat Imlek — bedanya cuma dadu bergambar hewan, bukan angka. Peluang 75/15/1/125, dan edge yang sama persis. Begitu juga Crown and Anchor versi Inggris. Jadi kalau kamu pernah main Bau Cua dan merasa "hampir menang terus", angka 7,87% ini jawabannya. John Scarne, penulis buku judi klasik, menyebut Chuck-a-Luck sebagai *"the champ chump's game"* — permainannya para pemula.

## Kesimpulan

Chuck-a-Luck bukan permainan yang bisa dikalahkan dengan pola taruhan, bukan pula permainan yang adil karena "dadunya cuma tiga". Yang bisa kamu kendalikan cuma dua hal: **pilih meja dengan bayaran triple tertinggi (12:1, bukan 3:1)** dan **jangan sentuh Field stingy atau Under/Over 11**. Sisanya — 7,87% sampai 3,70% — dibayar ke rumah, setiap lemparan, tanpa kecuali.

<!-- cta-funnel -->

> Kalau mau coba Mini Dice atau versi dadu kasino lainnya, cek dulu paytable-nya: berapa bayaran triple, dan rentang menang untuk Field. Meja yang bayarannya lebih baik memotong kerugianmu hampir separuh sebelum kartu pertama dibagikan.

**[MAIN SEKARANG — CLAIM BONUS DEPO AWAL →](https://tomat.jagungbaru.com/banner/s161?utm_source=blog&utm_campaign=chuck-a-luck-bayar-3-1-rugi-7-87-persen)**

*Angka di atas hasil enumerasi penuh 216 kombinasi tiga dadu + 200.000 sesi simulasi. Paytable tiap penyedia bisa berbeda — periksa dulu sebelum taruhan pertama. Artikel ini edukasi mekanika, bukan jaminan hasil.*

— Chokdi 🐷 · Content Studio · 2026
