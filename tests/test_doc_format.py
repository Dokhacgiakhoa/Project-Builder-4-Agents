"""Document format tests for Agents (frontmatter, mandatory sections, match with INDEX)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check_links  # noqa: E402

SECTIONS = ["When to choose", "When not to choose", "Target directory", "Constraints", "Adding a feature", "Common mistakes"]


def make_repo(tmp_path, body, frontmatter, index_id="A-001"):
    (tmp_path / "INDEX.md").write_text(
        f"| ID | Tier | When to use | Document |\n| {index_id} | P | demo | [x](profiles/architecture/x.md) |\n", encoding="utf-8")
    doc = tmp_path / "profiles" / "architecture" / "x.md"
    doc.parent.mkdir(parents=True)
    doc.write_text(frontmatter + body, encoding="utf-8")
    return doc


GOOD_FM = '---\nid: A-001\ntype: decision\nwhen: "demo"\nnot_when: "large"\n---\n'
GOOD_BODY = "# X\n\n" + "".join(f"## {s}\ncontent\n\n" for s in SECTIONS)


def test_real_repo_docs_follow_the_format():
    assert check_links.check_doc_format() == []


def test_good_decision_doc_passes(tmp_path):
    doc = make_repo(tmp_path, GOOD_BODY, GOOD_FM)
    assert check_links.check_doc_format(tmp_path, [doc]) == []


def test_numbered_headings_are_accepted(tmp_path):
    body = "# X\n\n" + "".join(f"## {i}. {s}\ncontent\n\n" for i, s in enumerate(SECTIONS, 1))
    doc = make_repo(tmp_path, body, GOOD_FM)
    assert check_links.check_doc_format(tmp_path, [doc]) == []


def test_missing_frontmatter_is_reported(tmp_path):
    doc = make_repo(tmp_path, GOOD_BODY, "")
    assert any("missing frontmatter" in e for e in check_links.check_doc_format(tmp_path, [doc]))


def test_decision_missing_section_and_not_when(tmp_path):
    fm = '---\nid: A-001\ntype: decision\nwhen: "demo"\n---\n'
    doc = make_repo(tmp_path, GOOD_BODY.replace("## Constraints", "## Other"), fm)
    errors = " | ".join(check_links.check_doc_format(tmp_path, [doc]))
    assert "not_when" in errors and "constraints" in errors


def test_id_mismatch_with_index_is_reported(tmp_path):
    doc = make_repo(tmp_path, GOOD_BODY, GOOD_FM, index_id="A-009")
    assert any("differs from INDEX.md" in e for e in check_links.check_doc_format(tmp_path, [doc]))


def test_doc_not_in_index_is_reported(tmp_path):
    doc = make_repo(tmp_path, GOOD_BODY, GOOD_FM)
    other = doc.with_name("y.md")
    other.write_text(GOOD_FM + GOOD_BODY, encoding="utf-8")
    assert any("no row in INDEX.md" in e for e in check_links.check_doc_format(tmp_path, [other]))


def test_decision_too_long_is_reported(tmp_path):
    doc = make_repo(tmp_path, GOOD_BODY + "line\n" * 130, GOOD_FM)
    assert any("longer than" in e for e in check_links.check_doc_format(tmp_path, [doc]))


def test_invalid_type_is_reported(tmp_path):
    fm = GOOD_FM.replace("type: decision", "type: essay")
    doc = make_repo(tmp_path, GOOD_BODY, fm)
    assert any("invalid type" in e for e in check_links.check_doc_format(tmp_path, [doc]))
