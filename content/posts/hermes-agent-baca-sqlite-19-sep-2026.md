---
title: "Hermes Agent Bisa Baca Database SQLite Sendiri (19-Sep-2026)"
date: 2026-09-20T01:20:00+07:00
draft: false
tags: ["Hermes Agent", "AI Agent", "Tools", "Update"]
---

Kalau kamu pernah nyuruh AI agent "coba lihat isi file `.db` ini", jawabannya biasanya muter-muter: agent nulis script Python dulu, jalanin di terminal, baru baca hasilnya. Mulai 19 September 2026, Hermes Agent sudah bisa membuka database SQLite langsung lewat tool `read_file` — tanpa script perantara, tanpa risiko database kamu kena lock.

Ini bukan fitur yang heboh di media sosial, tapi buat orang yang kerja harian dengan data, ini jenis perbaikan yang bikin agent terasa jauh lebih pintar.

## 🗄️ Apa yang Berubah

Sebelumnya, `read_file` cuma kenal dokumen Office (`.docx`, `.xlsx`), notebook (`.ipynb`), dan PDF. File database ditolak dengan pesan polos: *"Cannot read binary file"*.

Sekarang ekstensi `.db`, `.sqlite`, dan `.sqlite3` ikut masuk daftar dokumen yang bisa dibaca. Hasilnya bukan dump biner yang bikin konteks agent meledak, tapi **ringkasan skema**:

- Nama setiap tabel plus jumlah barisnya
- Statement `CREATE TABLE` aslinya
- **5 baris pertama** tiap tabel ditampilkan sebagai tabel markdown
- Daftar index, view, dan trigger

Ibaratnya dulu kamu dikasih file `.zip` yang belum dibuka; sekarang kamu dikasih daftar isi plus cuplikan halamannya.

## 🔒 Kenapa Ini Aman

Bagian ini yang bikin saya senang. Databasenya dibuka dengan mode khusus:

```
mode=ro&immutable=1
```

Artinya database dibuka **read-only** dan koneksi **tidak menyentuh file WAL/journal** di sampingnya. Jadi database yang sedang dipakai aplikasi lain — misalnya MariaDB kamu sedang tidak, tapi SQLite app kamu sedang jalan — tetap bisa dibaca **tanpa mengambil lock** dan tanpa mengubah satu byte pun.

Ada juga pagar keamanan: file `.db` yang isinya bukan SQLite (magic bytes-nya tidak cocok) ditolak dengan pesan jujur *"not a SQLite database"*, bukan pesan biner generik yang bikin bingung.

Bonus yang jarang dibahas: sebuah angka yang dipakai di balik layar — **5 baris preview dan maksimal 200 tabel**. Sisa tabel yang tidak ditampilkan dihitung dan diberi keterangan, bukan dibuang diam-diam. Angka ini penting kalau kamu baca database produksi berisi ratusan tabel: kamu tahu ada yang disembunyikan, dan tahu cara query sisanya lewat terminal.

## ⚔️ Bonus: File Konflik Git Ikut Ketahuan

Ada satu lagi di patch yang sama. Kalau hasil baca file kamu mengandung penanda konflik git yang **berpasangan** (`<<<<<<<` dan `>>>>>>>`), hasil `read_file` sekarang membawa field:

```
conflict_blocks: 1
```

Beserta saran untuk menyelesaikan konfliknya dulu. Kuncinya kata **berpasangan**: kalau cuma ada satu penanda nyasar di dalam string atau file uji, tidak dihitung. Jadi tidak muncul alarm palsu.

## 🐛 Bug Nyata yang Ketemu Sambil Jalan

Yang menarik, ini bukan fitur yang direncanakan dari awal. Semuanya berawal dari issue #77367 — sebuah usulan panjang dari pengguna yang membandingkan Hermes Agent dengan proyek lain, lalu menyusun daftar celah fitur.

Waktu maintainer Hermes memvalidasi daftar itu secara langsung, pas bagian "SQLite reader" dan "enhanced fetch", mereka malah nemu bug sungguhan: sebuah URL yang menunjuk file `.sqlite` **mengembalikan 824.157 karakter data biner mentah** ke dalam konteks agent. Bukan halaman, bukan teks — sampah biner yang langsung menghabiskan jatah konteks model.

Akar masalahnya satu kalimat: dua jalur kode di Hermes terlalu percaya **bentuk input** (ekstensi file, atau asumsi "ini pasti dari halaman web") dan tidak memeriksa **isi bytes-nya**. Perbaikan patch #115974 akhirnya dilakukan dua arah sekaligus: mengajarkan `read_file` membaca SQLite, dan mengajarkan `web_extract` menolak payload biner dengan pesan yang menjelaskan jenis filenya, lalu mengarahkan ke `curl -L -o` + `read_file`.

Detail teknisnya: PR #115974 di-merge 19 September 2026 pukul 10:07:48 UTC (commit `11d68e4652`), menyentuh 8 file dengan +195/−17 baris. Signature dua huruf sengaja tidak dipakai untuk deteksi biner — supaya paragraf berbahasa manusia seperti "MZ…" atau "BMW…" tidak salah dituduh file ZIP.

## 💡 Praktik Buat Pengguna Indonesia

Tiga hal praktis yang bisa langsung kamu pakai:

1. **Backup SQLite sekarang lebih aman diperiksa.** Mau cek isi backup tanpa risiko mengubah apa pun? Cukup baca file `.db`-nya — mode read-only plus `immutable=1` menjaga backup tetap utuh.
2. **Jangan harap lihat semua data.** Cuma 5 baris pertama dan 200 tabel pertama yang tampil. Untuk analisis serius tetap lanjut ke terminal dengan `sqlite3`.
3. **Kalau agent lihat `.db` di dalam konteks, dia tidak lagi buta.** Ini yang paling kerasa: agent tidak lagi berasumsi file biner tidak berguna, dan tidak lagi menghabiskan konteks untuk byte sampah.

## 🧭 Kesimpulan

Patch kecil, dampak besar. Fitur "baca SQLite" ini contoh bagus bahwa kualitas agent ditentukan bukan cuma dari modelnya, tapi dari seberapa rapi tool-nya mengurus input yang tidak ramah. Dua pelajaran yang bisa dibawa ke proyek apa pun: **periksa bytes, bukan cuma ekstensi**, dan **buka data read-only kalau kamu cuma mau lihat**.

Pertanyaan buat kamu: sudah punya database SQLite di server yang belum pernah kamu beranikan buka lewat agent? Cobain sekarang — dan kabari hasilnya di kolom komentar.

— Chokdi 🐷 · Content Studio · 2026
