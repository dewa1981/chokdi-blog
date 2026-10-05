---
title: "AGENTS.md vs GEMINI.md vs CLAUDE.md: Cara Ngunci Agent AI Biar Kerjaannya Nggak Melenceng"
date: 2026-10-05T23:05:00+07:00
draft: false
tags: ["AI Agent", "Hermes", "Tutorial", "Produktivitas"]
---

Kalau kamu pakai lebih dari satu agent AI — atau satu agent untuk beberapa proyek sekaligus — kamu pasti pernah mengalami ini: **agent-nya lupa aturan, kerja di proyek yang salah, atau tanya hal yang sebenarnya sudah pernah kamu jelaskan.**

Solusinya bukan "ingat-ingat terus". Solusinya **file instruksi**. Dan hampir setiap agent AI modern punya file seperti itu — cuma namanya beda-beda.

## Peta file instruksi per alat

Ini yang bikin bingung kalau kamu pakai beberapa alat sekaligus:

| Alat | File per-proyek | File global (selalu kebaca) |
| --- | --- | --- |
| **Gemini CLI** | `GEMINI.md` | `~/.gemini/GEMINI.md` |
| **Grok / xAI CLI** | `AGENTS.md` | — |
| **Claude Code** | `CLAUDE.md` | `~/.claude/CLAUDE.md` |
| **OpenAI Codex** | `AGENTS.md` | `~/.codex/AGENTS.md` |
| **Cursor** | `.cursor/rules/*.mdc` | — |
| **Hermes Agent** | `.hermes.md` / `AGENTS.md` | `~/.hermes/AGENTS.md` |

**Pola umumnya sama di semua alat:** file di **direktori kerja** = aturan proyek; file di **home** = aturan pribadi/global. Yang beda cuma nama file dan jumlah tingkatannya.

`AGENTS.md` sudah jadi semacam standar tidak resmi (Codex, Grok, dan Hermes membacanya). Gemini memilih `GEMINI.md` sendiri; Claude `CLAUDE.md`. Cursor paling beda — pakai folder aturan berformat MDC.

## Urutan prioritas di Hermes

Di Hermes, kalau ada beberapa file di folder yang sama, yang menang berurutan:

1. **`.hermes.md`** — paling menang, menimpa semua
2. `AGENTS.override.md`
3. `AGENTS.md`
4. `CLAUDE.md` (huruf besar menang atas `claude.md`)
5. `HERMES.md`

Selain itu, `SOUL.md` (identitas agent) dan `MEMORY.md` + `USER.md` (memori) **selalu** ikut dan tidak bisa dimatikan per-proyek.

## Pola 3 lapis: cara memakainya untuk banyak proyek

Kalau satu agent mengerjakan beberapa proyek yang mirip tapi tidak boleh tercampur (misalnya dua brand berbeda dalam satu sistem pembayaran), satu file saja tidak cukup. Susunannya:

**Lapis 1 — Global (`~/.hermes/AGENTS.md`)**
Selalu kebaca, dari mana pun agent dijalankan. Isinya: daftar proyek, folder masing-masing, aturan persilangan, dan **"proyek ini BUKAN proyek itu"** secara eksplisit.

**Lapis 2 — Per proyek (`<folder-proyek>/AGENTS.md`)**
Kebaca otomatis **kalau** direktori kerja agent ada di folder itu. Isinya: berkas apa saja yang ada, mana yang kredensial, larangan spesifik, dan alamat detailnya.

**Lapis 3 — Skill**
Pengetahuan yang dipakai tiap kali topiknya muncul, tidak peduli direktorinya di mana. Ini jaring terakhir, dan yang paling tahan lama karena ikut ter-load saat topiknya relevan.

**Kenapa harus 3?** Karena tiap lapis punya titik buta:
- Global selalu ada, tapi tidak bisa memuat detail semua proyek (kepanjangan).
- Per-proyek detail, tapi hanya kebaca kalau agent benar-benar berada di folder itu.
- Skill kebaca lintas folder, tapi baru muncul kalau topiknya disebut.

## Cara membuktikan file-nya benar-benar dibaca (bukan cuma ditulis)

Di sinilah banyak orang salah: menulis `AGENTS.md`, lalu **menganggap** agent membacanya. Jangan berasumsi — uji.

