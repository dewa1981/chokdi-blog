---
title: "MiniMax Code + BYOK 9router: Coding Agent Gratis dengan Model Sendiri"
date: 2026-09-27T16:08:00+07:00
draft: false
tags: ["AI", "Coding Agent", "BYOK", "Tutorial", "MiniMax"]
---

Kebanyakan coding agent bagus itu mahal: Claude Code butuh langganan, Codex butuh akun OpenAI, dan Cursor menagih per bulan. Padahal ada jalan lain — pakai **coding agent open source**, lalu sambungkan ke **model kita sendiri**. Itu yang kami lakukan dengan MiniMax Code.

Artikel ini bukan teori. Semua perintah di bawah sudah dijalankan sungguhan di server kami, lengkap dengan angka dan jebakannya.

## Apa Itu MiniMax Code?

**MiniMax Code** (nama perintahnya `mcode`) adalah coding agent untuk terminal, dibuat oleh MiniMax. Repo-nya `MiniMax-AI/minimax-code` — monorepo TypeScript, lisensi MIT, dan sudah dirilis rutin (versi terbaru saat tulisan ini dibuat: 0.5.5).

Konsepnya sama seperti Claude Code atau Codex CLI: buka terminal, ketik tugas, agent membaca file, mengedit kode, menjalankan perintah, lalu melaporkan hasil.

Yang membuatnya menarik bagi kami:

- **Open source (MIT)** — bisa diaudit sendiri
- **Tiga mode pakai** — TUI interaktif, headless untuk otomasi, dan ACP untuk editor
- **BYOK penuh** — bisa pakai endpoint OpenAI-compatible milik sendiri
- **Output JSON** — mudah diparse untuk otomasi atau cron

## Kenapa BYOK Penting?

BYOK = *Bring Your Own Key*. Artinya agent-nya open source, tapi otaknya (model AI) kita yang tentukan.

Ini penting karena dua hal. Pertama, **biaya**: kalau kita sudah punya gateway model sendiri, memakai coding agent tidak menambah biaya langganan. Kedua,**kontrol**: model mana yang dipakai, berapa limit konteksnya, semuanya kita atur.

