# Roadmap — LUDOC Thinking Engine

## Concluído
- [x] Arquitetura de Orquestração Soberana (Model CoALA).
- [x] Integração de Memórias (Semântica + Episódica).
- [x] Motor Actor-Critic com proteção HITL.
- [x] Integração nativa da skill `last30days` (RTI) via Python.
- [x] Migração para Kustomize SSOT (ConfigMap Generator).

## Pendente

### Otimização e Escalabilidade
- [ ] Otimizar loop de inferência para o modelo `gemma3:12b` (ou `qwen2.5-coder:32b`).
- [ ] Implementar técnicas de quantização avançada (IQ-imatrix) para o modelo de raciocínio.
- [ ] Ajustar timeouts do `envoy` para acomodar modelos mais lentos.

### Marca e Documentação (BrandDocs)
- [ ] Definir identidade visual e gerar template de proposta/relatório (`brand-docs`).
- [ ] Renomear repositório (conflito Red Hat) e atualizar referências globais.

### Ecossistema A2A (Protocolo AICP)
- [ ] Implementar suporte a sub-agentes assíncronos (`workflow` facet).
- [ ] Expandir o catálogo de skills para gerenciamento completo do cluster K8s.
