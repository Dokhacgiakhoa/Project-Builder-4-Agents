"""English is the source language (ADR-0026): the engine must emit English only, and language packs must stay consistent."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from auditor_engine import ProjectAuditor  # noqa: E402

# Letters that only occur in Vietnamese (an accent like the "a" in "Diataxis" is not enough to flag a string).
VIETNAMESE = re.compile("[ăâêôơưđĂÂÊÔƠƯĐạảãậầẩẫắằẳẵặẹẻẽếềểễệịỉĩọỏõốồổỗộớờởỡợụủũứừửữựỳỵỷỹ]")
PACK_DIR = SCRIPTS / "reviewer_shell" / "static" / "js" / "lang"


def _project(tmp_path: Path) -> Path:
    """A project that exercises many engine branches, with English-only content of its own."""
    (tmp_path / "README.md").write_text("# Demo\n\nShort readme.\n", encoding="utf-8")
    (tmp_path / "app.py").write_text(
        "import os\n\ndef f():\n    try:\n        1 / 0\n    except Exception:\n        pass\n\n"
        "API_KEY = 'abcdef1234567890'\n", encoding="utf-8")
    (tmp_path / "package.json").write_text('{"name": "demo", "dependencies": {"express": "*"}}', encoding="utf-8")
    (tmp_path / ".env").write_text("TOKEN=abc\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "ui.tsx").write_text("export const A = () => <div/>;\n", encoding="utf-8")
    return tmp_path


def test_report_and_ui_data_contain_no_vietnamese(tmp_path):
    auditor = ProjectAuditor(_project(tmp_path))
    score = auditor.run()
    report = auditor.generate_markdown_report(score).read_text(encoding="utf-8")
    bad = [line for line in report.splitlines() if VIETNAMESE.search(line)]
    assert not bad, "Vietnamese text in the engine report: " + " | ".join(bad[:5])

    ui_data = json.dumps({"pillars": auditor.all_pillars, "log": auditor.get_logs() if hasattr(auditor, "get_logs") else "",
                          "profile": auditor.profile}, ensure_ascii=False, default=str)
    assert not VIETNAMESE.search(ui_data), "Vietnamese text in the data sent to the UI"


def test_severity_values_are_english(tmp_path):
    auditor = ProjectAuditor(_project(tmp_path))
    auditor.run()
    severities = {f.severity for f in auditor.collect_findings()}
    assert severities and severities <= {"High", "Medium", "Low"}


def _load_pack(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return json.loads(text[text.index("= {") + 2: text.rindex(";")])


@pytest.mark.parametrize("pack_file", sorted(PACK_DIR.glob("*.engine.js")), ids=lambda p: p.name)
def test_language_pack_is_consistent(pack_file):
    pack = _load_pack(pack_file)
    assert pack["exact"] and pack["templates"]
    # English is the key: no key may be written in the target language.
    assert not [k for k in pack["exact"] if VIETNAMESE.search(k)]
    seen = set()
    for t in pack["templates"]:
        assert t["en"] not in seen, f"duplicate template: {t['en'][:60]}"
        seen.add(t["en"])
        assert not VIETNAMESE.search(t["en"]), f"template key is not English: {t['en'][:60]}"
        en_names = set(re.findall(r"\{(p\d+)\}", t["en"]))
        tr_names = set(re.findall(r"\{(p\d+)\}", t["tr"]))
        assert tr_names <= en_names, f"translation uses placeholders the English template lacks: {t['en'][:60]}"
        assert en_names, f"template without placeholders belongs in 'exact': {t['en'][:60]}"
