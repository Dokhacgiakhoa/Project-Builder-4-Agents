"""
AI LLM Evaluator for Deep Architectural Review
Supports: Google Gemini, OpenAI, Anthropic Claude
"""

import json
import urllib.request
import urllib.error


class LLMEvaluator:
    @staticmethod
    def evaluate(provider: str, api_key: str, model: str, audit_data: dict) -> dict:
        """
        Gửi dữ liệu benchmark cho LLM để phân tích chuyên sâu và đưa ra lời khuyên kiến trúc.
        """
        if not api_key or not api_key.strip():
            return {
                "success": False,
                "error": "Chưa nhập API Key. Vui lòng mở Cài đặt (Settings) và nhập API Key của bạn."
            }

        prompt = f"""
Bạn là Senior Principal Software Architect. Hãy đọc kết quả thẩm định kiến trúc mã nguồn dưới đây và đưa ra:
1. Đánh giá tổng quan về rủi ro kiến trúc lớn nhất của dự án.
2. Top 3 hành động cần làm ngay để refactor theo chuẩn Clean Architecture & Anti-Crash.
3. Kế hoạch từng bước để xử lý các vi phạm cụ thể.

DỮ LIỆU THẨM ĐỊNH (AUDIT DATA):
- Điểm tổng: {audit_data.get('total_score', 0)} / 100
- Xếp hạng: {audit_data.get('grade', 'N/A')}
- Loại hình dự án: {audit_data.get('profiler', {}).get('archetype', 'N/A')}
- Tech Stack: {json.dumps(audit_data.get('profiler', {}), ensure_ascii=False)}
- Điểm từng hạng mục: {json.dumps(audit_data.get('categories', {}), ensure_ascii=False)}
- Khoảng trống (Gaps): {json.dumps(audit_data.get('gaps', []), ensure_ascii=False)}
- Rác & Vi phạm (Bloat): {json.dumps(audit_data.get('bloat', []), ensure_ascii=False)}
- Danh sách vi phạm mã nguồn: {json.dumps(audit_data.get('violations', [])[:15], ensure_ascii=False)}

Hãy trả lời bằng tiếng Việt, súc tích, chuyên nghiệp, định dạng Markdown rõ ràng.
"""

        try:
            if provider == "gemini":
                return LLMEvaluator._call_gemini(api_key, model or "gemini-2.0-flash", prompt)
            elif provider == "openai":
                return LLMEvaluator._call_openai(api_key, model or "gpt-4o", prompt)
            elif provider == "claude":
                return LLMEvaluator._call_claude(api_key, model or "claude-3-5-sonnet-20241022", prompt)
            else:
                return {"success": False, "error": f"Nhà cung cấp không hỗ trợ: {provider}"}
        except Exception as e:
            return {"success": False, "error": f"Lỗi gọi LLM API: {str(e)}"}

    @staticmethod
    def _call_gemini(api_key: str, model: str, prompt: str) -> dict:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 2048
            }
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return {"success": True, "analysis": text}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            return {"success": False, "error": f"Gemini HTTP {e.code}: {err_body}"}

    @staticmethod
    def _call_openai(api_key: str, model: str, prompt: str) -> dict:
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a Senior Principal Software Architect."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["choices"][0]["message"]["content"]
                return {"success": True, "analysis": text}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            return {"success": False, "error": f"OpenAI HTTP {e.code}: {err_body}"}

    @staticmethod
    def _call_claude(api_key: str, model: str, prompt: str) -> dict:
        url = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": model,
            "max_tokens": 2048,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["content"][0]["text"]
                return {"success": True, "analysis": text}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            return {"success": False, "error": f"Claude HTTP {e.code}: {err_body}"}
