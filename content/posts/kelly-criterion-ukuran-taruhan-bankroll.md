---
title: "Kelly Criterion: Rumus Ukuran Taruhan yang di Kasino Menjawab Nol"
date: 2026-10-28T00:11:00+07:00
draft: false
tags: ["Kasino", "Manajemen Bankroll", "Peluang", "Kelly Criterion"]
---

Semua orang sibuk mencari apa yang mau dipasang. Hampir tidak ada yang menghitung **berapa besar** yang pantas dipasang. Padahal dua pertanyaan itu bobotnya sama: menebak pemenang dengan benar tapi memasang 40% modal sekali kalah bisa menghapus keunggulan berbulan-bulan. Kelly criterion — rumus dari Bell Labs tahun 1956 — menjawab pertanyaan kedua, dan jawabannya untuk sebagian besar meja kasino justru **nol**.

## Siapa Kelly dan apa yang dia maksimalkan

John Larry Kelly Jr., peneliti Bell Labs, mempublikasikan criterion ini pada 1956. Yang dimaksimalkan bukan rata-rata keuntungan, tapi **logaritma kekayaan** — dalam praktik sama dengan memaksimalkan laju pertumbuhan majemuk jangka panjang. Perbedaan "rata-rata" vs "log" inilah inti seluruh artikel: rata-rata bisa didongkrak taruhan raksasa, pertumbuhan tidak.

Untuk taruhan yang hasilnya cuma menang atau kalah, rumusnya satu baris:

**f\* = (b × p − q) / b**

dengan `p` peluang menang, `q = 1 − p`, dan `b` keuntungan bersih per unit taruhan (odds desimal minus 1).

| Skenario | p | b | f\* |
|---|---|---|---|
| Lempar koin adil | 50,00% | 1,00 | 0,00% |
| Koin yang bias 55% | 55,00% | 1,00 | **10,00%** |
| Odds 1,90, tebakan 55% | 55,00% | 0,90 | **5,00%** |
| Odds 1,90, tebakan 53% | 53,00% | 0,90 | 0,78% |
| Odds 1,90, peluang asli 50% | 50,00% | 0,90 | **−5,56%** |
| Roulette Eropa merah/hitam | 48,65% | 1,00 | **−2,70%** |

## Satu angka, dua arti

Perhatikan baris pertama dan terakhir. Pada taruhan bayaran 1:1, Kelly runtuh jadi `f* = 2p − 1` — yang persis sama dengan nilai ekspektasi per unit. Artinya di taruhan 1:1, **ukuran taruhan optimal dan house edge adalah angka yang sama**, cuma beda tanda. Untuk roulette Eropa, f\* = −2,70%: tidak ada taruhan optimal, karena setiap rupiah yang dipasang menambah kerugian ekspektasi. Di [meja roulette](/posts/roulette-house-edge-martingale/) angka ini tidak berubah oleh pola taruhan apa pun.

Karena itu untuk permainan bertepi negatif, Kelly bukan alat menang — dia alat diagnosis. Selama `b × p < q`, jawabannya negatif, dan tindakan yang benar adalah **tidak bertaruh**. Bandingkan dengan [baccarat banker vs player](/posts/baccarat-banker-vs-player-house-edge/) dan [blackjack basic strategy](/posts/blackjack-basic-strategy-ev-per-kartu/): keduanya cuma menggeser tepi rumah dari 1,06%–0,5%, bukan membalikkannya.

## Rumus ini menghukum kesalahan taksir

Bagian paling tidak nyaman: `p` di rumus itu bukan kebenaran, tapi **tebakanmu**. Umpan baliknya brutal. Kalau kamu menaksir peluang 55% di odds 1,90 lalu memasang 5% modal, hasilnya positif **0,1127% per taruhan**. Tapi kalau peluang sebenarnya cuma 53%, angka itu berubah jadi **−0,0779% per taruhan** — bukan lebih kecil, tapi sudah rugi. Kalau aslinya 52%: −0,1732%. Kalau aslinya 50%: −0,3638%.

Sebabnya, taksiran 55% menghasilkan taruhan 6,4 kali lebih besar dari f\* yang benar (5,00% vs 0,78%). Di atas 2× f\*, pertumbuhan berbalik negatif. Inilah alasan pemain profesional memakai **fractional Kelly**, dan simulator Monte Carlo mengonfirmasi: ketidakpastian pada `p` menurunkan ukuran optimal (σ 5% menurunkan f\* dari 0,40 ke 0,38; σ 20% ke 0,36).

## Setengah Kelly: 75% pertumbuhan, 33% lebih lambat

