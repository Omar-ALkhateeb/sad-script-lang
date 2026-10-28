# lang/stdlib/random.py
"""Random Standard Library (`استورد عشوائيات`)."""

import random as _py_random
from ..types import RuntimeError, List


class RandomModule:
    __type_name__ = "مكتبة"

    @staticmethod
    def عدد(من: int = 0, إلى: int = 100) -> int:
        return _py_random.randint(int(من), int(إلى))

    @staticmethod
    def رقم_صحيح(من: int = 0, إلى: int = 100) -> int:
        return RandomModule.عدد(من, إلى)

    @staticmethod
    def كسر(من: float = 0.0, إلى: float = 1.0) -> float:
        return round(_py_random.uniform(float(من), float(إلى)), 4)

    @staticmethod
    def رقم_عشري(من: float = 0.0, إلى: float = 1.0) -> float:
        return RandomModule.كسر(من, إلى)

    @staticmethod
    def اختر(قائمة):
        if not قائمة or len(قائمة) == 0:
            raise RuntimeError("لا يمكن الاختيار العشوائي من قائمة فارغة.")
        return _py_random.choice(list(قائمة))

    @staticmethod
    def اخلط(قائمة) -> List:
        copied = List(قائمة)
        _py_random.shuffle(copied)
        return copied

    @staticmethod
    def عينة(قائمة, العدد: int) -> List:
        if int(العدد) > len(قائمة):
            raise RuntimeError(
                f"حجم العينة المطلوبة ({العدد}) أكبر من عدد عناصر القائمة ({len(قائمة)})."
            )
        return List(_py_random.sample(list(قائمة), int(العدد)))