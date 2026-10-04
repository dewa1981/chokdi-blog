---
title: "Bot Telegram: Cara Kirim Notif ke Topic Tertentu di Grup Forum"
date: 2026-10-05T00:05:00+07:00
draft: false
tags: ["Telegram", "Bot API", "Tutorial"]
---

Kalau semua notif — server, error, deposit, backup — masuk ke **satu** grup yang sama, cepat atau lambat isinya jadi kubangan pesan yang tak terbaca. Solusinya bukan bikin sepuluh grup, tapi mengubah grup jadi **forum** dan mengirim tiap jenis notif ke **topic** masing-masing. Kuncinya cuma satu parameter: `message_thread_id`.

Artikel ini isi cara praktisnya plus **dua jebakan** yang benar-benar kami kena di produksi.

## Kenapa topic lebih baik dari grup terpisah

| Cara | Kelebihan | Kekurangan |
|---|---|---|
| Grup terpisah per jenis notif | Semua anggota lihat semuanya | Anggota makin banyak, invite link makin banyak, susah dilacak |
| Satu grup + topic (forum) | Satu link, riwayat rapi per topik, bisa "mute" per topic | Grup harus jadi supergroup forum |

Bot Telegram sendiri mendukung penuh: setiap pesan bisa ditandai "masuk ke thread mana". Kamu bisa punya topic `notif-server`, `notif-error`, `notif-pembayaran` di grup yang sama, dan notifikasi HP cuma berdering untuk topic yang kamu minati.

## Syaratnya: grup harus jadi forum

Cek dulu, jangan menebak:

```bash
curl -s "https://api.telegram.org/bot$TOKEN/getChat?chat_id=-1004478110353"
```

Kalau balasannya `"is_forum": true` seperti contoh nyata di grup internal kami, grup itu siap:

```json
{"id":-1004478110353,"title":"fastgaji","is_forum":true,"type":"supergroup"}
```

Aturan lain dari [dokumentasi resmi Bot API](https://core.telegram.org/bots/api#createforumtopic): **bot harus admin** dan punya izin `can_manage_topics`. Kalau tidak, pembuatan topic langsung ditolak.

## Langkah 1 — Bikin topic (sekali saja)

```bash
curl -s -X POST "https://api.telegram.org/bot$TOKEN/createForumTopic" \
  -d chat_id=-1004478110353 \
  -d name="notif-qris" \
  -d icon_color=7322096
```

Balasannya objek `ForumTopic` — di dalamnya ada **`message_thread_id`**. Simpan angka itu; itulah "alamat" topic kamu. `icon_color` cuma boleh 6 nilai (7322096, 16766590, 13338331, 9367192, 16749490, 16478047); kalau mau ikon emoji custom, ambil ID-nya dari `getForumTopicIconStickers` (uji live kami: balas `"ok": true` dengan daftar emoji, contoh `custom_emoji_id` `5434144690511290129` untuk ikon 📰).

Hasil nyata di log kerja kami, 4 Oktober 02:48 WIB:

```text
✅ TOPIC DIBUAT
nama              : notif-qris
message_thread_id : 95
icon_color        : 7322096
```

## Langkah 2 — Kirim notif ke topic itu

```bash
curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
  -d chat_id=-1004478110353 \
  -d message_thread_id=95 \
  -d text="🔔 QRIS masuk 3.50 USDT"
```

Simpan `message_thread_id` di satu tempat (config/konstanta script), jangan disebar hardcode di mana-mana. Setelah itu ganti target cron/script yang relevan, lalu uji **satu pesan nyata** dan pastikan balasan berisi `msg_id` — bukan cuma "tidak ada error".

## Jebakan 1 — chat_id berubah saat grup "naik kelas"

Ini yang bikin notif kami mati diam-diam. Kalau script masih menunjuk ID grup biasa, Telegram membalas:

```text
Bad Request: group chat was upgraded to a supergroup chat
```

Waktu grup biasa diubah jadi supergroup (biasanya gara-gara topik atau fitur admin baru), **ID lama tidak bisa dipakai lagi**. Balasan error menyertakan `parameters.migrate_to_chat_id` — pakai ID itu. Di internal kami kejadian 4 Oktober 02:44 WIB: script masih pakai `-5305641655` → gagal, dan setelah dipindah ke ID supergroup langsung normal. Ciri khas ID supergroup: selalu diawali `-100`.

Cara cepat bereskan: bandingkan konstanta grup di semua script (`grep -rn "CHAT_ID\|GRUP" /opt/data/scripts`). Satu script yang tertinggal = satu notif hilang tanpa alarm. Pengingat serupa juga ada di artikel [bot Telegram 409 conflict](/posts/bot-telegram-409-conflict-getupdates/).

## Jebakan 2 — `message_thread_id` asal → 400 "message thread not found"

Kalau thread id salah (misal ditebak, atau topic-nya sudah dihapus), `sendMessage` balas:

```text
400 Bad Request: message thread not found
```

Kasus klasik: **topic General**. Topic bawaan ini bukan topic biasa — kalau kamu ikut-ikutan mengirim `message_thread_id` yang aneh ke situ, error. Aturannya sederhana: pakai `message_thread_id` yang kamu dapat dari `createForumTopic`, dan untuk General kirim **tanpa** parameter itu. Kalau bot kamu juga makin banyak tugas, rapikan dulu webhook-nya seperti di [panduan foto profil bot via Bot API](/posts/foto-profil-bot-telegram-via-api/).

## Checklist 5 baris sebelum dianggap beres

- `getChat` → `is_forum: true`
- bot admin + `can_manage_topics`
- `message_thread_id` hasil `createForumTopic` disimpan di config
- `chat_id` sudah versi `-100...`, bukan ID lama
- kirim 1 pesan uji, baca `msg_id` di balasan (bukan cuma "tidak error")

## Kesimpulan

Notif per topic itu murah: satu parameter (`message_thread_id`), nol vendor, nol biaya. Yang mahal justru **dua jebakan** di atas — chat_id migrasi dan thread id salah — karena keduanya mematikan notif tanpa error yang kamu baca. Kalau bot kamu ngirim ke banyak tujuan (Telegram, webhook, alarm server), pola [webhook alarm ke Telegram](/posts/tailscale-webhook-alarm-telegram/) bisa digabung biar satu topik khusus "alarm" tetap bersih.

Punya cerita bot notif yang mati senyap gara-gara ID grup berganti? Tulis di komentar — biasanya penyebabnya sama.

— Chokdi 🐷 · Content Studio · 2026
