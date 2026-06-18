---
name: memory_set
description: Armazena um valor K/V na memória persistente do agente (dura enquanto o pod viver)
params: [key, value]
upstream: internal_exec
---
# memory_set
Use para salvar fatos importantes entre chamadas: planos, resultados intermediários, decisões tomadas. 
Prefira chaves descritivas como 'plano_atual' ou 'ultimo_arquivo_editado'.
