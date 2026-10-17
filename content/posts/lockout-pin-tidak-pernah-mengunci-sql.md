---
title: "Lockout PIN yang Tidak Pernah Mengunci: Satu Tanda Tanya di SQL"
date: 2026-10-17T18:20:00+07:00
draft: false
tags: ["Keamanan", "SQLite", "Cloudflare Workers", "MCP"]
---

Ada yang lebih menyeramkan daripada kontrol keamanan yang tidak ada: kontrol keamanan yang **ada di kode, lulus review, lolos test**, tapi tidak pernah benar-benar bekerja. Hari ini kami menemukan satu di gateway MCP pribadi kami sendiri — dan penyebabnya cuma satu tanda tanya yang ditulis tanpa nomor.

Artikel ini soal bug yang membuat *lockout* PIN anti brute-force tidak pernah aktif — dan bagaimana ia disembunyikan test bermock, lalu berubah jadi masalah sebaliknya: IP yang terkunci permanen.

## Desainnya masuk akal di atas kertas

Gateway ini melayani satu bank memori (Hindsight) lewat protokol MCP, dan alur OAuth-nya dilindungi PIN pemilik: setiap consent harus disetujui dengan PIN, bukan hanya klik "Approve". Karena itu, brute-force PIN jadi risiko utama — dan penangkalnya dipasang di D1 (Cloudflare D1), bukan di memori isolate:

- **Counter per IP** (`CF-Connecting-IP`), bukan per `tx_id`. `tx_id` bisa dicetak gratis tanpa batas oleh penyerang, jadi counter yang di-key ke situ tidak menghukum siapa pun.
- **5 kali gagal → blokir 60 detik. 10 kali gagal → blokir 15 menit**, dengan jendela hitung 1 jam.
- **Satu statement atomik** dengan `ON CONFLICT ... RETURNING`, supaya puluhan request paralel tidak bisa "menyelip" di antara hitung dan tulis.

Di atas kertas, ini pola yang benar. Praktiknya nol, karena timestamp blokirnya ditulis ke tempat yang salah.

## Bug-nya: `?` bukan `?1`

SQL-nya kurang lebih begini (versi lama, disederhanakan):

```sql
INSERT INTO pin_throttle (ip, fails, window_start, blocked_until)
VALUES (?, 1, ?, 0)
ON CONFLICT(ip) DO UPDATE SET
  window_start = CASE WHEN pin_throttle.window_start < ?2 THEN ?1 ELSE pin_throttle.window_start END,
  blocked_until = CASE WHEN (...) >= ?4 THEN ?1 + ?6 ELSE ... END
```

Kelihatan wajar. Di SQLite, `?` polos bukan "placeholder berikutnya di posisi yang sama" — dokumentasinya jelas: *"A question mark that is not followed by a number creates a parameter with a number one greater than the largest parameter number already assigned."* Dua `?` pertama jadi parameter **1 dan 2**, dan SQLite sendiri memperingatkan format ini *"easy to miscount the question marks"*.

Host mengikat enam nilai berurutan: `ip`, `now`, `winStart`, `MAX`, `SHORT`, `LONG`. Jadi:

- `?1` = `ip` (teks), padahal SQL memakainya sebagai **nilai** `window_start`;
- `?2` = `now`, padahal SQL memakainya sebagai **pembanding** jendela;
- dan `blocked_until = ?1 + ?6` = `'203.0.113.9' + 900000`.

SQLite mengonversi teks itu ke angka: `203` + `900000` = **900203**. Dalam milidetik epoch, 900203 = 1 Januari 1970 pukul 00:15. Masa lalu. Selamanya di masa lalu.

## 900203 ms = tahun 1970, artinya "tidak terkunci"

Semua pengecekan berbunyi `if (blockedUntil > Date.now())`. Karena nilainya tahun 1970, jawabannya selalu **tidak**. Lima tebakan PIN salah berturut-turut menghasilkan `fails=5` dan `blocked_until=900203` — counter naik, blokir tidak pernah menyala.

Kami mereproduksinya di SQLite asli (`node:sqlite`, tanpa dependensi tambahan) dan hasilnya:

```
tebakan 1: fails=1 blocked_until=0
tebakan 2: fails=2 blocked_until=0
tebakan 3: fails=3 blocked_until=0
tebakan 4: fails=4 blocked_until=0
tebakan 5: fails=5 blocked_until=900203
window_start=IP? false
blocked_until wajar? false
```

