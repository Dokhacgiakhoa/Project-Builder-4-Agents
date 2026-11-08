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

    # Khởi động watchdog với check_interval = 0.05s
    t = start_watchdog(shutdown_ev, timeout=30.0, check_interval=0.05, clock=mock_clock)

    time.sleep(0.1)
    assert not shutdown_ev.is_set()

    # Thời gian trôi bình thường (mỗi tick tăng <= 2s < 10s) thêm 15s -> chưa trigger
    for _ in range(15):
        current_time[0] += 1.0
        time.sleep(0.01)
    assert not shutdown_ev.is_set()

    # Nhận heartbeat mới
    record_heartbeat(timestamp=current_time[0])

    # Trôi tiếp 20s (< 30s timeout) -> chưa trigger
    for _ in range(20):
        current_time[0] += 1.0
        time.sleep(0.01)
    assert not shutdown_ev.is_set()

    # Trôi tiếp 15s (tổng 35s không có heartbeat) -> trigger!
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

    # Trôi thời gian tới hơn 3x timeout (105s) theo từng bước nhỏ (3s < 10s)
    for _ in range(35):
        current_time[0] += 3.0
        time.sleep(0.06)
    time.sleep(0.1)
    assert not shutdown_ev.is_set()

    # Khi audit kết thúc (audit_running = False), watchdog lập tức trigger vì đã quá timeout
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

    # Giả lập máy tính Sleep/Hibernate trong 1 giờ: clock nhảy 3600s trong 1 tick
    current_time[0] += 3600.0
    time.sleep(0.12)
    # Watchdog phát hiện tick gap 3600s > suspension threshold (10s) -> re-arm và KHÔNG trigger
    assert not shutdown_ev.is_set()

    # Sau khi thức dậy, silence bình thường 15s (< 30s timeout) -> chưa trigger
    for _ in range(15):
        current_time[0] += 1.0
        time.sleep(0.01)
    assert not shutdown_ev.is_set()

    # Silence tiếp tục thêm 20s (tổng 35s > 30s) mà không có heartbeat mới -> trigger!
    for _ in range(20):
        current_time[0] += 1.0
        time.sleep(0.01)
    time.sleep(0.1)
    assert shutdown_ev.is_set()
    t.join(timeout=1.0)
