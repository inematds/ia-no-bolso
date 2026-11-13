#!/usr/bin/env bash
# Roda a IA sem censura no PC, offline, só para você (127.0.0.1). Testado no Linux em 13/11/2026.
#   bash kit/pc/rodar.sh            # compila o llama.cpp (só CPU), baixa o Q4 uma vez e sobe o servidor
#   QUANT=Q6_K bash kit/pc/rodar.sh # versão maior
#   PORTA=18431 THREADS=4 bash kit/pc/rodar.sh
# Depois do download, desligue a internet: continua funcionando. Chat em http://127.0.0.1:$PORTA
set -euo pipefail
DIR=${IA_NO_BOLSO_DIR:-$HOME/.local/share/ia-no-bolso}
QUANT=${QUANT:-Q4_K_M}
PORTA=${PORTA:-18431}
THREADS=${THREADS:-4}
CTX=${CTX:-4096}
REPO=AtomicChat/LFM3-1.7B-Uncensored-GGUF
ARQ=LFM3-1.7B-Uncensored-AD-$QUANT.gguf
case $QUANT in
  Q4_K_M) BYTES=1132208000 ;;
  Q6_K)   BYTES=1587969920 ;;
  *) echo "QUANT deve ser Q4_K_M ou Q6_K"; exit 1 ;;
esac
mkdir -p "$DIR"

# 1) llama.cpp recente (precisa do suporte a LFM3; Ollama antigo recusa o arquivo)
if [ ! -x "$DIR/llama.cpp/build/bin/llama-server" ]; then
  command -v cmake >/dev/null || { echo "instale cmake e um compilador C++ (ex.: sudo apt install cmake build-essential)"; exit 1; }
  [ -d "$DIR/llama.cpp" ] || git clone --depth 1 https://github.com/ggml-org/llama.cpp "$DIR/llama.cpp"
  cmake -S "$DIR/llama.cpp" -B "$DIR/llama.cpp/build" -DGGML_CUDA=OFF -DLLAMA_CURL=OFF -DCMAKE_BUILD_TYPE=Release
  cmake --build "$DIR/llama.cpp/build" -j "$(nproc)" --target llama-server llama-bench
fi

# 2) modelo (uma vez só; confere o tamanho exato)
if [ "$(stat -c %s "$DIR/$ARQ" 2>/dev/null || echo 0)" != "$BYTES" ]; then
  echo "baixando $ARQ (~$((BYTES / 1000000)) MB)…"
  curl -L --fail -C - -o "$DIR/$ARQ" "https://huggingface.co/$REPO/resolve/main/$ARQ"
  [ "$(stat -c %s "$DIR/$ARQ")" = "$BYTES" ] || { echo "tamanho diferente do esperado: apague $DIR/$ARQ e rode de novo"; exit 1; }
fi

# 3) porta livre e só no loopback
if ss -ltn 2>/dev/null | grep -q ":$PORTA "; then echo "porta $PORTA ocupada: PORTA=<outra> bash $0"; exit 1; fi
echo "IA no bolso: http://127.0.0.1:$PORTA  (Ctrl+C para parar; nada sai desta máquina)"
exec "$DIR/llama.cpp/build/bin/llama-server" -m "$DIR/$ARQ" -t "$THREADS" -c "$CTX" --host 127.0.0.1 --port "$PORTA"
