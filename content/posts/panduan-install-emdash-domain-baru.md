---
title: "Panduan Install EmDash di Domain Baru (Hemat 3 Jam)"
date: 2026-09-29T21:05:00+07:00
draft: false
tags: ["Cloudflare", "CMS", "Tutorial", "Email", "AI"]
---

**Sudah teruji:** 29 September 2026 — dari nol sampai admin panel bisa dibuka di `emdash.ano99.com`.
**Waktu aktual:** ~3 jam di percobaan pertama; dengan panduan ini target **20–30 menit**.

> Panduan ini ditulis dari pengalaman nyata, termasuk **7 masalah** yang kami temui.
> Empat di antaranya sudah kami selesaikan dengan patch — sisanya cara menghindarinya.

---

## Ringkasan cepat

```bash
# 1. Scaffold
npm create emdash@latest emdash-baru -- --platform cloudflare --template blog --pm pnpm --yes --no-install
cd emdash-baru && pnpm install

# 2. Buat resource Cloudflare (ganti nama!)
npx wrangler d1 create <db>
npx wrangler r2 bucket create <media>
npx wrangler kv namespace create <sessions>

# 3. Isi binding di wrangler.jsonc  → lihat bagian 3

# 4. Set siteUrl di astro.config.mjs → WAJIB, kalau tidak setup produksi gagal
#    siteUrl: "https://<domain-kamu>"

# 5. Deploy
npx wrangler deploy

# 6. Tuntaskan setup (bagian 6) — INI BAGIAN YANG PALING SERING MACET
```

---

## 1. Persiapan yang menentukan

### Node + pnpm

```bash
node -v            # butuh >= 20
npm install -g pnpm
pnpm -v
```

Node hanya dipakai untuk **build & deploy**. Aplikasinya jalan penuh di Cloudflare — tidak ada server Node yang perlu dijaga.

### Pilih domain sejak awal — jangan pakai `*.workers.dev`

Ini keputusan paling penting. Passkey (WebAuthn) **terikat ke domain**:

- Passkey yang didaftarkan di `proyek.xxx.workers.dev` **tidak bisa** dipakai di domain lain.
- Kalau nanti pindah domain, semua pengguna harus **daftar passkey ulang**.

**Jadi:** siapkan domain dulu, deploy pertama langsung ke domain itu.

> Di pekerjaan kami, kesalahan ini memaksa reset setup dan mendaftarkan passkey dua kali.

### Resource Cloudflare

Butuh tiga: **D1** (database), **R2** (media), **KV** (sesi).

```bash
npx wrangler d1 create emdash-db
npx wrangler r2 bucket create emdash-media
npx wrangler kv namespace create emdash-sessions
```

**Untuk instalasi kedua dan seterusnya:** jangan pakai nama yang sama. Nama resource Cloudflare **global dalam satu akun** — `emdash-db` kedua akan ditolak.

---

## 2. Scaffold

```bash
npm create emdash@latest emdash-baru -- \
  --platform cloudflare --template blog --pm pnpm --yes --no-install
cd emdash-baru
pnpm install
```

`--platform cloudflare` memilih target Worker (bukan Node). `--no-install` mempercepat scaffold — dependensi dipasang di langkah berikutnya.

---

## 3. Binding di `wrangler.jsonc`

Tempel ID dari langkah 1. Enam binding yang dibutuhkan:

```jsonc
{
  "d1_databases": [
    { "binding": "DB", "database_name": "<db>", "database_id": "<id-d1>" }
  ],
  "r2_buckets": [
    { "binding": "MEDIA", "bucket_name": "<media>" }
  ],
  "kv_namespaces": [
    { "binding": "SESSIONS", "id": "<id-kv>" }
  ],
  "vars": {
    "SESSION": "<secret-acak-panjang>",
    "IMAGES": "1"
  }
}
```

> `SESSION` = kunci penandatanganan sesi. Buat yang acak dan panjang:
> `openssl rand -hex 32`. Simpan di secrets, bukan di repo publik.

---

## 4. `siteUrl` — jangan dilewatkan

Di `astro.config.mjs`:

```js
export default defineConfig({
  siteUrl: "https://<domain-kamu>",   // ← WAJIB
  // ...
});
```

Tanpa ini, setup produksi gagal dengan peringatan:

```
Set siteUrl or EMDASH_SITE_URL before running production setup
```

Tidak ada masalah di localhost, tapi **gagal di produksi** — jadi jangan baru sadar setelah deploy.

---

## 5. Domain + deploy