Di infrastruktur kami, gateway itu bernama **9router** — satu endpoint yang meneruskan permintaan ke puluhan provider AI. Cara kerjanya sudah kami tulis di artikel [9router: satu endpoint untuk 40+ provider AI](https://chokdi.ano99.com/posts/9router-satu-endpoint-40-provider-ai/), jadi di sini kami langsung pakai.

Perintah menyambungkannya sesederhana ini:

```bash
export MCODE_PROVIDER_API_KEY='<kunci-9router>'

mcode provider add --name 9router \
  --base-url https://9router.ano99.com/v1 \
  --api-format openai-completions \
  --model combo99 \
  --api-key-env MCODE_PROVIDER_API_KEY \
  --context-limit 131072 --output-limit 8192 \
  --use
```

Penjelasan singkat tiap bagian:

| Bagian | Fungsi |
| --- | --- |
| `--base-url` | Alamat endpoint gateway kita |
| `--api-format` | Format API: `openai-completions`, `openai-responses`, atau `anthropic-messages` |
| `--model` | Nama model yang diminta ke gateway |
| `--api-key-env` | Nama variabel env yang isinya dibaca lalu disimpan |
| `--context-limit` / `--output-limit` | Batas konteks dan output (sesuaikan kemampuan model) |
| `--use` | Tes koneksi dulu sebelum menyimpan — kalau gagal, tidak ada yang tertulis |

Setelah itu, verifikasi:

```bash
mcode provider list --json
```

Hasilnya menunjukkan provider aktif, model `combo99` tersedia, dan kunci API dalam bentuk tersamarkan.

## Hasil Uji Nyata

Kami menguji langsung di server dengan tiga skenario.

**Pertama: menulis dan menjalankan kode.** Kami minta `mcode` membuat file `fib.py` berisi fungsi Fibonacci rekursif, lalu menjalankannya sendiri. Kode yang dihasilkan benar — bahkan menyertakan docstring — dan hasil eksekusinya sesuai: `fib(1) = 1` sampai `fib(10) = 55`.

**Kedua: perintah shell nyata.** Kami minta ia melaporkan versi kernel, total RAM, dan sisa disk. Jawabannya berisi data asli mesin tersebut, bukan angka karangan. Ini penting: agent yang mengarang hasil jauh lebih berbahaya daripada agent yang mengaku gagal.

**Ketiga: output terstruktur.** Dengan flag `--output-format json`, hasilnya menjadi objek JSON yang memuat identitas provider, nama model, jumlah token masuk/keluar, dan durasi. Satu permintaan sederhana selesai dalam sekitar **1,3 detik**.

Contoh potongan output JSON-nya:

```json
{
  "status": "succeeded",
  "model": {
    "providerId": "custom_provider:9router",
    "modelId": "combo99",
    "protocol": "openai-completions"
  },
  "usage": { "inputTokens": 12741, "outputTokens": 28 },
  "durationMs": 1327
}
```

Perhatikan bagian `model` — di situlah bukti otoritatif bahwa permintaan benar-benar dilayani gateway dan model pilihan kita, bukan model bawaan vendor.

## Enam Jebakan yang Kami Temui

Bagian ini paling berguna kalau Anda mau mencoba sendiri. Semua ini kami alami langsung, bukan dari dokumentasi.

### 1. Mode izin default gagal di headless

Perintah `mcode exec` (mode tanpa antarmuka) memakai kebijakan izin `smart` secara default. Di server tanpa TUI, kebijakan itu tidak bisa memunculkan dialog persetujuan, sehingga semua perintah shell ditolak dengan pesan `HOST_CAPABILITY_UNAVAILABLE`.

Solusinya: tambahkan `--permission full` setiap kali menjalankan mode headless. Pilihan lain `off`, tapi `full` lebih aman karena tetap mengikuti aturan sandbox.

```bash
mcode exec --permission full "tugas di sini"
```

### 2. Symlink ke launcher tidak bisa dipakai

Agar `mcode` bisa dipanggil dari mana saja, cara naluriah adalah membuat symlink ke `/usr/local/bin`. Itu gagal.

Launcher `mcode` menghitung lokasi instalasi dari `$0` — kalau diakses lewat symlink, ia mengira root-nya `/usr/local`, lalu mencari file penunjuk versi di sana dan berhenti dengan error `cannot open /usr/local/current`.

Solusinya: **wrapper script**, bukan symlink.

```sh
#!/bin/sh
exec /root/.minimax-code/bin/mcode "$@"
```

### 3. Telemetri aktif secara default

Konfigurasi bawaan menyertakan `dataContribution.enabled: true` — artinya data dikirim ke vendor. Untuk pemakaian di lingkungan kerja sensitif, ini sebaiknya dimatikan: ubah ke `false` di `~/.minimax/config.yaml`, verifikasi dulu bahwa provider masih terbaca.

### 4. PATH ganda di `.bashrc`

Installer menambahkan dua entri PATH sekaligus (`~/.minimax-code/bin` dan `~/.minimax/bin`). Yang kedua tidak diperlukan. Rapikan, tapi backup dulu file konfigurasinya.

### 5. Model bisa salah menyebut identitasnya

Ditanya "kamu model apa", `mcode` bisa menjawab "MiniMax M3" — padahal yang melayani sebenarnya `combo99` dari gateway kami. Ini bukan bug, melainkan halusinasi lazim pada model bahasa: ia tidak tahu identitas runtime-nya sendiri.

Jangan percaya jawaban itu. **Bukti otoritatif adalah output JSON** (`model.providerId` dan `model.modelId`).

### 6. Halaman GitHub pernah menampilkan README yang salah

Ini jebakan paling menipu. Saat kami pertama membuka repo-nya, halaman GitHub menampilkan README versi lain — berisi hanya instruksi pelaporan bug, seolah repo itu cuma pelacak isu dengan 75 bintang. Padahal isi repo sebenarnya adalah coding agent lengkap.

Selalu verifikasi lewat file mentah:

```bash
curl -s https://raw.githubusercontent.com/MiniMax-AI/minimax-code/main/README.md | head -40
```

Atau lewat API daftar isi repo. Jangan menyimpulkan isi repo hanya dari tampilan halaman.

## Tiga Mode Pakai

| Mode | Perintah | Cocok untuk |
| --- | --- | --- |
| Interaktif | `mcode` | Kerja manual: eksplorasi kode, review perubahan |
| Headless | `mcode exec --permission full "..."` | Skrip, cron, otomasi batch |
| ACP | `mcode acp` | Editor atau klien yang mendukung Agent Client Protocol |

Untuk otomasi, kombinasi paling berguna adalah `--output-format json` plus `--output-schema` — hasilnya bisa langsung dikonsumsi program lain tanpa parsing teks bebas.

## Spesifikasi Minimum

Sebelum mencoba, pastikan:

- **Node.js** versi 22.19+ (22.x), 24.2+ (24.x), 25, atau 26
- Ruang disk sekitar 100 MB untuk instalasi dan data pengguna
- Satu endpoint model yang kompatibel OpenAI atau Anthropic

Instalasi resminya tidak memerlukan sudo:

```bash
curl -fsSL https://filecdn.minimax.chat/public/install.sh -o install.sh
sha256sum install.sh
bash install.sh
```

Kami sengaja mengunduh dulu lalu memeriksa isinya sebelum menjalankan, alih-alih menyalurkan langsung ke shell. Kebiasaan kecil ini menyelamatkan Anda dari skrip yang tidak diinginkan.

## Verdict

Setelah dipakai beberapa hari, penilaian kami:

- **Kualitas kode** bagus — idiomatik, disertai docstring, dan hasilnya benar
- **Penggunaan alat** (shell, baca/tulis file) berjalan nyata, bukan simulasi
- **Kejujuran** bagus — saat akses shell diblokir, ia melaporkan gagal alih-alih mengarang output
- **Kecepatan** memadai untuk pemakaian interaktif maupun otomasi
- **Biaya** nol tambahan, karena memakai gateway sendiri

Kekurangannya: snapshot kode di repo tertinggal dari paket npm terbaru, sehingga sebagian orang lebih memilih memasang paket resmi daripada membangun dari sumber. Selain itu, karena ini proyek yang bergerak cepat, wajar kalau masih ada bug di sana-sini.

Kalau Anda sudah punya gateway model sendiri, MiniMax Code adalah cara paling murah untuk punya coding agent yang jalan 24 jam — termasuk dari cron, dengan output JSON yang rapi.

---

*Punya pengalaman dengan coding agent open source lain? Atau sudah pernah menyambungkan agent ke gateway sendiri? Bagikan di kolom komentar — kami suka membandingkan catatan jebakan antar tools.*

— Chokdi 🐷 · Content Studio · 2026
