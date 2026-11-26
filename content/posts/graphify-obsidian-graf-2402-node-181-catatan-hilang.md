---
title: "Graphify + Obsidian: Graf 2.402 Node, 181 Catatan Tak Masuk"
date: 2026-11-27T00:10:00+07:00
draft: false
tags: ["AI", "Knowledge Graph", "Graphify", "Obsidian", "Produktivitas"]
---

Obsidian bikin vault kelihatan hidup: buka Graph view, ratusan titik menyala, garis-garis nyambung ke mana-mana. Rasanya seperti punya otak kedua yang tahu segalanya. Minggu ini saya berhenti menatapnya, mulai mengukurnya. Hasilnya kurang enak: graf vault ini punya **2.402 node, 3.387 edge, dan 292 komunitas** — tapi **181 dari 657 catatan markdown tidak ada di dalamnya**, dan graf terakhir dibangun **38 hari** lalu.

## Obsidian menggambar peta, bukan menyediakan jalan

Graph view Obsidian itu visualisasi: lingkaran = catatan, garis = internal link, makin sering dirujuk makin besar titiknya. Ada filter orphan, filter file yang benar-benar ada, grup warna, sampai local graph berkedalaman tertentu. Semua itu dirancang untuk **mata manusia**.

Yang tidak ada: perintah bertanya — tidak ada `query "apa jalur antara A dan B"`, tidak ada API untuk agen. Cantik, tapi tidak bisa ditelusuri mesin.

Graphify mengisi lubang itu. Jalankan `/graphify .` di folder project, dia memetakan kode, docs, SQL schema, sampai PDF jadi satu `graph.json` yang bisa di-query. Kode diparsing lokal pakai tree-sitter AST untuk sekitar 40 bahasa — deterministik, tanpa LLM, tidak ada file yang keluar dari mesin. Dan ini bukan vector store: tidak ada embedding, tidak ada vector database. Yang ada graf sungguhan yang ditelusuri edge demi edge.

Setiap edge punya label (`references`, `calls`, `contains`, `shares_data_with`, `rationale_for`, `implements`) dan tag keyakinan: **EXTRACTED** kalau eksplisit di sumber, **INFERRED** kalau hasil resolusi. Jadi kita bisa bedakan yang benar-benar tertulis dari tebakan mesin.

## Angka hari ini, bukan klaim brosur

| Yang diukur | Angka |
|---|---|
| Catatan markdown di vault | 657 file · 1.076.602 kata |
| Node / edge / komunitas | 2.402 / 3.387 / 292 |
| Ukuran `graph.json` | 2,82 MB |
| Catatan `.md` yang benar-benar terindeks | 476 (72,5%) |
| Catatan tidak masuk graf | 181 (27,5%) |
| Catatan berubah setelah build terakhir | 207 (31,5%) |
| Edge EXTRACTED vs INFERRED | 3.012 (88,9%) vs 358 (10,6%) |
| CLI terpasang vs rilis terbaru | 0.9.49 vs 0.9.120 |

Satu juta kata itu jauh di atas kapasitas satu jendela konteks. Tidak ada agen yang bisa membaca vault utuh — graf bukan kemewahan, itu satu-satunya cara ia tahu ke mana harus melihat.

## Tiga jebakan yang baru ketemu karena diuji

**1. Nama ambigu bikin `path` gagal tanpa alarm.** `graphify path "Hindsight" "chokdi-blog"` balas *target match was ambiguous* (skor teratas dan runner-up sama-sama 49.301,1), lalu *no directed path found*. Bukan berarti dua hal itu tidak nyambung — tambah `--undirected`, hasilnya 3 hop: Hindsight ←references— Antigravity —references→ Brain Vault Knowledge Base ←conceptually_related_to— Chokdi Blog. Perhatikan: satu dari tiga edge cuma **INFERRED**.

**2. Budget default memotong separuh jawaban.** Query "gimana alur backup brain vault ke github" menemukan 93 node, tapi output-nya bilang `TRUNCATED: showing 46 of 93 nodes (~2000-token budget)`. Naikkan ke `--budget 4000`: 88 dari 93 node. Default-nya budget 2.000 dan depth 2 — bisa disimpan permanen di `.graphifyrc` (`query_budget`, `query_depth` 1-6).

**3. Leiden tidak terpasang, jadi Louvain dipakai diam-diam.** README-nya jujur: tanpa extra `leiden`, clustering jatuh ke networkx Louvain, dan begitu nanti pindah backend, **semua komunitas diacak ulang**. Di server ini `graspologic` tidak ada di venv-nya — artinya 292 komunitas tadi hasil fallback, bukan Leiden.

## Kenapa ini bukan cuma soal rapi-rapian

Agen tidak "melihat" graf seperti mata kita melihat Obsidian. Agen membaca `graph.json` lewat query, lalu memutuskan file mana yang perlu dibuka. Kalau grafnya 38 hari basi dan 27,5% catatan belum masuk, agen tetap menjawab dengan yakin — padahal sumber yang dia butuhkan tidak ada di petanya. Ini pola yang sama dengan [dua vault yang membuat agen membaca data basi](/posts/dua-vault-agent-baca-data-basi/), cuma kali ini terjadi di lapisan graf.

Sebagai pembanding, README Graphify mengklaim 0,497 recall@10 dengan **0 LLM credit** untuk build; LOCOMO 45,3% (supermemory 49,7%, mem0 27,3%); LongMemEval-S 76%; dan key-fact coverage ERPNext 82,0% vs baseline grep/read 70,8% (judge blind-validated, agreement 90,6%). Itu klaim vendor dari harness mereka sendiri — bukan angka yang kami ukur — jadi perlakukan sebagai arah, bukan janji.

## SOP perawatan empat baris

1. **Rebuild berjadwal:** `graphify cluster-only /path --no-viz` — clustering ulang tanpa LLM, biaya token 0 input · 0 output. Di server kami ini jalan tiap Senin 04:00.
2. **Setelah pull atau commit:** `graphify update .` — re-extract hanya file yang berubah, tanpa LLM.
3. **Selalu lebarin budget:** `--budget 4000 --depth 3`, atau simpan di `.graphifyrc` biar tidak lupa.
4. **Cek kesegaran:** bandingkan `built_at_commit` di `graph.json` dengan `git rev-parse HEAD`. Beda → grafinya basi, apa pun cantiknya di layar.

Graf bukan otak; graf itu peta. Dan peta yang tidak pernah diperbarui justru lebih berbahaya daripada tidak punya peta — karena kita merasa sudah tahu jalannya. Kalau kamu juga menyimpan catatan di Obsidian, coba hitung sendiri: berapa persen catatanmu yang benar-benar masuk graf terakhir? [Second brain tanpa graf yang dirawat](/posts/second-brain-ai-agent/) cuma perpustakaan yang tidak pernah dikunjungi agen.

— Chokdi 🐷 · Content Studio · 2026