Tambahkan custom domain (Cloudflare → Workers → domain kustom), lalu:

```bash
npx wrangler deploy
```

Migrasi database **jalan otomatis** saat deploy pertama (di percobaan kami: 89 migrasi). Verifikasi:

```bash
curl -s -o /dev/null -w "%{http_code}" https://<domain-kamu>/
```

---

## 6. Tuntaskan Setup — bagian yang paling sering macet

Setup **tidak selesai** hanya dengan membuka halaman admin. Ada beberapa langkah, dan kalau satu terlewat, **halaman admin akan terus memantul ke wizard** tanpa pesan yang jelas.

Cek status:

```bash
curl -s https://<domain>/_emdash/api/setup/status
# {"needsSetup":true,...}  ← belum selesai
```

### Yang harus ada sebelum dianggap selesai

Di tabel `options`, **semua ini** harus ada:

| Opsi | Isi |
|---|---|
| `emdash:setup_complete` | `true` |
| `emdash:site_title` | `"Judul Situs"` ← **string JSON yang benar** |
| `emdash:site_tagline` | `"Tagline"` |
| `emdash:setup_state` | kalau ada, **hapus** |

> ⚠️ **Nilai JSON harus benar, bukan ter-escape ganda.** Kalau kamu menulis
> `"\"Judul\""`, penguraian JSON gagal — dan gejalanya **bukan** error di halaman setup,
> tapi **pengiriman email mati total** (`SyntaxError: Unexpected token '\'`).
> Nilai yang benar: `"Judul Situs"` (tanda kutip JSON biasa, tanpa garis miring).

Setelah benar, `/_emdash/admin` harus mengembalikan **HTTP 200**, bukan redirect ke setup.

### Kalau ingin mengisi database langsung

```bash
npx wrangler d1 execute <db> --remote --command "SELECT name FROM options"
```

Buat baris pengguna juga boleh — **tapi perhatikan format kolomnya.** Ini pernah menjebak kami:

- Kolom waktu harus **ISO 8601** (`2026-09-29T10:00:00.000Z`).
  `datetime('now')` SQLite menghasilkan `2026-09-29 10:00:00` — **tidak terbaca** oleh kode.
- Hasilnya: pengguna "ada" di database, tapi fitur login **diam-diam tidak jalan**.

> **Aturan:** kalau menulis baris database manual, bandingkan dengan baris yang **dibuat aplikasi sendiri** — kolom per kolom.

---

## 7. Login tanpa passkey (jalur darurat)

Passkey butuh perangkat yang mendukung. Ada situasi di mana kamu butuh masuk **sebelum** ada passkey sama sekali.

### Token API (paling berguna untuk agent)

```bash
# Buat token + admin lewat CLI
npx emdash whoami
npx emdash content list posts
```

### Login tautan email (magic-link)

Butuh pengiriman email aktif (bagian 8). Kirim ke email yang terdaftar:

```bash
curl -X POST https://<domain>/_emdash/api/auth/magic-link/send \
  -H "Content-Type: application/json" \
  -H "Origin: https://<domain>" \
  -d '{"email":"<email-terdaftar>"}'
```

> ⚠️ **Alamat email harus SAMA PERSIS dengan yang terdaftar.** Kalau dikirim ke alamat lain,
> server akan tetap menjawab `200 {"success":true}` (sengaja, untuk mencegah orang menebak
> siapa saja yang terdaftar) — tapi **tidak ada email yang dikirim**.
>
> Satu-satunya bukti yang jujur: **periksa tabel `auth_tokens`.** Kalau tidak ada baris baru,
> tidak ada yang terkirim.

### Batas percobaan

Endpoint login punya **rate limit 3 kali / 5 menit per IP**. Kalau kena, halaman **tetap** menampilkan error generik ("Something went wrong") — dan otomatis membalas `200`.

```bash
# bersihkan rate limit sebelum uji ulang
npx wrangler d1 execute <db> --remote --command "DELETE FROM _emdash_rate_limits"
```

> Kalau tidak dibersihkan, uji berikutnya gagal **dan terlihat seperti bug yang berbeda**.

---

## 8. Email dari domain sendiri

EmDash bisa mengirim magic-link. Butuh **plugin provider** — bukan sekadar konfigurasi SMTP.

### Kalau aplikasi bilang "EMAIL_NOT_CONFIGURED"

Artinya provider belum terpasang. Pilihannya:

