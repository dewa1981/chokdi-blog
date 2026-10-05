---
title: "Repo 824 Bintang, Tapi Isinya Cuma Starter Kit — dan Skill Desain 7.455 Bintang di Baliknya"
date: 2026-10-05T07:35:00+07:00
draft: false
tags: ["AI", "Desain", "Skill", "OpenSource", "CMS"]
---

Kalau lihat repo dengan **824 bintang dalam sehari**, wajar kalau kita mikir itu produk serius. Kami periksa satu-satu hari ini — dan ternyata isinya **starter kit kosong**, tapi ada harta karun lain yang nyempil di dalamnya: **koleksi skill desain berlisensi MIT dengan 7.455 bintang**.

Ini catatan lengkapnya.

## Apa yang diumumkan

Tanggal 4 Oktober 2026, Marcel Kargul (kargul.studio — studio desain & engineering untuk startup) mengumumkan di X bahwa salah satu karyanya **akhirnya di-open-source**. Yang muncul kemudian: organisasi GitHub **kargulstudio** berisi tiga repo TypeScript.

## Angka sebenarnya (dari GitHub API, bukan teks halaman)

| Repo | Bintang | Fork | Issue | Dibuat | Push terakhir |
| --- | --- | --- | --- | --- | --- |
| sales-crm | **824** | 170 | 1 | 4 Okt 2026 | 4 Okt 2026 |
| workflow-editor | 381 | 55 | 1 | 15 Sep 2026 | 3 Okt 2026 |
| kanban | 19 | 7 | 0 | 16 Sep 2026 | 3 Okt 2026 |

Bintangnya asli dan cepat naik — 824 dalam hitungan jam. Tapi bintang tidak menjawab pertanyaan yang lebih penting: **isinya apa?**

## Kejutan pertama: semua itu bernama "kargul-starter"

Buka `package.json` di ketiga repo, isinya sama persis:

```json
{
  "name": "kargul-starter",
  "version": "0.1.0",
  "private": true
}
```

Bukan `sales-crm` versi 2.0, bukan `workflow-editor` produksi. Semuanya **satu boilerplate** yang di-rename. Isinya Next.js 16 + React 19 + Tailwind CSS 4, ditambah zustand, motion, Rive, Lottie, PhotoSwipe. Kualitas rapi — tapi ini **kerangka**, bukan aplikasi.

Tiga bukti pendukung:

**1. Repo bernama "sales-crm" isinya halaman marketing.** Cek daftar route-nya: cuma `app/layout.tsx`, `app/page.tsx`, `app/robots.ts`, `app/sitemap.ts`, `app/llms.txt/route.ts`. Tidak ada `/dashboard`, tidak ada `/deals`, tidak ada database. Nama "sales-crm" itu nama repo, bukan isi repo.

**2. "Workflow editor" itu simulasi, bukan eksekusi.** Ini bagian yang paling menarik untuk dibedah. Ambil file `workflow-run.ts` (mesin yang menjalankan alur):

```
const SAMPLE_SUBSCRIBER = "maya.chen@hey.com";
...
case "wait-until":
  return `Would wait until ${node.title} — skipped in test run`;
case "send-webhook":
  return `POST ${node.rules?.url ?? "https://hooks.buzzing.email/crm"} responded 200 OK in 184ms`;
```

Perhatikan: subscriber-nya **hardcoded** `maya.chen@hey.com`, aksi "tunggu sampai tanggal X" dilompati dengan komentar *"skipped in test run"*, dan webhook-nya tidak pernah dipanggil — hanya **dibuatkan string** "responded 200 OK in 184ms". Animasi simpul yang bergerak di video demo itu **simulasi visual** (`STEP_DURATION = 720` milidetik per langkah). Tidak ada backend, tidak ada worker, tidak ada pengiriman email nyata.

**3. README menyuruh baca file yang tidak ada.** Kedua repo menginstruksikan: *"Read `CONVENTIONS.md` before writing any component — it is the whole spec for how this repo is built."* File itu **404 di ketiga repo**. Dokumentasi acuan yang disebut sebagai "whole spec" tidak ikut dipublikasikan.

Tidak ada juga file `LICENSE` di ketiganya — artinya secara hukum default-nya *all rights reserved*, bukan open source dalam arti bebas dipakai.

## Kejutan kedua: harta karunnya justru skill, bukan kode

Yang menarik bukan tiga repo itu. Yang menarik ada di dalam `sales-crm/.agents/skills/` — **13 skill desain** plus `skills-lock.json` yang menunjukkan asalnya: repo **`jakubkrehel/skills`**.

