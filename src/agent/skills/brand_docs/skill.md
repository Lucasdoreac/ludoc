---
name: generate_brand_docs
description: Injeta dados estruturados em templates corporativos OOXML (.docx, .pptx, .xlsx).
params: [template_name, data]
upstream: internal_exec
---

# Diretrizes de Operação (Ponytail Principles para OOXML):
1. ZERO formatação Markdown. Você atua como um motor de preenchimento de payload.
2. Extraia a intenção do usuário e serialize as informações solicitadas no bloco `data`.
3. O caminho final do documento gerado será gerenciado internamente pela ferramenta, não o inclua nos parâmetros a menos que solicitado.
