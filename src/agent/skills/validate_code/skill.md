---
name: validate_code
description: Valida sintaxe Python via ast.parse e ruff (se disponível)
params: [code]
upstream: internal_exec
---
# validate_code
Esta skill é chamada automaticamente pelo sistema durante write_file e fs_edit.
Você também pode chamá-la manualmente para validar blocos de código antes de tentar gravar.
Só prossiga se result.valid for true.
