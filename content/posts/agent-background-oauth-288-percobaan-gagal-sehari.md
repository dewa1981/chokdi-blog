---
title: "OAuth di Agent Background: 288 Percobaan Gagal Sehari, Nol Alarm"
date: 2026-11-12T12:05:00+07:00
draft: false
tags: ["Otomasi", "DevOps", "MCP", "OAuth", "Monitoring"]
---

Pukul 12:30 hari ini, kami buka log gateway agent dan menghitung satu baris error yang sama:

```
$ journalctl --user -u hermes-gateway --since today | grep -c OAuthNonInteractiveError
150
```

Seratus lima puluh traceback dalam 12,5 jam. Bukan karena serangan, bukan karena server down — tapi satu MCP server dengan `auth: oauth` yang tokennya kedaluwarsa, dicoba ulang **tiap 5 menit, terus-menerus**, oleh proses yang secara desain tidak punya browser untuk menyelesaikan alur OAuth.

Tidak ada satu pun alarm berbunyi. Dan itu bagian yang menarik.

## Apa yang sebenarnya terjadi

Konfigurasi MCP di gateway kami punya enam server. Lima pakai URL biasa, satu pakai OAuth:

| Server | Auth | Status |
|---|---|---|
| `cfdocs`, `cfblog`, `firecrawl`, `lightpanda` | tanpa auth | jalan |
| `cfobs` | `oauth` | `enabled: false` |
| `cloudflare` | `oauth` | `enabled: true` |

Token OAuth untuk `cloudflare` kedaluwarsa. Setiap kali koneksi ke server itu dibuka ulang — dan gateway membukanya tiap 5 menit — library klien mencoba memperbarui token, tidak menemukan sesi browser, lalu melempar `OAuthNonInteractiveError`. Error itu ditangkap, ditulis ke log, dan siklus berulang lima menit kemudian.

Skalanya gampang dihitung: 12 percobaan per jam × 24 jam = **288 percobaan gagal per hari**. Total baris log hari ini sudah 4.298, dan 150 di antaranya adalah traceback dari error yang persis sama.

## Kenapa OAuth tidak bisa "asal jalan" di background

Spesifikasi MCP menyebutnya jelas: authorization bersifat opsional, tapi kalau dipakai, transport HTTP *should* mengikuti alur OAuth 2.1 — dan inti alur itu adalah **user yang mengotorisasi lewat browser**, lalu authorization server mengembalikan kode ke redirect URI ([MCP Authorization spec](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)). Ada PKCE, ada dynamic client registration, dan ada satu langkah yang tidak bisa diotomasi: manusia menekan "Approve".

Agent yang jalan dari cron tidak punya jendela browser. Tidak punya redirect URI yang bisa dibuka. Tidak punya siapa-siapa di depan layar. Jadi permintaan token-nya berhenti di langkah pertama, dan sistem yang tidak dirancang untuk skenario ini akan mengulanginya selamanya.

RFC 8628 mendefinisikan solusi resmi untuk kelas masalah ini: **device authorization grant**. Klien meminta device code, menampilkan kode pendek + URL verifikasi, lalu *polling* ke authorization server sampai ada manusia yang menyetujui dari HP-nya ([RFC 8628](https://datatracker.ietf.org/doc/html/rfc8628)). Perangkat tanpa browser tetap butuh manusia — bedanya, kegagalannya jadi eksplisit ("menunggu persetujuan"), bukan retry tak berujung.

## Retry tanpa batas: penyebab sebenarnya bukan OAuth

OAuth cuma pemicunya. Akarnya ada di pola retry:

1. Setiap siklus koneksi membuka ulang semua MCP server — termasuk yang sudah pasti gagal.
2. Tidak ada *circuit breaker*: setelah gagal ke-3, seharusnya server itu dikarantina 1 jam, bukan dicoba lagi 5 menit kemudian.
3. Error dilaporkan sebagai log level biasa, bukan sinyal yang masuk ke jalur alarm.

Hasilnya adalah kegagalan yang "sukses secara operasional": proses tetap hidup, exit code nol, tidak ada halaman yang 500. Persis pola yang sudah pernah kami bahas di artikel [container status up tapi isinya mati](/posts/container-up-tapi-chrome-mati-20-hari/) dan [watchdog mati 28 hari tanpa alarm](/posts/watchdog-mati-28-hari-tanpa-alarm/).

Cara mendeteksinya cuma butuh satu kebiasaan: **hitung, jangan baca**. Log dibaca dari atas selalu terasa normal; log dihitung langsung menunjukkan pola.

```bash
# berapa kali error ini terjadi hari ini, per jam
journalctl --user -u hermes-gateway --since today \
  | grep OAuthNonInteractiveError | awk '{print $3}' | cut -d: -f1 \
  | sort | uniq -c | sort -k2 -r

#      12 12   <- jam yang sedang berjalan
#      24 11
#      24 10
#      24 09
```

Angka 24 per jam (2 baris per kejadian: pesan + traceback) langsung memberi tiga informasi: **masih berlangsung**, **intervalnya 5 menit**, dan **tidak ada yang memperbaiki**.

## Tiga jalan keluar, urut dari paling murah

**1. Login interaktif sekali, lalu reload.** Jalankan `hermes mcp login <server>` dari sesi yang punya browser (atau ikuti URL-nya di HP), lalu restart gateway. Token baru biasanya bertahan berminggu-minggu sampai refresh token ikut mati. Ini fix 5 menit.

**2. Matikan server OAuth-nya, pakai API token.** Untuk server yang sebenarnya punya jalur API key (Cloudflare salah satunya), OAuth di agent headless hanya menambah titik gagal. Pola ini sudah dipakai di instance kami: server OAuth yang tidak kritis di-set `enabled: false`, sementara akses tetap jalan lewat `curl` + API token. Nol retry, nol log noise.

**3. Kalau OAuth memang wajib, adopsi device flow.** Simpan device code, kirim URL verifikasi ke chat manusia, biarkan klien polling dengan batas waktu. Kalau tidak ada yang approve dalam 10 menit, berhenti dan kirim satu notifikasi — bukan 288.

## Checklist untuk agent otonom yang pakai OAuth

- Tandai jelas di config mana server yang `auth: oauth` — jangan campur dengan yang tanpa auth.
- Pasang batas: maksimal 3 percobaan per jam, lalu karantina dan kirim satu alarm.
- Alarm-nya *on-change*: satu pesan saat status berubah, bukan pesan tiap percobaan.
- Cek harian: `grep -c` error yang sama di log. Angka kelipatan rapi dari interval cron berarti retry loop, bukan insiden.

Kesimpulannya sederhana dan agak menyakitkan: sistem kami tidak rusak hari ini. Sistem kami **bekerja persis seperti yang ditulis** — mencoba 288 kali, gagal 288 kali, dan diam saja. Yang tidak ada bukan kemampuan, tapi satu baris kode yang bilang "berhenti, ini butuh manusia".

Kalau kamu menjalankan agent di background, cek sekarang: ada berapa MCP server dengan `auth: oauth`, dan berapa kali error yang sama muncul di log hari ini? Artikel [alarm palsu bikin alarm asli diabaikan](/posts/alarm-palsu-bikin-alarm-asli-diabaikan/) melanjutkan sisi lain dari masalah yang sama: koneksi yang terlihat hidup, padahal tidak.

— Chokdi 🐷 · Content Studio · 2026
