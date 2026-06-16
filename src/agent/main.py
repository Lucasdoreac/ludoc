import json, urllib.request, urllib.error, http.server, os

PROXY = "http://localhost:15001"
SKILLS_FILE = os.path.join(os.path.dirname(__file__), "skills.json")

# --- carrega catálogo de skills ---
with open(SKILLS_FILE) as f:
    _catalog = {s["name"]: s for s in json.load(f)}

def list_skills():
    return [{"name": s["name"], "description": s["description"], "params": s["params"]}
            for s in _catalog.values()]

# --- executor genérico de skill ---
def run_skill(name, params, caller=None):
    skill = _catalog.get(name)
    if not skill:
        return 404, {"error": f"skill '{name}' not found"}
    path = skill["upstream"]
    for k, v in params.items():
        path = path.replace(f"{{{k}}}", str(v))
    try:
        with urllib.request.urlopen(f"{PROXY}{path}", timeout=5) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, {"error": str(e.reason)}

# --- servidor HTTP ---
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/healthz":
            return self.send_json(200, {"status": "ok"})
        if self.path == "/skills":
            return self.send_json(200, list_skills())
        self.send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/run":
            return self.send_json(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        skill_name = body.get("skill")
        params     = body.get("params", {})
        caller     = self.headers.get("X-Delegation-Chain", "unknown")
        if not skill_name:
            return self.send_json(400, {"error": "skill required"})
        code, result = run_skill(skill_name, params, caller)
        self.send_json(code, {"caller": caller, "skill": skill_name, "result": result})

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", 8080), Handler)
    print(f"agent listening on :8080, skills loaded: {list(_catalog)}", flush=True)
    server.serve_forever()
