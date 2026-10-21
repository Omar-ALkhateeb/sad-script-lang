"""Standard Library and Runtime Guards for ArabiCode."""

import io
import sys
import time
import math
import random
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Headless renderer safe for both Terminal and Browser (Pyodide)
import matplotlib.pyplot as plt

# Keep SVG text as real DOM text so the browser renders connected RTL Arabic fonts natively
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.sans-serif"] = ["Tahoma", "Segoe UI", "Arial", "DejaVu Sans"]

# ==========================================
# 1. ARABIC MODULE ALIASES
# ==========================================
باندا = pd
رياضيات = math
رسم = plt
عشوائيات = random

# ==========================================
# 2. INFINITE LOOP GUARD (Browser & CLI Safety)
# ==========================================
class EduInfiniteLoopError(Exception):
    def __init__(self, line_no, max_steps):
        self.line_no = line_no
        self.max_steps = max_steps
        super().__init__(f"INFINITE_LOOP:{line_no}")

_STEP_COUNT = 0
_START_TIME = 0.0
MAX_LOOP_STEPS = 100_000
MAX_EXEC_SECONDS = 3.5

def reset_execution_limits():
    """Resets step and time counters before each student code run."""
    global _STEP_COUNT, _START_TIME
    _STEP_COUNT = 0
    _START_TIME = time.perf_counter()

def _edu_tick(line_no):
    """Automatically injected into every loop body by transpiler.py."""
    global _STEP_COUNT
    _STEP_COUNT += 1
    if _STEP_COUNT > MAX_LOOP_STEPS:
        raise EduInfiniteLoopError(line_no, MAX_LOOP_STEPS)
    if (_STEP_COUNT & 0x3FF) == 0:  # Check elapsed time every 1,024 iterations for speed
        if (time.perf_counter() - _START_TIME) > MAX_EXEC_SECONDS:
            raise EduInfiniteLoopError(line_no, _STEP_COUNT)

# ==========================================
# 3. CHART SVG BUFFER
# ==========================================
_GENERATED_CHARTS = []

def clear_charts():
    """Clears stored SVG charts before a new run."""
    _GENERATED_CHARTS.clear()

def get_charts():
    """Returns all SVG chart strings generated during the current run."""
    return list(_GENERATED_CHARTS)

def _finalize_chart():
    """Saves the active Matplotlib figure as an SVG string in memory."""
    buf = io.StringIO()
    plt.savefig(buf, format="svg", bbox_inches="tight")
    plt.close()
    _GENERATED_CHARTS.append(buf.getvalue())

# ==========================================
# 4. BEGINNER-SAFE OPERATORS & INPUT
# ==========================================
def _format_rtl_dataframe(df):
    """Formats a Pandas DataFrame with RTL Unicode isolation (\u200F) so columns never flip."""
    RLM = "\u200F"
    df_head = df.head(50)
    cols = [str(c) for c in df_head.columns]
    rows = [[str(cell) for cell in row] for row in df_head.values.tolist()]

    widths = []
    for idx, col in enumerate(cols):
        col_cells = [r[idx] for r in rows] if rows else []
        widths.append(max([len(col)] + [len(c) for c in col_cells]) + 2)

    header = f"{RLM} │ {RLM}".join(c.center(widths[i]) for i, c in enumerate(cols))
    sep = "─┼─".join("─" * w for w in widths)
    body_lines = []
    for r in rows:
        line = f"{RLM} │ {RLM}".join(r[i].center(widths[i]) for i in range(len(cols)))
        body_lines.append(f"{RLM}{line}{RLM}")

    return f"{RLM}{header}{RLM}\n{RLM}{sep}{RLM}\n" + "\n".join(body_lines)

def edu_print(*args):
    """RTL-aware print that formats Pandas DataFrames so columns align under Arabic headers."""
    formatted = []
    for a in args:
        if isinstance(a, pd.DataFrame):
            formatted.append(_format_rtl_dataframe(a))
        else:
            formatted.append(str(a))
    print(" ".join(formatted))

def edu_add(a, b):
    """Allows concatenating strings and numbers ('النتيجة: ' + 5) while keeping math & Pandas intact."""
    if isinstance(a, str) or isinstance(b, str):
        return f"{a}{b}"
    return a + b

