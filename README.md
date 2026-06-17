# Ludoc — Sovereign AI Agent Orchestrator

Sovereign AI agent orchestration harness designed for high-integrity, local-first environments. Motorized by Python, secured by Envoy Proxy (OBridge), and compliant with the Model Context Protocol (MCP).

## Core Architecture

| Component | Role | Description |
|---|---|---|
| **Ludoc Agent** | Logic Plane | Python agent executing skills with a hardened ReAct loop. |
| **OBridge** | Proxy Plane | Envoy sidecar enforcing security and `X-Delegation-Chain` headers. |
| **Workspace** | Data Plane | Persistent sandbox via PVC for agent-generated code and files. |
| **Mock Records** | Extension | Mock API for patient records used in integration testing. |

## Key Features

- **MCP Compliant**: Supports official Model Context Protocol (HTTP transport) via `/tools` and `/tools/call`.
- **Zero-Trust Hardening**: Pods run as non-root (UID 1000) with strict resource limits and no privilege escalation.
- **Persistence**: 100Mi PersistentVolumeClaim (PVC) mounted at `/tmp/workspace` for state durability.
- **Optimized ReAct**: Custom loop for small LLMs (e.g., `qwen2.5:0.5b`) with hard stops for tool call looping.
- **Sovereign-First**: Built for air-gapped or local clusters (Kind/Bare-Metal) using Ollama.

## Quick Start (Deploy in 5m)

```sh
# 1. Apply Infrastructure
kubectl apply -k deploy/overlays/default

# 2. Wait for Readiness
kubectl rollout status deployment/ludoc-agent
kubectl rollout status deployment/patient-records
```

## Validation & Testing

Run the automated grounding check to verify health, skills, and MCP compliance:

```powershell
# Port-forward the agent service
kubectl port-forward svc/ludoc-agent 8080:8080

# Execute validation script
./grounding-check.ps1
```

### Manual MCP Tool Call Example

```sh
curl -X POST http://localhost:8080/tools/call \
  -H "Content-Type: application/json" \
  -H "X-Delegation-Chain: manual-test" \
  -d '{
    "name": "memory_set",
    "arguments": {"key": "status", "value": "production-ready"}
  }'
```

## Repository Structure

- `src/agent/`: Core Python logic, skills catalog, and ReAct loop.
- `deploy/base/`: K8s manifests (Deployment, PVC, ConfigMaps) — Single Source of Truth.
- `deploy/overlays/`: Environment-specific configurations (Default, Cliente-A, etc.).
- `SKILL.md`: Strict AlignDev development rules for agents.
- `CONTEXT.md`: Project state tracking (GSD Core).

## Maintenance

- **Rollback**: `kubectl rollout undo deployment/ludoc-agent`
- **Cleanup**: `kubectl delete -k deploy/overlays/default`

---
*Ludoc — Empowering sovereign intelligence.*
