# lang/compiler/emitter.py
"""AST-to-Target Code Emitter."""

import re
from lark import Transformer, v_args
from .sourcemap import tag_line

ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
INTERP_PATTERN = re.compile(r"\{([^{}]+)\}")


def _indent(text: str, spaces: int = 4) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else line for line in text.splitlines())


def _normalize_interp_expr(match: re.Match) -> str:
    raw_expr = match.group(1).strip()
    normalized = raw_expr.translate(ARABIC_DIGITS).replace("،", ",")
    return f"{{نص({normalized})}}"


@v_args(meta=True)
class Emitter(Transformer):
    def __init__(self):
        super().__init__()
        self._loop_id = 0

    def start(self, meta, stmts):
        body = "\n".join(str(s) for s in stmts if s is not None)
        return body if body.strip() else "pass"

    def block(self, meta, stmts):
        valid = [str(s) for s in stmts if s is not None]
        return "\n".join(valid) if valid else "pass"

    # --- Statements ---
    def var_assign(self, meta, items):
        target, expr = items[0], items[1]
        return tag_line(f"{target} = {expr}", meta.line)

    def aug_assign(self, meta, items):
        target, op, expr = items[0], str(items[1]), items[2]
        if op == "+=":
            return tag_line(f"{target} = __add__({target}, {expr})", meta.line)
        return tag_line(f"{target} {op} {expr}", meta.line)

    def global_stmt(self, meta, items):
        names = [str(tok) for tok in items]
        return tag_line(f"global {', '.join(names)}", meta.line)

    def lval_var(self, meta, items):
        return str(items[0])

    def lval_index(self, meta, items):
        return f"{items[0]}[{items[1]}]"

    def lval_attr(self, meta, items):
        return f"{items[0]}.{items[1]}"

    def if_stmt(self, meta, items):
        cond = items[0]
        body = _indent(items[1])
        out = [tag_line(f"if {cond}:", meta.line), body]
        for clause in items[2:]:
            if clause is not None:
                out.append(str(clause))
        return "\n".join(out)

    def elif_clause(self, meta, items):
        cond, body = items[0], _indent(items[1])
        return f"{tag_line(f'elif {cond}:', meta.line)}\n{body}"

    def else_clause(self, meta, items):
        body = _indent(items[0])
        return f"{tag_line('else:', meta.line)}\n{body}"

    def repeat_stmt(self, meta, items):
        count_expr = items[0]
        body_str = items[-1]
        self._loop_id += 1
        var = f"_rep_{self._loop_id}"
        guard = tag_line("__loop_guard__()", meta.line)
        full_body = _indent(f"{guard}\n{body_str}")
        return f"{tag_line(f'for {var} in range(int({count_expr})):', meta.line)}\n{full_body}"

    def for_range_stmt(self, meta, items):
        var_name = str(items[0])
        start_expr = items[1]
        end_expr = items[2]
        body_str = items[3]
        guard = tag_line("__loop_guard__()", meta.line)
        full_body = _indent(f"{guard}\n{body_str}")
        header = f"for {var_name} in مدى({start_expr}, {end_expr}):"
        return f"{tag_line(header, meta.line)}\n{full_body}"

    def for_each_stmt(self, meta, items):
        var_name = str(items[0])
        iter_expr = items[1]
        body_str = items[2]
        guard = tag_line("__loop_guard__()", meta.line)
        full_body = _indent(f"{guard}\n{body_str}")
        return f"{tag_line(f'for {var_name} in {iter_expr}:', meta.line)}\n{full_body}"

    def while_stmt(self, meta, items):
        cond_expr = items[0]
        body_str = items[1]
        guard = tag_line("__loop_guard__()", meta.line)
        full_body = _indent(f"{guard}\n{body_str}")
        return f"{tag_line(f'while {cond_expr}:', meta.line)}\n{full_body}"

    def params(self, meta, items):
        return [str(tok) for tok in items]

    def func_def(self, meta, items):
        func_name = str(items[0])
        raw_params = items[1] if items[1] is not None else []
        body_str = items[2]
        param_str = ", ".join(raw_params)
        return f"{tag_line(f'def {func_name}({param_str}):', meta.line)}\n{_indent(body_str)}"

    def method_def(self, meta, items):
        fname = str(items[0])
        if fname in ("انشئ", "أنشئ", "بناء", "init"):
            fname = "__init__"
        raw_params = list(items[1]) if items[1] is not None else []
        if not raw_params or raw_params[0] != "هذا":
            raw_params.insert(0, "هذا")
        body_str = items[2]
        param_str = ", ".join(raw_params)
        return f"{tag_line(f'def {fname}({param_str}):', meta.line)}\n{_indent(body_str)}"

    def class_def(self, meta, items):
        class_name = str(items[0])
        members = [str(m) for m in items[1:] if m is not None]
        body = _indent("\n".join(members)) if members else "    pass"
        return (
            f"{tag_line(f'class {class_name}:', meta.line)}\n"
            f"    __type_name__ = '{class_name}'\n"
            f"{body}"
        )

    def import_names(self, meta, items):
        return [str(tok) for tok in items]

    def import_module(self, meta, items):
        raw_target = str(items[0]).strip('"').strip("'")
        var_name = raw_target.split("/")[-1].split(".")[0]
        return tag_line(f'{var_name} = __import_module__("{raw_target}")', meta.line)

    def import_from(self, meta, items):
        raw_target = str(items[0]).strip('"').strip("'")
        names = items[1]
        lhs = ", ".join(names) + ("," if len(names) == 1 else "")
        return tag_line(f'{lhs} = __import_module__("{raw_target}", {repr(names)})', meta.line)

    def return_stmt(self, meta, items):
        val = f" {items[0]}" if items and items[0] is not None else ""
        return tag_line(f"return{val}", meta.line)

    def break_stmt(self, meta, items):
        return tag_line("break", meta.line)

    def continue_stmt(self, meta, items):
        return tag_line("continue", meta.line)

    def try_stmt(self, meta, items):
        try_body = _indent(items[0])
        err_var = str(items[1])
        catch_body = _indent(items[2])
        return (
            f"{tag_line('try:', meta.line)}\n{try_body}\n"
            f"except Exception as _raw_err:\n"
            f"    {err_var} = String(str(_raw_err))\n"
            f"{catch_body}"
        )

    def expr_stmt(self, meta, items):
        return tag_line(str(items[0]), meta.line)

    # --- Expressions ---
    def paren(self, meta, items):
        return f"({items[0]})"

    def or_expr(self, meta, items):
        return "(" + " or ".join(str(x) for x in items) + ")"

    def and_expr(self, meta, items):
        return "(" + " and ".join(str(x) for x in items) + ")"

    def not_op(self, meta, items):
        return f"(not {items[0]})"

    def comp_in(self, meta, items):
        return "in"

    def comp_not_in(self, meta, items):
        return "not in"

    def comp_op(self, meta, items):
        return str(items[0])

    def comparison(self, meta, items):
        return "(" + " ".join(str(x) for x in items) + ")"

    def sum(self, meta, items):
        res = str(items[0])
        for i in range(1, len(items), 2):
            op = str(items[i])
            rhs = str(items[i + 1])
            if op == "+":
                res = f"__add__({res}, {rhs})"
            else:
                res = f"({res} - {rhs})"
        return res

    def product(self, meta, items):
        return "(" + " ".join(str(x) for x in items) + ")"

    def neg(self, meta, items):
        return f"(-{items[0]})"

    def pos(self, meta, items):
        return f"(+{items[0]})"

    def power(self, meta, items):
        if len(items) == 1:
            return str(items[0])
        return f"({items[0]} ** {items[1]})"

    # --- Atoms & Literals ---
    def number_lit(self, meta, items):
        return str(items[0]).translate(ARABIC_DIGITS)

    def string_lit(self, meta, items):
        raw = str(items[0])
        inner = raw[1:-1]
        if INTERP_PATTERN.search(inner):
            converted = INTERP_PATTERN.sub(_normalize_interp_expr, inner)
            quote = raw[0]
            return f"String(f{quote}{converted}{quote})"
        return f"String({raw})"

    def true_lit(self, meta, items):
        return "True"

    def false_lit(self, meta, items):
        return "False"

    def none_lit(self, meta, items):
        return "None"

    def var_ref(self, meta, items):
        return str(items[0])

    def expr_list(self, meta, items):
        return ", ".join(str(x) for x in items)

    def list_lit(self, meta, items):
        inner = items[0] if items and items[0] is not None else ""
        return f"List([{inner}])"

    def dict_pair(self, meta, items):
        return f"{items[0]}: {items[1]}"

    def dict_items(self, meta, items):
        return ", ".join(str(x) for x in items)

    def dict_lit(self, meta, items):
        inner = items[0] if items and items[0] is not None else ""
        return f"Dict({{{inner}}})"

    def kwarg(self, meta, items):
        return f"{items[0]}={items[1]}"

    def arg_list(self, meta, items):
        return ", ".join(str(x) for x in items)

    def func_call(self, meta, items):
        callee = str(items[0])
        if callee == "True":
            callee = "عدد"
        args = items[1] if len(items) > 1 and items[1] is not None else ""
        return f"{callee}({args})"

    def index_access(self, meta, items):
        return f"{items[0]}[{items[1]}]"

    def attr_access(self, meta, items):
        return f"{items[0]}.{items[1]}"
