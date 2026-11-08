"""
Backend Server for Project Builder Analytics (Modern Antigravity 2.0 Web Shell)
Built on Python Standard Library (http.server + threading + json)
100% Zero-dependency & Offline-capable.
"""

import os
import sys
import time
import json
import urllib.error
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

from auditor_engine import ProjectAuditor
from reviewer_shell.settings_manager import SettingsManager
from reviewer_shell.llm_evaluator import LLMEvaluator
from reviewer_shell.connectivity import check_internet

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    STATIC_DIR = Path(sys._MEIPASS) / "reviewer_shell" / "static"
else:
    STATIC_DIR = Path(__file__).resolve().parent / "static"
CURRENT_VERSION = "0.1.0"  # must equal the GitHub release tag (v0.1.0); bump together

SHUTDOWN_EVENT = threading.Event()
_LAST_HEARTBEAT = time.time()
_WATCHDOG_TIMEOUT = 180.0


def record_heartbeat(timestamp: float | None = None) -> None:
    global _LAST_HEARTBEAT
    _LAST_HEARTBEAT = time.time() if timestamp is None else timestamp


def is_audit_running() -> bool:
    with _AUDIT_JOBS_LOCK:
        return any(j.get("state") == "running" for j in _AUDIT_JOBS.values())


def check_watchdog(now: float, last_heartbeat: float, timeout: float = 30.0, audit_running: bool = False) -> bool:
    if audit_running:
        return False
    return (now - last_heartbeat) >= timeout


def start_watchdog(shutdown_event: threading.Event, timeout: float = 30.0, check_interval: float = 1.0, clock=time.time) -> threading.Thread:
    def _watchdog_loop():
        last_tick = clock()
        suspension_threshold = max(10.0 * check_interval, 10.0)
        while not shutdown_event.is_set():
            time.sleep(check_interval)
            now = clock()
            tick_gap = now - last_tick
            last_tick = now

            if tick_gap > suspension_threshold:
                logger.info("System sleep/stall detected (tick gap %.1fs > %.1fs). Re-arming watchdog.", tick_gap, suspension_threshold)
                record_heartbeat(now)
                continue

            audit_active = is_audit_running()
            if check_watchdog(now, _LAST_HEARTBEAT, timeout=timeout, audit_running=audit_active):
                logger.info("Watchdog timeout (no heartbeat for %.1fs, no audit running) -> setting shutdown event.", timeout)
                shutdown_event.set()
                break
    t = threading.Thread(target=_watchdog_loop, daemon=True, name="HeartbeatWatchdog")
    t.start()
    return t

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
$dialog.Description = 'Select the project folder to check (Project Builder Analytics)'
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


# Các lượt quét chạy nền, UI hỏi tiến độ thật để không có cảm giác treo.
_AUDIT_JOBS = {}
_AUDIT_JOBS_LOCK = threading.Lock()
_MAX_AUDIT_JOBS = 8


def start_audit_job(target_dir):
    job = {"state": "running", "pct": 0, "message": "Starting...", "auditor": None,
           "result": None, "started": time.time(), "target_dir": str(target_dir)}
    job_id = os.urandom(8).hex()

    def progress(pct, msg):
        job["pct"], job["message"] = max(job["pct"], pct), msg

    def work():
        try:
            job["result"] = ReviewerAPIHandler.run_audit_to_result(
                target_dir, on_auditor=lambda a: job.__setitem__("auditor", a), progress=progress)
        except Exception as e:  # không để luồng nền chết mà UI vẫn chờ
            job["result"] = {"success": False, "error": f"Error while scanning the source code: {e}"}
        job["state"] = "done"

    with _AUDIT_JOBS_LOCK:
        for old in [k for k, v in _AUDIT_JOBS.items() if v["state"] == "done"][:max(0, len(_AUDIT_JOBS) - _MAX_AUDIT_JOBS + 1)]:
            _AUDIT_JOBS.pop(old, None)
        _AUDIT_JOBS[job_id] = job
    threading.Thread(target=work, daemon=True).start()
    return job_id


