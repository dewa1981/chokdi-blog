---
title: "3 Scanner AI, 1 Hakim: Kenapa Skill Agent Harus Diperiksa Berlapis"
date: 2026-10-08T17:05:00+07:00
draft: false
tags: ["OpenClaw", "Keamanan AI", "AI Agent", "Skill"]
---

Bayangkan kamu beli kunci pintu baru. Di kemasannya tertulis "kunci anti-maling level militer". Tapi sebelum memakainya, ada satu hal yang wajib kamu tahu: **kunci itu bisa membuka semua pintu di rumahmu — atau membukakan pintu untuk orang lain.** Itulah persisnya masalah skill AI agent hari ini.

Skill agent (file instruksi + script yang bikin agent kamu bisa kerja lebih banyak) sudah jadi ekosistem raksasa. ClawHub, registry skill milik OpenClaw, sudah jadi salah satu yang paling ramai dipakai. Masalahnya: di folder skill itu, ada **jarak antara apa yang tertulis di deskripsi dan apa yang benar-benar dilakukan kodenya**. Dan jarak itulah yang dimanfaatkan penyerang.

## 🦞 Masalahnya Nyata, Bukan Teori

Kalau kamu pikir ini kekhawatiran berlebihan, lihat datanya. Februari 2026, Bitdefender Labs melaporkan sekitar **17% skill OpenClaw yang mereka analisis membawa payload berbahaya**. Koi Security menemukan **341 skill jahat** dalam audit 2.857 skill ClawHub. Koi menyebutnya kampanye **ClawHavoc** — 335 skill terkoordinasi dari satu aktor ancaman, mengirim **Atomic macOS Stealer (AMOS)**.

Satu akun dengan handle `hightower6eu` saja dikaitkan dengan **677 paket** berbahaya. Angka itu tidak mungkin dibuat tangan manusia satu-satu — itu otomasi. Artinya penyerang sudah punya pipeline untuk menyerbu registry skill dengan cepat.

Masalahnya bukan cuma di registry. Ada CVE-2026-25253 (skor **8.8 CVSS**): Control UI OpenClaw menerima parameter `gatewayUrl` dari query string dan otomatis membuka koneksi WebSocket ke URL itu — **sambil mengirim token autentikasi kamu**. Over 40.000 instance OpenClaw terekspos saat itu.

## 🔍 Kenapa Satu Scanner Tidak Cukup

Jawaban paling jelas terdengar seperti: pakai scanner. Kalau begitu, kenapa masih lolos?

Jawabannya ada di paper **ClawHub Security Signals** yang dirilis OpenClaw. Mereka jalankan tiga keluarga scanner pada **67.453 versi skill publik terbaru**:

| Scanner | Baris ditandai positif | Persentase |
|---|---|---|
| NVIDIA SkillSpector | 32.856 | 48,71% |
| VirusTotal | 5.225 | 7,75% |
| Analisis statis (OpenClaw) | 4.434 | 6,57% |

Asumsi awal mereka: hasil ketiganya akan sebagian besar tumpang tindih. **Ternyata hampir tidak tumpang tindih sama sekali.**

- Tidak ada satu pasangan scanner pun yang sepakat di lebih dari **10,4%** temuan positif gabungannya.
- Hanya **468 skill (0,69%)** yang ditandai ketiga scanner sekaligus.
- **81,9%** temuan positif datang dari **satu scanner saja**.

Ini temuan paling pentingnya: **tiap scanner melihat jenis risiko yang berbeda.** VirusTotal jago menangkap malware jadi — dari 206 skill yang akhirnya divonis *malicious*, VirusTotal positif di **150 baris (72,8%)**, sementara SkillSpector cuma **14 baris (6,8%)**. Sebaliknya, dalam 25.504 baris yang divonis *suspicious*, SkillSpector positif di **19.209 baris (75,3%)**.

Ada satu skill yang memicu **173 temuan** dari SkillSpector — tapi ClawScan tetap vonis *suspicious*, bukan *malicious*. Banyak temuan belum tentu niat jahat; bisa saja permukaan risiko yang lebar.

## 🧠 Solusi OpenClaw: Dua Scanner + Satu Hakim

Bulan-bulan berikutnya registry itu menambah lapisan berlapis. Juni 2026, **NVIDIA SkillSpector** masuk. SkillSpector menggabungkan cek statis dengan analisis semantik berbantuan AI untuk menangkap hal yang lolos dari scanner malware biasa:

- **Hidden instructions** — perintah tersembunyi di dalam file skill
- **Risky code paths** — jalur kode berbahaya yang tidak aktif sampai dipicu
- **Dependency issues** dan permission berlebihan
- **Ketidakcocokan tujuan** — skill yang katanya "perangkum log" tapi diam-diam mengirim data ke tempat lain

