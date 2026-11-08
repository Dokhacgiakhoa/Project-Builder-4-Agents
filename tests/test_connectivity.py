"""Reachability probe used by the About & Version dialog (update check, kit knowledge update)."""
from __future__ import annotations

import sys
import time
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from reviewer_shell.connectivity import REQUIRED_HOSTS, check_internet  # noqa: E402


def test_all_hosts_reachable():
    out = check_internet(fetch=lambda url, timeout: None)
    assert out["online"] is True
    assert set(out["hosts"]) == set(REQUIRED_HOSTS)
    assert all(out["hosts"].values())


def test_offline_marks_every_host_unreachable():
    def boom(url, timeout):
        raise urllib.error.URLError("no network")

    out = check_internet(fetch=boom)
    assert out["online"] is False
    assert not any(out["hosts"].values())


def test_http_error_still_counts_as_reachable():
    def not_found(url, timeout):
        raise urllib.error.HTTPError(url, 404, "Not Found", None, None)

    assert check_internet(fetch=not_found)["online"] is True


def test_partial_failure_reports_per_host():
    def only_api(url, timeout):
        if "raw.githubusercontent.com" in url:
            raise OSError("timed out")

    out = check_internet(fetch=only_api)
    assert out["online"] is False
    assert out["hosts"]["api.github.com"] is True
    assert out["hosts"]["raw.githubusercontent.com"] is False


def test_hung_probe_does_not_block_and_counts_unreachable():
    def hang(url, timeout):
        time.sleep(5)

    start = time.perf_counter()
    out = check_internet(hosts={"example.invalid": "https://example.invalid/"}, timeout=0.2, fetch=hang)
    assert time.perf_counter() - start < 3
    assert out == {"online": False, "hosts": {"example.invalid": False}}


def test_empty_host_list_is_not_online():
    assert check_internet(hosts={}, fetch=lambda u, t: None) == {"online": False, "hosts": {}}
