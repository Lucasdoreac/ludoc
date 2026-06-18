"""Cliente Ollama via urllib. Zero dependências externas."""
import json, urllib.request, urllib.error, os

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
if not OLLAMA_HOST.startswith("http"):
    OLLAMA_HOST = f"http://{OLLAMA_HOST}"
# Arquitetura AICP (Agentic Interoperability): 1.5B p/ Pensar, 3B p/ Agir
THINKER_MODEL = os.environ.get("THINKER_MODEL", "qwen2.5-coder:3b")
ACTOR_MODEL   = os.environ.get("ACTOR_MODEL", "qwen2.5-coder:3b")
DEFAULT_MODEL = ACTOR_MODEL 
CONTEXT_CHAR_LIMIT = int(os.environ.get("CONTEXT_CHAR_LIMIT", "12000"))

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
2. Use CLI commands ONLY via `execute_shell`.
   - CORRECT: {"action": "execute_shell", "params": {"command": "ls /tmp/workspace"}}
   - WRONG: {"action": "ls", ...}
3. BEWARE: Tools like `read_file` do not exist. Use `execute_shell` with `cat`.
4. Respond in JSON format only.

If the user asks for code, DON'T EXECUTE IT. Just return it in a final_answer.

JSON format:
For tools: {"action": "SKILL_NAME", "params": {"param1": "value1"}}
For final answer: {"action": "final_answer", "params": {"text": "YOUR_ANSWER_HERE"}}

RULES:
- NO TALKING. NO EXPLANATIONS.
- DO NOT REPEAT TOOLS.
- SHIP MINIMAL CODE."""

def parse_llm_response(raw_content):
    """
    Sanitização determinística (Zero Regex) para modelos CoT (DeepSeek-R1).
    Isola o raciocínio e expurga artefatos Markdown.
    """
    content = raw_content
    # 1. Isolar e descartar o bloco de pensamento (CoT)
    if "</think>" in content:
        content = content.split("</think>")[-1]
    
    content = content.strip()
    # 2. Expurgo de artefatos Markdown
    if content.startswith("```json"): content = content[7:]
    elif content.startswith("```"): content = content[3:]
    if content.endswith("```"): content = content[:-3]
        
    content = content.strip()
    # 3. Parse estrito
    try:
        # Tenta encontrar o primeiro bloco JSON válido
        import re
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return json.loads(content)
    except json.JSONDecodeError as e:
        return {
            "error": f"JSON Decode Error: {str(e)}", 
            "action": "final_answer", 
            "params": {"text": f"Falha de formatação JSON: {str(e)}"}
        }

def call(messages: list, model: str = DEFAULT_MODEL, tools_context: str = "") -> dict:
    system = MAESTRO_SYSTEM
    if tools_context: system += f"\n\nAvailable skills:\n{tools_context}"
    
    if "deepseek-r1" in model.lower():
        system += "\nINSTRUCTION: You are a THINKER. Always use <thought> tags to plan your next action step-by-step."

    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}] + messages,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1}
    }
    try:
        # Forçar proxy vazio
        proxy_handler = urllib.request.ProxyHandler({})
        opener = urllib.request.build_opener(proxy_handler)
        
        req = urllib.request.Request(
            f"{OLLAMA_HOST}/api/chat",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        print(f"DEBUG: Enviando payload para Ollama: {len(json.dumps(payload).encode())} bytes")
        with opener.open(req, timeout=300) as r:
            resp = json.loads(r.read())
            return parse_llm_response(resp["message"]["content"])
    except Exception as e:
        print(f"DEBUG: Erro na chamada ao Ollama: {e}")
        return {"error": f"ollama unreachable: {e}", "action": "final_answer",
                "params": {"text": f"LLM unavailable: {e}"}}
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
    except Exception:
        return False
