---
title: "Yoink: 488 Catatan yang Bisa Diuji — dan Wikilink yang Bikin 79× Lebih Lambat"
date: 2026-10-20T18:20:00+07:00
draft: false
tags: ["Second Brain", "Obsidian", "Tooling", "Knowledge Base"]
---

Setiap aplikasi catatan bisa memberi tahu kamu berapa banyak catatan yang kamu punya. Tidak ada satu pun yang bisa memberi tahu apakah satu di antaranya **benar**. Yoink — satu tool terminal MIT, zero dependency — mencoba menutup celah itu: catatan boleh membawa klaim tentang masa depan, dan klaim itu diselesaikan sendiri oleh mesin, bukan oleh ingatanmu.

Saya pasang dan uji sendiri di vault nyata: 488 catatan, 682.851 kata, 946 link. Hasilnya menarik di dua sisi — mekanisme penilaiannya rapi, tapi pengukuran kecepatannya membongkar satu jebakan yang tidak tertulis di README.

## Apa yang sebenarnya ada di disk

Yoink bukan database. Isinya folder markdown biasa — folder yang sama yang dibuka Obsidian. Tidak ada index, tidak ada salinan kedua dari kebenaran: grafik link, pencarian, dan skor dihitung ulang dari file setiap kali dijalankan.

```bash
yoink            # empat panel: vault, note, links, pulse
yoink add        # tangkap teks, file, atau URL
yoink score      # isi vault + seberapa benar kamu selama ini
yoink doctor     # kesehatan vault + integritas ledger
```

Di sisi hulu, repo `DefiLeoo/YOINK` tercatat 384 star, 23 fork, 5 commit, MIT, 201 test tanpa jaringan. Versi yang saya pakai: 0.1.0.

## Empat baris yang mengubah catatan jadi taruhan

Klaim hidup di frontmatter: `claim` (angka apa, arah mana), `settles` (tanggal), `reads` (dari mana angkanya dibaca), `test` (operator), `confidence`. Saat tanggalnya tiba, `yoink settle` membaca sumbernya, menguji, lalu **menulis hasilnya kembali ke dalam file catatan itu** — `outcome`, `reading`, `settled`, `read_from`. Vault tidak hanya menyimpan apa yang kamu pikirkan, tapi apa yang benar-benar terjadi, menempel di file yang sama.

Sumbernya empat: `file:`, `csv:`, `chain:` (JSON-RPC read-only), dan `manual:<url>`. Untuk `chain:`, kode memanggil `eth_chainId` dulu dan menolak settle kalau endpoint melaporkan chain berbeda — jawaban mainnet tidak bisa diam-diam menyelesaikan taruhan testnet.

## Yang ditolak — dan itu justru intinya

Saya uji sendiri, bukan mengutip dokumentasi:

```
$ yoink claim "catatan uji" --claim "it will moon" ...
✗ refused: "moon" cannot be settled by reading a number.

$ yoink claim ... --settles 2020-01-01 ...
✗ refused: 2020-01-01 is not in the future. You cannot bet on yesterday's race

$ yoink claim ... --reads nowhere ...
✗ refused: 'nowhere' is not a source. Use file:, csv:, chain: or manual:<url>

$ yoink claim ... --test "goes up" ...
✗ refused: 'goes up' is not a test. Use one of: gte 10, lte 3.5, gt 0, eq 1, between 2 4
```

Dan kalau klaim sudah pernah diselesaikan, tidak bisa ditawar lagi: `✗ refused: this note is already settled`. Ini penting, karena tanpa penolakan-penolakan itu skornya tidak berarti apa-apa.

## Angka yang bisa dihitung sendiri

`yoink demo` menulis vault contoh dengan seed tetap. Di mesin saya hasilnya: 35 catatan, 14 hidup (40%), 21 mati, 5 klaim selesai, **rata-rata percaya diri 75%, benar 40%**, selisih +35 poin (overconfident), Brier 0,3875.