def audit_job_status(job_id, since=0):
    job = _AUDIT_JOBS.get(job_id)
    if job is None:
        return {"success": False, "error": "Scan session not found."}
    auditor = job["auditor"]
    logs = list(auditor.scan_logs) if auditor is not None else []
    status = {"success": True, "job_id": job_id, "state": job["state"], "pct": job["pct"], "message": job["message"],
              "target_dir": job.get("target_dir", ""),
              "elapsed": round(time.time() - job["started"], 1),
              "logs": logs[since:], "next": len(logs),
              "plan": list(auditor.scan_plan) if auditor is not None else [],
              "current": auditor.scan_current if auditor is not None else None}
    if job["state"] == "done":
        status["result"] = job["result"]
    return status


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

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        if not self._request_is_local():
            self.send_error(403, "Forbidden")
            return
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/status":
            self._send_json({"status": "ready", "version": CURRENT_VERSION})
        elif path == "/api/connectivity":
            self._send_json(check_internet())
        elif path == "/api/settings":
            self._send_json(mask_settings(SettingsManager.get_settings()))
        elif path == "/api/check-update":
            self._handle_check_update()
        elif path == "/api/audit-status":
            q = urllib.parse.parse_qs(parsed.query)
            try:
                since = max(0, int(q.get("since", ["0"])[0]))
            except ValueError:
                since = 0
            job_id = q.get("job", [""])[0]
            if not job_id:
                with _AUDIT_JOBS_LOCK:
                    if _AUDIT_JOBS:
                        job_id = list(_AUDIT_JOBS.keys())[-1]
            self._send_json(audit_job_status(job_id, since))
        else:
            # Phục vụ file tĩnh (HTML, CSS, JS)
            super().do_GET()

    def do_POST(self):
        if not self._request_is_local():
            # Đọc bỏ phần body chưa nhận để client không bị reset kết nối khi nhận 403
            try:
                self.rfile.read(min(int(self.headers.get("Content-Length", 0)), 1_000_000))
            except (ValueError, OSError):
                pass
            self.close_connection = True
            self.send_error(403, "Forbidden")
            return
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self._read_json_body()

        if path == "/api/heartbeat":
            record_heartbeat()
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
        elif path == "/api/update-knowledge":
            from auditor_engine.knowledge import update_pack
            self._send_json(update_pack(str(body.get("ref") or "main")))
        elif path == "/api/llm-test":
            self._handle_llm_test(body)

        elif path == "/api/open-report":
            report_path = body.get("path", "")
            if report_path and os.path.exists(report_path) and is_open_allowed(report_path):
                open_with_shell(report_path)
                self._send_json({"success": True})
            else:
                self._send_json({"success": False, "error": "The report file does not exist."})

        elif path == "/api/open-folder":
            folder_path = body.get("path", "")
            if folder_path and os.path.isdir(folder_path) and is_open_allowed(folder_path):
                open_with_shell(folder_path)
                self._send_json({"success": True})
            else:
                self._send_json({"success": False, "error": "The folder does not exist."})

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
            self._send_json({"success": False, "error": "The project folder is invalid or does not exist."})
            return

        if body.get("async"):
            # Chạy nền: UI hỏi tiến độ thật qua GET /api/audit-status thay vì chờ một request dài.
            self._send_json({"success": True, "job_id": start_audit_job(target_dir)})
            return

        self._send_json(self.run_audit_to_result(target_dir))

    @staticmethod
    def run_audit_to_result(target_dir, on_auditor=None, progress=None):
        """Chạy một lượt quét và trả về dict kết quả (success=False + error nếu lỗi)."""
        try:
            target_path = Path(target_dir).resolve()
            auditor = ProjectAuditor(target_path)
            if on_auditor:
                on_auditor(auditor)
            score = auditor.run(progress)
            report_file = auditor.generate_markdown_report(score)
            allow_open_path(report_file.resolve())
            allow_open_path(target_path)

            grade = auditor.get_letter_grade(score)
            report_data = auditor.serialize_report_data()

            def _cat(key, default_name, default_max):
                d = auditor.details.get(key) or {}
                p_obj = next((p for p in auditor.all_pillars if p.get('key') == key), None)
                has_crit = (p_obj.get('has_critical', False) if p_obj else d.get('has_critical', False))
                crit_cnt = (p_obj.get('critical_count', 0) if p_obj else d.get('critical_count', 0))
                return {
                    "name": d.get("name", default_name),
                    "score": d.get("points_earned", 0),
                    "max": d.get("max_points", default_max),
                    "is_na": d.get("is_na", key not in auditor.details),
                    "found": d.get("found", []),
                    "missing": d.get("missing", []),
                    "has_critical": has_crit,
                    "critical_count": crit_cnt,
                }

            categories = {
                "01_readme": _cat("readme", "Readme & Onboarding", 15),
                "02_backend": _cat("backend", "Backend & Core Flow", 20),
                "03_frontend": _cat("frontend", "Frontend & UI/UX", 20),
                "04_database": _cat("database", "Database & Query Safety", 15),
                "05_anticrash": _cat("anticrash", "Runtime Anti-Crash", 20),
                "06_contracts": _cat("contracts", "Hồ Sơ Kiến Trúc & Hợp Đồng API", 10),
                "07_agent_ecosystem": _cat("agent_ecosystem", "Hệ Sinh Thái AI Agent", 15),
                "08_security": _cat("security", "Bảo Mật & Chuỗi Cung Ứng", 15),
                "09_cloud": _cat("cloud", "Hạ Tầng Cloud & DevOps", 15),
                "10_microservices": _cat("microservices", "Hệ Thống Phân Tán & Gateway", 15),
                "11_data_caching": _cat("data_caching", "Kỹ Thuật Dữ Liệu & Cache", 15),
                "12_observability": _cat("observability", "Giám Sát & Vận Hành", 15),
            }

            result = {
                "success": True,
                "target_dir": str(target_path),
                "total_score": score,
                "grade": grade,
                "quality_gate": getattr(auditor, "quality_gate", "PASSED"),
                "critical_count": getattr(auditor, "critical_count", 0),
                "raw_score": getattr(auditor, "raw_score", score),
                "profiler": auditor.profile,
                "kit_config": report_data["kit_config"],
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
                "findings": report_data["findings"],
                "baseline": report_data["baseline"],
                "safety": report_data["safety"],
                "scope": report_data["scope"],
                "analysis": report_data["analysis"],
                "insights": report_data["insights"],
                "ai_prompt": auditor.get_ai_prompt(),
                "report_file": str(report_file.resolve()),
            }

            # Cập nhật thư mục gần nhất vào settings
            SettingsManager.save_settings({"last_target_directory": str(target_path)})
            return result

        except Exception as e:
            return {"success": False, "error": f"Error while scanning the source code: {str(e)}"}

    @staticmethod
    def _resolve_llm_key(body):
        provider = body.get("provider", "gemini")
        api_key = str(body.get("api_key", "")).strip()
        if not api_key:  # không truyền key thì dùng key đã lưu (UI không bao giờ nhận lại key)
            api_key = SettingsManager.get_settings().get(f"{provider}_api_key", "")
        return provider, api_key

    def _handle_llm_test(self, body):
        provider, api_key = self._resolve_llm_key(body)
        self._send_json(LLMEvaluator.test_connection(provider, api_key, body.get("model", "")))

    def _handle_llm_review(self, body):
        provider, api_key = self._resolve_llm_key(body)
        audit_data = body.get("audit_data", {})
        resp = LLMEvaluator.evaluate(provider, api_key, body.get("model", ""), audit_data,
                                     include_code=bool(body.get("include_code")),
                                     language=str(body.get("language") or "en"))
        if resp.get("success"):
            # Lưu kết quả AI cạnh báo cáo để không mất khi đóng ứng dụng
            target = audit_data.get("target_dir", "")
            if target and os.path.isdir(target):
                try:
                    out = Path(target) / "project-review-ai.md"
                    sent = "yes (secrets masked)" if resp.get("sent_code") else "no"
                    out.write_text(f"# AI Deep Review\n\n> Provider: {provider}. Source code included: {sent}.\n\n"
                                   f"{resp['analysis']}\n", encoding="utf-8")
                    allow_open_path(out.resolve())
                    resp["saved_to"] = str(out)
                except OSError:
                    pass
        self._send_json(resp)

    def _handle_check_update(self):
        try:
            url = "https://api.github.com/repos/Dokhacgiakhoa/Project-Builder-4-Agents/releases/latest"
            req = urllib.request.Request(url, headers={"User-Agent": "Project-Builder-Analytics"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                latest_tag = data.get("tag_name", f"v{CURRENT_VERSION}").lstrip("v")
                has_update = parse_version(latest_tag) > parse_version(CURRENT_VERSION)
                self._send_json({
                    "current_version": CURRENT_VERSION,
                    "latest_version": latest_tag,
                    "has_update": has_update,
                    "release_notes": data.get("body", "Latest version on GitHub."),
                    "html_url": data.get("html_url", "https://github.com/Dokhacgiakhoa/Project-Builder-4-Agents")
                })
        except urllib.error.HTTPError as e:
            # GitHub "latest" ignores pre-releases and drafts, so 404 means no stable release is published yet.
            msg = "No stable release has been published yet." if e.code == 404 else str(e)
            self._send_json({
                "current_version": CURRENT_VERSION,
                "latest_version": CURRENT_VERSION,
                "has_update": False,
                "error": msg
            })
        except Exception as e:
            self._send_json({
                "current_version": CURRENT_VERSION,
                "latest_version": CURRENT_VERSION,
                "has_update": False,
                "error": str(e)
            })


def start_server(port=8998, watchdog_timeout=180.0):
    record_heartbeat()
    server = ThreadingHTTPServer(("127.0.0.1", port), ReviewerAPIHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    if watchdog_timeout and watchdog_timeout > 0:
        start_watchdog(SHUTDOWN_EVENT, timeout=watchdog_timeout)
    return server, port, SHUTDOWN_EVENT
