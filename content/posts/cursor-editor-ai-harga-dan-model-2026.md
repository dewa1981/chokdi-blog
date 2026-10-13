---
title: "Cursor 2026: Editor AI + Cloud Agent, Ini Harga & Daftar Modelnya"
date: 2026-10-14T00:05:00+07:00
draft: false
tags: ["AI", "Tutorial", "Coding"]
---

Cursor itu apa sih? Singkatnya: editor kode dengan AI sebagai mesin utama, bukan tempelan chat. Versi Oktober 2026 jauh lebih besar dari itu — ada cloud agent yang jalan di VM sendiri, code review otomatis, sampai CLI headless untuk CI. Artikel ini merangkum harga terbaru, daftar modelnya, dan jawaban jujur untuk satu pertanyaan yang sering muncul: bisa dipakai pakai DeepSeek nggak?

## Apa Itu Cursor — Versi Pendeknya

Cursor dibangun dari VS Code, jadi shortcut, ekstensi, dan tema tetap familiar. Yang membedakan ada di lapisan atasnya:

- **Agent mode** — mengerjakan tugas berantai: baca repo, edit banyak file, jalankan test, buat PR.
- **Tab completion** — saran lintas-baris yang mengikuti pola kode proyek.
- **Cloud Agents** — agent yang jalan di mesin cloud, lepas dari laptopmu.
- **Bugbot & Origin** — review pull request otomatis plus hosting kode bawaan.
- **Customize** — Rules (`.cursor/rules/*.mdc`), Skills, Subagents, Hooks, MCP, Plugin.
- **CLI & headless** — bisa dijalankan dari terminal dan CI, bukan hanya dari GUI.

Konsepnya mirip agent CLI seperti Claude Code atau Codex — bedanya Cursor menaruh semuanya di satu editor dengan diff visual.

## Harga Cursor (per Oktober 2026)

Halaman resmi Cursor sekarang menampilkan satu tangga paket untuk perorangan dan tim:

| Paket | Harga | Catatan |
|---|---|---|
| Free | $0/bulan | Request agent & chat terbatas |
| Plus | $8/bulan | Hanya model Grok |
| Premium | $30/bulan | 4x kuota Plus — paket paling populer |
| Super | $100/bulan | 15x kuota Plus |
| Ultra | $200/bulan | 50x kuota Plus, akses model paling awal |
| Teams | $30+/user/bulan | Pooled usage, analitik, kontrol admin |
| Enterprise | Custom | Kontrol jaringan, audit log, SSO, invoice |

Dua hal yang sering bikin kaget pemakai baru:

1. **Cloud agents baru terbuka dari paket Premium ke atas.** Di Free dan Plus, fitur itu ditandai garis datar alias tidak tersedia.
2. **Kuota penyegaran mingguan**, jadi satu hari boros tidak langsung menghabiskan jatah sebulan. Kalau tetap habis, kamu bisa top-up on-demand dengan tarif API yang sama — kualitas dan kecepatan request tidak diturunkan.

Dokumentasi Cursor juga menyebut varian kursi tim: Teams Standar sekitar $40/user/bulan dan kursi Premium sekitar $120/user/bulan (5x batas agent). Untuk perbandingan nyata: pemakai agent harian biasanya jatuh di total **$60–100 per bulan**, sementara power user yang menjalankan banyak agent dan automasi sering lewat **$200 per bulan**.

## Dua Kolam Model — Ini yang Paling Menentukan Biaya

Cursor punya dua kolam kuota terpisah, dan keduanya di-reset mengikuti siklus tagihan bulanan:

- **Cursor Models** — kuota besar untuk model rumah sendiri: Grok 4.7, Grok 4.6, Grok 4.5, dan Composer 2.5.
- **Other Models** — model pihak ketiga, ditagih mengikuti harga API model tersebut.

Harga per satu juta token (input / output) untuk beberapa model yang paling sering dipakai:

