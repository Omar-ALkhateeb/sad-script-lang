# lang/stdlib/math.py
"""Math Standard Library (`استورد رياضيات`) with standard Arabic math names."""

import math as _py_math
from ..types import RuntimeError


class MathModule:
    __type_name__ = "مكتبة"

    باي = _py_math.pi
    ط = _py_math.pi
    هـ = _py_math.e

    @staticmethod
    def جذر(x: float) -> float:
        if x < 0:
            raise RuntimeError("لا يمكن حساب الجذر التربيعي لعدد سالب.")
        return _py_math.sqrt(x)

    @staticmethod
    def قوة(الأساس: float, الأس: float) -> float:
        return _py_math.pow(الأساس, الأس)

    @staticmethod
    def مطلق(x):
        return abs(x)

    @staticmethod
    def سقف(x: float) -> int:
        return _py_math.ceil(x)

    @staticmethod
    def أرضية(x: float) -> int:
        return _py_math.floor(x)

    @staticmethod
    def جا(زاوية: float) -> float:
        return _py_math.sin(_py_math.radians(زاوية))

    @staticmethod
    def جيب(زاوية: float) -> float:
        return MathModule.جا(زاوية)

    @staticmethod
    def جتا(زاوية: float) -> float:
        return _py_math.cos(_py_math.radians(زاوية))

    @staticmethod
    def جيب_تمام(زاوية: float) -> float:
        return MathModule.جتا(زاوية)

    @staticmethod
    def ظا(زاوية: float) -> float:
        return _py_math.tan(_py_math.radians(زاوية))

    @staticmethod
    def ظل(زاوية: float) -> float:
        return MathModule.ظا(زاوية)

    @staticmethod
    def لوغاريتم(x: float, الأساس: float = _py_math.e) -> float:
        if x <= 0:
            raise RuntimeError("حساب اللوغاريتم يتطلب عدداً موجباً أكبر من الصفر.")
        return _py_math.log(x, الأساس)