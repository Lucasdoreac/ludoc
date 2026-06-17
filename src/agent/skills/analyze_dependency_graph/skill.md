---
name: analyze_dependency_graph
description: Retorna grafo de dependências das skills (nós, arestas, policy)
params: []
upstream: internal_exec
---
# analyze_dependency_graph
Use antes de refatorar qualquer skill para entender o impacto. 
Verifique cycles antes de criar novas dependências entre skills.
