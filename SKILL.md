# SKILL.md — AlignDev Development Rules

As an agent operating in this repository, you MUST follow these strict rules to maintain system integrity and security.

## 1. Code Validation
- **MANDATORY**: Always validate modified Python files using `ast.parse` or `ruff` BEFORE saving.
- Use the `validate_code` skill if available, or run `python3 -m ast` locally.
- Never commit code with syntax errors.

## 2. Security & Delegation
- **Header Enforcement**: Never ignore or omit the `X-Delegation-Chain` header in local tests or inter-service requests.
- All requests to `/run` or `/chat` MUST include this header to pass through OBridge.
- Do not bypass the Envoy sidecar for production-like validations.

## 3. Dependency Management
- **Stdlib First**: Use only native Python standard library dependencies whenever possible.
- If an external library is required, it must be added to the `Dockerfile` and documented in `CONTEXT.md`.
- Avoid heavy frameworks; prefer `urllib` over `requests` for core agent logic.

## 4. Atomic Edits
- Prefer the `fs_edit` skill for surgical changes to existing files.
- Ensure `old_string` includes enough context to be unique.
- Always `read_file` before attempting an edit to verify current state and indentation.

## 5. Environment Isolation
- All file operations must be relative to the sandbox `WORKSPACE` (`/tmp/workspace`) or explicitly allowed project paths.
- Prevent path traversal by normalizing all input paths.
