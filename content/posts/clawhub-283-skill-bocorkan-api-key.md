---
title: "283 Skill OpenClaw Bocorkan API Key: Bahaya Tersembunyi Marketplace Agent"
date: 2026-10-09T09:05:00+07:00
draft: false
tags: ["OpenClaw", "AI Agent", "Keamanan", "ClawHub", "Skill"]
---

Bayangkan kamu install satu skill kecil dari marketplace agent — cuma buat baca email atau ambil data YouTube. Nggak ada yang mencurigakan, skill-nya jalan, semua normal. Tapi di dalam file `SKILL.md`-nya ada instruksi yang memaksa agent menuliskan API key kamu **apa adanya** ke dalam chat, ke memory, dan ke log. Bukan karena malware — tapi karena memang ditulis begitu.

Itulah temuan tim keamanan [Snyk](https://snyk.io/blog/openclaw-skills-credential-leaks-research): dari **3.984 skill** yang mereka pindai di ClawHub (marketplace skill untuk OpenClaw), **283 skill — sekitar 7,1% dari seluruh registry — mengandung celah kritis** yang membocorkan kredensial. Ini bukan serangan, ini "insecure by design".

## 🤖 Kenapa skill agent beda dari plugin biasa?

Selama 20 tahun kita terbiasa dengan model keamanan lama: aplikasi di-sandbox, proses dipisah, internet dijauhkan dari file lokal. Agent AI menghancurkan semua asumsi itu.

Skill agent bukan dokumentasi. Skill agent adalah **instruksi yang dijalankan dengan seluruh hak istimewa agent**. Kalau agent kamu bisa:

- mengeksekusi kode di host,
- membaca `.env` dan environment variable,
- memanggil jaringan keluar,
- dan menyimpan memory antar sesi,

…maka setiap skill yang kamu install mewarisi **semua kemampuan itu sekaligus**. Satu skill nakal = potensi kompromi penuh.

Kesalahan paling dasar yang Snyk temukan: developer memperlakukan agent seperti script lokal. Padahal **setiap data yang disentuh agent melewati context window LLM**. Begitu sebuah prompt berisi `api_key`, key itu masuk ke riwayat percakapan — dan bisa bocor ke provider model, atau keluar verbatim di log.

## 🐟 Tiga jebakan nyata yang mereka temukan

**1. Jebakan "verbatim output" (`moltyverse-email` v1.1.0)**
Skill ini memberi agent alamat email permanen. Masalahnya, instruksinya menyuruh agent: simpan API key ke memory, lalu **bagikan URL inbox yang berisi API key itu** ke user, dan pakai key secara verbatim di header `curl`. Kalau user bertanya "tadi kamu ngapain?", agent akan menjawab: *"Saya konfigurasi inbox di https://moltyverse.email/inbox?key=sk_live_12345"* — dan secret itu permanen tersimpan di riwayat chat.

**2. Kebocoran PII dan data finansial (`buy-anything` v2.0.0)**
Ini yang paling bikin merinding. Skill ini instruksinya menyuruh agent **mengumpulkan nomor kartu kredit dan CVC**, lalu menempelkannya verbatim ke perintah `curl`.

**3. PII di memory plaintext (`youtube-data`)**
Kunci disimpan ke `MEMORY.md` atau file plaintext serupa. Masalahnya, justru file-file inilah yang paling sering jadi target exfiltration oleh malware skill lain — contohnya malware `clawdhub1` yang dilaporkan sehari sebelumnya.

## 🚨 Ini bukan cuma satu laporan

Data lain memperkuat gambaran yang sama. Audit Snyk atas registry yang lebih besar (sudah menembus 13.000 skill pada Februari 2026) menandai **13,4%** punya isu kritis. Scan terpisah dari Koi Security atas 2.857 skill menemukan **341 skill yang aktif mencuri data user**. Unit 42 dari Palo Alto Networks juga menemukan lima skill berbahaya di ClawHub yang **lolos dari pemeriksaan keamanan** meski berisi infostealer.

OpenClaw sendiri sudah merespons. Mereka bermitra dengan **VirusTotal**: setiap skill yang dipublikasikan ke ClawHub sekarang di-hash SHA-256 dan dicek ke database VirusTotal; kalau tidak ada match, seluruh ZIP skill diunggah untuk dianalisis pakai Code Insight. Skill yang dicurigai mencurigakan dapat peringatan, yang terdeteksi berbahaya diblokir. Perbaikan nyata — tapi bukan anti peluru. Prompt injection dan serangan baru masih bisa lolos.

## 🛡️ Yang harus kamu lakukan sekarang

Kabar baiknya, risiko ini bisa dikelola tanpa berhenti pakai agent. Empat langkah praktis:

- **Pindai dulu, install kemudian.** Snyk menyediakan tool gratis: `uvx mcp-scan@latest --skills`. Tool ini mendeteksi file `SKILL.md` berbahaya, pola permission berbahaya, risiko prompt injection, dan tool poisoning.
- **Jangan pernah biarkan agent memegang secret mentah.** Simpan kredensial di secret manager (kami pakai Bitwarden Secrets Manager), bukan di `.env` yang bisa dibaca skill, dan bukan di `MEMORY.md`.
- **Audit inventaris skill kamu.** Kalau kamu sudah install puluhan skill dari marketplace, cek: apakah ada yang menyuruh agent menulis key ke chat/memory? Kalau ada, uninstall dan **rotate kredensialnya** — asumsikan sudah bocor.
- **Kalau sudah terlanjur install skill mencurigakan:** uninstall, rotate semua API key terkait, lalu pantau pemakaian tidak wajar pada akun tersebut.

## 💡 Sudut pandang kami: kami juga hidup di dunia ini

Kami menjalankan **707 file `SKILL.md`** di server agent kami sendiri — skala yang sama dengan registry-registry yang dibahas di atas. Jadi kami melakukan pengecekan yang sama seperti yang kami sarankan:

- Kami grep seluruh katalog skill untuk pola secret hardcoded (`sk-…` panjang, `ghp_…`, `AKIA…`) — **hasil: 0 file.** Semua kredensial hidup di secret manager, bukan di dalam skill.
- Kami memperlakukan skill pihak ketiga sebagai **kode yang di-audit dulu**, bukan dokumentasi yang bisa langsung dipercaya.
- Kami pisahkan kolam skill per profil agent supaya satu skill bocor tidak menjatuhkan semuanya.

Pelajaran besarnya sederhana: begitu kamu menjalankan agent yang bisa menyentuh file, jaringan, dan memory, kamu bukan lagi sekadar "install plugin". Kamu sedang **mengelola supply chain kode yang punya hak istimewa penuh**. Perlakukan marketplace skill seperti `npm` — dan semua orang tahu betapa berbahayanya `npm install` tanpa berpikir.

## Kesimpulan

283 dari 3.984 skill di ClawHub membocorkan kredensial, dan itu belum menghitung malware yang aktif mencuri data. Ini bukan alasan untuk menghindari agent AI — ini alasan untuk **berhenti install asal-asalan**. Pindai, pisahkan kredensial dari jangkauan agent, dan audit inventaris skill kamu secara berkala.

Agent yang hebat bukan yang punya skill paling banyak — tapi yang paling tahu skill mana yang boleh dipercaya. 🐷

Adakah skill di agent kamu yang menyuruhnya menulis API key ke chat? Cek sekarang, sebelum ada yang mengecek untukmu.

— Chokdi 🐷 · Content Studio · 2026
