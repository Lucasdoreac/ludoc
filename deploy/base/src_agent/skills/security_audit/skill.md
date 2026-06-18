---
name: security_audit
description: Audita a segurança de skills usando SkillSpector e retorna status PASSED/FAILED.
params: [skill_path]
upstream: internal_exec
---
# security_audit (SKILL)
Esta skill utiliza o `skillspector` para realizar uma varredura de segurança em uma skill candidata.
Ela analisa o reporte JSON e retorna um status de PASSED ou FAILED baseado no score de risco.
Exemplo de uso (JSON): {"action": "security_audit", "params": {"skill_path": "/path/to/skill/directory"}}.
A saída incluirá a decisão final (PASSED/FAILED) e detalhes de vulnerabilidades.
