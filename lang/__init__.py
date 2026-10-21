"""Public API for the edu educational compiler package."""

import io
import sys
import traceback
import contextlib
import pandas as pd
from lark import Lark, UnexpectedInput

from . import stdlib
from .checker import SemanticAnalyzer, EduCompileError
from .transpiler import PythonTranspiler, extract_student_line
from .errors import explain_syntax_error, explain_runtime_error, ar_type

parser = Lark.open("grammar.lark", rel_to=__file__, parser="lalr", propagate_positions=True)

def _extract_workspace_state(exec_globals, base_keys):
    """Extracts user variables and Pandas DataFrames for the React IDE workbench."""
    variables = []
    dataframes = {}

    for name, val in exec_globals.items():
        if name in base_keys or name.startswith("_") or callable(val) or isinstance(val, type(sys)):
            continue

        t_ar = ar_type(val)
        if isinstance(val, pd.DataFrame):
            preview_str = f"جدول ({val.shape[0]} صف × {val.shape[1]} عمود)"
            df_clean = val.head(100).fillna("")
            dataframes[name] = {
                "name": name,
                "shape": [int(val.shape[0]), int(val.shape[1])],
                "columns": [str(c) for c in df_clean.columns],
                "dtypes": {str(col): str(dtype) for col, dtype in val.dtypes.items()},
                "rows": [[str(cell) for cell in row] for row in df_clean.values.tolist()],
            }
        elif isinstance(val, pd.Series):
            preview_str = f"عمود ({len(val)} عنصر)"
        else:
            preview_str = repr(val)
            if len(preview_str) > 120:
                preview_str = preview_str[:117] + "..."

        variables.append({
            "name": str(name),
            "type": str(t_ar),
            "value": str(preview_str),
        })

    return variables, dataframes


def execute_educational_code(source_code):
    lines = source_code.splitlines()
    stdlib.clear_charts()
    stdlib.reset_execution_limits()
    stdout_buffer = io.StringIO()

    # Stage 1: Parse Syntax
    try:
        tree = parser.parse(source_code)
    except UnexpectedInput as e:
        err_msg = explain_syntax_error(e, source_code, parser)
        return {
            "ok": False, "stdout": "", "error": err_msg,
            "error_line": getattr(e, "line", 1), "python_code": "",
            "charts": [], "variables": [], "dataframes": {}
        }

    # Stage 2: Static Semantic Analysis
    try:
        func_globals = SemanticAnalyzer().analyze(tree)
    except EduCompileError as ce:
        line_text = lines[ce.line - 1] if 0 < ce.line <= len(lines) else ""
        pointer = " " * max(0, ce.col - 1) + "^"
        err_msg = (
            f"❌ خطأ منطقي قبل التشغيل (السطر {ce.line}، العمود {ce.col}):\n"
            f"    {line_text}\n"
            f"    {pointer}\n"
            f"💡 التشخيص: {ce.message}"
        )
        return {
            "ok": False, "stdout": "", "error": err_msg,
            "error_line": ce.line, "python_code": "",
            "charts": [], "variables": [], "dataframes": {}
        }

    # Stage 3: Transpile to Python
    python_code = PythonTranspiler(func_globals=func_globals).transform(tree)

    # Stage 4: Execute & Extract Live Memory State
    exec_globals = {k: v for k, v in vars(stdlib).items() if not k.startswith("__")}
    exec_globals["__name__"] = "__main__"
    base_keys = set(exec_globals.keys())

    try:
        compiled_bytecode = compile(python_code, "<student_code>", "exec")
        with contextlib.redirect_stdout(stdout_buffer):
            exec(compiled_bytecode, exec_globals)
    except Exception as e:
        tb_frames = traceback.extract_tb(e.__traceback__)
        py_line = next((f.lineno for f in reversed(tb_frames) if f.filename == "<student_code>"), 1)
        student_line = extract_student_line(py_line, python_code)
        err_msg = explain_runtime_error(e, student_line, source_code, tree, exec_globals)
        variables, dataframes = _extract_workspace_state(exec_globals, base_keys)
        return {
            "ok": False,
            "stdout": stdout_buffer.getvalue(),
            "error": err_msg,
            "error_line": getattr(e, "line_no", student_line),
            "python_code": python_code,
            "charts": stdlib.get_charts(),
            "variables": variables,
            "dataframes": dataframes,
        }

    variables, dataframes = _extract_workspace_state(exec_globals, base_keys)
    return {
        "ok": True,
        "stdout": stdout_buffer.getvalue(),
        "error": "",
        "error_line": None,
        "python_code": python_code,
        "charts": stdlib.get_charts(),
        "variables": variables,
        "dataframes": dataframes,
    }