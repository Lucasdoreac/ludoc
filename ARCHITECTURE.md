# Arquitetura: Ludoc-Agent (MCP/SSE)

## Visão Geral
O Ludoc-Agent foi refatorado de um servidor HTTP legada para um provedor de ferramentas compatível com o [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). Ele utiliza transporte SSE (Server-Sent Events) servido por Uvicorn (ASGI) para garantir estabilidade, isolamento e performance dentro do ambiente Kubernetes.

## Fluxo de Comunicação
1. **Transporte:** Clientes MCP conectam-se via HTTP/SSE (`GET /sse`) na porta `8080`.
2. **Protocolo:** JSON-RPC 2.0 (MCP).
3. **Integração ACP:** Endpoints estáticos (`/acp/discover`, `/acp/execute`) permitem que orquestradores legados ou externos consumam ferramentas MCP nativamente via POST.
4. **Execução:** O servidor `src/agent/server.py` invoca as ferramentas (skills) registradas via decorador `@mcp.tool()`.

## Componentes da Soberania
- **Entrypoint:** `src/agent/server.py` (ASGI app).
- **Transporte:** SSE (Server-Sent Events) sobre HTTP.
- **Tools:** Definidas em `skills/` (frontmatter) e implementadas no `server.py`.
- **Provisionamento:** Código injetado via ConfigMap (`ludoc-config`), deploy via Kustomize em Kubernetes, imagem base `python:3.13-slim`.

## Endpoints ACP
- `/acp/discover`: Retorna `agent_id`, lista de *capabilities* (ferramentas) e endpoints disponíveis.
- `/acp/execute`: Recebe `{"skill": "...", "params": {...}}` e retorna o resultado da ferramenta MCP serializado.
