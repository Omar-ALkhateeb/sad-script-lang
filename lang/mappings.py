"""Centralized Arabic-to-Python vocabulary, signatures, and orthography normalizers."""

ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

def normalize_ar(word):
    """Normalizes Alef variants (أ/إ/آ -> ا), Taa Marbuta (ة -> ه), and strips Tatweel (ـ)."""
    table = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ة": "ه", "ى": "ي", "ـ": ""})
    return str(word).translate(table)

# 1. Global Built-in Functions
BUILTIN_MAP = {
    "طول": "len", "length": "len",
    "مجموع": "sum", "sum": "sum",
    "أصغر": "min", "min": "min",
    "أكبر": "max", "max": "max",
    "قرب": "round", "round": "round",
    "مطلق": "abs", "abs": "abs",
    "ادخل": "edu_input", "input": "edu_input",
    "نص": "str", "عدد_صحيح": "int", "عدد_عشري": "float", "قائمة": "list", "نوع": "type",
    "متوسط": "edu_average", "average": "edu_average",
    "رتب": "edu_sort", "sort_list": "edu_sort",
    "بدل": "edu_swap", "swap": "edu_swap",
    "عشوائي": "edu_random_int", "random_int": "edu_random_int",
    "اختر_عشوائي": "edu_random_choice", "random_choice": "edu_random_choice",
    "اقرأ_جدول": "edu_load_csv", "load_csv": "edu_load_csv",
    "احفظ_جدول": "edu_save_csv", "save_csv": "edu_save_csv",
    "عمود": "edu_column", "get_column": "edu_column",
    "صف_بيانات": "edu_filter", "filter_data": "edu_filter",
    "ارسم_أعمدة": "edu_bar_chart", "draw_bar": "edu_bar_chart",
    "ارسم_خط": "edu_line_chart", "draw_line": "edu_line_chart",
    "ارسم_نقاط": "edu_scatter_chart", "draw_scatter": "edu_scatter_chart",
    "ارسم_دائري": "edu_pie_chart", "draw_pie": "edu_pie_chart",
}

# 2. Expected (min_args, max_args) for Compile-Time Validation
BUILTIN_ARITY = {
    "طول": (1, 1), "length": (1, 1),
    "متوسط": (1, 1), "average": (1, 1),
    "مطلق": (1, 1), "abs": (1, 1),
    "قرب": (1, 2), "round": (1, 2),
    "بدل": (3, 3), "swap": (3, 3),
    "عشوائي": (2, 2), "random_int": (2, 2),
    "اختر_عشوائي": (1, 1), "random_choice": (1, 1),
    "ادخل": (0, 1), "input": (0, 1),
    "رتب": (1, 2), "sort_list": (1, 2),
    "اقرأ_جدول": (1, 5), "load_csv": (1, 5),
    "احفظ_جدول": (2, 3), "save_csv": (2, 3),
    "عمود": (2, 2), "get_column": (2, 2),
    "صف_بيانات": (2, 2), "filter_data": (2, 2),
    "ارسم_أعمدة": (2, 5), "draw_bar": (2, 5),
    "ارسم_خط": (2, 5), "draw_line": (2, 5),
    "ارسم_نقاط": (2, 5), "draw_scatter": (2, 5),
    "ارسم_دائري": (2, 3), "draw_pie": (2, 3),
}

