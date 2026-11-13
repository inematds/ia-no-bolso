# Uso responsável

Um modelo "sem censura" é um modelo aberto do qual tiraram o reflexo de recusar. Ele responde quase tudo — e por isso a responsabilidade passa a ser **sua**, não do modelo.

1. **Privado não é anônimo.** Rodar no celular esconde a pergunta das empresas de IA; não muda o que é crime.
2. **Sem recusa também erra.** No nosso teste ele disse "4 g de paracetamol por dose" (o limite é por **dia**). Em saúde, direito e dinheiro, confira com um profissional antes de agir.
3. **Modelo pequeno, conhecimento pequeno.** 41% no MMLU (número do publicador): bom para rascunho, resumo e conversa; fraco para fato exato.
4. **Modelo baixado é arquivo de terceiro.** Baixe só do repositório oficial (`AtomicChat/...` ou `LiquidAI/...`); o `rodar.sh` confere o tamanho exato.
5. **Servidor do PC só para você.** O `rodar.sh` escuta em `127.0.0.1`. Não troque por `0.0.0.0` sem senha e firewall; para acessar de fora, veja o kit [ia-privada-3-niveis](https://inematds.github.io/ia-privada-3-niveis/guia/) (Tailscale).
6. **Menores de idade:** não instale modelo sem censura em aparelho usado por crianças.
7. **Licença:** o modelo segue a LFM Open License v1.0 da Liquid AI. Leia antes de usar em produto.

**Quando NÃO usar o sem censura:** se a versão normal responde, use a normal (`LiquidAI/LFM3-1.7B-GGUF`). Só vá para a sem censura quando a normal recusar uma pergunta legítima.
