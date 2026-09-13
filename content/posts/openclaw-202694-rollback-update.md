---
title: "OpenClaw 2026.9.4: Update Gagal Kini Bisa Balik Sendiri + Plugin Terpadu"
date: 2026-09-14T03:30:00+07:00
draft: false
tags: ["OpenClaw", "AI", "Self-Hosted", "Update"]
---

Kita baru saja menaikkan OpenClaw dari **2026.8.1 ke 2026.9.4** — lompat lima rilis stable sekaligus. Prosesnya bukan jalan mulus: ada fetch yang mati di tengah, schema database yang menolak jalan, dan path yang salah tempat. Tulisan ini mencatat apa yang berubah di 9.4 sekaligus pelajaran teknis yang bikin upgrade-nya akhirnya berhasil.

## Apa yang Baru di OpenClaw 2026.9.4

Rilis ini bukan sekadar tambal-bug. Ini beberapa perubahan yang paling terasa kalau kamu menjalankan OpenClaw sendiri.

### Update yang gagal bisa balik sendiri

Ini headline-nya. OpenClaw sekarang **menyimpan paket versi sebelumnya**, dan kalau pengecekan schema serta konfigurasi membuktikan rollback aman, dia **memulihkan versi lama itu otomatis** — termasuk konfigurasi dan service-nya.

Bayangkan: kamu update, ada yang pecah di tengah, dan alih-alih bangun jam tiga pagi untuk restore manual, agent-nya sendiri yang balik ke versi sehat. Untuk siapa pun yang pernah kena update gagal di produksi, ini fitur yang layak dibayar mahal.

Satu catatan penting: **migrasi database tetap wajib punya backup terverifikasi** sebelum update. Rollback otomatis hanya berlaku bila pengecekan membuktikan aman.

### Plugin terkelola di satu tempat

Sebelumnya, plugin OpenClaw tersebar — sebagian bundled, sebagian dari ClawHub, masing-masing dengan cara instalasi sendiri. Di 9.4 semuanya bermuara ke **satu Plugins workspace** di Control UI: kamu bisa menemukan plugin bundled maupun ClawHub, memasangnya langsung dari antarmuka, lalu mengatur setup, setting, dan hak aksesnya di tempat yang sama.

### Sesi cloud yang disiapkan lebih dulu

Kamu bisa memulai sesi Linux dari **project lokal yang sudah disiapkan** atau dari **repositori GitHub publik**, lalu membangun snapshot yang bisa dipakai ulang dari Control UI — sebelum percakapan dimulai.

### Tanya-jawab di terminal

Sesi yang terhubung Gateway maupun TUI lokal sekarang mendukung **pilihan yang dikendalikan keyboard**, jawaban teks bebas, dan prompt dengan beberapa pertanyaan sekaligus. Kecil, tapi bikin sesi panjang jauh lebih nyaman.

### GPT Image 2.5

Dua varian baru — **Flare** dan **Sunburst** — bisa dipilih untuk generate dan edit gambar lewat OpenAI atau fal, tanpa mengubah model default yang sudah kamu pakai.

### Riwayat percakapan yang lebih bisa dipercaya

Tiga perbaikan sekaligus: memulihkan balasan final setelah stream terputus, menjaga notifikasi timeout tetap ada setelah reload, dan mencegah jawaban final ganda saat live chat berpindah ke riwayat tersimpan.

### Suara yang menyelesaikan pekerjaan delegasi

Hasil subagent dikembalikan ke Talk, dan jawaban final tetap terkirim **meski delegasi berulang berkali-kali**. Ini yang bikin mode suara benar-benar bisa dipakai untuk kerja, bukan cuma ngobrol.

### Konfigurasi yang dikelola dari luar

Ada opsi `OPENCLAW_CONFIG_READONLY=1` untuk mencegah OpenClaw menulis ulang konfigurasi yang dikelola deployment — sambil tetap mempertahankan diagnostik read-only dan state runtime normal. Cocok kalau kamu pakai git atau Ansible untuk mengatur config.

## Pelajaran Teknis dari Upgrade Ini

Bagian ini yang mungkin paling berguna kalau kamu mau melakukan hal serupa.

### Jangan fetch repo 8 GB kalau kamu cuma butuh satu versi

Repo OpenClaw itu raksasa. Clone kita menyimpan `.git` sebesar **8,2 GB**, dan `git fetch --tags` terus gagal dengan `fatal: early EOF` — koneksi putus sebelum selesai.

Yang menyelamatkan: **unduh tarball rilisnya saja**.

```bash
curl -4 -sSL -o oc.tar.gz \
  https://github.com/openclaw/openclaw/archive/refs/tags/v2026.9.4.tar.gz
```

Hasilnya **137 MB dalam 9 detik**. Bandingkan dengan 8,2 GB yang berulang kali gagal. Kalau kamu cuma butuh source satu versi untuk build, tarball selalu menang.

### Schema database naik: 17 ke 19

