"""
Backend Server for Project Reviewer (Modern Antigravity 2.0 Web Shell)
Built on Python Standard Library (http.server + threading + json)
100% Zero-dependency & Offline-capable.
"""

import os
import sys
import time
import json
import urllib.parse
import urllib.request
import subprocess
import threading
import logging
import platform
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# Thêm đường dẫn scripts vào sys.path để import project_auditor
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from project_auditor import ProjectAuditor
from reviewer_shell.settings_manager import SettingsManager
from reviewer_shell.llm_evaluator import LLMEvaluator

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    STATIC_DIR = Path(sys._MEIPASS) / "reviewer_shell" / "static"
else:
    STATIC_DIR = Path(__file__).resolve().parent / "static"
CURRENT_VERSION = "2.1.0"

SHUTDOWN_EVENT = threading.Event()

logger = logging.getLogger("reviewer_shell")

MAX_BODY_BYTES = 2 * 1024 * 1024  # 2 MB
API_KEY_FIELDS = ("gemini_api_key", "openai_api_key", "claude_api_key")

# Chỉ cho phép mở các đường dẫn do chính server này sinh ra (báo cáo / thư mục đã quét).
_ALLOWED_OPEN_PATHS = set()
_ALLOWED_LOCK = threading.Lock()


def _norm_path(p):
    return os.path.normcase(os.path.realpath(str(p)))


def allow_open_path(p):
    with _ALLOWED_LOCK:
        _ALLOWED_OPEN_PATHS.add(_norm_path(p))


def is_open_allowed(p):
    with _ALLOWED_LOCK:
        return _norm_path(p) in _ALLOWED_OPEN_PATHS


def open_with_shell(path):
    """Mở tệp/thư mục bằng ứng dụng mặc định của hệ điều hành."""
    if hasattr(os, "startfile"):
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def parse_version(v):
    """'2.10.0' -> (2, 10, 0); các thành phần không phải số được coi là 0."""
    parts = []
    for chunk in str(v).lstrip("vV").split("."):
        digits = "".join(ch for ch in chunk if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def mask_settings(settings):
    """Không bao giờ trả API key về trình duyệt; chỉ báo đã cấu hình hay chưa."""
    safe = dict(settings)
    for field in API_KEY_FIELDS:
        safe["has_" + field] = bool(str(safe.get(field, "")).strip())
        safe[field] = ""
    return safe


def choose_folder_native(initial_dir=""):
    """Mở hộp thoại chọn thư mục gốc Windows qua PowerShell."""
    try:
        ps_code = """
Add-Type -AssemblyName System.Windows.Forms
$dialog = New-Object System.Windows.Forms.FolderBrowserDialog
$dialog.Description = 'Chọn thư mục dự án cần Benchmark'
$dialog.ShowNewFolderButton = $false
if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    Write-Output $dialog.SelectedPath
}
"""
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_code],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        folder = res.stdout.strip()
        if folder and os.path.isdir(folder):
            return folder
    except Exception as e:
        print(f"[FolderPicker] Error: {e}")
    return None


class ReviewerAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def log_message(self, format, *args):
        # Ẩn bớt console log để giữ terminal sạch
        pass

    def _request_is_local(self):
        """Chặn truy cập chéo trang (CSRF) và DNS rebinding: Host/Origin phải là loopback."""
        port = self.server.server_address[1]
        allowed_hosts = {f"127.0.0.1:{port}", f"localhost:{port}", f"[::1]:{port}"}
        if (self.headers.get("Host") or "").lower() not in allowed_hosts:
            return False
        origin = self.headers.get("Origin")
        if origin is not None and origin.lower() not in {f"http://{h}" for h in allowed_hosts}:
            return False
        return True

    def do_GET(self):
        if not self._request_is_local():
            self.send_error(403, "Forbidden")
            return
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/status":
            self._send_json({"status": "ready", "version": CURRENT_VERSION})
        elif path == "/api/settings":
            self._send_json(mask_settings(SettingsManager.get_settings()))
        elif path == "/api/check-update":
            self._handle_check_update()
        else:
            # Phục vụ file tĩnh (HTML, CSS, JS)
            super().do_GET()

    def do_POST(self):
        if not self._request_is_local():
            self.send_error(403, "Forbidden")
            return
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self._read_json_body()

        if path == "/api/heartbeat":
            self._send_json({"status": "alive"})

        elif path == "/api/shutdown":
            SHUTDOWN_EVENT.set()
            self._send_json({"status": "shutting down"})

        elif path == "/api/select-folder":
            folder = choose_folder_native(body.get("initial", ""))
            self._send_json({"folder": folder})

        elif path == "/api/settings":
            updates = dict(body)
            for field in API_KEY_FIELDS:
                # Khóa rỗng nghĩa là "giữ nguyên khóa đã lưu" (UI không bao giờ nhận lại khóa).
                if not str(updates.get(field, "")).strip():
                    updates.pop(field, None)
                else:
                    updates[field] = str(updates[field]).strip()
            for k in [k for k in updates if k.startswith("has_")]:
                updates.pop(k, None)
            ok, msg = SettingsManager.save_settings(updates)
            self._send_json({"success": ok, "message": msg})

        elif path == "/api/run-audit":
            self._handle_run_audit(body)

        elif path == "/api/open-report":
            report_path = body.get("path", "")
            if report_path and os.path.exists(report_path) and is_open_allowed(report_path):
                open_with_shell(report_path)
                self._send_json({"success": True})
            else:
                self._send_json({"success": False, "error": "Tệp báo cáo không tồn tại."})

        elif path == "/api/open-folder":
            folder_path = body.get("path", "")
            if folder_path and os.path.isdir(folder_path) and is_open_allowed(folder_path):
                open_with_shell(folder_path)
                self._send_json({"success": True})
            else:
                self._send_json({"success": False, "error": "Thư mục không tồn tại."})

        elif path == "/api/llm-review":
            self._handle_llm_review(body)

        else:
            self.send_error(404, "Endpoint not found")

    def _read_json_body(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length > MAX_BODY_BYTES:
                logger.warning("Request body quá lớn: %s bytes", length)
                return {}
            if length > 0:
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                return data if isinstance(data, dict) else {}
        except Exception as e:
            logger.warning("Không đọc được JSON body: %s", e)
        return {}

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _handle_run_audit(self, body):
        target_dir = body.get("target_dir", "").strip()
        if not target_dir or not os.path.isdir(target_dir):
            self._send_json({"success": False, "error": "Thư mục dự án không hợp lệ hoặc không tồn tại."})
            return

        try:
            target_path = Path(target_dir).resolve()
            auditor = ProjectAuditor(target_path)
            score = auditor.run()
            report_file = auditor.generate_markdown_report(score)
            allow_open_path(report_file.resolve())
            allow_open_path(target_path)

            # Chuẩn hóa dữ liệu trả về cho Frontend UI
            grade = auditor.get_letter_grade(score)
            
            categories = {
                "01_readme": {
                    "name": "Readme & Onboarding",
                    "score": auditor.details.get('readme', {}).get('points_earned', 0),
                    "max": auditor.details.get('readme', {}).get('max_points', 15),
                    "is_na": auditor.details.get('readme', {}).get('is_na', False),
                    "found": auditor.details.get('readme', {}).get('found', []),
                    "missing": auditor.details.get('readme', {}).get('missing', [])
                },
                "02_backend": {
                    "name": "Backend & Core Flow",
                    "score": auditor.details.get('backend', {}).get('points_earned', 0),
                    "max": auditor.details.get('backend', {}).get('max_points', 20),
                    "is_na": auditor.details.get('backend', {}).get('is_na', False),
                    "found": auditor.details.get('backend', {}).get('found', []),
                    "missing": auditor.details.get('backend', {}).get('missing', [])
                },
                "03_frontend": {
                    "name": "Frontend & UI/UX",
                    "score": auditor.details.get('frontend', {}).get('points_earned', 0),
                    "max": auditor.details.get('frontend', {}).get('max_points', 20),
                    "is_na": auditor.details.get('frontend', {}).get('is_na', False),
                    "found": auditor.details.get('frontend', {}).get('found', []),
                    "missing": auditor.details.get('frontend', {}).get('missing', [])
                },
                "04_database": {
                    "name": "Database & Query Safety",
                    "score": auditor.details.get('database', {}).get('points_earned', 0),
                    "max": auditor.details.get('database', {}).get('max_points', 15),
                    "is_na": auditor.details.get('database', {}).get('is_na', False),
                    "found": auditor.details.get('database', {}).get('found', []),
                    "missing": auditor.details.get('database', {}).get('missing', [])
                },
                "05_anticrash": {
                    "name": "Runtime Anti-Crash",
                    "score": auditor.details.get('anti_crash', {}).get('points_earned', 0),
                    "max": auditor.details.get('anti_crash', {}).get('max_points', 20),
                    "is_na": auditor.details.get('anti_crash', {}).get('is_na', False),
                    "found": auditor.details.get('anti_crash', {}).get('found', []),
                    "missing": auditor.details.get('anti_crash', {}).get('missing', [])
                },
                "06_contracts": {
                    "name": "Hồ Sơ Kiến Trúc & Hợp Đồng API",
                    "score": auditor.details.get('contracts', {}).get('points_earned', 0),
                    "max": auditor.details.get('contracts', {}).get('max_points', 10),
                    "is_na": auditor.details.get('contracts', {}).get('is_na', False),
                    "found": auditor.details.get('contracts', {}).get('found', []),
                    "missing": auditor.details.get('contracts', {}).get('missing', [])
                },
                "07_agent_ecosystem": {
                    "name": "Hệ Sinh Thái AI Agent",
                    "score": auditor.details.get('agent_ecosystem', {}).get('points_earned', 0),
                    "max": auditor.details.get('agent_ecosystem', {}).get('max_points', 15),
                    "is_na": auditor.details.get('agent_ecosystem', {}).get('is_na', False),
                    "found": auditor.details.get('agent_ecosystem', {}).get('found', []),
                    "missing": auditor.details.get('agent_ecosystem', {}).get('missing', [])
                },
            }

            result = {
                "success": True,
                "target_dir": str(target_path),
                "total_score": score,
                "grade": grade,
                "profiler": auditor.profile,
                "all_pillars": auditor.all_pillars,
                "active_pillars": auditor.active_pillars,
                "scan_logs": auditor.scan_logs,
                "total_files": len(auditor.tree.all_files),
                "code_files": len(auditor.tree.code_files),
                "categories": categories,
                "strengths": auditor.innovations if auditor.innovations else auditor.details.get('readme', {}).get('found', []),
                "gaps": auditor.gaps,
                "bloat": auditor.bloat,
                "violations": auditor.violations,
                "ai_prompt": auditor.get_ai_prompt(),
                "report_file": str(report_file.resolve())
            }

            # Cập nhật thư mục gần nhất vào settings
            SettingsManager.save_settings({"last_target_directory": str(target_path)})
            self._send_json(result)

        except Exception as e:
            self._send_json({"success": False, "error": f"Lỗi trong quá trình quét mã nguồn: {str(e)}"})

    def _handle_llm_review(self, body):
        provider = body.get("provider", "gemini")
        api_key = body.get("api_key", "").strip()
        model = body.get("model", "")
        audit_data = body.get("audit_data", {})

        # Nếu không truyền API key thì thử lấy từ settings
        if not api_key:
            settings = SettingsManager.get_settings()
            key_field = f"{provider}_api_key"
            api_key = settings.get(key_field, "")

        resp = LLMEvaluator.evaluate(provider, api_key, model, audit_data)
        self._send_json(resp)

    def _handle_check_update(self):
        try:
            url = "https://api.github.com/repos/Dokhacgiakhoa/Project-Starter-Kit/releases/latest"
            req = urllib.request.Request(url, headers={"User-Agent": "Project-Reviewer-App"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                latest_tag = data.get("tag_name", "v2.1.0").lstrip("v")
                has_update = parse_version(latest_tag) > parse_version(CURRENT_VERSION)
                self._send_json({
                    "current_version": CURRENT_VERSION,
                    "latest_version": latest_tag,
                    "has_update": has_update,
                    "release_notes": data.get("body", "Phiên bản mới nhất trên GitHub."),
                    "html_url": data.get("html_url", "https://github.com/Dokhacgiakhoa/Project-Starter-Kit")
                })
        except Exception as e:
            self._send_json({
                "current_version": CURRENT_VERSION,
                "latest_version": CURRENT_VERSION,
                "has_update": False,
                "error": str(e)
            })


def start_server(port=8998):
    server = ThreadingHTTPServer(("127.0.0.1", port), ReviewerAPIHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    return server, port, SHUTDOWN_EVENT
