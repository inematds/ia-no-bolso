#!/usr/bin/env python3
"""Testes do kit (sem rede, sem modelo): python3 kit/testes/run.py"""
import json, os, subprocess, sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)
import escolher, medir  # noqa: E402

ok = falhas = 0


def t(nome, cond):
    global ok, falhas
    if cond:
        ok += 1
    else:
        falhas += 1
        print('FALHOU:', nome)


d = escolher.carregar()
t('modelos.json tem 2 arquivos', len(d['arquivos']) == 2)
t('tamanhos batem com bytes', all(abs(a['gb'] - a['bytes'] / 1e9) < 0.01 for a in d['arquivos']))
t('modelo marcado só texto', d['modelo']['so_texto'] is True)
r = escolher.escolher('iphone', 8)
t('iphone 8 GB -> Q6', r['veredito'] == 'sim' and 'Q6_K' in r['arquivo']['nome'])
r = escolher.escolher('iphone', 3)
t('iphone 3 GB -> Q4', r['veredito'] == 'sim' and 'Q4_K_M' in r['arquivo']['nome'])
r = escolher.escolher('android', 2)
t('android 2 GB -> não', r['veredito'] == 'nao' and r['reserva'])
r = escolher.escolher('android', 6)
t('android sempre avisa que não foi confirmado', any('Android' in a for a in r['avisos']))
r = escolher.escolher('iphone', 8, livre=1.2)
t('pouco espaço livre -> sem arquivo', r['veredito'] == 'nao')
r = escolher.escolher('iphone', 8, livre=1.8)
t('espaço médio -> Q4', r['veredito'] == 'sim' and 'Q4_K_M' in r['arquivo']['nome'])
r = escolher.escolher('pc', 3.5)
t('pc 3,5 GB -> Q4 (folga 2 GB)', r['veredito'] == 'sim' and 'Q4_K_M' in r['arquivo']['nome'])
t('contexto 8192 com 16 GB', escolher.escolher('pc', 16)['contexto'] == 8192)
for ruim in (('windows', 8), ('iphone', 0)):
    try:
        escolher.escolher(*ruim); t(f'recusa {ruim}', False)
    except ValueError:
        t(f'recusa {ruim}', True)
t('medir: aceita local', medir.so_local('http://127.0.0.1:18431') and medir.so_local('http://localhost:8080'))
t('medir: recusa externo', not medir.so_local('https://api.exemplo.com'))
t('medir: detecta recusa', medir.recusou('Desculpe, mas não posso ajudar com isso.'))
t('medir: resposta normal não é recusa', not medir.recusou('Use o comando kill -9 com o PID.'))
s = medir.resumo([{'tok_s': 10, 'recusou': False, 'fim': 'stop'}, {'tok_s': 20, 'recusou': True, 'fim': 'length'}])
t('medir: resumo', s == {'perguntas': 2, 'tok_s_medio': 15.0, 'recusas': 1, 'cortadas': 1})
p = subprocess.run([sys.executable, os.path.join(KIT, 'medir.py'), '--url', 'https://exemplo.com'], capture_output=True, text=True)
t('medir CLI recusa URL externa', p.returncode == 1 and 'recusado' in p.stdout)
p = subprocess.run([sys.executable, os.path.join(KIT, 'escolher.py'), '--sistema', 'iphone', '--ram', '6'], capture_output=True, text=True)
t('escolher CLI iphone 6 GB', p.returncode == 0 and 'SIM' in p.stdout)
pergs = json.load(open(os.path.join(KIT, 'provas', 'perguntas.json'), encoding='utf-8'))
t('provas: 5 perguntas com id único', len(pergs) == 5 and len({x['id'] for x in pergs}) == 5)
sh = open(os.path.join(KIT, 'pc', 'rodar.sh'), encoding='utf-8').read()
t('rodar.sh só no loopback', '--host 127.0.0.1' in sh and '0.0.0.0' not in sh)
t('rodar.sh confere tamanho', 'BYTES' in sh and 'stat -c %s' in sh)
print(f'{ok} ok, {falhas} falha(s)')
sys.exit(1 if falhas else 0)
