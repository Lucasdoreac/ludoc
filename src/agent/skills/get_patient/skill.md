---
name: get_patient
description: Busca registro de paciente por ID
params: [patient_id]
upstream: /patients/{patient_id}
---
# get_patient
Use esta skill para recuperar dados de um único paciente. Passe apenas o ID numérico. Nunca infira IDs — solicite ao usuário se necessário.
