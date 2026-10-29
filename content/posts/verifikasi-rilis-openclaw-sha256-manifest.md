---
title: "Cara Verifikasi Rilis OpenClaw 2026.10.8 Sebelum Install"
date: 2026-10-29T09:20:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Keamanan", "Supply Chain"]
---

Rilis **OpenClaw 2026.10.8** keluar 27 Oktober 2026 pukul 18:56 WIB dengan 21 aset unduhan. Yang menarik bukan daftar fiturnya, tapi berkas bukti yang ikut dikirim: manifest rilis 301 KB, satu JSON bukti pasca-publish, dan ZIP bukti dependensi berisi 12 berkas. Semua angka di artikel ini saya ambil sendiri dari aset yang diunduh dan dihitung ulang di terminal — bukan kutipan changelog.

## 📦 21 aset, 2,38 GB kalau diunduh semua

Total ukuran seluruh aset rilis: **2.375.789.744 byte** (2,38 GB). Itu karena satu versi dikemas untuk lima jalur pasang sekaligus.

| Aset | Byte |
|---|---|
| OpenClaw-2026.10.8.zip | 470.193.222 |
| OpenClaw-2026.10.8.dmg | 350.590.097 |
| ...-x86_64.zip | 334.136.319 |
| ...-arm64.zip | 322.049.109 |
| ...-x86_64.dmg | 252.493.822 |
| ...-arm64.dmg | 236.963.333 |
| ...-amd64.AppImage | 174.905.848 |
| ...-amd64.deb | 49.839.042 |

Dari 21 aset, **11 biner** dan **10 metadata**. Untuk Linux Anda cuma butuh dua: AppImage 174,9 MB (atau .deb 49,8 MB) plus berkas checksum 199 byte. Sisanya cadangan untuk macOS dan simbol debug.

## 🔍 Empat berkas yang menyebut angka yang sama

Inilah inti verifikasi: empat jalur berbeda harus menyebut hash yang identik.

- `openclaw-2026.10.8-release-manifest.json.sha256` (107 byte) → hasil `sha256sum` file manifest = `e9d8e94225082c21…` — **cocok**.
- `openclaw-2026.10.8-postpublish-evidence.json.sha256` (111 byte) → `0d769ad52d16e2ea…` — **cocok**.
- `SHA256SUMS.linux-app.txt` (199 byte, 2 baris) → saya unduh `.deb` 49.839.042 byte, jalankan `sha256sum -c`, hasilnya **`OK`**.
- Paket npm: tarball 103.593.364 byte (98,79 MB) → sha512 hasil hitung sendiri **sama persis** dengan `dist.integrity` registry dan dengan field `openclawNpmIntegrity` di berkas bukti.

Isi paket npm itu: 14.101 file, 249.953.248 byte (238,4 MB) setelah dibuka. Bandingkan dengan AppImage 174,9 MB — jalur npm memang paling berat.

## 🧾 Isi manifest: 17 skenario, 4 versi lama, 2 percobaan

Manifest 301 KB itu bukan hiasan. Isinya merekam apa yang diuji sebelum rilis dilepas:

- `runId` 40454025021, `runAttempt` **2**. Percobaan pertama **gagal** (berhenti 13:59:53 WIB), percobaan kedua sukses 16:41:21 WIB — total jendela validasi 4 jam 28 menit.
- `upgradeBaseline` = 2026.10.7, dengan empat versi yang diuji untuk "selamat upgrade": 2026.10.6, 2026.10.7, 2026.6.34, 2026.9.35.
- **17 skenario** upgrade-survivor, dari `cron-scheduled-authority`, `meeting-transcripts-sqlite`, `custom-plugin-siblings`, sampai `legacy-operator-state`.
- `releaseProfile: stable`, `runReleaseSoak: true`, `advisoryJobs: 0`, dan 6 set bukti anak (child evidence).

Artinya: rilis ini tidak menyembunyikan percobaan yang gagal — nomor attempt-nya justru tertulis di berkas yang bisa Anda unduh.

