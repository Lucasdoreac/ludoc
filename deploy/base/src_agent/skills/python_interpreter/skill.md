---
name: python_interpreter
description: Executa código Python puro em um ambiente isolado (sandbox)
params: [code]
upstream: internal_exec
---
# python_interpreter
Use para realizar cálculos complexos, processamento de dados ou testar algoritmos isolados.
Não tem acesso ao sistema de arquivos do projeto — para manipular arquivos use `write_file` ou `execute_shell`.
