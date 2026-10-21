"""AST-to-Python code generator with source line markers and loop guards."""

from lark import Transformer, v_args
from .mappings import (
    ARABIC_DIGITS,
    BUILTIN_MAP, NORM_BUILTIN_MAP,
    METHOD_MAP, NORM_METHOD_MAP,
    ATTR_MAP, NORM_ATTR_MAP,
    KWARG_MAP, NORM_KWARG_MAP,
    lookup_norm,
)

@v_args(meta=True)
class PythonTranspiler(Transformer):
    def __init__(self, func_globals=None):
        super().__init__()
        self.func_globals = func_globals or {}

    def _indent(self, code_str):
        if not code_str or not str(code_str).strip():
            return "    pass"
        return "\n".join("    " + line for line in str(code_str).split("\n"))

    def _loop_body(self, meta, body_str):
        tick_line = f"    _edu_tick({meta.line})  #__EDU_LINE__:{meta.line}"
        return f"{tick_line}\n{self._indent(body_str)}"

    def start(self, meta, stmts):
        header = "try:\n    from lang.stdlib import *\nexcept ImportError:\n    from stdlib import *"
        body = "\n".join(str(s) for s in stmts if s is not None)
        return f"{header}\n{body}"

    def statement(self, meta, items):
        stmt_str = str(items[0])
        lines = stmt_str.split("\n")
        if "#__EDU_LINE__:" not in lines[0]:
            lines[0] = f"{lines[0]}  #__EDU_LINE__:{meta.line}"
        return "\n".join(lines)

    def block(self, meta, stmts):
        return "\n".join(str(s) for s in stmts if s is not None) if stmts else "pass"

    def assignment(self, meta, items): return f"{items[0]} = {items[1]}"
    def aug_assignment(self, meta, items): return f"{items[0]} {items[1]} {items[2]}"
    def assign_var(self, meta, items): return str(items[0])
    def assign_index(self, meta, items): return f"{items[0]}[{items[1]}]"
    def assign_attr(self, meta, items):
        attr = str(items[1])
        return f"{items[0]}.{lookup_norm(ATTR_MAP, NORM_ATTR_MAP, attr)}"

    def print_stmt(self, meta, items):
        return f"edu_print({items[0] if items and items[0] is not None else ''})"

    def return_stmt(self, meta, items):
        return f"return {items[0]}" if items and items[0] is not None else "return"

    def break_stmt(self, meta, _): return "break"
    def continue_stmt(self, meta, _): return "continue"

    def if_stmt(self, meta, items):
        res = f"if {items[0]}:\n{self._indent(items[1])}"
        for extra in items[2:]:
            if extra is not None:
                res += f"\n{extra}"
        return res

    def elif_clause(self, meta, items): return f"elif {items[0]}:\n{self._indent(items[1])}"
    def else_clause(self, meta, items): return f"else:\n{self._indent(items[0])}"

    def repeat_stmt(self, meta, items):
        return f"for _ in range(int({items[0]})):\n{self._loop_body(meta, items[1])}"

    def for_range_stmt(self, meta, items):
        return f"for {items[0]} in edu_range({items[1]}, {items[2]}):\n{self._loop_body(meta, items[3])}"

    def for_in_stmt(self, meta, items):
        return f"for {items[0]} in {items[1]}:\n{self._loop_body(meta, items[2])}"

    def while_stmt(self, meta, items):
        return f"while {items[0]}:\n{self._loop_body(meta, items[1])}"

    def func_def(self, meta, items):
        name = str(items[0])
        params = str(items[1]) if items[1] is not None else ""
        globals_needed = self.func_globals.get((meta.line, name), set())
        global_decl = f"    global {', '.join(sorted(globals_needed))}\n" if globals_needed else ""
        body = self._indent(items[2])
        return f"def {name}({params}):\n{global_decl}{body}"

    def try_stmt(self, meta, items):
        try_body = self._indent(items[0])
        err_var = str(items[1]) if items[1] is not None else "_err"
        catch_body = self._indent(items[2])
        return (
            f"try:\n{try_body}\n"
            f"except EduInfiniteLoopError:\n    raise\n"
            f"except Exception as {err_var}:\n{catch_body}"
        )

    def params(self, meta, items): return ", ".join(str(x) for x in items)
    def param(self, meta, items): return str(items[0])
    def default_param(self, meta, items): return f"{items[0]}={items[1]}"
    def expr_stmt(self, meta, items): return str(items[0])

    def bool_or(self, meta, items): return f"({items[0]} or {items[1]})"
    def bool_and(self, meta, items): return f"({items[0]} and {items[1]})"
    def bool_not(self, meta, items): return f"(not {items[0]})"
    def compare(self, meta, items): return f"({items[0]} {items[1]} {items[2]})"
    def in_op(self, meta, items): return f"({items[0]} in {items[1]})"
    def not_in_op(self, meta, items): return f"({items[0]} not in {items[1]})"
    def bit_and(self, meta, items): return f"({items[0]} & {items[1]})"
    def bit_or(self, meta, items): return f"({items[0]} | {items[1]})"
    def add(self, meta, items): return f"edu_add({items[0]}, {items[1]})"
    def sub(self, meta, items): return f"({items[0]} - {items[1]})"
    def mul(self, meta, items): return f"({items[0]} * {items[1]})"
    def div(self, meta, items): return f"({items[0]} / {items[1]})"
    def floordiv(self, meta, items): return f"({items[0]} // {items[1]})"
    def mod(self, meta, items): return f"({items[0]} % {items[1]})"
    def pow_op(self, meta, items): return f"({items[0]} ** {items[1]})"
    def neg(self, meta, items): return f"(-{items[0]})"
    def pos(self, meta, items): return f"(+{items[0]})"
    def parens(self, meta, items): return f"({items[0]})"

    def number(self, meta, items): return str(items[0]).translate(ARABIC_DIGITS)
    def string(self, meta, items): return str(items[0])
    def bool_true(self, meta, _): return "True"
    def bool_false(self, meta, _): return "False"
    def none_val(self, meta, _): return "None"
    def var(self, meta, items): return str(items[0])
    def array(self, meta, items): return "[" + ", ".join(str(x) for x in items if x is not None) + "]"
    def dict_literal(self, meta, items): return "{" + ", ".join(str(x) for x in items if x is not None) + "}"
    def kv_pair(self, meta, items): return f"{items[0]}: {items[1]}"
    def arg_list(self, meta, items): return ", ".join(str(x) for x in items if x is not None)

    def kwarg(self, meta, items):
        key = str(items[0])
        return f"{lookup_norm(KWARG_MAP, NORM_KWARG_MAP, key)}={items[1]}"

    def func_call(self, meta, items):
        func_name = str(items[0])
        args = str(items[1]) if len(items) > 1 and items[1] is not None else ""
        mapped = lookup_norm(BUILTIN_MAP, NORM_BUILTIN_MAP, func_name)
        return f"{mapped}({args})"

    def method_call(self, meta, items):
        obj, method_name = str(items[0]), str(items[1])
        args = str(items[2]) if len(items) > 2 and items[2] is not None else ""
        mapped = lookup_norm(METHOD_MAP, NORM_METHOD_MAP, method_name)
        return f"{obj}.{mapped}({args})"

    def attr_access(self, meta, items):
        attr = str(items[1])
        return f"{items[0]}.{lookup_norm(ATTR_MAP, NORM_ATTR_MAP, attr)}"

    def index_access(self, meta, items): return f"{items[0]}[{items[1]}]"
    def slice_expr(self, meta, items):
        start = str(items[0]) if len(items) > 0 and items[0] is not None else ""
        end = str(items[1]) if len(items) > 1 and items[1] is not None else ""
        return f"{start}:{end}"

def extract_student_line(py_line_no, python_code):
    py_lines = python_code.splitlines()
    for idx in range(min(py_line_no, len(py_lines)) - 1, -1, -1):
        line_str = py_lines[idx]
        if "#__EDU_LINE__:" in line_str:
            return int(line_str.split("#__EDU_LINE__:")[1].strip())
    return 1