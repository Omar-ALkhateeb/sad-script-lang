# lang/compiler/__init__.py
"""Compiler pipeline entry point with line-preserving comment stripper."""

from lark import Lark
from .checker import SemanticAnalyzer, CompileError
from .emitter import Emitter
from .sourcemap import extract_source_line

parser = Lark.open("grammar.lark", rel_to=__file__, parser="lalr", propagate_positions=True)


def _strip_comments(source_code: str) -> str:
    """
    Strips // and # comments outside of string literals while preserving
    exact line numbers and code column positions.
    """
    out_lines = []
    for line in source_code.splitlines():
        in_quote = None
        i = 0
        n = len(line)
        clean_end = n
        while i < n:
            ch = line[i]
            if in_quote:
                if ch == "\\" and i + 1 < n:
                    i += 2
                    continue
                if ch == in_quote:
                    in_quote = None
            else:
                if ch in ('"', "'"):
                    in_quote = ch
                elif ch == "#":
                    clean_end = i
                    break
                elif ch == "/" and i + 1 < n and line[i + 1] == "/":
                    clean_end = i
                    break
            i += 1
        out_lines.append(line[:clean_end].rstrip())
    return "\n".join(out_lines) + "\n"


def compile_source(source_code: str) -> tuple[object, str]:
    """Strips comments (keeping exact line numbers), parses, scope-checks, and emits code."""
    cleaned = _strip_comments(source_code)
    tree = parser.parse(cleaned)
    SemanticAnalyzer().analyze(tree)
    raw_emitted = Emitter().transform(tree)
    if isinstance(raw_emitted, tuple):
        raw_emitted = raw_emitted[0]
    return tree, str(raw_emitted)


__all__ = ["parser", "compile_source", "CompileError", "extract_source_line"]
