# Ludoc — Sovereign AI Agent Orchestrator

**Sovereign AI agent orchestration harness** designed for high-integrity, local-first environments. Motorized by Python FastMCP framework, supporting multi-protocol agent communication (MCP/ACP/ADK), and optimized for enterprise-grade autonomous operations with Actor-Critic architecture.

## 🎯 Core Philosophy

- **Local-First**: Complete sovereignty with no cloud dependencies
- **Multi-Protocol**: Native support for MCP, ACP, and ADK standards  
- **Security-First**: HITL guards, path traversal protection, non-root execution
- **Dynamic Architecture**: Skills loaded at runtime from Markdown definitions
- **Enterprise-Ready**: Kubernetes deployment with resource limits and monitoring

## 🌐 Multi-Protocol Architecture

### MCP (Model Context Protocol) - Anthropic ✅
- **Status**: **Production Ready** 
- **Implementation**: FastMCP framework with SSE transport
- **Endpoints**: `/tools`, `/tools/call`, `/sse`
- **Spec**: [MCP Specification](https://modelcontextprotocol.io/specification/2025-03-26)
- **Use Case**: Primary LLM-to-tools integration transport
- **Features**: JSON structured logging, automatic skill discovery, schema validation

### ACP (Agent Communication Protocol) - IBM ✅
- **Status**: **Implemented**
- **Endpoints**: `/acp/discover`, `/acp/negotiate`, `/acp/execute`
- **Spec**: [IBM ACP Docs](https://www.ibm.com/think/topics/agent-communication-protocol)
- **Use Case**: Agent-to-agent communication and capability negotiation
- **Features**: Dynamic capability discovery, inter-agent task execution

### ADK (Agent Development Kit) - Google 📋
- **Status**: **Planned**
- **Integration**: Agent creation and deployment patterns
- **Spec**: [Google ADK](https://cloud.google.com/application-development-kit)
- **Use Case**: Rapid agent development with standardized lifecycle

## 🏗️ Architecture: Actor-Critic with HITL

Ludoc implements a **Sovereign Orchestration Harness** with multi-layer validation:

### Core Components

| Component | Layer | Description |
|---|---|---|
| **FastMCP Server** | Transport | SSE-based MCP transport with Starlette/uvicorn backend |
| **The Doer (Actor)** | Execution | Hardened ReAct loop executing dynamic skills in `/tmp/workspace` sandbox |
| **The Critic** | Integrity | Automatic AST + Ruff validation for Python file mutations |
| **HITL Guard** | Security | Human-In-The-Loop protection for dangerous shell commands |
| **Semantic Memory** | Context | Active injection of `SKILL.md` + `CONTEXT.md` into LLM prompts |
| **Episodic Memory** | Learning | Session distillation into `episodes.md` for continuous learning |
| **A2A Inference** | Models | `deepseek-r1:1.5b` (Thinker) + `qwen2.5-coder:3b` (Actor) |

### Advanced Features

- **🎯 Dynamic Skill Loading**: 20+ skills defined in Markdown with YAML frontmatter
- **🔒 Path-Guard Protection**: OS-agnostic traversal protection using `pathlib`
- **📊 Structured Logging**: JSON logging with thread-safe emission (Fase 2 PRD)
- **🧠 Memory Systems**: Semantic (CONTEXT.md/SKILL.md) + Episodic (episodes.md)
- **🛡️ Security Hardening**: Non-root pods (UID 1000), resource limits, no privilege escalation
- **🔄 Multi-Format Support**: Flat ConfigMap layout (cluster) + tree structure (dev local)

## 📦 Quick Start

### Prerequisites
- Kubernetes cluster (Kind/K3s/minikube)
- kubectl configured
- Ollama running locally (for development)

### Deployment

```bash
# Deploy full stack to local cluster
kubectl apply -k deploy/overlays/default

# Wait for rollout completion
kubectl rollout status deployment/ludoc-agent

# Port-forward for local testing
kubectl port-forward svc/ludoc-agent 8080:8080
```

### Validation

```powershell
# Run automated integrity check
./grounding-check.ps1

# Manual health check
curl http://localhost:8080/healthz

# Test available skills
curl http://localhost:8080/skills

# Test MCP tools endpoint
curl http://localhost:8080/tools
```

## 🧪 Development & Testing

### Local Development
```bash
# Install dependencies
pip install -r src/agent/requirements.txt

# Run agent directly (requires Ollama)
cd src/agent
python3 server.py
```

### Code Validation
- **Critic Loop**: Python mutations automatically pass through AST + Ruff validation
- **Manual Validation**: Use `validate_code` skill before `fs_edit`
- **Integration Testing**: `./grounding-check.ps1` validates API responses and skill execution

### Available Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/healthz` | GET | Service health check |
| `/skills` | GET | List all available skills |
| `/tools` | GET | MCP tool catalog with schemas |
| `/tools/call` | POST | Execute MCP tool |
| `/chat` | POST | Submit task for ReAct processing |
| `/acp/discover` | GET/POST | Discover ACP agent capabilities |
| `/acp/negotiate` | POST | Negotiate ACP capabilities |
| `/acp/execute` | POST | Execute ACP task |

## 📂 Repository Structure

```
ludoc/
├── src/agent/           # 🎯 Single source of truth
│   ├── server.py        # FastMCP-based production server
│   ├── llm.py           # Ollama client (Thinker/Actor models)
│   ├── cleaner.py       # Context relevance filtering
│   ├── acp_client.py    # ACP protocol implementation
│   └── skills/          # Dynamic skill catalog
│       ├── execute_shell/
│       ├── fs_edit/
│       ├── validate_code/
│       └── [20 total skills]
├── deploy/
│   ├── base/           # Base Kubernetes manifests
│   │   ├── kustomization.yaml  # ConfigMap-free (uses root)
│   │   └── ludoc-agent.yaml   # Deployment spec
│   └── overlays/default/      # Environment-specific patches
├── kustomization.yaml  # 🔄 Central ConfigMap generator
├── SKILL.md            # 🧠 Semantic memory (rules)
├── CONTEXT.md          # 🧠 Semantic memory (state)
└── CLAUDE.md           # 🤖 Claude Code development guide
```

## 🛡️ Security by Design

### HITL (Human-in-the-Loop) Protection
- **Dangerous Commands**: `rm`, `push`, `kill`, `wget`, `curl`, `apt`, `sh`, `bash` require explicit approval
- **Path Traversal Protection**: OS-agnostic validation using `pathlib.Path.is_relative_to()`
- **Non-Root Execution**: All pods run as UID 1000 with no privilege escalation

### Code Validation (The Critic)
- **Automatic AST Validation**: All Python code checked for syntax errors
- **Ruff Integration**: Style and error checking when available
- **Atomic Edits**: String replacement requires uniqueness to prevent accidental modifications

## 🛠️ Available Skills (20+ Tools)

### File System Operations
- **`fs_read`**: Read files with line numbers and pagination
- **`fs_edit`**: Atomic string replacement with uniqueness validation  
- **`fs_search`**: Pattern search across workspace (regex support)
- **`write_file`**: Create/overwrite files with path validation

### Execution & Code
- **`execute_shell`**: Shell command execution with HITL guards
- **`python_interpreter`**: Isolated Python code execution
- **`validate_code`**: AST + Ruff validation for Python code

### Memory & Context
- **`memory_set`**: Store K/V pairs in persistent memory
- **`memory_get`**: Retrieve values (or list all with `key=*`)
- **`get_context`**: Get project state, skills, and next steps
- **`distill_experience`**: Extract learning for episodic memory

### Advanced Operations
- **`web_search`**: DuckDuckGo search for external information
- **`web_fetch`**: URL content retrieval with HTML parsing
- **`git`**: Safe git operations (status, diff, log, add, commit)
- **`todo_write`**: Task management (add/complete/list/clear)

### Analysis & Security  
- **`analyze_dependency_graph`**: Skill dependency analysis
- **`security_audit`**: Skill security scanning via SkillSpector
- **`bridge_mcp`**: Host binary integration (graphify, etc.)

### Document Generation
- **`generate_brand_docs`**: OOXML template filling (.docx, .pptx, .xlsx)
- **`last30days`**: 30-day research across Reddit, X, YouTube, HN

## 🔮 Configuration

### Environment Variables
```bash
# LLM Configuration  
OLLAMA_HOST=http://127.0.0.1:11434
THINKER_MODEL=deepseek-r1:1.5b
ACTOR_MODEL=qwen2.5-coder:3b
CONTEXT_CHAR_LIMIT=12000

# System Configuration
SKILL_PROXY=http://localhost:8000
ACP_AGENT_ID=ludoc-auto-generated
WORKSPACE=/tmp/workspace
```

### Model Specifications
- **Thinker**: `deepseek-r1:1.5b` (Reasoning/Planning) - ~1.5GB VRAM
- **Actor**: `qwen2.5-coder:3b` (Implementation/Coding) - ~2GB VRAM
- **Total Memory**: Optimized for 8GB RAM environments

## 📊 Monitoring & Observability

### Structured Logging (JSON)
```json
{
  "ts": "2026-06-18T21:14:12.139Z",
  "level": "info", 
  "event": "skill_loaded",
  "name": "web_fetch",
  "source": "/app/src/agent/skill_web_fetch.md"
}
```

### Health & Metrics
- **Liveness**: TCP probe on port 8080
- **Readiness**: TCP probe on port 8080  
- **Resource Limits**: 100m CPU / 128Mi RAM → 500m CPU / 256Mi RAM
- **Startup Probe**: Application initialization detection

## 🤝 Contributing

This project follows **Sovereign Development Principles**:
- **Local-First**: All development happens on local infrastructure
- **Security-First**: Every code mutation passes through The Critic
- **Standards-Based**: MCP, ACP, and ADK protocol compliance
- **Documentation-First**: Semantic memory drives system behavior

### Development Workflow
1. Read `CLAUDE.md` for development guidelines
2. Check `CONTEXT.md` for current project state
3. Reference `SKILL.md` for AlignDev rules
4. Test locally with `./grounding-check.ps1`

## 📜 License

Sovereign AI infrastructure - Enterprise integrity maintained.

---

**Ludoc — Sovereign intelligence, enterprise integrity, local-first.**
