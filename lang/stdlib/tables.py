# lang/stdlib/tables.py
"""Tabular Data Engine (`استورد جداول`) with concise 1-word Arabic methods."""

import difflib
from pathlib import Path
import pandas as pd

from ..types import RuntimeError, List, Dict
from .charts import bar_chart, line_chart, scatter_chart, pie_chart


class Column:
    """Represents a single tabular column (عمود)."""

    __type_name__ = "عمود"

    def __init__(self, data):
        if isinstance(data, Column):
            self._s = data._s.copy()
        elif isinstance(data, pd.Series):
            self._s = data
        else:
            self._s = pd.Series(list(data) if not isinstance(data, list) else data)

    def متوسط(self) -> float:
        return float(self._s.mean())

    def مجموع(self):
        val = self._s.sum()
        return val.item() if hasattr(val, "item") else val

    def أكبر(self):
        val = self._s.max()
        return val.item() if hasattr(val, "item") else val

    def اكبر(self):
        return self.أكبر()

    def أصغر(self):
        val = self._s.min()
        return val.item() if hasattr(val, "item") else val

    def اصغر(self):
        return self.أصغر()

    def وسيط(self) -> float:
        return float(self._s.median())

    def عدد(self) -> int:
        return int(self._s.count())

    def فريد(self) -> List:
        return List(self._s.unique().tolist())

    def كقائمة(self) -> List:
        return List(self._s.tolist())

    def _unwrap(self, other):
        return other._s if isinstance(other, Column) else other

    def __add__(self, other): return Column(self._s + self._unwrap(other))
    def __radd__(self, other): return Column(self._unwrap(other) + self._s)
    def __sub__(self, other): return Column(self._s - self._unwrap(other))
    def __rsub__(self, other): return Column(self._unwrap(other) - self._s)
    def __mul__(self, other): return Column(self._s * self._unwrap(other))
    def __rmul__(self, other): return Column(self._unwrap(other) * self._s)
    def __truediv__(self, other): return Column(self._s / self._unwrap(other))
    def __rtruediv__(self, other): return Column(self._unwrap(other) / self._s)
    def __gt__(self, other): return Column(self._s > self._unwrap(other))
    def __lt__(self, other): return Column(self._s < self._unwrap(other))
    def __ge__(self, other): return Column(self._s >= self._unwrap(other))
    def __le__(self, other): return Column(self._s <= self._unwrap(other))
    def __eq__(self, other): return Column(self._s == self._unwrap(other))
    def __ne__(self, other): return Column(self._s != self._unwrap(other))

    def __len__(self) -> int:
        return len(self._s)

    def __iter__(self):
        return iter(self._s.tolist())

    def __repr__(self) -> str:
        return f"عمود({self._s.tolist()})"


class TableGroup:
    """Grouped table returned by جدول.تجميع('العمود')."""

    __type_name__ = "تجميع"

    def __init__(self, grouped):
        self._g = grouped

    def متوسط(self) -> "Table":
        return Table(self._g.mean(numeric_only=True).reset_index())

    def مجموع(self) -> "Table":
        return Table(self._g.sum(numeric_only=True).reset_index())

    def عدد(self) -> "Table":
        return Table(self._g.count().reset_index())

    def أكبر(self) -> "Table":
        return Table(self._g.max(numeric_only=True).reset_index())

    def أصغر(self) -> "Table":
        return Table(self._g.min(numeric_only=True).reset_index())


