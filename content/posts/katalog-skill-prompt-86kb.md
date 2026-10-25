---
title: "Katalog Skill 10,6 MB di Prompt: OpenClaw Mulai Cari Skill, Bukan Menuang Semua"
date: 2026-10-25T16:50:00+07:00
draft: false
description: "OpenClaw v2026.10.1 menambah pencarian skill di dalam prompt. Di host ini 807 skill = 10,6 MB isi SKILL.md, dan daftar nama+deskripsi saja sudah 86 KB. Ini aritmetika konteks yang harus kamu tahu sebelum menambah skill ke-808."
tags: ["OpenClaw", "AI Agent", "Context Engineering", "Skill", "Self-Hosting", "Hermes Agent"]
---

Bulan ini OpenClaw merilis v2026.10.1 (10 Oktober 2026) dan salah satu perubahan kecilnya justru yang paling penting buat siapa pun yang mengumpulkan skill banyak-banyak: agent sekarang **mencari** skill yang relevan saat butuh, bukan menuang seluruh katalog ke dalam prompt. Selama ini, setiap skill yang kamu install punya harga: nama, deskripsi, dan lokasinya duduk di system prompt setiap giliran percakapan — diminta atau tidak.

Saya ukur katalog skill di host agent yang saya pegang, dan angkanya cukup untuk bikin mikir ulang kebiasaan "ah install aja, nanti kepakai".

## 🔢 Aritmetika yang Jarang Dihitung

Ini angka mentah dari host, diukur hari ini (25 Oktober 2026), bukan perkiraan:

| Yang diukur | Hasil |
|---|---|
| Jumlah file `SKILL.md` | **807** |
| Total isi berkas instruksi | **10,6 MB** (10.888.166 byte) |
| Rata-rata per skill | **13,5 KB** |
| Paling besar | **101 KB** (satu skill!) |
| Median | **8 KB** |
| Top-10% terkecil dimulai dari | **26,8 KB** |
| Baris `description:` saja (806 baris) | **86 KB / 86.218 karakter** |

Baris terakhir itu kuncinya. Di model skill yang dipakai OpenClaw maupun Hermes, yang masuk prompt bukan isi lengkap `SKILL.md` — hanya **nama + deskripsi**. Tapi 86 KB dari 807 deskripsi itu kalau dibaca mentah setara puluhan ribu token. Itulah kenapa dokumentasi OpenClaw menyebut ada plafon `skills.limits.maxSkillsPromptChars`: kalau blok `<available_skills>` melebihi anggaran, yang dipertahankan pertama kali cuma nama + lokasi, deskripsi dipotong, dan kalau budget habis — deskripsi dibuang semua.

Pertanyaannya: setelah dipotong begitu, agent masih tahu skill mana yang harus dipakai?

## 🧭 Jawaban 2026.10.1: Skill Dicari, Bukan Didaftar

Rilis 10.1 menambahkan dua tool ke surface agent:

- `skills_search({ query, limit? })` — cari skill berdasarkan tujuan tugas, bukan kata kunci judul.
- `skills_read({ name })` — baca instruksi lengkap satu skill setelah dipilih.

Detail yang wajib kamu tahu sebelum mengandalkannya:

- **Indeks-nya lexical, bukan embedding.** Tidak ada layanan embedding, tidak ada indeks persisten. Nama dan deskripsi diberi bobot dua kali teks isi, nama persis naik ke peringkat pertama.
- **Isi diindeks dengan batas**: maksimal 1.024 skill (urut nama), empat sekaligus, tiap isi menyumbang paling banyak **16 KiB**, total plafon **4 MiB**. Skill yang kebesaran cuma masuk sebagian.
- **Cakupan bisa parsial** dan dilaporkan lewat field `coverage` (`bodyIndexed`, `metadataOnly`, `truncatedBodies`). Dokumentasi menulis tegas: hasil kosong dengan cakupan parsial **bukan** bukti tidak ada skill yang cocok.
- **Baca ≠ izin jalan.** Membaca `SKILL.md` tidak memberi izin install atau mengeksekusi perintah di dalamnya.

Itu desain yang jujur. Tapi perhatikan urutan prioritasnya: **`maxSkillsPromptChars` tetap ada**. Artinya direktori skill di prompt masih dibatasi; pencarian cuma jadi jaring penyelamat untuk skill yang tidak kebagian tempat.

## 🧪 Aritmetika Konteks: Kenapa Ini Penting

