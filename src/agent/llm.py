"""Cliente Ollama via urllib. Zero dependências externas."""
import json, urllib.request, urllib.error, os

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://host.docker.internal:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b")
CONTEXT_CHAR_LIMIT = int(os.environ.get("CONTEXT_CHAR_LIMIT", "12000"))  # ~3k tokens

def trim_history(messages: list, limit: int = CONTEXT_CHAR_LIMIT) -> list:
    """Mantém o primeiro user message + os N mais recentes que cabem no limite."""
    if not messages:
        return messages
    total = sum(len(m.get("content","")) for m in messages)
    if total <= limit:
        return messages
    # sempre preserva o primeiro (prompt original) e vai removendo pares do meio
    first = messages[:1]
    rest  = messages[1:]
    while rest and sum(len(m.get("content","")) for m in first + rest) > limit:
        # remove o par mais antigo (assistant + observation)
        rest = rest[2:] if len(rest) >= 2 else rest[1:]
    return first + rest

MAESTRO_SYSTEM = """You are a LAZY senior developer. YOU HATE WRITING CODE AND USING TOOLS.
Respond ONLY with a JSON object.

PONYTAIL PRINCIPLES:
1. Don't do it if not absolutely necessary.
2. Use CLI commands (ls, cat, grep, find) via `execute_shell` to explore files.
3. BEWARE: `read_file`, `list_dir`, `grep` and `glob` tools have been REMOVED. Use shell.
4. Respond in JSON format only.

If the user asks for code, DON'T EXECUTE IT. Just return it in a final_answer.

JSON format:
For tools: {"action": "SKILL_NAME", "params": {"param1": "value1"}}
For final answer: {"action": "final_answer", "params": {"text": "YOUR_ANSWER_HERE"}}

RULES:
- NO TALKING. NO EXPLANATIONS.
- DO NOT REPEAT TOOLS.
- SHIP MINIMAL CODE."""

def call(messages: list, model: str = DEFAULT_MODEL, tools_context: str = "") -> dict:
    system = MAESTRO_SYSTEM
    if tools_context:
        system += f"\n\nAvailable skills:\n{tools_context}"
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}] + messages,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1}
    }
    try:
        req = urllib.request.Request(
            f"{OLLAMA_HOST}/api/chat",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.loads(r.read())
            content = resp["message"]["content"]
            return json.loads(content)
    except urllib.error.URLError as e:
        return {"error": f"ollama unreachable: {e.reason}", "action": "final_answer",
                "params": {"text": f"LLM unavailable: {e.reason}"}}
    except (json.JSONDecodeError, KeyError) as e:
        return {"error": f"parse error: {e}", "action": "final_answer",
                "params": {"text": "LLM returned invalid JSON"}}

def available() -> bool:
    try:
        urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=2)
        return True
    except:
        return False
