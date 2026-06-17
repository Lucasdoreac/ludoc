# Ludoc — Sovereign AI Agent Orchestrator

Sovereign AI agent orchestration harness designed for high-integrity, local-first environments. Motorized by Python, secured by Envoy Proxy (OBridge), and optimized for enterprise-grade autonomous operations.

## 🚀 Advanced Architecture (Actor-Critic)

Ludoc implements a **Sovereign Orchestration Harness** with multi-layer validation:

| Component | Layer | Description |
|---|---|---|
| **The Doer (Actor)** | Execution | Hardened ReAct loop executing dynamic skills in a sandboxed workspace. |
| **The Critic** | Integrity | Automatic syntax validation (AST/Ruff) for every Python file mutation. |
| **HITL Guard** | Security | Human-In-The-Loop protection for dangerous shell commands (rm, push, curl). |
| **Semantic Memory** | Context | Active injection of `SKILL.md` (Rules) and `CONTEXT.md` (State) into the LLM prompt. |
| **Episodic Memory** | Learning | Session distillation into `episodes.md` for continuous task-specific learning. |

## 🛠 Key Features

- **Dynamic Skill Loading**: Tools are defined in Markdown (`skill.md`) with YAML Front Matter. No more static JSON catalogs.
- **CLI-Native Exploration**: Optimized for token efficiency. LLMs are instructed to use standard terminal commands (`ls`, `cat`, `grep`) instead of heavy MCP schemas.
- **MCP Compliant**: Supports official Model Context Protocol (HTTP transport) via `/tools` and `/tools/call`.
- **Zero-Trust Hardening**: Pods run as non-root (UID 1000) with strict resource limits and no privilege escalation.
- **OBridge Sidecar**: Envoy proxy enforcing security headers and `X-Delegation-Chain` traceability.

## 📦 Deployment

Deploy the sovereign stack in your local cluster (Kind/K3s/Bare-metal):

```sh
# Apply complete infrastructure
kubectl apply -k deploy/overlays/default

# Wait for rollout completion
kubectl rollout status deployment/ludoc-agent
```

## 🔍 Validation & Testing

Verify system integrity, HITL blocks, and Critic loops:

```powershell
# Port-forward the agent service
kubectl port-forward svc/ludoc-agent 8080:8080

# Execute automated grounding check
./grounding-check.ps1
```

## 📂 Repository Structure

- `src/agent/skills/`: **Dynamic Catalog**. Each folder contains a `skill.md` defining a tool.
- `src/agent/main.py`: Core server with Actor-Critic logic and memory injection.
- `deploy/base/`: Enterprise manifests (ludoc-config.yaml is the source of truth).
- `SKILL.md`: AlignDev development rules (Semantic Memory).
- `CONTEXT.md`: Project state tracking (Semantic Memory).

## 🛡 Security by Design (SBD)

Ludoc implements a **Security Blacklist** for `execute_shell`. Commands like `rm`, `wget`, `curl`, and `apt` are blocked unless an explicit `"approved": true` parameter is signed in the request.

---
*Ludoc — Sovereign intelligence, enterprise integrity.*
