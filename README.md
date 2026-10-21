```text
╭──────────────────────────────────────────────────────────────────────────╮
│   ____            _ ____            _       _                            │
│  / ___|  __ _  __| / ___|  ___ _ __(_)_ __ | |_                          │
│  \___ \ / _` |/ _` \___ \ / __| '__| | '_ \| __|                         │
│   ___) | (_| | (_| |___) | (__| |  | | |_) | |_     ⟦ صـادسكربت ⟧        │
│  |____/ \__,_|\__,_|____/ \___|_|  |_| .__/ \__|    SadScript v1.0.0     │
│                                      |_|                                 │
├──────────────────────────────────────────────────────────────────────────┤
│  An Arabic-First Programming & Data Science Language + WebAssembly IDE   │
╰──────────────────────────────────────────────────────────────────────────╯
```

# ⟦ صادسكربت ⟧ — SadScript

**SadScript (`صادسكربت`)** is a modern, Arabic-first programming language and browser-based IDE designed for algorithms, data analysis (**Pandas**), and data visualization (**Matplotlib**). It transpiles to Python and runs 100% client-side in the browser via **WebAssembly (Pyodide)**.

* **File Extensions:** `.sad`, `.sd`, `.صاد`

---

## ✨ Key Features

* **Forgiving Arabic Syntax:** Supports both Arabic-Indic (`٠-٩`) and ASCII (`0-9`) numerals, Arabic (`،`) and English (`,`) commas, and flexible Hamza/Taa-Marbuta spelling (`اذا` / `إذا`, `دالة` / `داله`).
* **First-Class Data Science:** Built-in Arabic wrappers for **Pandas** DataFrames (`اقرأ_جدول`, `حذف_الفارغ`, `رتب_قيم`) and one-line **Matplotlib** SVG charts (`ارسم_أعمدة`, `ارسم_خط`, `ارسم_دائري`).
* **Smart Diagnostics & Quick-Fix:** Static semantic analysis + runtime inspection that catches errors in Arabic and suggests one-click typo fixes for variable and DataFrame column names.
* **Zero-Setup Browser IDE:** Built with React, TypeScript, Tailwind CSS (Solarized Light theme), CodeMirror 6 (with RTL BiDi operator isolation), and a background Pyodide Web Worker.

---

## ⚡ Quick Examples

### 1. FizzBuzz (`fizzbuzz.sad`)
```text
دالة فيز_باز(الحد) {
    لكل رقم من ١ الى الحد {
        اذا رقم % ٣ == ٠ و رقم % ٥ == ٠ {
            اطبع("فيز باز")
        } والا_اذا رقم % ٣ == ٠ {
            اطبع("فيز")
        } والا_اذا رقم % ٥ == ٠ {
            اطبع("باز")
        } والا {
            اطبع(رقم)
        }
    }
}

فيز_باز(١٥)
```

### 2. Data Analysis & Plotting (`main.sad`)
```text
// 1. Read CSV into a Pandas DataFrame
جدول = اقرأ_جدول("students.csv")

// 2. Compute a new column
جدول["المعدل"] = (جدول["الرياضيات"] + جدول["العلوم"]) / ٢

// 3. Clean, sort, and display top 3 rows
أفضل_الطلاب = جدول.حذف_الفارغ().رتب_قيم(حسب="المعدل"، تصاعدي=خطأ).أول(٣)
اطبع(أفضل_الطلاب)

// 4. Generate an SVG bar chart in one line
جدول.ارسم_أعمدة("الاسم"، "المعدل"، العنوان="معدلات الطلاب النهائية")
```

---

## 📖 Syntax & Built-ins Cheat Sheet

### Control Flow & Keywords
| SadScript (Arabic) | Python Equivalent | Example |
| :--- | :--- | :--- |
| `اذا` / `والا_اذا` / `والا` | `if` / `elif` / `else` | `اذا س > ٥ { ... } والا { ... }` |
| `لكل ... من ... الى ...` | `for i in range(a, b+1)` | `لكل ع من ١ الى ١٠ { ... }` |
| `لكل ... في ...` | `for item in list` | `لكل عنصر في قائمة { ... }` |
| `كرر ... مرات` | `for _ in range(n)` | `كرر ٣ مرات { ... }` |
| `طالما` | `while` | `طالما س > ٠ { ... }` |
| `دالة` / `ارجع` | `def` / `return` | `دالة جمع(أ، ب) { ارجع أ + ب }` |
| `حاول` / `التقط` | `try` / `except` | `حاول { ... } التقط خطأ { ... }` |
| `و` / `او` / `ليس` | `and` / `or` / `not` | `اذا س > ٠ و س < ١٠ { ... }` |
| `صحيح` / `خطأ` / `فارغ` | `True` / `False` / `None` | `نشط = صحيح` |

### Core Built-in Functions
| SadScript Function | Description |
| :--- | :--- |
| `اطبع(قيمة)` | Print values or formatted RTL DataFrames to the console |
| `ادخل(رسالة)` | Read user input (`input()`) |
| `طول(س)` / `مجموع(س)` / `متوسط(س)` | Length (`len`), Sum (`sum`), Mean (`mean`) |
| `أكبر(س)` / `أصغر(س)` / `قرب(س، ن)` | Max (`max`), Min (`min`), Round (`round`) |
| `رتب(قائمة)` / `بدل(قائمة، أ، ب)` | Sort list (`sorted`) / Swap two elements in-place |
| `نص(س)` / `عدد_صحيح(س)` / `عدد_عشري(س)` | Cast to `str`, `int`, `float` |

### Data Science (Pandas & Charts)
| SadScript Method | Equivalent | Description |
| :--- | :--- | :--- |
| `اقرأ_جدول("file.csv")` | `pd.read_csv()` | Load a CSV file into a DataFrame |
| `احفظ_جدول(جدول، "out.csv")` | `df.to_csv()` | Save DataFrame to a CSV file |
| `جدول.أول(ن)` / `جدول.آخر(ن)` | `df.head(n)` / `df.tail(n)` | First or last $n$ rows |
| `جدول.ملخص()` | `df.describe()` | Summary statistics |
| `جدول.حذف_الفارغ()` / `جدول.املأ_الفارغ(٠)` | `df.dropna()` / `df.fillna(0)` | Handle missing values |
| `جدول.رتب_قيم(حسب="...", تصاعدي=خطأ)` | `df.sort_values()` | Sort rows by column |
| `جدول.ارسم_أعمدة(س، ص، العنوان="...")` | `plt.bar()` | Render a bar chart |
| `جدول.ارسم_خط(س، ص، العنوان="...")` | `plt.plot()` | Render a line chart |

---

## 🚀 Quick Start (Local Development)

### Run the Web IDE
```bash
cd ide
npm install
npm run dev
```

### Run via CLI
```bash
python3.10 -m lang.cli fizzbuzz.sad --emit-py
```

---

## 📄 License

Licensed under the **MIT License**.

```text
MIT License

Copyright (c) 2026 Omar Nabeel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```