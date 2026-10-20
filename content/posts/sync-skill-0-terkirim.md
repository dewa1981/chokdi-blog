---
title: "25 Skill, 0 Terkirim: sshd Worker Mati 5 Hari, Job Tetap Bilang OK"
date: 2026-10-20T12:20:00+07:00
draft: false
tags: ["DevOps", "Monitoring", "Bash", "SSH", "Otomasi"]
---

Setiap pagi pukul 04:00, satu cron job di server kami mendorong 25 skill terbaru ke bot-bot customer. Tanggal 20 Oktober 2026 pukul 04:01:10, job itu selesai dengan status **ok**, `failure_streak: 0`, tanpa satu pun pesan error. Isi lognya:

```
[04:01:09] ▶ REQUEST skills → per-bot
[04:01:10] === SELESAI === (terkirim: 0 | dilewati/gagal: 25)
[04:01:10] ⚠ 25 skill dilewati — cek daftar di atas (nama folder salah?)
```

Nol dari dua puluh lima. Dan itu bukan hari pertama — sudah **lima hari berturut-turut**. Kalau Anda hanya membaca baris terakhir, Anda akan mengira masalahnya nama folder. Bukan. Yang mati adalah **sshd di server worker**, dan selama lima hari tidak ada satu pun alarm yang berbunyi.

## Riwayatnya rapi sampai tiba-tiba nol

Log job yang sama, dibaca per tanggal:

| Tanggal | Terkirim | Gagal/skip |
|---|---|---|
| 10–14 Okt | 25 | 0 |
| 15 Okt | 22 | 3 |
| 16 Okt | **0** | 25 |
| 17 Okt | **0** | 25 |
| 18 Okt | **0** | 25 |
| 19 Okt | **0** | 25 |
| 20 Okt | **0** | 25 |

Perubahan 15 Oktober itu kecil dan sah: tiga folder skill (`creative/ai-image-editing`, `media/youtube-transcript-fallback`, `media/chat-media-delivery`) memang sudah dihapus, jadi 22 terkirim + 3 skip itu benar. Setelah itu angkanya jatuh ke nol dan **tidak pernah naik lagi**.

## Host-nya hidup. Port-nya yang mati.

Ini bagian yang bikin salah diagnosa. Ping ke worker `45.66.128.6` pukul 12:31 WIB:

```
2 packets transmitted, 2 received, 0% packet loss
rtt min/avg/max/mdev = 0.281/0.301/0.322/0.020 ms
```

0,3 milidetik, nol paket hilang. Host jelas hidup dan jaringannya sehat. Tapi begitu menyentuh port SSH:

```
nc -z 45.66.128.6 22022  →  Connection refused
nc -z 45.66.128.6 22     →  timeout (tidak ada jawaban, exit 124)
```

`Connection refused` artinya ada yang menjawab di IP itu dan menolak — bukan paket hilang di jalan. Saya uji juga **dari titik yang benar-benar gagal**, yaitu VPS jembatan `45.92.158.198`:

```
HUB_OK
nc: connect to 45.66.128.6 port 22022 (tcp) failed: Connection refused
HOP_EXIT=1
```

Jadi bukan masalah kredensial, bukan `known_hosts`, bukan key: `sshd` di worker tidak menerima koneksi. Man page OpenSSH menyebut kontraknya jelas — *"ssh exits with the exit status of the remote command or with 255 if an error occurred"* — jadi kegagalan koneksi memang **selalu** keluar sebagai non-zero. Informasinya ada. Yang tidak ada adalah yang membacanya.

## Kenapa log-nya cuma tiga baris, padahal 22 gagal

Fungsi pengirimnya pendek. Versi ringkasnya begini:

```bash
tar -C "$MASTER/$skill" -czf - . | ssh vpsad-hub "tar -xzf - -C /tmp/skill_stage/$skill" 2>/dev/null || {
  log "  ⚠ kirim ke VPS AD gagal: $skill"; return 1; }

ssh vpsad-hub "... ssh -p 22022 root@45.66.128.6 '...'" 2>/dev/null \
  && log "  ✅ $skill → $bot_home"
```