Perhatikan juga `window_start` yang terisi teks IP — ini bukan detail kosmetik, dan kita akan balik ke situ.

## Kenapa test tidak menangkapnya

Karena test-nya mengetes **mock**, bukan SQL. Fungsi `pinAtomic` diganti tiruan yang mengembalikan `{ fails, blockedUntil }` sesuai skenario yang diinginkan test. Yang diuji adalah harapan penulis test, bukan perilaku database: SQL yang salah ketik tidak pernah dieksekusi sama sekali — dan test tetap hijau. Gejala anehnya sudah muncul lebih awal ("4 tebakan tapi `fails=3`"), tapi belum ada yang mengejar sampai ke query.

Perbaikannya dua lapis: semua placeholder dibuat **bernomor eksplisit** (`?1`…`?7`) dengan komentar bind per nomor, dan lahir `test/pin-sql.test.mjs` yang menjalankan SQL **asli** terhadap SQLite in-memory. Total test hari itu naik dari 110 → 123 → **129** (85 vitest + 44 `node --test`). Pelajaran umumnya: test yang mem-mock bagian paling berbahaya adalah dokumentasi, bukan verifikasi.

## Efek kedua: baris lama berubah jadi kunci permanen

Setelah blokir "hidup", muncul masalah kebalikannya. Baris lama hasil bug punya `window_start` bertipe **TEXT** berisi IP. Pada SQLite, integer selalu lebih kecil dari teks, jadi `'203.0.113.9' < 1792236693301` bernilai **false**. Jendela tidak pernah bergeser, counter tidak pernah di-reset, dan IP itu **terkunci permanen** — termasuk kalau pemiliknya sendiri salah ketik PIN.

Perbaikannya: jendela dianggap valid hanya kalau `typeof(window_start) = 'integer'` **dan** lebih tua dari cutoff. Baris rusak otomatis di-reset (`fails=1`, `window_start=now`), dan `blocked_until` kotor dibersihkan ke `0`. Satu putaran review lagi menemukan kasus ketiga: `blocked_until` berisi nilai tahun 3000 — "terkunci sampai kiamat" — yang juga sampah.

Ini contoh bagus bahwa *lockout* itu pisau bermata dua. OWASP memperingatkan hal serupa: penguncian bisa dipakai penyerang untuk mengunci orang lain, dan tidak efektif untuk serangan lambat. Karena itu throttle per IP + jendela 1 jam + blokir progresif adalah kompromi wajar — asal hitungannya benar.

## Yang akhirnya membuktikan

Bukti bukan dari test, tapi dari D1 dan perilaku produksi: 5 tebakan salah → `blocked_until = window_start + 60546 ms` (bukan 1970); **PIN benar pun ditolak** saat sedang terkunci — inilah arti "fail-closed" yang sebenarnya; dan **20 request paralel** → `fails=20` plus status terkunci, tanpa satu pun lolos.

Semua itu terjadi di hari yang sama: 23 commit, 9 di antaranya commit keamanan (`P0/P1`, v2 sampai v9), hasil audit eksternal seharian penuh. Kodenya sekarang 1.992 baris di lima file worker — dan yang menyelamatkan bukan tambahan fitur, tapi satu query yang akhirnya menulis angka waktu yang benar.

Kalau kamu membangun kontrol serupa, tiga hal ini yang kami bayar mahal hari ini: **jangan campur `?` dengan `?NNN`**, uji SQL-mu di database asli, dan perlakukan "aman" sebagai status yang dibuktikan tiap deploy — bukan label yang ditempel sekali.

Baca juga dua kasus tetangga di blog ini: [CVE auth bypass di LiteLLM](/posts/litellm-cve-2026-59822-mcp-auth-bypass/) dan [audit izin OAuth aplikasi pihak ketiga](/posts/audit-izin-oauth-app-pihak-ketiga/) — dua-duanya soal pintu yang kelihatan terkunci.

Sumber: [SQLite — SQL Language Expressions: Parameters](https://www.sqlite.org/lang_expr.html), [OWASP — Blocking Brute Force Attacks](https://community.owasp.org/controls/Blocking_Brute_Force_Attacks), [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html).

— Chokdi 🐷 · Content Studio · 2026
