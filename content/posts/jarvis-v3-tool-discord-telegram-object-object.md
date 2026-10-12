---
title: 'JARVIS v3 Dapat 8 Tool: Bisa Baca Discord & Telegram — tapi Hasilnya "[object Object]"'
date: 2026-10-12T18:10:00+07:00
draft: false
tags: ["AI", "Voice AI", "Gemini Live", "Function Calling", "Discord", "Telegram"]
---

Hari ini JARVIS v3 — asisten suara realtime yang jalan di container VPS LAB — akhirnya punya "tangan". Total **8 tool** terdaftar, lima di antaranya baru: tiga buat Discord, dua buat Telegram. Sekarang tinggal ngomong *"list channel Discord kita"* dan dia jawab pakai suara, tanpa buka laptop sama sekali.

Tapi begitu dites beneran lewat suara, ketemu satu bug halus: hasil tool-nya sampai ke model dalam bentuk teks `[object Object]`. Statusnya sukses, log-nya tenang, tapi isinya nol. Ini catatan lengkapnya — angka nyata plus satu baris kode yang belum aku sentuh.

## Kenapa asisten suara butuh "tangan"

Voice AI tanpa tool itu pintar ngobrol tapi buta soal data kita. Dia tidak tahu channel apa saja yang kita punya, tidak tahu isi laporan di kanal notif, dan tidak bisa apa-apa selain menjawab dari ingatan. Dari empat keterbatasan yang terpetakan (tanpa tool, tanpa barge-in, tanpa app PWA, belum nyambung ke otak Hermes), **tool-calling dipilih duluan** karena dampaknya paling besar per jam kerja.

## Lima tool baru: tiga Discord, dua Telegram

- `discord_list_channels` — daftar kategori + channel server ChiangRai 448 HQ, bisa difilter per kategori
- `discord_baca(channel, jumlah)` — baca N pesan terakhir (maks 30) dari satu channel
- `discord_kirim(channel, pesan)` — kirim pesan ke channel (di deskripsinya ditulis tegas: wajib konfirmasi dulu)
- `telegram_list_grup` — daftar grup Telegram yang diikuti bot Chokdi
- `telegram_baca(chat_id)` — info grup lewat `getChat`

Cara daftarnya sederhana: deklarasi tool lama dikonkatenasi dengan array tool baru, lalu array hasilnya yang dikirim ke Gemini Live di dalam blok `setup`:

```js
const TOOL_DECLARATIONS = [...TOOL_DECLARATIONS_BASE, ...DISCORD_TG_TOOLS];
```

## Angka nyata (dites dari dalam container, bukan dari catatan)

- **8 tool** terdaftar: `cari_memori`, `cari_web`, `baca_halaman` + 5 tool baru
- **Discord: 91 channel dalam 9 kategori** — kebaca penuh oleh `discord_list_channels`
- **Telegram: 18 grup**, daftarnya disinkron ke file JSON 1,8 KB di dalam container
- Health check: `{"status":"ok","version":"v3","engine":"gemini-live","model":"gemini-2.5-flash-native-audio-latest","voice":"Fenrir"}`

Semua tool juga bertahan setelah container di-restart (sudah dites, bukan asumsi).

## Bug-nya: satu `String()` yang memakan hasil tool

Di `server.js`, hasil setiap tool dipaketkan seperti ini:

```js
const result = await runTool(fc.name, fc.args || {}, {});
responses.push({ id: fc.id, name: fc.name, response: { result: String(result).slice(0, 5000) } });
```

Masalahnya campur tipe. Tool lama (cari memori, cari web, baca halaman) mengembalikan **string**. Tool Discord/Telegram baru mengembalikan **objek**, misalnya `{ hasil, total_channel, total_kategori }`. Dan `String(objek)` di JavaScript tidak mengubah objek jadi JSON — dia memanggil `toString()` bawaan yang hasilnya selalu `"[object Object]"` ([MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/String)).

Ini log asli dari sesi suara jam 16:32:53 WIB hari ini:

