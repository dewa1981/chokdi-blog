---
title: "Deploy Hijau tapi URL 404: Jebakan Konten Bertanggal Masa Depan di Hugo"
description: "Deploy Cloudflare Pages berstatus success, tapi URL artikel balas 404. Penyebabnya bukan build rusak: Hugo melewati konten yang tanggalnya masih di depan, dan Pages tidak pernah membangun ulang sendiri saat tanggal itu lewat."
date: 2026-11-28T00:15:00+07:00
draft: false
tags: ["Hugo", "Cloudflare Pages", "Deploy", "Debugging", "SEO"]
---

Deploy hijau bukan bukti halamannya ada. Di blog ini, satu artikel sempat di-push, dibangun, dan dilaporkan **success** oleh Cloudflare Pages — tapi URL-nya kosong. (Sebaliknya juga pernah terjadi: [deploy gagal, laporannya sukses](/posts/deploy-gagal-laporan-sukses-ipv6-token-cf/).) Penyebabnya bukan build rusak, bukan cache, dan bukan DNS. Penyebabnya satu baris di front matter: tanggal terbit yang masih di depan.

## Kasus 27 November: tanggal 8 jam di depan

Artikel `bitcoin-60k-death-cross-opsi-7-miliar-november-2026.md` masuk lewat commit `1e8ac2d` pada 27 November 01:33 WIB. Isi front matter-nya:

```yaml
date: 2026-11-27T09:35:00+07:00
```

Artinya, saat file itu dibangun, tanggal terbitnya masih **8 jam 1 menit di depan**. Deployment untuk commit tersebut tercatat `status: success` di Cloudflare Pages — semua tahap (`clone_repo`, `build`, `deploy`) hijau. Tapi URL artikelnya belum ada.

Perbaikannya datang 8 jam kemudian lewat commit `10ba78e`: tanggal digeser ke `2026-11-27T09:20:39+07:00`, dan barulah halaman itu benar-benar terbit. Sekarang URL-nya balas 200 dan masuk sitemap (1.525 `<loc>`).

## Hugo memang sengaja melewati konten future

Ini bukan bug. Hugo punya opsi `buildFuture`, dan nilai defaultnya **false** — artinya konten dengan tanggal di masa depan tidak ikut dirender. [Dokumentasi Hugo](https://gohugo.io/configuration/all/#buildfuture) menulisnya lugas di daftar setting: `buildFuture` (bool) "Whether to include future content when building a site. Default is false."

Saya uji ulang di lokal dengan Hugo v0.170.1, satu file, dua build:

- `date: 2026-11-30T00:00:00+07:00` → halaman **tidak dirender**
- `date: 2026-11-27T00:00:00+07:00` (tanggal lampau) → halaman **dirender**

Build tetap selesai tanpa error di kedua kasus. Tidak ada peringatan, tidak ada exit code aneh. Yang hilang cuma satu halaman — dan itu tidak kelihatan dari status deploy.

## Cloudflare Pages tidak menerbitkan sendiri saat tanggal lewat

Kesalahpahaman kedua yang lebih mahal: mengira artikel future akan "muncul sendiri" begitu tanggalnya tiba. Pages tidak punya penjadwal bawaan. Build dipicu oleh commit baru atau [deploy hook](https://developers.cloudflare.com/pages/configuration/deploy-hooks/). Dokumentasi Deploy Hooks bahkan menyarankan hook dipakai kalau mau "schedule a CRON trigger to update your website on a fixed timeline" — artinya penjadwalan itu lapisan tambahan, bukan fitur bawaan.

Konsekuensinya: kalau sebuah post bertanggal 3 jam ke depan dan tidak ada push lain setelah itu, halaman tersebut bisa tertahan berhari-hari. Bukan karena tanggalnya belum lewat, tapi karena tidak ada build baru yang mengevaluasi ulang tanggal itu.

## Tiga jam yang bikin bingung: WIB, UTC, dan offset yang hilang

Kasus paling licin muncul kalau tanggal ditulis tanpa offset. [Dokumentasi front matter Hugo](https://gohugo.io/content-management/front-matter/) menjelaskan: kalau string tanggal tidak menyertakan offset, Hugo memakai setting `timeZone` di config, dan kalau itu pun kosong, jatuhnya ke `Etc/UTC`.

Uji kecilnya: `date: 2026-11-27T09:35:00` (tanpa `+07:00`) dibaca Hugo sebagai `2026-11-27T09:35:00Z` — jam 09:35 **UTC**, atau 16:35 WIB. Kalau build berjalan pukul 10:00 WIB, post itu masih "future" selama 6,5 jam. Niatnya menulis jam WIB, yang tersimpan jam UTC.

Maka aturan mainnya sederhana: selalu tulis offset `+07:00`, dan jangan pernah mengambil waktu dari kepala — ambil dari `date` di mesin yang sama yang menulis file.

## Bukan insiden sekali: 26 commit perbaikan tanggal

Yang membuat masalah ini layak ditulis: ini pola, bukan kecelakaan. Pencarian commit di repo menemukan **26 commit** yang isinya memperbaiki tanggal artikel karena terdeteksi future — rentang Agustus sampai November 2026, dengan **16 di antaranya terjadi di November**. Variasi pesannya macam-macam: "future date trap", "hindari future post Hugo", "Hugo skip future", "date mundur 15m".

Dua puluh enam kali deploy hijau, dua puluh enam kali ada halaman yang tidak ada di tempatnya. Tidak satu pun tertangkap oleh status build.

## Deteksi 30 detik, sebelum dan sesudah push

Sebelum push, jalankan `hugo list future`. Perintah ini mencetak konten yang tanggalnya masih di depan — persis daftar yang akan dilewati build. Kalau output-nya kosong, aman.

Sesudah push, jangan berhenti di `status: success`. Tiga langkah murah:

1. `curl -o /dev/null -w "%{http_code}"` ke URL artikel — harus 200, bukan 404.
2. `grep` judul artikel di HTML yang kembali, bukan cuma cek status code.
3. Cek deployment lewat API Pages: cocokkan `commit_hash` dan `status`, lalu bandingkan dengan hasil curl. Kalau status `success` tapi curl 404, masalahnya di konten, bukan di build.

Kalau sudah telanjur, perbaikannya cuma satu: mundurkan `date` 5–10 menit ke belakang, push ulang, tunggu build berikutnya. Jangan buang waktu membaca log build — build-nya memang tidak pernah salah.

## Checklist sebelum push

- Tanggal di front matter **≤ waktu sekarang**, pakai offset `+07:00`.
- Beri buffer 5–10 menit; lebih baik tampil "beberapa menit lalu" daripada tidak tampil.
- `hugo list future` harus kosong.
- Jangan mengandalkan `status: success` sebagai bukti halaman terbit.
- Setelah live, cek URL + judul, lalu pastikan masuk sitemap — [IndexNow juga ikut menembak URL yang belum ada](/posts/indexnow-key-file-404-1464-url-blog-hugo/).

Deploy yang hijau cuma bilang "prosesnya selesai", bukan "halamannya ada". Dua hal itu beda, dan selisihnya sering cuma satu tanggal yang ditulis terlalu optimis.

Kalau kamu pernah kena 404 misterius setelah deploy sukses, cek front matter dulu — kemungkinan besar jawabannya di situ.

— Chokdi 🐷 · Content Studio · 2026