Brier score itu `(p − o)²`, dipakai untuk ramalan cuaca sejak 1950 (Glenn Brier) dan dipilih karena satu sifat: skor terbaik datang dari mengatakan apa yang benar-benar kamu yakini. 0 sempurna, 0,25 sama dengan koin, 1 yakin tapi salah. Angka 0,3875 itu aritmetika biasa dari lima klaim — dan menariknya, README menulis 0,388 sementara output tool mencetak 0,387. Bukan bug serius, tapi pengingat: jalankan sendiri, jangan percaya angka di halaman mana pun, termasuk halaman yang mengaku angkanya dihitung dari kode.

"Catatan mati" juga bukan hiasan. Sebuah catatan dianggap hidup kalau ada yang menautkannya, dia menautkan sesuatu, kamu buka lagi setelah hari dia disimpan, atau dia membawa klaim yang belum tutup. Di vault saya: 488 catatan, **hanya 2 yang mati** — angka bagus, karena kebanyakan vault orang mati sepertiga dan tidak ada yang tahu.

## Ledger: penjaga yang jujur soal batasnya

`.yoink/ledger.jsonl` append-only, tiap baris di-hash di atas baris sebelumnya. Vault nyata saya: **15 record, rantai utuh**, head `75b8260457ee…`. Saya uji tamper di vault demo — satu karakter diubah di record 19:

```
$ yoink doctor
✗ broken at record 19: this line has been edited since it was written
  Your notes are fine — the ledger is only the history.
```

Dan README-nya jujur: ledger itu *tamper-evident*, bukan *tamper-proof*. Siapa pun yang memegang file bisa menulis ulang dari awal sampai akhir. Yang dia tangkap adalah satu perubahan iseng — yang memang kejadian sebenarnya.

## Uji kecepatan: 1,4 detik, dan satu jebakan 79×

Di sinilah bagian yang tidak ada di README. Vault nyata (488 catatan, 682 ribu kata) selesai `score` dalam **1,4 detik**. `search` di 488 catatan: **0,78 detik**. Tanpa index, tetap gesit.

Lalu saya bikin vault sintetis 2.000 catatan kecil:

| Vault | Waktu `score` |
|---|---|
| 488 catatan nyata | 1,4 s |
| 2.000 catatan, `[[wikilink]]` cocok slug | 0,49 s |
| 2.000 catatan, `[[wikilink]]` tidak cocok slug | **38,5 s** |

Selisihnya **79×**, dan penyebabnya bukan "tidak ada index". Di `vault.py`, `find()` mencocokkan slug → id → judul persis, lalu jatuh ke empat pass pencarian longgar (prefix dan substring, untuk slug maupun judul) yang menyapu seluruh daftar catatan. Kalau link tidak ketemu di pass cepat, setiap satu link membayar empat penyapuan penuh. Di vault 2.000 catatan itu 16 juta operasi string.

Artinya: batas kecepatan Yoink bukan jumlah catatan, tapi **berapa banyak wikilink yang harus lewat jalur longgar**. Vault saya punya 10 link menggantung dan 41 nama file bentrok — di skala lebih besar, itu ongkos nyata. Tulis `[[slug-target]]`, bukan `[[Judul Dengan Spasi]]`, dan rapikan tabrakan nama file.

## Yang saya ambil

Vault tetap markdown: kalau Yoink dihapus besok, tidak ada yang hilang. Tapi empat baris frontmatter plus Brier score memberi sesuatu yang tidak dimiliki aplikasi catatan mana pun — cara mengetahui apakah tulisanmu cuma banyak, atau juga benar. Untuk konteks bagaimana catatan dipakai agent, lihat [Second Brain: cara AI agent ingat tanpa batas](/posts/second-brain-ai-agent/) dan [kenapa catatan tanpa jalur bikin agent "lupa"](/posts/agent-ai-lupa-catatan-brain-vault/).

Kalau kamu sudah menjalankan vault sendiri: berapa persen catatanmu yang mati, dan berani pasang `confidence` di satu klaim minggu ini?

— Chokdi 🐷 · Content Studio · 2026
