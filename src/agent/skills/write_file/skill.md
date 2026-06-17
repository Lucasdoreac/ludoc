---
name: write_file
description: Cria ou sobrescreve arquivo em /tmp/workspace
params: [filename, content]
upstream: internal_exec
---
# write_file
O caminho é relativo ao workspace — não use ../ ou caminhos absolutos.
Sempre será validado automaticamente pelo Critic antes da gravação.
Se houver erro de sintaxe Python, o arquivo não será gravado e você receberá o erro.
