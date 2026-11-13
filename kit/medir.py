#!/usr/bin/env python3
"""Mede a sua IA local: velocidade (tokens/s), tempo até a resposta e se ela recusa pergunta normal.

Uso (com o kit/pc/rodar.sh no ar):
  python3 kit/medir.py                       # usa http://127.0.0.1:18431 e kit/provas/perguntas.json
  python3 kit/medir.py --url http://127.0.0.1:8080 --saida minhas-medidas.json

Só fala com endereço local (127.0.0.1/localhost): recusa URL de fora, para a medida não vazar nada.
Funciona com qualquer servidor compatível com /v1/chat/completions (llama-server, LM Studio, Ollama).
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
RECUSA = ('não posso ajudar', 'nao posso ajudar', 'não posso fornecer', "i can't help", 'i cannot help',
          'não é apropriado', 'sorry, but i', 'desculpe, mas não')


def so_local(url):
    h = urllib.parse.urlparse(url).hostname or ''
    return h in ('127.0.0.1', 'localhost', '::1')


def recusou(texto):
    t = (texto or '').lower()
    return any(r in t for r in RECUSA)


def perguntar(url, pergunta, max_tokens=1800):
    corpo = json.dumps({'messages': [{'role': 'user', 'content': pergunta}],
                        'max_tokens': max_tokens, 'temperature': 0.3}).encode()
    req = urllib.request.Request(url.rstrip('/') + '/v1/chat/completions', data=corpo,
                                 headers={'Content-Type': 'application/json'})
    t0 = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=900))
    seg = time.time() - t0
    m = r['choices'][0]['message']
    tm = r.get('timings', {})
    toks = tm.get('predicted_n') or r.get('usage', {}).get('completion_tokens')
    tps = tm.get('predicted_per_second') or (toks / seg if toks else None)
    return {'resposta': m.get('content') or '', 'pensou_chars': len(m.get('reasoning_content') or ''),
            'fim': r['choices'][0].get('finish_reason'), 'tokens': toks,
            'tok_s': round(tps, 1) if tps else None, 'segundos': round(seg, 1)}


def resumo(res):
    v = [r['tok_s'] for r in res if r.get('tok_s')]
    return {'perguntas': len(res), 'tok_s_medio': round(sum(v) / len(v), 1) if v else None,
            'recusas': sum(1 for r in res if r['recusou']),
            'cortadas': sum(1 for r in res if r.get('fim') == 'length')}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--url', default='http://127.0.0.1:18431')
    ap.add_argument('--perguntas', default=os.path.join(AQUI, 'provas', 'perguntas.json'))
    ap.add_argument('--saida', default='medidas.json')
    a = ap.parse_args(argv)
    if not so_local(a.url):
        print('recusado: o medidor só fala com 127.0.0.1/localhost'); return 1
    perguntas = json.load(open(a.perguntas, encoding='utf-8'))
    res = []
    for p in perguntas:
        r = perguntar(a.url, p['pergunta'])
        r.update(id=p['id'], tipo=p['tipo'], pergunta=p['pergunta'], recusou=recusou(r['resposta']))
        res.append(r)
        print(f"{p['id']:<20} {r['tok_s'] or '?':>6} tok/s  {r['segundos']:>6}s  {'RECUSOU' if r['recusou'] else 'respondeu'}")
    s = resumo(res)
    json.dump({'resumo': s, 'respostas': res}, open(a.saida, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"média {s['tok_s_medio']} tok/s · recusas {s['recusas']}/{s['perguntas']} · cortadas {s['cortadas']} → {a.saida}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
