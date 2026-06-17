---
name: distill_experience
description: Extrai um sumário conciso da tarefa e solução para memória episódica
params: [task, solution]
upstream: internal_exec
---
# distill_experience
Esta skill é chamada automaticamente ao final de uma sessão bem-sucedida.
Gera um registro no formato: "Tarefa: <Intenção> | Solução: <O que foi consertado e as lições aprendidas>".
O resultado é apensado ao arquivo `/tmp/workspace/episodes.md`.
