# CONTEXT.md — Ludoc (GSD Core)

## Discuss
- **Architecture**: AI Agent Orchestrator sovereign (no cloud). Motor in Python, Skills declarative in JSON.
- **Sidecar**: Envoy Proxy (OBridge) handles security and the `X-Delegation-Chain` header. All POST requests must pass through it.
- **Brand**: Transitioning to "Ludoc". Name conflict with Red Hat Ludoc exists; renaming is considered.
- **Decision**: Using `qwen2.5:0.5b` for local testing. Optimized ReAct loop with hard stops for tool looping.

## Plan
- **Short-term**:
  - Optimize ReAct reliability for small models.
  - Integrate AlignDev standards via `SKILL.md`.
  - Implement basic linting (ast.parse, ruff) in `validate_code` skill.
- **Medium-term**:
  - Rename project to avoid conflicts.
  - Implement full brand documentation.
  - Expand skill catalog for cluster management.

## Execute
1. **Local Setup**:
   - Ensure Kind is running.
   - Run `kubectl apply -k deploy/overlays/default`.
2. **Local Testing**:
   - Forward port 8080: `kubectl port-forward deploy/ai-agent-orchestrator 8080:8080`.
   - Test health: `curl http://localhost:8080/healthz`.
3. **Chat Endpoint**:
   - Requires Ollama at `host.docker.internal:11434`.
   - `curl -X POST http://localhost:8080/chat -H "Content-Type: application/json" -H "X-Delegation-Chain: local-test" -d '{"prompt": "List patients"}'`.

## Verify
- **Integrity Check**: Run `./grounding-check.ps1` to validate API responses and skill execution.
- **Code Quality**: Use `validate_code` skill to check new Python scripts.
- **Audit**: Check Envoy logs for `X-Delegation-Chain` enforcement.
