#!/usr/bin/env python3
"""Meu celular aguenta? — diz qual arquivo do modelo baixar, em qual app e com qual contexto.

Uso:
  python3 kit/escolher.py --sistema iphone --ram 8
  python3 kit/escolher.py --sistema android --ram 6 --livre 4
  python3 kit/escolher.py --sistema pc --ram 16

Sem internet, sem dependência. Os tamanhos vêm de kit/modelos.json (conferidos no Hugging Face em 13/11/2026).
"""
import argparse, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))


def carregar():
    with open(os.path.join(AQUI, 'modelos.json'), encoding='utf-8') as f:
        return json.load(f)


def escolher(sistema, ram, livre=None, dados=None):
    """ESTIMATIVA (regra de folga, não medida em celular). Devolve dict com veredito, arquivo, app, contexto e avisos. Regra: o arquivo inteiro precisa caber
    na memória com folga para o sistema e o app (arquivo + 1,5 GB no celular, + 2 GB no PC)."""
    dados = dados or carregar()
    sistema = sistema.lower()
    if sistema not in ('iphone', 'android', 'pc'):
        raise ValueError('sistema deve ser iphone, android ou pc')
    if ram <= 0:
        raise ValueError('ram deve ser maior que zero')
    folga = 2.0 if sistema == 'pc' else 1.5
    avisos = []
    escolhido = None
    for q in sorted(dados['arquivos'], key=lambda a: -a['gb']):  # maior que couber
        if q['gb'] + folga <= ram:
            escolhido = q
            break
    if livre is not None and escolhido and livre < escolhido['gb'] + 0.5:
        menor = min(dados['arquivos'], key=lambda a: a['gb'])
        if livre >= menor['gb'] + 0.5:
            escolhido = menor
            avisos.append('pouco espaço livre: fique com a versão menor')
        else:
            escolhido = None
            avisos.append(f"libere espaço: precisa de ~{menor['gb'] + 0.5:.1f} GB livres")
    app = dados['apps'][sistema]
    if sistema == 'android':
        avisos.append('Android: este arquivo LFM3 ainda não foi confirmado em app de Android; teste e, se não carregar, '
                      'use o modelo reserva (kit/modelos.json → reserva)')
    if sistema == 'iphone':
        avisos.append('iPhone: o app pede iOS 18 ou mais')
    contexto = 4096 if ram < 12 else 8192
    if escolhido is None:
        return {'veredito': 'nao', 'arquivo': None, 'app': app, 'contexto': None,
                'reserva': dados['reserva'], 'avisos': avisos or [f'com {ram} GB de memória, prefira o modelo reserva']}
    return {'veredito': 'sim', 'arquivo': escolhido, 'app': app, 'contexto': contexto,
            'reserva': dados['reserva'], 'avisos': avisos}


def main(argv=None):
    ap = argparse.ArgumentParser(description='Meu celular aguenta a IA sem censura offline?')
    ap.add_argument('--sistema', required=True, choices=['iphone', 'android', 'pc'])
    ap.add_argument('--ram', type=float, required=True, help='memória do aparelho em GB (Ajustes → Sobre)')
    ap.add_argument('--livre', type=float, help='espaço livre de armazenamento em GB (opcional)')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args(argv)
    r = escolher(a.sistema, a.ram, a.livre)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    if r['veredito'] == 'sim':
        q = r['arquivo']
        print(f"SIM (estimativa pela memória; confirme no aparelho). Baixe {q['nome']} ({q['gb']:.2f} GB).")
        print(f"App: {r['app']['nome']} — {r['app']['onde']}")
        print(f"Contexto: {r['contexto']} tokens.")
    else:
        print(f"NÃO com este modelo. Reserva: {r['reserva']['nome']} ({r['reserva']['gb']} GB).")
    for av in r['avisos']:
        print('Aviso:', av)
    return 0 if r['veredito'] == 'sim' else 2


if __name__ == '__main__':
    sys.exit(main())