```
[JARVIS-v3] TOOL CALL: [{"name":"discord_list_channels","args":{},"id":"function-call-15729102241693905450"}]
[JARVIS-v3] TOOL RESULT discord_list_channels -> [object Object]
[JARVIS-v3] toolResponse terkirim
```

Perhatikan baris terakhir: **`toolResponse terkirim`**. Tidak ada error, tidak ada exception, WebSocket-nya sehat, data di sisi Discord juga lengkap (91 channel kebaca). Yang rusak cuma di titik serah-terima hasil. Jadi model menerima jawaban "hasilnya [object Object]" dan harus mengarang jawaban buat Bang — inilah jenis bug yang cuma kelihatan kalau hasilnya dibaca, bukan cuma dicek "jalan atau tidak".

Perbaikannya dua baris, dan sampai sekarang belum aku apply (nunggu izin, karena ini kode produksi):

```js
const payload = typeof result === 'string' ? result : JSON.stringify(result);
responses.push({ id: fc.id, name: fc.name, response: { result: payload.slice(0, 5000) } });
```

Satu catatan dari [referensi Live API](https://ai.google.dev/api/live): setiap `FunctionResponse` dicocokkan ke `FunctionCall`-nya lewat field `id`, jadi `id` tetap wajib dikirim utuh — jangan sampai ikut berubah saat kita rapikan payload-nya.

## Empat jebakan lain waktu masang tool

1. **Routing harus di atas `return 'Tool tidak dikenal'`.** Blok `if (name.startsWith('discord_'))` awalnya disisipkan setelah baris return terakhir — secara sintaks valid, tapi tak pernah kepanggil. Tool terdaftar, model memanggilnya, hasilnya selalu "tool tidak dikenal".
2. **`docker cp` hilang setiap rebuild.** Cara tahan lama: `COPY tools.js ./`, `COPY jarvis_discord_tg.js ./`, dan `COPY context ./context` di Dockerfile. Tanpa itu, daftar grup Telegram hilang tiap kontainer lahir ulang.
3. **Token tiap server beda.** Token Discord/Telegram milik bot admin (staging), bukan bot utama yang bukan admin. Kirim lewat file, jangan pernah lewat chat.
4. **Tool yang tidak bisa dijangkau sebaiknya jangan didaftarkan.** Handler `buka_browser` (Lightpanda) masih ada di `runTool`, tapi sengaja **tidak** masuk daftar deklarasi — container tidak bisa menghubungi service yang bind ke IP Tailscale. Kalau didaftarkan, model akan memanggil tool yang dijamin gagal dan mengarang alasan.

## Selamat tinggal copy-paste channel ID

`discord_baca` menerima **nama** channel, bukan ID: ada cache resolver nama → ID sekali jalan, jadi ngomong *"baca channel chokdi-notif"* saja cukup. Untuk Telegram, `telegram_list_grup` membaca daftar grup hasil sinkron dari server Chokdi, sebab Bot API tidak punya endpoint "list semua grup" — keterbatasan platform yang dijembatani file, bukan dipaksa.

## Kesimpulan

Delapan tool, 91 channel Discord, 18 grup Telegram, dan satu baris `String()` yang bikin semuanya tampak bodoh di telinga. Pelajaran yang paling mahal hari ini bukan soal API-nya, tapi soal verifikasi: **"toolResponse terkirim" bukan bukti tool-nya bekerja**. Kalau sebuah hasil tidak pernah dibaca manusia, bug-nya bisa hidup berhari-hari di balik log yang hijau.

Kalau kamu bangun voice agent sendiri, luangkan 1 menit buat tes satu tool end-to-end dan baca apa yang benar-benar keluar — bukan cuma cek log tidak error.

Artikel terkait: [Bikin JARVIS Sendiri: Realtime Voice AI](/posts/bikin-jarvis-realtime-voice-ai/) dan [Discord vs Telegram: Kategori, Channel, Thread](/posts/discord-vs-telegram-kategori-channel-thread/).

Kamu paling sering pakai voice assistant buat baca chat, kirim pesan, atau riset web? Tulis di komentar — aku lagi mau tambah tool ke-9.

— Chokdi 🐷 · Content Studio · 2026
