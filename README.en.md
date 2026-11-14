# AI in Your Pocket

[![AI in Your Pocket](guia/assets/banner-en.jpg)](https://inematds.github.io/ia-no-bolso/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

When you use AI in a regular app, your question leaves your phone and goes to a company’s server. **AI in your pocket** works the other way around: it’s a small, open model (LFM3 1.7B, in an uncensored version) that you download once and run on your device, even in airplane mode. It’s for people who want privacy and don’t want to hear “I can’t answer that” in response to ordinary questions. This guide shows whether your phone can handle it, gives step-by-step instructions for iPhone and Android, and includes a free kit for running the same model on your computer.

## 📖 User guide

Full guide (landing + step by step): **https://inematds.github.io/ia-no-bolso/guia/en/**

📱 **Try it on your phone, nothing to install:** https://inematds.github.io/ia-no-bolso/celular/?lang=en — opens in the browser, downloads 1.1 GB once and then works in airplane mode (tested in Chrome emulating Android and on a real phone on Nov 14, 2026). Tip: after it starts, use "Add to Home screen" and it becomes an app with an icon.

---

**Everything you ask your phone’s AI gets sent to a company’s computer. And sometimes it even refuses to answer a normal question.**

**AI in Your Pocket** is an AI that lives on your phone: it works in airplane mode, sends nothing to the cloud, and doesn’t refuse normal questions. This kit tells you whether your device can handle it, shows you the steps for iPhone and Android, runs the same model on your computer for your use only, and measures speed and refusals with your questions.


## The model

| | |
|---|---|
| Model | **LFM3 1.7B**, by Liquid AI (open, LFM Open License v1.0) |
| Uncensored version | [`AtomicChat/LFM3-1.7B-Uncensored-GGUF`](https://huggingface.co/AtomicChat/LFM3-1.7B-Uncensored-GGUF) |
| Size | **1.13 GB** (Q4_K_M) or 1.59 GB (Q6_K) |
| What it does | **text only** (the repository doesn’t include the image component) |
| According to the publisher | refusals of harmful requests 61.7% → 0%; false refusals 5.2% → 0%; MMLU 41.0% → 41.0% |

The kit does **not** include the model file: it is downloaded directly from Hugging Face. Read Liquid AI’s license before using it.

## In 1 minute

```bash
git clone https://github.com/inematds/ia-no-bolso && cd ia-no-bolso
python3 kit/escolher.py --sistema iphone --ram 8      # can my phone handle it? which file?
bash kit/pc/rodar.sh                                   # on PC: compiles llama.cpp, downloads 1.1 GB, starts at 127.0.0.1:18431
python3 kit/medir.py                                   # speed + refusals with 5 normal questions
python3 kit/testes/run.py                              # 23 kit tests, no network
```

## On your phone (full step-by-step guide in [kit/CELULAR.md](kit/CELULAR.md))

- **iPhone** — **OnDevice: Local AI Studio** app (App Store, iOS 18+). Models → search Hugging Face → `atomic chat` → **LFM3-1.7B-Uncensored-GGUF** → download → load → ask. It worked on an iPhone 16 (26 tokens/s on a 16 Pro Max, in the test shown). PocketPal did **not** load this file.
- **Android** — **Layla** app (imports GGUF). **Not yet confirmed** with this file: test it. If it won’t open, use the fallback: `LiquidAI/LFM3-1.7B-GGUF` (regular version, with safeguards).
- **Privacy proof:** after downloading, turn on **airplane mode** and ask a question. If it answers, everything is on the device.

## What we measured (13/11/2026)

Without a test phone, we ran it on a PC **using only the processor, 4 cores** (the closest thing to a phone), while the machine was busy:

| Measurement | Result |
|---|---|
| Ollama 0.33.2 | **didn’t open** the file ("failed to validate GGUF") |
| llama.cpp `5676dfb` (13/11) | opened it |
| Generation (`llama-bench`) | ~14–21 tokens/s |
| `kit/medir.py` (5 normal questions) | average **19.8 tokens/s**, **0 refusals** |
| Detail | it **thinks in English** before answering: a long answer takes 1–3 min |

> ⚠️ **The most important finding:** we asked for the maximum paracetamol dose twice. The first time, it answered **"4 g per dose"** (wrong and dangerous: the usual limit is 4 g **per day**). The second time, it got it right. Small models are a gamble: **for health, legal, and financial matters, check with a professional.** Full answers in [exemplo/](exemplo/).

## Files

| File | What it’s for |
|---|---|
| `kit/escolher.py` | Can my phone handle it? Recommends a file, app, and context based on memory and free space |
| `kit/pc/rodar.sh` | Compiles llama.cpp (CPU only), downloads the model and checks its size, starts it **only on 127.0.0.1** |
| `kit/medir.py` | Measures tokens/s, time, and refusals; refuses to connect to any non-local address |
| `kit/provas/perguntas.json` | 5 normal questions (including 2 about “false refusals”) — replace them with yours |
| `kit/modelos.json` | Files, sizes, apps, and fallback, checked on 13/11/2026 |
| `kit/CELULAR.md` | iPhone and Android step-by-step guide, with the airplane mode proof |
| `kit/USO-RESPONSAVEL.md` | Rules: uncensored means you’re responsible |
| `exemplo/` | Our measurements and raw answers |

## Related kits

- [ia-privada-3-niveis](https://inematds.github.io/ia-privada-3-niveis/guia/) — private AI on your computer (regular or uncensored), accessible from anywhere through Tailscale.
- [ia-sem-censura-defensiva](https://github.com/inematds/ia-sem-censura-defensiva) — use an uncensored model to defend yourself, not to attack.
- [provedores-semcensura](https://github.com/inematds/provedores-semcensura) — when you can’t run it locally.

More free kits at **[inema.club](https://inema.club)**.

## License

Kit: MIT. Model: LFM Open License v1.0 (Liquid AI) — not included in this repository.