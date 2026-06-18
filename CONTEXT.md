# CONTEXT.md — LUDOC (Thinking Engine)

## Multi-Protocol Strategy
- **MCP**: Primary transport for tool integration.
- **ACP**: Communication backbone for agent-to-agent negotiation.
- **ADK**: Developer framework for new agent orchestration.

## Discuss
- **Architecture**: Sovereign AI Agent Orchestrator (Model CoALA).
- **Inference Strategy**: **A2A (Agent-to-Agent)** optimized for 8GB RAM.
- **Models**:
  - **Thinker**: `deepseek-r1:1.5b` (Reasoning/Planning).
  - **Actor**: `qwen2.5-coder:3b` (Implementation/Coding).
- **Protocol**: **Multi-Protocol Backbone (MCP+ACP+ADK)** using CoT tags and tiered execution.
- **Decision**: Moving away from monolithic models to an Execution Ladder.

## Current Status (2026-06-18)
- **Migration Complete**: Eliminated legacy `main.py`, established `server.py` as single source of truth
- **20 Skills Operational**: All skills loaded with FastMCP framework + MCP compliance
- **Multi-Protocol Ready**: MCP-SSE (production), ACP endpoints implemented, ADK patterns established
- **Deployment Validated**: Kind cluster tested, health checks passing, all endpoints operational
- **Documentation Updated**: README, SKILL.md, and CONTEXT.md reflect current architecture

## Plan
- **Short-term**:
  - Continue ACP testing and refinement.
  - Add more advanced security_audit capabilities.
  - Expand skill catalog for cluster management.
- **Medium-term**:
  - Implement full brand documentation generation.
  - Add monitoring and observability features.
  - Expand A2A inference patterns.

## Execute
1. **Local Setup**:
   - Ensure Kind is running.
   - Run `kubectl apply -k deploy/overlays/default`.
2. **Local Testing**:
   - Forward port 8080: `kubectl port-forward svc/ludoc-agent 8080:8080`.
   - Test health: `curl http://localhost:8080/healthz`.
3. **Chat Endpoint**:
   - Requires Ollama at `host.docker.internal:11434`.
   - `curl -X POST http://localhost:8080/chat -H "Content-Type: application/json" -H "X-Delegation-Chain: local-test" -d '{"prompt": "List patients"}'`.

## Verify
- **Integrity Check**: Run `./grounding-check.ps1` to validate API responses and skill execution.
- **Code Quality**: Use `validate_code` skill to check new Python scripts.
- **Audit**: Check Envoy logs for `X-Delegation-Chain` enforcement.
