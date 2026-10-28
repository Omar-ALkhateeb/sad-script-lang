# lang/stdlib/builtins.py
"""Core built-in functions available globally in every program."""

import random as _py_random
from ..types import RuntimeError, String, List, Dict, typeof, type_name
from .tables import Table, Column, TablesModule
from .charts import bar_chart, line_chart, scatter_chart, pie_chart, ChartsModule
from .math import MathModule
from .random import RandomModule
from .http import HttpModule


def print_out(*args):
    """RTL-aware print function that formats Table objects cleanly."""
    parts = []
    for a in args:
        if isinstance(a, Table):
            parts.append(a.format_rtl())
        elif isinstance(a, bool):
            parts.append("صح" if a else "خطأ")
        elif a is None:
            parts.append("فارغ")
        else:
            parts.append(str(a))
    print(" ".join(parts))


def read_input(prompt_text: str = "") -> String:
    try:
        return String(input(str(prompt_text)))
    except EOFError:
        raise RuntimeError(
            "دالة 'ادخل()' تتطلب طرفية تفاعلية مباشرة. في المتصفح، يمكنك إسناد القيمة مباشرة لمتغير أو قراءتها من ملف."
        )


def length(obj) -> int:
    if hasattr(obj, "__len__"):
        return len(obj)
    raise RuntimeError(f"لا يمكن حساب 'طول()' لقيمة من نوع '{type_name(obj)}'.")


def total(seq):
    if isinstance(seq, Column):
        return seq.مجموع()
    try:
        return sum(seq)
    except Exception:
        raise RuntimeError("دالة 'مجموع()' تتطلب قائمة أو عموداً يحتوي على أرقام فقط.")


def mean(seq) -> float:
    if isinstance(seq, Column):
        return seq.متوسط()
    items = list(seq)
    if not items:
        raise RuntimeError("لا يمكن حساب المتوسط لقائمة فارغة.")
    return float(sum(items) / len(items))


def maximum(*args):
    target = args[0] if len(args) == 1 and hasattr(args[0], "__iter__") else args
    if isinstance(target, Column):
        return target.أكبر()
    items = list(target)
    if not items:
        raise RuntimeError("لا يمكن حساب القيمة العظمى ('أكبر') لقائمة فارغة.")
    return max(items)


def minimum(*args):
    target = args[0] if len(args) == 1 and hasattr(args[0], "__iter__") else args
    if isinstance(target, Column):
        return target.أصغر()
    items = list(target)
    if not items:
        raise RuntimeError("لا يمكن حساب القيمة الصغرى ('أصغر') لقائمة فارغة.")
    return min(items)


def sort_seq(seq, حسب: str = None, تصاعدي: bool = True, **kwargs):
    asc = kwargs.get("ascending", تصاعدي)
    if isinstance(seq, Table):
        return seq.رتب(حسب=حسب, تصاعدي=asc)
    return List(seq).رتب(تصاعدي=asc)


def swap(seq, i: int, j: int) -> List:
    if not isinstance(seq, (list, List)):
        raise RuntimeError("دالة 'بدل()' تتطلب تمرير قائمة كمعامل أول.")
    seq[i], seq[j] = seq[j], seq[i]
    return seq


def indices(seq) -> List:
    return List(range(length(seq)))


def inclusive_range(start: int, end: int = None, step: int = 1) -> List:
    if end is None:
        return List(range(int(start)))
    return List(range(int(start), int(end) + (1 if step > 0 else -1), int(step)))


def to_int(val=0) -> int:
    try:
        return int(float(str(val).strip()))
    except Exception:
        raise RuntimeError(f"لا يمكن تحويل القيمة '{val}' إلى عدد صحيح (عدد).")


def to_float(val=0.0) -> float:
    try:
        return float(str(val).strip())
    except Exception:
        raise RuntimeError(f"لا يمكن تحويل القيمة '{val}' إلى عدد كسري (كسر).")


def to_bool(val=False) -> bool:
    if isinstance(val, str):
        v = val.strip()
        if v in ("صح", "صحيح", "true", "True", "1", "١"):
            return True
        if v in ("خطأ", "خطا", "false", "False", "0", "٠", "", "فارغ", "عدم"):
            return False
    return bool(val)


def to_string(val="") -> String:
    if isinstance(val, bool):
        return String("صح" if val else "خطأ")
    if val is None:
        return String("فارغ")
    return String(str(val))


def to_list(val=None) -> List:
    if val is None:
        return List()
    if isinstance(val, Column):
        return val.كقائمة()
    return List(val)


def to_dict(val=None) -> Dict:
    if val is None:
        return Dict()
    return Dict(val)


CORE_BUILTINS = {
    # Internal runtime hooks
    "__print__": print_out,
    "List": List,
    "Dict": Dict,
    "String": String,
    # 1-Word Type Constructors (+ Backward-Compatible Aliases)
    "نوع": typeof,
    "عدد": to_int,
    "صحيح": to_int,
    "عدد_صحيح": to_int,
    "كسر": to_float,
    "عشري": to_float,
    "عدد_عشري": to_float,
    "نص": to_string,
    "منطق": to_bool,
    "منطقي": to_bool,
    "قائمة": to_list,
    "قاموس": to_dict,
    "جدول": Table,
    "جدول_بيانات": Table,
    "عمود": Column,
    # Core Built-in Functions
    "اطبع": print_out,
    "إطبع": print_out,
    "ادخل": read_input,
    "إدخل": read_input,
    "طول": length,
    "مجموع": total,
    "متوسط": mean,
    "أكبر": maximum,
    "اكبر": maximum,
    "أصغر": minimum,
    "اصغر": minimum,
    "قرب": round,
    "مطلق": abs,
    "رتب": sort_seq,
    "بدل": swap,
    "تبديل": swap,
    "فهارس": indices,
    "مدى": inclusive_range,
    "عشوائي": _py_random.randint,
    "اختر": RandomModule.اختر,
    "اختر_عشوائي": RandomModule.اختر,
    # Data & Chart Global Shortcuts (1-word chart methods live on `جدول` and `رسوم`)
    "اقرأ": Table.from_csv,
    "إقرأ": Table.from_csv,
    "اقرأ_جدول": Table.from_csv,
    "اقرأ_ملف": Table.from_csv,
    "احفظ": lambda tbl, path: tbl.احفظ(path),
    "احفظ_جدول": lambda tbl, path: tbl.احفظ(path),
    "ارسم_أعمدة": bar_chart,
    "ارسم_اعمدة": bar_chart,
    "ارسم_خط": line_chart,
    "ارسم_نقاط": scatter_chart,
    "ارسم_دائري": pie_chart,
    # Pre-bound Standard Library Modules
    "جداول": TablesModule(),
    "رسوم": ChartsModule(),
    "رياضيات": MathModule(),
    "عشوائيات": RandomModule(),
    "طلبات": HttpModule(),
    "صح": True,
    "صحيح": True,
    "خطأ": False,
    "خطا": False,
    "فارغ": None,
    "عدم": None,
}
