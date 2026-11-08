"""AI Deep Review: an optional deep-analysis layer, needs network (ADR-0018).

Unlike the old version: the AI receives the Project Model + conclusions (structure, dependency graph, evidence), not just the score.
Source code is sent only when the user explicitly agrees (include_code) and secrets are always masked before sending.
Supports: Google Gemini, OpenAI, Anthropic Claude (standard library, no external dependency).
"""

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_MODELS = {"gemini": "gemini-2.0-flash", "openai": "gpt-4o", "claude": "claude-sonnet-5-5"}
TIMEOUT = 90
MAX_OUTPUT_TOKENS = 4096
MAX_CODE_FILES = 4
MAX_CODE_LINES = 80

_SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S),
    re.compile(r"(?i)((?:api[_-]?key|secret|token|passw(?:or)?d|authorization)[\"']?\s*[:=]\s*[\"']?)[^\s\"',;]{6,}"),
    re.compile(r"\b(sk-[A-Za-z0-9_\-]{16,}|AIza[0-9A-Za-z_\-]{20,}|AKIA[0-9A-Z]{12,}|gh[pousr]_[A-Za-z0-9]{20,})\b"),
]


def mask_secrets(text: str) -> str:
    text = _SECRET_PATTERNS[0].sub("[PRIVATE KEY REMOVED]", text)
    text = _SECRET_PATTERNS[1].sub(lambda m: m.group(1) + "[REDACTED]", text)
    return _SECRET_PATTERNS[2].sub("[REDACTED]", text)


def _code_excerpts(audit_data: dict) -> list[dict]:
    """Take the head of the largest files (hotspots), secrets masked. Called only when the user allows it."""
    root = Path(audit_data.get("target_dir", ""))
    out = []
    for hot in (audit_data.get("analysis", {}).get("hotspots", {}).get("large_files") or [])[:MAX_CODE_FILES]:
        p = (root / hot["file"]).resolve()
        try:
            p.relative_to(root.resolve())
            lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()[:MAX_CODE_LINES]
        except (OSError, ValueError):
            continue
        out.append({"file": hot["file"], "total_lines": hot["loc"], "head": mask_secrets("\n".join(lines))})
    return out


def build_prompt(audit_data: dict, include_code: bool = False, language: str = "en") -> str:
    a, ins = audit_data.get("analysis", {}), audit_data.get("insights", {})
    context = {
        "kind": a.get("kind"), "languages": a.get("languages"), "stack": a.get("stack"),
        "architecture": a.get("architecture"), "components": a.get("components"), "edges": a.get("edges"),
        "cycles": a.get("cycles"), "hotspots": a.get("hotspots"), "test_ratio": a.get("test_ratio"),
        "loc": {"code": a.get("code_loc"), "test": a.get("test_loc"), "docs": a.get("doc_loc")},
        "kit_profile_match": ins.get("profile"), "static_bottlenecks": ins.get("bottlenecks"),
        "static_strengths": ins.get("strengths"), "limits": ins.get("limits"),
        "rule_findings": (audit_data.get("findings") or [])[:20],
        "rule_score": {"total": audit_data.get("total_score"), "grade": audit_data.get("grade")},
    }
    excerpts = _code_excerpts(audit_data) if include_code else []
    code_block = ("\nCODE EXCERPTS (file heads, secrets masked):\n" + json.dumps(excerpts, ensure_ascii=False)) if excerpts else \
        "\n(No source code is attached; rely only on the static analysis model below.)"
    return (
        "You are a senior software architect reviewing a project that a user vibe-coded with an AI agent.\n"
        "The data below is the tool's STATIC ANALYSIS result (languages, stack from real imports, dependency graph, "
        "comparison with kit knowledge). Please:\n"
        "1. Judge whether the analysis model is reasonable and point out where it may be wrong (static analysis cannot see dynamic imports).\n"
        "2. Assess the real architecture, the biggest bottleneck and why it is dangerous for this project.\n"
        "3. Give an upgrade roadmap in small steps, each naming concrete files/components and how to verify it.\n"
        "Rely only on the provided data; do not invent files or components that are not in it. "
        f"Reply in {'Vietnamese' if language == 'vi' else 'English'}, concise, in Markdown.\n\n"
        "PROJECT MODEL:\n" + json.dumps(context, ensure_ascii=False) + code_block + "\n"
    )


def _http_json(url: str, payload: dict, headers: dict, provider: str) -> dict:
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")[:400]
        hint = {401: "Invalid API Key.", 403: "The API Key lacks permission or is blocked.",
                404: "The model does not exist for this key.", 429: "Rate limit or quota exceeded."}.get(e.code, "")
        raise RuntimeError(f"{provider} HTTP {e.code}. {hint} {body}".strip())
    except urllib.error.URLError as e:
        raise RuntimeError(f"Could not connect to {provider} (Internet required): {e.reason}")


def _call(provider: str, api_key: str, model: str, prompt: str, max_tokens: int) -> str:
    if provider == "gemini":
        data = _http_json(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
            {"contents": [{"parts": [{"text": prompt}]}],
             "generationConfig": {"temperature": 0.3, "maxOutputTokens": max_tokens}},
            {"x-goog-api-key": api_key}, "Gemini")
        return data["candidates"][0]["content"]["parts"][0]["text"]
    if provider == "openai":
        data = _http_json(
            "https://api.openai.com/v1/chat/completions",
            {"model": model, "temperature": 0.3, "max_tokens": max_tokens,
             "messages": [{"role": "system", "content": "You are a senior software architect."},
                          {"role": "user", "content": prompt}]},
            {"Authorization": f"Bearer {api_key}"}, "OpenAI")
        return data["choices"][0]["message"]["content"]
    if provider == "claude":
        data = _http_json(
            "https://api.anthropic.com/v1/messages",
            {"model": model, "max_tokens": max_tokens, "messages": [{"role": "user", "content": prompt}]},
            {"x-api-key": api_key, "anthropic-version": "2023-06-01"}, "Claude")
        return data["content"][0]["text"]
    raise RuntimeError(f"Unsupported provider: {provider}")


class LLMEvaluator:
    @staticmethod
    def evaluate(provider: str, api_key: str, model: str, audit_data: dict, include_code: bool = False, language: str = "en") -> dict:
        if not api_key or not api_key.strip():
            return {"success": False, "error": "No API Key entered. Open Settings > API Keys and enter your key."}
        if not audit_data.get("analysis"):
            return {"success": False, "error": "No analysis data yet. Run Health Check first."}
        try:
            prompt = build_prompt(audit_data, include_code, language)
            text = _call(provider, api_key.strip(), model or DEFAULT_MODELS.get(provider, ""), prompt, MAX_OUTPUT_TOKENS)
            return {"success": True, "analysis": text, "sent_code": include_code}
        except Exception as e:
            return {"success": False, "error": f"LLM API error: {e}"}

    @staticmethod
    def test_connection(provider: str, api_key: str, model: str) -> dict:
        """A very small test call to validate the key + model before the user waits for a long review."""
        if not api_key or not api_key.strip():
            return {"success": False, "error": "No API Key entered."}
        try:
            _call(provider, api_key.strip(), model or DEFAULT_MODELS.get(provider, ""), "Reply with the single word: ok", 32)
            return {"success": True, "message": "Connection OK: the API Key and model are valid."}
        except (KeyError, IndexError):
            # HTTP 200 but no text (e.g. a reasoning model used up its tokens): the key and model are still valid
            return {"success": True, "message": "Connection OK: the API Key and model are valid."}
        except Exception as e:
            return {"success": False, "error": str(e)}
