---
name: execute_shell
description: Executa comando shell no sandbox /tmp/workspace
params: [command]
upstream: internal_exec
---
# execute_shell
Use apenas para comandos de leitura e execução de código dentro do sandbox. 
Nunca execute comandos destrutivos (rm -rf, dd, mkfs) ou que modifiquem configurações do sistema.
Comandos bloqueados (requerem HITL): rm, push, kill, wget, curl, apt, sh, bash.
Se precisar ler arquivos, use `cat`, `grep`, `find`, `ls`.
