# lang/diagnostics/__init__.py
from .syntax_errors import explain_syntax_error
from .runtime_errors import explain_runtime_error

__all__ = ["explain_syntax_error", "explain_runtime_error"]