| Cara | Kelebihan | Catatan |
|---|---|---|
| `cloudflareEmail()` | Tanpa API key, gratis | Domain harus di-onboard ke Cloudflare Email |
| `emdash-smtp` | Pakai layanan apa pun (Resend/SES/Mailgun) | Perlu key, tapi paling fleksibel |

Untuk Resend:

```bash
pnpm add emdash-smtp
```

```js
// astro.config.mjs
import emdashSmtp from "emdash-smtp";
export default defineConfig({
  plugins: [emdashSmtp()],
});
```

### Domain: pakai subdomain, jangan root

Pakai **`mail.domainkamu.com`** untuk kirim, dan biarkan root untuk terima.

**Alasannya:** root domain sering sudah punya `MX` (Email Routing/kotak surat). Menaruh
autentikasi pengiriman di sana berisiko bertabrakan. Subdomain memisahkan reputasi kirim
dari alur terima.

Verifikasi **DKIM** dan **SPF** selesai dalam ~3 menit (di pengalaman kami, otomatis).

### Kredensial provider disimpan di DATABASE, bukan di `.env`

Ini bagian yang **paling banyak menghabiskan waktu kami**. Plugin membangun kunci penyimpanan
**berlapis** dari kodenya:

```
ctx.kv.set("settings:global", ...)
  → createKVAccess():  "settings:" dibuang  →  settings.get("global")
  → createSettingsAccess():  prefix = `plugin:<id>:settings:`
  ⇒ kunci nyata di DB: plugin:<id>:settings:global
  ⇒ kunci non-settings: plugin:<id>:<kunci>       (mis. plugin:<id>:state:selectedProviderId)
```

**Tiga jebakan yang menimpa kami:**

1. **Tabel salah.** Ada `_plugin_storage` **dan** `options`. `ctx.kv` menulis ke **`options`** —
   menulis ke `_plugin_storage` **tidak berpengaruh apa pun, tanpa error**.
2. **Nama field pemilih provider salah.** Kode membaca **`primaryProviderId`** *di dalam*
   `settings:global`; `selectedProviderId` hanya status tampilan di admin panel.
3. **Nilai `state:*` disimpan sebagai string mentah** — `resend`, **bukan** `"resend"`.
   Versi ber-tanda-kutip gagal dibaca **secara senyap**.

**Gejala kalau salah:** plugin **jatuh ke transport default** — di Cloudflare Workers itu
`sendmail`, yang gagal dengan:

```
[unenv] child_process.spawn is not implemented yet!
```

> Error itu artinya **provider salah**, **bukan** kredensial salah. Jangan buang waktu
> memeriksa API key.

Kalau provider benar tapi belum ada **from email**:

```
A default from email must be configured before sending
```

→ Isi `fromEmail` + `fromName` di dalam `settings:global`.

### Kalau email masuk folder Spam

Domain baru belum punya reputasi. Tambahkan:

```
_dmarc.mail.<domain>   TXT   "v=DMARC1; p=none; rua=mailto:dmarc@mail.<domain>"
mail.<domain>          TXT   "v=spf1 include:amazonses.com ~all"
```

`p=none` = hanya memantau, tidak memblokir apa pun. Aman untuk tahap awal.
Bangun reputasi dengan: klik **"Bukan spam"** di setiap kiriman, dan **kirim rutin**.

---

## 9. Menerbitkan konten (MCP + CLI)

### MCP

```
POST https://<domain>/_emdash/api/mcp
Authorization: Bearer <token ec_pat_...>
Accept: application/json, text/event-stream
```

> ⚠️ **Header `Accept` itu WAJIB.** Tanpa `text/event-stream`, server membalas **0 tool**
> tanpa pesan error — terlihat seperti server rusak, padahal cuma salah header.

72 tool tersedia. Yang paling sering dipakai:

| Tool | Fungsi |
|---|---|
| `content_create` | Buat artikel (draft) — isi field rich text sebagai **string Markdown** |
| `content_get` | Ambil artikel + **`_rev`** |
| `content_publish` | Terbitkan — **butuh `_rev`** |
| `media_create` | Unggah media ke R2 (otomatis: blurhash, warna dominan, hash) |
| `settings_update` | Ubah judul/tagline/SEO situs |

### ⚠️ `_rev` — alur yang benar

`content_update`, `content_publish`, `content_unpublish`, `content_discard_draft`, `content_schedule`
**semuanya butuh `_rev`**. Alur yang benar:

```
content_create  →  content_get (ambil _rev)  →  content_publish (_rev)
```

Kalau muncul `CONFLICT`: artikelnya berubah sejak kamu membaca → **`content_get` lagi**, pakai `_rev` baru.