| f | Pertumbuhan per taruhan | Relatif ke full Kelly | Taruhan sampai modal 2× |
|---|---|---|---|
| 2,50% (quarter) | +0,2188% | 43,7% | 316,8 |
| 5,00% (half) | +0,3753% | **74,9%** | 184,7 |
| 10,00% (full) | +0,5008% | 100% | 138,4 |
| 20,00% (2× Kelly) | **−0,0138%** | −2,7% | tak pernah |

Setengah taruhan cuma kehilangan seperempat pertumbuhan, dan itu sudah hasil hitungan, bukan perasaan. Sementara 2× Kelly praktis berhenti tumbuh: −0,0138% per taruhan. Di atas itu, makin besar taruhan makin cepat bangkrut — bukan makin cepat kaya.

## Kenapa rata-rata menipu: 5.000 jalur, 500 taruhan

Simulasi 5.000 jalur × 500 taruhan, peluang menang 55% di bayaran 1:1, modal awal Rp1.000:

| f | Median akhir | Persentil 10 | Persentil 90 | Jalur rugi | Drawdown ≥50% | Bangkrut |
|---|---|---|---|---|---|---|
| 5,00% | 6.529 | 1.608 | 26.509 | 4,80% | 59,74% | 0,00% |
| 10,00% | 12.234 | 737 | 203.075 | 13,00% | 99,90% | 0,00% |
| 20,00% | 933 | 0 | 272.501 | 52,90% | 100% | 13,14% |
| 30,00% | 0 | 0 | 1.759 | 89,96% | 100% | 72,68% |

Lihat baris 20%: persentil 90 mencapai 272.501 — inilah yang bikin orang percaya taruhan besar brilian — tapi median-nya **933**, artinya lebih dari separuh jalur justru rugi setelah 500 taruhan, dan 13,14% habis total. Nilai ekspektasi aritmetika malah makin gila: di f = 10% hasilnya 144,8× modal, di f = 30% jadi 2,6 juta× modal, dan di f = 100% (all-in) mencapai 4,97 × 10²⁰ kali modal — padahal peluangnya bertahan sampai taruhan ke-500 adalah nol, karena satu kalah saja di all-in langsung menghabiskan modal. Rata-rata dibentuk oleh jalur yang nyaris mustahil; median yang kamu alami.

Cek silangnya rapi: `exp(500 × 0,5008%)` = 12,2 kali, median simulasi 12.234 dari modal 1.000 — cocok. Pertumbuhan logaritmik memang meramal median, bukan rata-rata.

## Aturan praktis

- Hitung `f*` dulu; kalau negatif, **jangan bertaruh** — tidak ada ukuran yang benar untuk taruhan bertepi negatif.
- Pakai **quarter sampai half Kelly** (2,5%–5% modal untuk tepi tipis), sisakan ruang untuk salah taksir.
- Jangan pernah melewati **2× f\***: di titik itu pertumbuhan nol.
- Ingat [konversi odds desimal/Malay/Indo/HK](/posts/format-odds-desimal-malay-indo-hk/) sebelum menghitung `b` — salah format odds membuat `f*` salah 100%.
- Untuk pasar gol, garis seperti [over/under 2,5](/posts/over-under-total-gol-garis-2-5-push/) punya push yang mengubah `p` efektif; hitung ulang, jangan pakai angka mentah.

## Kesimpulan

Kelly criterion bukan mesin uang. Dia timbangan: memberi tahu berapa besar taruhan yang membuat pertumbuhan majemuk maksimal **kalau** keunggulanmu nyata, dan dengan tegas menyebut nol kalau keunggulan itu tidak ada. Justru karena itu rumus ini berguna di kasino — dia menghitung sendiri bahwa tepi rumah 2,70% berarti taruhan optimalnya negatif 2,70%.

<!-- cta-funnel -->
> Sudah paham angkanya? Sekarang pilih mejanya: **[klaim akses meja VIP dan hitung sendiri ukuran taruhanmu →](https://tomat.jagungbaru.com/banner/vip?utm_source=blog&utm_campaign=kelly-criterion-ukuran-taruhan-bankroll)** — pasang kecil, main panjang.

Sumber: [Kelly criterion (Wikipedia)](https://en.wikipedia.org/wiki/Kelly_criterion) · [Why fractional Kelly? — simulasi Monte Carlo](https://matthewdowney.github.io/uncertainty-kelly-criterion-optimal-bet-size.html) · semua angka payout, growth rate, dan simulasi di artikel ini dihitung ulang secara lokal (awk + 5.000 jalur × 500 taruhan, seed tetap).

— Chokdi 🐷 · Content Studio · 2026
