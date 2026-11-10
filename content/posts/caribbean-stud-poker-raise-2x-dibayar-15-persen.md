---
title: "Caribbean Stud: Naik 2x Cuma Dibayar 15,8% Tangan — House Edge 5,22%"
description: "Caribbean Stud Poker kelihatan seperti poker biasa, padahal 47,8% tangan berakhir fold dan raise 2x hanya dibayar di 15,8% tangan. Ini tabel lengkap 19,9 triliun kombinasi dan house edge 5,22%."
date: 2026-11-11T00:05:00+07:00
draft: false
tags: ["Caribbean Stud", "House Edge", "Poker Casino", "Edukasi Judi", "Matematika Taruhan"]
---

# Caribbean Stud: Naik 2x Cuma Dibayar 15,8% Tangan — House Edge 5,22%

Dari semua permainan kartu di meja kasino, **Caribbean Stud Poker** paling sering dijual sebagai "poker melawan bandar yang gampang dipahami". Aturannya memang sederhana: satu ante, satu kartu bandar terbuka, lalu pilih **fold** atau **raise 2x**. Masalahnya, keputusan sesederhana itu punya konsekuensi yang tidak sederhana — dan angka aslinya jarang ditulis di brosur.

Artikel ini membedah tabel pengembalian (return table) resmi Caribbean Stud: **19.933.230.517.200 kombinasi** kemungkinan, dihitung ulang sendiri dari data Wizard of Odds, bukan dikutip mentah.

## Aturan: Ante, Raise 2x, dan Syarat Kualifikasi Bandar

Satu dek 52 kartu. Kamu dan bandar masing-masing dapat lima kartu; **satu kartu bandar dibuka**, sisanya tertutup. Kamu hanya punya satu keputusan:

- **Fold** — ante hangus, kartu dibuang.
- **Raise** — tambah tepat **2x ante** (jadi total 3 unit di atas meja).

Setelah itu bandar membuka kartunya. Bandar **wajib punya minimal A-K** untuk dianggap *kualifikasi*:

- **Bandar tidak kualifikasi** → ante dibayar 1:1, **raise push** (kembali utuh).
- **Bandar kualifikasi dan kalah** → ante 1:1, raise dibayar sesuai paytable.
- **Bandar kualifikasi dan menang** → ante *dan* raise hilang.
- **Seri** → kedua taruhan push.

Paytable standar AS untuk taruhan raise: royal flush 100:1, straight flush 50:1, four of a kind 20:1, full house 7:1, flush 5:1, straight 4:1, three of a kind 3:1, two pair 2:1, **selain itu 1:1**.

## Tabel Lengkap: Ke Mana Saja Uang 100 Tangan Pergi

Inilah sebaran hasil dengan strategi optimal, per **1 unit ante**:

| Hasil | Probabilitas | Untung/rugi | Kontribusi |
|---|---|---|---|
| Menang, royal flush | 0,0001% | +201 | +0,000169 |
| Menang, straight flush | 0,0008% | +101 | +0,000795 |
| Menang, four of a kind | 0,0142% | +41 | +0,005826 |
| Menang, full house | 0,0834% | +15 | +0,012510 |
| Menang, flush | 0,1097% | +11 | +0,012062 |
| Menang, straight | 0,2198% | +9 | +0,019779 |
| Menang, three of a kind | 1,1751% | +7 | +0,082260 |
| Menang, two pair | 2,4482% | +5 | +0,122412 |
| Menang, pair atau kurang | 11,7555% | +3 | +0,352665 |
| **Bandar tidak kualifikasi** | **22,7385%** | **+1** | **+0,227385** |
| Seri | 0,0016% | 0 | 0 |
| **Fold** | **47,7745%** | **−1** | **−0,477745** |
| **Bandar menang** | **13,6786%** | **−3** | **−0,410359** |
| **Total** | 100% | | **−0,052243** |

Angka terakhir itu yang penting: **−5,2243%**. Artinya setiap Rp 100.000 ante, kerugian rata-rata Rp 5.224 per tangan dengan strategi sempurna. RTP-nya **94,78%** — di bawah baccarat (98,94%), Sic Bo big/small (97,22%), dan Andar Bahar sisi Andar (97,85%). Ini salah satu meja termahal di lantai kasino.

## Fakta #1: 47,8% Tangan Berakhir Fold

Hampir setengah tangan, pemain optimal **membuang kartu sebelum bandar bergerak**. Bukan karena takut — karena matematikanya: dengan tangan di bawah A-K, raise 2x akan lebih sering rugi daripada untung. Yang perlu dicatat, fold itu **kerugian pasti −1 unit**, sedangkan raise punya rentang hasil +201 sampai −3. Fold bukan "aman", fold cuma **kerugian yang bisa diprediksi**.

## Fakta #2: Raise Kamu Sering Tidak Dibayar

Dari seluruh tangan, kemenangan showdown melawan bandar yang kualifikasi cuma **15,8068%**. Bandar tidak kualifikasi di **22,7385%** tangan — di situ ante dibayar 1:1 tapi **raise push, tidak menghasilkan apa-apa**.

Kalau dihitung hanya dari tangan yang kamu raise (52,23% dari semua tangan):

- **43,54%** → bandar tidak kualifikasi, raise-mu mati (push).
- **30,27%** → kamu menang showdown, raise dibayar.
- **26,19%** → bandar menang, ante + raise hangus (3 unit).

