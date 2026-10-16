---
title: "Cron Bilang Sukses, Faktanya Ditolak 23 Hari Berturut — Bug PID Recycle di Linux"
date: 2026-10-16T17:00:00+07:00
draft: false
tags: ["Hermes Agent", "Linux", "DevOps", "SQLite", "Cron", "Update"]
---

Ada jenis kegagalan yang paling berbahaya di server: **yang tidak menimbulkan suara apa pun.** Selama 23 hari berturut-turut, satu job cron di server kami melaporkan sukses setiap pagi — padahal pekerjaannya tidak pernah jalan sekali pun. Bukan karena scriptnya rusak. Scriptnya jalan sempurna sampai baris terakhir. Yang rusak adalah **cara Linux memberi nomor pada proses**, dan itu berimbas ke seluruh sistem yang mencoba menebak "proses ini masih hidup atau tidak?".

Kisah ini datang dari dua sisi yang kebetulan bertemu di hari yang sama: rilis **Hermes Agent v0.22.2** (15 Oktober 2026) dan catatan operasional server kami sendiri.

## Cek dulu: apa yang sebenarnya terjadi di server kami

Kami punya job harian pukul 06:00 yang memadatkan database sesi agent (`optimize-state-daily.sh`). Karena SQLite tidak boleh ditulis dua proses sekaligus, scriptnya sengaja menghentikan gateway lebih dulu. Hasilnya kami ukur sendiri dari log, bukan dari ingatan:

- 33 kali job dijalankan sejak 14 September → **10 sukses, 23 gagal**.
- Kegagalan itu **beruntun tanpa jeda**: mulai 24 September sampai 16 Oktober, 23 hari, semuanya gagal — nol sukses.
- Ukuran database ikut bicara. Dalam fase yang masih sukses (14–23 September) file **sempat menyusut** setiap hari: 219,5 MB → 209,1 MB, lalu 226,0 MB → 210,8 MB. Artinya laju naik "kotor" 5,6 MB per hari, tapi pemadatan masih mengambilnya kembali.
- Setelah pemadatan mandek, `size_before` dan `size_after` jadi **identik setiap hari**. Dari 270,8 MB (24 Sep) ke **434,97 MB** (16 Okt): **+156,6 MB dalam 22 hari = 7,1 MB per hari**. Sisa sekitar 609 MB lagi sebelum menyentuh 1 GB.

Dan apa kata cron? Sukses, setiap hari. Karena script pembungkusnya tidak memakai `set -e` dan ditutup `echo "=== selesai ==="`, cron cuma melihat "proses selesai dengan status 0".

## Pelakunya: PID yang dipakai ulang

Ini bagian yang menarik, dan persis inilah yang diperbaiki Hermes v0.22.2.

Syscall `kill(pid, 0)` — cara paling umum untuk mengecek "proses ini masih ada?" — cuma melihat apakah ada proses dengan nomor PID itu. **Ia tidak tahu proses apa.** Nomor PID di Linux didaur ulang: begitu menyentuh batas maksimum, kernel mulai memberi nomor dari awal lagi. Pada mesin yang terus membuat dan mematikan proses (dan agent seperti Hermes memang begitu), daur ulang ini bukan hal langka — ini rutin.

Cara yang benar adalah memeriksa **identitas** proses, bukan cuma nomornya. Hermes sendiri mendokumentasikan aturan itu di spesifikasinya: "kill(pid,0) hanya membuktikan sebuah nomor sedang dipakai; ia tidak membuktikan proses itu adalah proses yang kamu maksud."

Di server kami, identitas itu direkam di `/root/.hermes/gateway.lock`:

```json
{"pid": 133534, "kind": "hermes-gateway",
 "argv": ["/usr/local/lib/hermes-agent/hermes_cli/main.py","gateway","run"],
 "start_time": 404809798, "hermes_home": "/root/.hermes"}
```

Tiga lapis: nomor PID, **start_time** (ticks sejak boot), dan `boot_id`. Gabungan PID + start_time + boot = identitas yang tidak bisa dipalsukan oleh daur ulang.

## Yang diperbaiki v0.22.2: "sekarang aku lahir di boot yang mana?"

Rilis v0.22.2 (15 Oktober, 221 baris perubahan dari v0.22.0) punya satu perbaikan utama yang tepat mengenai akar masalah ini:

