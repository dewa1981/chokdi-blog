---
title: "Hermes Agent Tidak Punya Bug Bounty: 1 Boundary yang Diakui, 6 yang Bukan"
date: 2026-10-21T17:10:00+07:00
draft: false
tags: ["Hermes Agent", "Keamanan", "AI Agent", "Open Source"]
---

Kalau kamu menjalankan agent AI yang bisa eksekusi shell, baca file, dan pasang plugin sendiri, pertanyaan yang paling penting bukan "agent-nya pintar atau tidak" — tapi "kalau modelnya ternyata dihipnotis lewat prompt injection, apa yang menahan dia?" Nous Research baru saja menjawab itu secara tertulis di `SECURITY.md` Hermes Agent: satu-satunya boundary yang mereka akui adalah **isolasi di level OS**. Sisanya — approval gate, redaksi kredensial, pattern scanner, allowlist tool — secara eksplisit disebut *heuristik, bukan kandang*. Kabar yang jarang ditulis media lain: **Hermes Agent tidak punya program bug bounty.**

## 🚧 Boundary yang diakui cuma satu: OS

Dokumen itu tidak berbelit. Kalimatnya: *"The only security boundary against an adversarial LLM is the operating system. Nothing inside the agent process constitutes containment."* Artinya, apa pun yang berjalan di dalam proses Python agent — termasuk security scanner yang kamu banggakan — sedang memeriksa string yang dikendalikan penyerang.

Lalu mereka membelah isolasi jadi dua postur yang harus dipilih sadar:

- **Terminal-backend isolation** — perintah shell dan file tools jalan di container, host remote, atau cloud sandbox. Tapi tool eksekusi kode, subprocess MCP, plugin, hook, dan skill tetap diangkat ke interpreter agent. Cocok kalau yang kamu takutkan cuma `rm -rf` hasil halusinasi.
- **Whole-process wrapping** — seluruh pohon proses agent dikurung. Semua jalur kena: shell, code execution, MCP, file tools, plugin, hook, skill loading. Ini postur yang **didukung** kalau agent memakan konten yang tidak kamu kendalikan: web terbuka, email masuk, kanal multi-user, MCP server pihak ketiga.

Penutupnya keras: operator yang pakai backend `local` untuk input tak terpercaya — atau mengira sandbox terminal ikut mengurung plugin — sedang beroperasi **di luar postur keamanan yang didukung**. Kalau kamu pernah merasa aman karena "sudah pakai Docker", baca ulang bagian itu.

## 🔑 Redaksi kredensial itu pengurang, bukan containment

Hermes menyaring environment untuk komponen berkepercayaan rendah: subprocess shell, subprocess MCP, script cron, dan child proses eksekusi kode. API key provider dan token gateway dicabut secara default; variabel yang dideklarasikan operator atau skill yang dimuat tetap lewat.

Dokumennya sendiri jujur menyebut efeknya: *"This reduces casual exfiltration. It is not containment."* Komponen yang hidup di dalam proses agent — skill, plugin, handler hook — bisa membaca apa pun yang bisa dibaca agent, termasuk kredensial di memori. Mitigasinya bukan scrubbing environment, tapi **review operator sebelum instal**.

## 🧩 Plugin: hak penuh, tanpa alarm

Plugin dimuat ke dalam proses agent dan berjalan dengan hak yang sama: kredensial yang sama, tool yang sama, hook yang sama. Yang lebih perlu diwaspadai, banyak plugin membawa service latar, network listener, dan dependency sendiri.

Aturan yang ditulis: boundary plugin pihak ketiga = review sebelum instal. Dan bug pada plugin yang jahat **bukan** kerentanan Hermes Agent — yang masuk ranah adalah bug di jalur instal/discovery yang menghalangi operator melihat apa yang sedang dia pasang.

## 💰 Tidak ada bug bounty

Ini bagian yang sering dilewatkan: laporan kerentanan lewat GitHub Security Advisories atau security@nousresearch.com, jangan buka issue publik. Dan tertulis datar: **"Hermes Agent does not operate a bug bounty program."**

Praktisnya buat kita: tidak akan ada hadiah uang untuk temuan CVE, tapi tidak ada salahnya melapor privat. Yang lebih penting, bedakan hasil tes dengan hasil rilis: **laporan diterima** bukan berarti **sudah dipatch**. Tunggu commit fix atau versi rilisnya sebelum bilang "sudah aman".

## 🕰️ Kenapa dokumen ini lahir

Konteksnya bukan kosong. Sepanjang 2026 framework agent kelas ini digempur temuan: sembilan CVE ke OpenClaw dalam empat hari pada Maret 2026 (termasuk CVE-2026-22172, CVSS 9.9 — client mendeklarasikan scope-nya sendiri saat handshake WebSocket), lalu audit independen terhadap Hermes Agent v0.8.0 yang dirilis April 2026 mengangkat 4 Critical dan 9 High di konfigurasi default. Sampai sekarang, tab security advisories di repo Hermes sendiri masih kosong; semua laporan masuk lewat kanal privat, bukan publik.

Yang menarik, tidak semua klaim audit itu masih berlaku di v0.22. Kebijakan plugin/dependency sudah bergeser ke arah review operator, dan audit adalah potret satu commit, bukan sifat permanen. Tapi sebagian peringatan lamanya tetap relevan (misalnya soal env rahasia yang bocor ke subprocess cron) — dan itu justru jadi bahaya sendiri: artikel lama terus beredar, orang mengira semuanya sudah beres, padahal yang berubah cuma sebagian.

## 🛠️ Praktisnya buat kamu yang self-host

- **Pilih isolasi sesuai input, bukan sesuai kenyamanan.** Agent yang baca web/email/DM orang asing → whole-process wrapping. Agent pribadi yang inputnya cuma kamu, dan kamu percaya operatornya → sandbox terminal cukup.
- **Anggap `~/.hermes/hooks/` dan `config.yaml` setara kode produksi.** Siapa pun yang bisa menulis ke situ sudah bisa jalan sebagai kamu.
- **Review skill & plugin sebelum pasang.** Bukan karena Hermes jahat, tapi karena boundary-nya memang di situ.
- **Jangan berharap hadiah dari laporan keamanan.** Lapor privat, dokumentasikan, tunggu fix dirilis.
- **Update rutin punya alasan keamanan, bukan cuma fitur baru.** Rilis cepat v0.22.x membawa perbaikan gateway; versi lama yang tak disentuh adalah versi yang tetap rentan.

## Kesimpulan

Dokumen keamanan Hermes Agent itu jarang dipuji justru karena jujur: mereka bilang sendiri bahwa semua pertahanan in-process hanyalah pencegah kecelakaan, dan satu-satunya kandang adalah OS. Buat operator, ini sebenarnya kabar bagus — kamu tahu persis di mana harus menaruh usaha. Tapi jangan menunggu bug bounty yang tidak ada, dan jangan menganggap "sudah di-sandbox" otomatis berarti "sudah terkunci". Cek posturnya hari ini, sebelum ada yang mengecek untukmu.

Kalau kamu juga menjalankan agent di server produksi, coba cek satu hal: backend terminal-mu `local` atau container? Jawaban itu menentukan seberapa besar kerusakan yang bisa terjadi kalau model hari ini salah baca satu halaman web.

Baca juga: [Docker Backend di Hermes: Sandbox per Sesi](/posts/docker-backend-hermes-sandbox-agent/) dan [Hermes Agent vs OpenClaw: 3 Sudut Pandang](/posts/hermes-vs-openclaw-3-sudut/).

— Chokdi 🐷 · Content Studio · 2026
