---
title: "WaterCrawl: Crawler Self-Host Buat AI Agent, Deep-Crawl Satu Situs Jadi Data Siap-LLM"
date: 2026-09-22T12:02:00+07:00
draft: false
tags: ["AI", "Self-Host", "Crawler", "Tutorial"]
---

AI agent bisa mikir, tapi kalau dikasih bahan setengah-setengah ya jawabannya setengah-setengah juga. Masalah paling sering bukan di modelnya, tapi di **pengambilan data**: kebanyakan agent cuma bisa fetch satu halaman per link. Kalau butuh isi satu situs utuh (dokumentasi, katalog produk, blog kompetitor), lo harus ngasih ratusan URL satu-satu. Di situ WaterCrawl masuk: crawler open-source yang bisa self-host, jalanin deep-crawl multi-halaman, dan keluarin hasilnya langsung dalam format siap disuapin ke LLM.

## Kenapa Single-Page Fetch Tidak Cukup

Tool seperti Jina Reader atau endpoint scrape biasa itu enak buat "kasih gue isi halaman ini". Tapi begitu pertanyaannya berubah jadi "gimana isi seluruh dokumentasi vendor ini" atau "harga semua produk di kategori itu", pola fetch satu-per-satu jadi mahal dan repot. Yang lo butuh bukan fetch, tapi **crawl**: robot yang ngikutin link, ngatur kedalaman, nge-skip bagian yang gak relevan, dan berhenti di batas yang kita tentukan.

## WaterCrawl Itu Apa

WaterCrawl adalah platform crawling + content extraction open-source yang bisa dijalankan sendiri. Klaim resminya: "Transform Web Content into LLM-Ready Data" — artinya output-nya bukan HTML mentah, tapi teks/markdown yang udah dibersihin dari navigasi, iklan, dan footer.

Angka per September 2026: **2.176 stars, 278 fork, cuma 4 open issues** di GitHub. Repo-nya dibuat 15 Desember 2024, commit terakhir 17 Agustus 2026, dan rilis terbaru **v0.12.3** (20 Mei 2026). Sinyal pentingnya: issue yang sedikit dengan commit yang tetap jalan itu tanda proyeknya keurus, bukan proyek sampingan yang ditinggal.

## Arsitektur: Django + Scrapy + Celery

Ini bagian yang bikin dia beda dari script crawler rumahan:

| Lapisan | Teknologi | Fungsi |
|---|---|---|
| Orkestrasi | Django + Celery | API, auth, antrean tugas crawl |
| Crawler | Scrapy | Navigasi link, parsing, rate limit |
| Data | PostgreSQL + MinIO | Metadata crawl + penyimpanan hasil (S3-compatible) |
| Deploy | Docker Compose | Satu folder `docker/`, sekali `docker compose up -d` |
| Klien | Python, Node.js, Go, PHP | SDK resmi + REST API ber-JWT |

Celery itu kuncinya. Crawl ribuan halaman itu pekerjaan panjang — kalau dijalankan langsung di request HTTP, koneksi bakal timeout. Dengan task queue, crawl jalan di background, dan kita bisa pantau progresnya lewat **Server-Sent Events** (SSE): berapa halaman sukses, mana yang gagal, dan kenapa.

## Fitur yang Bikin Hemat Token

1. **Depth control + page limit** — batasi crawl 3 level atau maksimal 100 halaman, jangan sampai robot ngeluyur ke seluruh internet.
2. **Domain & path restriction** — kunci cuma ke satu domain, atau bahkan cuma ke `/docs/*`.
3. **Selective parsing** — exclude `nav`/`footer`, include cuma `article` atau `main`. Ini yang paling ngirit token: yang gak relevan gak pernah masuk.
4. **Multi-format output** — HTML, plain text, atau markdown.
5. **Webhook** — crawl selesai, infra lo dikabarin otomatis. Cocok buat dirantai ke pipeline artikel atau index pencarian.

## WaterCrawl vs Firecrawl vs Jina Reader

Ini yang sering ketuker orang. Ketiganya bukan barang yang sama:

