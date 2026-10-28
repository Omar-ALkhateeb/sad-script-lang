# lang/compiler/checker.py
"""Static semantic analyzer enforcing scope rules before execution."""

from lark import Tree
from .scopes import Scope, ScopeKind


class CompileError(Exception):
    def __init__(self, message: str, line: int = 1, col: int = 1):
        super().__init__(message)
        self.message = message
        self.line = line or 1
        self.col = col or 1


class SemanticAnalyzer:
    def __init__(self):
        self.current_scope = Scope(ScopeKind.MODULE, name="<module>")

    def _push(self, kind: ScopeKind, name: str = ""):
        self.current_scope = Scope(kind, parent=self.current_scope, name=name)

    def _pop(self):
        if self.current_scope.parent is not None:
            self.current_scope = self.current_scope.parent

    def analyze(self, tree: Tree):
        self._visit(tree)

    def _visit(self, node):
        if not isinstance(node, Tree):
            return

        data = node.data
        line = getattr(node.meta, "line", 1)
        col = getattr(node.meta, "column", 1)

        if data in ("break_stmt", "continue_stmt"):
            if not self.current_scope.inside(ScopeKind.LOOP):
                kw = "توقف" if data == "break_stmt" else "استمر"
                raise CompileError(
                    f"لا يمكن استخدام الأمر '{kw}' خارج الحلقات التكرارية (كرر / لكل / طالما).",
                    line, col,
                )

        elif data == "return_stmt":
            if not self.current_scope.inside(ScopeKind.FUNCTION):
                raise CompileError(
                    "لا يمكن استخدام الأمر 'ارجع' خارج تعريف الدالة (دالة ...).",
                    line, col,
                )

        elif data == "global_stmt":
            if not self.current_scope.inside(ScopeKind.FUNCTION):
                raise CompileError(
                    "الكلمة المفتاحية 'عام' تستخدم فقط داخل الدوال للإشارة إلى متغير عام.",
                    line, col,
                )

        elif data == "class_def":
            class_name = str(node.children[0])
            self.current_scope.define(class_name)
            self._push(ScopeKind.CLASS, name=class_name)
            for child in node.children[1:]:
                self._visit(child)
            self._pop()
            return

        elif data in ("func_def", "method_def"):
            func_name = str(node.children[0])
            self.current_scope.define(func_name)
            self._push(ScopeKind.FUNCTION, name=func_name)
            for child in node.children[1:]:
                self._visit(child)
            self._pop()
            return

        elif data in ("repeat_stmt", "for_range_stmt", "for_each_stmt", "while_stmt"):
            self._push(ScopeKind.LOOP)
            for child in node.children:
                self._visit(child)
            self._pop()
            return

        for child in node.children:
            self._visit(child)
