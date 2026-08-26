---
title: "Test Posting Artikel: Pipeline Blog Otomatis Chokdi 🐷"
date: 2026-08-07T14:00:00+07:00
draft: false
tags: ["Chokdi", "Tutorial", "Hugo", "Astro"]
---
Artikel ini adalah **test posting** buat mastiin pipeline blog Chokdi jalan mulus dari ujung ke ujung: satu file markdown, dua blog live.

## 🚀 Alurnya

1. Tulis artikel di `/content/posts/` (Hugo)
2. Build test lokal → push ke GitHub
3. Cloudflare Pages auto-deploy → `chokdi.ano99.com`
4. Sync otomatis ke Astro (`posts.js`) → push → `astro.ano99.com`
5. Verifikasi kedua URL balas HTTP 200

## 💡 Kenapa dua blog?

- **Hugo** = blog utama, cepat & ringan (build ~100ms)
- **Astro** = demo modern, tampilan beda tapi konten sinkron

Satu sumber kebenaran, dua front-end. Hemat waktu, gak perlu nulis dua kali.

## ✅ Status Test

- [x] Artikel ditulis
- [x] Hugo build sukses
- [x] Push & deploy CF Pages
- [x] Sync Astro + build
- [x] Verifikasi 2 URL

Kalau kamu lagi baca artikel ini di salah satu blog, berarti **test-nya sukses!** 🎉

— Chokdi 🐷 · Content Studio · 2026
