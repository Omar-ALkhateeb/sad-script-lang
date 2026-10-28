# lang/compiler/scopes.py
"""Lexical scope tree for semantic analysis."""

from enum import Enum, auto


class ScopeKind(Enum):
    MODULE = auto()
    CLASS = auto()
    FUNCTION = auto()
    LOOP = auto()


class Scope:
    def __init__(self, kind: ScopeKind, parent: "Scope" = None, name: str = ""):
        self.kind = kind
        self.parent = parent
        self.name = name
        self.symbols: set[str] = set()
        self.explicit_globals: set[str] = set()

    def define(self, name: str):
        self.symbols.add(name)

    def inside(self, *kinds: ScopeKind) -> bool:
        curr = self
        while curr is not None:
            if curr.kind in kinds:
                return True
            curr = curr.parent
        return False