Kami cek repo asalnya:

| | jakubkrehel/skills |
| --- | --- |
| Bintang | **7.455** |
| Fork | 277 |
| Bahasa | Markdown |
| Dibuat | 10 Jul 2026 |
| Push terakhir | 3 Okt 2026 |
| Lisensi | **MIT** ✅ |

Pemiliknya Jakub Krehel — desainer yang menulis di jakub.kr dan menerbitkan majalah desain engineering *Interfaces*. Isinya 13 skill untuk agen AI:

- **better-interface** — orkestrator: menggabungkan semua skill `better-*` jadi satu review lintas disiplin
- **better-ui** — radius konsentris, optical alignment, ikon kontekstual, hit area, animasi
- **better-typography** — type scale, spacing, variable font, OpenType, pemotongan teks
- **better-colors** — bikin palet, token semantik, konversi format, cek kontras
- **better-accessibility** — fokus & keyboard, form, ukuran target sentuh, screen reader, ARIA
- **better-layout**, **better-writing**, **interface-review**, **variant**, dan lainnya

### Kenapa ini menarik untuk kita

Ada satu prinsip di `better-interface` yang layak dikutip mentah:

> *"A trigger is a failure whatever the style guide says; a density, radius, or voice you merely disagree with is not a finding. So the bar for reporting is evidence, not taste."*

Artinya: skill itu **tidak menilai berdasarkan selera**. Pelanggaran aksesibilitas = temuan, apa pun kata style guide. Soal "menurut saya radiusnya kurang besar" = bukan temuan. Ini persis yang bikin review desain oleh agen AI sering tidak berguna — model menilai rasa, bukan bukti.

Dan `variant` menyelesaikan masalah klasik "bikin 3 opsi desain": tiga varian **tidak boleh** cuma beda warna aksen, karena kita jadi tidak belajar apa pun. Setiap varian harus berbeda pada **satu sumbu** — struktur, kepadatan, penekanan, tipografi, atau gaya bahasa.

## Kaitannya ke versi EmDash 1.1

Kebetulan di hari yang sama kami juga menguji **EmDash 1.1** (CMS open-source Astro dari Cloudflare, sudah kami pakai di `masthead.ano99.com`). Rilis 1.1 membawa hal yang **sejalan** dengan masalah di atas:

- **HTML block terisolasi** — blok HTML/CSS/JS kini dirender dalam iframe ber-origin buram: skrip di dalamnya jalan, tapi **tidak bisa** membaca cookie, storage, atau halaman situs induk
- **Blok iframe bawaan** — ketik `/iframe`, tempel URL; YouTube/Vimeo otomatis jadi player, iframe-nya sandboxed + lazy-load + kebijakan referrer ketat
- **Microsoft Entra ID** untuk login editor
- **WebMCP** (eksperimen) — agen AI di browser bisa memanggil `search_site` ke konten publik

Pola yang sama muncul di dua tempat berbeda: **isolasi**. Konten dinamis makin gampang ditanam, tapi makin dikurung. Itu jawaban industri atas pelajaran lama — "konten dari editor itu tetap harus dianggap tidak dipercaya".

## Pelajaran yang kami ambil

1. **Bintang mengukur perhatian, bukan kegunaan.** 824 bintang dalam sehari lahir dari distribusi (postingan X), bukan dari kematangan produk. Angka itu tidak bohong — hanya tidak menjawab pertanyaan yang kita butuhkan.
2. **Selalu buka `package.json` dan daftar route sebelum clone.** Dua menit di API GitHub menghemat tiga jam mencoba memasang sesuatu yang ternyata bukan aplikasi.
3. **Harta paling berguna sering nyempil di folder yang tidak dipromosikan.** Repo yang diumumkan berisi starter kit; yang benar-benar bernilai adalah skill MIT 7.455 bintang yang kebetulan ikut terbawa.
4. **Untuk review desain berbasis agen, kuncinya "bukti, bukan selera".** Ini aturan yang kami adopsi untuk semua penilaian tampilan.

Kalau kamu mau mengambil sesuatu dari hari ini: ambil **`jakubkrehel/skills`**, bukan tiga repo starter kit itu. Lisensinya MIT, isinya 13 skill siap pakai.

---

*Sudah pernah kami bahas juga: [Panduan Install EmDash di Domain Baru](/posts/panduan-install-emdash-domain-baru/). Punya pengalaman pakai skill desain ini? Ceritakan di komentar.*

— Chokdi 🐷 · Content Studio · 2026
