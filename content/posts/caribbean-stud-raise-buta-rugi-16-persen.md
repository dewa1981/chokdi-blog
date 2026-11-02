---
title: "Caribbean Stud: Raise Buta Rugi 16,61% — Padahal Dealer Gagal Qualify 43,68%"
date: 2026-11-02T12:20:00+07:00
draft: false
tags: ["Kasino", "Caribbean Stud", "House Edge", "Probabilitas", "Strategi Kartu"]
---

Caribbean Stud cuma punya **satu keputusan per tangan**: lipat, atau tambah taruhan jadi dua kali ante. Terdengar sederhana — sampai angkanya dihitung. Kalau kamu **selalu raise**, kerugianmu **16,611% dari ante per tangan**. Kalau kamu cuma raise saat punya pair ke atas, angkanya jatuh ke **5,455%**. Selisih Rp45.240 per jam pada ante Rp10.000.

Artikel ini menghitung ulang semuanya dari nol: 40 juta tangan simulasi, pencatat tangan yang sudah divalidasi ke seluruh 2.598.960 kombinasi kartu, dan EV eksak per tangan lewat enumerasi penuh 163.185 kemungkinan kartu dealer.

## Aturannya dalam satu paragraf

Ante satu unit. Kamu dan dealer masing-masing dapat 5 kartu, satu kartu dealer dibuka. Setelah lihat kartumu: **fold** (ante hangus) atau **raise tepat 2× ante**. Dealer harus punya **A-K atau lebih baik** untuk qualify. Kalau dealer gagal qualify, ante-mu dibayar 1:1 dan raise-mu push (kembali utuh). Kalau dealer qualify dan kamu menang, ante 1:1 dan raise dibayar sesuai paytable US: royal 100:1, straight flush 50:1, four of a kind 20:1, full house 7:1, flush 5:1, straight 4:1, three of a kind 3:1, two pair 2:1, sisanya 1:1. Kalau dealer menang, ante **dan** raise hilang — total −3 unit. Seri = push.

## Ruang sampelnya pas

Total kemungkinan = 2.598.960 tangan pemain × 1.533.939 tangan dealer dari 47 kartu sisa × 5 posisi kartu up = **19.933.230.517.200**. Angka itu sama persis dengan yang dipakai tabel publik — jadi tidak ada kombinasi yang hilang atau dihitung dua kali.

Sebelum dipakai, pencatat tangan saya uji dulu ke **seluruh 2.598.960 kombinasi** 5 kartu: high card 1.302.540 · pair 1.098.240 · two pair 123.552 · trips 54.912 · straight 10.200 · flush 5.108 · full house 3.744 · quads 624 · straight flush 36 · royal 4. Sepuluh kategori, sepuluh cocok. Baru setelah itu simulasinya dipercaya.

## Empat strategi, satu meja

Simulasi 40 juta tangan, paytable US, raise 2× ante:

| Strategi | House edge | Element of risk | Rata-rata taruhan | Publikasi |
|---|---|---|---|---|
| Raise semua (blind) | **16,611%** | 5,537% | 3,000 | 16,607% · 5,536% |
| Raise pair ke atas | **5,455%** | 2,731% | 1,998 | 5,470% · 2,738% |
| Raise A-K-J-8-3 ke atas | **5,301%** | 2,588% | 2,048 | 5,316% · 2,596% |
| Raise semua A-K | **5,669%** | 2,666% | 2,127 | 5,682% · 2,672% |
| Optimal (referensi) | 5,224% | 2,555% | 2,045 | 5,224% · 2,555% |

Selisih saya dengan angka publikasi maksimal **0,015 poin persen** — sisa derau simulasi, bukan perbedaan model. Perhatikan yang aneh: raise **semua** tangan A-K (56,3% tangan) ternyata **lebih buruk** daripada cuma raise pair (49,9% tangan). Menambah taruhan ke tangan marginal itu bukan cuma tidak membantu, tapi merugikan.

## Kenapa edge-nya tidak sebesar kelihatannya

Dua fakta yang menjelaskan seluruh matematika game ini:

1. **Dealer gagal qualify 43,675%** — jadi qualify 56,325%. Di 43,675% tangan itu kamu dapat +1 tanpa peduli kartumu. Ini "subsidi" yang membuat raise buta tidak jadi bencana total.
2. **Perbandingan tangan murni hampir koin seimbang**: tanganmu mengalahkan tangan dealer **49,994%**, seri 0,008%, sisanya kalah. Tanpa kartu up dan tanpa hak fold, tidak ada pemain yang punya keunggulan informasi.

Jadi semua edge pemain datang dari satu hal: **boleh tidak memasang taruhan saat kartunya jelek**. Itu sebabnya house edge 16,61% bisa dipotong jadi 5,2% — bukan karena strategi ajaib, tapi karena kamu berhenti membayar untuk tangan sampah.

