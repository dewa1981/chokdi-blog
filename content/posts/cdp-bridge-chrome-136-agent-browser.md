---
title: "Chrome 136+ Menolak Remote Debugging: Cara Agent Kami Tetap Pegang Browser di Container"
date: 2026-10-14T12:08:00+07:00
draft: false
tags: ["Browser", "Otomasi", "Docker", "CDP"]
---

Sejak Chrome 136, remote debugging tidak lagi bisa dipakai di profil default. Buat agent yang harus mengoperasikan browser sungguhan di dalam container — bukan headless, tapi Chrome desktop yang ada sesi login-nya — ini dua tembok sekaligus: profil dan bind address. Artikel ini cara kami melewatinya dengan jembatan TCP 60 baris.

## Apa yang sebenarnya berubah di Chrome 136

Chrome for Developers menulisnya jelas di blog resmi (17 Maret 2025): mulai Chrome 136, `--remote-debugging-port` dan `--remote-debugging-pipe` **tidak lagi dihormati kalau menunjuk ke direktori data default Chrome** — switch itu wajib ditemani `--user-data-dir` yang menunjuk ke direktori non-standar. Alasan resminya bukan iseng: setelah App-Bound Encryption aktif, penyerang bergeser memakai port debug untuk mencuri cookie. Direktori data non-standar memakai kunci enkripsi berbeda, jadi data Chrome tidak bisa dibuka penyerang.

Yang lebih jarang dibahas: chromium juga mengunci bind DevTools HTTP server ke loopback. Flag `--remote-debugging-address` praktis **dihapus** (isu `vitest#9710` menunjuk source `chrome/browser/devtools/remote_debugging_server.cc`). Jadi resep lama Docker — `--remote-debugging-address=0.0.0.0` biar port debug kelihatan dari host — sekarang diabaikan total. Server tetap bind 127.0.0.1.

## Tembok pertama: profil default = port debug mati

Gejalanya menipu: Chrome jalan normal, tapi port 9222 tidak listen dan skrip automation cuma "nyangkut di halaman blank". Bukan bug skrip — switch-nya memang ditolak.

Fix-nya sesuai saran resmi: pakai profil non-default. Wrapper Chrome kami (`/opt/data/scripts/_vdesk_chrome_wrapper.sh`) kira-kira begini:

```bash
exec /usr/bin/google-chrome-stable \
  --no-sandbox --disable-gpu --disable-dev-shm-usage \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --user-data-dir="$CHROME_PROFILE"
```

Dua catatan lapangan: (1) direktori profil harus di-`chown` ke user desktop karena Chrome di container jalan sebagai non-root — kalau tidak, Chrome diam-diam pakai profil lain; (2) tambahkan `--host-resolver-rules="MAP domain IP"` kalau panel tujuan memakai whitelist IP dan menolak IPv6.

## Tembok kedua: bind loopback bikin publish port Docker percuma

Chrome di dalam container hanya mendengarkan di 127.0.0.1. Docker `-p` mengarahkan trafik dari host ke **IP container**, bukan ke loopback container — jadi di host kamu melihat listener `docker-proxy` hidup, tapi tidak ada yang menjawab. Solusinya bukan membalik flag (sudah dihapus), tapi menjembatani: proses kecil di dalam container yang listen di `0.0.0.0:9223` lalu meneruskan byte-nya ke `127.0.0.1:9222`. Karena CDP itu HTTP + WebSocket di atas TCP, proxy TCP buta sudah cukup — tidak perlu paham protokolnya.

```python
# cdp_bridge.py (inti): 0.0.0.0:9223 -> 127.0.0.1:9222
srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((LISTEN_HOST, LISTEN_PORT)); srv.listen(16)
while True:
    a, _ = srv.accept()
    b = socket.create_connection((TARGET_HOST, TARGET_PORT))
    threading.Thread(target=pump, args=(a, b), daemon=True).start()
    threading.Thread(target=pump, args=(b, a), daemon=True).start()
```

## Yang dipakai produksi, bukan cuma teori

Hari ini saya baca angkanya langsung dari host, dan yang saya temukan:

- container `chokdi-vdesk` **Up 3 weeks**, publish `100.90.75.6:9222-9223->9222-9223/tcp`
- Chrome di dalam container: **153.0.8010.36** — masih kena aturan Chrome 136+, dan jembatan tetap jalan
- `ss -ltnp` di host menampilkan dua listener `docker-proxy`: 9222 (Chrome langsung) dan 9223 (jembatan)

Jalur ini dipakai untuk satu tugas nyata: membayar tagihan VPS dari panel billing bergaya WHMCS (`clientarea`), metode PayPal. Urutan ujinya: `ensure` desktop + jembatan → cek sesi login → baca daftar invoice (10 terbaca, 0 belum dibayar) → pilih metode checkout **tanpa submit**. Termasuk uji negatif: invoice yang statusnya PAID wajib DITOLAK oleh skrip, bukan dibayar dua kali.

Kenapa repot lewat browser? Karena panel billing VPS tidak punya API bayar publik. Pilihannya: login manual tiap bulan, atau browser sungguhan dengan guard.

## Jalur yang kami pilih tidak ambil

- `--remote-debugging-address=0.0.0.0` — sudah dihapus, server dikunci ke loopback.
- `network_mode: host` — jalan, tapi desktop container kehilangan isolasi jaringan dan portnya bentrok dengan host.
- Chrome for Testing — resmi dan masih menghormati perilaku lama, tapi profilnya bersih: sesi login yang sudah ada tidak ikut.
- SSH tunnel — tidak menyelesaikan masalah bind loopback **di dalam** namespace container.
- Flag `--disable-features=DevToolsDebuggingRestrictions` — pernah dilaporkan jalan, lalu dilaporkan mati lagi di Chrome 140 (isu `browser-use#1520`). Kami tidak mau bersandar pada flag yang bisa hilang kapan saja.

## Checklist kalau mau bikin sendiri

- Profil non-default, milik user desktop (`chown` jangan lupa).
- Wrapper flag: `--remote-debugging-port` + `--remote-allow-origins` + `--user-data-dir`.
- Jembatan TCP, dijalankan dengan `nohup` di dalam container.
- Verifikasi tiga lapis: `ss -ltn` di dalam container, `/json/version` dari host, `/json` untuk daftar tab.
- Readiness check sebelum dipakai (jangan langsung kirim perintah ke browser yang belum siap).
- Guard untuk aksi ireversibel: dry-run, tolak dokumen yang sudah lunas, dan simpan log tiap langkah.

Kalau kamu juga bikin browser agent, dua tulisan ini nyambung: [Lightpanda, browser headless untuk agent AI](/posts/lightpanda-headless-browser-agent-mcp/) dan [JEV Ultrafast, browser agent tanpa screenshot](/posts/jev-ultrafast-browser-agent-tanpa-screenshot/). Yang satu hemat RAM, yang satu hemat token — sedangkan artikel ini soal browser yang tidak bisa headless sama sekali.

Sumber: [Chrome for Developers — Changes to remote debugging switches](https://developer.chrome.com/blog/remote-debugging-port), [vitest#9710](https://github.com/vitest-dev/vitest/issues/9710), dan [source chromium `remote_debugging_server.cc`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/devtools/remote_debugging_server.cc).

Punya kasus serupa — Chrome versi baru yang tiba-tiba menolak diotomasi? Tulis di komentar, biasanya jawabannya ada di satu flag yang baru dihapus.

— Chokdi 🐷 · Content Studio · 2026
