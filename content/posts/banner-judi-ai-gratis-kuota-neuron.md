---
title: "Banner Judi dari AI Gratis: Hitung Kuota Neuron Sebelum Kebablasan"
date: 2026-10-01T18:20:00+07:00
draft: false
tags: ["AI", "Banner", "Cloudflare", "Judi", "Otomasi"]
---

Bikin banner dan artwork untuk landing page judi itu sekarang tinggal satu panggilan API — dan harganya bisa nol. Tapi ada satu angka yang hampir selalu dilupakan orang: **neuron**. Satu model bisa 8,7 kali lebih mahal dari model lain di provider yang sama, dan itu menentukan apakah kuota harianmu cukup untuk 7 gambar atau 63 gambar.

## Yang gratis itu bukan "unlimited"

Cloudflare Workers AI termasuk di paket Free: **10.000 neuron per hari tanpa biaya**, dan hitungannya reset tiap 00:00 UTC (07:00 WIB). Kalau lewat, tergantung paket: Workers Free → request gagal; Workers Paid → kelebihannya ditagih **$0,011 per 1.000 neuron**.

Masalahnya, "neuron" bukan satuan yang seragam antar model. Ambil dua model image generation FLUX.2 [klein] dari Black Forest Labs yang tersedia di Workers AI:

| Model | Satuan harga | Perkiraan neuron untuk banner 1344×768 |
|---|---|---|
| `@cf/black-forest-labs/flux-2-klein-9b` | 1.363,64 neuron per MP pertama (1024×1024) | ±1.364 neuron |
| `@cf/black-forest-labs/flux-2-klein-4b` | 26,05 neuron per tile output 512×512 | ±156 neuron (6 tile) |

Artinya dengan kuota gratis 10.000 neuron: **±7 gambar/hari dengan klein-9b**, atau **±63 gambar/hari dengan klein-4b**. Selisihnya 8,7×, untuk ukuran output yang sama.

Kalau diproyeksikan ke uang: klein-9b ≈ $0,015 per gambar (100 gambar = $1,50), klein-4b ≈ $0,0017 per gambar (100 gambar = $0,17). Bandingkan dengan penyedia image AI komersial yang bisa $17 sehari untuk volume produksi — selisihnya yang membuat kami pindah total ke jalur ini.

## Bukti tes, bukan teori

Kami tidak mau menebak, jadi tesnya dijalankan langsung dari server produksi (1 Okt 2026, 18:31 WIB) lewat gateway 9router kami:

- `POST /v1/images/generations`, model `cloudflare-ai/@cf/black-forest-labs/flux-2-klein-9b`, `size: 1344x768`
- Hasil: **HTTP 200**, balasan JSON **782.347 byte**, gambar ter-decode **586.725 byte**
- Isi sebenarnya: **JPEG 1344×768** (bukan PNG — walau namanya sering disimpan `.png`, magic bytes-nya `FF D8 FF`)

Temuan terakhir itu penting untuk pipeline: kalau kamu menyimpan `.png` hasil API lalu meng-upload apa adanya, kamu mengirim 587 KB per gambar ke setiap pengunjung. Setelah di-encode ulang (ffmpeg, kualitas tinggi), file yang sama jadi **182.240 byte — hemat 68,9%** tanpa ubah dimensi. Untuk banner yang tampil di hero [landing page judi](/posts/landing-page-judi-modern-tanpa-js/), ini beda antara halaman terasa instan dan halaman yang berat di 4G.

### Anggaran realistis satu hari kerja

Kebutuhan kami sehari: 6 artwork game (mahjong, olympus, fortune, casino, football, dragon) + 2–3 banner brand. Semua pakai klein-9b:

- 8 gambar × 1.363,64 neuron = **10.909 neuron** → sedikit di atas kuota gratis (≈ $0,12 kalau ditagih)

Pola yang lebih hemat: **klein-4b untuk iterasi prompt dan draft**, klein-9b hanya untuk versi final yang di-publish. Satu sesi "coba-coba 20 prompt" pakai klein-4b cuma ±3.100 neuron — budget yang sama di klein-9b baru dapat 2 gambar.

## Jebakan yang bikin banner gagal di menit terakhir

1. **Moderation cooldown.** Kalau generate banyak request beruntun, Cloudflare menandai sementara semuanya (error 3030) — termasuk prompt yang tadi lolos. Jeda **±30 detik antar request**, lalu prompt yang sama biasanya lolos 200.
2. **Teks AI sering typo.** Nama brand adalah hal pertama yang dicek mata pengunjung. Setiap gambar wajib lewat pemeriksaan visual sebelum dipakai — jangan asal pakai karena "sudah bayar neuron".
3. **Jangan pakai model salah.** `flux-1-schnell` menolak ukuran kustom (`width/height` → error 400); pakai keluarga `flux-2-klein`.
4. **Simpan master-nya sendiri.** Kadang hasil generate cuma nyangkut di URL sementara penyedia. Untuk aset yang dipakai di LP produksi, unduh + host di CDN sendiri, baru dipanggil dari HTML.

## Kesimpulan

Image AI untuk banner judi bisa benar-benar gratis, tapi cuma kalau kamu tahu kursnya. Tiga aturan yang kami pakai sekarang: **(1)** hitung neuron sebelum generate, bukan sesudah kena limit; **(2)** klein-4b untuk eksplorasi, klein-9b untuk final; **(3)** kompres sebelum deploy — 69% berat file itu uang dan kecepatan.

Kalau kamu juga produksi LP judi dalam jumlah besar, cek dulu [audit konversi tombol yang sering mati](/posts/audit-konversi-lp-judi-tombol-mati/) dan versi [AMP untuk halaman judi](/posts/amp-landing-page-judi-2026/) — gambar cuma satu dari tiga hal yang menentukan halaman itu menghasilkan atau tidak.

Referensi: [Cloudflare Workers AI — Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/) · [Black Forest Labs — FLUX.2 [klein]](https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence)

— Chokdi 🐷 · Content Studio · 2026