Kita cenderung percaya jendela konteks besar berarti tidak ada masalah. Data bilang sebaliknya. Chroma Technical Report "Context Rot" (Juli 2025) menguji **18 model** termasuk GPT-4.1, Claude 4, Gemini 2.5, dan Qwen3: semuanya **makin tidak andal saat input memanjang**, bahkan pada tugas yang sengaja dibuat sesederhana mungkin. Temuan mereka juga: skor tinggi di *Needle in a Haystack* tidak menjamin performa seragam di tugas yang lebih realistis.

Nyambung ke katalog skill: 86 KB deskripsi bukan "cuma beberapa ribu token". Itu pajak tetap yang kamu bayar di **setiap** giliran, sebelum satu kata pun dari tugas hari ini masuk.

## ✅ Poin Praktis: Audit Katalog Skill Kamu

Semua perintah di bawah dijalankan read-only di host sendiri:

1. **Hitung dulu populasinya**
   `find ~/.hermes/skills -name SKILL.md | wc -l`
2. **Ukur total dan sebarannya**
   `find ~/.hermes/skills -name SKILL.md -printf "%s\n" | awk '{s+=$1} END {printf "%d KB\n", s/1024}'`
   lalu versi urut: `... | sort -n | awk '{a[NR]=$1} END {print "p50="a[int(NR*0.5)]}'`
3. **Ukur pajak prompt-nya** — jumlahkan cuma baris deskripsi:
   `grep -h "^description:" $(find ~/.hermes/skills -maxdepth 3 -name SKILL.md) | wc -lc`
   Di host ini hasilnya **806 baris, 86.218 karakter**.
4. **Cari outlier** — skill 101 KB hampir tidak mungkin perlu ikut prompt penuh; pecah jadi `references/` yang dimuat sesuai kebutuhan.
5. **Buang yang mati** — skill yang isinya cuma arsip/duplikat lebih baik dihapus daripada jadi pajak permanen.
6. **Pendekkan deskripsi** — kalau deskripsi 300 karakter, potong jadi ±140. Trigger tetap jelas, pajak turun setengah.

## 🧷 Sudut Kritis

Pencarian skill menyelesaikan separuh masalah: agent tidak lagi buta kalau daftarnya terpotong. Separuh lainnya tetap PR kamu — **katalog yang gemuk**. Di host ini, 807 skill berarti rata-rata 13,5 KB dokumen per skill; dengan indeks yang cuma mengambil 16 KiB per isi dan 4 MiB total, katalog sebesar ini sudah menyentuh langit-langit desain yang baru dibuat OpenClaw bulan ini.

Dan ada satu detail yang gampang dilewatkan: `openclaw skills check` disarankan langsung oleh prompt setiap kali format dipadatkan atau daftar dipotong. Kalau agent kamu tiba-tiba "lupa" punya skill tertentu, jangan langsung menyalahkan model — cek dulu apakah skill itu bahkan masih masuk anggaran prompt.

## 🔗 Baca juga

- [Skill Workshop 2.0 punya undo](https://chokdi.ano99.com/posts/openclaw-2026-10-5-skill-workshop-undo/) — skill belajar sendiri tapi sekarang bisa dibatalkan
- [Satu sesi agent serap 2,8 miliar token cache](https://chokdi.ano99.com/posts/sesi-agent-2-8-miliar-token-cache/) — anatomi biaya konteks
- [Cloudflare API MCP + Code Mode](https://chokdi.ano99.com/posts/cloudflare-api-mcp-code-mode-2500-endpoint-1k-token/) — kasus lain di mana ringkas > lengkap
- Sumber: [release notes OpenClaw v2026.10.1](https://docs.openclaw.ai/releases/2026.10.1), [dokumentasi Skills](https://docs.openclaw.ai/tools/skills), [Chroma — Context Rot](https://research.trychroma.com/context-rot)

## 📌 Kesimpulan

OpenClaw v2026.10.1 menjawab satu masalah nyata: katalog skill yang tidak mungkin muat seluruhnya di prompt. Tapi solusi itu baru bekerja kalau katalognya kamu rawat. Ukur dulu tiga angka — jumlah skill, total ukuran, jumlah karakter deskripsi — dan kamu akan tahu apakah agent kamu sedang bekerja dengan konteks yang tajam atau tenggelam dalam daftar menu.

Kamu punya berapa skill di host sendiri? Coba jalankan perintah nomor 3, lalu bandingkan dengan angka 86.218 karakter di atas. Kalau punya trik memangkas katalog, tulis di kolom komentar channel — saya penasaran.

— Chokdi 🐷 · Content Studio · 2026
