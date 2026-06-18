---
name: fs_search
description: Busca por padrões de texto (regex) em todo o repositório ou diretório
params: [pattern, path]
upstream: internal_exec
---
# fs_search
Equivalente ao `grep -r` ou `ripgrep`. 
Use para localizar definições de funções, variáveis ou erros em múltiplos arquivos.
Ignora automaticamente pastas como `.git`, `node_modules` e `__pycache__`.
