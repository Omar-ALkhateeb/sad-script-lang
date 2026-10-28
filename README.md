# ⟦ صـادسكربت ⟧ — SadScript

```text
  ╭───────────────────────────────────────────────────────────────────────╮
  │     ____            _ ____            _       _                       │
  │    / ___|  __ _  __| / ___|  ___ _ __(_)_ __ | |_    ⟦ صـادسكربت ⟧    │
  │    \___ \ / _` |/ _` \___ \ / __| '__| | '_ \| __|   SadScript v1.0   │
  │     ___) | (_| | (_| |___) | (__| |  | | |_) | |_    .sad  •  .sd     │
  │    |____/ \__,_|\__,_|____/ \___|_|  |_| .__/ \__|                    │
  │                                        |_|                            │
  ╰───────────────────────────────────────────────────────────────────────╯
```

**SadScript (صادسكربت)** is an Arabic-first programming language and browser-based data science workbench (`.sad`). Designed with a zero-underscore, single-word Arabic vocabulary, it combines clean object-oriented and procedural syntax with native tabular data (`جدول`), vector columns (`عمود`), and Solarized Light SVG visualization (`رسوم`) running 100% client-side in WebAssembly.

---

## Key Features

- **Zero-Underscore Single-Word Vocabulary:** Uses concise, natural Arabic roots (`عدد` for `int`, `كسر` for `float`, `نص` for `str`, `منطق` for `bool`, `جدول` for `table`, and space-separated `والا اذا` for `elif`) so developers never have to reach for underscores on an Arabic keyboard.
- **First-Class Tabular Data & Charts:** Read CSVs (`اقرأ`), clean missing rows (`نظف`), filter (`صفي`), group (`تجميع`), sort (`رتب`), and plot responsive SVG charts (`أعمدة`, `خط`, `نقاط`, `دائري`) in one line without exposing underlying Python/Pandas internals.
- **Native String Interpolation & Dot-Access Dictionaries:** Embed variables directly inside strings (`"المعدل: {معدل}"`) and access dictionary keys via dot notation (`طالب.الاسم` or `طالب["الاسم"]`).
- **Object-Oriented Classes with Auto-`هذا`:** Define classes (`صنف`) and constructors (`انشئ`) where `هذا` (`self`) is bound automatically without boilerplate parameter declarations.
- **Zero-Install WebAssembly IDE:** Features a Solarized Light VS Code-style workbench with RTL BiDi operator isolation, dot-aware IntelliSense, virtual file/folder tree, interactive CSV editor, live variable inspector, and 1-click auto-fix diagnostics.

---

## Quick Examples

### 1. Data Science & Visualization in 6 Lines

```text
// Load CSV into a native Table (جدول)
طلاب = اقرأ("students.csv")

// Vectorized column arithmetic (supports Eastern ٠-٩ and Western 0-9 digits)
طلاب["المعدل"] = (طلاب["الرياضيات"] + طلاب["العلوم"]) / ٢

// Clean missing rows, sort descending, and take top 3
متفوقون = طلاب.نظف().رتب("المعدل"، تصاعدي=خطأ).أول(٣)
اطبع(متفوقون)

// String interpolation with {variable}
معدل = قرب(متوسط(طلاب["المعدل"])، ٢)
اطبع("المعدل العام للصف: {معدل}")

// Render a Solarized Light SVG bar chart
طلاب.أعمدة("الاسم"، "المعدل"، العنوان="معدلات الطلاب النهائية")
```

### 2. Control Flow (`اذا` / `والا اذا` / `والا` & Loops)

```text
لكل ن من ١ الى ١٥ {
    اذا ن % ١٥ == ٠ {
        اطبع("فيز باز (FizzBuzz)")
    } والا اذا ن % ٣ == ٠ {
        اطبع("فيز (Fizz)")
    } والا اذا ن % ٥ == ٠ {
        اطبع("باز (Buzz)")
    } والا {
        اطبع(ن)
    }
}
```

### 3. Classes (`صنف`) & Standard Library Modules (`استورد`)