class Table:
    """First-class Table (جدول) wrapping pd.DataFrame."""

    __type_name__ = "جدول"

    def __init__(self, data):
        if isinstance(data, Table):
            self._df = data._df.copy()
        elif isinstance(data, pd.DataFrame):
            self._df = data.copy()
        else:
            try:
                self._df = pd.DataFrame(data)
            except Exception:
                raise RuntimeError(
                    "تعذر إنشاء الجدول من البيانات المدخلة. تأكد من تمرير قاموس أعمدة أو قائمة صفوف."
                )

    @classmethod
    def from_csv(cls, filename: str) -> "Table":
        path = Path(str(filename))
        if not path.exists():
            available_csvs = [p.name for p in Path(".").glob("*.csv")]
            hint = f" (ملفات CSV المتاحة: {'، '.join(available_csvs)})" if available_csvs else ""
            raise RuntimeError(f"ملف البيانات '{filename}' غير موجود في المشروع.{hint}")
        try:
            return cls(pd.read_csv(path))
        except Exception:
            raise RuntimeError(f"تعذر قراءة ملف البيانات '{filename}'. تأكد من أنه بتنسيق CSV صحيح.")

    def احفظ(self, filename: str) -> "Table":
        self._df.to_csv(str(filename), index=False)
        return self

    def _check_col(self, col_name: str):
        col_str = str(col_name)
        if col_str not in self._df.columns:
            available = [str(c) for c in self._df.columns]
            matches = difflib.get_close_matches(col_str, available, n=1, cutoff=0.5)
            hint = f" هل تقصد '{matches[0]}'؟" if matches else ""
            cols_str = "، ".join(f"'{c}'" for c in available)
            raise RuntimeError(
                f"العمود '{col_str}' غير موجود في الجدول.{hint} "
                f"(الأعمدة المتاحة: {cols_str})"
            )

    def __getitem__(self, key):
        if isinstance(key, Column):
            return Table(self._df[key._s])
        if isinstance(key, (list, List)):
            cols = [str(c) for c in key]
            for col in cols:
                self._check_col(col)
            return Table(self._df[cols])
        col_str = str(key)
        self._check_col(col_str)
        return Column(self._df[col_str])

    def __setitem__(self, key, value):
        col_str = str(key)
        if isinstance(value, Column):
            self._df[col_str] = value._s.values
        else:
            try:
                self._df[col_str] = value
            except ValueError:
                raise RuntimeError(
                    f"طول القيم المضافة للعمود '{col_str}' لا يطابق عدد صفوف الجدول ({len(self._df)})."
                )

    @property
    def الأعمدة(self) -> List:
        return List(str(c) for c in self._df.columns)

    @property
    def الشكل(self) -> List:
        return List([int(self._df.shape[0]), int(self._df.shape[1])])

    @property
    def صفوف(self) -> int:
        return int(self._df.shape[0])

    @property
    def عدد_الصفوف(self) -> int:
        return int(self._df.shape[0])

    @property
    def طول(self) -> int:
        return len(self._df)

    def __len__(self) -> int:
        return len(self._df)

    def أول(self, ن: int = 5) -> "Table":
        return Table(self._df.head(int(ن)))

    def اول(self, ن: int = 5) -> "Table":
        return self.أول(ن)

    def آخر(self, ن: int = 5) -> "Table":
        return Table(self._df.tail(int(ن)))

    def اخر(self, ن: int = 5) -> "Table":
        return self.آخر(ن)

    def نظف(self) -> "Table":
        return Table(self._df.dropna())

    def حذف_الفارغ(self) -> "Table":
        return self.نظف()

    def املأ(self, القيمة=0) -> "Table":
        return Table(self._df.fillna(القيمة))

    def املأ_الفارغ(self, القيمة=0) -> "Table":
        return self.املأ(القيمة)

    def رتب(self, حسب: str = None, تصاعدي: bool = True, **kwargs) -> "Table":
        target_col = str(حسب or kwargs.get("by", ""))
        asc = kwargs.get("ascending", تصاعدي)
        if not target_col:
            raise RuntimeError("يرجى تحديد اسم العمود للترتيب، مثال: جدول.رتب('المعدل')")
        if not isinstance(asc, bool):
            raise RuntimeError(
                "المعامل 'تصاعدي' في دالة 'رتب()' يتطلب قيمة منطقية ('صح' أو 'خطأ') — هل تقصد 'خطأ'؟"
            )
        self._check_col(target_col)
        return Table(self._df.sort_values(by=target_col, ascending=asc))
    
    def رتب_قيم(self, حسب: str = None, تصاعدي: bool = True, **kwargs) -> "Table":
        return self.رتب(حسب=حسب, تصاعدي=تصاعدي, **kwargs)

    def صفي(self, شرط: Column) -> "Table":
        if not isinstance(شرط, Column):
            raise RuntimeError(
                "دالة 'صفي()' تتطلب شرط مقارنة على عمود، مثال: جدول.صفي(جدول['المعدل'] >= ٨٥)"
            )
        return Table(self._df[شرط._s])

    def رشح(self, شرط: Column) -> "Table":
        return self.صفي(شرط)

    def تجميع(self, العمود: str) -> TableGroup:
        col_str = str(العمود)
        self._check_col(col_str)
        return TableGroup(self._df.groupby(col_str))

    def ملخص(self) -> "Table":
        return Table(self._df.describe().reset_index())

    def صف(self, فهرس: int) -> Dict:
        if not isinstance(فهرس, int) or فهرس < 0 or فهرس >= len(self._df):
            raise RuntimeError(
                f"رقم الصف ({فهرس}) خارج حدود الجدول (الصفوف المتاحة من 0 إلى {max(0, len(self._df) - 1)})."
            )
        row_dict = self._df.iloc[فهرس].to_dict()
        return Dict({str(k): (v.item() if hasattr(v, "item") else v) for k, v in row_dict.items()})

    def أعمدة(self, س: str, ص: str, العنوان="الرسم البياني", **kwargs):
        s_col, y_col = str(س), str(ص)
        self._check_col(s_col)
        self._check_col(y_col)
        bar_chart(self._df[s_col], self._df[y_col], العنوان=kwargs.get("title", العنوان), المحور_السيني=s_col, المحور_الصادي=y_col)

    def اعمدة(self, س: str, ص: str, العنوان="الرسم البياني", **kwargs):
        self.أعمدة(س, ص, العنوان=العنوان, **kwargs)

    def ارسم_أعمدة(self, س: str, ص: str, العنوان="الرسم البياني", **kwargs):
        self.أعمدة(س, ص, العنوان=العنوان, **kwargs)

    def ارسم_اعمدة(self, س: str, ص: str, العنوان="الرسم البياني", **kwargs):
        self.أعمدة(س, ص, العنوان=العنوان, **kwargs)

    def خط(self, س: str, ص: str, العنوان="الرسم الخطي", **kwargs):
        s_col, y_col = str(س), str(ص)
        self._check_col(s_col)
        self._check_col(y_col)
        line_chart(self._df[s_col], self._df[y_col], العنوان=kwargs.get("title", العنوان), المحور_السيني=s_col, المحور_الصادي=y_col)

    def ارسم_خط(self, س: str, ص: str, العنوان="الرسم الخطي", **kwargs):
        self.خط(س, ص, العنوان=العنوان, **kwargs)

    def نقاط(self, س: str, ص: str, العنوان="مخطط التبعثر", **kwargs):
        s_col, y_col = str(س), str(ص)
        self._check_col(s_col)
        self._check_col(y_col)
        scatter_chart(self._df[s_col], self._df[y_col], العنوان=kwargs.get("title", العنوان), المحور_السيني=s_col, المحور_الصادي=y_col)

    def ارسم_نقاط(self, س: str, ص: str, العنوان="مخطط التبعثر", **kwargs):
        self.نقاط(س, ص, العنوان=العنوان, **kwargs)

    def دائري(self, التسميات: str, القيم: str, العنوان="الرسم الدائري", **kwargs):
        l_col, v_col = str(التسميات), str(القيم)
        self._check_col(l_col)
        self._check_col(v_col)
        pie_chart(self._df[l_col], self._df[v_col], العنوان=kwargs.get("title", العنوان))

    def ارسم_دائري(self, التسميات: str, القيم: str, العنوان="الرسم الدائري", **kwargs):
        self.دائري(التسميات, القيم, العنوان=العنوان, **kwargs)

    def format_rtl(self) -> str:
        RLM = "\u200F"
        df_head = self._df.head(50)
        cols = [str(c) for c in df_head.columns]
        rows = [[str(cell) for cell in row] for row in df_head.values.tolist()]

        widths = []
        for idx, col in enumerate(cols):
            col_cells = [r[idx] for r in rows] if rows else []
            widths.append(max([len(col)] + [len(c) for c in col_cells]) + 2)

        header = f"{RLM} │ {RLM}".join(c.center(widths[i]) for i, c in enumerate(cols))
        sep = "─┼─".join("─" * w for w in widths)
        body_lines = [
            f"{RLM}" + f"{RLM} │ {RLM}".join(r[i].center(widths[i]) for i in range(len(cols))) + f"{RLM}"
            for r in rows
        ]
        return f"{RLM}{header}{RLM}\n{RLM}{sep}{RLM}\n" + "\n".join(body_lines)

    def to_ide_dict(self, name: str) -> dict:
        df_clean = self._df.head(100).fillna("")
        return {
            "name": name,
            "shape": [int(self._df.shape[0]), int(self._df.shape[1])],
            "columns": [str(c) for c in df_clean.columns],
            "dtypes": {str(col): str(dtype) for col, dtype in self._df.dtypes.items()},
            "rows": [[str(cell) for cell in row] for row in df_clean.values.tolist()],
        }

    def __repr__(self) -> str:
        return self.format_rtl()


class TablesModule:
    """Importable `جداول` standard library module."""

    __type_name__ = "مكتبة"

    @staticmethod
    def اقرأ(filename: str) -> Table:
        return Table.from_csv(filename)

    @staticmethod
    def اقرأ_ملف(filename: str) -> Table:
        return Table.from_csv(filename)

    @staticmethod
    def اقرأ_جدول(filename: str) -> Table:
        return Table.from_csv(filename)

    @staticmethod
    def احفظ(table: Table, filename: str) -> Table:
        if not isinstance(table, Table):
            raise RuntimeError("الدالة 'احفظ' تتطلب تمرير كائن من نوع 'جدول'.")
        return table.احفظ(filename)

    @staticmethod
    def احفظ_ملف(table: Table, filename: str) -> Table:
        return TablesModule.احفظ(table, filename)

    @staticmethod
    def أنشئ(data) -> Table:
        return Table(data)

    @staticmethod
    def جدول(data) -> Table:
        return Table(data)

    @staticmethod
    def عمود(values) -> Column:
        return Column(values)