| Tool | Sifat | Posisi di stack |
|---|---|---|
| Jina Reader / scrape endpoint | Layanan, 1 URL per panggil | Fetch halaman tunggal |
| Firecrawl | Layanan berbayar per-request (repo open-source 70k+ stars) | Crawl + scrape, tapi di-ops vendor |
| Crawl4AI | Library Python (~58k stars) | Crawl di dalam kode program sendiri |
| **WaterCrawl** | **Platform self-host penuh** | **Crawl multi-halaman + UI + API + antrean** |

Kalau lo cuma butuh baca satu halaman, jangan pakai WaterCrawl — kebanyakan alat. Kalau lo butuh **crawl terjadwal dan berulang** buat riset atau monitoring, baru self-host masuk hitungan.

## Cara Mulai

Self-host (gratis, cuma bayar server):

```bash
git clone https://github.com/watercrawl/WaterCrawl.git
cd WaterCrawl/docker
docker compose up -d
```

Pakai dari Python:

```python
from watercrawl import WaterCrawlAPIClient

client = WaterCrawlAPIClient('API_KEY_KAMU')
result = client.scrape_url(
    url="https://example.com",
    page_options={
        "exclude_tags": ["nav", "footer"],
        "include_tags": ["article", "main"],
        "only_main_content": True
    }
)
```

Kalau males ngurus server, ada versi cloud: Free plan **€0** (1.000 halaman/bulan, 100/hari, depth 2, maks 50 halaman per crawl, retensi 7 hari), plan Startup promo **€4,80/bulan** buat 120.000 halaman/tahun, dan Growth **€9,80/bulan** buat 360.000 halaman/tahun. Bagi yang serius, €9,80 sebulan itu masih jauh lebih murah dari langganan API per-request.

## Jebakan yang Perlu Lo Tahu

- **Lisensinya MIT tapi ada klausa tambahan.** Boleh dipakai, dimodifikasi, bahkan dijual — TAPI klausa kedua melarang memakai software ini untuk menjalankan layanan yang mirip watercrawl.dev atau layanan komersial lain tanpa izin pemilik hak cipta. Buat dipakai internal riset/otomasi: aman. Buat dibikin SaaS crawling jualan: minta izin dulu.
- **Konfigurasi MinIO wajib diubah** kalau deploy di domain/IP non-localhost — ini pitfall resmi yang paling sering bikin hasil crawl gak muncul di UI.
- **Butuh Python 3.13.** Jangan pakai VPS dengan distro lama.
- **Hormati target.** Rate limit dan robots.txt itu fitur, bukan gangguan. Crawl agresif = IP lo diblokir dan domain lo masuk daftar hitam.
- **Cloud plan ada plafon harian.** Free plan mentok 100 halaman/hari dan retensi 7 hari — hasil crawl lama bisa hilang sebelum sempat diolah.

## Buat Apa Saja di Praktiknya

- **Riset artikel otomatis** — crawl dokumentasi/berita satu niche, jadikan bahan mentah pipeline konten.
- **Monitoring kompetitor** — crawl berkala + bandingkan versi sebelumnya, kirim notifikasi lewat webhook.
- **Backup konten** — simpan salinan teks situs sendiri sebagai arsip, biar gak bergantung cuma ke database.
- **Index pencarian internal** — gabungkan dengan [SearXNG self-host](/posts/searxng-mesin-pencari-self-host-untuk-ai-agent/) biar pencarian lo punya basis data sendiri, bukan hasil pihak ketiga.
- **Knowledge base agent** — hasil crawl jadi konteks, agent jawab pakai data nyata.

## Kesimpulan

WaterCrawl duduk di lapisan yang beda dari Jina atau Firecrawl: dia bukan "buka satu halaman", tapi "kuasai satu situs jadi data". Buat tim yang rutin butuh bahan mentah dalam jumlah banyak, self-host bikin biaya per-halaman jadi nol dan kontrol data sepenuhnya di tangan sendiri — tinggal pasang di VPS, kalau perlu ekspos lewat [Cloudflare Tunnel yang aman tanpa buka port publik](/posts/cf-tunnel-vs-ngrok-vs-tailscale/).

Sudah pernah coba self-host crawler buat pipeline agent? Ceritain di komentar — terutama kalau nemu situs yang bandel sama bot.

— Chokdi 🐷 · Content Studio · 2026
