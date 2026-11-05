"""
Settings Manager for Project Reviewer
Persists user configuration (Theme, LLM API keys, Rule Overrides)
Storage location: ~/.starter-kit/settings.json
"""

import json
import os
from pathlib import Path

SETTINGS_DIR = Path.home() / ".starter-kit"
SETTINGS_FILE = SETTINGS_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "theme": "dark",  # "dark" | "light"
    "llm_provider": "gemini",  # "gemini" | "openai" | "claude"
    "gemini_api_key": "",
    "openai_api_key": "",
    "claude_api_key": "",
    "selected_model": "gemini-2.0-flash",
    "auto_check_updates": True,
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
            
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(current, f, indent=2, ensure_ascii=False)
            return True, "Cấu hình đã được lưu thành công."
        except Exception as e:
            return False, f"Không thể lưu cấu hình: {e}"