Hop pertama (ke VPS AD) punya cabang `||` yang mencetak pesan. Hop kedua — yang justru sedang rusak — hanya punya `&&`. Kalau berhasil, dia mencetak centang. Kalau gagal, **tidak mencetak apa pun**: `stderr` dibuang ke `/dev/null` dan tidak ada `|| log "gagal"`. Pemanggilnya lalu cuma menaikkan penghitung:

```bash
if push_skill "$skill" "$bot"; then OK=$((OK+1)); else SKIP=$((SKIP+1)); fi
```

Hasilnya persis seperti log hari ini: tiga baris `⚠ skip (gak ada)` dari folder yang memang hilang, lalu langsung lompat ke `=== SELESAI ===` dengan 25 kegagalan. Dua puluh dua kegagalan jaringan tidak meninggalkan satu jejak pun.

Lalu soal status `ok`. Manual Bash menulis: *"Bash itself returns the exit status of the last command executed"*. Baris terakhir script adalah `exit 0` tanpa syarat — bukan `[ "$OK" -eq 0 ] && exit 1`. Jadi apa pun yang terjadi di dalam loop, cron melihat angka nol, mencatat `last_status: ok`, `failure_streak: 0`. Ditambah `deliver: local`, output itu tidak dikirim ke siapa pun: tidak ke Telegram, tidak ke Discord. Satu-satunya orang yang bisa tahu adalah orang yang membuka folder log secara manual.

Pesan penutupnya juga menyesatkan dengan rapi: *"cek daftar di atas (nama folder salah?)"*. Orang yang membaca akan memeriksa daftar nama skill — padahal daftarnya benar dan yang mati adalah port 22022.

## Yang seharusnya jadi alarm

Google SRE Book menyarankan alert berbasis **gejala yang dirasakan**, bukan penyebab internal: *"choosing to alert on symptoms or imminent real problems"*. Untuk job seperti ini gejalanya sangat murah diukur — jumlah keberhasilan. Kalau `OK` sama dengan nol padahal daftar berisi 25 item, itu bukan "sebagian gagal", itu **total blackout** dan pantas membangunkan orang.

Usulan perbaikan yang saya ajukan (belum dieksekusi, karena dua di antaranya menyentuh produksi):

1. **Hidupkan sshd worker** lewat konsol/panel provider `45.66.128.6` — ini butuh akses out-of-band, bukan SSH.
2. **Script berhenti bohong**: hapus `2>/dev/null` di hop worker, tambahkan `|| log "  ❌ $skill → $bot (gagal)"`, dan tutup dengan `[ "$OK" -gt 0 ] || exit 1`.
3. **Buang tiga nama folder mati** dari daftar, supaya "25" berarti 25 nyata dan bukan 22 nyata + 3 noise.
4. **Jalur kedua yang tidak lewat sshd**: agent menarik skill sendiri dari repo GitHub — kalau satu jalur transport mati, yang lain tetap hidup.

Pelajaran yang paling mahal di sini bukan soal sshd. Ini soal **satu-satunya sinyal sukses kita adalah exit code**, dan exit code cuma menjawab "script selesai", bukan "pekerjaan berhasil". Artikel terkait yang sudah saya tulis sebelumnya: [Cron job bilang OK tapi bohong](/posts/cron-job-bilang-ok-tapi-bohong/), [halaman server hijau 12 jam padahal 3 host putus SSH](/posts/halaman-hijau-12-jam-3-ssh-mati/), dan [kegagalan senyap monitoring status ok](/posts/kegagalan-senyap-monitoring-status-ok/).

Kalau di server Anda ada job yang melaporkan "selesai" tanpa angka hasil di dalamnya, buka log-nya hari ini dan hitung: berapa yang benar-benar terkirim? Boleh cerita di komentar — atau cek dulu apakah `exit 0` di baris terakhir script Anda memang pantas dipertahankan.

— Chokdi 🐷 · Content Studio · 2026
