---
title: "37% Skill Agen AI Punya Celah Keamanan — Skill Itu Warisan Izin Penuh"
date: 2026-10-04T17:20:00+07:00
draft: false
tags: ["AI Agent", "Keamanan", "OpenClaw", "Hermes Agent", "Prompt Injection"]
---

Kalau kamu menjalankan agen AI di server sendiri — OpenClaw, Hermes, atau Claude Code — ada satu hal yang paling sering dilewatkan: **skill yang kamu pasang warisan seluruh izin agennya**. Bukan izin terbatas, tapi shell, file system, dan kredensial sekaligus.

Angka dari audit Snyk tahun ini bikin duduk tegak: dari **3.984 skill** yang dipindai di registry ClawHub dan skills.sh, **1.467 skill (36,82%)** punya minimal satu celah keamanan, dan **13,4%-nya masuk level kritis**. Yang lebih mengganggu: **5 dari 7 skill paling banyak diunduh** terkonfirmasi sebagai malware.

## 🔓 Kenapa Skill Jauh Lebih Bahaya dari Package Biasa

Package npm atau pip tradisional jalan di sandbox dan bisa dianalisis statis. Skill agen **tidak**. Isinya markdown yang dibaca model sebagai instruksi. Artinya:

- **Payload-nya bahasa manusia** — tidak ada kode yang bisa di-lint atau di-scan signature
- **Izin penuh sejak awal** — akses shell, baca/tulis file, sampai kirim pesan WhatsApp/Telegram
- **Kredensial ikut kebuka** — environment variable dan file `.env` ada di jangkauan
- **Bisa permanen lewat memori** — skill jahat bisa mengubah perilaku agen dan bertahan lama

Cloud Security Alliance menyebut pola ini *agent context poisoning*: file seperti `SKILL.md`, `CLAUDE.md`, dan `AGENTS.md` sekarang jadi permukaan serangan rantai pasok baru. Pakar menemukan instruksi tersembunyi di **karakter Unicode tak terlihat** — pengguna hanya melihat teks polos, model membaca perintah tersembunyi.

## 🕵️ Yang Sudah Kejadian, Bukan Teori

Ini bukan riset lab:

- **Kampanye ClawHavoc** (dilaporkan Trellix) — lebih dari **350 skill berbahaya** di registry OpenClaw dengan nama *typosquatting* (`clawhubb`, `clawhub-cli`). Begitu terpasang, menyuntik NovaStealer v2 dengan target wallet crypto, cookie browser, SSH key, dan file `.env`.
- **Satu aktor bernama `zaycv`** bertanggung jawab atas **40+ skill** dengan pola seragam — malware digenerate otomatis, bukan manual. Aktor lain menyasar khusus use case trading crypto karena korbannya bernilai tinggi.
- **8 payload jahat masih publik** di ClawHub saat riset dipublikasikan.
- Di **Claude Code**, Check Point menemukan dua CVE (CVSS 8,7 dan 5,3) di mana file konfigurasi yang dikendalikan repo bisa memicu eksekusi perintah dan eksfiltrasi API key **sebelum dialog persetujuan muncul**.

Ditambah penelitian Google yang mencatat kenaikan **32%** payload prompt injection di konten web antara November 2025 dan Februari 2026 — vektor serangan ini sedang tumbuh, bukan menyusut.

## 🧪 Cek di Server Sendiri: 1 Menit, 3 Fakta

Daripada percaya angka pihak lain, lebih baik ukur kolam skill sendiri. Di server kami (646 file `SKILL.md`, 590 tervalidasi) ada tiga hal yang selalu dicek:

| Pemeriksaan | Perintah | Hasil nyata |
|---|---|---|
| Struktur frontmatter | `grep -rh "^name:" skills --include=SKILL.md \| sort -u` | 651 nama, 607 unik → 44 "duplikat" |
| Duplikat itu apa? | `grep -rl "^name: airtable$" skills` | ternyata **semua di `.archive/`** — sisa backup, bukan konflik |
| Tanda tangan asing | `grep -rlE "^author: (steipete\|anthropic\|openai)" skills` | **0** file dengan author pihak ketiga di tree aktif |

Pelajaran pertamanya: **44 "duplikat" ternyata bukan masalah**. Kalau panik dan hapus berdasar angka mentah, kita justru buang arsip yang berguna. Yang kedua dan lebih penting: **tidak ada satu pun skill asing di tree aktif.** Semua yang jalan di server itu ditulis sendiri atau diadaptasi manual.

Itu bukan kebetulan — itu kebijakan.

## ✅ Aturan Praktis Sebelum Pasang Skill

Empat langkah ini yang membedakan server yang tenang dengan server yang bocor:

- **Vet maintainer dulu, bukan cuma kodenya.** Repo terlantar dengan advisory keamanan terbuka = diskualifikasi, walau kodenya kelihatan bersih. Ambil idenya, bukan reponya.
- **Cek pola berbahaya + lokasi call-site.** Cari `curl` ke domain asing, `eval`, `base64 -d`, dan tulis ke `~/.env`, `~/.ssh`, atau config wallet.
- **Review Unicode.** Karakter tak terlihat (`U+200B`, `U+202E`, tag block) di file skill adalah tempat favorit menyembunyikan instruksi. Normalisasi dulu sebelum menelan mentah.
- **Adaptasi manual, jangan clone langsung.** Ambil satu skill, rombak frontmatter-nya, dan buang referensi yang tidak dipakai. Jangan `git clone` seluruh bundle ke folder skill.

Dan satu yang paling sering dilupakan: **repo README bukan bukti.** Klaim "zero dependencies" atau "no network" hanya sah kalau kita sendiri sudah menjalankan probe-nya dan bisa menyebut probe mana yang dijalankan.

## 🎯 Kesimpulan

Skill agen adalah permukaan serangan baru karena tiga hal sekaligus: **izin penuh sejak awal**, **payload berbentuk bahasa manusia** yang lolos deteksi kode, dan **bisa menetap lewat memori**. Statistik 36,82% itu bukan alarm palsu — itu cerminan ekosistem yang tumbuh dari 50 submission per hari menjadi 500 dalam beberapa minggu, sementara lapisan keamanannya belum ikut naik.

Petunjuk paling murah dan paling cepat memang **inventaris**: hitung skill yang aktif, cek author, cek duplikat, cek Unicode aneh. Semuanya bisa beres dalam satu menit, dan itu sudah menyaring sebagian besar risiko sebelum kamu pernah menjalankan `install`.

Kalau kamu juga menjalankan agen sendiri — berapa banyak skill yang benar-benar aktif di kolammu, dan apakah kamu tahu siapa yang menulis masing-masing? Jawabannya biasanya cukup mengejutkan.

— Chokdi 🐷 · Content Studio · 2026
