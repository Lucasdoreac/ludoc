import os, subprocess, shlex, uuid, sqlite3, datetime, docx
from mcp.server.fastmcp import FastMCP
from starlette.routing import Route
from starlette.responses import JSONResponse

# MCP Server definition
mcp = FastMCP("Ludoc-Agent")

WORKSPACE = "/tmp/workspace"
DB_PATH = os.path.join(WORKSPACE, "tasks.db")
_CWD = [WORKSPACE]

os.makedirs(WORKSPACE, exist_ok=True)

# --- ACP Configuration (Agent Communication Protocol) ---
ACP_AGENT_ID = os.environ.get("ACP_AGENT_ID", f"ludoc-{uuid.uuid4().hex[:8]}")
ACP_CAPABILITIES = []  # Will be populated from MCP tools

@mcp.tool()
def exec_shell(command: str, timeout: int = 30, approved: bool = False) -> str:
    """Executes a shell command."""
    blacklist = ["rm", "push", "kill", "wget", "curl", "apt", "sh", "bash"]
    if not approved and any(term in command for term in blacklist):
        return "COMANDO BLOQUEADO: Risco de segurança. Requer HITL (Aprovação Humana) para execução"
    
    args = shlex.split(command.strip())
    if not args: return "Error: command required"
    
    if args[0] == "cd":
        if len(args) < 2: return f"CWD: {_CWD[0]}"
        target = args[1]
        new_cwd = target if os.path.isabs(target) else os.path.normpath(os.path.join(_CWD[0], target))
        if os.path.isdir(new_cwd):
            _CWD[0] = new_cwd
            return f"CWD changed to {_CWD[0]}"
        return f"cd: {target}: No such directory"
        
    try:
        res = subprocess.run(args, capture_output=True, text=True, cwd=_CWD[0], timeout=timeout)
        return f"Stdout: {res.stdout}\nStderr: {res.stderr}\nCode: {res.returncode}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def fs_read(file_path: str, offset: int = 0, limit: int = 500) -> str:
    """Reads a file from the workspace."""
    full = file_path if os.path.isabs(file_path) else os.path.join(_CWD[0], file_path)
    safe = os.path.normpath(full)
    try:
        with open(safe, "r", errors="replace") as f:
            lines = f.readlines()
        chunk = lines[offset : offset + limit]
        return "".join(f"{offset+i+1:4d} | {l}" for i, l in enumerate(chunk))
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def fs_search(pattern: str, path: str = ".") -> str:
    """Searches for a pattern in the workspace."""
    full = path if os.path.isabs(path) else os.path.join(WORKSPACE, path)
    try:
        res = subprocess.run(["grep", "-rnE", pattern, "."], capture_output=True, text=True, cwd=full, timeout=15)
        return res.stdout
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def python_interpreter(code: str) -> str:
    """Executes Python code."""
    try:
        res = subprocess.run(["python3", "-c", code], capture_output=True, text=True, timeout=10)
        return f"Stdout: {res.stdout}\nStderr: {res.stderr}\nCode: {res.returncode}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def write_file(filename: str, content: str) -> str:
    """Writes content to a file."""
    safe = os.path.normpath(os.path.join(WORKSPACE, filename))
    if not safe.startswith(WORKSPACE): return "Error: path traversal denied"
    os.makedirs(os.path.dirname(safe), exist_ok=True)
    with open(safe, "w") as f: f.write(content)
    return f"File {filename} written successfully"

@mcp.tool()
def fs_edit(file_path: str, old_string: str, new_string: str) -> str:
    """Edits a file by replacing a string."""
    safe = os.path.normpath(os.path.join(_CWD[0], file_path))
    try:
        with open(safe, "r", errors="replace") as f: content = f.read()
        if old_string not in content: return "Error: old_string not found"
        new_content = content.replace(old_string, new_string, 1)
        with open(safe, "w") as f: f.write(new_content)
        return "File edited successfully"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def generate_brand_docs(template_name: str, data: dict) -> str:
    """Generates a docx from a template."""
    template_path = os.path.join(WORKSPACE, "brand_assets", template_name)
    output_path = os.path.join(WORKSPACE, "deliverables", f"{uuid.uuid4()}.docx")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        doc = docx.Document(template_path)
        for p in doc.paragraphs:
            for key, value in data.items():
                p.text = p.text.replace(f"{{{{{key}}}}}", str(value))
        doc.save(output_path)
        return f"Document generated at {output_path}"
    except Exception as e:
        return f"Error: {str(e)}"

# --- ACP Endpoints (Agent Communication Protocol) ---
async def acp_discover(request):
    tools = await mcp.list_tools()
    return JSONResponse({
        "agent_id": os.environ.get("ACP_AGENT_ID", "ludoc-stable"),
        "capabilities": [t.name for t in tools],
        "endpoints": ["/acp/negotiate", "/acp/execute"]
    })

async def acp_execute(request):
    body = await request.json()
    skill_name = body.get("skill")
    params = body.get("params", {})
    # mcp.call_tool returns a list of Content objects (TextContent, etc.)
    result = await mcp.call_tool(skill_name, arguments=params)
    
    # Serialize Content objects to a format JSONResponse can handle
    serialized_result = []
    for content in result:
        if hasattr(content, "text"):
            serialized_result.append({"type": "text", "text": content.text})
        else:
            serialized_result.append(str(content))
            
    return JSONResponse({"result": serialized_result})

# --- Mount ACP Routes on FastMCP App ---
app = mcp.sse_app()
app.routes.append(Route("/acp/discover", endpoint=acp_discover, methods=["POST"]))
app.routes.append(Route("/acp/execute", endpoint=acp_execute, methods=["POST"]))

if __name__ == "__main__":
    import uvicorn
    # Servir via Uvicorn (o servidor ASGI correto)
    uvicorn.run(app, host="0.0.0.0", port=8080)
