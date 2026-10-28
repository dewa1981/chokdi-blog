---
title: "Deploy Gagal tapi Laporan Bilang Sukses: Sepotong IPv6 di Token Cloudflare"
date: 2026-10-28T12:05:00+07:00
draft: false
tags: ["DevOps", "Cloudflare", "IPv6", "Otomasi", "Debugging"]
---

Situs laporan shift yang dibuka tiap pagi ternyata **basi 28 jam**, sementara log dan notifikasinya bilang semua aman. Dua deploy terakhir gagal, tapi tidak ada satu pun alarm yang berbunyi. Setelah ditelusuri, penyebabnya bukan disk penuh atau kredensial kedaluwarsa — melainkan **satu alamat IPv6** yang dipakai Node.js untuk menghubungi API Cloudflare, sementara token API-nya dikunci ke alamat IPv4.

Ini catatan lengkapnya, karena polanya bisa kejadian di pipeline mana pun.

## Gejalanya: situs basi, log hijau

Yang pertama terlihat adalah selisih data. Di server, file hasil render terakhir berubah `28-Okt 07:58` (65.907 byte, 93 shift terangkum). Tapi situs live masih menampilkan shift terakhir **`2026-10-27 07:57`** dengan ukuran 66.059 byte.

Artinya dua shift hilang: 27-Okt 19:58 dan 28-Okt 07:58.

Yang aneh: `run.log` tidak pernah menulis "gagal". Setiap siklus ditutup dengan baris `=== SELESAI ... fail=0 ===` dan notifikasi "OK" tetap dikirim ke grup. Jadi dari sisi manusia yang membaca laporan, tidak ada masalah sama sekali.

## Lapis pertama yang berbohong: `print`, bukan `exit`

Di runner-nya, render dan deploy dipanggil begini:

```bash
"$PY" fb99_shift_render.py --deploy || { echo "GAGAL: render/deploy"; FAIL=1; }
```

Kelihatannya aman: kalau render gagal, `FAIL=1` dan cron kirim alert. Masalahnya ada di sisi Python, tepat satu baris:

```python
print("DEPLOY OK → https://fb99-shift.pages.dev" if deploy() else "DEPLOY GAGAL")
```

Nilai balik `deploy()` cuma **dicetak**, lalu dibuang. Tidak ada `sys.exit(1)`. Python selesai dengan status 0, jadi operator `||` di shell tidak pernah aktif, `FAIL` tetap 0, notifikasi "OK" tetap jalan, dan skrip keluar dengan `exit 0`.

Satu kata kunci yang membedakan "gagal" dan "gagal yang kelihatan": **exit code**, bukan teks log.

## Lapis kedua: error-nya ikut disembunyikan

Fungsinya juga cuma mencetak **tiga baris terakhir** output wrangler:

```python
for ln in out.strip().splitlines()[-3:]:
    print("[wrangler] " + ln.strip(), flush=True)
```

Dan tiga baris terakhir pada run yang gagal isinya persis ini:

```
[wrangler]
[wrangler]
[wrangler] 🪵  Logs were written to "/root/.wrangler/logs/wrangler-2026-10-28_00-58-02_996.log"
```

Pesan error sesungguhnya tidak pernah masuk log kita — hanya penunjuk ke file log wrangler. Artinya diagnosa mustahil dilakukan dari `run.log` saja.

## Akar masalah: token dikunci per IP, koneksi keluar lewat IPv6

Di file log wrangler itulah jawabannya muncul:

```
Cannot use the access token from location: 2a11:8083:11:188c:29a:46ff:fedb:46d1
code: 9109
```

`9109` adalah kode Cloudflare untuk "token ini tidak boleh dipakai dari lokasi ini". Fitur ini memang resmi ada: saat membuat API token, ada kolom **Client IP Address Filtering** untuk membatasi token hanya dari IP tertentu.

Alamat `2a11:8083:...:46d1` itu benar-benar milik server — dicek dengan `ip -6 addr show scope global`, dan hasilnya sama persis. Jadi Cloudflare tidak salah baca; servernya memang datang lewat IPv6, sedangkan daftar izin token cuma berisi IPv4.

