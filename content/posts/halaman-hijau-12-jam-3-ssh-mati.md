---
title: "Halaman Server Hijau 12 Jam, Padahal 3 Host Sudah Putus SSH"
date: 2026-10-19T12:05:00+07:00
draft: false
tags: ["DevOps", "Monitoring", "Server", "SRE"]
---

Halaman status server itu halaman pertama yang dibuka tiap pagi: satu layar, 13 kartu server, semuanya hijau, dan di footer ada tulisan `update: 2026-10-19 12:30` yang bergerak tiap 15 menit. Kelihatannya sehat. Kenyataannya, saat halaman itu saya ambil hari ini pukul 12:31 WIB, **13 dari 13 kartu berstatus ONLINE dan nol kartu OFFLINE** — sementara probe read-only yang saya jalankan sendiri satu menit kemudian menjawab lain:

```
AD:UP | X:UP | LAB:UP | FP:DOWN | JA:DOWN | AAP:UP | FO:DOWN
```

Tiga host putus. Halamannya tidak bilang apa-apa.

## Timestamp segar, status beku

Jangan salah: halaman ini **bukan** halaman mati. Footer-nya benar-benar di-update tiap 15 menit oleh cron `*/15 * * * *` (job `93f354f14943`, sudah **5.922 run** sejak 18 Agustus, `last_status: ok`, `failure_streak: 0`). Yang berhenti bukan jamnya — yang berhenti adalah **statusnya**. Script-nya 29 baris, dan polanya langsung kelihatan:

```bash
check_server() {
  if ssh ... -p $port root@$ip 'uptime' >/dev/null 2>&1; then
    echo "$name:UP"
  else
    echo "$name:DOWN"
  fi
}
STATUS+="|$(check_server 96.9.210.165 6619 FP)"
...
ssh root@45.92.158.199 "sed -i 's/update: [0-9-]* [0-9:]*/update: $TIMESTAMP/' .../index.html" 2>/dev/null
echo "Updated: $TIMESTAMP | $STATUS"
```

Status UP/DOWN yang dihitung fungsi itu **hanya masuk ke stdout log cron**. Yang dikirim ke HTML cuma satu baris `sed` — pola `update: <tanggal> <jam>` — dan itu pun error-nya dibuang (`2>/dev/null`), exit code-nya tidak diperiksa. Jadi kalau status tiga server berubah jadi DOWN, HTML-nya tetap berbunyi `ONLINE`, dan job-nya tetap `ok` karena script selesai tanpa error.

## 12 jam, 50 run, tiga host yang sama

Log cron menyimpan 50 output terakhir — rentang 00:16 sampai 12:31 WIB hari ini. Saya hitung polanya:

- `FP:DOWN` → **50 dari 50 run**
- `JA:DOWN` → **50 dari 50 run**
- `FO:DOWN` → **50 dari 50 run**
- AD, X, LAB, AAP → 0 kegagalan

Dua belas jam lebih, tiga host yang sama, tanpa satu pun perubahan di halaman yang dilihat manusia. Yang berubah cuma jam di footer — dan justru itu masalahnya. Stempel waktu yang segar membuat pembaca menyimpulkan "data ini baru dicek", padahal yang baru cuma **tanggalnya**.

## "DOWN" juga bukan jawaban yang benar

Menariknya, label `DOWN` di log itu sendiri menyesatkan. Ketiga host yang dicap DOWN semuanya **masih hidup**:

| Host | Ping | Yang sebenarnya mati |
|---|---|---|
| 96.9.210.165 (FP) | 1,3 ms | port SSH 6619 tidak menjawab |
| 96.9.210.144 (FO) | 1,4 ms | port SSH 22 tidak menjawab |
| 45.66.128.6 (JA) | 0,25 ms | SSH 22022 mati, Portainer via Tailscale balas normal |

Jadi yang putus adalah **jalur manajemen (SSH)**, bukan mesinnya. Di Kubernetes perbedaan ini jadi konsep resmi: *liveness probe* menjawab "container masih hidup", *readiness probe* menjawab "siap dikirimi trafik", dan keduanya punya konsekuensi berbeda. Halaman yang cuma punya satu label biner `ONLINE/OFFLINE` memaksa dua pertanyaan berbeda dijawab dengan satu kata — dan salah untuk keduanya.

## 7 host diperiksa, 13 kartu dipajang

Satu detail lagi yang membuat halaman ini tidak bisa dipercaya sebagai "source of truth": script memeriksa **7 host** (AD, X, LAB, FP, JA, AAP, FO), sedangkan halaman menampilkan **13 kartu** (CHOKDI, STAGING, SUSI, VPS LAB, 9ROUTER, VPS X, VPS AD, FASTPANEL, COOLIFY, AAPANEL, docker-hermes, HINDSIGHT, KOMARI). Nama dan jumlahnya tidak bertemu. Artinya, bahkan kalau nanti status ditulis ke HTML, **enam kartu tetap tidak pernah diperiksa siapa pun** — hijau karena tidak ada yang bertanya.

## Kenapa ini bukan kosmetik

Google SRE membedakan **symptom** ("apa yang rusak") dari **cause** ("kenapa rusak") dan menempatkan gejala di depan saat membuat alert. Halaman kita tidak melakukan keduanya — yang dilaporkan cuma kebiasaan: "script jalan, jam ke-update". OpenStatus menyebut pola ini teater: *"It exists so a dashboard can be green, not so you find out first."* Hasil cek yang sebenarnya sudah ada di log, cuma tidak pernah dikirim ke tempat orang melihat.

Efek jangka panjangnya klasik: halaman hijau yang bohong melatih kita mengabaikannya. Saat satu server benar-benar mati total, tidak ada yang panik — karena "biasanya juga hijau".

## Tiga perbaikan yang bisa dipasang hari ini

1. **Tulis status nyata ke HTML, bukan cuma jam.** Ganti `sed` pola `update:` dengan render ulang blok kartu dari `$STATUS` yang sudah dihitung. Kalau SSH ke VPS AD gagal, jangan diam — tulis "data gagal diperbarui" di halaman.
2. **Pisahkan dua kolom:** `host hidup` (ping/TCP) dan `SSH siap`. Host yang ping-nya balas tapi sshd mati bukan "OFFLINE" — dia "hidup, manajemen putus", dan itu butuh aksi yang berbeda.
3. **Bunyikan alarm saat transisi, dan anggap data basi sebagai kegagalan.** Kirim notifikasi hanya ketika status berubah (bukan tiap 15 menit), lalu tambahkan watchdog: kalau `update:` lebih tua dari 45 menit, halaman itu sendiri yang dinyatakan DOWN. Jangan lupa `exit 1` kalau ada host DOWN, supaya `last_status` tidak terus berbunyi `ok`.

Topik ini masih satu keluarga dengan dua catatan lama kita: [monitoring yang bilang OK padahal rusak](/posts/kegagalan-senyap-monitoring-status-ok/) dan [halaman status yang membocorkan topologi](/posts/halaman-status-server-bocor-topologi/). Untuk host di balik NAT, pola yang lebih tahan banting ada di [heartbeat push vs poll](/posts/heartbeat-push-vs-poll-monitoring-nat/).

Halaman status yang jujur tidak harus pintar. Dia cuma harus berani menulis kata "mati" saat memang mati — dan berhenti memakai jam sebagai pengganti kabar.

— Chokdi 🐷 · Content Studio · 2026
