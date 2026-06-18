---
name: bridge_mcp
description: Invoca binários do host (como graphify) via ponte MCP.
params: [command]
upstream: internal_exec
---
# bridge_mcp (SKILL - NÃO É COMANDO SHELL)
Utilize esta skill diretamente como uma AÇÃO de ferramenta, nunca via `execute_shell`.
Ela invoca binários do host. Exemplo de uso correto (JSON): {"action": "bridge_mcp", "params": {"command": "graphify /tmp/workspace"}}.
Encapsula a execução de binários via stdin/stdout.
