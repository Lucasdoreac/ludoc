"""ACP Client para comunicação inter-agentes"""
import json, urllib.request, urllib.error

class ACPClient:
    def __init__(self, registry=None):
        self.registry = registry or {}

    def discover(self, agent_url):
        """Descobre capacidades de um agente remoto"""
        try:
            req = urllib.request.Request(
                f"{agent_url}/acp/discover",
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as r:
                return json.loads(r.read())
        except Exception as e:
            return {"error": str(e)}

    def negotiate(self, agent_url, capabilities):
        """Negocia capacidades com agente remoto"""
        try:
            req = urllib.request.Request(
                f"{agent_url}/acp/negotiate",
                data=json.dumps({"capabilities": capabilities}).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as r:
                return json.loads(r.read())
        except Exception as e:
            return {"error": str(e)}

    def execute(self, agent_url, skill, params):
        """Executa skill em agente remoto"""
        try:
            req = urllib.request.Request(
                f"{agent_url}/acp/execute",
                data=json.dumps({"skill": skill, "params": params}).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, {"error": str(e.reason)}
        except Exception as e:
            return 500, {"error": str(e)}
