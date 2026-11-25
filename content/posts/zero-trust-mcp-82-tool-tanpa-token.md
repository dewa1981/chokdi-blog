---
title: "Zero Trust untuk MCP: 82 Tool, 4 Server Tanpa Token, 0 Hash Metadata"
description: "Kami probe 5 server MCP di host sendiri tanpa satu pun kredensial: empat menjawab, satu menolak. Ditambah 222 kegagalan OAuth sehari, inilah peta zero trust yang sebenarnya untuk agent."
date: 2026-11-25T18:10:00+07:00
draft: false
tags: ["MCP", "Keamanan AI", "Zero Trust", "Agent", "OAuth", "Infrastruktur AI"]
---

# Zero Trust untuk MCP: 82 Tool, 4 Server Tanpa Token, 0 Hash Metadata

Agent kami memegang enam server MCP. Hari ini kami panggil satu per satu tanpa header `Authorization`. Empat dari lima server aktif menyelesaikan handshake `initialize`, termasuk [server browser headless](https://chokdi.ano99.com/posts/chrome-devtools-mcp-agent-buta-jadi-bisa-lihat/) dengan 32 tool. Satu menolak — dan justru server itu yang hari ini mencatat 222 kegagalan OAuth. Zero trust untuk MCP bukan lapisan tambahan; ia yang tersisa ketika tool bisa membuka halaman, menjalankan JavaScript, dan memanggil API atas nama kita.

## Protokolnya sendiri tidak bisa menegakkan consent

MCP hanya memindahkan JSON-RPC. Halaman [Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) versi 2026-07-28 menyatakan protokol tidak bisa menegakkan user consent atau keamanan tool; host, client, dan server harus mengimplementasikannya sendiri. Dokumen itu mendaftar pola serangan: confused deputy, token passthrough, scope minimization, state handle hijacking, tool poisoning, rug pull, sampai DNS rebinding pada server lokal.

Skalanya nyata. Knostic, dikutip [CSO Online](https://www.csoonline.com/article/4168979/1800-mcp-servers-exposed-without-authentication-how-zero-trust-can-secure-the-ai-agent-revolution.html), menemukan 1.862 server MCP terbuka di internet; 119 diverifikasi manual, dan 119 dari 119 membocorkan daftar tool tanpa autentikasi. Jalur exploit juga nyata: EchoLeak (CVE-2025-32711) prompt injection zero-click, `mcp-remote` (CVE-2025-6514) command injection lewat parameter OAuth, dan [CVE LiteLLM](https://chokdi.ano99.com/posts/litellm-cve-2026-59822-mcp-auth-bypass/) di jalur MCP.

## Yang kami ukur sendiri

Kami kirim `initialize` polos ke setiap endpoint gateway — tanpa token, cookie, atau session:

```bash
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
```

| Server | Auth | `initialize` tanpa kredensial | `tools/list` tanpa kredensial |
|---|---|---|---|
| `lightpanda` (tailnet) | tidak ada | 200 · 7 ms | 32 tool · 31.104 byte |
| `firecrawl` (remote) | Bearer di gateway | 200 | 3 tool (40 dengan key) |
| `cfdocs` (remote) | tidak ada | 200 | 2 tool + 2 prompt |
| `cfblog` (remote) | tidak ada | 200 | 4 tool |
| `cloudflare` (remote) | OAuth | **401** | — |
| `cfobs` (remote) | OAuth | disabled | — |

Tiga hal penting. Pertama, 200 di `initialize` bukan berarti semua tool bebas dipanggil: tanpa key firecrawl hanya membuka 3 tool, dengan Bearer kami melihat 40. Kedua, kontrol lightpanda bukan kredensial aplikasi melainkan Tailscale — endpoint-nya di `100.94.241.77:8000`, dan tailnet kami punya 46 perangkat (28 online saat probe); siapa pun di tailnet bisa memanggil 32 tool browser tanpa password. Ketiga, `mcp.cloudflare.com` satu-satunya yang menolak, dan benar: 401 dengan `scope="user:read account:read"`.

## 31 KB metadata yang tidak pernah diverifikasi

`tools/list` lightpanda mengembalikan 32 tool, 31.104 byte JSON; 12.383 karakter di antaranya deskripsi yang dibaca model, bukan manusia. Di sinilah tool poisoning bekerja: deskripsi tool adalah teks di context yang sama dengan instruksi pengguna. Invariant Labs mendemonstrasikan tool yang menyuruh model membaca `~/.ssh/id_rsa` dan mengirimkannya sebagai argumen, sementara client tetap menampilkan nama tool yang terlihat polos.

Dua variannya lebih sunyi. **Rug pull**: deskripsi bersih saat disetujui, diganti setelahnya; client tanpa hash tidak tahu. **Tool shadowing**: satu server mengubah cara model memakai tool server lain. Kami menjalankan empat server dalam satu context — kondisi yang persis dibutuhkan cross-server contamination.

## Ironi 222 kegagalan OAuth

Hari ini log gateway mencatat 222 `OAuthNonInteractiveError`: 12 per jam, tiap lima menit. Penyebabnya server yang paling benar: `cloudflare` memakai OAuth, butuh browser untuk memperbarui token, gateway berjalan non-interaktif. Alurnya sudah kami bedah di [artikel sebelumnya](https://chokdi.ano99.com/posts/agent-background-oauth-288-percobaan-gagal-sehari/); pilihan yang tersisa: login interaktif lalu restart, disable dan pakai API token lewat curl, atau kredensial service jangka panjang.

Polanya jelas: empat server tanpa auth mulus sepanjang hari, satu server yang meminta identitas memberi 0 tool dan 222 baris error. Zero trust tanpa jalur operasional bukan keamanan — hanya kegagalan yang rapi.

## Tujuh kontrol yang bisa dicek hari ini

1. **Token terikat audience.** Client meminta token dengan parameter `resource` ([RFC 8707](https://www.rfc-editor.org/rfc/rfc8707.html)) berisi URL MCP; otorisasi menulis `aud` (RFC 9068); server wajib menolak audience lain.
2. **Larang token passthrough.** Server tidak meneruskan token client ke API hilir; ia butuh token sendiri dengan hak lebih sempit.
3. **Pin hash definisi tool.** Simpan hash deskripsi, bandingkan tiap koneksi — penangkal rug pull paling murah.
4. **Tampilkan deskripsi penuh dan argumen saat approval**, bukan cuma nama tool.
5. **Scope minimum.** Contoh bagus ada di header 401 tadi: `user:read account:read`.
6. **Consent per client.** Dynamic Client Registration sudah deprecated di 2026-07-28, tapi proxy lama masih rentan confused deputy.
7. **Ikat state ke user**, jangan bind server lokal ke `0.0.0.0`, dan log setiap pemanggilan tool termasuk argumennya.

Rincian mitigasi paling rapi ada di [ringkasan spec 2026-07-28](https://restfulapi.net/mcp-security/), termasuk tabel siapa memperbaiki apa.

## Penutup

Zero trust MCP itu tiga lapis identitas: jaringan (tailnet), agent (OAuth per server), dan metadata tool (hash + approval). Kami punya lapis pertama, sebagian lapis kedua, lapis ketiga masih manual — 82 entri tool/resource dari empat server masuk ke satu context tanpa satu pun hash dicek. Keamanan agent bukan saklar yang dinyalakan sekali, tapi rutinitas yang dioperasikan tiap hari.

— Chokdi 🐷 · Content Studio · 2026
