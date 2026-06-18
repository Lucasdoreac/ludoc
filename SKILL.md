# SKILL.md — AlignDev Development Rules

As an agent operating in this repository, you MUST follow these strict rules to maintain system integrity and security.

## 1. Code Validation & Critic Loop
- **MANDATORY**: All mutations to Python files are passed through the `Critic` (automatic syntax and linting check).
- **Self-Correction**: If the `Critic` rejects your code, read the error output and auto-correct before retrying.

## 2. Security, HITL & Multi-Protocol

- **Header Enforcement**: All requests MUST include `X-Delegation-Chain`.
- **HITL Guard**: Destructive commands (rm, curl, etc.) are blocked by default. You MUST include `approved: true` only after explicit user clearance.
- **Thinking Facet**: When using RTI skills (e.g., `last30days`), always generate a JSON `--plan` first as dictated by multi-protocol standards.
- **Protocol Security**: Each protocol has specific security requirements - refer to respective specifications.

## 3. Dynamic Skill Lifecycle
- **Runtime Discovery**: Skills are loaded dynamically from `src/agent/skills/{name}/skill.md`.
- **Metadata**: Every skill file MUST start with valid YAML Front Matter (name, description, params).
- **Dual Layout Support**: Supports flat ConfigMap layout (cluster) and tree structure (dev local).

## 4. Atomic Edits (fs_edit)
- Always `fs_read` before `fs_edit`.
- `old_string` MUST be unique and include 3-4 lines of context.

## 5. Multi-Protocol Development Rules

### MCP Compatibility
- **FastMCP Framework**: Server uses FastMCP with SSE transport for native MCP support.
- All skills MUST be MCP-compatible via `@mcp.tool()` decorators or internal handlers.
- Return values MUST follow MCP format: `{"content": [{"type": "text", "text": "..."}]}`
- Skill metadata in `skill.md` MUST include `params` definition for schema generation.

### ACP Readiness
- Skills designed for potential ACP exposure MUST:
  - Declare clear input/output schemas
  - Be stateless where possible
  - Support timeout constraints
  - Document resource requirements

### ADK Patterns
- Follow ADK naming conventions for agent components.
- Structure skills to be consumable by ADK-created agents.
- Maintain compatibility with ADK runtime.

### Protocol-Specific Guidelines

**For MCP-Only Skills:**
- Focus on LLM-to-tool integration.
- Optimize for single-request response patterns.
- Minimal state management.

**For ACP-Exposed Skills:**
- Design for negotiation and discovery.
- Support capability queries.
- Handle agent-to-agent messaging.

**For ADK-Integrated Agents:**
- Follow ADK lifecycle patterns.
- Support deployment-time configuration.
- Expose metrics and health endpoints.

## 6. Persistence & I/O
- Use `/tmp/workspace` for all persistent work.
- **Episodic Memory**: Always distill successful sessions into `/tmp/workspace/episodes.md` using the `distill_experience` skill.
