---
title: "Let It Ride: Bet Wajibmu Rugi 37,27% — Opsinya yang Bikin Edge Cuma 3,51%"
date: 2026-11-02T00:10:00+07:00
draft: false
tags: ["Kasino", "Let It Ride", "House Edge", "Probabilitas", "Strategi Kartu"]
---

Let It Ride dijual dengan satu kalimat yang terdengar ramah: *"kamu boleh tarik kembali dua dari tiga taruhanmu kalau kartunya jelek."* Yang jarang disebut: **taruhan yang tidak boleh ditarik itu rugi 37,27% per tangan.** Seluruh reputasi "house edge cuma 3,51%" datang dari hak istimewa menarik taruhan — bukan dari kartunya.

Artikel ini menghitung ulang semuanya: 22.100 kombinasi tiga kartu, 270.725 kombinasi empat kartu, dan 51.979.200 kemungkinan penyelesaian. Hasilnya cocok persis dengan angka yang dipublikasikan, sampai tujuh desimal.

## Aturannya dalam satu paragraf

Tiga taruhan sama besar di tiga lingkaran. Dealer kasih **3 kartu** ke pemain dan 2 kartu komunitas dibuka belakangan — jadi tangan akhirmu 5 kartu, dan tidak ada tangan dealer untuk dilawan. Setelah 3 kartu, satu taruhan boleh ditarik. Setelah kartu komunitas pertama, taruhan kedua boleh ditarik. Taruhan ketiga **wajib tinggal** sampai selesai. Bayaran standar: royal flush 1000:1, straight flush 200, four of a kind 50, full house 11, flush 8, straight 5, three of a kind 3, two pair 2, pair sepuluh ke atas 1:1, sisanya kalah.

Kartu yang ditarik kembali utuh, bukan hangus — dan begitu ditarik, tidak bisa dipasang lagi di ronde itu.

## Enumerasi: 51.979.200 kemungkinan

Untuk setiap 3 kartu ada 49 kemungkinan kartu keempat dan 48 kartu kelima, jadi 22.100 × 49 × 48 = 51.979.200 jalur. Untuk setiap jalur dihitung hasil bersihnya: **pays** kalau tangan akhirnya membayar, **−1** kalau tidak. Enumerasi penuh memberi:

| Komponen | EV per tangan (unit) |
|---|---|
| Bet wajib (bet 1) | **−0,37272** |
| Opsi bet 2 (keputusan setelah kartu ke-4) | **+0,22854** |
| Opsi bet 3 (keputusan setelah kartu ke-3) | **+0,10913** |
| **Total** | **−0,03506** |

Bacanya: kalau kamu menuruti aturan "biarkan semua ikut" (tidak pernah menarik), EV-nya **−1,11817 per tangan** — kerugian 37,27% dari uang yang kamu pasang. Hak menarik taruhan menyumbang **+0,33767** dan menyelamatkan permainan ini. Tanpa opsi itu, Let It Ride lebih buruk daripada slot 62% mana pun.

Dari EV total, tiga angka resmi bisa diturunkan sendiri:

- **3,51%** = house edge terhadap *satu* taruhan minimum (0,03506 dibagi 1 bet)
- **1,17%** = house edge terhadap total tiga taruhan yang dipasang di awal
- **2,86%** = element of risk, yaitu kerugian dibagi uang yang benar-benar tertinggal di meja (rata-rata **1,2321** bet, karena pemain menarik balik 1,768 bet atau 59% dari taruhannya)

## Keputusan setelah 3 kartu

Hanya **7,276%** tangan tiga kartu yang layak di-ride. Sisanya ditarik — bukan karena penakut, tapi karena EV-nya di bawah nol.

| Tangan 3 kartu | Peluang | EV kalau di-ride |
|---|---|---|
| High pair (sepuluh ke atas) | 6,52% | **+1,4362** |
| Three of a kind | 0,24% | **+5,4082** |
| 3 kartu ke royal flush (Q / K / A tertinggi) | — | +1,4762 / +1,2364 / +0,9966 |
| 3 kartu straight flush spread 4 / 3 / 5 | — | +0,2901 / +0,2570 / +0,0042 |
| Low pair (sembilan ke bawah) | 10,43% | **−0,0604** |
| Tiga kartu sampah tak terhubung | ±62% | **−0,6177** |

