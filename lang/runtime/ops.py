# lang/runtime/ops.py
"""Safe runtime operators and infinite-loop protection."""

import time
from ..types import RuntimeError, String, List

MAX_LOOP_ITERATIONS = 100_000
MAX_EXECUTION_SECONDS = 4.0

_loop_count = 0
_start_time = 0.0


def reset_limits():
    global _loop_count, _start_time
    _loop_count = 0
    _start_time = time.monotonic()


def loop_guard():
    global _loop_count
    _loop_count += 1
    if _loop_count > MAX_LOOP_ITERATIONS:
        raise RuntimeError(
            f"تم إيقاف الحلقة تلقائياً بعد ({MAX_LOOP_ITERATIONS}) دورة لمنع تجميد البرنامج (تأكد من شرط التوقف)."
        )
    if _loop_count % 1000 == 0 and (time.monotonic() - _start_time) > MAX_EXECUTION_SECONDS:
        raise RuntimeError(
            f"استغرق تنفيذ البرنامج وقتاً أطول من الحد المسموح ({MAX_EXECUTION_SECONDS} ثوانٍ) وتم إيقافه."
        )


def add(a, b):
    """Auto-coerces string + any value into a native String and list + list into a List."""
    if isinstance(a, str) or isinstance(b, str):
        sa = "صحيح" if a is True else ("خطأ" if a is False else ("فارغ" if a is None else str(a)))
        sb = "صحيح" if b is True else ("خطأ" if b is False else ("فارغ" if b is None else str(b)))
        return String(sa + sb)
    res = a + b
    if isinstance(res, list) and not isinstance(res, List):
        return List(res)
    return res