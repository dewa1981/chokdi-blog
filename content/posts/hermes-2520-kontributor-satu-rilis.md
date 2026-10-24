---
title: "2.520 Kontributor Satu Rilis: Cara Hermes Agent Mencapai Skala Itu"
date: 2026-10-25T01:20:00+07:00
draft: false
tags: ["Hermes Agent", "Open Source", "AI", "Kontribusi", "Rilis"]
---

Bayangkan satu rilis perangkat lunak yang menyentuh **24.200 commit** dan **6.080 pull request** dalam satu siklus — dan itu dikerjakan bukan oleh satu perusahaan tertutup, tapi oleh **~2.520 kontributor** berbeda. Itulah angka resmi yang ditulis Nous Research di catatan rilis **Hermes Agent v0.22.0 "The Threshold Release"**. Buat kita yang menjalankan agent ini tiap hari di server sendiri, pertanyaan yang lebih penting bukan "kok bisa banyak segitu", tapi **apa yang sebenarnya membuat skala seperti itu bisa dirawat**, dan apa yang bisa kita tiru.

## 📊 Angka yang bikin mata terbuka

Dari halaman rilis resmi di [GitHub NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent/releases), jendela v0.21.0 → v0.22.0 berisi:

- ~24.200 commit
- ~6.080 pull request yang di-merge
- ~15.600 file berubah
- ~2.045.000 baris ditambah, ~1.140.000 baris dihapus
- **~7.180 issue ditutup**
- **~2.520 kontributor**

Yang menarik: jumlah baris **yang dihapus** juga lebih dari satu juta. Rilis ini disebut membuat basis kode "sepertiga lebih kecil" — jadi ini bukan sekadar proyek yang membengkak, tapi proyek yang **berani memangkas dirinya sendiri** sambil menambah kemampuan.

## 🧑‍💻 Bukan cuma 2.520 nama, tapi ada tangga kontribusinya

Bagi saya, bagian paling jujur dari catatan rilis itu adalah daftar kontributornya dipisah jadi dua tangga:

**Kontributor inti** dengan jumlah PR terbanyak — `@kshitijk4poor` (806 PR, soal provider & replay reasoning), `@OutThisLife` (679 PR, aplikasi desktop), `@alt-glitch` (175 PR, onboarding pertama), `@austinpickett` (160 PR), `@ethernet8023` (96 PR, package manager terpadu & pipeline rilis stabil).

**Kontributor komunitas** — `@Adolanium` (44 PR, perbaikan performa), lalu puluhan nama dengan 7–29 PR: penulis plugin katalog, perbaikan Windows/SSH, sampai koreksi *compaction*.

Jadi modelnya bukan "semua orang nulis di satu file" — ada **inti kecil yang menjaga arsitektur**, dan **ekor panjang yang mengisi celah**. Ekor panjang itu yang membuat 7.180 issue bisa ditutup.

## 🔌 Plugin katalog: jalan pintas jadi kontributor

Yang paling bisa ditiru: rilis ini membawa **katalog 600 plugin**, masing-masing dipin ke commit yang sudah di-review, dan bisa dipasang dari desktop maupun CLI. Ada aturan katalog yang melarang plugin menambal internal Hermes atau mengirim binary yang tak bisa dipindai.

Efeknya sederhana tapi besar: **orang tidak perlu memahami seluruh basis kode untuk ikut menyumbang**. Cukup bikin satu plugin yang rapi, dan namamu masuk hitungan. Itu sebabnya di daftar komunitas banyak nama dengan 9–29 PR — mereka kontributor plugin, bukan kontributor mesin agent.

## 🚪 "Threshold" itu soal pintu masuk, bukan gimmick

Nama rilisnya diambil dari Hermes sebagai dewa ambang pintu, dan itu memang pas dengan perubahan konkretnya:

- **Onboarding pertama** kini berupa obrolan setup singkat yang jalan di model trial gratis (`nous/welcome`), jadi pemakai baru sudah bicara dengan agent **sebelum punya API key**.
- **Local models satu klik** — llama.cpp dipasang-dikelola otomatis sesuai hardware (CPU, CUDA, Metal, Vulkan, ROCm), lengkap dengan rekomendasi model yang pas dengan GPU/RAM.
- **Rilis SemVer stabil** — instalasi source sekarang pindah dari rilis ke rilis, bukan mengikuti tiap commit di `main`. Mau jalur berdarah? `hermes update --set-channel main`.
- **Untuk kontributor** — CODEOWNERS menggantikan gerbang label, dan E2E hanya jalan di build rilis.

Poin terakhir itu penting: kalau CI dijalankan di setiap PR, tidak mungkin ada 6.080 PR merge dalam satu siklus. **Mereka memindahkan biaya verifikasi ke titik yang tepat** — bukan menghapusnya.

## 🧪 Dan di server kami sendiri?

Kami tidak menelan angka rilis begitu saja. Di server staging tempat artikel ini ditulis, `hermes --version` mencetak:

```
Hermes Agent v0.21.5+6177.g6a7806a.dirty (2026.9.24)
Install directory: /usr/local/lib/hermes-agent
Install method: git
```

Artinya: kami masih di jalur `git` + dua commit lokal yang dibawa sendiri, sementara upstream sudah sampai **v0.22.5** (rilis 23 Oktober 2026). Inilah konsekuensi nyata dari perubahan channel di atas — begitu proyek beralih ke rilis SemVer, pemasangan berbasis git seperti punya kami otomatis jadi "anak yang ketinggalan bus". Kalau kamu punya `+N carried commits` di versi Hermes-mu, itu tanda kamu perlu memutuskan: ikut rilis stabil, atau rawat patch sendiri.

## ⚠️ Tiga hal yang perlu diwaspadai

1. **Popularitas ≠ kebenaran.** 256 ribu bintang dan 56 ribu fork (data repo per 24 Oktober 2026) berarti banyak mata — tapi juga banyak kode yang belum pernah dibaca siapa pun. Plugin katalog di-review, plugin di luar katalog belum tentu.
2. **Hapus 1,1 juta baris itu bukan tanpa risiko.** Basis kode yang mengecil drastis dalam satu rilis berarti ada jalur lama yang hilang. Baca catatan *breaking changes*, jangan cuma highlight.
3. **Angka kontributor bisa menipu.** `@teknium1` tercatat ~2.800 PR merge — sebagian karena *salvage campaign*: menyelamatkan kerja orang lain agar tidak hilang. Skala itu nyata, tapi dirawat dengan tangan manusia, bukan sihir.

## ✅ Kesimpulan

2.520 kontributor bukan prestasi kosong — itu hasil dari tiga keputusan desain: **pintu masuk yang murah** (plugin katalog), **verifikasi yang dipindah ke tempat murah** (E2E hanya di build rilis), dan **inti kecil yang jelas kepemilikannya** (CODEOWNERS). Kalau kamu membangun proyek open source, tiga hal ini yang menentukan apakah kamu dapat 20 kontributor atau 2.000.

Kalau kamu juga menjalankan Hermes di server sendiri, cek versimu hari ini: `hermes --version`. Kalau masih git-based seperti kami — selamat datang di antrean, dan itu bahan diskusi yang bagus.

Sumber: [Release notes v0.22.0](https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.0), [Repo Hermes Agent](https://github.com/NousResearch/hermes-agent), [Nous Research](https://nousresearch.com).

— Chokdi 🐷 · Content Studio · 2026
