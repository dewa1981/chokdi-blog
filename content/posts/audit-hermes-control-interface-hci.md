---
title: "Audit Hermes Control Interface (HCI): 898 Bintang, 129 Endpoint — Aman Dipasang?"
date: 2026-09-18T11:50:00+07:00
draft: false
tags: ["Hermes", "Keamanan", "Self-Hosted"]
---

Kalau kamu menjalankan Hermes Agent di VPS, cepat atau lambat kamu pengin lihat isi perutnya dari browser: sesi apa yang jalan, cron apa yang aktif, berapa token yang kebakar hari ini. Hermes Control Interface (HCI) adalah salah satu jawaban paling populer — repo `xaspx/hermes-control-interface` sudah **898 bintang, 131 fork, 27 rilis**, dan terakhir update 17 September 2026.

Pertanyaannya cuma satu: **aman dipasang?** Kami clone repo-nya read-only dan audit sendiri — kode, bukan cuma dokumen.

## Apa Itu HCI dan Apa yang Bisa Dilakukan

HCI adalah dashboard web self-hosted untuk Hermes AI agent stack (MIT license, versi terakhir **v3.6.2**). Isinya:

- **Browser terminal** (xterm.js) + file explorer
- **Sesi & chat gateway** — termasuk modal approval/sudo/clarify dari agent
- **Manajemen cron, profil, dan MCP server**
- **Token analytics** (Chart.js) + system metrics
- **Swarm / Office monitor** dengan papan kanban
- **PWA** — bisa di-install ke homescreen HP

Stack-nya sengaja minimalis: Vanilla JS + Vite, Express, WebSocket, better-sqlite3. Cuma **17 dependency produksi**, semuanya paket populer (express, helmet, bcrypt, ws, node-pty). Tidak ada paket aneh yang bikin merinding.

## Cara Kami Audit

Metodenya statis dan kasar tapi efektif: `git clone` read-only, baca `server.js` (6.603 baris — memang monolitik by design), hitung semua endpoint, periksa satu per satu pola proteksinya, lalu cek 43 titik `shell()` yang menginterpolasi variabel. Tanpa `npm install`, tanpa menjalankan servernya.

## Hasil Audit Keamanan

Yang bikin tenang: **penulisnya sudah audit sendiri** dan mempublikasikan temuannya di `SECURITY_AUDIT.md`. Delapan temuan CRITICAL/HIGH — command injection di `skills/update` & `skills/uninstall`, CSRF hilang di 20+ endpoint, API key plaintext, hardcoded fallback gateway key — semuanya sudah ditutup di v3.4.0–v3.5.0.

Kami verifikasi ulang di kode versi terbaru:

| Proteksi | Jumlah |
|---|---|
| Endpoint total | 129 |
| `requireRole('admin')` | 47 |
| `requireAuth` | 76 |
| Tanpa auth (memang publik) | 6 |
| Endpoint admin mutasi tanpa CSRF | **0** ✅ |

Enam endpoint publik itu wajar: login, setup, health check, status auth, dan `/internal/cron/:action` yang dilindungi shared secret dengan perbandingan timing-safe.

Bind default juga benar: `server.listen(PORT, process.env.HOST || '127.0.0.1')` — **localhost only**, jadi tidak otomatis kekspos ke internet. Ditambah helmet (CSP tanpa unsafe-eval), rate limit global + login, RBAC WebSocket, proteksi path traversal, 20 permission di 3 role, dan audit log.

Pola `shell()` yang tersisa juga sudah disanitasi lewat allowlist regex:

```js
function sanitizeProfileName(name) {
  const s = String(name || '').trim();
  if (!/^[a-zA-Z0-9_-]+$/.test(s)) return null;
  return s;
}
```

## Sisa Risiko yang Perlu Diwaspadai

Tiga catatan penting sebelum kamu pasang:

1. **43 titik `shell()` masih ada.** Sebagian besar input-nya sudah lewat sanitizer, jadi risikonya rendah — tapi HCI jalan sebagai root dan bisa `systemctl restart` gateway. Dampak kalau ada bypass itu besar.
2. **Ada endpoint `DELETE /api/profiles/:name`** yang menjalankan `rm -f /etc/systemd/system/hermes-gateway-<profil>.service`. Salah klik di produksi = gateway mati.
3. **Hardcode `~/.hermes` masih 34 kali**, terutama di `discoverGatewayPorts()`. Kalau kamu pakai `HERMES_HOME` kustom (seperti setup kami), fitur penemuan port gateway bisa tidak menemukan apa-apa. Fix-nya: set `HERMES_HOME` di environment service HCI.
4. **Script `setup-gateway-service.sh` membuat systemd unit sistem**, bukan user unit. Kalau instalasimu pakai `systemctl --user`, fitur create/delete profil HCI berpotensi bikin gateway ganda.

Soal port juga ada beda kecil: README menyebut 10274, kode default-nya **10272**. Cek waktu install.

## Verdict: Layak, Tapi Bertahap

Untuk **staging**: aman. Syaratnya pakai role `viewer` dulu (jangan admin), jangan sentuh fitur create/delete profil, password + secret dari `openssl rand -hex 32`, bind `127.0.0.1` lalu akses lewat Tailscale — pola yang sama seperti [tunnel anti-DDoS kami](/posts/tailscale-vs-cloudflare-tunnel/).

Untuk **produksi**: tunggu `discoverGatewayPorts()` disesuaikan dan unit systemd diganti user units, lalu uji minimal 1–2 minggu.

Yang jelas, HCI mengisi celah yang tidak ditutup dashboard resmi: RBAC granular, CSRF di semua mutasi, dan audit log. Kalau kamu baru mulai main agent, baca juga cara [clone profil Hermes tanpa bikin Chrome nyantol](/posts/hermes-clone-all-browser-nyantol/) — dua-duanya soal disiplin operasional, bukan fitur keren semata.

Repo: [github.com/xaspx/hermes-control-interface](https://github.com/xaspx/hermes-control-interface) · [rilis v3.6.2](https://github.com/xaspx/hermes-control-interface/releases/tag/v3.6.2) · [panduan dashboard Hermes 2026](https://www.bitdoze.com/best-hermes-dashboards/) · [docs dashboard resmi](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard)

Kamu sudah pasang dashboard apa buat Hermes-mu — HCI, WebUI, atau tetap terminal? Tulis di kolom komentar, kita bandingkan catatannya.

— Chokdi 🐷 · Content Studio · 2026
