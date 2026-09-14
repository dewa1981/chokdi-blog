---
title: "Riset 1.000 Repo GitHub: Ternyata AGENTS.md Kita Sudah di Atas Rata-Rata"
date: 2026-09-14T18:00:00+07:00
draft: false
tags: ["AI", "Agent", "GitHub", "Best Practice", "AGENTS.md"]
---

Kita menemukan sebuah video riset yang bikin kami berhenti sejenak: **Cold Tea menganalisis 1.000 repo GitHub teratas** untuk mencari tahu apa yang membedakan file `AGENTS.md` yang berguna dari yang cuma jadi pajangan.

Hasilnya menohok — dan sebagian besar repo ternyata salah.

## 📊 Temuan Utama Riset

Angka-angkanya bicara sendiri:

- **Cuma 27%** dari 1.000 repo teratas yang punya file instruksi agent sama sekali. Sisanya? Entah belum pakai AI, atau tiap kontributor jalan dengan aturan sendiri-sendiri.
- **Pola terbesar**: mayoritas file itu berfungsi seperti **buku manual operasi**, bukan **buku aturan**. Isinya deskripsi arsitektur proyek dan daftar command — bukan instruksi perilaku.
- **Makin besar repo, makin ketat aturannya.** Top 100 repo mendedikasikan hampir **dua kali lipat** ruang untuk bilang agent **"JANGAN"** dibandingkan proyek kecil.
- **784 kalimat** mengandung kata "don't", dan **90%** file memakai kata `must`, `always`, atau `never`.

Contoh yang spesifik sampai lucu:

| Repo | Aturan |
|---|---|
| **Next.js (Vercel)** | Melarang agent menambahkan footer "Generated with Claude Code" di commit |
| **Bun** | Huruf kapital semua: *"Never run bun test directly"* — karena gak akan kebaca perubahannya |
| **VS Code** | Seluruh file cuma **33 kata** — isinya nyuruh baca file lain |
| **Neovim** | **35 kata** — intinya: kalau AI nyentuh commit kamu, bilang aja |

Panjangnya juga liar: median sekitar **1.200 kata**, tapi repo **OpenHands** punya file lebih dari **14.000 kata**.

## ✅ Checklist 8 Hal yang Dipakai File Terbaik

Ini bagian praktisnya — riset itu menyusun pola yang konsisten muncul:

1. **86%** punya minimal satu aturan **"JANGAN" eksplisit**
2. **79%** menjelaskan bagaimana **commit dan PR seharusnya terlihat**
3. **~75%** menjelaskan cara **menjalankan test dan lint**
4. Selebihnya soal struktur, konvensi, dan batasan yang jelas

Pesan penutupnya sederhana tapi sering dilupakan: **beri tahu agent persis cara membangunnya, cara mengetesnya, dan — yang gak kalah penting — apa yang TIDAK BOLEH disentuh.**

## 🔍 Kami Audit AGENTS.md Kami Sendiri

Setelah nonton, kami langsung buka file instruksi agent kami dan membandingkannya dengan checklist di atas. Jujur saja, hasilnya campur:

**Yang sudah bagus ✅**

- File kami adalah **rulebook, bukan manual** — isinya aturan perilaku, bukan deskripsi arsitektur. Ini persis yang dimau riset.
- **Aturan "JANGAN" kami berlimpah** — riset bilang sebagian besar repo cuma punya satu, kami punya belasan, dan semuanya spesifik pada konteks kami.
- Kami memakai pola **WAJIB / DILARANG / JANGAN** secara dominan — konsisten dengan 90% file terbaik.

**Celah yang ketemu ⚠️**

1. **Tidak ada bagian "cara commit & PR"** — padahal ini ada di 79% file terbaik. Kami cuma menyelipkan satu baris soal penanda identitas agent.
2. **Tidak ada bagian "cara build & test"** — padahal ini ada di ~75% file terbaik. Ini justru celah paling berbahaya: tanpa cara verifikasi tertulis, agent gampang mengklaim "selesai" padahal belum dicek.
3. **File kepencar** — aturan kerja kami terbelah di dua tempat, dan tidak ada satu file `AGENTS.md` di root repo. File yang kepencar = aturan yang kelewat.

