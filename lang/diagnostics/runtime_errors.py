# lang/diagnostics/runtime_errors.py
"""Translates runtime exceptions into clean Arabic diagnostics."""

import re
import difflib
from ..types import RuntimeError, type_name


def explain_runtime_error(exc: Exception, line_no: int, source_code: str, env: dict) -> str:
    lines = source_code.splitlines()
    safe_line = max(1, min(line_no or 1, max(1, len(lines))))
    line_text = lines[safe_line - 1] if lines else ""

    # 1. Fast-path: Native RuntimeError raised directly by our types/stdlib!
    if isinstance(exc, RuntimeError) or getattr(exc, "is_native_error", False):
        diagnosis = str(exc)
    elif isinstance(exc, ZeroDivisionError):
        diagnosis = "لا يمكن القسمة على صفر! تأكد من أن المقسوم عليه لا يساوي ٠."
    elif isinstance(exc, NameError):
        m = re.search(r"name '([^']+)' is not defined", str(exc))
        missing = m.group(1) if m else "غير معروف"
        candidates = [k for k in env.keys() if not k.startswith("_")]
        close = difflib.get_close_matches(missing, candidates, n=1, cutoff=0.55)
        suggest = f" هل تقصد '{close[0]}'؟" if close else ""
        diagnosis = f"المتغير أو الأمر '{missing}' غير معرّف.{suggest}"
    elif isinstance(exc, AttributeError):
        m = re.search(r"'([^']+)' object has no attribute '([^']+)'", str(exc))
        if m:
            attr = m.group(2)
            diagnosis = f"هذا الكائن لا يحتوي على خاصية أو دالة باسم '{attr}'."
        else:
            diagnosis = "حاولت استدعاء خاصية أو دالة غير موجودة في هذا الكائن."
    elif isinstance(exc, TypeError):
        msg = str(exc)
        if "missing" in msg and "required positional argument" in msg:
            diagnosis = "عدد المدخلات الممررة للدالة أقل من المطلوب."
        elif "takes" in msg and "positional argument" in msg:
            diagnosis = "عدد المدخلات الممررة للدالة أكثر مما تستقبله الدالة."
        elif "not callable" in msg:
            diagnosis = "حاولت استدعاء متغير عادي كأنه دالة باستخدام الأقواس ()."
        else:
            diagnosis = "العملية غير مدعومة بين هذه الأنواع من البيانات."
    else:
        diagnosis = f"حدث خطأ أثناء تنفيذ هذا السطر: {str(exc)}"

    return (
        f"❌ خطأ أثناء التشغيل (السطر {safe_line}):\n"
        f"    {line_text}\n"
        f"💡 التشخيص: {diagnosis}"
    )