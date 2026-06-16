# Deep Research: Tool Gap Analysis

Você é um agente de análise. Execute as etapas abaixo em ordem, usando apenas as skills disponíveis.

## Etapa 1 — Inventário atual
Chame `GET /skills` e liste todas as skills disponíveis no catálogo.

## Etapa 2 — Research externo
Execute as seguintes buscas via skill `web_search` e extraia as tools/capacidades listadas:

1. `web_search`: "AI coding agent tools 2025 capabilities list"
2. `web_search`: "MCP tools standard list filesystem memory search"
3. `web_search`: "Claude Code built-in tools list"
4. `web_search`: "Codex agent tools capabilities"
5. `web_search`: "autonomous agent tool use benchmark standard tools"

Para cada resultado relevante, use `web_fetch` na URL para extrair a lista de tools mencionadas.

## Etapa 3 — Análise de gap
Compare o inventário da Etapa 1 com as tools encontradas na Etapa 2.

Organize o resultado em três categorias:

### ✅ Já temos
Tools do padrão que o harness já possui.

### ❌ Falta — Alta prioridade
Tools presentes em 3+ fontes externas que não existem no catálogo.
Para cada uma: nome, o que faz, por que é importante.

### ⚠️ Falta — Baixa prioridade
Tools presentes em 1-2 fontes externas.

## Etapa 4 — Recomendação
Liste as 3 próximas skills a implementar, em ordem de impacto, com:
- Nome da skill
- Params necessários
- Implementação estimada (stdlib Python? lib externa?)
- system_instruction sugerida

## Output final
Retorne um JSON estruturado com as categorias acima + recomendações.
