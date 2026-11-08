import threading
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from reviewer_shell.server import check_watchdog, start_watchdog, record_heartbeat


def test_watchdog_does_not_trigger_before_timeout():
    t0 = 1000.0
    assert check_watchdog(now=t0 + 10.0, last_heartbeat=t0, timeout=30.0, audit_running=False) is False
    assert check_watchdog(now=t0 + 29.9, last_heartbeat=t0, timeout=30.0, audit_running=False) is False


def test_watchdog_triggers_after_timeout_when_idle():
    t0 = 1000.0
    assert check_watchdog(now=t0 + 30.0, last_heartbeat=t0, timeout=30.0, audit_running=False) is True
    assert check_watchdog(now=t0 + 45.0, last_heartbeat=t0, timeout=30.0, audit_running=False) is True


def test_watchdog_does_not_trigger_while_audit_is_running():
    t0 = 1000.0
    assert check_watchdog(now=t0 + 60.0, last_heartbeat=t0, timeout=30.0, audit_running=True) is False


def test_watchdog_thread_with_injectable_clock():
    shutdown_ev = threading.Event()
    current_time = [1000.0]

    def mock_clock():
        return current_time[0]

    record_heartbeat(timestamp=1000.0)

    # Start the watchdog with check_interval = 0.05s
    t = start_watchdog(shutdown_ev, timeout=30.0, check_interval=0.05, clock=mock_clock)

    time.sleep(0.1)
    assert not shutdown_ev.is_set()

    # Time passes normally (each tick advances <= 2s < 10s), another 15s -> not triggered yet
    for _ in range(15):
        current_time[0] += 1.0
        time.sleep(0.01)
    assert not shutdown_ev.is_set()

    # Receive a new heartbeat
    record_heartbeat(timestamp=current_time[0])

    # Another 20s pass (< 30s timeout) -> not triggered yet
    for _ in range(20):
        current_time[0] += 1.0
        time.sleep(0.01)
    assert not shutdown_ev.is_set()

    # Another 15s pass (35s total with no heartbeat) -> trigger!
    for _ in range(15):
        current_time[0] += 1.0
        time.sleep(0.01)
    time.sleep(0.1)
    assert shutdown_ev.is_set()
    t.join(timeout=1.0)


def test_watchdog_thread_does_not_fire_while_audit_running_at_3x_timeout(monkeypatch):
    shutdown_ev = threading.Event()
    current_time = [1000.0]

    def mock_clock():
        return current_time[0]

    from reviewer_shell import server as srv_mod
    monkeypatch.setattr(srv_mod, 'is_audit_running', lambda: True)

    record_heartbeat(timestamp=1000.0)

    timeout = 30.0
    t = start_watchdog(shutdown_ev, timeout=timeout, check_interval=0.05, clock=mock_clock)

    time.sleep(0.1)
    assert not shutdown_ev.is_set()

    # Time passes beyond 3x the timeout (105s) in small steps (3s < 10s)
    for _ in range(35):
        current_time[0] += 3.0
        time.sleep(0.06)
    time.sleep(0.1)
    assert not shutdown_ev.is_set()

    # When the audit ends (audit_running = False), the watchdog triggers immediately because the timeout has been exceeded
    monkeypatch.setattr(srv_mod, 'is_audit_running', lambda: False)
    current_time[0] += 1.0
    time.sleep(0.15)
    assert shutdown_ev.is_set()
    t.join(timeout=1.0)


def test_watchdog_survives_clock_jump_sleep_resume():
    shutdown_ev = threading.Event()
    current_time = [1000.0]

    def mock_clock():
        return current_time[0]

    record_heartbeat(timestamp=1000.0)

    timeout = 30.0
    t = start_watchdog(shutdown_ev, timeout=timeout, check_interval=0.05, clock=mock_clock)

    time.sleep(0.1)
    assert not shutdown_ev.is_set()

    # Simulate the computer sleeping/hibernating for 1 hour: the clock jumps 3600s in one tick
    current_time[0] += 3600.0
    time.sleep(0.12)
    # The watchdog detects a tick gap of 3600s > suspension threshold (10s) -> re-arms and does NOT trigger
    assert not shutdown_ev.is_set()

    # After waking up, a normal 15s of silence (< 30s timeout) -> not triggered yet
    for _ in range(15):
        current_time[0] += 1.0
        time.sleep(0.01)
    assert not shutdown_ev.is_set()

    # Silence continues for another 20s (35s total > 30s) with no new heartbeat -> trigger!
    for _ in range(20):
        current_time[0] += 1.0
        time.sleep(0.01)
    time.sleep(0.1)
    assert shutdown_ev.is_set()
    t.join(timeout=1.0)
