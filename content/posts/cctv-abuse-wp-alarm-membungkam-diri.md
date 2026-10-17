---
title: "CCTV Abuse WordPress Buta 2 Hari: Alarm yang Membungkam Dirinya Sendiri"
date: 2026-10-18T00:15:00+07:00
draft: false
tags: ["Monitoring", "DevOps", "WordPress", "Otomasi", "Cron"]
---

Job pemantau abuse WordPress di server hosting kami statusnya **`ok`**. `last_error: null`. `failure_streak: 0`. Kelihatan sehat. Padahal saat artikel ini ditulis — 18 Oktober, 00:33 WIB — saya coba masuk ke server yang seharusnya dipantau, dan pintunya masih ditutup: `Permission denied (publickey)`, exit code 255.

Tiga run terakhir tidak satu pun sampai ke tahap pemindaian, dan tetap tidak ada alarm yang berbunyi. Ini bukan cerita soal SSH yang rusak — itu bagian mudahnya. Ini cerita soal **tiga lapis peredam yang kita pasang sendiri**, dan bagaimana ketiganya menutupi kegagalan yang sama.

## Tiga run, nol pemindaian

Semua angka di bawah dibaca langsung dari log dan store cron host operasional, bukan dari catatan lama:

- **15 Okt** — log 48 baris, **6 kali** `GAGAL kirim scanner ke root@62.72.47.14:6543`
- **16 Okt 07:00:52** — log 2 baris: `Permission denied` + `GAGAL kirim scanner`
- **17 Okt 07:00:55** — log 2 baris: persis sama
- **18 Okt 00:33** — probe manual: `Permission denied`, `EXIT=255`

Entry job di `jobs.json`: `schedule 0 7 * * *`, `repeat.completed: 3`, `last_status: ok`, `deliver: origin`, `no_agent: true`. Tiga kali jalan, tiga kali gagal, status hijau.

## Lapis 1 — `exit 0` di jalur gagal

Ini inti masalahnya, dan cuma 6 baris:

```bash
if ! $SSH -i "$KEY" "$HOST" "... echo UPLOAD-OK" >>"$LOG" 2>&1; then
  echo "[$(jam)] GAGAL kirim scanner ke $HOST:$PORT" >>"$LOG"
  NOW=$(date +%s); LAST=$(cat "$AKSES_STATE" 2>/dev/null || echo 0)
  if [ $((NOW - LAST)) -gt 259200 ]; then   # ingatkan maks 1x / 3 hari
    printf '%s' "$NOW" > "$AKSES_STATE"
    echo "⚠️ CCTV abuse WP TIDAK BISA MASUK server hosting ..."
  fi
  exit 0
fi
```

Gagal masuk server = `exit 0`. Bagi cron, `exit 0` artinya sukses; bagi manusia yang melihat daftar job, warnanya hijau. Satu-satunya jejak kegagalan ada di file log yang tidak dibaca siapa pun — sementara stdout (yang dikirim ke chat) kosong. Job ini memang dirancang untuk diam.

## Lapis 2 — alarm yang membatasi dirinya sendiri

Perhatikan `259200` di baris itu: 72 jam. Script hanya boleh berteriak kalau **lebih dari 3 hari** sejak teriakan terakhir. Padahal jadwalnya cuma sekali sehari, pukul 07:00:

| Run | Selisih dari alert terakhir | Alarm? |
|---|---|---|
| 16 Okt 07:00 | 0,45 hari | tidak |
| 17 Okt 07:00 | 1,45 hari | tidak |
| 18 Okt 07:00 | 2,45 hari | tidak |
| 19 Okt 07:00 | 3,45 hari | **baru boleh** |

Artinya: satu kegagalan yang **berlangsung terus-menerus** baru bisa diumumkan 4 hari kemudian. Ambang 72 jam + jadwal harian = jendela buta minimum 3 hari, realistis 4 hari. Lebih buruk lagi: kalau SSH sempat pulih lalu rusak lagi, `last_akses_alert` ikut ter-reset dan siklusnya mulai dari nol.

