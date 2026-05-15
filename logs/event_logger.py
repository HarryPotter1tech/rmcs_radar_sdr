import os
import threading
from datetime import datetime
from pprint import pformat


LOGS_DIR = os.path.abspath(os.path.dirname(__file__))
os.makedirs(LOGS_DIR, exist_ok=True)

# per-module locks to avoid interleaved writes
_locks: dict[str, threading.Lock] = {}


def _get_lock(module: str) -> threading.Lock:
    if module not in _locks:
        _locks[module] = threading.Lock()
    return _locks[module]


def _log_path(module: str) -> str:
    filename = f"{module}.log"
    return os.path.join(LOGS_DIR, filename)


def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(module: str, message: str, tag: str | None = None) -> None:
    """Append a timestamped message to module-specific log file.

    Args:
        module: short module name used to name the log file (e.g. 'unity', 'sdr_signal').
        message: message text to append.
        tag: optional tag string to include (e.g. '[unity]').
    """
    path = _log_path(module)
    line = f"[{_timestamp()}] {tag or ''} {message}\n"
    lock = _get_lock(module)
    with lock:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line)


def _stringify_data(data) -> str:
    if isinstance(data, (bytes, bytearray)):
        return data.hex(" ")
    if isinstance(data, dict):
        return pformat(data, width=120, sort_dicts=True)
    if hasattr(data, "__dict__"):
        return pformat(getattr(data, "__dict__"), width=120, sort_dicts=True)
    return pformat(data, width=120, sort_dicts=True)


def log_data(module: str, label: str, data, tag: str | None = None) -> None:
    """Append a structured data snapshot to the module-specific log file."""
    log(module, f"{label}: {_stringify_data(data)}", tag=tag)


def log_thread_start(module: str, thread_name: str) -> None:
    log(module, f"Thread '{thread_name}' started")


def log_thread_stop(module: str, thread_name: str) -> None:
    log(module, f"Thread '{thread_name}' stopped")
