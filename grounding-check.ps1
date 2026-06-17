# Grounding Check - Ludoc
# Valida integridade das skills e do loop ReAct

$baseUrl = "http://localhost:8080"
$headers = @{
    "Content-Type" = "application/json"
    "X-Delegation-Chain" = "grounding-check"
}

Write-Host "--- Iniciando Validação Ludoc (ludoc-agent) ---" -ForegroundColor Cyan

# 1. Health Check
try {
    $resp = Invoke-RestMethod -Uri "$baseUrl/healthz" -Method Get
    if ($resp.status -eq "ok") {
        Write-Host "[OK] Health Check" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] Health Check" -ForegroundColor Red
    }
} catch {
    Write-Host "[ERROR] Agente inacessível em $baseUrl" -ForegroundColor Red
}

# 2. Skills Listing (Legacy)
try {
    $skills = Invoke-RestMethod -Uri "$baseUrl/skills" -Method Get
    if ($skills.Count -ge 16) {
        Write-Host "[OK] Legacy Skills carregadas: $($skills.Count)" -ForegroundColor Green
    }
} catch {
    Write-Host "[ERROR] Falha ao listar skills" -ForegroundColor Red
}

# 3. MCP Tools Listing (Official Spec)
try {
    $mcpTools = Invoke-RestMethod -Uri "$baseUrl/tools" -Method Get
    if ($mcpTools.tools.Count -ge 16) {
        Write-Host "[OK] MCP Tools carregadas: $($mcpTools.tools.Count)" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] MCP Tools inconsistentes" -ForegroundColor Red
    }
} catch {
    Write-Host "[ERROR] Falha no endpoint MCP /tools" -ForegroundColor Red
}

# 4. MCP Tool Call Test
$callPayload = @{
    name = "memory_set"
    arguments = @{ key = "check"; value = "passed" }
} | ConvertTo-Json

try {
    $callResp = Invoke-RestMethod -Uri "$baseUrl/tools/call" -Method Post -Headers $headers -Body $callPayload
    if ($callResp.content[0].type -eq "text") {
        Write-Host "[OK] MCP /tools/call funcional" -ForegroundColor Green
    }
} catch {
    Write-Host "[ERROR] Falha no teste de chamada MCP" -ForegroundColor Red
}

# 5. Chat Endpoint (Dry Run)
$payload = @{
    prompt = "Quem é você?"
    max_iter = 1
} | ConvertTo-Json

try {
    $chatResp = Invoke-RestMethod -Uri "$baseUrl/chat" -Method Post -Headers $headers -Body $payload
    Write-Host "[OK] Chat respondeu (checar trace para detalhes)" -ForegroundColor Green
} catch {
    if ($_.Exception.Response.StatusCode -eq 503) {
        Write-Host "[SKIP] Chat falhou (Ollama offline - esperado se não houver cluster local)" -ForegroundColor Yellow
    } else {
        Write-Host "[ERROR] Chat endpoint falhou: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "--- Fim da Validação ---"
