---
title: "Cara Ganti Foto Profil Bot Telegram dari Terminal (Bot API 9.4+)"
date: 2026-10-04T00:20:00+07:00
draft: false
tags: ["Telegram", "Bot", "API", "Tutorial"]
---

Sejak **Bot API 9.4 (9 Februari 2026)**, bot Telegram boleh mengganti foto profilnya **sendiri** lewat API. Sebelum itu satu-satunya cara adalah buka @BotFather satu per satu. Kalau kamu mengurus belasan bot (satu bot per agent, per klien, atau per brand), bedanya jelas: klik manual 15 menit versus satu perintah `curl`.

Masalahnya endpoint ini gampang salah payload, dan pesan errornya bikin salah diagnosa. Catatan di bawah ini hasil uji langsung ke API Telegram — termasuk membedakan error yang artinya "payload salah" dan "method tidak ada".

## Dua method baru: set dan remove

| Method | Parameter | Fungsi |
|---|---|---|
| `setMyProfilePhoto` | `photo` (InputProfilePhoto, **wajib**) | Ganti foto profil bot |
| `removeMyProfilePhoto` | tidak ada | Hapus foto profil bot |

Keduanya membalas `True` kalau berhasil. Yang perlu dicatat: **tidak ada `getMyProfilePhoto`** — kalau dipanggil, Telegram membalas **404 Not Found**. Jadi jangan heran kalau "method pembaca"-nya tidak ketemu; memang tidak dibuat.

## InputProfilePhoto: static atau animated

Parameter `photo` bukan file mentah, tapi **objek JSON**. Dua jenisnya:

- **InputProfilePhotoStatic** — `type: "static"`, berkas **.JPG**. PNG bukan format yang diterima untuk static photo.
- **InputProfilePhotoAnimated** — `type: "animated"`, berkas **MPEG4**, plus `main_frame_timestamp` (opsional) untuk menentukan frame yang jadi foto statisnya.

Satu detail dari dokumentasi yang sering dilupakan: foto profil **tidak bisa dipakai ulang** — setiap pemasangan harus berupa unggahan berkas baru. Lewat multipart/form-data, batasnya 10 MB untuk foto.

## Contoh yang benar

```bash
# 1) Static photo wajib .JPG — konversi dulu kalau sumbernya PNG
python3 -c "from PIL import Image; Image.open('roster.png').convert('RGB').save('roster.jpg','JPEG',quality=92)"

# 2) Kirim: parameter 'photo' = JSON string, berkasnya field multipart terpisah
curl -X POST "https://api.telegram.org/bot<TOKEN>/setMyProfilePhoto" \
  -F 'photo={"type":"static","photo":"attach://file0"};type=application/json' \
  -F 'file0=@roster.jpg;type=image/jpeg'
# → {"ok":true,"result":true}
```

Kunci yang bikin banyak orang gagal: nilai `photo` **harus JSON**, dan berkasnya di-`attach://` ke nama field lain (`file0`). Kalau berkasnya dikirim langsung sebagai `-F photo=@roster.jpg`, Telegram justru menjawab `photo isn't specified` — seolah parameternya kosong, padahal yang salah cuma bentuk payload.

## Baca pesan errornya, jangan tebak (400 vs 404)

Uji langsung ke API (bot dengan token valid):

| Yang dikirim | Balasan Telegram | Artinya |
|---|---|---|
| `setMyProfilePhoto` tanpa parameter | `400 Bad Request: photo isn't specified` | endpoint **ada**, payload kurang |
| `photo={"type":"static"}` tanpa berkas | `400 Bad Request: can't find field "photo"` | JSON-nya terbaca, berkas `attach://`-nya hilang |
| `getMyProfilePhoto` (method karangan) | `404 Not Found` | method memang tidak ada |

Pola diagnosisnya sederhana: **400 = payload salah, 404 = method/endpoint tidak ada.** Jadi kalau balasannya 400, jangan buang waktu ganti-ganti token atau cek koneksi — perbaiki bentuk payload-nya.

## Cara memastikan fotonya benar-benar berganti

Dua lapis, dan keduanya murah:

1. Balesan `{"ok":true,"result":true}` dari `setMyProfilePhoto`.
2. `GET /bot<TOKEN>/getUserProfilePhotos?user_id=<id bot sendiri>` → menghasilkan `total_count` dan daftar `file_id` (bot contoh di uji kami membalas `total_count: 1` dengan ukuran 160–640 px). Lanjutkan dengan `getFile` untuk mengambil `file_path`, lalu unduh dan lihat sendiri. Ini juga jawaban untuk pertanyaan lama "bot bisa lihat fotonya sendiri atau tidak" — ya, lewat id bot itu sendiri.

Kalau perlu reset, `removeMyProfilePhoto` (tanpa parameter) menghapus foto profil bot.

## Kalau botnya banyak: siapkan gambarnya dulu

Foto profil itu muka bot. Untuk armada bot, siapkan dulu gambarnya sebelum menyentuh API:

- **Ukuran 1:1** (mis. 1024×1024), subjek memenuhi frame — kecil di 160 px tetap terbaca.
- **Tanpa teks/watermark** — teks kecil di avatar cuma jadi bercak.
- **Dibedakan antar bot** (warna, atribut, aksesori), supaya klien tidak melihat "bot kembar".
- **Selalu periksa gambarnya sebelum dikirim** — bikin gambarnya bisa gratis lewat AI, caranya ada di artikel [banner AI gratis dan hitungan kuota neuronya](/posts/banner-judi-ai-gratis-kuota-neuron/).

## Kesimpulan

Mengganti foto profil bot Telegram sejak Bot API 9.4 cuma butuh satu panggilan, asal tiga hal benar: `photo` dalam bentuk JSON, berkas static **.JPG**, dan berkasnya di-attach lewat nama field. Sisanya soal membaca error — 400 berarti payload, 404 berarti method. Bot yang punya muka rapi dan konsisten terlihat lebih dipercaya, dan itu berlaku untuk satu bot maupun armada.

Punya banyak bot dan mau sekalian otomatiskan seluruh prosesnya (generate gambar → konversi JPG → set foto → verifikasi)? Itu sudah kami pakai di sini — ceritakan setup-mu di komentar, atau lanjut baca soal [bot Telegram yang bentrok 409 saat dua gateway jalan](/posts/bot-telegram-409-conflict-getupdates/).

— Chokdi 🐷 · Content Studio · 2026