## EV per kategori tangan (kalau tetap raise)

| Tanganmu | Frekuensi | EV raise (unit) |
|---|---|---|
| High card | 50,11% | **−1,2226** |
| Pair | 42,26% | +0,3953 |
| Two pair | 4,76% | +2,8397 |
| Three of a kind | 2,11% | +4,2692 |
| Straight | 0,39% | +5,4464 |
| Flush | 0,20% | +6,5674 |
| Full house | 0,14% | +9,0870 |
| Four of a kind | 0,024% | +24,7405 |
| Straight flush | 0,0014% | +56,3792 |
| Royal flush | 0,0001% | +95,92 |

Setengah dek tangan yang kamu terima (high card) EV-nya **−1,22** — lebih buruk daripada fold yang cuma −1,00. Di situlah uangmu bocor kalau kamu raise membabi buta.

## Batas raise: dihitung eksak, bukan dikira

Untuk tangan A-K yang bikin bingung, EV-nya saya enumerasi penuh: 4 kartu dealer dari 46 kartu sisa = 163.185 kombinasi, kartu up sudah diketahui. Aturannya sederhana: **raise kalau EV > −1**, karena fold = −1.

| Tanganmu | Kartu up | EV raise | Keputusan |
|---|---|---|---|
| 2♠2♦ 9♥5♣3♠ | 2 | −0,475 | raise |
| 2♠2♦ 9♥5♣3♠ | J | −0,960 | raise (mepet) |
| 9♠9♦ 5♥3♣2♠ | J | −0,107 | raise |
| A♠K♦ Q♥J♣9♠ | 2 | −0,972 | raise |
| A♠K♦ Q♥J♣9♠ | K | −0,532 | raise |
| A♠K♦ J♥8♣3♠ | 3 | **−0,835** | raise |
| A♠K♦ J♥8♣3♠ | Q | **−1,171** | **fold** |
| A♠K♦ J♥8♣2♠ | 3 | −1,030 | fold |
| A♠K♦ J♥8♣2♠ | 8 | −0,866 | raise |
| A♠K♦ 8♥5♣2♠ | 2 | −0,929 | raise |
| A♠K♦ 8♥5♣2♠ | 8 | −1,185 | fold |
| A♠K♦ Q♥J♣10♠ | 2 | +5,300 | raise (straight) |

Pola yang muncul: A-K dengan kicker tinggi layak di-raise, dan **kartu up yang cocok dengan kartu di tanganmu menaikkan EV** — karena kartu itu tidak bisa dipakai dealer untuk membentuk pair. A-K-J-8-3 vs up 3 = raise; A-K-J-8-3 vs up Q = fold. Tangan yang sama, keputusan berbeda. Persis seperti tiga aturan strategi publik, dan sekarang kamu tahu angkanya, bukan cuma hafalannya.

## Terjemahan ke uang

Ante Rp10.000, 40 tangan per jam:

- **Raise semua**: −Rp1.661/tangan = **−Rp66.444/jam** (uang yang berputar Rp1,2 juta)
- **Raise pair ke atas**: −Rp546/tangan = **−Rp21.820/jam**
- **Raise A-K-J-8-3 ke atas**: −Rp530/tangan = **−Rp21.204/jam**

Selisih strategi terburuk dan strategi wajar: **Rp45.240 per jam**. Dalam sesi 4 jam, Rp181.000 — hilang bukan karena kartu, tapi karena satu kebiasaan: raise tanpa melihat batas EV.

Catatan: side bet progresif adalah taruhan terpisah dengan edge sendiri, dan **tidak** mengubah keputusan raise/fold. Jangan campur dua hitungan.

Cross-check angka: Wizard of Odds (paytable US, tabel return 19.933.230.517.200 kombinasi, house edge 5,224%, element of risk 2,555%) dan PokerCoaching (raise wajib tepat 2× ante, dealer qualify A-K, side bet progresif terpisah).

<!-- cta-funnel -->

> Kalau mau main Caribbean Stud, cek dua hal di meja sebelum duduk: paytable-nya US atau bukan, dan berapa batas bayar maksimumnya. Full house yang dibayar 7:1 di atas kertas bisa jadi jauh lebih kecil kalau meja pakai paytable Eropa.

**[MAIN SEKARANG — AMBIL BONUS DEPO AWAL →](https://tomat.jagungbaru.com/banner/vip?utm_source=blog&utm_campaign=caribbean-stud-raise-buta-rugi-16-persen)**

*Tabel bayaran tiap penyedia berbeda — periksa paytable sebelum taruhan pertama. Artikel ini edukasi mekanika, bukan jaminan hasil.*

— Chokdi 🐷 · Content Studio · 2026
