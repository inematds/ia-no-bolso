# CLAUDE.md — ia-no-bolso

Kit "IA no bolso": IA sem censura (LFM3 1.7B, AtomicChat) offline no celular e no PC. Guia em `guia/` (PT/EN/ES).
- Commits: autor `inematds <inematds@gmail.com>`. Nunca commitar `.gguf`.
- Testes: `python3 kit/testes/run.py` (sem rede). Fatos e números só os de `exemplo/` e do README (conferidos 13/11/2026).
- Não citar autor/canal/site do vídeo de referência.

## Self-learning

When I correct you, or you catch yourself making a mistake: before continuing, add the lesson as a one-line rule under ## Lessons, so it never happens again.

## Lessons
- celular/: wllama usa WebGPU por padrão (n_gpu_layers 99999) e no celular real aborta ao ligar ("Falhou: abort") — no celular carregar com `n_gpu_layers: 0` e cair para modos mais leves (n_ctx 512, 1 núcleo); a emulação Pixel 7 no PC não pega isso. Teste headless: a página abre em inglês, esperar "Pronta|Ready". (14/11/2026)
- celular/ (página "abre e usa", wllama 3.13 vendorizado): carregar o modelo com `loadModelFromUrl(<resolve/main/arquivo>)`, nunca `loadModelFromHF` — este consulta a API do HF antes do cache e falha no modo avião. No sw.js, `fetch(..., {cache:'no-cache'})`, senão o celular fica com a página velha do cache. (13/11/2026)
- Teste da página: Chrome headless emulando Pixel 7 (playwright-core + ~/.cache/ms-playwright/chromium-1254), com `ctx.setOffline(true)` para a prova do modo avião. Celular de verdade: só o Nei. (13/11/2026)
