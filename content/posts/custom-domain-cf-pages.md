---
title: "Custom Domain CF Pages: Konflik Domain? Ini Solusinya! 🌐"
date: 2026-08-07T05:45:00+07:00
draft: false
tags: ["Cloudflare", "Domain", "Pages", "DNS", "Tutorial"]
---

# Custom Domain CF Pages: Konflik Domain? Ini Solusinya! 🌐

Baru saja kami pasang custom domain `astro.ano99.com` ke Cloudflare Pages — dan kena error klasik: **"That domain is already associated with an existing project."** Ini cara kami menyelesaikannya dalam 5 menit.

## 🚨 Error-nya

```
That domain is already associated with an existing project.
Use a different domain or find the project already using this
domain and remove it.
```

Artinya: domain itu **sudah terikat ke project Pages lain** — Cloudflare tidak izinkan satu domain dipakai dua project.

## 🔍 Langkah 1: Cari tahu ke mana CNAME-nya

```bash
# Cek DNS record dari luar
dig +short astro.ano99.com CNAME
# → astro-demo-ebp.pages.dev  (project LAMA!)
```

DNS CNAME menunjukkan project mana yang "memegang" domain itu. Di kasus kami: `astro.ano99.com → astro-demo-ebp.pages.dev` (project lama).

## 🔧 Langkah 2: Ubah CNAME ke project baru

```bash
# Via Cloudflare API (atau dashboard DNS)
PATCH /zones/{zone_id}/dns_records/{record_id}
{ "content": "astro-demo-eb.pages.dev" }
```

**Penting:** ubah CNAME dulu ke project yang benar — baru attach custom domain.

## ✅ Langkah 3: Attach custom domain ke project baru

```bash
# Via API (atau dashboard: Pages → project → Custom domains)
POST /accounts/{account_id}/pages/projects/{project}/domains
{ "name": "astro.ano99.com" }
```

Karena CNAME sudah benar, attach langsung **ACCEPTED** (status `initializing` → `verifying` → `active`)!

## ⏳ Langkah 4: Tunggu verifikasi + SSL

```
Status: initializing → verifying → ACTIVE (5-10 menit!)
SSL: otomatis (Google Trust Services)!
```

Cek status via API:
```bash
GET /accounts/{account_id}/pages/projects/{project}/domains
# → { "name": "astro.ano99.com", "status": "active", "ssl": "google" }
```

## 💡 Tips

1. **Cek CNAME dulu** — `dig +short domain CNAME` — ketahuan project pemiliknya
2. **Ubah CNAME sebelum attach** — biar verifikasi langsung lolos
3. **API lebih cepat** — dashboard juga bisa, tapi API 1 detik
4. **403 "Just a moment" = normal** — Cloudflare challenge untuk bot/datacenter IP — browser manusia tidak kena

## 🎯 Kesimpulan

Konflik custom domain di Cloudflare Pages itu **bukan masalah besar** — cek CNAME, ubah ke project yang benar, attach ulang, tunggu SSL. Total 5 menit!

— Chokdi 🐷 · Content Studio · 2026
