# Legio Imperialis

Mod de Crusader Kings III, prefixo `li_`, alvo 1.20.x. Início em 867 com Kensoriel Liphe como aventureiro em Jerusalém, o acampamento Legio Imperialis e o elenco de 35 fundadores, só com conteúdo vanilla. Está parado: cumpriu o papel de banco de testes e serve de base futura para Total Conversions.

**Leia primeiro:** `Meus Mods CK3\Legio Imperialis\ESTADO - Legio.md` (estado atual e onde está cada coisa). Testes, validação e roteiro de playtest ficam em `Meus Mods CK3\Legio Imperialis\`; spec e plano aprovados, em `arquivo\superpowers\` dessa pasta.

## Caminhos

| Recurso | Caminho |
|---|---|
| Mod (este repositório) | `C:\Users\rique\Documents\Paradox Interactive\Crusader Kings III\mod\LegioImperialis`, descritor `...\mod\LegioImperialis.mod` |
| Jogo | `H:\SteamLibrary\steamapps\common\Crusader Kings III` |
| Logs | `C:\Users\rique\Documents\Paradox Interactive\Crusader Kings III\logs` |
| Docs e ferramentas | `C:\Users\rique\Documents\Workspace\Meus Mods CK3`; nas sessões na nuvem, `/mnt/project-files/Meus Mods CK3` |

## Regras do conteúdo

- Todos os fundadores com cultura `greek` e `rite = roman_rite`; DNA, brasões, casamentos, almas gêmeas, amizades e idades preservados.
- Sistemas próprios ficam no Cultus Imperialis: aqui não entram traços Sanguinis, Apostolus ou Immortal, nem religião, cultura ou traço customizados.
- Brasões usam texturas de mods de heráldica do autor de propósito; os nomes das texturas ficam como estão.
- on_actions nativos: encadeie on_actions próprios e deixe o trigger e o effect do vanilla intactos.
- O mod é independente do Cultus Imperialis e nunca roda junto com ele. Os arquivos originais do Imperialis e do Workshop são somente leitura.
- UTF-8 **com BOM** em `.txt` e `.yml`; `descriptor.mod` sem BOM.

## Git e validação

- Remoto `origin` = github.com/Licaesar/Legio-Imperialis. Trabalho numa branch a partir da `main`, push da branch liberado; a `main` muda só por PR que o autor mescla.
- CI (`.github/workflows/check.yml`): `.github/scripts/check_mod.py` confere BOM, chaves `{ }` e localização. Local: `python .github/scripts/check_mod.py .`.
- Suíte estática completa no PC: `Meus Mods CK3\Legio Imperialis\dev\test_legio.py`.
- Preserve saves e playsets existentes. O autor faz o playtest; o agente lê os logs.
