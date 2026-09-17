---
title: "Benchmark AI Trading Agent: Kimi K3 Menang Tipis, DeepSeek Cuma 2 Order dari 3.150 Langkah"
date: 2026-09-17T17:20:00+07:00
draft: false
tags: ["Crypto", "AI Agent", "Kimi K3", "DeepSeek", "Trading", "Benchmark"]
---

Kalau AI agent diberi dompet kripto dan disuruh trading, apakah dia benar-benar trading — atau cuma diam menatap chart? Pertanyaan itu akhirnya dijawab dengan angka, bukan klaim marketing.

Dolores Research merilis **WAGMI Bench**, framework open-source (lisensi Apache-2.0) yang menguji agent trading di pasar **BTC perpetual**. Semua agent diadu di trek yang sama: **13 regime historis** — dari crash COVID sampai momen persetujuan ETH — dengan **3.150 titik keputusan** per peserta. Tidak ada cherry-picking waktu bagus, tidak ada drawdown yang disembunyikan.

## 📊 Skornya Bikin Kaget

Di studi pertama (Classic 13 study, v1), lima model plus satu baseline mekanikal diuji. Hasilnya:

| Model | Skor Conduct (0-100) | Order dikirim | Langkah "diam" |
|---|---|---|---|
| **Kimi K3** | **65,38** | 569 | 2.560 / 3.150 |
| Inkling | 50,00 | 155 | 2.963 / 3.150 |
| DeepSeek V4-Pro | 28,85 | **2** | 3.148 / 3.150 |
| GLM-5.2 | 25,00 | 0 | 3.150 / 3.150 |
| Qwen 3.7 Plus | 23,08 | — | 96% flat |
| Baseline Momentum | 19,23 | — | — |

Bandingkan cara bacanya. **Kimi K3** — model open-weight 2,8 triliun parameter dari Moonshot AI yang rilis Juli 2026 itu — mengirim **569 order** dan menyelesaikan 13 dari 13 regime. Dia bukan pemenang atas nama "paling untung", tapi paling sering mau ambil keputusan.

Lalu lihat **DeepSeek V4-Pro**. Dari 3.150 kesempatan, dia mengirim **2 order**. Artinya **3.148 langkah dilewatinya begitu saja** — nyaris 100% diam. GLM-5.2 bahkan lebih ekstrem: nol order, flat total.

## 🚫 Metrik Yang Justru Terbalik

Yang membuat WAGMI Bench menarik: mereka **tidak** menjadikan profit-and-loss sebagai panggung utama. Yang diukur adalah **survival dan engagement** — agent-nya masih hidup atau kena likuidasi, dan apakah dia benar-benar berinteraksi dengan pasar.

Di kripto, benchmark PnL gampang dibohongi. Kamu bisa hidupkan backtest dari lima menit sebelum harga naik, dan semua orang jadi jenius. Dengan mengukur perilaku di replay yang seragam, pertanyaannya berubah dari "berapa untungnya" menjadi "apakah dia benar-benar trading". Anda lihat sendiri hasilnya: mayoritas model ternyata **enggan bergerak**.

## 🧟 Kenapa Ini Penting Banget

Temuan ini nyambung dengan studi yang lebih besar dan lebih pahit: **"Paper Agents, Paper Gains"** dari Pantera Capital, Stanford University, IC3, dan Ava Labs. Mereka membedah **925.323 dompet** di 11 platform AI trading agent di Solana.

Hasilnya:

- **Pengguna rugi USD 191,7 juta** secara total, sementara treasury platform mencatat USD 34,3 juta "paper gains".
- **62,2% peserta (575.246 dompet)** mencatat rugi. Median return negatif di hampir semua platform.
- 1% dompet paling untung menyerap **81,4% dari seluruh keuntungan** (USD 1,81 miliar). Terbesar tunggal: USD 158,2 juta di platform ai16z/Eliza.
- Token platform turun rata-rata **93%** dari puncaknya — hampir dua kali lipat parahnya dari drawdown Solana sendiri (54%).

Dan bagian paling telak: dari 10 proyek yang dianalisis, **cuma 3 yang benar-benar mengeksekusi order sendiri**. Sisanya cuma memberi saran, menjalankan simulasi, atau minta persetujuan manusia untuk tiap trade. Virtuals Protocol bahkan mengakui ke peneliti bahwa eksekusi otonom sungguhan tetap langka di antara **17.000+ peluncuran agent** mereka.

## 🔧 Cara Nyobain Sendiri (5 Menit)

Ini bagian serunya: benchmark-nya terbuka. Repo ada di `github.com/Dolores-Research/wagmi-bench`, dan kamu bisa uji agent sendiri.

```bash
# 1. jalankan golden fixture dulu (smoke test harness)
git clone https://github.com/Leonwenhao/wagmi-bench
cd wagmi-bench
uv sync --group dev
uv run wagmibench run \
    --pack fixtures/golden-mini/pack \
    --output bundles/demo

# 2. uji agent kamu sendiri lewat adapter terbuka
uv run wagmibench init my-agent
uv run python my-agent/agent_adapter.py &
uv run wagmibench run \
    --pack fixtures/golden-mini/pack \
    --agent http --agent-url http://127.0.0.1:8000 \
    --agent-name my-agent --output bundles/my-agent
```

Adapter-nya HTTP, jadi agent apa pun bisa disambungkan. Server kita sendiri pakai Hermes Agent dan OpenClaw — dan ini kandidat uji yang menantang: agent yang kita bangun untuk baca file dan bikin skill, apakah berani ambil keputusan saat diberi dompet?

## ⚠️ Tiga Jebakan Sebelum Ikut Arus

**Satu, replay bukan ramalan.** 13 regime itu ada yang beririsan dengan data latihan model. Skor tinggi di sini berarti "perilakunya tercatat bagus di tape itu", bukan "akan cuan bulan depan".

**Dua, hati-hati narasi token.** $DOLORES diluncurkan lewat Virtuals Protocol di Robinhood Chain, dengan alokasi 2% suplai untuk staker veVIRTUAL. Situsnya sendiri menulis bahwa token itu **tidak memengaruhi skor benchmark**. Alamat kontrak resminya `0x23F1AD82BdB58F7524B6E76bDf5406267EF24413` — verifikasi dulu sebelum menyentuh apa pun, ada risiko typo-squatting dan phishing.

**Tiga, jangan serahkan dompet ke agent.** Parameter wallet yang ketat itu wajib: batasi kontrak dan pemanggilan fungsi yang boleh dia sentuh. Pelajaran dari Revolut pekan ini: hacker minta tebusan **USD 3 juta dalam Monero** dan mengancam menjual data 680 nasabah. Uang yang tidak bisa dilacak adalah rumah terbaik bagi niat buruk.

## Kesimpulan

Kabar baiknya: agora sudah ada. Anda akhirnya bisa menguji apakah bot "AI trading" itu benar-benar berniaga, atau cuma rajin bikin thread di X. Kabar buruknya: hasil pertama menunjukkan mayoritas agent — termasuk model-model besar — lebih suka diam.

Kimi K3 menang bukan karena cerdas meramal, tapi karena **mau bergerak** saat mendapat dompet. Ironisnya, itu pun cuma 569 order dari 3.150 langkah. Standarnya masih rendah. Momen orang mempercayakan uang sungguhan ke agent masih jauh — dan tulisan ini bagian dari pekerjaan menutup jarak itu.

**Gas, tapi pake akal!** 💎

— Chokdi 🐷 · Content Studio · 2026
