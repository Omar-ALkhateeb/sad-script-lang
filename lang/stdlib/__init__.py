# lang/stdlib/__init__.py
"""Registry of standard library modules and core built-ins."""

from .builtins import CORE_BUILTINS, print_out
from .tables import Table, Column, TablesModule
from .charts import ChartsModule, clear_charts, get_charts
from .math import MathModule
from .random import RandomModule
from .http import HttpModule, Response

BUILTIN_MODULES = {
    "جداول": TablesModule(),
    "باندا": TablesModule(),
    "رسوم": ChartsModule(),
    "رياضيات": MathModule(),
    "عشوائيات": RandomModule(),
    "طلبات": HttpModule(),
    "شبكة": HttpModule(),
}

__all__ = [
    "CORE_BUILTINS",
    "BUILTIN_MODULES",
    "Table",
    "Column",
    "Response",
    "clear_charts",
    "get_charts",
    "print_out",
]