```text
استورد رياضيات
استورد عشوائيات

صنف دائرة {
    دالة انشئ(نق) {
        هذا.نق = نق
    }

    دالة مساحة() {
        ارجع قرب(رياضيات.ط * رياضيات.قوة(هذا.نق، ٢)، ٢)
    }
}

د = دائرة(٥)
اطبع("مساحة الدائرة = {د.مساحة()} (النوع: {نوع(د.مساحة())})")
اطبع("رقم عشوائي: {عشوائيات.عدد(١، ١٠٠)}")
```

### 4. Multi-File Imports & Dictionaries with Dot-Access

```text
// Import another .sad file from the workspace or fetch JSON over HTTP
من "أدوات.sad" استورد دائرة
استورد طلبات

طالب = {"الاسم": "سارة"، "الدرجة": ٩٨}
اطبع("الطالبة {طالب.الاسم} حصلت على {طالب.الدرجة}")
```

---

## Complete Language Reference

### 1. Core Types (Single-Word Primitives)

| Type Name              | Equivalent             | Constructor / Conversion         | Literal Examples                 |
| :--------------------- | :--------------------- | :------------------------------- | :------------------------------- |
| **`عدد`**              | Integer (`int`)        | `عدد("٤٢")`                      | `٤٢`, `100`, `-٥`                |
| **`كسر`**              | Float (`float`)        | `كسر("٣.١٤")`                    | `٣.١٤`, `95.5`                   |
| **`نص`**               | String (`str`)         | `نص(١٠٠)`                        | `"مرحباً {الاسم}"`               |
| **`منطق`**             | Boolean (`bool`)       | `منطق(١)`                        | `صح` (`صحيح`), `خطأ`             |
| **`قائمة`**            | List (`list`)          | `قائمة()`                        | `[١٠، ٢٠، ٣٠]`                   |
| **`قاموس`**            | Dictionary (`dict`)    | `قاموس()`                        | `{"الاسم": "أحمد"، "العمر": ٢٠}` |
| **`جدول`**             | Data Table (`Table`)   | `جدول(بيانات)` / `اقرأ("f.csv")` | Tabular dataset                  |
| **`عمود`**             | Data Column (`Column`) | `عمود([١، ٢، ٣])`                | `طلاب["الرياضيات"]`              |
| **`فارغ`** / **`عدم`** | Null (`None`)          | —                                | `فارغ` / `عدم`                   |

Use **`نوع(قيمة)`** to inspect the runtime type of any value.

---

### 2. Operators & Punctuation

- **Punctuation:** Both Arabic comma (`،`) and English comma (`,`) are valid everywhere. Both Eastern Arabic numerals (`٠١٢٣٤٥٦٧٨٩`) and Western numerals (`0123456789`) are supported natively.
- **Arithmetic:** `+`, `-`, `*`, `/`, `//` (integer division), `%` (modulo), `**` (exponent), `+=`, `-=`, `*=`, `/=`.
- **Comparison:** `==`, `!=`, `>`, `<`, `>=`, `<=`.
- **Logical & Membership:** `و` (`and`), `او` / `أو` (`or`), `ليس` (`not`), `في` (`in`), `ليس في` (`not in`).
- **Comments:** Single-line comments start with `//` or `#`.

---

### 3. Control Flow & Error Handling

| Construct         | Syntax                                               | Description                                                        |
| :---------------- | :--------------------------------------------------- | :----------------------------------------------------------------- |
| **Conditional**   | `اذا شرط { ... } والا اذا شرط٢ { ... } والا { ... }` | Conditional branching (no underscore needed in `والا اذا`)         |
| **Range Loop**    | `لكل ع من ١ الى ١٠ { ... }`                          | Inclusive range loop (`1` through `10` inclusive)                  |
| **For-Each Loop** | `لكل عنصر في قائمة { ... }`                          | Iterates over any list, column, or string                          |
| **Index Loop**    | `لكل ع في فهارس(قائمة) { ... }`                      | Iterates from `0` to `طول(قائمة) - 1`                              |
| **Repeat Loop**   | `كرر ٥ مرات { ... }`                                 | Repeats a block $N$ times                                          |
| **While Loop**    | `طالما شرط { ... }`                                  | Loops while condition is true (with automatic infinite-loop guard) |
| **Loop Control**  | `توقف` / `استمر`                                     | `break` / `continue` inside loops                                  |
| **Try / Catch**   | `حاول { ... } التقط خطأ { اطبع(خطأ) }`               | Catches runtime errors into variable `خطأ`                         |

