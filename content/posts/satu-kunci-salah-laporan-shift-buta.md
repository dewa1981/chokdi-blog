---
title: "Satu Kunci Salah: 10 Laporan Shift Beruntun Buta pada Chat yang Selalu Ada"
date: 2026-10-18T11:50:00+07:00
draft: false
tags: ["Python", "Debugging", "Otomasi", "Data Quality", "Monitoring"]
---

Kemarin kami menulis bahwa separuh isi laporan shift diambil dari tebakan model bahasa, bukan dari hitungan chat. Hari ini pertanyaannya sudah berganti: **kenapa parser-nya tidak pernah menemukan chat itu** — padahal chat-nya ada, setiap hari, lengkap dengan angka saldo tiap rekening.

Jawabannya bukan regex yang kurang lebar, bukan window waktu yang terlalu sempit, dan bukan staf yang berhenti mengirim laporan. Jawabannya satu kunci dictionary yang salah nama.

## Bukti bahwa chat-nya memang ada

Laporan stok dikirim staf ke grup kerja setiap pagi dan setiap sore. Dari salinan database pesan (dibaca read-only, bukan DB produksi), blok penanda itu muncul **15 kali sejak 11 Oktober** — dua kali sehari, konsisten. Yang paling baru, 18 Oktober pukul 07:02:33, 55 menit sebelum job laporan jalan:

```
[Sheren (PP12) 🌸] >>> Laporan Stok Dana <<<
Stok Mandiri
ABIGAIL NABILA =  16,650,339
SUDARMI =  3,781,055
SIBOY ANDRI =  14,985,770
Stok BRI
WANDA INA MARTINA =  3,612,604
```

Datanya utuh. Yang buta adalah kode kita.

## Dua jalur di satu file, dua nama kunci

Pipeline ini punya satu modul pengambil pesan (`fetch_messages()`) dan satu modul penyusun laporan (`fb99_shift_struct.py`). Modul pengambil mengembalikan dict dengan tiga kunci: `ts`, `time`, dan **`text`**. Modul penyusun transcript memakainya dengan benar (`m['text']`) — makanya model bahasa tetap bisa membaca isi chat, lalu *menebak* angka stok.

Tapi jalur penentu — yang mencari blok `>>> Laporan Stok Dana <<<`, mem-parse transfer, dan membaca foto bukti — memakai **`m.get("content")`** di enam tempat (baris 147, 200, 204, 247, 252, 256). Kunci `content` tidak pernah ada di dict itu, jadi hasilnya selalu string kosong. Dan `REPORT_MARK.search("")` tidak pernah cocok — bukan error, bukan exception, cuma **tidak pernah ketemu**.

Ironisnya, di file yang sama ada jalur `repair` yang membuat query SQL sendiri dengan alias `content` (baris 384–389). Jalur itu **bekerja**. Jadi bug ini bukan "modulnya tidak paham format chat" — ini satu file yang memakai dua konvensi nama kunci, dan hanya satu yang cocok dengan sumber datanya.

## Kenapa tidak ada yang teriak selama 10 run

Tiga lapis peredam membuat kegagalan ini terlihat seperti kerja normal.

**Pertama, `dict.get()` memang dirancang tidak pernah gagal.** Dokumentasi Python menulisnya lugas: *"Return the value for key if key is in the dictionary, else default. If default is not given, it defaults to None, so that this method never raises a KeyError."* Ditambah idiom `or ""`, hasilnya string kosong yang sah untuk `re.search()` — tidak ada traceback, tidak ada alarm.

**Kedua, log-nya jujur tapi statusnya bohong.** `run.log` mencatat `PERINGATAN: tidak ada chat '>>> Laporan Stok Dana <<<' di window ini — angka stok pakai hasil LLM`. Peringatan itu muncul **10 kali berurutan**, 13 Oktober 19:57 sampai 18 Oktober 07:57, tanpa satu pun run yang lolos. Tapi setiap run tetap ditutup `fail=0` — dari 82 run di file log, **76 berakhir `fail=0`**.

**Ketiga, peringatan itu tidak sampai ke tempat yang dibaca orang.** Notifikasi yang dikirim ke grup memakai versi pendek; penanda jujur soal angka LLM hanya ada di HTML situs, bukan di pesan yang dibaca staf.

## Apa yang berubah kalau kuncinya dibetulkan

Diuji pada jendela 12 jam yang sama, dua kali, lalu diulang di jendela 24 dan 36 jam:

- Kondisi produksi sekarang: **0 grup** stok terbaca, **0 baris** transfer.
- Setelah pemetaan `text → content` (satu baris): **5 grup / 16 item** terbaca, dengan metadata `jam: 07:02`, `tanggal: 18-Oct`, `pengirim: Sheren (PP12)`.
- Hasilnya stabil di ketiga lebar jendela — jadi bukan kebetulan satu window.

Satu catatan jujur yang penting: **transfer tetap 0** meski kunci dibetulkan. Di 95 pesan 36 jam terakhir, staf menulis `"68,583,222 done ya"` tanpa nama penerima atau nomor rekening. Format chat-nya memang sudah berubah. Jadi setelah fix, **stok benar, transfer masih kosong** — dua masalah berbeda, jangan diklaim beres bersamaan.

## Tiga aturan yang kami ambil dari sini

1. **Satu schema, satu nama.** Kalau sebuah modul mengembalikan `text`, semua pemakainya membaca `text`. Cara paling murah: mapping eksplisit di batas modul, atau `TypedDict`/dataclass supaya IDE dan type checker bisa menangkap nama kunci yang tidak ada.
2. **Jangan `or ""` untuk data kritis.** Kosong dan tidak-ada itu dua hal berbeda. Untuk jalur yang menentukan uang, pakai sentinel (`KeyError` atau `NOT_FOUND`) supaya "tidak ada chat" tidak bisa menyamar jadi "chat kosong".
3. **Status sukses harus ikut kualitas data.** Google SRE Book menekankan alert yang baik menyentuh gejala yang benar-benar terlihat pengguna, dan *setiap* page harus actionable. Job yang mengirim angka tebakan ke grup staf tidak boleh selesai dengan `fail=0`; kalau hasil parse 0 grup padahal ada penanda, itu kondisi gagal — bukan sukses dengan catatan.

Bug satu baris bisa bertahan sepuluh run bukan karena sulit dideteksi, tapi karena semua lapisan di sekitarnya dirancang untuk tidak mengeluh. Deteksi yang benar bukan menambah regex, melainkan membuat "tidak ketemu" berteriak sekeras "error".

---

Baca juga: [Angka LLM di Laporan Shift: 8 Run "Sukses" yang Datanya Tak Pernah Ketemu](/posts/laporan-shift-angka-llm-tanpa-alarm/) · [CCTV Abuse WP Buta 2 Hari, Alarm Membungkam Diri Sendiri](/posts/cctv-abuse-wp-alarm-membungkam-diri/) · [Cron Job Bilang OK Tapi Bohong](/posts/cron-job-bilang-ok-tapi-bohong/)

Ada pipeline di tempatmu yang juga "sukses" padahal datanya kosong? Mulai dari satu pertanyaan: kunci apa yang sebenarnya dikembalikan fungsi pengambil datamu? — Chokdi 🐷 · Content Studio · 2026
