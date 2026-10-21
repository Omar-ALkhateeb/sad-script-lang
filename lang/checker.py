"""Two-pass static semantic analyzer and lexical scope validator."""

import difflib
from .mappings import (
    BUILTIN_MAP,
    NORM_BUILTIN_MAP,
    NORM_BUILTIN_ARITY,
    normalize_ar,
)

class EduCompileError(Exception):
    def __init__(self, line, col, message):
        self.line = line
        self.col = col
        self.message = message

class SemanticAnalyzer:
    def __init__(self):
        self.loop_depth = 0
        self.func_stack = []
        self.base_builtins = {"باندا", "رياضيات", "رسم", "عشوائيات"} | set(BUILTIN_MAP.keys())
        self.scopes = [set(self.base_builtins)]
        self.user_func_arity = {}
        self.func_globals = {}

    def analyze(self, tree):
        self._collect_functions(tree)
        self._visit(tree)
        return self.func_globals

    def _is_defined(self, name):
        if normalize_ar(name) in NORM_BUILTIN_MAP:
            return True
        return any(name in scope for scope in reversed(self.scopes))

    def _all_visible_names(self):
        out = set()
        for s in self.scopes:
            out |= s
        return out

    def _check_security(self, name, line, col):
        if "__" in str(name):
            raise EduCompileError(line, col, f"لا يسمح باستخدام الأسماء التي تحتوي على '__' مثل '{name}' لأسباب أمنية.")

    def _collect_functions(self, tree):
        for node in getattr(tree, "children", []):
            if hasattr(node, "data") and node.data == "statement":
                stmt = node.children[0]
                if hasattr(stmt, "data") and stmt.data == "func_def":
                    func_name = str(stmt.children[0])
                    params_node = stmt.children[1]
                    min_a, max_a = 0, 0
                    if params_node is not None and hasattr(params_node, "children"):
                        max_a = len(params_node.children)
                        min_a = sum(1 for p in params_node.children if p.data == "param")
                    self.scopes[0].add(func_name)
                    self.user_func_arity[func_name] = (min_a, max_a)

    def _visit(self, node):
        if not hasattr(node, "data"):
            return

        rule = node.data
        line = getattr(node.meta, "line", 1)
        col = getattr(node.meta, "column", 1)

        if rule == "assignment":
            target_node, expr_node = node.children[0], node.children[1]
            self._visit(expr_node)
            if hasattr(target_node, "data") and target_node.data == "assign_var":
                var_name = str(target_node.children[0])
                self._check_security(var_name, line, col)
                if len(self.scopes) > 1 and var_name in self.scopes[0] and var_name not in self.scopes[-1] and var_name not in self.base_builtins:
                    self.func_globals[self.func_stack[-1]].add(var_name)
                else:
                    self.scopes[-1].add(var_name)
            else:
                self._visit(target_node)
            return

        if rule == "aug_assignment":
            target_node, _, expr_node = node.children[0], node.children[1], node.children[2]
            self._visit(expr_node)
            if hasattr(target_node, "data") and target_node.data == "assign_var":
                var_name = str(target_node.children[0])
                self._check_security(var_name, line, col)
                if not self._is_defined(var_name):
                    suggestion = self._suggest_name(var_name)
                    raise EduCompileError(line, col, f"لا يمكن تحديث المتغير '{var_name}' باستخدام '{node.children[1]}' لأنه غير معرّف مسبقاً.{suggestion}")
                if len(self.scopes) > 1 and var_name in self.scopes[0] and var_name not in self.scopes[-1]:
                    self.func_globals[self.func_stack[-1]].add(var_name)
            else:
                self._visit(target_node)
            return

        if rule == "func_def":
            func_name = str(node.children[0])
            self._check_security(func_name, line, col)
            self.scopes[-1].add(func_name)
            func_key = (line, func_name)
            self.func_stack.append(func_key)
            self.func_globals[func_key] = set()

            local_scope = set()
            params_node, body_node = node.children[1], node.children[2]
            if params_node is not None and hasattr(params_node, "children"):
                for p in params_node.children:
                    p_name = str(p.children[0])
                    self._check_security(p_name, line, col)
                    local_scope.add(p_name)
                    if p.data == "default_param":
                        self._visit(p.children[1])

            self.scopes.append(local_scope)
            self._visit(body_node)
            self.scopes.pop()
            self.func_stack.pop()
            return

        if rule in ("for_range_stmt", "for_in_stmt"):
            loop_var = str(node.children[0])
            self._check_security(loop_var, line, col)
            for expr_child in node.children[1:-1]:
                self._visit(expr_child)
            self.scopes[-1].add(loop_var)
            self.loop_depth += 1
            self._visit(node.children[-1])
            self.loop_depth -= 1
            return

        if rule in ("repeat_stmt", "while_stmt"):
            self._visit(node.children[0])
            self.loop_depth += 1
            self._visit(node.children[1])
            self.loop_depth -= 1
            return

        if rule == "try_stmt":
            try_block, catch_var, catch_block = node.children[0], node.children[1], node.children[2]
            self._visit(try_block)
            if catch_var is not None:
                self.scopes[-1].add(str(catch_var))
            self._visit(catch_block)
            return

        if rule == "break_stmt" and self.loop_depth == 0:
            raise EduCompileError(line, col, "الأمر 'توقف' (break) لا يمكن استخدامه إلا داخل حلقة تكرار.")

        if rule == "continue_stmt" and self.loop_depth == 0:
            raise EduCompileError(line, col, "الأمر 'استمر' (continue) لا يمكن استخدامه إلا داخل حلقة تكرار.")

        if rule == "return_stmt" and not self.func_stack:
            raise EduCompileError(line, col, "الأمر 'ارجع' (return) لا يمكن استخدامه إلا داخل 'دالة' (function).")

        if rule == "func_call":
            func_name = str(node.children[0])
            self._check_security(func_name, line, col)
            arg_list_node = node.children[1] if len(node.children) > 1 and node.children[1] is not None else None
            arg_count = len(arg_list_node.children) if arg_list_node else 0

            if not self._is_defined(func_name):
                suggestion = self._suggest_name(func_name)
                raise EduCompileError(line, col, f"الدالة '{func_name}' غير معروفة.{suggestion}")

            arity_bounds = NORM_BUILTIN_ARITY.get(normalize_ar(func_name)) or self.user_func_arity.get(func_name)
            if arity_bounds:
                min_a, max_a = arity_bounds
                if not (min_a <= arg_count <= max_a):
                    expected_str = f"{min_a}" if min_a == max_a else f"بين {min_a} و {max_a}"
                    raise EduCompileError(
                        line, col,
                        f"الدالة '{func_name}' تتطلب {expected_str} من المدخلات، لكنك مررت لها {arg_count}."
                    )

        if rule == "var":
            var_name = str(node.children[0])
            self._check_security(var_name, line, col)
            if not self._is_defined(var_name):
                suggestion = self._suggest_name(var_name)
                raise EduCompileError(line, col, f"المتغير '{var_name}' غير معرّف قبل استخدامه.{suggestion}")

        for child in node.children:
            self._visit(child)

    def _suggest_name(self, wrong_name):
        visible = self._all_visible_names()
        norm_wrong = normalize_ar(wrong_name)
        for cand in visible:
            if normalize_ar(cand) == norm_wrong:
                return f" هل تقصد '{cand}'؟ (انتبه للهمزة أو التاء المربوطة)"
        matches = difflib.get_close_matches(wrong_name, visible, n=1, cutoff=0.6)
        return f" هل تقصد '{matches[0]}'؟" if matches else ""