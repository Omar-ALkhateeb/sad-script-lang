# lang/types/string.py
"""Native String (نص) implementation with single-word Arabic methods."""

from .base import RuntimeError


class String(str):
    """First-class Arabic-aware string type."""

    __type_name__ = "نص"

    def قسم(self, فاصل: str = None):
        from .list import List
        return List(String(p) for p in super().split(فاصل))

    def استبدل(self, القديم: str, الجديد: str) -> "String":
        return String(super().replace(str(القديم), str(الجديد)))

    def نظف(self, أحرف: str = None) -> "String":
        return String(super().strip(أحرف))

    def يبدأ(self, بادئة: str) -> bool:
        return super().startswith(str(بادئة))

    def يبدأ_بـ(self, بادئة: str) -> bool:
        return self.يبدأ(بادئة)

    def ينتهي(self, لاحقة: str) -> bool:
        return super().endswith(str(لاحقة))

    def ينتهي_بـ(self, لاحقة: str) -> bool:
        return self.ينتهي(لاحقة)

    def يضم(self, جزء: str) -> bool:
        return str(جزء) in self

    def موقع(self, جزء: str) -> int:
        return super().find(str(جزء))

    def كبير(self) -> "String":
        return String(super().upper())

    def صغير(self) -> "String":
        return String(super().lower())

    def حرف(self, index: int) -> "String":
        if not isinstance(index, int):
            raise RuntimeError("فهرس النص يجب أن يكون عدداً صحيحاً.")
        if index < -len(self) or index >= len(self):
            raise RuntimeError(
                f"الفهرس ({index}) خارج حدود النص (طول النص {len(self)} حرفاً)."
            )
        return String(super().__getitem__(index))

    @property
    def طول(self) -> int:
        return len(self)