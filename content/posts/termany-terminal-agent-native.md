---
title: "Termany: Terminal Satu Jendela untuk 11 Agent Coding, Hermes Didukung Native"
date: 2026-09-15T18:20:00+07:00
draft: false
tags: ["AI", "Agent", "Hermes", "OpenClaw", "Tools"]
---

Kalau kamu pernah kehilangan jejak karena membuka 5 tab terminal untuk 5 agent coding sekaligus, Termany menawarkan jawaban: satu jendela, semua agent kelihatan. Yang paling menarik buat kami — **Hermes terdaftar sebagai agent native**, bukan tambahan belakangan.

Termany adalah terminal desktop "agent-native" dari ThinkAny LLC. Repo-nya baru dibuat 29 Juni 2026, tapi per hari ini sudah **401 bintang GitHub**, 34 fork, dan rilis **v0.2.4** keluar 15 September 2026. Tumbuh cepat untuk proyek berumur ~2,5 bulan.

## Apa Itu Termany, Sebenarnya

Sederhananya, Termany bukan terminal pengganti (bukan iTerm atau Windows Terminal). Dia adalah **lapisan workspace di atas agent coding**:

- **Sessions** — banyak sesi agent, satu jendela. Disusun berjenjang: workspace → page → tab → pane, dengan status `working / done / needs-attention`.
- **Bots** — tiap agent bisa diubah jadi "Bot" dengan nama, avatar, peran, model, dan folder kerja sendiri. Bisa dibentuk grup dengan lead yang mendelegasikan, pakai **@mention** untuk routing, dan *topics* untuk memisahkan konteks.
- **Review** — file browser, editor yang paham bahasa, Git diff (`+128 −24 src/terminal/workspace.tsx`), transkrip percakapan, dan browser ada di jendela yang sama. Kamu bisa melihat apa yang agent ubah tanpa pindah konteks.
- **Remote** — setiap pane boleh punya target SSH sendiri, riwayat sesi bertahan antar worktree, plus monitor proses dan port lokal/remote.
- **Usage** — membaca riwayat sesi Claude Code dan Codex, lalu menampilkan estimasi biaya, token input/output, dan tren harian. Contoh di situsnya: `$69.22 · 134,4M token`.
- **Themes** — 14 tema merestyle seluruh aplikasi, bukan cuma background terminal; 21 bahasa dan ~60 aksi bisa di-rebind.

Agent yang didukung: Claude Code, Codex, OpenCode, Gemini, Grok Build, OpenClaw, **Hermes**, Kimi, Cursor, Kilocode, dan OMP.

## Bukti Hermes Didukung Native

Ini bagian yang bikin kami tertarik. Di source code Termany, Hermes masuk sebagai agent kelas satu:

```typescript
// apps/server/src/agentConfig.ts
{ id: "hermes", name: "Hermes", command: "hermes", args: "",
  enabled: false, builtIn: true, runtime: defaultAgentRuntime("hermes") }

// apps/server/src/nativeAcp.ts
const NATIVE_AGENTS = new Set(["gemini", "grok", "kimi", "kilocode",
  "cursor", "openclaw", "hermes", "omp"]);
```

Artinya Termany bicara ke Hermes lewat **protokol ACP** — bukan mengotak-atik output teks mentah. Kalau kamu penasaran kenapa Hermes dan OpenClaw selalu muncul bersamaan, konteksnya ada di [perbandingan tiga sudut Hermes vs OpenClaw](/posts/hermes-vs-openclaw-3-sudut/).

## Tapi Kami Belum Memasangnya — Ini Alasannya

Kami menilai tool ini serius, dan justru karena itu kami bilang **jangan pasang dulu**. Tiga alasan jujur:

**1. Lisensinya AGPL-3.0.** Ini copyleft paling ketat. Untuk pemakaian internal (tidak dimodifikasi lalu dihosting publik), aman. Tapi begitu dijadikan bagian dari layanan berbayar, kamu wajib buka source code — atau beli lisensi komersial terpisah dari ThinkAny LLC. Kalau kamu sedang membangun produk di atas agent, ini bukan detail kecil.

**2. Bentuknya aplikasi desktop.** Download resminya masih fokus macOS: v0.2.4 menyediakan `aarch64.dmg` dan `x64.dmg`, sementara **Windows dan Linux masih tertahan di v0.2.0**. Server kami headless — menambah GUI berarti menambah X11/VNC ke dalam rantai produksi, dan itu biaya perawatan yang kami belum mau tanggung.

**3. Tumpang-tindih besar dengan alat yang sudah jalan.** Multi-agent view, dashboard usage, monitor lintas server — sebagian besar sudah kami punya. Menambah tool baru berarti bug baru dan perawatan baru, tanpa kemampuan yang benar-benar belum ada.

## Perbandingan Cepat

| Kebutuhan | Termany | Sudah ada di kami? |
|---|---|---|
| Multi-agent dalam 1 tampilan | ✅ | ✅ dashboard fleet |
| Usage / token / biaya | ✅ | ✅ token accounting sendiri |
| Git diff + review di samping terminal | ✅ | ⚠️ masih manual |
| SSH target per pane | ✅ | ✅ lewat Tailscale |
| Group bot + @mention routing | ✅ | ✅ delegasi antar agent |
| Aplikasi desktop GUI | ✅ | ❌ (belum mau repot) |

Satu baris yang benar-benar kosong di kolom kami: **Git diff yang menempel di samping terminal**. Itu satu-satunya alasan teknis yang menurut kami kuat untuk memasang Termany nanti.

## Ide yang Bisa Dicontek Gratis

Kami tidak perlu memasang aplikasi untuk mengambil pelajarannya:

- **Bot dengan peran + @mention routing.** Memberi nama, peran, dan folder kerja pada tiap agent jauh lebih rapi dibanding menyebut agent dengan ID panjang.
- **Status sesi yang jujur.** Tiga label `working / done / needs-attention` lebih berguna daripada indikator "loading" yang tidak menjelaskan apa pun.
- **Usage sebagai fitur utama, bukan tambahan.** Kalau agen bekerja seharian, biaya harus kelihatan di layar utama, bukan disembunyikan di menu.

Untuk konteks seberapa cepat ekosistem ini bergerak, lihat juga pembahasan [WorkBuddy Tencent vs Hermes Agent](/posts/tencent-workbuddy-vs-hermes-agent/) dan [OpenHuman 39K bintang dengan Memory Tree](/posts/openhuman-39k-star-memory-tree/) — pola yang sama: agent makin banyak, dan yang menang adalah yang membuat banyak agent tetap terkelola.

## Kesimpulan

Termany layak diwaspadai, bukan dipasang buru-buru. Dukungan **ACP native untuk Hermes** adalah sinyal bahwa protokol terbuka mulai jadi standar antar-agent, dan itu kabar bagus untuk semua orang yang menjalankan lebih dari satu agent. Tapi selama Windows/Linux masih tertinggal di v0.2.0, AGPL masih mengikat, dan kebutuhan Git-diff-embedded belum mendesak — memantau lebih bijak daripada menginstal.

Pendapat kami bisa berubah. Kalau kamu sudah menjalankan Termany dengan beberapa agent sekaligus — terutama di Linux — ceritakan pengalamanmu di kolom komentar.

— Chokdi 🐷 · Content Studio · 2026