Hermes punya fungsi internal yang membangun "instruction context" dari direktori kerja. Panggil langsung dan lihat hasilnya:

```
from agent.prompt_builder import build_context_files_prompt
r = build_context_files_prompt(cwd="/opt/data/proyek-saya", skip_soul=True)
print(len(r), "char")
print("AGENTS.md termuat:", "AGENTS.md" in r)
```

Hasil uji nyata di server kami:

| Direktori kerja | Karakter termuat | File termuat? |
| --- | --- | --- |
| `~/.hermes` (global) | 9.168 | ✅ ya |
| `/opt/data/oasis_ops` | 3.060 | ✅ ya |
| `/opt/data/mplay_ops` | 2.933 | ✅ ya |
| `/opt/data/bo_ops` | 3.339 | ✅ ya |
| `/tmp` (kontrol) | 0 | ✅ benar, tidak ada aturan nyasar |

Baris terakhir itu penting: **adanya file di folder lain tidak "bocor"** ke pekerjaan yang tidak berkaitan. Uji negatif seperti ini yang membuktikan isolasi benar-benar bekerja.

### Jebakan saat menguji

Kalau kamu memanggil fungsi internal itu dari luar runtime-nya, kamu bisa kena error modul yang tidak lengkap (contoh nyata: `ModuleNotFoundError: No module named 'ruamel'`). Solusinya sederhana — modul-modul itu ada di cache paket, tinggal tambahkan ke jalur impor:

```
PYTHONPATH=/root/.cache/uv/archive-v0/<hash> python -c "..."
```

Atau lebih rapi: jalankan lewat interpreter yang memang dipakai aplikasinya.

## Yang sering bikin agent tetap melenceng (walau file sudah ada)

Empat penyebab, semuanya pernah kami alami:

1. **File-nya di folder yang tidak pernah jadi direktori kerja.** Kamu menulis peraturan proyek di `proyek/AGENTS.md`, tapi agent selalu jalan dari home. Solusinya: ringkas poin krusialnya di file global.
2. **Aturan ditulis sebagai narasi, bukan larangan eksplisit.** Riset terhadap ribuan repositori menemukan bahwa **86% file instruksi agent terbaik memuat minimal satu aturan "JANGAN"** yang tegas. "Sebaiknya hati-hati" tidak bekerja; "JANGAN ubah logika transfer" bekerja.
3. **Tidak ada daftar "ini bukan proyek itu".** Batas paling efektif bukan daftar hal yang boleh, tapi daftar hal yang **dilarang disentuh dari sini**.
4. **Instruksi baru tidak dicatat.** Setiap kali user memberi fakta baru (alamat server, path, jadwal), kalau tidak langsung ditulis ke file instruksi/memori, ia akan hilang di sesi berikutnya.

## Pelajaran dari sisi kami

Kami memakai 3 lapis ini untuk mengunci beberapa proyek yang mirip tapi tidak boleh tercampur, plus satu aturan yang paling sering dilanggar:

> **Ambil memori dulu sebelum menjawab — jangan tanya balik, jangan bilang tidak tahu.**

Aturan itu ditulis eksplisit di file global setelah kami menyadari agent sering bertanya ulang hal yang sudah pernah dijelaskan (alamat server, path berkas, jadwal). Ternyata masalahnya bukan "agent bodoh" — masalahnya **aturannya tidak pernah ditulis di tempat yang selalu dibaca.**

## Kesimpulan

File instruksi itu murah: satu file markdown. Yang mahal adalah waktu yang habis karena agent mengerjakan hal yang salah, atau karena kamu harus menjelaskan ulang hal yang sama tiap hari.

Kalau kamu memakai beberapa agent AI sekaligus, mulailah dengan satu keputusan: **mana aturan yang harus selalu ada (global), mana yang spesifik per proyek, dan mana yang layak jadi pengetahuan lintas proyek.** Setelah itu, uji bahwa file-nya benar-benar dibaca — jangan percaya begitu saja.

---

*Sudah pernah kami bahas juga: [Panduan Install EmDash di Domain Baru](/posts/panduan-install-emdash-domain-baru/). Punya pengalaman ngunci agent pakai AGENTS.md? Ceritakan di komentar.*

— Chokdi 🐷 · Content Studio · 2026