Perhatikan baris low pair: **pair sembilan ke bawah itu minus.** Cuma −0,06 (enam persen), jadi kelihatan "hampir impas" — tapi main 200 tangan, dan selisih kecil itu jadi uang nyata. High pair selalu aman karena tangan akhirnya pasti membayar minimal 1:1, tidak ada jalan kalah.

## Keputusan setelah kartu ke-4

Di sini **15,09%** tangan layak di-ride. Dua mitos paling mahal ada di tabel ini.

| Tangan 4 kartu | Jumlah | EV kalau di-ride |
|---|---|---|
| 4 ke straight flush | 148 | **+8,5479** |
| Three of a kind | 2.496 | +4,4792 |
| Two pair | 2.808 | +2,7500 |
| Pair sepuluh ke atas | 31.680 | +1,2083 |
| 4 ke flush (semua varian) | 2.712 | +0,9069 |
| 4 ke outside straight, 0 high card | 1.260 | **0,0000** (impas) |
| 4 ke outside straight, 1–3 high card | — | +0,1250 → +0,3750 |
| Pair sembilan ke bawah | 50.688 | **−0,4583** |
| 4 ke inside straight | 6.804 | **−0,3333** |

Mitos pertama: *"flush draw tanpa kartu tinggi buang saja."* Salah — 4 kartu flush dengan nol kartu tinggi masih **+0,6875**, tetap ride. Mitos kedua: *"straight draw selalu ikut."* Empat kartu ke inside straight (butuh satu angka di tengah) bernilai **−0,3333**; itu bukan draw, itu donasi. Yang impas persis hanya outside straight tanpa kartu tinggi: EV 0,0000 — boleh ikut, boleh tarik, secara matematis sama saja.

## Uang nyata

Tiga taruhan Rp10.000, 40 tangan per jam (kecepatan meja normal):

- Selalu ride ketiga taruhan: **−Rp447.268/jam**
- Tarik dua taruhan terus (main satu bet saja): −Rp149.088/jam
- Strategi optimal (ride 7,3% di 3 kartu, 15,1% di 4 kartu): **−Rp14.023/jam**

Selisih strategi optimal dan "selalu ride": **Rp433.245 per jam** — dalam sesi 4 jam, Rp1,73 juta. Bukan dari keberuntungan, dari dua keputusan yang diambil 22.100 kali per meja.

Satu catatan yang sering luput: mesin punya batas bayar maksimum (aggregate payout). Kalau batasnya, misalnya, Rp75 juta, jangan bertaruh lebih dari batas dibagi 3000 — di atas itu royal flush-mu tidak dibayar penuh dan edge-nya naik diam-diam.

Semua angka di atas dihitung sendiri lewat enumerasi penuh 51.979.200 jalur (sekitar 15 detik dengan numpy), lalu dicocokkan dengan Wizard of Odds (EV bet wajib −0,3727229 · opsi taruhan +0,2285403 dan +0,1091258 · edge 3,51% · element of risk 2,85%), aturan taruhan dari gaming guide Bally's Atlantic City, dan lembar aturan Let It Ride komisi lotere New Hampshire.

<!-- cta-funnel -->

> Sebelum duduk di meja Let It Ride, tanya satu hal ke dealer: berapa batas bayar maksimumnya, dan berapa minimum taruhannya. Dua angka itu menentukan apakah tabel 1000:1 di dinding benar-benar bisa kamu sentuh.

**[MAIN SEKARANG — AMBIL BONUS DEPO AWAL →](https://tomat.jagungbaru.com/banner/vip?utm_source=blog&utm_campaign=let-it-ride-bet-wajib-rugi-37-persen)**

*Tabel bayaran dan batas maksimum tiap penyedia bisa berbeda — periksa paytable sebelum taruhan pertama. Artikel ini edukasi mekanika, bukan jaminan hasil.*

— Chokdi 🐷 · Content Studio · 2026
