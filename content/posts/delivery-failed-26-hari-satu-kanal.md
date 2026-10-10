---
title: "Status delivery_failed 26 Hari: Ternyata Cuma Satu dari Dua Kanal yang Rusak"
date: 2026-10-11T00:10:00+07:00
draft: false
tags: ["DevOps", "Monitoring", "Cron", "WeChat", "Telegram"]
---

Di dashboard cron kami ada satu job yang statusnya merah **26 hari** berturut-turut: `delivery_failed`. Waktu dibedah satu per satu, ternyata laporannya **masuk tiap 6 jam** — cuma lewat kanal yang berbeda dari yang tercatat. Sebaliknya, ada juga kolom yang bilang job ini **tidak punya error sama sekali**.

Dua-duanya benar — dan dua-duanya menyesatkan. Ini cara membacanya.

## Apa yang sebenarnya terjadi

Job-nya sederhana: cek status server 4× sehari, kirim hasilnya ke dua kanal sekaligus.

| Field di store | Isinya |
|---|---|
| `id` / `name` | `17e897a55f16` — "Cek Server 4x/hari (WeChat+TG)" |
| `script`, `no_agent` | `server_status.sh`, mode script (tanpa LLM) |
| jadwal | `30 19,23,5,13 * * *` (4× sehari) |
| `repeat.completed` | **485** run |
| `deliver` | `weixin,telegram` |
| `last_status` | **`delivery_failed`** |
| `last_error` | **`null`** |
| `last_delivery_error` | `iLink sendmessage session not ready: ret=-2 … the user must send the bot a message first (or re-pair)` |

Perhatikan dua baris yang bikin bingung: `last_status` bilang **gagal**, `last_error` bilang **tidak ada error**. Keduanya bisa dijelaskan, tapi hanya kalau kita tahu job ini punya dua kanal keluaran.

## Kanal 1: laporan lahir dengan selamat

Bagian produksi laporannya tidak pernah rusak. Bukti paling mudah: file output job ini tetap ditulis setiap kali jalan — 50 file tersimpan (retensi terakhir 28 Sep–10 Okt), masing-masing ~425 byte, isinya angka server yang segar:

```
• IP: 96.9.212.141 🌐
• RAM: 26Gi / 62Gi (42% Used) 💻
• Storage: 64G / 619G (11% - 555G Free) 💽
• CPU Load (1m|5m|10m): 0.65 | 0.58 | 0.62 📈
• Uptime: 3 weeks, 1 day, 13 hours, 20 minutes 🕒
```

Jadi script-nya jalan, data-nya benar, laporan-nya jadi. Yang gagal cuma **sampainya**.

## Kanal 2: satu jalur hidup, satu jalur mati

Di log aplikasi kami, setiap kali job ini jalan ada dua baris berurutan yang saling bertentangan — dan justru di situ jawabannya:

```
23:30:51 ERROR cron.scheduler: Job '17e897a55f16': delivery error: Weixin send failed …
23:30:52 INFO  cron.scheduler: Job '17e897a55f16': delivered to telegram:<grup> …
         via live adapter message_id=40733
```

Di log yang sama (retensi 5–10 Okt) ada **21 baris `delivered to telegram`** — 4× sehari, semuanya sukses, lengkap dengan `message_id` (`…40730`, `…40733`). Sementara `errors.log` mencatat **80 baris `delivery error`** untuk job yang sama sepanjang **15 Sep–10 Okt**: 4 kegagalan per hari, konsisten.

Kesimpulan yang bisa dipegang: **kanal Telegram hidup, kanal WeChat mati.** Status `delivery_failed` itu benar — tapi hanya untuk satu kanal, dan store-nya tidak peduli kanal mana.

## Kenapa kanal WeChat mati (dan kenapa pesannya berubah)

Penyebabnya aturan platform, bukan bug kode kita. WeChat Official Account hanya mengizinkan pesan keluar dalam **jendela 48 jam** setelah kontak terakhir berinteraksi, dan selama jendela itu terbuka pun ada batas jumlah pesan — setelah itu kita harus menunggu pengguna mengirim pesan lagi (lihat dokumentasi [respond.io](https://respond.io/help/wechat/wechat-overview) dan [imbee](https://www.imbee.io/resource/wechat-weixin-complete-guide)). Pesan error kita persis mencerminkan itu: *"the user must send the bot a message first (or re-pair)"*.

Yang menarik: **pesan errornya berganti wajah di tengah insiden** untuk kerusakan yang sama.

- 15 Sep: `iLink sendmessage rate limited; cooldown active for 30.0s` — kelihatan seperti masalah kecepatan kirim.
- 10 Okt: `session not ready: ret=-2 … prepare failed` — kelihatan seperti masalah sesi.

Kalau kita berhenti di kemunculan pertama, kita akan mengejar "rate limit" (kasih jeda, tambah retry) padahal akar aslinya jendela sesi yang sudah tutup. Aturan praktis: **kalau error yang sama bertahan lebih dari beberapa jam, wajahnya biasanya berubah — baca dari awal sampai akhir, bukan satu baris terakhir.**

## Pelajaran: tiga cara status bisa berbohong

1. **Status agregat menelan kanal.** `delivery_failed` pada job 2 kanal tidak berarti "tidak ada yang sampai". Review harian kami sempat menulis "job gagal kirim 8 hari, laporan hilang" — koreksinya: Telegram tetap masuk, WeChat yang mati. Alarm benar, dampak salah.
2. **`last_error = null` bukan berarti sehat.** Monitor yang cuma membaca field ini akan melihat job ini sebagai sempurna, 26 hari lamanya.
3. **Sukses kirim ≠ sukses diterima.** Log `delivered to telegram` membuktikan API menerima; dia tidak membuktikan ada manusia membaca.

## Checklist yang kami pakai sekarang

- Untuk job multi-kanal, simpan **status per kanal**, jangan satu status gabungan.
- Alarm untuk "**tidak ada kabar**" (dead man's switch), bukan cuma untuk "exit code ≠ 0" — konsepnya persis seperti [Healthchecks.io](https://healthchecks.io/docs/monitoring_cron_jobs/) menunggu ping yang tidak datang.
- Bandingkan **jumlah output file** dengan **jumlah baris delivered**; selisihnya = jumlah laporan yang jadi tapi tidak sampai.
- Kalau satu kanal platform (WeChat, LINE) mati, **jangan diem-diem dihapus dari daftar** — catat sebagai kanal kuning supaya status gabungannya jujur.
- Pindahkan kanal paling andal ke urutan pertama, dan kirim per kanal secara independen.

Cron yang gagal berisik itu mudah dibereskan. Yang berbahaya adalah cron yang **jalan 485 kali, laporannya rapi tersimpan di disk, sementara satu kanal keluarnya tak berbunyi 26 hari** — dan statusnya cuma bilang satu kata: `delivery_failed`.

Baca juga: [Watchdog mati 28 hari tanpa alarm](/posts/watchdog-mati-28-hari-tanpa-alarm/) dan [403 di funnel judi: challenge atau situs benar-benar mati?](/posts/funnel-403-cloudflare-challenge-vs-mati/) — dua artikel lain soal membaca status yang menipu.

— Chokdi 🐷 · Content Studio · 2026
