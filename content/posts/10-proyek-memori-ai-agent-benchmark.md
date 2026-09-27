---
title: "10 Proyek Memori AI untuk Agent — dan Mana yang Benar-Benar Dipakai"
date: 2026-09-27T23:55:00+07:00
draft: false
tags: ["AI", "Agent Memory", "Open Source", "Benchmark", "Knowledge Graph"]
---

Ada satu masalah yang hampir semua orang salah pahami soal AI agent.

Bukan soal modelnya kurang pintar. Bukan soal konteksnya kurang panjang.

Masalahnya sederhana: **agent mulai dari NOL setiap sesi baru.**

Model bisa menampung 1 juta token, tapi tetap bertemu kamu seperti orang asing setiap pagi. Kamu jelasin ulang proyeknya, aturannya, keputusan kemarin — lagi, lagi, dan lagi.

Ini yang coba diperbaiki oleh sekelompok proyek open-source yang belakangan naik cepat. Ada yang sudah kami pakai sehari-hari, ada yang baru kami pelajari minggu ini.

---

## Siklus yang Mereka Semua Kejar

Sebelum masuk daftar, ada satu pola yang berulang di semua proyek ini:

```
pengalaman → ingat → hubungkan → ambil kembali → bertindak → perbarui
```

Perhatikan kata **hubungkan**. Itu bagian yang paling sering dilewatkan.

Menyimpan fakta itu mudah. Yang sulit adalah tahu fakta mana yang berhubungan dengan fakta mana — dan kapan fakta itu berubah.

---

## 10 Proyek Memori AI

### 01. Mem0

**Repo:** `mem0ai/mem0` — 66K+ bintang

Salah satu yang paling populer. Pendekatannya menyimpan memori sebagai vektor dan mengambilnya kembali berdasarkan kemiripan makna.

**Cocok untuk:** agent pribadi, asisten yang perlu ingat preferensi pengguna.

---

### 02. Hindsight

**Repo:** `vectorize-io/hindsight`

Pendekatannya tiga langkah: **retain → recall → reflect**.

Bagian `reflect` yang membedakannya. Selain mencari fakta, dia bisa **merenung** — menyusun jawaban dari banyak memori sekaligus, bukan cuma mengembalikan potongan yang cocok.

**Cocok untuk:** agent yang perlu menyimpulkan, bukan cuma mengingat.

---

### 03. memU

**Repo:** `NevaMind-AI/memU`

Konsepnya beda: **memori disimpan sebagai wiki** — file markdown yang bisa dibaca manusia, bukan database yang cuma bisa dibaca mesin.

Yang menarik: dia bisa **mengubah riwayat kerja agent jadi skill markdown otomatis**. Bukan cuma mengingat apa yang terjadi, tapi menyaring pelajaran yang bisa dipakai lagi.

**Cocok untuk:** siapa pun yang ingin memorinya bisa dibuka, diedit, dan dibaca sendiri.

---

### 04. Cognee

**Repo:** `topoteretes/cognee`

Mengubah dokumen, kode, dan percakapan menjadi **knowledge graph** — graf pengetahuan yang menghubungkan entitas satu dengan yang lain.

Kelebihan praktisnya: bisa jalan **tanpa LLM sama sekali** (pakai model kecil lokal untuk ekstraksi). Jadi bisa gratis.

**Cocok untuk:** "company brain" — menyatukan dokumentasi, tiket, dan percakapan tim.

---

### 05. Graphiti

**Repo:** `getzep/graphiti` — 31K+ bintang

Knowledge graph, tapi dengan satu tambahan penting: **waktu**.

Setiap fakta punya jendela validitas — kapan mulai benar, dan kapan (kalau pernah) digantikan. Jadi sistemnya bisa jawab: *"apa yang benar sekarang"* dan *"apa yang benar bulan lalu"*.

Semua fakta juga bisa dilacak balik ke **episode** — data mentah asalnya.

**Cocok untuk:** data yang terus berubah dan perlu jejak historis.

---

### 06. OpenViking

**Repo:** `volcengine/OpenViking`

Dari Volcengine. Fokusnya membuat agent **stateful** — punya keadaan yang bertahan, bukan sekadar fungsi yang dipanggil ulang.

---

### 07. Letta

**Repo:** `letta-ai/letta`

Yang ini menambahkan dimensi berbeda: bukan cuma memori, tapi **identitas**.

Agent yang ingat siapa dirinya, bukan cuma apa yang terjadi. Memori dan kepribadian dijaga bersamaan lintas sesi.

**Cocok untuk:** agent yang perlu konsisten sebagai "satu orang" dari waktu ke waktu.

---

### 08. Letta Code

**Repo:** `letta-ai/letta-code`

Versi Letta yang diarahkan untuk kerja coding — memori melewati tumpukan alat (editor, terminal, repositori).

---

### 09. OpenMemory

**Repo:** `mem0ai/openmemory`