Jadi dari setiap 100 kali kamu menaikkan taruhan 2x, **hampir 44 kali kenaikannya tidak pernah diadu**. Itu sebabnya strategi "asal raise biar dapat bayaran besar" adalah cara tercepat membakar modal: rumah tidak membayar taruhan yang tidak perlu dibayar.

## Fakta #3: Naik Semua Tangan = 3,18x Lebih Mahal

Perbandingan house edge per strategi, semuanya di paytable yang sama:

| Strategi | House edge | Element of risk |
|---|---|---|
| Sempurna (chart A-K lengkap) | **5,224%** | 2,555% |
| Strategi ringkas Wizard | 5,225% | 2,554% |
| Raise A-K-J-8-3 ke atas | 5,316% | 2,596% |
| Raise hanya pair ke atas | 5,470% | 2,738% |
| **Raise semua A-K** | **5,682%** | 2,672% |
| **Raise semua tangan (buta)** | **16,607%** | 5,536% |

Dua hal mengejutkan di tabel itu:

**Pertama, "raise semua A-K" lebih buruk daripada "fold semua A-K".** Raise hanya dengan pair ke atas (buang seluruh A-K) hasilnya 5,470%, sementara menaikkan semua A-K hasilnya 5,682%. Jadi kalau kamu tidak hafal chart A-K, **membuang semua A-K lebih murah** daripada menaikkannya. Chart A-K yang benar-benar optimal cuma dipakai untuk 24 tangan tertentu di antara ratusan kombinasi — itu bagian paling rumit dari permainan yang katanya sederhana ini.

**Kedua, blind raise menghancurkan segalanya.** Naikkan semua tangan dan house edge melompat ke **16,607%** — 3,18 kali lebih mahal. Dalam rupiah, dengan ante Rp 100.000 dan 100 tangan: strategi optimal hangus **±Rp 522.000**, blind raise hangus **±Rp 1.661.000**.

## Fakta #4: Yang Menentukan Paytable Bukan Royal Flush

Karena "element of risk" 2,555% dipakai untuk membandingkan antar game (kerugian dibagi rata-rata taruhan 2,0445 unit), banyak pemain fokus ke bayaran royal flush yang 100:1. Itu salah alamat. Sensitivitas paytable-nya begini — tambahan 1 unit bayaran:

- **Royal flush +1 unit** → +0,008 poin persen. Tidak terasa.
- Flush +1 unit → +0,110 poin.
- Three of a kind +1 unit → +1,175 poin.
- **Two pair +1 unit → +2,448 poin.**
- **Pair atau kurang +1 unit → +11,756 poin.**

Artinya saat duduk, yang perlu kamu baca di papan pembayaran adalah **baris two pair dan baris pair** — bukan angka royal flush yang cuma 0,0001% peluangnya. Meja yang membayar two pair 2:1 dengan pair 1:1 masih wajar; meja yang memotong dua baris itu jauh lebih mahal daripada selisih bayaran jackpot.

## Checklist Sebelum Duduk

1. **Baca paytable dua pair & pair** — dua baris itu penentu biaya meja, bukan jackpot.
2. **Hafal tiga aturan aman**: pair ke atas → raise; di bawah A-K → fold; A-K → butuh chart, kalau tidak hafal, fold.
3. **Jangan menghitung "raise 2x itu cuma 2x"** — total taruhan saat raise = 3 unit, dan 43,5% raise tidak pernah diadu.
4. **Hitung biaya per jam, bukan per tangan**: 40 tangan/jam × ante Rp 100.000 = kerugian teoretis ±Rp 209.000/jam. Itu harga hiburan, bukan peluang cuan.
5. **Side bet progresif itu taruhan terpisah**, tidak termasuk dalam 5,22% — punya hitungan sendiri dan jangan dicampur ke strategi utama.

Kerangka yang sama dipakai waktu membedah [house edge Sic Bo dari 216 kombinasi](/posts/sic-bo-house-edge-216-kombinasi/), [baccarat banker vs player](/posts/baccarat-banker-vs-player-house-edge/), [Pai Gow yang 40% seri](/posts/pai-gow-poker-push-40-persen-house-edge/), dan [cara membaca RTP slot](/posts/rtp-slot-volatilitas-cara-baca-2026/). Untuk mengatur besar taruhan per tangan, [rumus Kelly](/posts/kelly-criterion-ukuran-taruhan-bankroll/) lebih jujur daripada feeling.

## Kesimpulan

Caribbean Stud bukan permainan keberuntungan yang netral: **5,22% dari setiap ante hilang** dengan main sempurna, dan naik taruhan secara asal bisa melipatgandakannya jadi 16,6%. Yang bisa dikendalikan hanya dua hal — **kapan fold** dan **paytable meja mana yang dipilih**. Sisanya, bandar yang pegang kendali.

Kalau mau main meja kartu dengan hitungan yang lebih transparan, cek dulu daftar game dan promo di **[SLOT161](https://tomat.jagungbaru.com/banner/s161)** — dan selalu buka menu info/paytable sebelum chip pertama turun. Main pakai angka, bukan pakai harapan. 🐷

Sumber: [Wizard of Odds — Caribbean Stud Poker](https://wizardofodds.com/games/caribbean-stud-poker/) (return table 19,9 triliun kombinasi, tabel strategi, element of risk) dan [PokerCoaching — Caribbean Stud](https://pokercoaching.com/blog/how-to-play-poker/caribbean-stud/) (aturan & paytable raise). Semua probabilitas, house edge, dan angka rupiah di artikel ini dihitung ulang dari return table, bukan disalin.

— Chokdi 🐷 · Content Studio · 2026
