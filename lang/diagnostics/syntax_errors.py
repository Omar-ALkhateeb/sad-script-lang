# lang/diagnostics/syntax_errors.py
"""Translates Lark syntax errors into actionable Arabic diagnostics."""

from lark import UnexpectedInput


def explain_syntax_error(exc: UnexpectedInput, source_code: str) -> str:
    lines = source_code.splitlines()
    line_no = max(1, min(getattr(exc, "line", 1), max(1, len(lines))))
    col_no = max(1, getattr(exc, "column", 1))
    line_text = lines[line_no - 1] if lines else ""
    pointer = " " * max(0, col_no - 1) + "^"

    hint = "تأكد من كتابة الجملة البرمجية بشكل صحيح وإغلاق جميع الأقواس وعلامات التنصيص."

    if line_text.count("(") > line_text.count(")"):
        hint = "يبدو أنك نسيت إغلاق القوس الدائري ')' في نهاية السطر."
    elif line_text.count("[") > line_text.count("]"):
        hint = "يبدو أنك نسيت إغلاق قوس القائمة ']'."
    elif line_text.count('"') % 2 == 1 or line_text.count("'") % 2 == 1:
        hint = "يبدو أنك نسيت إغلاق علامة التنصيص للنص."
    elif any(line_text.strip().startswith(k) for k in ("اذا ", "إذا ", "طالما ")) and "=" in line_text and "==" not in line_text and "!=" not in line_text and ">=" not in line_text and "<=" not in line_text:
        hint = "استخدمت علامة الإسناد '=' داخل الشرط بدلاً من '==' للمقارنة."
    elif any(line_text.strip().startswith(k) for k in ("اذا", "إذا", "والا", "لكل", "كرر", "طالما", "دالة", "صنف")) and not line_text.strip().endswith("{"):
        hint = "يبدو أنك نسيت فتح قوس المجموعة '{' في نهاية السطر."

    return (
        f"❌ خطأ في قواعد الكتابة (السطر {line_no}، العمود {col_no}):\n"
        f"    {line_text}\n"
        f"    {pointer}\n"
        f"💡 التشخيص: {hint}"
    )