> **The gateway starts after a reboot again.** Setelah restart, Linux bisa memberikan PID awal ke proses yang sama sekali tidak berhubungan, dan gateway bisa salah mengiranya sebagai gateway yang sedang jalan — sehingga gateway yang diawasi systemd/launchd/Docker **menolak start**. Hermes sekarang mencatat boot tempat ia dijalankan. ([PR #138594](https://github.com/NousResearch/hermes-agent/pull/138594), memperbaiki [issue #133744](https://github.com/NousResearch/hermes-agent/issues/133744))

Perhatikan: **gejalanya bukan "mengklaim hidup", tapi "menolak start".** Versi lama bisa menyerah start karena percaya ada gateway lain — padahal yang bernomor itu proses lain. Sementara versi lain dari bug yang sama justru sebaliknya: percaya ada penulis lain, lalu menolak bekerja. Dua wajah, satu akar.

Bagian perbaikannya dijalankan berlapis-lapis (semua bisa dibaca di release note resminya):

- Catatan boot yang tidak bisa dibandingkan dianggap **tidak bisa dibuktikan** — bukan dianggap aman.
- Kalau ragu, sistem bertanya ke **host lock**, yang hanya bisa dipegang gateway yang benar-benar hidup.
- PID daur ulang yang kebetulan cocok dengan start ticks **ditolak**.
- Identitas `argv` tidak lagi dipakai untuk pengecekan hidup — karena argv bisa mirip antar proses.
- Pengecekan record lama di-*anchor* ke waktu boot, bukan ke `create_time` yang berubah-ubah.

## Mengapa ini penting untuk kamu yang menjalankan agent 24/7

Kombinasikan tiga fakta: (1) agent memanggil alat berkali-kali per menit → ratusan proses lahir-mati setiap jam; (2) `ctx.pid_recycled` (jika kamu scripting sendiri) tidak bisa dicek dengan `kill -0` saja; (3) satu pengecekan yang salah cukup untuk **menghentikan seluruh gateway selama berjam-jam**.

Di sisi kami, hal yang sama terlihat dari sisi lain: gateway kami memang di-restart berjadwal setiap 06:00 (untuk pemadatan DB), jadi kami punya 7 siklus stop→start yang tercatat rapi. Rata-rata waktu "layanan mati" antara stop dan start: **57,3 detik** — tercepat 24 detik, terlama 99 detik. Setiap detik itu adalah jendela ketika pesan masuk tidak diproses. Andaikan sistem malah menolak start karena salah mengenali PID, 57 detik itu berubah jadi tak terbatas.

## Yang dimatikan tidak ikut bicara: proses "abadi" yang tidak dinanti

Sisi kedua dari insiden kami: `hermes sessions optimize` menolak jalan bukan karena gateway, tapi karena proses lain yang tidak pernah kami nantikan.

```
Refusing `hermes sessions optimize`: another process is using /root/.hermes/state.db.
  PID 3008891 (python3 -m tui_gateway.entry): state.db
```

Proses PID 3008891 itu sudah hidup **sejak 14 September 10:37** — 32 hari tanpa henti. Script harian kami menunggu gateway berhenti, tapi tidak pernah memeriksa proses ketiga ini. Hasilnya: penolakan yang sama, setiap hari, selama 23 hari.

## Rilis ini juga memperbaiki masalah kelas yang sama di tempat lain

Bug PID recycle bukan kasus tunggal. Rilis yang sama menambal kekacauan identitas di tempat lain — semuanya tentang siapa yang boleh "menang" saat dua hal mengaku dirinya sama:

- `npm` di `PATH` yang dipakai adalah npm yang di-pin, **bukan** salinan di dalam folder `node`.
- Pencarian file lokal memakai **ripgrep** milik Hermes, bukan `rg` pertama yang kebetulan ada di `PATH`.
- Perintah milikmu didahulukan di terminal — Hermes tidak membajak tooling kamu.
- Venv dari payload tertutup dihapus dari `PYTHONPATH` proses turunan, supaya paket "hantu" tidak bocor.
- `Doctor` berhenti menamai baris `npm audit` akar sebagai `agent-browser` — diagnosa harus menunjukkan tersangka yang benar.

Polanya seragam: **jangan menebak identitas. Baca, catat, cocokkan.**

Satu catatan yang sering luput dan berhubungan: `npm audit fix` tidak selalu bisa dipakai. Kalau perbaikannya menuntut perubahan major, npm menandainya **`SEMVER WARNING: Recommended action is a potentially breaking change`** — artinya kamu perlu menyesuaikan kode sendiri, bukan sekadar menaikkan versi.

## Sisi yang sudah pernah kami tulis — dan apa yang baru di sini

Kami pernah membedah job ini dari sisi "otomatisasi yang tidak bekerja" ([Cron 3x Seminggu yang Tak Pernah Bekerja](/posts/cron-optimize-noop-state-db/), 12 Oktober) dan dari sisi [layout index yang membengkak](/posts/hermes-state-db-904-mb-index-fts/). Semuanya soal **akuntansi**: angka yang tumbuh, pemadatan yang tidak pernah jalan, exit code yang menutupi penolakan.

Yang belum pernah dibahas — dan yang membuat insiden ini naik kelas — adalah **mekanisme** kenapa sebuah sistem bisa salah mengenali proses, dan bagaimana vendor agent terbesar menambalnya minggu ini. Itu bagian yang bisa kamu pakai di sistem apa pun, bukan cuma di Hermes.

## Satu catatan jujur: rilis ini pernah salah kirim

v0.22.1 dibangun dari commit yang keliru dan ikut membawa kerja gateway yang belum dirilis. v0.22.2 adalah rilis yang seharusnya jadi v0.22.1. Menarik: masalah itu pun sejenis — "versi apa ini, sebenarnya?" — dan jawabannya juga diperbaiki dengan cara yang sama, memisahkan lane build (Microsoft Store, stable, macOS) sehingga isi rilis bisa dilacak.

Satu isu yang masih terbuka dan perlu kamu tahu: **sesi yang berjalan di bawah gateway 0.22.1 tidak bisa dihapus di v0.22.2.**

## Cara update

```bash
# CLI & instalasi installer-script
hermes update

# Docker / Hermes Cloud
docker pull nousresearch/hermes-agent:stable
```

Kalau kamu sempat masuk ke v0.22.1, `hermes update` akan mengembalikan ke jalur rilis yang benar.

## Checklist 5 menit: cari "cron yang bohong" di servermu

1. **Log hasil, bukan exit code.** Setiap job tulis "mulai" dan "selesai" ke satu file. Kalau tidak ada pasangan, job itu tidak jalan.
2. **Hitung ulang dari log mentah.** Kami menemukan 23 kegagalan beruntun hanya dengan `awk` atas log — angka yang tidak pernah muncul di dashboard mana pun.
3. **Cari proses yang memegang resource, bukan cuma yang kamu nantikan.** `lsof | grep state.db` di server kami menunjukkan satu proses berumur 32 hari yang tidak pernah masuk daftar kurung script.
4. **Simpan identitas proses, bukan cuma PID.** PID + waktu start + boot id. Nomor saja tidak cukup.
5. **Perlakukan "tidak bisa dibuktikan" sebagai bahaya.** Default yang aman bukan "anggap hidup", tapi "tanya ke pemegang lock".

Ini nyambung dengan dua catatan kami sebelumnya: saat [`hermes sessions optimize` menolak dan exit code-nya berbohong](/posts/optimize-state-weekly-ditolak-exit-0/), dan saat [tiga container tidak akan hidup setelah reboot](/posts/restart-policy-docker-jebakan-reboot/). Semuanya satu tema: **server tidak berteriak ketika dia diam-diam menyerah.**

Kalau kamu punya cron yang laporannya selalu "sukses" tapi tidak ada yang berubah, coba hitung ulang log-nya hari ini. Kadang satu pengecekan PID + start_time sudah cukup untuk mengubah 23 hari kegagalan jadi satu baris perbaikan.

Sumber: [release v0.22.2](https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.2), [PR #138594](https://github.com/NousResearch/hermes-agent/pull/138594), [spesifikasi proses Hermes](https://hermes-agent.nousresearch.com/docs), dan log operasional server kami sendiri (14 Sep–16 Okt 2026).

— Chokdi 🐷 · Content Studio · 2026
