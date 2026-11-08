"""Sinh scripts/auditor_engine/knowledge_pack.json từ INDEX.md và các tài liệu quyết định của kit (ADR-0018).

Pack là bản chụp có phiên bản để Health Check đối chiếu offline. Chạy lại mỗi khi tài liệu kit đổi
(`sync_docs.py` gọi tự động); `--check` trả mã lỗi nếu pack lệch tài liệu.
"""

from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripts" / "auditor_engine" / "knowledge_pack.json"
ROW = re.compile(r"^\|\s*([A-Z]-\d{3})\s*\|\s*([CPL])\s*\|\s*(.*?)\s*\|\s*\[[^\]]*\]\(([^)]+)\)\s*\|\s*$")
SECTIONS = {
    "when to choose": "when_to_choose", "when not to choose": "when_not_to_choose", "constraints": "constraints",
    "common mistakes": "common_mistakes", "adding a feature": "adding_a_feature", "upgrade indicators": "upgrade_indicators",
}
SCHEMA = 1


def _clean(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    return text.strip()


def parse_doc(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    info: dict = {}
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    body = text
    if m:
        body = text[m.end():]
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            if k.strip() in ("type", "not_when"):
                info[k.strip()] = v.strip().strip('"')
    t = re.search(r"^#\s+(.+)$", body, re.M)
    info["title"] = t.group(1).strip() if t else path.stem
    current = None
    sections: dict[str, list[str]] = {}
    for line in body.splitlines():
        h = re.match(r"^##\s+(.*)", line)
        if h:
            current = SECTIONS.get(re.sub(r"[^\w\s]", "", h.group(1)).strip().lower())
            continue
        if current and re.match(r"^\s*(?:[*\-]|\d+\.)\s+", line):
            sections.setdefault(current, []).append(_clean(re.sub(r"^\s*(?:[*\-]|\d+\.)\s+", "", line)))
    if sections:
        info["sections"] = {k: v[:8] for k, v in sections.items()}
    return info


def build() -> dict:
    docs = []
    index = (ROOT / "INDEX.md").read_text(encoding="utf-8")
    for line in index.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        doc_id, tier, when, rel = m.groups()
        entry = {"id": doc_id, "tier": tier, "when": _clean(when), "path": rel}
        p = ROOT / rel
        if p.is_file() and p.suffix == ".md":
            entry.update(parse_doc(p))
            if rel.startswith("profiles/architecture/") and entry.get("type") == "decision":
                entry["slug"] = p.stem
        docs.append(entry)
    return {"schema": SCHEMA, "kit_ref": "main", "docs": docs}


def main() -> int:
    pack = build()
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.is_file() else {}
    same = {k: v for k, v in old.items() if k != "generated"} == pack
    if "--check" in sys.argv:
        if not same:
            print("knowledge_pack.json lệch tài liệu kit: chạy python scripts/build_knowledge_pack.py")
            return 1
        print("knowledge_pack.json khớp tài liệu kit.")
        return 0
    if not same:
        pack["generated"] = datetime.date.today().isoformat()
        OUT.write_text(json.dumps(pack, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"Đã sinh knowledge_pack.json: {len(pack['docs'])} tài liệu.")
    else:
        print("knowledge_pack.json không đổi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