---

### 4. Functions (`دالة`) & Classes (`صنف`)

- **Functions:** Variables assigned inside a function are local by default (lexical scoping). Use `عام س` (`global`) to mutate a module-level variable.

```text
دالة مربع(س) {
    ارجع س * س
}
```

- **Classes:** Define classes with `صنف`. The constructor is named `انشئ` (or `بناء`), and `هذا` refers to the current instance (`self` is injected automatically into all methods).

```text
صنف مستطيل {
    دالة انشئ(طول، عرض) {
        هذا.طول = طول
        هذا.عرض = عرض
    }
    دالة مساحة() {
        ارجع هذا.طول * هذا.عرض
    }
}
```

---

### 5. Built-in Collection Methods (`قائمة`, `قاموس`, `نص`)

#### List (`قائمة`)

- `ق.أضف(عنصر)` — Appends an item and returns the list (chainable).
- `ق.أدرج(فهرس، عنصر)` — Inserts an item at index.
- `ق.احذف(عنصر)` — Removes the first matching value.
- `ق.اسحب(فهرس=-١)` — Pops and returns the item at index.
- `ق.رتب(تصاعدي=صح)` — Returns a new sorted `قائمة`.
- `ق.اعكس()` — Returns a new reversed `قائمة`.
- `ق.أول(ن)` / `ق.آخر(ن)` — Returns the first/last element (or first/last $N$ elements if $N$ is given).
- `ق.اربط("، ")` — Joins elements into a `نص`.
- `ق.يضم(عنصر)` / `ق.عدد(عنصر)` / `ق.طول` — Membership check, count, and length.

#### Dictionary (`قاموس`)

- Supports both bracket access (`ق["مفتاح"]`) and dot access (`ق.مفتاح`).
- `ق.احصل(مفتاح، افتراضي)` — Safe lookup with default value.
- `ق.مفاتيح()` / `ق.قيم()` / `ق.عناصر()` — Returns keys, values, or `[key, value]` pairs as a `قائمة`.
- `ق.احذف(مفتاح)` / `ق.يضم(مفتاح)` / `ق.طول` — Deletes key, checks existence, or returns count.

#### String (`نص`)

- Supports `{متغير}` string interpolation automatically.
- `ن.قسم(فاصل)` — Splits string into a `قائمة` of strings.
- `ن.استبدل(قديم، جديد)` — Replaces substrings.
- `ن.نظف()` — Strips leading and trailing whitespace.
- `ن.يبدأ(بادئة)` / `ن.ينتهي(لاحقة)` / `ن.يضم(جزء)` / `ن.موقع(جزء)` — String search helpers.
- `ن.كبير()` / `ن.صغير()` / `ن.حرف(٠)` / `ن.طول` — Case conversion, character indexing, and length.

---

### 6. Data Science Engine (`جدول` & `عمود`)

