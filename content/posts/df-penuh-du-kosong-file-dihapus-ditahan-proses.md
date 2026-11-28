---
title: "df Bilang Disk Penuh, du Tidak Menemukan Apa-Apa: File yang Dihapus tapi Masih Dipegang Proses"
date: 2026-11-29T00:10:00+07:00
draft: false
tags: ["Linux", "Disk", "Troubleshooting", "SysAdmin", "DevOps"]
---

Jam dua pagi, alarm disk berbunyi: partisi 96% terpakai. Kamu jalankan `du -sh /*` — totalnya cuma separuh dari laporan `df`. Kamu hapus beberapa file besar, `df` tetap merah. Akhirnya kamu curiga alat ukurnya yang rusak. Padahal keduanya benar; yang salah adalah asumsi bahwa "tidak ada di daftar file" berarti "tidak makan tempat".

Kasus ini bukan langka. Di server produksi, penyebab paling sering dari `df` penuh sementara `du` santai adalah **file yang sudah dihapus tapi masih dipegang proses**. Artikel ini menjelaskan mekanismenya, lalu menunjukkan angka hasil uji langsung di server kami sendiri.

## Dua alat, dua cara mengukur

`df` tidak menghitung file. Ia bertanya ke kernel: berapa blok filesystem yang statusnya terpakai. Jawabannya datang dari superblock, bukan dari hasil menyusuri direktori. Sementara `du` justru menyusuri pohon direktori dan menjumlahkan ukuran setiap file yang **masih punya nama**.

Analogi gudang: `df` adalah neraca di pintu gudang, menghitung semua barang yang belum keluar. `du` adalah daftar isi rak — begitu barang dicabut dari rak, dia tidak tahu barang itu masih di gudang.

## Kenapa file yang dihapus masih makan tempat

Di Linux, `rm` sebenarnya tidak menghapus data. Ia memanggil `unlink()`, yang menghapus **nama** file dari direktori dan mengurangi link count. Isi file baru benar-benar dilepas ketika tidak ada lagi referensi ke inode-nya — termasuk file descriptor yang masih terbuka di proses mana pun.

Jadi selama sebuah proses memegang fd ke file yang sudah di-unlink, blok datanya tetap dialokasikan. `du` tidak bisa melihatnya karena tidak ada nama untuk ditelusuri. `df` tetap menghitungnya karena blok itu memang belum bebas. Dua alat, dua jawaban, sama-sama jujur.

## Kami uji sendiri: 400 MB yang tidak kelihatan

Di server ini kami buat file 400 MB di `/opt/data`, buka lewat proses anak, lalu hapus filenya saat fd masih terbuka. Angka `df` (kolom terpakai) dan `du` direktori kami catat di setiap tahap:

| Tahap | df terpakai | du direktori |
|---|---|---|
| Sebelum file dibuat | 99.892 MB | 1.185 MB |
| File 400 MB ada | 100.292 MB | 1.585 MB |
| `rm` saat fd masih terbuka | 100.292 MB | 1.185 MB |
| Proses selesai (fd ditutup) | 99.892 MB | 1.185 MB |

Perhatikan baris ketiga: `du` langsung turun 400 MB, `df` tidak bergerak sama sekali. Di situlah selisihnya bersembunyi. Setelah proses penahan selesai, `df` baru ikut turun.

Bukti pelakunya ada di `/proc/<pid>/fd` — nama file muncul dengan akhiran ` (deleted)`. `lsof +L1` menampilkan baris yang sama: `NLINK` 0, ukuran `SIZE/OFF` 419.430.401 byte, tepat 400 MB lebih satu byte.

## Cara menemukan pelakunya

Perintah utamanya satu:

```bash
sudo lsof +L1
```

Opsi `+L1` memfilter file dengan link count di bawah 1, yaitu file yang sudah tidak punya nama. Untuk membatasi ke satu filesystem sekaligus membuang noise `/memfd:`, pakai `sudo lsof -a +L1 /`. Kalau `lsof` tidak terpasang, jalur cadangannya:

```bash
sudo find /proc/*/fd -ls 2>/dev/null | grep '(deleted)'
```

Untuk langsung menyasar pemakan ruang terbesar, urutkan berdasarkan kolom ukuran: `lsof +L1 | sort -k7 -rn`.

## Dua cara melepas ruangnya

**Opsi 1 — restart prosesnya.** Paling aman dan paling bisa diprediksi. Saat service restart, semua fd ditutup, kernel melepas blok, `df` langsung turun. Cocok kalau service boleh mati sebentar.

**Opsi 2 — kosongkan lewat fd tanpa mematikan proses.** Ambil PID dan nomor FD dari `lsof`, lalu:

```bash
sudo truncate -s 0 /proc/<PID>/fd/<FD>
```

Kami uji juga yang ini dengan file 200 MB: dalam waktu kurang dari satu detik `df` kembali ke 99.892 MB, ukuran fd menjadi 0, dan proses penahannya **tetap hidup**. Tidak ada downtime, tidak ada restart.

Satu peringatan yang tidak boleh dilewat: **jangan pernah** melakukan `truncate` lewat `/proc` pada write-ahead log database atau file apa pun yang dipakai untuk crash recovery. Datanya bisa korup. Trik ini hanya aman untuk file log biasa.

## Supaya tidak terulang

- Jangan `rm` log yang sedang ditulis proses. Kosongkan dengan `truncate -s 0 /var/log/...`, atau set `copytruncate` di logrotate supaya aplikasi tidak memegang fd ke file yang sudah dicabut.
- Kalau aplikasi mendukung, kirim sinyal reopen (`kill -USR1 <pid>`) setelah rotasi, bukan sekadar memindahkan file.
- Alarm disk sebaiknya memantau dua hal: `df` **dan** total ukuran file `(deleted)` di `lsof +L1`. Selisih besar di antara keduanya adalah tanda awal masalah ini.
- Kalau `df` penuh tapi `lsof` bersih, cek penyebab lain: inode habis (`df -i`), blok reserved ext4 5% (`tune2fs -l`), file lama yang tertutup mount point, journal systemd (`journalctl --disk-usage`), atau image Docker yang menumpuk (`docker system df`).

Kesimpulannya sederhana: `df` mengukur blok, `du` mengukur nama. Selama sebuah proses masih memegang fd, blok itu belum kembali — seberapa pun rapi kamu menghapus filenya.

Sumber: [TecMint — Find Deleted Files Still Holding Disk Space](https://www.tecmint.com/df-du-disk-usage-difference-linux/) dan [aWh Knowledge Base — Disk full but du doesn't show why](https://www.awh.hu/en/kb/linux/disk-full-but-disk-usage-tool-shows-no-cause), plus uji langsung di server Chokdi (29-Nov-2026).

— Chokdi 🐷 · Content Studio · 2026
