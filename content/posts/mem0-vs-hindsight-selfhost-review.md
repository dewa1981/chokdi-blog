---
title: "Mem0 vs Hindsight Self-Host: 97.8% Memori mem0 Ternyata Junk?"
date: 2026-08-26T18:50:00+07:00
draft: false
tags: ["AI", "Memory", "Review", "Hindsight", "Mem0"]
---

Hermes Agent mendukung 8 memory provider: openviking, honcho, mem0, hindsight, holographic, retaindb, byterover, dan supermemory. Dua yang paling sering dibandingkan untuk self-host adalah **mem0** dan **Hindsight**. Mana yang lebih bagus? Daripada percaya klaim pemasaran, mari lihat apa kata user yang benar-benar menjalankannya di production. Hasilnya cukup mengejutkan.

## Temuan Besar: 97.8% Memori mem0 Adalah Junk

Pada Maret 2026, seorang user membuka issue di GitHub mem0ai/mem0 (issue #4573) dengan judul yang sangat jujur: *"What we found after auditing 10,134 mem0 entries: 97.8% were junk"*.

Ceritanya begini: dia menjalankan mem0 self-host di production selama **32 hari** — satu AI agent, satu manusia, obrolan harian, backend Qdrant. Dua model ekstraksi dipakai: gemma2:2b (lokal via Ollama) 20 hari pertama, lalu Claude Sonnet 4.6 untuk 12 hari terakhir. Karena agent-nya mulai "mengingat" hal yang tidak pernah diceritakan, dia memutuskan mengaudit seluruh database-nya: **10.134 entri**.

Hasil auditnya brutal:

- **2.468 entri** langsung dihapus: duplikat hash, klaster halusinasi seperti "formal communication style" dan "software developer at Google", plus **668 salinan halusinasi feedback-loop yang sama**
- **2.943 entri** (37.6%) terdeteksi near-duplicate via cosine similarity
- Dari 829 cluster survivor, hanya **7 yang dipertahankan**
- Setelah dibaca satu-satu: dari 10.134 entri, hanya **224 yang selamat** — dan 186 di antaranya harus ditulis ulang dari nol karena malformed
- **Kesimpulan: hanya 38 entri yang benar-benar bersih**

Yang paling penting: **upgrade model ekstraksi tidak memperbaiki apa pun**. Junk rate tetap ~98% baik dengan gemma2:2b maupun Claude Sonnet 4.6. Ini bukan bug satu titik — ini bukti bahwa pipeline ekstraksi mem0 rusak di kondisi production nyata.

## Review User Lain di Komunitas

Temuan #4573 bukan kasus terisolasi. Cek review di Reddit, Hacker News, dan Medium:

- **Reddit r/Rag** — post "Summary of My Mem0 Experience" dibuka dengan kalimat *"I had a pretty terrible experience with mem0"*
- **Hacker News** — thread "Ask HN: Mem0 stores memories, but doesn't learn user patterns" — kritik utamanya: mem0 hanya menyimpan fakta mentah, tidak belajar pola dari fakta-fakta itu
- **Reddit r/AI_Agents** — seorang peneliti melakukan security audit forensik mem0 dan menemukan **23 kerentanan severity tinggi**
- **Medium (honest review)** — free tier cuma 100 memories/bulan (hanya untuk testing), plus hidden cost yang menumpuk untuk startup

## Kenapa Hindsight Berbeda?

Hindsight dirancang dengan pendekatan yang berbeda sejak awal. Alih-alih sekadar vector store dengan LLM extraction, Hindsight memakai:

1. **Knowledge graph + entity resolution** — fakta saling terhubung, bukan titik-titik terisolasi
2. **Observation layer** — mengatasi kontradiksi fakta. Contoh nyata: kalau Januari agent pakai Redux lalu Maret pindah ke Zustand, vector search naif akan mengembalikan keduanya dan bikin agent bingung. Observation layer menyelesaikan ini
3. **Reflect** — fitur yang tidak dimiliki mem0: membaca seluruh graph dan mensintesis jawaban kaya konteks, bukan sekadar recall fakta
4. **Konsolidasi otomatis** — fakta terkait digabung jadi observation, mencegah penumpukan junk seperti yang terjadi di mem0
5. **Temporal memory** — tahu KAPAN sebuah informasi terjadi

Bukti kualitasnya juga terukur: **Hindsight menembus 91.4% di benchmark LongMemEval** — sistem memory agent pertama yang melewati angka 90% (diumumkan resmi via PR Newswire dan arXiv paper).

## Perbandingan Self-Host Head-to-Head

| Aspek | mem0 self-host | Hindsight self-host |
|---|---|---|
| Stack | Qdrant + API wrapper (1-2 container) | 1 container (PostgreSQL + API) |
| Tipe memori | Flat vector store | Knowledge graph + temporal + semantic |
| Reflect | ❌ Tidak ada | ✅ Baca seluruh graph, sintesis jawaban |
| Anti-junk / dedup | ❌ Terbukti 97.8% junk di production | ✅ Observation layer + konsolidasi |
| Isolasi multi-agent | Satu DB, user_id string | Bank per agent (1 key = 1 bank) |
| Kecepatan recall | ~0.36s (vector-only) | 2.4-3.4s (reranker cross-encoder lokal, lebih akurat) |
| Ekosistem & docs | ✅ Matang, komunitas besar | Komunitas kecil tapi fokus |
| Biaya | LLM ekstraksi + embedder + Qdrant | DeepSeek murah + embedding lokal offline |

## Kesimpulan

Mem0 memang lebih populer dan punya ekosistem lebih besar — itu tidak bisa dipungkiri. Tapi untuk penggunaan production jangka panjang, ada masalah fundamental di pipeline ekstraksinya yang membuat agent "mengingat" sampah: hampir 98% dari apa yang disimpannya ternyata junk.

Hindsight mengambil jalan yang lebih sulit tapi lebih benar: membangun memori sebagai knowledge graph dengan konsolidasi, observation, dan reflect. Hasilnya lebih akurat, lebih hemat biaya di skala besar, dan — paling penting — tidak bikin agent mengingat hal yang tidak pernah terjadi.

Kalau kamu baru mulai dan butuh sesuatu yang simpel dengan komunitas besar, mem0 masih oke untuk dicoba. Tapi kalau kamu serius membangun agent jangka panjang yang harus ingat dengan benar — Hindsight adalah pilihan yang lebih masuk akal.

Punya pengalaman pakai mem0 atau Hindsight? Cerita di kolom komentar, ya! 💬

— Chokdi 🐷 · Content Studio · 2026
