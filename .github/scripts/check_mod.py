"""Verificacao estatica que roda sem a pasta do jogo (GitHub Actions e PC).

Confere so o que depende dos arquivos do mod:
- BOM: todo .txt, .yml e .gui com UTF-8 BOM; descriptor.mod sem BOM.
- Chaves { } balanceadas em cada script (ignora comentarios e strings).
- Localizacao: cabecalho l_<idioma>: e nenhuma chave repetida no mesmo idioma.
- Decisao de teste: arquivos de TEST_FILES com linha ativa (nao comentada).

Uso: python .github/scripts/check_mod.py [pasta_do_mod] [--publicacao]
Com --publicacao, decisao de teste ativa e FALHA; sem ele, e AVISO.
Saida: exit code 1 se houver FALHA.
"""
import os
import re
import sys

BOM = b'\xef\xbb\xbf'
SKIP_DIRS = {'.git', '.github', '.vscode'}
TEST_FILES = [
    'common/decisions/ci_test_decisions.txt',
    'common/scripted_effects/ci_test_effects.txt',
    'localization/english/ci_test_l_english.yml',
]
LOC_KEY = re.compile(r'^\s*([A-Za-z0-9_.\-]+):\d*\s*"')
LOC_HEADER = re.compile(r'^l_[a-z_]+:\s*$')

fails = []
warns = []


def fail(msg):
    fails.append(msg)
    print('FALHA:', msg)


def warn(msg):
    warns.append(msg)
    print('AVISO:', msg)


def mod_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            yield os.path.relpath(full, root).replace(os.sep, '/'), full


def check_bom(rel, raw):
    if rel == 'descriptor.mod':
        if raw.startswith(BOM):
            fail(f'{rel}: descriptor.mod deve ficar sem BOM')
    elif rel.endswith(('.txt', '.yml', '.gui')) and not raw.startswith(BOM):
        fail(f'{rel}: sem UTF-8 BOM')


def check_braces(rel, text):
    depth = 0
    line = 1
    in_str = False
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == '\n':
            line += 1
            in_str = False  # strings do CK3 nao atravessam linhas
        elif in_str:
            if c == '\\':
                i += 1
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == '#':
            j = text.find('\n', i)
            i = n if j < 0 else j
            continue
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth < 0:
                fail(f'{rel}:{line}: "}}" sem "{{" correspondente')
                return
        i += 1
    if depth > 0:
        fail(f'{rel}: {depth} "{{" sem fechar no fim do arquivo')


def check_loc(rel, text, seen):
    lines = text.splitlines()
    first = next((l.strip() for l in lines if l.strip() and not l.lstrip().startswith('#')), '')
    if not LOC_HEADER.match(first):
        fail(f'{rel}: primeira linha deve ser o cabecalho l_<idioma>: (achei {first[:40]!r})')
        return
    lang = first[:-1]
    keys = seen.setdefault(lang, {})
    for num, l in enumerate(lines, 1):
        m = LOC_KEY.match(l)
        if not m:
            continue
        key = m.group(1)
        if key in keys and keys[key] != (rel, num):
            fail(f'{rel}:{num}: chave {key} repetida (ja em {keys[key][0]}:{keys[key][1]})')
        else:
            keys[key] = (rel, num)


def check_test_decision(root, publicacao):
    for rel in TEST_FILES:
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            continue
        text = open(path, encoding='utf-8-sig', errors='replace').read()
        active = [l for l in text.splitlines()
                  if l.strip() and not l.lstrip().startswith('#') and not LOC_HEADER.match(l.strip())]
        if active:
            msg = f'{rel}: decisao de teste ativa ({len(active)} linhas sem comentario); comente antes de publicar'
            (fail if publicacao else warn)(msg)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    publicacao = '--publicacao' in sys.argv
    root = os.path.abspath(args[0] if args else '.')
    seen = {}
    n = 0
    for rel, full in mod_files(root):
        if not rel.endswith(('.txt', '.yml', '.gui', '.mod')):
            continue
        n += 1
        raw = open(full, 'rb').read()
        check_bom(rel, raw)
        text = raw.decode('utf-8-sig', errors='replace')
        if rel.endswith(('.txt', '.gui')):
            check_braces(rel, text)
        elif rel.endswith('.yml') and rel.startswith('localization/'):
            check_loc(rel, text, seen)
    check_test_decision(root, publicacao)
    print(f'{n} arquivos conferidos: {len(fails)} falhas, {len(warns)} avisos')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
