# IA no bolso — passo a passo no celular

Antes de tudo: `python3 kit/escolher.py --sistema <iphone|android> --ram <GB> --livre <GB>` diz se cabe e qual arquivo baixar.
Sem computador? Regra simples: precisa de **~3 GB de memória** e **~2 GB livres** para a versão Q4 (1,13 GB).

## iPhone (mostrado funcionando num iPhone 16; não testado por nós)

1. **Instale** o app **OnDevice: Local AI Studio** na App Store. Pede **iOS 18 ou mais**.
2. **Primeira abertura:** o app pede para escolher um modelo. Escolha qualquer um, só para passar da tela.
3. **Modelos → busca do Hugging Face** (campo "Search online · Hugging Face") e digite **`atomic chat`**.
4. Toque em **LFM3-1.7B-Uncensored-GGUF** (publicador AtomicChat) e em **baixar**. São ~1,1 GB: use Wi-Fi.
5. Quando terminar, volte ao **assistente**, escolha o modelo baixado e mande uma pergunta.
6. Se o app mostrar "contexto", comece em **4.096**; baixe se faltar memória.

O que já se sabe: o **PocketPal falhou** ao carregar este arquivo, e o app da própria AtomicChat também não funcionou com ele (no teste mostrado). Use o OnDevice.

## Android (ainda não confirmado com este arquivo)

1. Instale o **Layla** (Play Store). Ele importa arquivos GGUF.
2. Baixe no navegador o arquivo `LFM3-1.7B-Uncensored-AD-Q4_K_M.gguf` em
   https://huggingface.co/AtomicChat/LFM3-1.7B-Uncensored-GGUF/tree/main
3. No Layla, importe o arquivo baixado e abra um chat.
4. **Não abriu?** O app ainda não tem o motor novo (LFM3 é recente). Use a reserva:
   `LiquidAI/LFM3-1.7B-GGUF` → `LFM3-1.7B-Q4_K_M.gguf` (versão normal, com travas de segurança), ou espere a atualização do app.

## A prova de privacidade (faça sempre)

1. Com o modelo carregado, ligue o **modo avião** (Wi-Fi e dados desligados).
2. Pergunte algo. **Se respondeu, a resposta saiu do seu aparelho**, não da nuvem.
3. Se der erro de conexão, o app está usando um servidor: não é IA no bolso.

## O que esperar

- **Velocidade:** 26 tokens/s num iPhone 16 Pro Max (teste mostrado). No nosso PC, só CPU, ~10–20.
- **Ele pensa antes** (em inglês) — a resposta longa demora mais do que parece.
- **Ele erra.** Na pergunta de dose de remédio, errou feio uma vez e acertou na outra. Confira coisa séria.
- **Bateria e calor:** rodar modelo esquenta o celular. Para conversa longa, deixe na tomada.