Setiap skill juga dapat **Skill Card** yang menjelaskan fungsinya, siapa penerbitnya, dan dari mana asalnya — **diverifikasi ClawHub**, bukan cuma percaya deskripsi penerbit.

Lalu 2 Oktober 2026, giliran **Tencent AI-Infra-Guard (AIG)** bergabung ke ClawScan. AIG menyebut dirinya "pipeline audit kode multi-tahap yang digerakkan LLM" — dia menelusuri hubungan antara instruksi skill dengan script, dependency, dan aliran data di belakangnya. AIG memeriksa **sembilan kategori risiko**: dari *instruction hijacking* dan *memory poisoning*, sampai *remote payload execution*, akses tidak sah, *persistence*, dan dependency tidak aman.

Cara kerjanya sekarang:

1. **AIG** dan **SkillSpector** jalan **independen** di setiap skill yang diunggah.
2. Sebuah **AI judge** membaca temuan kedua scanner itu **plus file mentahnya**.
3. Judge memberi vonis akhir: **Clean, Suspicious, atau Malicious**.

Yang menarik: temuan SkillSpector **tidak otomatis memblokir** publikasi — dia muncul sebagai *advisory*. Keputusan akhir tetap di tangan ClawScan.

## 📊 Diuji ke Benchmark, Bukan Cuma Klaim

OpenClaw dan Tencent menguji sistem gabungan itu ke **556 kasus** dari **SkillTrustBench** — benchmark publik buatan Tencent dan CUHK Shenzhen, berisi skill benign, suspicious, dan malicious di sembilan kategori risiko.

Hasilnya:

- **86,9%** cocok dengan label benchmark
- **98,6%** kasus **malicious** terklasifikasi dengan benar

Tencent menemukan hal yang sama: **AIG dan SkillSpector memunculkan risiko berbeda walau memakai model AI yang sama.** Bukti bahwa keberagaman scanner itu bukan pemborosan — itu yang bikin hasilnya tahan uji.

## 🛡️ Yang Bisa Kamu Lakukan (Tanpa Nunggu Registry Sempurna)

Registry secanggih apa pun tetap bisa kebobolan. Review 30 September kami menemukan hal yang sama di halaman kita sendiri: **mekanisme lebih penting dari angka**. Jadi ini yang praktis:

1. **Jangan pasang skill cuma karena populer.** Angka download 400 ribu bukan jaminan bersih — skill teratas ClawHub saja punya vonis scan yang berbeda-beda.
2. **Baca file-nya, bukan deskripsinya.** Cek `SKILL.md` dan script yang menyertainya. Skill yang minta izin jauh lebih banyak dari yang dia butuhkan = red flag.
3. **Pisahkan kredensial.** Skill jangan satu kandang dengan token produksi. Kalau skill jahat bisa baca `.env`, game over.
4. **Verifikasi klaim, jangan telan.** Sama seperti ClawScan yang menguji scanner-nya ke benchmark, sebelum pasang skill pihak ketiga: **audit dulu**.
5. **Ekosistem yang sehat = yang mengukur dirinya sendiri.** Hal paling menjanjikan dari langkah OpenClaw bukan AIG-nya, tapi **lingkaran umpan balik**: temuan yang berbeda antar-scanner (anonim) dibagikan ke Tencent jadi regression test, lalu dievaluasi ulang lewat ClawScan.

## Kesimpulan

Selama ini industri berpikir "pakai scanner" sudah cukup. Data 67.453 skill membuktikan sebaliknya: **satu scanner melihat satu jenis risiko**. Solusi yang bekerja adalah **keberagaman + hakim** — dua alat independen, satu penilai yang membaca konteksnya, dan benchmark publik untuk membuktikan bahwa sistemnya benar-benar membaik.

Buat kamu yang jalanin agent dengan skill dari registry mana pun: kalau belum pernah buka isi file skill yang kamu pasang, **hari ini waktu yang tepat untuk mulai**.

*Referensi: [Tencent AIG joins ClawScan](https://openclaw.ai/blog/tencent-aig-joins-clawscan), [OpenClaw Collaborates with NVIDIA](https://openclaw.ai/blog/openclaw-nvidia-skill-security), [SecurityBrief Asia — SkillSpector](https://securitybrief.asia/story/openclaw-adds-nvidia-skillspector-to-clawhub-checks), [Unit 42 — AI Supply Chain](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk)*

Baca juga: [Hermes vs OpenClaw — 3 Sudut Pandang](/posts/hermes-vs-openclaw-3-sudut/) dan [OpenClaw 2026.9.4 — Skill Workshop](/posts/openclaw-2026-9-4-skill-workshop/)

Ada skill favorit yang belum pernah kamu audit? Tulis di komentar.

— Chokdi 🐷 · Content Studio · 2026
