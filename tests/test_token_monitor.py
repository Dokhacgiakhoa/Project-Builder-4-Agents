"""Tests for scripts/token_monitor (pure engine)."""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from token_monitor import (  # noqa: E402
    Aggregator, TranscriptTailer, find_transcripts, parse_line, project_dir_name,
)

T0 = datetime(2026, 11, 7, 10, 0, 0, tzinfo=timezone.utc)


def rec(msg_id="m1", req="r1", ts=T0, inp=10, cc=100, cr=1000, out=50, model="claude-x", side=False, typ="assistant"):
    return json.dumps({
        "type": typ, "timestamp": ts.isoformat().replace("+00:00", "Z"), "requestId": req, "isSidechain": side,
        "sessionId": "s1",
        "message": {"id": msg_id, "model": model, "usage": {
            "input_tokens": inp, "cache_creation_input_tokens": cc, "cache_read_input_tokens": cr, "output_tokens": out}},
    })


def test_parse_line_extracts_fields():
    e = parse_line(rec())
    assert (e.input_tokens, e.cache_creation, e.cache_read, e.output_tokens) == (10, 100, 1000, 50)
    assert e.context_tokens == 1110 and e.new_tokens == 160 and e.model == "claude-x"


def test_parse_line_ignores_noise():
    assert parse_line("") is None
    assert parse_line("not json {usage") is None
    assert parse_line(rec(typ="user")) is None
    assert parse_line(json.dumps({"type": "assistant", "message": {"usage": {}}})) is None  # no timestamp
    assert parse_line(json.dumps({"type": "assistant", "timestamp": "bad", "message": {"usage": {"output_tokens": 1}}})) is None


def test_negative_or_non_int_values_become_zero():
    d = json.loads(rec())
    d["message"]["usage"]["output_tokens"] = -5
    d["message"]["usage"]["input_tokens"] = "x"
    e = parse_line(json.dumps(d))
    assert e.output_tokens == 0 and e.input_tokens == 0


def test_duplicates_counted_once():
    agg = Aggregator()
    for _ in range(4):  # same response written once per content block
        agg.add(parse_line(rec()))
    s = agg.snapshot()
    assert s.totals.turns == 1 and s.totals.output_tokens == 50 and s.totals.cache_read == 1000


def test_duplicate_keeps_largest_output():
    agg = Aggregator()
    agg.add(parse_line(rec(out=5)))
    agg.add(parse_line(rec(out=80)))
    agg.add(parse_line(rec(out=20)))
    assert agg.snapshot().totals.output_tokens == 80


def test_distinct_turns_sum_and_context_is_latest():
    agg = Aggregator()
    agg.add(parse_line(rec("m1", "r1", T0, cr=1000)))
    agg.add(parse_line(rec("m2", "r2", T0 + timedelta(minutes=1), cr=5000)))
    s = agg.snapshot()
    assert s.totals.turns == 2 and s.totals.cache_read == 6000
    assert s.context_now == 10 + 100 + 5000 and s.context_peak == s.context_now


def test_burn_rate_uses_recent_window_only():
    agg = Aggregator()
    agg.add(parse_line(rec("old", "r0", T0 - timedelta(hours=2), cc=1_000_000)))
    agg.add(parse_line(rec("a", "ra", T0, inp=0, cc=0, out=100)))
    agg.add(parse_line(rec("b", "rb", T0 + timedelta(minutes=2), inp=0, cc=0, out=100)))
    s = agg.snapshot(window_min=10)
    assert round(s.output_tokens_per_min) == 100  # 200 tokens over 2 minutes
    assert s.new_tokens_per_min < 1000            # the 1M-token old turn is excluded


def test_top_turns_ordered_by_new_tokens():
    agg = Aggregator()
    agg.add(parse_line(rec("a", "ra", T0, cc=10)))
    agg.add(parse_line(rec("b", "rb", T0 + timedelta(minutes=1), cc=9999)))
    agg.add(parse_line(rec("c", "rc", T0 + timedelta(minutes=2), cc=500)))
    assert [e.message_id for e in agg.snapshot(top_n=2).top_turns] == ["b", "c"]


def test_sidechain_can_be_excluded():
    agg = Aggregator()
    agg.add(parse_line(rec("a", "ra", T0, out=10)))
    agg.add(parse_line(rec("b", "rb", T0 + timedelta(minutes=1), out=90, side=True)))
    assert agg.snapshot().totals.output_tokens == 100
    assert agg.snapshot(include_sidechain=False).totals.output_tokens == 10


def test_empty_snapshot_is_safe():
    s = Aggregator().snapshot()
    assert s.totals.turns == 0 and s.context_now == 0 and s.top_turns == []


def test_records_without_ids_do_not_crash_and_warn():
    d = json.loads(rec())
    d["message"]["id"] = ""
    d.pop("requestId")
    agg = Aggregator()
    agg.add(parse_line(json.dumps(d)))
    assert "approximate" in agg.snapshot().warnings[0]


def test_project_dir_name_matches_claude_code_convention():
    assert project_dir_name(r"D:\Github\Project-Builder-4-Agents") == "D--Github-Project-Builder-4-Agents"


def test_tailer_reads_only_new_and_handles_partial_lines(tmp_path):
    f = tmp_path / "s.jsonl"
    f.write_text("a\nb\n", encoding="utf-8")
    t = TranscriptTailer()
    assert t.read_new(f) == ["a", "b"]
    assert t.read_new(f) == []
    with open(f, "a", encoding="utf-8") as fh:
        fh.write("c\npart")
    assert t.read_new(f) == ["c"]            # incomplete line is held back
    with open(f, "a", encoding="utf-8") as fh:
        fh.write("ial\n")
    assert t.read_new(f) == ["partial"]
    f.write_text("z\n", encoding="utf-8")    # truncation/replace restarts from the beginning
    assert t.read_new(f) == ["z"]


def test_tailer_missing_file_is_empty(tmp_path):
    assert TranscriptTailer().read_new(tmp_path / "nope.jsonl") == []


def test_find_transcripts_newest_first(tmp_path):
    proj = tmp_path / project_dir_name(r"C:\x\app")
    proj.mkdir()
    a, b = proj / "a.jsonl", proj / "b.jsonl"
    a.write_text("1")
    b.write_text("2")
    import os
    os.utime(a, (1, 1))
    assert [p.name for p in find_transcripts(tmp_path, r"C:\x\app")] == ["b.jsonl", "a.jsonl"]
    assert find_transcripts(tmp_path / "missing", None) == []
