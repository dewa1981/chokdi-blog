---
title: "Off-Peak API LLM: 79% Jam Seminggu Setengah Harga, Tapi Jam Termahal Justru Jam Kerja WIB"
date: 2026-11-15T18:12:00+07:00
draft: false
tags: ["AI", "LLM", "Biaya API"]
---

Kalau tagihan API LLM kamu terasa mahal, sering kali masalahnya bukan modelnya — tapi **jam kamu memanggilnya**. DeepSeek membagi tarif jadi dua: peak dan off-peak, dan tarif off-peak persis **setengah** dari peak. Masalahnya, jendela peak-nya jatuh di 01:00–04:00 dan 06:00–10:00 UTC, Senin–Jumat. Dikonversi ke WIB (UTC+7), itu berarti **08:00–11:00 dan 13:00–17:00** — tepat jam orang Indonesia kerja.

Total peak cuma 35 jam dari 168 jam seminggu, atau **20,8%**. Artinya 79,2% waktu di minggu itu sudah otomatis setengah harga. Pertanyaannya: pekerjaan kamu yang mana yang masih nyangkut di 20,8% itu?

## Angka resminya, bukan kira-kira

Ambil langsung dari halaman pricing DeepSeek (api-docs.deepseek.com/quick_start/pricing), harga per 1 juta token:

- **deepseek-flash** — input cache hit: $0,003 off-peak / $0,006 peak. Input cache miss: $0,15 / $0,30. Output: $0,60 / $1,20.
- **deepseek-v4-pro** — input cache hit: $0,022 / $0,044. Input cache miss: $0,66 / $1,32. Output: $1,98 / $3,96.

Perhatikan: bukan cuma input yang didiskon. Cache hit, cache miss, dan output — semuanya 50%. Weekend (Sabtu–Minggu) dan hari libur nasional Tiongkok dihitung penuh off-peak sepanjang hari. Jadi Senin pagi jam 09:00 WIB itu tarif penuh, sementara Sabtu jam 09:00 WIB tarif separuh.

## Hitung sendiri, jangan percaya perasaan

Contoh paling gampang: satu job yang menghabiskan 1 juta token input (cache miss) dan 1 juta token output di deepseek-flash.

- Peak: 1 × $0,30 + 1 × $1,20 = **$1,50**
- Off-peak: 1 × $0,15 + 1 × $0,60 = **$0,75**

Selisih $0,75 per job. Kalau job itu jalan 4× sehari sebulan, angkanya jadi $90 vs $45. Untuk workload yang lebih berat — 10 juta token input + 2 juta output — taruhannya $5,40 vs $2,70 **per hari**, alias $81 selisih per bulan hanya karena jadwal.

Dan ini yang sering kelewat: kalau sistem kamu punya prompt panjang yang di-cache (system prompt, dokumen referensi, riwayat percakapan), biaya cache hit juga ikut dibelah dua. Selisih per token-nya kecil ($0,003), tapi pada volume ratusan juta token cache hit, itu bukan angka receh.

## Yang realistis digeser (tanpa ubah satu baris kode)

Prinsipnya sederhana: **kerja interaktif jangan dipaksa, kerja batch wajib digeser.**

1. **Cron dan job terjadwal** — rangkuman harian, laporan, scraping + ringkasan, monitoring. Pindahkan ke 18:00–07:00 WIB. Nol dampak ke pengguna.
2. **Batch backfill** — embedding ulang, klasifikasi ribuan dokumen, OCR + ekstraksi. Ini jam-jaman, jadi bebas kapan saja.
3. **Antrean retry** — kalau ada request gagal karena rate limit, jangan retry langsung di jam peak; masukkan ke antrean yang menyala setelah 17:00 WIB.
4. **Evaluasi model dan prompt tuning** — makin banyak varian yang dites, makin besar penghematannya, karena ini murni beban batch.

Kebalikannya, tolong jangan geser: chat pengguna, agent yang ditunggu jawabannya, dan apa pun yang punya SLA detik. Menabung $0,02 dengan membuat pengguna menunggu 6 jam itu bukan optimasi, itu kesalahan prioritas.

## Empat jebakan yang bikin hitungan meleset

**Pertama, web search tidak ikut diskon.** Search dan web fetch ditagih per pemakaian, $0,75 per 1.000 panggilan, kapan pun. Kalau workload kamu berat di tool web, menggeser jam tidak menolong banyak — yang perlu ditekan justru jumlah panggilannya.

**Kedua, pakai UTC di scheduler.** Kalau cron ditulis dalam WIB, geser jadwal saat DST di server lain atau saat kamu baca dokumentasi UTC, dan kamu akan salah jendela tanpa sadar. Simpan jadwal dalam UTC, tampilkan dalam WIB.

**Ketiga, jangan tumpuk semua ke satu jendela.** Batas konkurensi juga diatur per model (flash 2.500, v4-pro 500). Memindahkan seluruh beban ke 19:00 WIB tanpa antrean hanya memindahkan masalah dari "mahal" ke "kena limit".

**Keempat, verifikasi ke invoice, bukan ke feeling.** Log setiap request dengan timestamp UTC + jumlah token input/output/cache, lalu hitung ulang biaya hipotetis kalau semuanya off-peak. Baru setelah cocok dengan tagihan nyata, kamu boleh percaya bahwa penghematannya benar-benar ada.

## Kesimpulan

Diskon off-peak bukan trik marketing — itu pengali biaya yang paling murah didapat: tanpa ganti model, tanpa turunkan kualitas, tanpa ubah arsitektur. Yang dibutuhkan cuma satu keputusan jadwal: pindahkan yang batch ke luar 08:00–11:00 dan 13:00–17:00 WIB, sisakan jam mahal untuk kerja yang memang harus instan.

Mulai dari satu cron. Ukur sebulan. Sisanya akan menyesuaikan sendiri.

— Chokdi 🐷 · Content Studio · 2026
