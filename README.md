# IA no bolso

[![IA no bolso](guia/assets/banner.jpg)](https://inematds.github.io/ia-no-bolso/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Quando você usa a IA de um aplicativo comum, a pergunta sai do celular e vai para o servidor de uma empresa. A **IA no bolso** é o contrário: um modelo pequeno e aberto (o LFM3 1.7B, numa versão sem censura) que você baixa uma vez e que roda dentro do aparelho, até no modo avião. Serve para quem quer privacidade e não quer ouvir "não posso responder" para pergunta normal. Este guia mostra se o seu celular aguenta, o passo a passo no iPhone e no Android, e um kit grátis para rodar o mesmo modelo no computador.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/ia-no-bolso/guia/**

📱 **Testar no celular sem instalar nada:** https://inematds.github.io/ia-no-bolso/celular/ — abre no navegador, baixa 1,1 GB uma vez e depois funciona no modo avião (testado no Chrome simulando Android; celular de verdade ainda não).

---

**Tudo o que você pergunta para a IA do celular vai parar no computador de uma empresa. E às vezes ela ainda se nega a responder uma pergunta normal.**

A **IA no bolso** é uma IA que mora dentro do seu celular: funciona no modo avião, não manda nada para a nuvem e não recusa pergunta normal. Este kit diz se o seu aparelho aguenta, mostra o passo a passo no iPhone e no Android, roda o mesmo modelo no seu computador só para você e mede a velocidade e as recusas com as suas perguntas.

## O modelo

| | |
|---|---|
| Modelo | **LFM3 1.7B**, da Liquid AI (aberto, licença LFM Open License v1.0) |
| Versão sem censura | [`AtomicChat/LFM3-1.7B-Uncensored-GGUF`](https://huggingface.co/AtomicChat/LFM3-1.7B-Uncensored-GGUF) |
| Tamanho | **1,13 GB** (Q4_K_M) ou 1,59 GB (Q6_K) |
| O que faz | **só texto** (o repositório não traz a parte de imagem) |
| Segundo o publicador | recusas a pedidos nocivos 61,7% → 0%; falsas recusas 5,2% → 0%; MMLU 41,0% → 41,0% |

O kit **não** traz o arquivo do modelo: ele é baixado direto do Hugging Face. Leia a licença da Liquid AI antes de usar.

## Em 1 minuto

```bash
git clone https://github.com/inematds/ia-no-bolso && cd ia-no-bolso
python3 kit/escolher.py --sistema iphone --ram 8      # meu celular aguenta? qual arquivo?
bash kit/pc/rodar.sh                                   # no PC: compila o llama.cpp, baixa 1,1 GB, sobe em 127.0.0.1:18431
python3 kit/medir.py                                   # velocidade + recusas com 5 perguntas normais
python3 kit/testes/run.py                              # 23 testes do kit, sem rede
```

## No celular (passo a passo completo em [kit/CELULAR.md](kit/CELULAR.md))

- **iPhone** — app **OnDevice: Local AI Studio** (App Store, iOS 18+). Modelos → busca do Hugging Face → `atomic chat` → **LFM3-1.7B-Uncensored-GGUF** → baixar → carregar → perguntar. Funcionou num iPhone 16 (26 tokens/s num 16 Pro Max, no teste mostrado). O PocketPal **não** carregou esse arquivo.
- **Android** — app **Layla** (importa GGUF). **Ainda não confirmado** com este arquivo: teste. Se não abrir, use a reserva: `LiquidAI/LFM3-1.7B-GGUF` (versão normal, com travas).
- **Prova de privacidade:** depois do download, ligue o **modo avião** e pergunte. Se responde, está tudo no aparelho.

## O que medimos (13/11/2026)

Sem celular de teste, rodamos no PC **só com o processador, 4 núcleos** (o mais perto de um celular), com a máquina ocupada:

| Medida | Resultado |
|---|---|
| Ollama 0.33.2 | **não abriu** o arquivo ("failed to validate GGUF") |
| llama.cpp `5676dfb` (13/11) | abriu |
| Geração (`llama-bench`) | ~14–21 tokens/s |
| `kit/medir.py` (5 perguntas normais) | média **19,8 tokens/s**, **0 recusas** |
| Detalhe | ele **pensa em inglês** antes de responder: resposta longa leva 1–3 min |

> ⚠️ **O achado mais importante:** perguntamos a dose máxima de paracetamol duas vezes. Na 1ª ele respondeu **"4 g por dose"** (errado e perigoso: o limite usual é 4 g **por dia**). Na 2ª acertou. Modelo pequeno é sorteio: **em saúde, direito e dinheiro, confira com um profissional.** Respostas completas em [exemplo/](exemplo/).

## Arquivos

| Arquivo | Para quê |
|---|---|
| `kit/escolher.py` | Meu celular aguenta? Diz arquivo, app e contexto pela memória e espaço livre |
| `kit/pc/rodar.sh` | Compila o llama.cpp (só CPU), baixa o modelo conferindo o tamanho, sobe **só em 127.0.0.1** |
| `kit/medir.py` | Mede tokens/s, tempo e recusas; recusa falar com endereço que não seja local |
| `kit/provas/perguntas.json` | 5 perguntas normais (inclui 2 de "falsa recusa") — troque pelas suas |
| `kit/modelos.json` | Arquivos, tamanhos, apps e reserva, conferidos em 13/11/2026 |
| `kit/CELULAR.md` | Passo a passo do iPhone e do Android, com a prova do modo avião |
| `kit/USO-RESPONSAVEL.md` | Regras: sem censura = a responsabilidade é sua |
| `exemplo/` | Nossas medidas e respostas brutas |

## Kits irmãos

- [ia-privada-3-niveis](https://inematds.github.io/ia-privada-3-niveis/guia/) — IA privada no computador (normal ou sem censura), acessível de qualquer lugar pelo Tailscale.
- [ia-sem-censura-defensiva](https://github.com/inematds/ia-sem-censura-defensiva) — usar modelo sem censura para se defender, não para atacar.
- [provedores-semcensura](https://github.com/inematds/provedores-semcensura) — quando não dá para rodar local.

Mais kits grátis em **[inema.club](https://inema.club)**.

## Licença

Kit: MIT. Modelo: LFM Open License v1.0 (Liquid AI) — não incluído neste repositório.
