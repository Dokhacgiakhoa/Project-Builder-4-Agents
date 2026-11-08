"""Reachability probe for features that need the Internet (update check, kit knowledge update).

The engine (not the browser) performs those downloads, so the engine must be the one to test reachability.
The probe uses urllib, the same stack as the real requests, so proxy environment settings apply equally.
An HTTP error status still proves the host answered, so it counts as reachable.
"""
from __future__ import annotations

import threading
import urllib.error
import urllib.request
from typing import Callable

# host name (as used by the UI) -> URL probed
REQUIRED_HOSTS: dict[str, str] = {
    "api.github.com": "https://api.github.com/",
    "raw.githubusercontent.com": "https://raw.githubusercontent.com/",
}


def _http_head(url: str, timeout: float) -> None:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Project-Builder-Analytics"})
    with urllib.request.urlopen(req, timeout=timeout):
        pass


def check_internet(
    hosts: dict[str, str] | None = None,
    timeout: float = 3.0,
    fetch: Callable[[str, float], None] = _http_head,
) -> dict:
    """Probe every host in parallel. Returns {"online": all reachable, "hosts": {host: bool}}."""
    targets = REQUIRED_HOSTS if hosts is None else hosts
    results: dict[str, bool] = {host: False for host in targets}
    lock = threading.Lock()

    def probe(host: str, url: str) -> None:
        try:
            fetch(url, timeout)
            ok = True
        except urllib.error.HTTPError:
            ok = True  # the server answered, so the network path works
        except (urllib.error.URLError, OSError, ValueError):
            ok = False  # DNS failure, refused, timeout, malformed URL
        with lock:
            results[host] = ok

    threads = [threading.Thread(target=probe, args=(h, u), daemon=True) for h, u in targets.items()]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout + 1.0)  # a hung probe leaves its host marked unreachable

    with lock:
        snapshot = dict(results)
    return {"online": bool(snapshot) and all(snapshot.values()), "hosts": snapshot}