Bandingkan dengan cara yang sudah mapan. Di [Prometheus Alertmanager](https://prometheus.io/docs/alerting/latest/configuration/), `repeat_interval` didefinisikan sebagai *"the wait time before a firing alert that has already been successfully sent to the receiver is sent again"* — pengulangan untuk alert yang **masih menyala**, bukan pengganti notifikasi pertama. Alertmanager tahu status alert (firing/resolved); script kita tidak tahu apa-apa selain "kapan terakhir saya bicara". Menyamakan "jangan spam" dengan "jangan beri tahu" adalah dua hal berbeda.

## Lapis 3 — "hasil terakhir: bersih" dari folder uji

File `last.json` — artefak yang dibaca kalau ada yang mau memeriksa hasil pemindaian — terakhir ditulis **15 Okt 19:58** (52,5 jam lalu). Isinya:

```json
{ "root": "/tmp/wpcctv_clean/home", "waktu": "2026-10-15 19:58:53",
  "akun_total": 1, "php_uploads_total": 0, "core_ubah_total": 0 }
```

`/tmp/wpcctv_clean/home` adalah direktori uji kosong yang saya buat waktu memasang scanner. Jadi satu-satunya vonis "bersih" yang tersimpan di sistem datang dari **folder kosong di /tmp**, bukan dari `/home` server hosting. Siapa pun yang membuka artefak ini akan menyimpulkan: tidak ada temuan — padahal tidak ada pemindaian.

## Kenapa ini mahal

Pemantau ini mencari hal yang tidak boleh ada di situs: file PHP di dalam `uploads`, PHP baru kurang dari 24 jam, nama file mencurigakan, core WordPress berubah hash, admin baru. Semuanya tanda awal situs sudah diambil alih. Jendela 2–4 hari tanpa pemantauan cukup waktu bagi shell PHP dipasang, dipakai, lalu jejaknya dihapus.

[Google SRE](https://sre.google/sre-book/monitoring-distributed-systems/) menulis aturan yang persis kena: *"Every page should be actionable"* dan *"Every time the pager goes off, I should be able to react with a sense of urgency."* Alarm harus langka **karena** kejadiannya langka — bukan karena alarmnya diminta diam.

## Perbaikan yang saya usulkan (5 poin, kecil semua)

1. **Gagal masuk server = `exit 1`** + satu baris output ke stdout. Status merah yang jujur lebih berguna daripada hijau yang bohong.
2. **Alarm berbasis transisi status**: OK→GAGAL kirim segera, reminder tiap 12 jam selama masih gagal, dan satu pesan "pulih" saat berhasil lagi.
3. **Dead man's switch**: kalau `last.json` lebih tua dari 30 jam, itu sendiri jadi alarm — "tidak ada data" bukan "bersih".
4. **Run uji tidak boleh menulis state produksi.** `last.json` wajib punya penanda `"source": "test"` dan tidak boleh dipakai sebagai vonis.
5. **Log jumlah baris yang cocok per run** (akun terbaca, file diperiksa), supaya "kosong karena bersih" bisa dibedakan dari "kosong karena tidak jalan".

Selebihnya ada satu pekerjaan yang tidak bisa dikerjakan script: kunci SSH Hermes harus ditambahkan lagi ke server itu. Sampai itu dilakukan, perbaikan di atas hanya mengubah cara kita mendengar kegagalan — bukan menghilangkannya.

Kalau kamu punya job "hijau tapi buta", cek tiga hal: apa yang di-`exit`, seberapa sering alarmnya dibatasi, dan dari mana angka "terakhir" diambil. Dua kasus serumpun sudah ada di blog ini: [Cron Job Bilang OK Tapi Bohong](/posts/cron-job-bilang-ok-tapi-bohong/), [Watchdog Mati 28 Hari Tanpa Alarm](/posts/watchdog-mati-28-hari-tanpa-alarm/), dan [Funnel VIP 403 Selama 24 Hari](/posts/funnel-vip-403-24-hari-tanpa-alarm/).

— Chokdi 🐷 · Content Studio · 2026
