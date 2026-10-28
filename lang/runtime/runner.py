# lang/runtime/runner.py
"""Executes compiled code in a sandboxed namespace and extracts IDE state."""

import io
import sys
import types
import traceback
import contextlib
from lark import UnexpectedInput

from ..compiler import compile_source, CompileError, extract_source_line
from ..types import type_name
from ..stdlib import CORE_BUILTINS, Table, Column, clear_charts, get_charts
from ..diagnostics import explain_syntax_error, explain_runtime_error
from .ops import add, loop_guard, reset_limits
from .loader import import_module, reset_module_cache


def _build_env() -> dict:
    env = dict(CORE_BUILTINS)
    env["__add__"] = add
    env["__loop_guard__"] = loop_guard
    env["__import_module__"] = import_module
    env["__name__"] = "__main__"
    return env


def compile_file_module(source_code: str, filename: str) -> types.SimpleNamespace:
    """Compiles and executes an imported .sad file in its own isolated scope."""
    _, compiled_code = compile_source(source_code)
    mod_env = _build_env()
    base_keys = set(mod_env.keys())
    bytecode = compile(compiled_code, filename, "exec")
    exec(bytecode, mod_env)
    exported = {
        k: v for k, v in mod_env.items() if k not in base_keys and not k.startswith("_")
    }
    ns = types.SimpleNamespace(**exported)
    ns.__type_name__ = f"ملف ({filename})"
    return ns


def _extract_workspace(env: dict, base_keys: set[str]):
    variables = []
    dataframes = {}

    for name, val in env.items():
        if name in base_keys or name.startswith("_") or callable(val) or isinstance(val, type(sys)):
            continue

        t_ar = type_name(val)
        if isinstance(val, Table):
            preview = f"جدول ({val.الشكل[0]} صف × {val.الشكل[1]} عمود)"
            dataframes[name] = val.to_ide_dict(name)
        elif isinstance(val, Column):
            preview = f"عمود ({len(val)} عنصر)"
        else:
            preview = repr(val)
            if len(preview) > 120:
                preview = preview[:117] + "..."

        variables.append({"name": str(name), "type": str(t_ar), "value": str(preview)})

    return variables, dataframes


def execute_educational_code(source_code: str) -> dict:
    lines = source_code.splitlines()
    clear_charts()
    reset_limits()
    reset_module_cache()
    stdout_buffer = io.StringIO()

    try:
        _, compiled_code = compile_source(source_code)
    except UnexpectedInput as e:
        return {
            "ok": False,
            "stdout": "",
            "error": explain_syntax_error(e, source_code),
            "error_line": getattr(e, "line", 1),
            "python_code": "",
            "charts": [],
            "variables": [],
            "dataframes": {},
        }
    except CompileError as ce:
        line_text = lines[ce.line - 1] if 0 < ce.line <= len(lines) else ""
        pointer = " " * max(0, ce.col - 1) + "^"
        err_msg = (
            f"❌ خطأ منطقي قبل التشغيل (السطر {ce.line}، العمود {ce.col}):\n"
            f"    {line_text}\n"
            f"    {pointer}\n"
            f"💡 التشخيص: {ce.message}"
        )
        return {
            "ok": False,
            "stdout": "",
            "error": err_msg,
            "error_line": ce.line,
            "python_code": "",
            "charts": [],
            "variables": [],
            "dataframes": {},
        }

    env = _build_env()
    base_keys = set(env.keys())

    try:
        bytecode = compile(compiled_code, "<sadscript>", "exec")
        with contextlib.redirect_stdout(stdout_buffer):
            exec(bytecode, env)
    except Exception as e:
        tb_frames = traceback.extract_tb(e.__traceback__)
        py_line = next((f.lineno for f in reversed(tb_frames) if f.filename == "<sadscript>"), 1)
        src_line = extract_source_line(py_line, compiled_code)
        err_msg = explain_runtime_error(e, src_line, source_code, env)
        variables, dataframes = _extract_workspace(env, base_keys)
        return {
            "ok": False,
            "stdout": stdout_buffer.getvalue(),
            "error": err_msg,
            "error_line": getattr(e, "line_no", None) or src_line,
            "python_code": compiled_code,
            "charts": get_charts(),
            "variables": variables,
            "dataframes": dataframes,
        }

    variables, dataframes = _extract_workspace(env, base_keys)
    return {
        "ok": True,
        "stdout": stdout_buffer.getvalue(),
        "error": "",
        "error_line": None,
        "python_code": compiled_code,
        "charts": get_charts(),
        "variables": variables,
        "dataframes": dataframes,
    }