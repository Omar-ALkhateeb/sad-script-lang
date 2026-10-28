# lang/types/base.py
"""Core runtime error and minimal single-word Type representations."""


class RuntimeError(Exception):
    """Native runtime error raised directly by built-in types and stdlib modules."""

    is_native_error = True

    def __init__(self, message: str, line_no: int = None):
        super().__init__(message)
        self.message = message
        self.line_no = line_no


class Type:
    """First-class type object returned by نوع(x)."""

    __type_name__ = "نوع"

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if isinstance(other, Type):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other.strip()
        return False


def type_name(val) -> str:
    """Returns the minimal 1-word Arabic type name for any runtime value."""
    if val is None:
        return "فارغ"
    if isinstance(val, bool):
        return "منطق"
    if isinstance(val, int):
        return "عدد"
    if isinstance(val, float):
        return "كسر"
    if hasattr(val, "__type_name__"):
        return str(val.__type_name__)
    if isinstance(val, str):
        return "نص"
    if isinstance(val, list):
        return "قائمة"
    if isinstance(val, dict):
        return "قاموس"
    if hasattr(val, "__class__") and val.__class__.__module__ not in ("builtins",):
        return val.__class__.__name__
    return "كائن"


def typeof(val) -> Type:
    """Built-in نوع(x) function."""
    return Type(type_name(val))