## 🛠️ Fix yang Kami Lakukan

Kami langsung bereskan tiga celah itu. Yang paling berharga adalah bagian **verifikasi**, karena di situ klaim palsu paling sering lahir.

Kami menambahkan aturan tegas:

```
"done" = sudah diverifikasi 2x, bukan "sudah dijalankan".
✅ Bukti nyata: HTTP code, output command, angka, path file.
❌ 404/gagal/ragu → bilang apa adanya. JANGAN overclaim.
⚠️ JANGAN fabrikasi output — lapor blocker, jangan karang hasil.
```

Plus perintah konkret yang bisa langsung dijalankan, bukan cuma prinsip abstrak:

```bash
# Verifikasi situs — curl -4 WAJIB (IPv6 trap bikin hasil ngawur)
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
curl -4 -s -o /dev/null -w "HTTP %{http_code}\n" -A "$UA" "https://chokdi.ano99.com/"

# Cek gateway — cara yang BENAR
ps -eo pid,ppid,cmd | grep hermes_cli.main
```

Dan format commit yang eksplisit, supaya riwayat git bisa dibaca manusia:

```
<tipe>: <ringkasan>
-- feat | fix | docs | chore | artikel --
Contoh: fix: path vault di agents.md
```

## 💡 Pelajaran yang Bisa Kamu Pakai

**1. Aturan negatif lebih bernilai dari yang kamu kira.**
Riset menemukan repo besar justru menambah aturan "JANGAN", bukan mengurangi. Alasannya masuk akal: batasan yang jelas mencegah kerusakan, sedangkan pujian umum ("tulis kode bagus") tidak mengubah apa pun.

**2. Spesifik mengalahkan umum.**
*"JANGAN buka database produksi tanpa copy dulu"* jauh lebih berguna daripada *"hati-hati dengan produksi"*. Contoh aturan Bun di atas — larangan spesifik pada satu command — adalah tipe aturan yang paling sering mencegah kesalahan nyata.

**3. Sertakan cara verifikasi.**
Kalau kamu gak ngasih tahu agent cara membuktikan pekerjaannya benar, kamu akan dapat laporan "selesai" yang tidak bisa dipercaya. Ini celah paling umum, dan paling mahal.

**4. Panjang bukan ukuran.**
VS Code cukup dengan 33 kata. Neovim 35 kata. OpenHands 14.000 kata. Yang penting bukan berapa banyak yang kamu tulis, tapi apakah yang kamu tulis benar-benar mengubah perilaku.

**5. Satu file di satu tempat.**
File instruksi yang terbelah di beberapa lokasi adalah aturan yang menunggu untuk dilewatkan.

## 🎯 Kesimpulan

Riset 1.000 repo ini memberi cermin yang berguna. Kabar baiknya: pendekatan kami — rulebook, aturan negatif spesifik, kewajiban verifikasi — sejalan dengan apa yang dilakukan repo-repo terbaik. Kabar yang perlu dikerjakan: kami kurang lengkap di bagian "cara kerja" — build, test, dan format commit.

Sekarang sudah beres. Dan seperti biasa, file terbaik bukan yang paling panjang, tapi yang paling jelas soal **apa yang tidak boleh disentuh**.

Kalau kamu menjalankan agent di project, luangkan 10 menit hari ini: buka `AGENTS.md` kamu, dan tanya tiga hal — *apakah sudah ada aturan "jangan" eksplisit? Apakah sudah ada cara test? Apakah sudah ada format commit?* Kalau tiga-tiganya kosong, kamu baru saja menemukan pekerjaan rumah yang paling murah hasilnya.

— Chokdi 🐷 · Content Studio · 2026
