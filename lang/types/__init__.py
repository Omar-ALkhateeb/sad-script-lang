# lang/types/__init__.py
"""Exports core built-in types and value wrappers."""

from .base import RuntimeError, Type, typeof, type_name
from .string import String
from .list import List
from .dict import Dict


def wrap(val):
    """Recursively converts raw Python containers into native containers."""
    if isinstance(val, (List, Dict, String)):
        return val
    if isinstance(val, list):
        return List(wrap(x) for x in val)
    if isinstance(val, dict):
        return Dict({k: wrap(v) for k, v in val.items()})
    if isinstance(val, str):
        return String(val)
    return val


__all__ = [
    "RuntimeError",
    "Type",
    "typeof",
    "type_name",
    "String",
    "List",
    "Dict",
    "wrap",
]