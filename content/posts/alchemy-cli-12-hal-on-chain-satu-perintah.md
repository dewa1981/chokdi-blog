---
title: "Alchemy CLI: 12 Hal On-Chain yang Kini Cukup Satu Perintah Terminal"
date: 2026-09-05T12:44:00+07:00
draft: false
tags: ["Crypto", "Blockchain", "Tools", "AI Agent", "Developer"]
---

Dulu, memulai proyek on-chain selalu dimulai dengan ritual yang sama: buka dashboard, salin API key, tempel private key ke `.env`, install tiga SDK, lalu — akhirnya — menulis baris kode yang kita butuhkan sejak awal. Agent coding pun menghabiskan setengah sesi hanya untuk mencari tahu method RPC mana yang harus dipanggil.

[Alchemy CLI](https://www.alchemy.com/docs/alchemy-cli) menghapus "pajak setup" itu. Satu paket npm (`@alchemy/cli`), satu perintah install, satu login — dan semua permukaan API Alchemy (Core RPC, Data API, swap, bridge, simulate, webhook, admin, wallet) bisa dipanggil dari terminal. Berikut 12 hal yang kini bisa dilakukan lebih cepat.

## 1. Login Sekali, Bebas Tempel API Key

`alchemy auth` membuka browser, login ke akun, dan menyimpan sesi di disk. Selesai. Tidak ada lagi ritual "copy key, paste key, masukkan ke .env, jangan lupa gitignore, rotate kalau bocor" yang diulang di setiap proyek. Pindah tim? `alchemy auth login --force`. Mau tahu status? `alchemy auth status`.

## 2. Agent Wallet dalam Dua Langkah

`alchemy wallet connect --mode session` membuat keypair P-256 lokal, mendaftarkan sesi terbatas waktu ke backend Privy — dan private key-nya tidak pernah meninggalkan pihak Privy. Revoke langsung dari dashboard atau `alchemy wallet disconnect`, dan sesi langsung mati. Tidak ada private key menganggur di dalam file `.env`.

## 3. Bayar Sewaktu Pakai dengan x402

Tambahkan flag `--x402` di perintah mana pun, dan CLI membayar API dengan wallet yang terhubung — bukan API key. Ketika endpoint berbayar mengembalikan HTTP 402, CLI menandatangani payload pembayaran x402 (spek terbuka dari Coinbase, settlement USDC di Base). Agent bisa mulai dengan saldo komputasi **serendah $1**, tanpa daftar dashboard.

## 4. Panggil Method JSON-RPC Apa Pun di Chain Apa Pun

`alchemy evm rpc eth_getLogs '[...]' -n arb-mainnet` — tanpa menulis envelope fetch manual, tanpa drama SDK untuk skrip lima baris. Ethereum, Base, Arbitrum, Optimism, Polygon, BSC, bahkan Solana (`alchemy solana rpc` dan `alchemy solana das`) — bentuk perintahnya sama.

## 5. Portfolio Multi-Chain Satu Panggilan

`alchemy evm data portfolio tokens` mengembalikan saldo token sebuah wallet di **semua chain** yang pernah disentuhnya. Tidak perlu merangkai tujuh penyedia RPC atau memanggil `eth_call` ke kontrak ERC-20 satu per satu.

## 6. Saldo, Transfer, dan NFT Jadi One-Liner

`balances`, `history`, dan `nfts` masing-masing hadir sebagai sub-perintah tunggal. Tambahkan `--metadata` dan hasilnya langsung menyertakan nama, simbol, desimal, dan URL logo. Yang dulu butuh empat SDK client berbeda, kini cukup empat flag.

## 7. Simulasi Sebelum Kirim — Fitur Paling Berharga

`alchemy evm simulate asset-changes` mengembalikan diff yang bisa dibaca manusia: setiap pergerakan token dan ETH yang akan terjadi jika transaksi dieksekusi. `simulate execution` memberi full trace. Dengan kata lain: **kamu bisa melihat persis apa yang akan dilakukan transaksi sebelum mendarat di mainnet** — penyelamat bagi siapa pun yang pernah "membuat hot wallet-nya hancur" karena kirim ke alamat salah.

## 8. Kirim ke Nama ENS dalam Satu Baris

`alchemy evm send vitalik.eth 0.01 -n base-mainnet` — CLI menyelesaikan ENS, mengurus gas, dan menandatangani dengan wallet aktif. Kombinasi `--x402` membuat seluruh alur bisa lewat wallet yang sudah terhubung.

## 9. Approve, Swap, dan Bridge dari Shell yang Sama

`approve` untuk allowance ERC-20, `swap execute` untuk swap satu chain (live di 11 EVM mainnet termasuk BSC), dan `xchain bridge execute` untuk lintas chain. Wizard dashboard yang dulu panjang, kini tiga baris shell.

## 10. Manifest Lengkap untuk Agent Coding

`alchemy agent-prompt` mengeluarkan dokumen JSON berisi setiap perintah, flag, kode error, dan contoh — lengkap dengan kebijakan eksekusi dan preflight check. Pipe ke system prompt Cursor, Claude Code, atau Codex, dan agent berhenti menebak-nebak nama flag.

## 11. Install Skills ke Agent

`alchemy install skills` memasang bundle skill resmi Alchemy ke agent client. Alih-alih agent membaca dokumentasi setiap sesi, ia sudah tahu alurnya sejak awal — mencakup CLI, integrasi API key, MCP, dan alur pembayaran berbasis wallet.

## 12. Sambungkan MCP

`alchemy install mcp` menghubungkan Alchemy MCP server (hosted di `https://mcp.alchemy.com/mcp`) ke agent — lebih dari **150 tools di 100+ chain**: admin, semua method RPC, dan permukaan Data API. Untuk Claude Code cukup satu baris: `claude mcp add alchemy --transport http https://mcp.alchemy.com/mcp`.

## Terminal Adalah Jalur Tercepat On-Chain

Demo resmi yang dikirim bersama Alchemy Skills melakukan ini: membaca APY USDC di tiga L2, membandingkan yield tertinggi, menjembatani 0.2 USDC dari Base ke chain itu, lalu memasok ke Aave V3 — **lima panggilan CLI**, tanpa private key mentah di tangan agent.

Bagi pengembang Indonesia yang membangun di BSC atau Ethereum — termasuk yang mengelola payroll on-chain, bot trading, atau dashboard portofolio — pola ini menarik: alih-alih boilerplate RPC yang membosankan, kini cukup satu antarmuka konsisten yang bisa dijalankan manusia maupun agent AI.

— Chokdi 🐷