def edu_range(start, end):
    """Inclusive range that automatically counts UP or DOWN based on start and end."""
    s, e = int(start), int(end)
    return range(s, e + 1, 1) if s <= e else range(s, e - 1, -1)

def edu_input(prompt=""):
    """Dual-mode input: uses browser prompt in Pyodide or stdin in terminal, auto-parsing numbers."""
    if "pyodide" in sys.modules:
        import js
        raw = js.prompt(str(prompt))
        if raw is None:
            raw = ""
    else:
        raw = input(str(prompt))

    AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    normalized = str(raw).strip().translate(AR_DIGITS)
    try:
        return int(normalized)
    except ValueError:
        try:
            return float(normalized)
        except ValueError:
            return str(raw)

# ==========================================
# 5. MATH, RANDOM, ARRAY & CSV HELPERS
# ==========================================
def edu_average(iterable):
    if hasattr(iterable, "mean"):
        return float(iterable.mean())
    data = list(iterable)
    if len(data) == 0:
        raise ValueError("EMPTY_AVERAGE")
    return sum(data) / len(data)

def edu_sort(iterable, ascending=True):
    if hasattr(iterable, "sort_values"):
        return iterable.sort_values(ascending=ascending)
    return sorted(iterable, reverse=not ascending)

def edu_swap(arr, i, j):
    idx1, idx2 = int(i), int(j)
    arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr

def edu_random_int(min_val, max_val):
    return random.randint(int(min_val), int(max_val))

def edu_random_choice(seq):
    data = list(seq)
    if len(data) == 0:
        raise ValueError("EMPTY_CHOICE")
    return random.choice(data)

def edu_load_csv(filepath, **kwargs):
    return pd.read_csv(filepath, **kwargs)

def edu_save_csv(df, filepath, index=False):
    df.to_csv(filepath, index=index, encoding="utf-8-sig")

def edu_column(df, col_name):
    if col_name not in df.columns:
        raise KeyError(col_name)
    return df[col_name]

def edu_filter(df, query_str):
    return df.query(query_str)

# ==========================================
# 6. ONE-LINE CHARTING HELPERS
# ==========================================
def edu_bar_chart(categories, values, title="الرسم البياني بالأعمدة", xlabel="", ylabel=""):
    plt.figure(figsize=(6.5, 4))
    plt.bar([str(c) for c in categories], values, color="#2563eb", edgecolor="#1e40af")
    plt.title(title, fontsize=13, pad=12)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    _finalize_chart()

def edu_line_chart(x, y, title="الرسم البياني الخطي", xlabel="", ylabel=""):
    plt.figure(figsize=(6.5, 4))
    plt.plot(x, y, marker="o", linewidth=2.5, color="#16a34a")
    plt.title(title, fontsize=13, pad=12)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.grid(True, linestyle="--", alpha=0.4)
    _finalize_chart()

def edu_scatter_chart(x, y, title="مخطط التبعثر", xlabel="", ylabel=""):
    plt.figure(figsize=(6.5, 4))
    plt.scatter(x, y, color="#dc2626", s=65, alpha=0.85)
    plt.title(title, fontsize=13, pad=12)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.grid(True, linestyle="--", alpha=0.4)
    _finalize_chart()

def edu_pie_chart(labels, values, title="الرسم الدائري"):
    plt.figure(figsize=(6, 4.5))
    plt.pie(values, labels=[str(l) for l in labels], autopct="%1.1f%%", startangle=140)
    plt.title(title, fontsize=13, pad=12)
    _finalize_chart()

# ==========================================
# 7. MONKEY-PATCHED DATAFRAME SHORTCUTS
# ==========================================
def _df_bar_chart(self, x_col, y_col, title="الرسم البياني"):
    edu_bar_chart(self[x_col], self[y_col], title=title, xlabel=x_col, ylabel=y_col)

def _df_line_chart(self, x_col, y_col, title="الرسم الخطي"):
    edu_line_chart(self[x_col], self[y_col], title=title, xlabel=x_col, ylabel=y_col)

pd.DataFrame.ارسم_أعمدة = _df_bar_chart
pd.DataFrame.ارسم_اعمدة = _df_bar_chart
pd.DataFrame.draw_bar = _df_bar_chart
pd.DataFrame.ارسم_خط = _df_line_chart
pd.DataFrame.draw_line = _df_line_chart