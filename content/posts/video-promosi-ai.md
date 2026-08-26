---
title: "Video Promosi AI: Dari Prompt ke Watermark 🎬"
date: 2026-08-07T06:00:00+07:00
draft: false
tags: ["AI", "Video", "ffmpeg", "Marketing", "Tutorial"]
---
Kami baru saja bikin video promosi Anti-DDoS dari nol: prompt → video AI → watermark logo → teks domain → siap posting. Ini alur lengkapnya.

## 🎬 Langkah 1: Generate Video (MCP Kling)

```json
{
  "model": "kling-video-v3_0_turbo",
  "arguments": [
    {"name": "prompt", "value": "glowing blue shield protecting server, red attack arrows bouncing off, dark futuristic cinematic"},
    {"name": "duration", "value": "10"},
    {"name": "resolution", "value": "1080p"}
  ]
}
```

40-120 detik kemudian: video 10 detik 1080p siap (100 credits).

## 🎨 Langkah 2: Siapkan Logo & Watermark

Bikin icon semi-transparan buat watermark:

```python
from PIL import Image
icon = Image.open("logo.png").resize((256, 256))
alpha = icon.split()[3].point(lambda a: int(a * 0.85))  # 85% opacity
icon.putalpha(alpha)
icon.save("watermark.png")
```

## 🖥️ Langkah 3: Composite dengan ffmpeg

```bash
ffmpeg -y -i video.mp4 -i watermark.png \
  -filter_complex "[0:v][1:v]overlay=30:H-h-30[bg];\
  [bg]drawtext=text='panel.ano99.com':\
  fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:\
  fontsize=34:fontcolor=white@0.85:x=w-tw-30:y=h-th-30:\
  shadowcolor=black@0.6:shadowx=2:shadowy=2[out]" \
  -map "[out]" -map 0:a? \
  -c:v libx264 -crf 20 -preset fast -c:a aac \
  video_final.mp4
```

Hasil: video + watermark logo (kiri-bawah) + teks domain (kanan-bawah) + shadow — **siap posting dalam 8 detik!**

## 📢 Langkah 4: Siapkan Caption

```
🛡️ Website kamu kebal DDoS — mulai FREE!
✅ SSL otomatis ✅ Cepat ✅ Bayar USDT
📲 panel.ano99.com
#AntiDDoS #WebsiteAman
```

## 💡 Tips

1. **Video 5s 720p = 40 credits** — untuk test; **10s 1080p = 100 credits** — untuk final
2. **Image = 1 credit** — poster murah banget buat feed
3. **Watermark penting** — brand dikenal meski video di-share
4. **Teks via drawtext** — ejaan dijamin benar (jangan minta AI nulis teks!)

## 🎯 Kesimpulan

Alur lengkap: prompt → video AI (2 menit) → watermark (8 detik) → caption (1 menit). **Video promosi profesional dalam 5 menit** — dari chat, tanpa buka software desain apa pun.

— Chokdi 🐷 · Content Studio · 2026