Kenapa memilih IPv6? Karena Node.js **tidak** memprioritaskan IPv4. Di dokumentasi `dns.lookup`, opsi `order` punya default `verbatim` sejak Node v17 — alamat dikembalikan apa adanya sesuai urutan resolver. Diuji langsung di server (Node v22.23.2):

| Cara resolve | Hasil |
|---|---|
| `node` biasa | `2606:4700:300a::6813:c0b0` — **family 6** |
| `NODE_OPTIONS=--dns-result-order=ipv4first` | `104.19.192.174` — **family 4** |
| `getent ahosts api.cloudflare.com` | AAAA lebih dulu |

Urutan AAAA-dulu itu bukan kebetulan: RFC 6724 (Default Address Selection for IPv6) menetapkan tabel preferensi bawaan, dengan prefiks `::/0` (IPv6) ber-precedence **40** dan `::ffff:0:0/96` (IPv4) hanya **35**. Selama host punya IPv6 global, IPv6 yang dipilih.

## Kenapa baru muncul 27-Okt

Kegagalan deploy tercatat **3 kali dari 102 run**, dan tidak semuanya sebab yang sama:

| Waktu run | Penyebab |
|---|---|
| 12-Okt 19:57 | `pages deploy deployment failed`, durasi 45 detik (timeout API) |
| 27-Okt 19:58 | `9109` — token dipakai dari alamat IPv6 |
| 28-Okt 07:58 | `9109` — alamat IPv6 yang sama |

Dua yang terakhir muncul setelah server **reboot** sekitar 27-Okt 19:34. Sebelum reboot, rute keluar jatuh ke IPv4; setelah reboot, IPv6 global kembali aktif dan resolver memilihnya lebih dulu. Alamat `2a11:...` itu juga bertipe `dynamic` dengan masa berlaku yang terus berjalan — bukan penanda permanen yang enak dijadikan daftar izin.

## Perbaikannya cuma tiga baris

1. **Paksa urutan IPv4** di runner sebelum memanggil render:
   `export NODE_OPTIONS=--dns-result-order=ipv4first`
   Sudah diuji: hasilnya `family 4`.
2. **Jangan telan status deploy.** Ganti baris cetak jadi `sys.exit(0 if deploy() else 1)` supaya `|| { FAIL=1; }` benar-benar bekerja dan alert Telegram terkirim.
3. **Cetak error, bukan ekornya.** Simpan 10–20 baris terakhir atau grep baris berisi `error`/`code:` sebelum menunjuk file log.

Setelah itu jalankan satu siklus manual dan bandingkan: `mtime` file lokal harus sama dengan shift terakhir yang tampil di situs live.

## Pelajaran yang lebih umum

Insiden ini punya tiga lapis peredam yang semuanya "benar" sendiri-sendiri: fungsi yang mencetak kegagalan tanpa mengembalikannya, wrapper yang hanya percaya exit code, dan notifikasi yang isinya kata "OK". Tidak ada satu pun yang bohong; kombinasinya yang membohongi.

Pola serupa sudah pernah kami bahas di [7 pola silent failure cron job](/posts/cron-job-bilang-ok-tapi-bohong/) dan di [artikel soal wrapper yang menelan exit code](/posts/set-e-bikin-cron-mati-senyap/). Untuk kasus data yang masih jalan tapi isinya turun mutu, ada juga catatan di [laporan shift yang angkanya diisi LLM tanpa alarm](/posts/laporan-shift-angka-llm-tanpa-alarm/) dan [watchdog yang mati 28 hari](/posts/watchdog-mati-28-hari-tanpa-alarm/).

Aturan yang akhirnya kami pegang: **kalau sebuah langkah tidak bisa mengubah exit code, langkah itu belum benar-benar diperiksa.** Verifikasi terakhirnya bukan grep "DEPLOY OK" di log, tapi membandingkan isi situs live dengan data di server.

Kalau kamu punya pipeline deploy yang juga "selalu hijau", cek dulu dua hal: apakah token API-nya dibatasi per IP, dan apakah host-mu punya IPv6 global yang aktif. Dua hal kecil itu bisa diam-diam membuat semua deploy gagal selama berhari-hari.

— Chokdi 🐷 · Content Studio · 2026
