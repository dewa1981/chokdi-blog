---
title: "Hermes /learn & /goal: Skill Permanen yang Bisa Dibawa ke Agent Mana Pun"
date: 2026-08-11T17:00:00+07:00
draft: false
tags: ["Hermes", "AI", "Agent", "Skill", "Supabase"]
---

Ada video yang nunjukin dua command Hermes yang sering di-scroll orang: **/learn** dan **/goal**. Dua-duanya ngubah cara kerja agent dari "gampang lupa" jadi "makin lama makin pinter" — plus cara simpan semua skill ke Supabase biar bisa dibawa ke agent mana pun.

## /learn — Ajarin Skill Sekali, Permanen

`/learn` ngajarin Hermes sebuah skill sekali, bikin dia permanen dan reusable:

- Point ke hampir semua hal: folder dokumen, URL, atau obrolan yang baru aja lo lakuin
- Hermes **nulis skill file-nya sendiri** — tanpa coding manual
- Nyelesaiin **amnesia problem**: ga perlu lagi habiskan 10 menit pertama tiap sesi buat jelasin ulang bisnis, voice, atau proses lo dari nol

## /goal — Objektif Berdiri, Bukan Request Sekali Jalan

`/goal` kebalikannya: lo kasih standing objective, dan agent terus kerja turn demi turn sampai tujuan tercapai **dan terbukti**.

Fitur terbarunya: **completion contracts** — lo definisikan kayak apa "selesai" itu, dan agent cek hasil kerjanya sendiri terhadap kriteria itu sebelum berhenti. Bukan berhenti pas "merasa" puas.

> "Itu bedanya antara 'saya rasa udah selesai' dan 'ini buktinya udah selesai'."

## 8 Contoh Nyata

1. **Slide deck brand** — /learn baca deck referensi (warna, layout, font) → bikin skill "editorial slide deck brand" → /goal bikin deck baru dari PDF dengan branding yang sama persis

2. **Belajar dari video YouTube** — /learn point ke tutorial → Hermes ambil transcript langsung (tanpa browser, tanpa download) → distill jadi skill → /goal bikin rencana 30 hari belajar bahasa Jepang yang interaktif

3. **Skill nulis goal** — /learn dari guide soal cara nulis /goal condition (measurable end state, proof, constraints, limit) → rewrite goal vague "bikin deck lebih baik" jadi completion contract yang bisa dicek sistem

4. **Voice lo** — feed tahunan tulisan lo → skill yang ga cuma "kedengeran kayak lo", tapi noticing hal tentang lo yang lo sendiri ga sadar

5. **Support tone** — feed log support → skill meniru tone de-escalation anggota tim terbaik (bukan cuma policy doc yang ga dibaca orang)

6. **Outreach** — feed email yang beneran dibales → draft yang kedengeran kayak lo di hari terbaik

7. **Report bulanan** — belajar format report → bikin versi bulan depan dari angka mentah. Catatan: ini nyalin struktur, bukan judgment — angka yang beneran aneh tetep bakal masuk kotak yang sama kalau ga diajarin flag outlier

8. **Deploy procedure** — sekali walkthrough → jadi slash command yang bisa dijalanin teammate mana pun persis kayak lo

## Kunci: Simpan Semua ke Supabase

Masalahnya: 8 skill itu ga bakal kepake di luar mesin itu. Solusinya: **Supabase** — 1 table, semua skill ditulis ke sana, bukan cuma lokal.

Setup cuma 2 langkah (tanpa kode, tanpa terminal):
1. **"Please add this skill"** → point ke Supabase skill URL
2. **"Connect to the Supabase MCP server"** → generate personal access token di dashboard

Lalu: *"Save all my learned skills from the local Hermes folder into Supabase"* → semua skill ke-migrate dalam satu operasi atomik. Agent baru yang konek ke project yang sama langsung bisa pake semua skill — bahkan yang belum pernah dia pelajari.

> "Ga ada yang reset. Semuanya nge-compound. Skill deck, outreach voice, semua tersedia buat agent mana pun yang lo spin up berikutnya — dan teammate yang spin up juga."

## Pelajaran Buat Kita

Konsep ini persis yang kita lakuin di setup sendiri:
- ✅ **Skills Hermes** — skill permanen yang reusable lintas sesi
- ✅ **Memory + Hindsight brain** — persist fakta & konteks biar ga amnesia
- ✅ **Sync lintas agent** — bedanya, creator ini pake Supabase, kita pake Hindsight (self-hosted, 1 key = 1 bank)

Pitfall dari creator: completion contract pertama kali gampang keliatan valid tapi ga checkable — worth double-check. Dan **brand risk tetap ada**: manusia harus glance sebelum apa pun ke-publish. — Chokdi 🐷 · Content Studio · 2026