Pendamping Mem0 — lapisan memori yang bisa dipakai bersama banyak aplikasi, bukan terkurung di satu agent.

---

### 10. Agent Memory Benchmark

**Repo:** `vectorize-io/agent-memory-benchmark`

Ini yang paling sering dilewatkan orang, padahal mungkin yang paling berguna: **alat ukurnya.**

Semua proyek di atas mengklaim dirinya bagus. Benchmark ini mencoba menjawab dengan angka: berapa akuratnya, seberapa cepat, dan **berapa biayanya**.

---

## Kenapa Benchmark Ini Penting

Ada satu kalimat di dokumentasinya yang layak dikutip:

> Sistem yang skornya 90% tapi biayanya $10 per pengguna per hari **tidak lebih baik** dari yang skornya 82% dengan biaya $0.10.

Itu poin yang sering hilang dalam diskusi memori AI. Akurasi tanpa mempertimbangkan biaya hanyalah setengah cerita.

### Datanya Terbuka

Yang bagus dari benchmark ini: **semua hasilnya dipublikasikan** dalam bentuk JSON. Bisa diunduh, dibaca, dan diverifikasi sendiri.

### Contoh Hasil

Dari data yang dipublikasikan (60 sistem, beberapa dataset):

```
Skor tertinggi           : 95-96%  (di dataset tertentu)
Sistem populer (Mem0)    : 67-80%  (tergantung konfigurasi)
Pendekatan graf (Zep)    : 73%
Pendekatan identitas     : 74%
```

**Tapi hati-hati membaca angka ini.** Ada tiga jebakan:

**Pertama**, tidak semua sistem diuji di dataset yang sama. Skor 95% dari satu dataset tidak bisa dibandingkan langsung dengan skor 73% dari dataset lain.

**Kedua**, benchmark ini dibangun di sekitar **kasus chatbot** — tanya jawab soal riwayat percakapan. Sedangkan agent zaman sekarang **bekerja**: meneliti, merencana, menjalankan tugas bertahap. Tugas-tugas itu belum terwakili penuh.

**Ketiga**, ada dataset yang paling ketat: di sana sistem tidak hanya dinilai jawabannya benar, tapi juga **memori mana yang TIDAK boleh muncul**. Noise dihitung sebagai kegagalan total, bukan pengurangan skor. Di dataset ini, hampir semua sistem skornya rendah — yang menunjukkan masalahnya masih sulit untuk semua orang.

---

## Yang Kami Pelajari Sendiri

Kami sudah menjalankan sistem memori di produksi, dan sempat mencoba beberapa yang lain. Beberapa catatan praktis:

**Soal format penyimpanan.** Memori berbentuk markdown (bukan database) punya satu keunggulan yang sering diremehkan: **bisa dibaca dan diperbaiki manusia**. Kalau sistem otomatis salah menyimpan sesuatu, kita bisa buka filenya dan betulkan. Dengan database, kita bergantung pada alatnya.

**Soal biaya.** Sistem yang butuh LLM untuk setiap operasi memori akan menambah biaya terus-menerus. Sistem yang bisa jalan dengan model kecil lokal menghilangkan biaya itu — dengan konsekuensi kualitas ekstraksi yang lebih rendah.

**Soal integrasi.** Sebagian proyek menyediakan adapter khusus untuk agent tertentu. Kalau kebetulan agent kita didukung resmi, pemasangannya jauh lebih mulus daripada harus menyambung lewat protokol umum.

**Soal risiko.** Perhatikan apa yang **diubah** oleh alat memori di sistem kita. Kalau dia menyentuh file konfigurasi kepribadian agent, pastikan ada cadangan otomatis dan cara menghapus bersih.

---

## Tiga Jalur yang Masuk Akal

Kalau harus memilih berdasarkan jenis pekerjaan:

**Untuk kerja coding:**
```
Sistem yang sudah terbukti → knowledge graph → agent khusus coding
```

**Untuk agent pribadi:**
```
Sistem populer → pengetahuan temporal → agent dengan identitas
```

**Untuk "otak perusahaan":**
```
Knowledge graph → pengetahuan temporal → sistem produksi
```

Urutannya sengaja dari yang paling mudah dipasang ke yang paling matang.

---

## Catatan Penutup

Semua proyek di daftar ini menyelesaikan masalah yang sama dengan cara berbeda. Tidak ada yang "paling benar" — yang ada adalah mana yang cocok dengan bentuk pekerjaan kita.

Yang jelas: **konteks yang lebih besar bukan memori.**

Model bisa menampung sejuta token dan tetap lupa nama kamu besok pagi. Yang membedakan bukan seberapa banyak yang bisa dia pegang sekaligus, tapi seberapa banyak yang bisa dia **bawa pulang** dari satu sesi ke sesi berikutnya.

Dan itu masalah yang sekarang sudah punya banyak solusi — tinggal pilih mana yang pas.
