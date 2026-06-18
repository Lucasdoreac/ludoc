# Roadmap — LUDOC Thinking Engine

## Concluído
- [x] Arquitetura de Orquestração Soberana (Model CoALA).
- [x] Integração de Memórias (Semântica + Episódica).
- [x] Motor Actor-Critic com proteção HITL.
- [x] Integração nativa da skill `last30days` (RTI) via Python.
- [x] Migração para Kustomize SSOT (ConfigMap Generator).
- [x] Suporte completo MCP (Model Context Protocol) com FastMCP framework.
- [x] Arquitetura FastMCP com SSE transport e 20 skills operacionais.
- [x] Eliminação de duplicação (main.py → server.py como fonte única).
- [x] ACP endpoints implementados (/acp/discover, /acp/negotiate, /acp/execute).

## Pendente

### Multi-Protocol Roadmap
- [x] MCP (Model Context Protocol) - ✅ Produção com FastMCP e SSE transport.
- [x] ACP (Agent Communication Protocol) - ✅ Endpoints implementados (/acp/discover, /acp/negotiate, /acp/execute).
- [ ] ADK (Agent Development Kit) - Integração com framework de criação.

### Otimização e Escalabilidade
- [ ] Otimizar loop de inferência para o modelo `gemma3:12b` (ou `qwen2.5-coder:32b`).
- [ ] Implementar técnicas de quantização avançada (IQ-imatrix) para o modelo de raciocínio.
- [ ] Ajustar timeouts do `envoy` para acomodar modelos mais lentos.

### Marca e Documentação (BrandDocs)
- [ ] Definir identidade visual e gerar template de proposta/relatório (`brand-docs`).

### Ecossistema A2A (Protocolo ACP)
- [ ] Implementar suporte a sub-agentes assíncronos via ACP (`workflow` facet).
- [ ] Expandir o catálogo de skills para gerenciamento completo do cluster K8s.
