# lang/types/list.py
"""Native List (قائمة) implementation."""

from .base import RuntimeError, type_name
from .string import String


class List(list):
    """First-class list with bounds validation and Arabic methods."""

    __type_name__ = "قائمة"

    def _validate_index(self, idx, for_write: bool = False):
        if not isinstance(idx, int) or isinstance(idx, bool):
            raise RuntimeError(
                f"فهرس القائمة يجب أن يكون عدداً صحيحاً، وليس '{type_name(idx)}'."
            )
        if idx < -len(self) or idx >= len(self):
            if len(self) == 0:
                raise RuntimeError("لا يمكن الوصول إلى عنصر داخل قائمة فارغة.")
            action = "تعديل" if for_write else "قراءة"
            raise RuntimeError(
                f"تعذر {action} العنصر في الفهرس ({idx}): القائمة تحتوي على {len(self)} عناصر فقط "
                f"(الفهارس المتاحة من 0 إلى {len(self) - 1})."
            )

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return List(super().__getitem__(idx))
        self._validate_index(idx, for_write=False)
        return super().__getitem__(idx)

    def __setitem__(self, idx, val):
        if isinstance(idx, slice):
            super().__setitem__(idx, val)
            return
        self._validate_index(idx, for_write=True)
        super().__setitem__(idx, val)

    def أضف(self, عنصر) -> "List":
        super().append(عنصر)
        return self

    def اضف(self, عنصر) -> "List":
        return self.أضف(عنصر)

    def أدرج(self, فهرس: int, عنصر) -> "List":
        super().insert(int(فهرس), عنصر)
        return self

    def احذف(self, عنصر) -> "List":
        if عنصر not in self:
            raise RuntimeError(f"العنصر '{عنصر}' غير موجود في القائمة لحذفه.")
        super().remove(عنصر)
        return self

    def اسحب(self, فهرس: int = -1):
        if len(self) == 0:
            raise RuntimeError("لا يمكن سحب عنصر من قائمة فارغة.")
        self._validate_index(فهرس, for_write=True)
        return super().pop(فهرس)

    def امسح(self) -> "List":
        super().clear()
        return self

    def أول(self, ن: int = None):
        if ن is None:
            if len(self) == 0:
                raise RuntimeError("القائمة فارغة ولا تحتوي على عنصر أول.")
            return self[0]
        return List(self[: int(ن)])

    def اول(self, ن: int = None):
        return self.أول(ن)

    def آخر(self, ن: int = None):
        if ن is None:
            if len(self) == 0:
                raise RuntimeError("القائمة فارغة ولا تحتوي على عنصر أخير.")
            return self[-1]
        return List(self[-int(ن) :])

    def اخر(self, ن: int = None):
        return self.آخر(ن)

    def رتب(self, تصاعدي: bool = True) -> "List":
        try:
            return List(sorted(self, reverse=not تصاعدي))
        except TypeError:
            raise RuntimeError(
                "لا يمكن ترتيب قائمة تحتوي على أنواع غير متجانسة (مثل نصوص وأرقام معاً)."
            )

    def اعكس(self) -> "List":
        return List(reversed(self))

    def اربط(self, فاصل: str = "، ") -> String:
        return String(str(فاصل).join(str(x) for x in self))

    def يضم(self, عنصر) -> bool:
        return عنصر in self

    def عدد(self, عنصر) -> int:
        return super().count(عنصر)

    @property
    def طول(self) -> int:
        return len(self)