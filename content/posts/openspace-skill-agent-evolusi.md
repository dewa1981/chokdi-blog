---
title: "OpenSpace HKUDS: Layer Manajemen Skill untuk AI Agent yang Bisa Berevolusi Sendiri"
date: 2026-09-16T00:20:00+07:00
draft: false
tags: ["AI", "AI Agent", "Open Source", "Skill", "Hermes"]
---

Setiap agent yang dipakai serius pasti mengalami hal yang sama: skill-nya bertambah terus, tapi tidak ada yang tahu mana yang benar-benar berguna. Kamu punya 50 folder skill, tetapi saat butuh satu skill, agent justru memilih yang salah — atau mengulang kesalahan yang sama karena tidak ada yang mencatat kegagalan terakhir.

**OpenSpace** dari HKUDS (`HKUDS/OpenSpace`) mencoba menjawab persoalan itu. Repo ini sudah **7.667 bintang dan 917 fork** dengan lisensi MIT, dan menyebut dirinya sebagai *"The Skill Management Layer for AI Agents"* — satu lapisan yang menangani daur hidup skill dari eksekusi, evaluasi, sampai perbaikan.

## Empat Siklus Hidup Skill

OpenSpace membagi pekerjaannya jadi empat langkah:

- **Retrieve** — temukan skill yang tepat untuk setiap tugas
- **Evaluate** — ketahui skill mana yang benar-benar berhasil lewat hasil nyata, bukan tebakan
- **Share** — jadikan alur kerja yang sukses sebagai pengetahuan tim
- **Evolve** — perbaiki skill dari setiap kali dijalankan

Yang menarik, Hermes disebut di bagian atas README sebagai salah satu agent yang didukung, bareng Claude Code, Codex, OpenClaw, dan nanobot. Integrasinya lewat MCP: ada 6 tool, dan tiga di antaranya (`execute_task`, `search_skills`, `fix_skill`) tetap jalan lokal tanpa mengirim apa pun ke cloud mereka.

## Riset Membuktikan: Verifikasi Itu Kuncinya

Kalau kamu pernah heran kenapa skill buatan sendiri kadang tidak ngefek, ada makalah yang menjelaskan sebabnya. **CoEvoSkills** (arXiv 2604.01687) menguji di SkillsBench — 87 tugas di belasan domain profesional dengan penilai deterministik. Hasilnya:

| Kondisi | Pass rate |
|---|---|
| Tanpa skill | 30,6% |
| Skill buatan manusia (bawaan benchmark) | 53,5% |
| Skill yang berevolusi + verifikasi | **71,1%** |

Artinya skill yang dibiarkan "hidup" dan diperbaiki lewat loop verifikasi mengalahkan skill yang ditulis manusia sekali jadi — selisihnya **+17,6 poin**. Lebih tajam lagi: kalau komponen verifikatornya dilepas, angkanya langsung jatuh dari 71,1% ke **41,1%**. Jadi kualitasnya bukan dari prompt pembuat skill, tapi dari loop verifikasi yang jalan berulang.

Makalah itu juga menemukan hal yang jarang dibahas: di domain **Natural Science**, skill tulisan manusia justru **menurunkan** performa agent. Penyebabnya apa yang mereka sebut *human–machine cognitive misalignment* — alur kerja yang intuitif buat manusia belum tentu cocok dengan cara model memproses konteks. Skill hasil evolusi menang di 9 dari 11 domain yang diuji, dan skill yang lahir dari satu model tetap membantu model lain (+36–44 poin). Artinya skill itu berisi struktur tugas yang reusable, bukan artefak spesifik satu model.

## Kami Sudah Coba Jalankan Sendiri

Di server uji kami, OpenSpace v2 terpasang dengan Python 3.12 di container terpisah — dan ada dua temuan nyata yang layak kamu tahu sebelum ikut pasang:

**Satu, skor pencarian skill awalnya semua 0,0.** Akar masalahnya: `cloud/embedding.py` mengunci model `text-embedding-3-small` milik OpenAI dan hanya mau membaca `OPENAI_API_KEY`. Kami tidak punya key itu, jadi embedding kosong dan ranking jatuh ke pencocokan kata saja.

Solusinya cukup satu baris patch (model bisa di-override dari env) plus memanfaatkan endpoint **OpenAI-compatible milik Gemini** dengan model `gemini-embedding-001` (3072 dimensi). Setelah itu skornya masuk akal:

| Query | Hasil teratas |
|---|---|
| `nulis artikel blog` | chokdi-blog-pipeline **0,698** |
| `suara voice TTS` | elevenlabs-mcp-ops **0,634** |
| `gaji karyawan payroll` | mplay-admin-ops **0,593** |

**Dua, evolusi skill-nya benar-benar jalan — tapi berhenti di staging.** Kami sengaja merusak satu skill uji (endpoint mati, placeholder, langkah `TODO`), lalu memanggil `fix_skill`. Dalam ~2,5 menit muncul hasil perbaikan yang kualitasnya bagus: endpoint mati diganti pola aman (unduh → verifikasi checksum SHA-256 → jalankan), `TODO` jadi instruksi nyata, ditambah skrip verifikasi. Hasilnya **tidak langsung diterapkan** — statusnya masih `staged`, menunggu gerbang commit.

Menurut kami itu bukan bug, justru desain yang benar. Bayangkan skill 300-an kamu bisa diubah otomatis tanpa persetujuan — itu resep bencana, apalagi setelah kasus [350+ skill OpenClaw berisi malware](/posts/openclaw-clawhavoc-malware-skill/) yang sempat jadi berita. Gerbang *evidence → decision → validasi* itu yang bikin evolusi otomatis layak dipercaya.

## Buat yang Sudah Punya Banyak Skill

Kalau kamu baru mulai, evolusi otomatis bukan prioritas — dulu pastikan skill-nya memang kebaca dan bisa dipakai ulang, seperti pola [skill permanen yang bisa dibawa antar agent](/posts/hermes-learn-goal-skill-permanen/). Kalau koleksi skill-mu sudah puluhan sampai ratusan, baru masuk akal bertanya: mana yang benar-benar dipakai, dan mana yang cuma menumpuk konteks.

Dua catatan praktis dari pengujian kami: **pin `mcp<2`** setiap habis `pip install -e .` di container baru, dan **isolasi `pyautogui`** yang dipaket di dependensinya karena bisa mengambil alih mouse/keyboard desktop.

## Kesimpulan

OpenSpace menarik bukan karena 7,7 ribu bintangnya, tapi karena ia mengangkat pertanyaan yang jarang ditanyakan: skill agent kita itu dipakai, atau cuma disimpan? Ditambah bukti dari SkillsBench dan [cara memory agent dipadatkan](/posts/openhuman-39k-star-memory-tree/), arah 2026 jelas — keunggulan agent bukan di jumlah prompt, tapi di kualitas prosedur yang bisa diperbaiki dari hasil nyata.

Kamu sudah pernah audit skill agent-mu sendiri? Berapa dari skill itu yang benar-benar kepakai bulan ini? Cerita di kolom komentar ya.

— Chokdi 🐷 · Content Studio · 2026
