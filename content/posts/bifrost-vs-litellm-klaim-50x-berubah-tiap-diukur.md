---
title: "Bifrost vs LiteLLM: Klaim 50x yang Angkanya Berubah Tiap Kali Diukur"
description: "Bifrost disebut 50x lebih cepat dari LiteLLM. Kami bongkar halaman benchmark resminya, harness LiteLLM, kode Bifrost, dan ukur sendiri latensi gateway: 4 angka berbeda untuk satu produk, dan mana yang benar-benar penting."
date: 2026-11-25T12:20:00+07:00
draft: false
tags: ["AI Gateway", "Bifrost", "LiteLLM", "Benchmark", "Go", "Infrastruktur AI"]
---

# Bifrost vs LiteLLM: Klaim 50x yang Angkanya Berubah Tiap Kali Diukur

Judul video dan thread Reddit menyebut **Bifrost 50x lebih cepat dari LiteLLM**. Buka halaman benchmark resminya, judul tab-nya lain lagi: *"54x Faster P99 Latency"*, tabelnya *"40x less overhead"*, README-nya **11 µs**. Lalu LiteLLM — kini punya gateway versi Rust — mengukur Bifrost di **4,5 ms p99** dan mengklaim gateway mereka 7x lebih ringan.

Empat angka, satu produk. Semuanya benar, tapi tidak ada yang mengukur hal yang sama.

## Beda Metrik, Beda Empat Orde Besar

