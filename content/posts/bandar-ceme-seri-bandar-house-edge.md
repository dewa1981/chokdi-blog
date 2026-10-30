---
title: "Bandar Ceme: House Edge 10,18% yang Lahir dari Satu Aturan Seri"
date: 2026-10-30T18:10:00+07:00
draft: false
tags: ["Kasino", "Ceme", "Domino", "Matematika Taruhan", "House Edge"]
---

# Bandar Ceme: House Edge 10,18% yang Lahir dari Satu Aturan Seri

Ceme kelihatan seperti permainan paling adil di meja online. Cuma 28 kartu, dua kartu per orang, nilai 0–9, tidak ada kartu "tinggi" macam blackjack dan tidak ada roda berputar. Nilai tangannya pun hampir rata di 10% untuk setiap angka — kelihatan seperti undian yang bersih.

Saya enumerasi seluruh kemungkinan: 378 tangan unik, lalu 122.850 kombinasi bandar melawan pemain. Hasilnya satu baris yang menjelaskan semuanya — **pemain menang 44,9076%, kalah 44,9076%, seri 10,1848%**. Karena seri dihitung milik bandar, house edge-nya persis **10,1848%**. Bukan 2%, bukan 5%. Sepuluh koma dua persen, di setiap tangan, tanpa kecuali.

## Mejanya cuma 28 kartu, 2 sampai 7 orang

Satu set domino double-six berisi 28 kartu (semua pasangan angka 0–6, termasuk balak), dimainkan 2 sampai 7 orang, satu orang jadi bandar, sisanya pemain biasa — masing-masing dapat 2 kartu. Nilai tangan = total pipa dua kartu, diambil angka terakhirnya (mod 10). Dua kartu 5-4 dan 3-2 = 14 pipa → nilai 4.

Yang penting dipahami: **tidak ada kartu yang "lebih besar" secara fisik**. Semua kekuatan cuma dari hasil penjumlahan. Karena itu distribusinya nyaris rata, dan justru di situ jebakannya.

## Distribusi nilai: hampir sempurna rata

Dari 378 tangan unik yang bisa dibentuk:

| Nilai | Jumlah tangan | Peluang |
|---|---|---|
| 0 | 37 | 9,79% |
| 1 | 39 | 10,32% |
| 2 | 38 | 10,05% |
| 3 | 39 | 10,32% |
| 4 | 37 | 9,79% |
| 5 | 38 | 10,05% |
| 6 | 37 | 9,79% |
| 7 | 38 | 10,05% |
| 8 | 37 | 9,79% |
| 9 | 38 | 10,05% |

Rata-rata nilai tangan = **4,4868**. Tidak ada angka yang lebih sering muncul secara berarti — beda terbesar cuma 0,53 poin persen (nilai 1 dan 3 vs nilai 0, 4, 6, 8). Artinya semua strategi "pilih meja yang sering keluar 9" itu omong kosong. Distribusinya seragam.

## 122.850 kombinasi: bandar vs pemain

Karena bandar dan pemain mengambil dari set yang sama, tangan mereka tidak independen — kalau bandar pegang balak enam, kartu itu hilang dari dek. Enumerasi penuh (378 × 325 pasangan yang tidak berbagi kartu) memberi:

| Hasil | Kombinasi | Peluang |
|---|---|---|
| Pemain menang | 55.169 | 44,9076% |
| Seri | 12.512 | 10,1848% |
| Pemain kalah | 55.169 | 44,9076% |
| **Total** | **122.850** | **100%** |

Lihat angkanya: menang dan kalah **persis sama** — 55.169 banding 55.169. Ini bukan kebetulan, ini konsekuensi dari dek yang simetris. Bandar dan pemain punya distribusi yang identik; yang membedakan mereka hanya satu hal, yaitu apa yang terjadi saat nilainya sama.

## Tanpa aturan seri, EV-nya nol

Ini bagian yang paling perlu kamu tahu. Kalau seri diperlakukan sebagai **push** (taruhan kembali), EV pemain = (55.169 − 55.169) / 122.850 = **0,0000%**. Permainan yang benar-benar adil, tanpa edge sama sekali.

Tapi di bandar ceme, seri = **bandar menang**. Maka EV-nya jadi (55.169 − 55.169 − 12.512) / 122.850 = **−10,1848%**.

Jadi seluruh keuntungan bandar bukan dari "kartu bandar lebih bagus", bukan dari pengocokan, bukan dari RTP yang diatur. Semuanya dari satu baris aturan: **nilai sama, bandar menang**. Kalau kamu paham ini, kamu paham 100% matematika meja ceme.

## Kartu terbaik pun tetap kalah 10,25% dari waktu

Peluang menang menurut nilai kartu sendiri (dihitung persis, bukan ditebak):

| Nilai kartu kamu | Peluang menang |
|---|---|
| 0 | 0,0000% |
| 1 | 9,7751% |
| 2 | 20,0324% |
| 3 | 30,0828% |
| 4 | 40,3493% |
| 5 | 50,1619% |
| 6 | 60,2328% |
| 7 | 70,0081% |
| 8 | 80,0249% |
| 9 | 89,7490% |

Perhatikan nilai 9 — kartu terbaik yang mungkin. Menangnya cuma **89,7490%**, bukan 100%. Sisa 10,251% adalah seri melawan bandar yang juga dapat 9, dan seri itu **kalah**. Dua-duanya dapat 9 terjadi 1.266 kali dari 122.850 = **1,0305%**. Jadi momen "sial, sama-sama sembilan" itu bukan mitos — itu 1 dari 97 tangan, dan selalu kamu yang bayar.

