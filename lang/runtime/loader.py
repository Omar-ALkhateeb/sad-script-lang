# lang/runtime/loader.py
"""Module loader (`استورد`) for stdlib modules and multi-file .sad imports."""

from pathlib import Path
import types
from ..types import RuntimeError
from ..stdlib import BUILTIN_MODULES

_MODULE_CACHE: dict[str, types.SimpleNamespace] = {}


def reset_module_cache():
    _MODULE_CACHE.clear()


def import_module(module_name: str, symbols: list[str] = None):
    clean = str(module_name).strip().strip('"').strip("'")

    # 1. Standard Library Modules
    if clean in BUILTIN_MODULES:
        mod = BUILTIN_MODULES[clean]
        if symbols:
            out = []
            for sym in symbols:
                if not hasattr(mod, sym):
                    raise RuntimeError(f"المكتبة '{clean}' لا تحتوي على '{sym}'.")
                out.append(getattr(mod, sym))
            return tuple(out)
        return mod

    # 2. Local .sad / .sd / .edu file in the workspace
    candidates = [
        Path(clean),
        Path(f"{clean}.sad"),
        Path(f"{clean}.sd"),
        Path(f"{clean}.edu"),
    ]
    found = next((p for p in candidates if p.exists() and p.is_file()), None)
    if not found:
        std_names = "، ".join(BUILTIN_MODULES.keys())
        raise RuntimeError(
            f"تعذر العثور على المكتبة أو الملف '{clean}'. "
            f"(المكتبات القياسية: {std_names} — أو تأكد من وجود الملف '{clean}.sad' في مشروعك)."
        )

    cache_key = str(found.resolve())
    if cache_key not in _MODULE_CACHE:
        from .runner import compile_file_module
        source = found.read_text(encoding="utf-8")
        _MODULE_CACHE[cache_key] = compile_file_module(source, found.name)

    loaded_mod = _MODULE_CACHE[cache_key]
    if symbols:
        out = []
        for sym in symbols:
            if not hasattr(loaded_mod, sym):
                raise RuntimeError(f"الملف '{found.name}' لا يحتوي على متغير أو دالة باسم '{sym}'.")
            out.append(getattr(loaded_mod, sym))
        return tuple(out)

    return loaded_mod