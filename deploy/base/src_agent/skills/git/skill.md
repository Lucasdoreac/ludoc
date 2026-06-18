---
name: git
description: Executa comando git no workspace (status, diff, log, add, commit)
params: [command]
upstream: internal_exec
---
# git
Use apenas comandos não-destrutivos por padrão (status, diff, log, show). 
Para add/commit, confirme com o usuário antes. 
Nunca execute push ou reset --hard sem instrução explícita.
