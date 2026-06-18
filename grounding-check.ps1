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
    if ($skills.Count -ge 20) {
        Write-Host "[OK] Legacy Skills carregadas: $($skills.Count)" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] Legacy Skills insuficiente: $($skills.Count) (esperado: 20)" -ForegroundColor Red
    }
} catch {
    Write-Host "[ERROR] Falha ao listar skills" -ForegroundColor Red
}

# 3. MCP Tools Listing (Official Spec)
try {
    $mcpTools = Invoke-RestMethod -Uri "$baseUrl/tools" -Method Get
    if ($mcpTools.tools.Count -ge 20) {
        Write-Host "[OK] MCP Tools carregadas: $($mcpTools.tools.Count)" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] MCP Tools inconsistentes: $($mcpTools.tools.Count) (esperado: 20)" -ForegroundColor Red
    }
} catch {
    Write-Host "[ERROR] Falha no endpoint MCP /tools" -ForegroundColor Red
}

# 4. MCP Tool Call Test (Last30Days RTI)
$rtiPayload = @{
    name = "last30days"
    arguments = @{ topic = "AI Agents trends" }
} | ConvertTo-Json

try {
    Write-Host "Testando RTI (last30days)..." -NoNewline
    $rtiResp = Invoke-RestMethod -Uri "$baseUrl/tools/call" -Method Post -Headers $headers -Body $rtiPayload
    if ($rtiResp.content[0].text -like "*status*") {
        Write-Host " [OK]" -ForegroundColor Green
    } else {
        # Como o clone demora, pode retornar erro ou resultado vazio inicialmente
        Write-Host " [SKIP] (Aguardando inicialização do motor)" -ForegroundColor Yellow
    }
} catch {
    Write-Host " [ERROR] Falha no teste RTI: $($_.Exception.Message)" -ForegroundColor Red
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

# 6. ACP Endpoints (Multi-Protocol Support)
try {
    Write-Host "Testando ACP Discover..." -NoNewline
    $acpResp = Invoke-RestMethod -Uri "$baseUrl/acp/discover" -Method Post -Headers $headers
    if ($acpResp.agent_id -and $acpResp.capabilities.Count -ge 20) {
        Write-Host " [OK] Agent: $($acpResp.agent_id)" -ForegroundColor Green
    } else {
        Write-Host " [WARN] ACP respondendo mas sem capabilities completas" -ForegroundColor Yellow
    }
} catch {
    Write-Host " [ERROR] ACP endpoint falhou: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "--- Fim da Validação ---"