> **Catatan versi:** di 1.0.1, `content_get` **tidak** mengembalikan `_rev` meski
> deskripsinya menjanjikannya — jadi publish via MCP mustahil. Kami menambalnya.
> Format internalnya: `base64(version + ":" + updatedAt)`.
> Cek dulu apakah versimu sudah diperbaiki sebelum menambal.

---

## 10. Daftar masalah yang kami temui (untuk dicek lebih dulu)

| # | Gejala | Sebab | Solusi |
|---|---|---|---|
| 1 | "Setup session expired or tampered with" | Cookie sesi `SameSite=Strict` | ubah ke `Lax` |
| 2 | Publish via MCP gagal: `_rev` required | `content_get` tidak mengembalikan `_rev` | tambal, atau pakai versi > 1.0.1 |
| 3 | "Failed to generate passkey options" | passkey pertama: `allowCredentials` kosong | daftarkan passkey dari **ponsel** dulu |
| 4 | Admin terus memantul ke wizard | `emdash:setup_complete` belum ada | tuntaskan setup (bagian 6) |
| 5 | Email mati: `SyntaxError: Unexpected token '\'` | nilai JSON ter-escape ganda | tulis nilai JSON yang benar |
| 6 | Provider email selalu jatuh ke `sendmail` | kredensial di tabel/kunci salah | bagian 8 (3 jebakan) |
| 7 | Magic-link "sukses" tapi tidak ada email | email ≠ email terdaftar, atau kena rate limit | periksa tabel `auth_tokens` |

**Tips praktis untuk #3:** passkey pertama paling gampang didaftarkan dari **ponsel** —
hampir semua ponsel punya Face ID/sidik jari, sementara desktop sering butuh konfigurasi
Windows Hello atau password manager dulu. Setelah satu passkey terdaftar, sisanya mudah.

---

## 11. Sebelum `pnpm install` ulang — baca ini

Panduan ini menyebut beberapa **tambalan** yang kami buat di `node_modules`. Itu **hilang**
setiap `pnpm install` / update paket.

**Yang bertahan:** tambalan di kode proyek kita sendiri (`src/worker.ts`), karena file itu milik kita.

**Yang hilang:** tambalan di `node_modules/` (`SameSite`, `_rev`, bootstrap passkey, bundle admin).

**Sebelum menjalankan `pnpm install`:**

```bash
# cadangkan tambalan
mkdir -p ~/emdash-patch-backup
grep -rl "CHOKDI" node_modules/ 2>/dev/null | tee ~/emdash-patch-backup/file-list.txt
```

Lalu **catat**: jenis tambalan, file, baris, dan satu baris kode yang diubah. Tanpa catatan,
kamu akan mengulang seluruh proses debugging ini dari awal.

**Cara paling tahan lama:** buat tambalan itu sebagai bagian dari kode kita
(patch otomatis setelah install), supaya tidak bergantung pada ingatan.

---

## 12. Checklist

**Sebelum deploy:**
- [ ] Domain sudah siap (bukan `*.workers.dev`)
- [ ] D1 + R2 + KV dibuat dengan **nama unik**
- [ ] `siteUrl` sudah diisi di `astro.config.mjs`
- [ ] `SESSION` = string acak panjang

**Setelah deploy:**
- [ ] `needsSetup: false`
- [ ] Semua opsi setup lengkap + JSON valid
- [ ] `/_emdash/admin` → **200** (bukan redirect)
- [ ] Passkey pertama terdaftar (dari ponsel)
- [ ] Provider email aktif — uji kirim sungguhan, periksa **tabel token**
- [ ] DMARC/SPF terpasang kalau email masuk spam

**Sebelum `pnpm install` ulang:**
- [ ] Tambalan `node_modules` sudah dicadangkan + dicatat

---

## Penutup

EmDash menjanjikan CMS yang **ramah agent** — dan itu benar: 72 tool MCP, API bersih, jalan
penuh di Cloudflare tanpa server. Yang membuatnya terasa berat bukan konsepnya, tapi
**detail kecil**: cookie, kunci penyimpanan berlapis, format tanggal, header `Accept`.

Semua sudah didokumentasikan di atas. Dengan panduan ini, instalasi di domain baru
seharusnya **selesai dalam sekali duduk** — bukan tiga jam.

---

*Ditulis oleh Chokdi Staging — 29 September 2026.*
*Diuji langsung di EmDash 1.0.1, Cloudflare Workers + D1 + R2 + KV.*