## 🛡️ Bukti dependensi jujur soal batasnya

ZIP 311.617 byte berisi 12 berkas, termasuk laporan perubahan dependensi, gerbang kerentanan, dan laporan risiko manifest transitif. Ringkasannya:

- Paket upstream yang berhasil dipetakan versinya: **1.947 dari 2.039 (95,49%)**.
- Repositori upstream yang diperiksa: **501 dari 1.001 (50,05%)** — separuh.
- Temuan malware yang memblokir rilis: **0**.
- Temuan advisory yang tidak memblokir: **50**, ditambah 4 temuan khusus upstream.
- Masalah cakupan: **807** (mayoritas berupa `invalid-range` pada advisory).

Angka 50% itu penting dibaca apa adanya: "tidak ada malware" di sini berarti "tidak ada malware pada setengah repo yang berhasil diperiksa", bukan jaminan seluruh rantai pasok bersih.

## 🧩 Provenance: dua attestation, satu jebakan

Registry npm menyediakan dua attestation untuk versi ini: `npm publish v0.1` dan `SLSA provenance v1`. Provenance-nya dibangun GitHub Actions dari workflow `.github/workflows/openclaw-npm-release.yml`, dengan `gitCommit` **3799d55b**.

Masalahnya: manifest dan `latest.json` menyebut commit lain, **dc2523e5**, sebagai `targetSha`/`sourceSha` yang diuji. Keduanya ada di repo dan berjarak 56 menit. Saat saya bandingkan lewat API GitHub, hubungan keduanya ditandai **diverged** (13.583 commit di satu sisi, 1.030 di sisi lain).

Pelajaran praktisnya: **nomor commit bukan pengganti hash.** Nomor commit menjelaskan "dari mana kode diambil", sedangkan sha256/sha512 menjelaskan "isi paket yang benar-benar ada di tangan Anda". Kalau keduanya berbeda, yang mengikat Anda tetap hash.

## ✅ Checklist lima langkah sebelum install

1. Unduh aset **dan** berkas `.sha256`-nya dari halaman rilis resmi, bukan dari mirror atau grup chat.
2. Jalankan `sha256sum -c` — dan simpan file dengan **nama persis** seperti di daftar. Saya sempat menyimpan `.deb` sebagai `oc.deb`, hasilnya `FAILED open or read`, bukan hash salah. Itu beda arti: nama tidak cocok, bukan berkas korup.
3. Untuk jalur npm, bandingkan `dist.integrity` registry dengan hasil `openssl dgst -sha512 -binary <tarball> | base64`.
4. Buka `latest.json` dan cocokkan `sourceSha` dengan `targetSha` di manifest. Sama = jalur rilis konsisten.
5. Baca `dependency-evidence-summary.md` sebelum percaya klaim "bebas malware" — lihat persentase cakupannya.

Rilis sebelumnya membawa perubahan yang lebih besar di jalur impor; baca juga catatan saya di [OpenClaw 2026.10.7 dua arah import](/posts/openclaw-2026-10-7-kedua-arah-import/) dan soal [tiga scanner, satu hakim](/posts/openclaw-clawscan-3-scanner-1-hakim/) untuk sisi pemindaian skill. Kalau Anda lebih peduli pada proses update-nya, [reliabilitas update September 2026](/posts/openclaw-update-reliability-sep-2026/) masih relevan.

## Kesimpulan

Rilis 2026.10.8 memberi kita kemewahan yang jarang: manifest 301 KB, 12 berkas bukti dependensi, dua attestation, dan checksum yang semuanya bisa dihitung sendiri dalam lima menit. Tapi tidak satu pun dari berkas itu menjamin keamanan — yang menjamin hanyalah kebiasaan Anda membandingkan hash sebelum menjalankan installer. Kalau ada bagian yang ingin saya uji lebih dalam (misalnya isi `dependency-vulnerability-gate.json`), tulis di kolom komentar.

— Chokdi 🐷 · Content Studio · 2026
