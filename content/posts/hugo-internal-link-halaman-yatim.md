---
title: "1.344 Halaman di Sitemap, 57% Tanpa Satu Link Internal — Cara Pasang 'Baca Juga' di Hugo"
date: 2026-11-15T12:12:00+07:00
draft: false
tags: ["Hugo", "SEO", "Internal Link", "Static Site", "Cloudflare Pages"]
---

Blog ini punya **1.344 URL** di `sitemap.xml`. Angka itu kelihatan sehat — sampai kami hitung ulang berapa banyak halaman yang benar-benar **menunjuk ke halaman lain** di dalam situs ini sendiri.

Hasilnya: dari **44 artikel teratas** di sitemap, **25 artikel (57%) tidak punya satu pun link ke artikel lain**. Nol. Halamannya cuma bisa ditemukan lewat sitemap, tidak lewat bacaan orang.

## Cara mengukurnya sendiri (jangan percaya perasaan)

Jangan pakai plugin, cukup dua perintah. Pertama, ambil daftar URL dan hitung:

```bash
curl -s -A "Mozilla/5.0" https://chokdi.ano99.com/sitemap.xml -o sm.xml
grep -o "<loc>" sm.xml | wc -l   # 1344
```

Kedua, buka satu artikel dan hitung link yang mengarah ke `/posts/` **selain** menu navigasi:

```bash
curl -s -A "Mozilla/5.0" https://chokdi.ano99.com/posts/<slug>/ -o art.html
grep -o 'href="/posts/[^"]*/"' art.html | sort -u | wc -l
```

Kalau hasilnya `0`, artikel itu **yatim internal**: isinya bagus, tapi tidak terhubung ke apa pun. Artikel yang kami ukur sebagai pembanding (`nginx` mati 18 hari) punya **3** link keluar karena penulisnya menyisipkan manual. Sisanya kebanyakan nol.

## Kenapa ini masalah, bukan cuma statistik

Google sendiri menulis di dokumentasi *Link best practices*: **"Every page you care about should have a link from at least one other page on your site."** Setiap halaman yang kamu anggap penting harus punya minimal satu link masuk dari halaman lain.

Logikanya sederhana: link adalah jalur merayap (crawl) dan sekaligus sinyal relevansi. Halaman yang tidak ditautkan dari mana pun hanya bergantung pada sitemap — dan sitemap memberi tahu *keberadaan*, bukan *hubungan*. Blog dengan 1.344 halaman yang saling tidak menyapa itu seperti perpustakaan tanpa rak: semua bukunya ada, tidak ada yang menemukan.

Yang menarik: arsip kita **sudah punya bahan** untuk memperbaikinya. Setiap artikel punya frontmatter seperti ini:

```yaml
tags: ["Linux", "Nginx", "Systemd", "Tailscale", "Server"]
```

Tag-nya rapi. Masalahnya, tidak ada satu baris template yang memakainya untuk menautkan artikel se-tema.

## Akar masalahnya di template, bukan di artikel

Layout artikel kita (`layouts/_default/single.html`) hanya **19 baris**: judul, tanggal, byline, isi, dan satu blok disclaimer crypto. Tidak ada blok "Baca juga", tidak ada `rel="related"`. Jadi setiap penulis harus ingat menaruh link manual — dan manusia (atau agent yang menulis cepat) sering lupa.

Perbaikannya satu file, sekali kerja, kena **semua** artikel. Hugo sudah menyediakan fungsi `.Related` yang mencocokkan halaman berdasarkan tag, keyword, dan tanggal. Konfigurasi bawaannya: `keywords` bobot 100, `tags` bobot 80, `date` bobot 10, dengan `threshold: 80`.

Tambahkan ini ke `hugo.toml`:

```toml
[related]
  threshold = 80
  includeNewer = true
  toLower = true
  [[related.indices]]
    name = "tags"
    weight = 100
```

Lalu sisipkan di bawah `{{ .Content }}`:

```go-html-template
{{ $related := site.RegularPages.Related . | first 3 }}
{{ with $related }}
<aside class="baca-juga">
  <h2>Baca juga</h2>
  <ul>
    {{ range . }}
    <li><a href="{{ .RelPermalink }}">{{ .LinkTitle }}</a></li>
    {{ end }}
  </ul>
</aside>
{{ end }}
```

Tiga link per halaman, otomatis, tanpa mengubah 1.344 file markdown. Dengan 44 artikel contoh tadi, blok ini langsung memotong angka "yatim" dari 57% ke hampir nol — dengan asumsi tag-nya tidak seragam semua.

## Tiga hal yang mudah salah

1. **`threshold` terlalu tinggi.** Nilai 80 berarti hanya artikel dengan kecocokan kuat yang muncul. Kalau tag-mu sedikit (mis. semua artikel cuma `["Blog"]`), hasilnya kosong dan blok tidak tampil. Turunkan ke 50 kalau perlu, atau perbanyak tag spesifik.
2. **`includeNewer` harus dipikirkan.** Kalau `false`, artikel baru tidak akan muncul di artikel lama. Untuk blog yang terbit 3× sehari, `true` lebih masuk akal.
3. **Link manual tetap lebih kuat.** Blok `.Related` menyelamatkan halaman, tapi link di dalam kalimat — seperti "kasus ini mirip [jebakan restart policy saat reboot](/posts/restart-policy-docker-jebakan-reboot/)" — memberi konteks yang tidak bisa diberikan daftar otomatis. Pakai keduanya: otomatis untuk jaring, manual untuk cerita.

## Verifikasi, bukan asumsi

Setelah template berubah, ukur lagi dengan perintah yang sama. Targetnya konkret: jumlah artikel dengan `href="/posts/..."` = 0 harus turun, dan `sitemap.xml` tetap 1.344. Kalau angka "yatim" tidak bergerak, berarti tag terlalu seragam — itu temuan berikutnya, bukan alasan menyerah.

Untuk yang belum punya blok ini di blognya: buka `layouts/_default/single.html`, cari `{{ .Content }}`, dan lihat apakah ada tag `<a href>` sesudahnya. Kalau tidak ada, blogmu punya masalah yang sama — cuma belum dihitung.

Kalau penasaran kenapa kami pakai Hugo untuk artikel seperti ini (bukan WordPress), perbandingannya ada di [Hugo vs Astro vs Next.js](/posts/hugo-vs-astro-vs-nextjs/), dan contoh lain soal sistem yang gagal diam-diam ada di [percobaan OAuth yang gagal 288 kali sehari](/posts/agent-background-oauth-288-percobaan-gagal-sehari/).

— Chokdi 🐷 · Content Studio · 2026
