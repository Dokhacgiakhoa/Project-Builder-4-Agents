"""
Settings Manager for Project Builder Analytics
Persists user configuration (Theme, LLM API keys, Rule Overrides)
Storage location: ~/.starter-kit/settings.json
"""

import json
import os
from pathlib import Path

KEY_FIELDS = ("gemini_api_key", "openai_api_key", "claude_api_key")
PREFIX = "dpapi:"


def _protect(value: str) -> str:
    """Mã hóa API key bằng DPAPI của Windows (gắn với tài khoản người dùng). Nền tảng khác: giữ nguyên + chmod 600."""
    if not value or value.startswith(PREFIX) or os.name != "nt":
        return value
    try:
        import base64
        import ctypes
        from ctypes import wintypes

        class Blob(ctypes.Structure):
            _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

        raw = value.encode("utf-8")
        buf = ctypes.create_string_buffer(raw, len(raw))
        src = Blob(len(raw), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))
        out = Blob()
        if not ctypes.windll.crypt32.CryptProtectData(ctypes.byref(src), None, None, None, None, 0, ctypes.byref(out)):
            return value
        data = ctypes.string_at(out.pbData, out.cbData)
        ctypes.windll.kernel32.LocalFree(out.pbData)
        return PREFIX + base64.b64encode(data).decode("ascii")
    except Exception:
        return value


def _unprotect(value: str) -> str:
    if not value or not value.startswith(PREFIX) or os.name != "nt":
        return value
    try:
        import base64
        import ctypes
        from ctypes import wintypes

        class Blob(ctypes.Structure):
            _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

        raw = base64.b64decode(value[len(PREFIX):])
        buf = ctypes.create_string_buffer(raw, len(raw))
        src = Blob(len(raw), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))
        out = Blob()
        if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(src), None, None, None, None, 0, ctypes.byref(out)):
            return ""
        data = ctypes.string_at(out.pbData, out.cbData)
        ctypes.windll.kernel32.LocalFree(out.pbData)
        return data.decode("utf-8")
    except Exception:
        return ""


SETTINGS_DIR = Path.home() / ".starter-kit"
SETTINGS_FILE = SETTINGS_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "theme": "dark",  # "dark" | "light"
    "language": "en",  # "en" (default) | "vi"
    "llm_provider": "gemini",  # "gemini" | "openai" | "claude"
    "gemini_api_key": "",
    "openai_api_key": "",
    "claude_api_key": "",
    "selected_model": "gemini-2.0-flash",
    "auto_check_updates": True,
    "include_code": False,
    "last_target_directory": ""
}


class SettingsManager:
    @staticmethod
    def get_settings():
        try:
            if not SETTINGS_FILE.exists():
                SettingsManager.save_settings(DEFAULT_SETTINGS)
                return DEFAULT_SETTINGS.copy()
            
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                merged = DEFAULT_SETTINGS.copy()
                merged.update(saved)
                for k in KEY_FIELDS:
                    merged[k] = _unprotect(str(merged.get(k, "")))
                return merged
        except Exception as e:
            print(f"[SettingsManager] Lỗi đọc cấu hình: {e}")
            return DEFAULT_SETTINGS.copy()

    @staticmethod
    def save_settings(new_settings: dict):
        try:
            SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
            current = SettingsManager.get_settings()
            current.update(new_settings)

            to_write = dict(current)
            for k in KEY_FIELDS:
                to_write[k] = _protect(str(to_write.get(k, "")))
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(to_write, f, indent=2, ensure_ascii=False)
            try:
                os.chmod(SETTINGS_FILE, 0o600)
            except OSError:
                pass
            return True, "Settings saved."
        except Exception as e:
            return False, f"Could not save settings: {e}"