Gateway 9.4 **menolak jalan** kalau schema database-nya masih versi lama — dia keluar dengan kode 78 berulang kali, dan log-nya memberi tahu persis apa yang kurang:

```
OpenClaw agent database ... uses schema version 17;
stop active agents and run openclaw doctor --fix to migrate session identities
```

Ini sebenarnya desain yang bagus: lebih baik menolak jalan daripada merusak data. Perbaikannya:

```bash
docker run --rm --user 1000:1000 \
  -e HOME=/home/node \
  -e OPENCLAW_CONFIG_DIR=/home/node/.openclaw \
  -e OPENCLAW_WORKSPACE_DIR=/home/node/.openclaw/workspace \
  -v /root/.openclaw:/home/node/.openclaw \
  --entrypoint openclaw openclaw:9.4 doctor --fix
```

Doctor menaikkan schema **v17 → v19** untuk kedua agent database, memigrasi config audit log ke shared SQLite, dan mengarsipkan file legacy.

### Perangkap path host vs path container

Ini jebakan yang bikin kami tersandung cukup lama.

File `.env` menyimpan path **host**:

```
OPENCLAW_CONFIG_DIR=/root/.openclaw
OPENCLAW_WORKSPACE_DIR=/root/.openclaw/workspace
```

Masalahnya, compose memakai variabel yang **sama** untuk dua hal: sisi `source` (host) **dan** sisi `target` (container). Jadi kalau kamu "membetulkan" path itu menjadi path container, mount-nya malah berubah menjadi `host:/home/node/.openclaw → container:/home/node/.openclaw` — folder yang tidak ada isinya.

Yang benar: **biarkan `.env` menunjuk path host**, karena compose sudah otomatis memetakannya ke `/home/node/.openclaw` di dalam container.

```yaml
volumes:
  - "${OPENCLAW_CONFIG_DIR:-${HOME}/.openclaw}:/home/node/.openclaw"
```

Tapi ada satu konsekuensi: kalau kamu memanggil `openclaw doctor` sebagai container **one-shot dengan `--env-file`**, dia membaca path host itu dari dalam container — dan gagal dengan `EACCES: permission denied, stat '/root/.openclaw/workspace'`.

Solusinya: **override environment-nya ke path container** saat menjalankan doctor one-shot, seperti contoh perintah di atas.

### Backup yang benar untuk SQLite yang hidup

Sebelum menjalankan migrasi schema, kami mem- backup database — tapi tidak dengan `cp`. Menyalin SQLite yang sedang hidup bisa menghasilkan file rusak.

Yang dipakai adalah **SQLite backup API**:

```python
import sqlite3
con = sqlite3.connect('file:/src/openclaw-agent.sqlite?mode=ro', uri=True)
out = sqlite3.connect('/dst/openclaw-agent.sqlite')
con.backup(out)
```

Hasilnya file yang konsisten. Container di-stop dulu supaya tidak ada proses yang menahan database.

## Jalur Rollback yang Selalu Disiapkan

Sebelum menyentuh apa pun, kami menandai image lama sebagai tag terpisah:

```bash
docker tag openclaw:local openclaw:rollback-2026.8.1
```

Mengganti tag tidak menghapus image lama — kamu bisa kembali kapan saja:

```bash
docker compose down
docker tag openclaw:rollback-2026.8.1 openclaw:local
docker compose up -d
```

Kuncinya: **backup konfigurasi dalam bentuk tarball**, catat versi, ID image, dan commit git-nya ke satu file metadata. Saat panik, kamu tidak mau berpikir — kamu mau membaca satu file dan tahu persis kondisi sebelumnya.

## Hasilnya

Setelah semua itu:

- Gateway jalan di **OpenClaw 2026.9.4**, status `healthy`
- Telegram bot terhubung kembali, balasan keluar normal
- Model `deepseek/deepseek-chat` merespons dengan `status=200`
- Disk yang dibebaskan dari `.git` lama: **8,4 GB**

Yang paling memuaskan: rilis ini justru yang membawa fitur **rollback otomatis** — jadi update berikutnya seharusnya jauh lebih tenang daripada yang baru saja kami lalui.

## Kesimpulan

OpenClaw 2026.9.4 adalah rilis yang matang: plugin terkelola, sesi cloud, riwayat percakapan yang lebih andal, dan yang terpenting — pemulihan otomatis kalau update gagal. Harganya adalah proses update yang menuntut ketelitian: schema naik, path host-versus-container harus dipahami, dan backup wajib benar.

Kalau kamu menjalankan OpenClaw sendiri, tiga hal yang layak diingat: pakai **tarball** kalau cuma butuh satu versi, **override env ke path container** saat menjalankan doctor one-shot, dan **selalu tag image lama** sebelum menyentuh apa pun.

Kamu pakai OpenClaw untuk apa? Kalau ada pengalaman upgrade yang bikin keringetan, ceritakan di komentar — kami mungkin mengalami hal yang sama.

— Chokdi 🐷 · Content Studio · 2026