Sebaliknya nilai 0: peluang menang benar-benar **nol**. Bukan kecil, nol. Tidak ada nilai di bawah 0.

## Kalau kamu yang jadi bandar

Kebalikan dari EV pemain: **+10,1848% per tangan pemain**. Bandar yang menghadapi 6 pemain, masing-masing taruh Rp100.000, secara rata-rata mengantongi **Rp61.109 per ronde** — bukan karena hoki, tapi karena 6 × 10,18% dari Rp100.000.

Tapi jadi bandar bukan jalan pintas. Bandar menanggung semua hasil sekaligus: satu ronde bisa kalah ke 6 orang bersamaan (Rp600.000), sementara pendapatannya rata-rata cuma Rp61.109 per ronde. Butuh modal besar untuk menahan ayunan itu, dan modal itu yang bikin banyak orang gagal jadi bandar jauh sebelum edge-nya bekerja. Edge positif tanpa bankroll cukup = bangkrut lebih dulu.

## Berapa tangan sampai edge-nya kelihatan

Simulasi normal (rata-rata −0,10185 unit per tangan, simpangan baku 0,9948):

| Jumlah tangan | EV | Simpangan | Peluang masih untung |
|---|---|---|---|
| 10 | −1,02 unit | 3,15 | 37,31% |
| 50 | −5,09 unit | 7,03 | 23,46% |
| 100 | −10,19 unit | 9,95 | 15,30% |
| 1.000 | −101,85 unit | 31,46 | 0,06% |

Dengan taruhan Rp100.000: 100 tangan → rata-rata rugi **Rp1.018.478** (masih ada 15,30% kemungkinan untung, jadi wajar kalau kamu merasa "menang"). 1.000 tangan → rata-rata rugi **Rp10.184.778**, dan peluang masih untung tinggal **0,06%**.

Ini yang bikin ceme terasa "bisa dimenangkan": di 10 tangan pertama, 37,31% orang memang pulang bawa profit. Tapi itu bukan skill — itu variansi. Peluang seri muncul minimal sekali dalam 10 tangan = **65,84%**, jadi hampir tiap sesi pendek kamu sudah ketemu aturan yang makan uangmu.

## Kartu spesial tidak menutup edge

Banyak aplikasi menambahkan bayaran khusus: kartu 6-6 dibayar 4x, twin 3x, nilai 9 dibayar 2x. Ini **bonus tambahan**, bukan kompensasi edge. Kalau "6-6" diartikan dua kartu yang masing-masing bernilai 6, peluangnya hanya **6 dari 378 = 1,5873%** — dan itu bonus yang dibayar bandar untuk kejadian langka, bukan pengurang 10,18% yang kamu bayar tiap tangan.

Jangan pernah menghitung bonus sebagai "modal balik". Bonus dibayar dari frekuensi yang sangat kecil, sementara edge diambil dari setiap tangan.

## Empat jebakan yang paling mahal

1. **Menganggap seri = uang kembali.** Tidak. Seri adalah kalah penuh. Ini satu-satunya sumber edge, dan menyangkanya push bikin kamu salah hitung total.
2. **Mengira nilai 0 itu netral.** Peluang menangnya nol — bukan 10%. Nilai 0 cuma menang kalau bandar juga 0, dan itu pun disebut seri alias kalah.
3. **Main panjang "biar balik modal".** Setiap tangan adalah taruhan baru dengan edge −10,18%. Memperpanjang sesi cuma memperbesar kerugian yang diharapkan, bukan memperkecil.
4. **Jadi bandar tanpa modal.** Edge +10,18% per tangan, tapi satu ronde bisa kalah ke semua pemain sekaligus. Tanpa bankroll, edge tidak pernah sempat bekerja.

Kalau mau membandingkan angka ini dengan meja lain, saya sudah membedah [baccarat banker vs player](/posts/baccarat-banker-vs-player-house-edge/) (edge 1,06%, lahir dari komisi), [sicbo 216 kombinasi](/posts/sicbo-216-kombinasi-house-edge/) (dari −2,78% sampai −47%), [craps pass line vs any 7](/posts/craps-house-edge-pass-line-vs-any-7/) (1,41% vs 16,67%), [dragon tiger](/posts/dragon-tiger-satu-kartu-tiga-aturan/) dan [roulette house edge](/posts/roulette-house-edge-martingale/). Pola yang sama muncul di semua meja: edge bukan dari keberuntungan lawan, tapi dari satu aturan kecil yang jarang dibaca. Kalau kamu serius mengatur ukuran taruhan, baca juga [kelly criterion](/posts/kelly-criterion-ukuran-taruhan-bankroll/) — di permainan dengan EV negatif, ukuran taruhan optimalnya nol.

**Ringkasnya:** ceme bukan permainan yang mengocok ulang nasib tiap tangan. Ia permainan dengan satu angka tetap — 10,18% untuk bandar, −10,18% untuk pemain — yang cuma disembunyikan oleh aturan seri yang kelihatan sepele.

<!-- cta-funnel -->
> **Mau lihat sendiri meja ceme dan bandar qiu-nya, dengan aturan seri yang ditulis terang?** VIP579 punya ceme, bandar qiu, domino, baccarat, roulette, sampai sicbo live — semua aturan meja terbuka, bukan disembunyikan di balik "syarat & ketentuan".
>
> 👉 **[GASPOL MASUK MEJA VIP SEKARANG](https://tomat.jagungbaru.com/banner/vip?utm_source=blog&utm_campaign=bandar-ceme-seri-bandar-house-edge)** — deposit 24 jam, WD cepat, bonus rollingan harian.
<!-- /cta-funnel -->

— Chokdi 🐷 · Content Studio · 2026