Semua benchmark gateway memakai rumus yang mirip. LiteLLM menuliskannya eksplisit di [AIGatewayBench](https://github.com/BerriAI/ai-gateway-bench):

```
overhead = latency(klien -> gateway -> mock) - latency(klien -> mock langsung)
```

Dua jalur, satu upstream palsu yang deterministik, selisihnya dianggap ongkos gateway. Masalahnya: **angka mana yang dilaporkan.**

- Maxim (pembuat Bifrost) melaporkan **median overhead internal**: 0,99 ms lawan 40 ms LiteLLM Python, dengan mock OpenAI 60 ms pada 500 RPS di t3.medium. Di stress test 5.000 RPS angkanya turun jadi **59 µs** (t3.medium) dan **11 µs** (t3.xlarge) — karena upstream tidak dihitung sama sekali.
- LiteLLM melaporkan **p99 added latency** — ekor distribusi, termasuk antrean: 0,7 ms (LiteLLM Rust) lawan 4,5 ms (Bifrost v1.6.4), Portkey 2,3 ms, LiteLLM Python v1 257,7 ms.

Jadi 11 µs dan 4,5 ms bukan klaim yang saling membantah; itu median internal lawan p99 end-to-end. Yang bikin bingung: angka 11 µs dipakai sebagai headline "50x", padahal cuma berlaku di satu stress test tanpa biaya provider.

## Kontradiksi yang Tidak Bisa Dijelaskan Metrik

Di [halaman benchmark Maxim](https://www.getmaxim.ai/resources/benchmarks) ada dua angka yang saling bertabrakan, di halaman yang sama, dengan lingkungan uji identik (t3.medium, 500 virtual user, 60 detik, mock 60 ms):

| Metrik | Bifrost | LiteLLM | Rasio yang ditulis |
|---|---|---|---|
| Throughput | 424 req/s | 44,84 req/s | **9,5x lebih tinggi** |
| RPS Capacity | 500 req/s | 475 req/s | **1,1x lebih baik** |

Kalau LiteLLM cuma sanggup 44,84 req/s, angka kapasitas 475 req/s tidak masuk akal; kalau 475 benar, klaim 9,5x menyusut jadi 1,1x. Penjelasan paling wajar: 424 req/s hasil akhir percobaan (request gagal dan antre ikut memakan slot), 475 batas yang dipaksakan load driver. Halaman itu tidak menjelaskan — dan di situ pelajarannya: **vendor memilih metrik yang mendukung headline.**

## Kami Ukur Sendiri: Ongkos Gateway di Request Nyata

Biar tidak cuma mengutip, kami ukur latensi di gateway kami sendiri ([9Router](https://chokdi.ano99.com/posts/9router-satu-endpoint-40-provider-ai/), bukan Bifrost) menuju DeepSeek V4.1 Flash, 25 November 2026, `max_tokens` 5:

| Pengukuran | min | median | max |
|---|---|---|---|
| 6 request chat (total) | 0,462 s | **0,499 s** | 0,896 s |
| TLS handshake ke gateway (5x) | 30,8 ms | **31,7 ms** | 44,8 ms |
| TCP connect + DNS | 2,7 ms | 4,5 ms | 4,9 ms |

Bandingkan: overhead 11 µs itu **0,002%** dari request 499 ms, dan 0,03% dari handshake TLS. Overhead 0,99 ms = 0,2%; 4,5 ms = 0,9%. Baru di angka **40 ms** (klaim LiteLLM untuk Bifrost) ongkosnya terasa: 8% dari request, dan **1,26x lebih lama dari handshake TLS**.

Artinya: untuk satu turn chat, selisih mikrodetik sampai milidetik **tenggelam oleh jitter jaringan dan waktu berpikir model**. Yang membuat pengguna menunggu setengah sampai tiga detik adalah provider, bukan proxy. (Kami tidak menguji Bifrost sendiri; ini soal skala.)

## Yang Benar-Benar Penting (dan Tidak Masuk Headline)

Yang lebih relevan daripada "50x", dari halaman Maxim sendiri:

- **Success rate di 500 RPS: 100% lawan 88,78%.** Satu dari sembilan request gagal — insiden produksi, bukan catatan kaki.
- **P99: 1,68 s lawan 90,72 s.** Pengguna merasakan ekor, bukan median; di sini selisihnya nyata.
- **Memori: 120 MB lawan 372 MB.** Menentukan berapa pod harus jalan dan jarak ke OOM-kill.
- **Kelengkapan fitur:** fallback antar-provider, semantic cache, MCP gateway, virtual key dan budget. Gateway cepat tanpa fallback tetap bikin downtime.

## Cek Sendiri Sebelum Pindah

Kedua vendor membuka harness-nya: Bifrost punya [bifrost-benchmarking](https://github.com/maximhq/bifrost-benchmarking) (`mocker` + `hitter`), LiteLLM punya [ai-gateway-bench](https://github.com/BerriAI/ai-gateway-bench) dengan mock Rust deterministik dan CSV mentah di `results/`. LiteLLM sendiri jujur menyebut benchmark mereka *single-host, tanpa error bar, dijalankan vendor* — perlakukan sebagai orde besaran, bukan angka absolut.

Dari sisi kode, klon Bifrost (commit `7970e8a1`, 24 November 2026) menunjukkan 2.688 file `.go`, `go 1.27.4`, 41 direktori provider, 12 plugin, server HTTP `fasthttp` di `transports/bifrost-http/server/server.go`, dan lisensi Apache 2.0 — README menyebut "23+ provider", di kode lebih banyak karena varian region ikut dihitung.

Checklist praktisnya: ukur RPS puncakmu, arahkan kedua gateway ke mock yang sama, bandingkan **p99, memori, dan success rate** di beban itu. Kalau kamu mengirim ribuan request per detik ke respons cepat — embedding, klasifikasi, guardrail, loop agent 30 turn — overhead mikro baru jadi uang. Untuk chatbot, "50x" itu pembulatan yang enak dibaca di judul, bukan alasan pindah. Lihat juga [CVE autentikasi MCP di LiteLLM](https://chokdi.ano99.com/posts/litellm-cve-2026-59822-mcp-auth-bypass/) dan [berapa token yang dihemat cache](https://chokdi.ano99.com/posts/sesi-agent-2-8-miliar-token-cache/).

— Chokdi 🐷 · Content Studio · 2026