# 3. Dot-Methods on Objects (Pandas DataFrame/Series, Lists, Strings, Dicts)
METHOD_MAP = {
    "جدول_بيانات": "DataFrame", "سلسلة": "Series", "اقرأ_جدول": "read_csv", "احفظ_جدول": "to_csv",
    "أول": "head", "آخر": "tail", "ملخص": "describe", "معلومات": "info",
    "حذف_الفارغ": "dropna", "املأ_الفارغ": "fillna", "احذف_عمود": "drop", "أعد_تسمية": "rename",
    "رتب_قيم": "sort_values", "رتب_فهرس": "sort_index", "تجميع": "groupby", "استعلم": "query",
    "متوسط": "mean", "مجموع": "sum", "أكبر": "max", "أصغر": "min", "وسيط": "median", "عدد": "count",
    "فريد": "unique", "عدد_القيم": "value_counts", "نسخة": "copy", "إعادة_فهرسة": "reset_index",
    "أضف": "append", "أدرج": "insert", "احذف": "remove", "اسحب": "pop", "امسح": "clear", "اعكس": "reverse",
    "استبدل": "replace", "قسم": "split", "ادمج": "join", "نظف": "strip",
    "مفاتيح": "keys", "قيم": "values", "عناصر": "items",
}

# 4. Dot-Attributes on Objects
ATTR_MAP = {
    "الأعمدة": "columns", "الشكل": "shape", "الأنواع": "dtypes",
    "القيم": "values", "الفهرس": "index", "موقع": "loc", "موقع_رقمي": "iloc", "منقول": "T",
}

# 5. Named Keyword Arguments
KWARG_MAP = {
    "حسب": "by", "تصاعدي": "ascending", "محور": "axis", "تعديل_مباشر": "inplace",
    "الأعمدة": "columns", "الفهرس": "index", "العنوان": "title",
    "المحور_السيني": "xlabel", "المحور_الصادي": "ylabel",
}

# 6. Error Diagnostic Translations
TYPE_NAMES_AR = {
    "int": "عدد صحيح", "float": "عدد عشري", "str": "نص",
    "list": "قائمة", "dict": "قاموس", "bool": "قيمة منطقية (صحيح/خطأ)",
    "NoneType": "قيمة فارغة (فارغ)", "DataFrame": "جدول بيانات (DataFrame)",
    "Series": "عمود بيانات (Series)", "function": "دالة",
    "builtin_function_or_method": "دالة مدمجة",
}

EXPECTED_TOKENS_AR = {
    "RPAR": "قوس دائري مغلق ')'", "LPAR": "قوس دائري مفتوح '('",
    "RBRACE": "قوس مجموعة مغلق '}' لإنهاء البلوك", "LBRACE": "قوس مجموعة مفتوح '{' لبدء البلوك",
    "RSQB": "قوس مربع مغلق ']'", "LSQB": "قوس مربع مفتوح '['",
    "EQUAL": "علامة يساوي '='", "COLON": "نقطتان رأسيتان ':' بين المفتاح والقيمة",
    "NUMBER": "رقم", "STRING": "نص بين علامتي تنصيص \"...\"",
    "IDENT": "اسم متغير أو دالة", "_TO": "كلمة 'الى' لتحديد نهاية المدى",
    "_IN": "كلمة 'في' أو 'من' داخل جملة التكرار (لكل)",
}

OP_NAMES_AR = {
    "add": "الجمع (+)", "sub": "الطرح (-)", "mul": "الضرب (*)", "div": "القسمة (/)",
    "floordiv": "القسمة الصحيحة (//)", "mod": "باقي القسمة (%)", "pow_op": "الأس (**)", "compare": "المقارنة",
}

def _build_norm_dict(d):
    return {normalize_ar(k): v for k, v in d.items()}

NORM_BUILTIN_MAP = _build_norm_dict(BUILTIN_MAP)
NORM_BUILTIN_ARITY = _build_norm_dict(BUILTIN_ARITY)
NORM_METHOD_MAP = _build_norm_dict(METHOD_MAP)
NORM_ATTR_MAP = _build_norm_dict(ATTR_MAP)
NORM_KWARG_MAP = _build_norm_dict(KWARG_MAP)

def lookup_norm(exact_dict, norm_dict, key):
    if key in exact_dict:
        return exact_dict[key]
    return norm_dict.get(normalize_ar(key), key)

REVERSE_NAMES_AR = {
    v: k for k, v in {**BUILTIN_MAP, **METHOD_MAP, **ATTR_MAP}.items()
    if "\u0600" <= k[0] <= "\u06FF"
}