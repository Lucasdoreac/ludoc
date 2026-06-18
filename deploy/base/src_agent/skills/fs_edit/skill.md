---
name: fs_edit
description: Edição atômica de arquivo por substituição exata de string (requer unicidade)
params: [file_path, old_string, new_string]
upstream: internal_exec
---
# fs_edit
Use para modificações cirúrgicas em arquivos existentes. 
old_string deve ser única no arquivo — inclua 3-4 linhas de contexto ao redor. 
Sempre chame `cat` via `execute_shell` antes para verificar o conteúdo exato. 
Se retornar erro de count>1, expanda o old_string. 
Se count=0, verifique espaços e indentação exatos.
Sempre será validado automaticamente pelo Critic antes da gravação se for arquivo Python.
