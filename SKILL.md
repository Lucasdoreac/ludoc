# SKILL.md — AlignDev Development Rules

As an agent operating in this repository, you MUST follow these strict rules to maintain system integrity and security.

## 1. Code Validation & Critic Loop
- **MANDATORY**: All mutations to Python files are passed through the `Critic` (automatic syntax and linting check).
- **Self-Correction**: If the `Critic` rejects your code, read the error output and auto-correct before retrying.

## 2. Security, HITL & AICP
- **Header Enforcement**: All requests MUST include `X-Delegation-Chain`.
- **HITL Guard**: Destructive commands (rm, curl, etc.) are blocked by default. You MUST include `approved: true` only after explicit user clearance.
- **Thinking Facet**: When using RTI skills (e.g., `last30days`), always generate a JSON `--plan` first as dictated by AICP standards.

## 3. Dynamic Skill Lifecycle
- **Runtime Discovery**: Skills are loaded dynamically from `src/agent/skills/{name}/skill.md`.
- **Metadata**: Every skill file MUST start with valid YAML Front Matter (name, description, params).

## 4. Atomic Edits (fs_edit)
- Always `fs_read` before `fs_edit`.
- `old_string` MUST be unique and include 3-4 lines of context.

## 5. Persistence & I/O
- Use `/tmp/workspace` for all persistent work.
- **Episodic Memory**: Always distill successful sessions into `/tmp/workspace/episodes.md` using the `distill_experience` skill.
