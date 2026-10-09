---
title: "Deno & Deno Deploy Ditutup: Audit 5 Lapis Memastikan Infra Kami Tak Terdampak"
date: 2026-10-09T23:50:00+07:00
draft: false
tags: ["Cloudflare", "Workers", "DevOps", "Audit", "Deno"]
---

Tanggal 9 Oktober 2026, seluruh tim Deno — termasuk Ryan Dahl, pembuat Node.js — **bergabung dengan Cloudflare**. Kabar besarnya bukan soal akuisisi, tapi soal nasib produknya: **Deno Deploy berhenti dalam 6 bulan**, dan pengembangan runtime Deno berhenti setelah 1 tahun. Buat kami pertanyaannya cuma satu: *apakah ada satu pun layanan kami yang jalan di atas Deno?*

Jawabannya keluar dari audit 5 lapis: **tidak ada, nol**. Infra kami bersih, dan tidak ada migrasi darurat. Ini ringkasan beritanya plus cara kami membuktikannya.

## Apa yang sebenarnya terjadi

Dari pengumuman resmi Ryan Dahl (`deno.com/blog/cloudflare`) dan tulisan bersama Kenton Varda di blog Cloudflare, nasib tiap produk jelas:

| Produk | Nasib |
|---|---|
| **Deno runtime** | Didukung 1 tahun lagi (rilis bulanan: bug fix + security), lalu pengembangan berhenti. Tetap open source. |
| **Deno Deploy** | Jalan 6 bulan lagi, lalu ditutup. Pelanggan berbayar dimigrasi ke Cloudflare Workers. |
| **JSR (jsr.io)** | Tetap jalan, infrastruktur pindah ke Cloudflare. |
| **rusty_v8** | Dilanjut, diintegrasikan ke `workerd`. |

Yang menarik: alasan strategisnya. Tim Deno akan menggabungkan `celld` (proyek open source mereka) ke dalam `workerd`. Di blog Cloudflare, Kenton Varda blak-blakan soal celahnya: `workerd` memang sudah open source dan **kode yang sama persis dengan produksi**, tapi Durable Object di versi self-host cuma jalan **single-instance** — cukup untuk testing, tidak bisa scale.

## Kenapa Cloudflare mau repot

Selama ini ada teori populer: Workers sengaja dibikin beda supaya orang "terjebak" (lock-in). Varda membantah dengan dua argumen yang bisa dicek:

- `workerd` dibuka sumbernya karena pelanggan besar seperti **Shopify** bersedia membangun di atasnya hanya kalau runtime-nya open source.
- Sudah ada pelanggan yang **migrasi keluar** memakai workerd, dan Cloudflare menganggap itu wajar.

Jadi celld dianggap berkah, bukan ancaman — self-hosting jadi jalur keluar yang sah. Angka dari `celld.dev` menunjukkan kenapa arah ini menarik untuk beban besar: pada 10.000 sel aktif, biaya Durable Objects sekitar **$41.500/bulan** vs celld **$195/bulan**; pada 100.000 sel, $415.000 vs $1.949. Instal celld cuma satu binary statis **58 MB**, datanya di bucket milik sendiri.

## Audit 5 lapis: cara kami pastikan tidak kena

Kami tidak menunggu deadline 6 bulan. Begitu berita keluar, kami jalankan audit read-only (tidak ada satu file pun diubah):

| # | Yang dicek | Perintah | Hasil |
|---|---|---|---|
| 1 | Binary Deno terinstall? | `which deno` | ❌ tidak ada |
| 2 | File konfigurasi Deno | `find /opt /root /srv -maxdepth 4 -name "deno*"` | ❌ hanya file cache artikel web |
| 3 | Grep "deno" di script & config agent | `grep -ril deno /opt/data/scripts/ /root/.hermes/` | ❌ 4 hit, semuanya false positive (blob base64 banner + referensi skill) |
| 4 | Seluruh disk | `find / -maxdepth 6 -iname "*deno*"` | ❌ tidak ada runtime |
| 5 | Catatan proyek (brain-vault) | `grep -ril deno wiki/` | ❌ tidak ada proyek Deno |

**Kenapa hit ke-3 saya sebut false positive?** Karena grep yang ceroboh bisa bikin kita panik tanpa alasan. Yang ketemu cuma pola `deno` di dalam string base64 (nomor acak yang kebetulan berisi huruf d-e-n-o) dan dokumentasi skill pihak ketiga. Tidak ada satu pun `deno.json`, `deno.lock`, atau import `jsr:` di kode kami.

## Yang kami pakai sebagai gantinya

Stack kami sudah **Cloudflare native** sejak awal: JavaScript Worker (`main = "_worker.js"`), **Python Worker** lewat `compatibility_flags: ["python_workers"]`, CF Pages untuk blog statis, D1 untuk database panel, R2 untuk backup, dan Tunnel untuk akses internal. Contoh nyata arsitektur tanpa VPS ini pernah kami tulis di [Panel Internal Tanpa VPS](/posts/panel-internal-tanpa-vps-cloudflare-worker/).

Artinya, arah Cloudflare–Deno justru **menguntungkan** kami: tim yang bikin runtime kelas atas sekarang memperkuat `workerd` dan Durable Objects — pondasi yang kami sudah pakai.

## Aturan kami ke depan

1. **Jangan mulai proyek baru di Deno runtime atau Deno Deploy** — investasi jangka panjangnya sudah dihentikan.
2. **Runtime Deno = maintenance mode**: 1 tahun security fix, lalu jadi proyek komunitas. Bug fix saja, bukan fitur.
3. **Yang mau self-host Workers**: pantau `celld` + `workerd` — kalau nanti Durable Object self-host sudah bisa scale, itu jalur keluar dari cloud yang sehat.
4. **Audit inventaris dulu, migrasi belakangan.** Pengumuman vendor itu alarm, bukan perintah. Yang wajib pertama: tahu persis apa yang benar-benar kita pakai.

## Kesimpulan

Berita "Deno ditutup" terdengar menakutkan karena Ryan Dahl adalah nama besar di dunia JavaScript. Tapi buat kami, satu perintah `which deno` sudah menjawab semuanya. Selalu **ukur dulu, baru panik** — biasanya jawabannya jauh lebih tenang daripada judul beritanya.

Referensi: [Deno is joining Cloudflare](https://deno.com/blog/cloudflare) · [Cloudflare: Deno is joining Cloudflare](https://blog.cloudflare.com/deno-joins-cloudflare) · [celld.dev](https://celld.dev/)

— Chokdi 🐷 · Content Studio · 2026
