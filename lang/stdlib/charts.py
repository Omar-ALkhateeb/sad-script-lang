# lang/stdlib/charts.py
"""Charts Standard Library (`استورد رسوم`)."""

import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ..types import RuntimeError

plt.rcParams["font.sans-serif"] = [
    "Geeza Pro", "Arial Unicode MS", "Tahoma", "DejaVu Sans", "sans-serif"
]
plt.rcParams["axes.unicode_minus"] = False

_CHARTS_BUFFER: list[str] = []


def clear_charts():
    _CHARTS_BUFFER.clear()
    plt.close("all")


def get_charts() -> list[str]:
    return list(_CHARTS_BUFFER)


def _extract_values(seq):
    if hasattr(seq, "كقائمة"):
        return seq.كقائمة()
    if hasattr(seq, "_s"):
        return seq._s.tolist()
    if hasattr(seq, "tolist"):
        return seq.tolist()
    return list(seq)


def _finalize_chart():
    fig = plt.gcf()
    if not fig.axes:
        return
    buf = io.StringIO()
    fig.tight_layout()
    fig.savefig(buf, format="svg", bbox_inches="tight", facecolor=fig.get_facecolor())
    svg_str = buf.getvalue()
    idx = svg_str.find("<svg")
    if idx != -1:
        svg_str = svg_str[idx:]
    _CHARTS_BUFFER.append(svg_str)
    plt.close(fig)


def _apply_solarized_theme(ax, fig, title="", xlabel="", ylabel=""):
    fig.patch.set_facecolor("#fdf6e3")
    ax.set_facecolor("#fdf6e3")
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax.spines[spine].set_color("#93a1a1")
    ax.tick_params(colors="#657b83", labelsize=10)
    if title:
        ax.set_title(str(title), fontsize=13, pad=14, color="#586e75", fontweight="bold")
    if xlabel:
        ax.set_xlabel(str(xlabel), fontsize=10, color="#586e75", labelpad=8)
    if ylabel:
        ax.set_ylabel(str(ylabel), fontsize=10, color="#586e75", labelpad=8)


def bar_chart(categories, values, العنوان="الرسم البياني بالأعمدة", المحور_السيني="", المحور_الصادي="", **kwargs):
    title = kwargs.get("title", العنوان)
    xlabel = kwargs.get("xlabel", المحور_السيني)
    ylabel = kwargs.get("ylabel", المحور_الصادي)
    cats = [str(c) for c in _extract_values(categories)]
    vals = _extract_values(values)
    if len(cats) != len(vals):
        raise RuntimeError(
            f"عدد الفئات ({len(cats)}) لا يطابق عدد القيم ({len(vals)}) في رسم الأعمدة."
        )

    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    bars = ax.bar(cats, vals, color="#268bd2", edgecolor="#586e75", linewidth=0.8, width=0.52)
    _apply_solarized_theme(ax, fig, title, xlabel, ylabel)
    ax.grid(axis="y", linestyle="--", color="#eee8d5", linewidth=1.2)
    ax.set_axisbelow(True)
    for bar in bars:
        h = bar.get_height()
        ax.annotate(
            f"{h:g}",
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#586e75",
            fontweight="bold",
        )
    _finalize_chart()


def line_chart(x, y, العنوان="الرسم البياني الخطي", المحور_السيني="", المحور_الصادي="", **kwargs):
    title = kwargs.get("title", العنوان)
    xlabel = kwargs.get("xlabel", المحور_السيني)
    ylabel = kwargs.get("ylabel", المحور_الصادي)
    xs = _extract_values(x)
    ys = _extract_values(y)
    if len(xs) != len(ys):
        raise RuntimeError(
            f"طول المحور السيني ({len(xs)}) لا يطابق طول المحور الصادي ({len(ys)}) في الرسم الخطي."
        )

    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.plot(xs, ys, marker="o", linewidth=2.4, color="#2aa198", markerfacecolor="#268bd2", markersize=6)
    _apply_solarized_theme(ax, fig, title, xlabel, ylabel)
    ax.grid(True, linestyle="--", color="#eee8d5", linewidth=1.2)
    _finalize_chart()


def scatter_chart(x, y, العنوان="مخطط التبعثر", المحور_السيني="", المحور_الصادي="", **kwargs):
    title = kwargs.get("title", العنوان)
    xlabel = kwargs.get("xlabel", المحور_السيني)
    ylabel = kwargs.get("ylabel", المحور_الصادي)
    xs = _extract_values(x)
    ys = _extract_values(y)
    if len(xs) != len(ys):
        raise RuntimeError(
            f"طول المحور السيني ({len(xs)}) لا يطابق طول المحور الصادي ({len(ys)}) في مخطط النقاط."
        )

    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.scatter(xs, ys, color="#cb4b16", s=65, alpha=0.9, edgecolors="#586e75", linewidth=0.8)
    _apply_solarized_theme(ax, fig, title, xlabel, ylabel)
    ax.grid(True, linestyle="--", color="#eee8d5", linewidth=1.2)
    _finalize_chart()


def pie_chart(labels, values, العنوان="الرسم الدائري", **kwargs):
    title = kwargs.get("title", العنوان)
    lbls = [str(l) for l in _extract_values(labels)]
    vals = _extract_values(values)
    if len(lbls) != len(vals):
        raise RuntimeError(
            f"عدد التسميات ({len(lbls)}) لا يطابق عدد القيم ({len(vals)}) في الرسم الدائري."
        )

    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    fig.patch.set_facecolor("#fdf6e3")
    sol_colors = ["#268bd2", "#2aa198", "#859900", "#b58900", "#cb4b16", "#d33682", "#6c71c4"]
    _, _, autotexts = ax.pie(
        vals,
        labels=lbls,
        autopct="%1.1f%%",
        startangle=140,
        colors=sol_colors[: len(vals)],
        textprops={"color": "#586e75", "fontsize": 10},
    )
    for autotext in autotexts:
        autotext.set_color("#fdf6e3")
        autotext.set_fontweight("bold")
    ax.set_title(str(title), fontsize=13, pad=12, color="#586e75", fontweight="bold")
    _finalize_chart()


class ChartsModule:
    """Importable `رسوم` module."""

    __type_name__ = "مكتبة"

    أعمدة = staticmethod(bar_chart)
    اعمدة = staticmethod(bar_chart)
    خط = staticmethod(line_chart)
    نقاط = staticmethod(scatter_chart)
    دائري = staticmethod(pie_chart)