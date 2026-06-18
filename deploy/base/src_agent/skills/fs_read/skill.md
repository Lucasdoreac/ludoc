---
name: fs_read
description: Lê conteúdo de arquivos com numeração de linhas e paginação (offset/limit)
params: [file_path, offset, limit]
upstream: internal_exec
---
# fs_read
SEMPRE use esta ferramenta antes de editar um arquivo com `fs_edit`.
A saída inclui o número da linha (ex: `10 | código`), permitindo que você identifique exatamente o bloco para o `old_string`.
Use `offset` e `limit` para ler arquivos grandes sem estourar o contexto.
