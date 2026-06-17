---
name: todo_write
description: Gerencia lista de tarefas do agente (action: add|complete|list|clear)
params: [action, task]
upstream: internal_exec
---
# todo_write
Use para decompor tarefas complexas. 
Antes de executar um plano multi-step: add cada passo. 
Marque complete após cada execução bem-sucedida. 
Use list para verificar o que falta.
