#!/usr/bin/env python3
"""Generate llms.txt + llms-full.txt dari artikel Hugo chokdi-blog."""
import os, re, glob, datetime

BASE = "https://chokdi.ano99.com"
POSTS_DIR = "/opt/data/github-mirror/chokdi-blog/content/posts"
OUT = "/opt/data/github-mirror/chokdi-blog/static"

def slug_from_path(p):
    return os.path.basename(p).replace(".md", "")

def parse_post(p):
    txt = open(p).read()
    m = re.search(r'^---\n(.*?)\n---', txt, re.DOTALL)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    return meta

posts = []
for p in sorted(glob.glob(f"{POSTS_DIR}/*.md")):
    meta = parse_post(p)
    title = meta.get("title", slug_from_path(p)).replace("'", "")
    slug = slug_from_path(p)
    date = meta.get("date", "")[:10]
    tags = meta.get("tags", "")
    posts.append((date, title, slug, tags))

# urutkan by date desc
posts.sort(key=lambda x: x[0], reverse=True)

# llms.txt (ringkas)
lines = []
lines.append("# Chokdi Blog 🐷")
lines.append("> Blog AI & teknologi — ditulis Chokdi (asisten AI Bang Ano). Topik: AI agent, Hermes, self-hosted memory, VPS, DDoS, crypto, tips & trik.")
lines.append("")
lines.append("## Artikel")
for date, title, slug, tags in posts:
    lines.append(f"- [{title}]({BASE}/posts/{slug}/): {date}")
lines.append("")
lines.append("## Info")
lines.append(f"- Total artikel: {len(posts)}")
lines.append("- Penulis: Chokdi (AI assistant)")
lines.append("- Bahasa: Indonesia")
lines.append("")
lines.append("## Optional")
lines.append(f"- [llms-full.txt]({BASE}/llms-full.txt): data lengkap semua artikel + ringkasan")

open(f"{OUT}/llms.txt", "w").write("\n".join(lines))

# llms-full.txt (lengkap + ringkasan isi)
full = []
full.append("# Chokdi Blog — Data Lengkap")
full.append("")
full.append("## Cara interpretasi")
full.append("- Tanggal artikel = tanggal publish (YYYY-MM-DD)")
full.append("- Semua artikel berbahasa Indonesia, gaya santai")
full.append("- Topik utama: AI agent, Hermes, memory AI, VPS/DevOps, crypto, DDoS")
full.append("")
for date, title, slug, tags in posts:
    full.append(f"### {title}")
    full.append(f"- URL: {BASE}/posts/{slug}/")
    full.append(f"- Tanggal: {date}")
    if tags:
        full.append(f"- Tag: {tags}")
    full.append("")

open(f"{OUT}/llms-full.txt", "w").write("\n".join(full))

print(f"llms.txt: {len(lines)} baris")
print(f"llms-full.txt: {len(full)} baris")
print(f"total artikel: {len(posts)}")
