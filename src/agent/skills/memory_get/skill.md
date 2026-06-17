---
name: memory_get
description: Recupera um valor da memória pelo key (ou lista todas as keys se key=*)
params: [key]
upstream: internal_exec
---
# memory_get
Use no início de uma tarefa para recuperar contexto anterior. 
Use key='*' para listar todas as entradas disponíveis.