| Model | Input | Output |
|---|---|---|
| Composer 2.5 | $0,50 | $2,50 |
| Grok 4.7 | $2 | $6 |
| Claude Sonnet 5.5 | $2 | $10 |
| Claude Opus 5.5 | $4 | $20 |
| Claude Fable 5.1 | $10 | $50 |
| Gemini 3.8 Flash | $0,75 | $3,50 |
| GPT-5.6 Sol | $4 | $20 |
| GPT-5.6 Luna | $0,20 | $1,20 |

Di paket Teams dan Enterprise, request ke model pihak ketiga masih dikenai **Cursor Token Rate $0,25 per juta token** di atas harga API model. Model Cursor sendiri (Grok dan Composer) bebas dari biaya tambahan ini. Kesimpulannya sederhana: kalau sensitif biaya, Composer dan Gemini Flash jauh lebih murah daripada Opus atau Fable.

## "Bisa Dipakai Pakai DeepSeek Nggak?"

Tidak ada DeepSeek di daftar model Cursor. Daftar modelnya berisi keluarga Grok, Anthropic (Sonnet, Opus, Fable, Haiku), Google (Gemini), OpenAI (GPT-5.6 Sol/Terra/Luna), dan Muse Spark. Paket termurah — Plus — bahkan hanya membuka model Grok.

Ada dua jalur kalau kamu memang ingin DeepSeek:

- **BYOK** — didukung, tapi dikenakan Cursor Token Rate dan kontrolnya lebih masuk akal di paket tim/enterprise, bukan paket personal.
- **Jalur terpisah** — biarkan Cursor untuk pekerjaan di dalam editor, dan taruh DeepSeek di agent CLI sendiri lewat gateway OpenAI-compatible. Pola ini yang kami pakai sehari-hari: satu CLI agent yang bisa menunjuk ke banyak provider, lengkap dengan catatan biaya per project.

## Cloud Agent: Bagian yang Paling Berubah

Cloud Agent adalah agent yang tidak berjalan di laptopmu. Dia menempati VM Ubuntu terisolasi milik Cursor, melakukan clone repo, bekerja di branch sendiri, lalu membuka pull request.

- **Bisa dinyalakan dari mana saja** — editor, web, Slack, mobile, atau API (buat agent, list run, stream event).
- **Environment & build** disiapkan di belakang layar, jadi agent mulai dengan dependency siap, bukan repo mentah.
- **Beberapa agent paralel** jalan sekaligus, masing-masing di VM dan branch sendiri.

Batasnya juga perlu jujur disebut: cerita agent berhenti di pull request, bukan sampai produksi. Kode diproses di infrastruktur milik Cursor, command terminal dijalankan otomatis (pintu masuk risiko prompt injection), dan audit trail lengkap baru ada di paket enterprise. Untuk tugas yang butuh akses database produksi, agent cloud bukan tempatnya.

## Jadi, Cursor atau Agent CLI?

Pakai Cursor kalau kerjamu banyak di editor: menilai diff, mengubah UI, debugging visual, dan kamu ingin cloud agent yang jalan sendiri sambil kamu tidur. Pakai agent CLI kalau tugasnya "satu perintah, satu hasil", ingin bayar per token tanpa langganan tetap, dan ingin bebas memilih provider — termasuk DeepSeek. Banyak developer akhirnya memakai keduanya: CLI untuk tugas yang jelas, editor untuk eksplorasi dan penilaian akhir.

Kalau penasaran dengan ekosistem agent CLI, dua tulisan kami sebelumnya bisa jadi lanjutan: [Termany: terminal agent native](/posts/termany-terminal-agent-native/) dan [AGENTS.md vs GEMINI.md vs CLAUDE.md](/posts/agents-md-vs-gemini-md-vs-claude-md/). Untuk yang ingin menjalankan model lokal gratis di editor, ada juga [Qwen 27B di VS Code](/posts/qwen27b-vscode-gratis/).

Menurutmu, $20–30 per bulan untuk agent yang menulis kode itu worth it — atau lebih baik bayar per token saja? Tulis di komentar, jawabannya biasanya tergantung seberapa sering kamu butuh agent berjalan tanpa ditunggui.

— Chokdi 🐷 · Content Studio · 2026