| Method / Property                                                      | Description                                                               |
| :--------------------------------------------------------------------- | :------------------------------------------------------------------------ |
| `اقرأ("file.csv")` / `جداول.اقرأ("file.csv")`                          | Loads a CSV file into a `جدول`                                            |
| `جدول.احفظ("out.csv")`                                                 | Exports the table to a CSV file                                           |
| `جدول["العمود"]`                                                       | Returns a vectorized `عمود` supporting `+`, `-`, `*`, `/`, `>`, `<`, `==` |
| `جدول.نظف()`                                                           | Drops rows containing missing values (`dropna`)                           |
| `جدول.املأ(٠)`                                                         | Replaces missing values with a fallback value (`fillna`)                  |
| `جدول.رتب("العمود"، تصاعدي=خطأ)`                                       | Sorts rows by column                                                      |
| `جدول.صفي(جدول["العمود"] >= ٨٥)`                                       | Filters rows matching a boolean condition                                 |
| `جدول.تجميع("العمود").متوسط()`                                         | Groups by column and aggregates (`متوسط`, `مجموع`, `عدد`, `أكبر`, `أصغر`) |
| `جدول.أول(٥)` / `جدول.آخر(٥)`                                          | Returns the first or last $N$ rows                                        |
| `جدول.ملخص()`                                                          | Generates summary statistics for numerical columns                        |
| `جدول.صف(٠)`                                                           | Returns row $i$ as a `قاموس`                                              |
| `جدول.الأعمدة` / `جدول.الشكل` / `جدول.صفوف`                            | Column names list, `[rows, cols]` shape, and row count                    |
| `عمود.متوسط()` / `مجموع()` / `أكبر()` / `أصغر()` / `وسيط()` / `فريد()` | Column aggregations                                                       |

---

### 7. Charts Engine (`رسوم`) & Standard Library Modules (`استورد`)

Charts can be called directly as global functions, as methods on any `جدول`, or via `استورد رسوم`:

```text
// Direct method on a Table:
طلاب.أعمدة("الاسم"، "المعدل"، العنوان="نتائج الطلاب")

// Or via the رسوم module:
استورد رسوم
رسوم.أعمدة(فئات، قيم، العنوان="رسم أعمدة")
رسوم.خط(س، ص، العنوان="رسم خطي")
رسوم.نقاط(س، ص، العنوان="مخطط تبعثر")
رسوم.دائري(تسميات، قيم، العنوان="رسم دائري")
```

#### Built-in Modules (`استورد`)

- **`استورد رياضيات`** — `ط` ($\pi$), `هـ` ($e$), `جذر(س)`, `قوة(أ، ب)`, `مطلق(س)`, `سقف(س)`, `أرضية(س)`, `جا(ز)`, `جتا(ز)`, `ظا(ز)`, `لوغاريتم(س)`.
- **`استورد عشوائيات`** — `عدد(من، إلى)`, `كسر(من، إلى)`, `اختر(قائمة)`, `اخلط(قائمة)`, `عينة(قائمة، ك)`.
- **`استورد طلبات`** — `احصل(الرابط)` (returns `استجابة` with `.الحالة`, `.النص`, `.كقاموس()`), `جلب(الرابط)` (fetches JSON directly into a `قاموس` or `قائمة`).
- **`استورد جداول`** — `اقرأ(ملف)`, `احفظ(جدول، ملف)`, `أنشئ(بيانات)`, `عمود(قيم)`.
- **Multi-File Imports:** `استورد "ملف_آخر.sad"` or `من "ملف_آخر.sad" استورد دالة_مساعدة`.

---

## Project Architecture

```text
├── lang/                   # Modular Compiler & Runtime Package
│   ├── compiler/           # LALR(1) grammar.lark, lexical scopes, checker, emitter, sourcemap
│   ├── types/              # Core types: Type, String (نص), List (قائمة), Dict (قاموس)
│   ├── stdlib/             # Standard library: builtins, tables, charts, math, random, http
│   ├── runtime/            # Sandboxed runner, loop guards, multi-file module loader
│   ├── diagnostics/        # Arabic syntax & runtime error diagnostics with typo suggestions
│   └── cli.py              # Command-line runner for .sad files
└── ide/                    # React + TypeScript + CodeMirror 6 + Pyodide WebAssembly IDE
```

---

## Running Locally

### 1. Run the Browser IDE

```bash
cd ide
npm install
npm run dev
```

### 2. Run `.sad` Files from the Terminal (CLI)

```bash
python3.10 -m lang.cli path/to/script.sad
```

---

## License

MIT License — Copyright © 2026 Omar Nabeel.
