# lang/types/dict.py
"""Native Dictionary (قاموس) with dot-access and typo suggestions."""

import difflib
from .base import RuntimeError
from .list import List


class Dict(dict):
    """First-class dictionary supporting both dict['key'] and dict.key."""

    __type_name__ = "قاموس"

    def __getitem__(self, key):
        if key not in self:
            keys_str = [str(k) for k in self.keys()]
            matches = difflib.get_close_matches(str(key), keys_str, n=1, cutoff=0.5)
            hint = f" هل تقصد '{matches[0]}'؟" if matches else ""
            available = "، ".join(f"'{k}'" for k in keys_str) if keys_str else "القاموس فارغ"
            raise RuntimeError(
                f"المفتاح '{key}' غير موجود في القاموس.{hint} (المفاتيح المتاحة: {available})"
            )
        return super().__getitem__(key)

    def __getattr__(self, name: str):
        if name.startswith("_"):
            raise AttributeError(name)
        return self.__getitem__(name)

    def __setattr__(self, name: str, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self[name] = value

    def احصل(self, المفتاح, افتراضي=None):
        return super().get(المفتاح, افتراضي)

    def مفاتيح(self) -> List:
        return List(super().keys())

    def قيم(self) -> List:
        return List(super().values())

    def عناصر(self) -> List:
        return List(List([k, v]) for k, v in super().items())

    def احذف(self, المفتاح) -> "Dict":
        if المفتاح not in self:
            raise RuntimeError(f"المفتاح '{المفتاح}' غير موجود في القاموس لحذفه.")
        del self[المفتاح]
        return self

    def يضم(self, المفتاح) -> bool:
        return المفتاح in self

    @property
    def طول(self) -> int:
        return len(self)