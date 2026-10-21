"""Friendly Arabic syntax and live-memory runtime error diagnostics."""

import difflib
from lark import UnexpectedCharacters, UnexpectedToken, Tree
from .mappings import (
    ARABIC_DIGITS,
    TYPE_NAMES_AR,
    EXPECTED_TOKENS_AR,
    OP_NAMES_AR,
    REVERSE_NAMES_AR,
)

SYNTAX_ERROR_EXAMPLES = {
    "استخدمت '=' (تعيين قيمة) بدلاً من '==' (المقارنة) داخل جملة الشرط 'اذا'.": [
        "اذا س = ٥ { اطبع(س) }",
        "اذا الاسم = \"أحمد\" { اطبع(الاسم) }",
    ],
    "نسيت إغلاق القوس الدائري ')' في نهاية الأمر.": [
        "اطبع(٥\n",
        "س = مجموع([١, ٢]\n",
    ],
    "نسيت إغلاق قوس المجموعة '}' في نهاية البلوك.": [
        "اذا س > ٥ {\n اطبع(س)\n",
        "كرر ٣ مرات {\n اطبع(١)\n",
    ],
    "نسيت فتح قوس المجموعة '{' بعد جملة الشرط أو التكرار أو الدالة.": [
        "اذا س > ٥\n اطبع(س) }",
        "كرر ٣ مرات\n اطبع(١) }",
    ],
    "نسيت إغلاق القوس المربع ']' في القائمة أو الفهرس.": [
        "ارقام = [١, ٢, ٣\n",
        "اطبع(ارقام[٠)\n",
    ],
    "نسيت وضع قيمة أو تعبير بعد علامة '='.": [
        "س =\n",
    ],
    "في حلقة 'لكل'، يجب كتابة 'من ... الى ...' أو 'في ...' بعد اسم المتغير.": [
        "لكل ع ١ الى ٥ { اطبع(ع) }",
    ],
}

def ar_type(val):
    t_name = val if isinstance(val, str) else type(val).__name__
    return TYPE_NAMES_AR.get(t_name, t_name)

def explain_syntax_error(exc, source_code, parser_instance):
    lines = source_code.splitlines()
    line_num = max(1, min(getattr(exc, "line", 1), len(lines))) if lines else 1
    col_num = max(1, getattr(exc, "column", 1))
    line_text = lines[line_num - 1] if lines else ""
    pointer = " " * (col_num - 1) + "^"

    reason = None
    if isinstance(exc, UnexpectedCharacters):
        if line_text.count('"') % 2 == 1 or line_text.count("'") % 2 == 1:
            reason = "فتحت علامة تنصيص للنص (\" أو ') في هذا السطر لكنك نسيت إغلاقها."
        else:
            bad_char = line_text[col_num - 1] if col_num <= len(line_text) else ""
            reason = f"الرمز '{bad_char}' غير مسموح به في هذا الموضع."

    if not reason:
        try:
            reason = exc.match_examples(parser_instance.parse, SYNTAX_ERROR_EXAMPLES, use_accepts=True)
        except Exception:
            reason = None

    if not reason and isinstance(exc, UnexpectedToken):
        expected_ar = [
            EXPECTED_TOKENS_AR[tok]
            for tok in getattr(exc, "expected", [])
            if tok in EXPECTED_TOKENS_AR
        ]
        unexpected_val = "نهاية الكود" if str(exc.token) == "$END" else str(exc.token)
        if expected_ar:
            unique_expected = list(dict.fromkeys(expected_ar))[:3]
            reason = f"توقف المترجم عند '{unexpected_val}' لأنه كان يتوقع رؤية: {' أو '.join(unique_expected)}."

    if not reason:
        reason = "تركيب الجملة غير مكتمل في هذا السطر. راجع الأقواس وعلامات الترقيم."

    return (
        f"❌ خطأ في قواعد الكتابة (السطر {line_num}، العمود {col_num}):\n"
        f"    {line_text}\n"
        f"    {pointer}\n"
        f"💡 التشخيص: {reason}"
    )

def _find_nodes_on_line(tree, target_line):
    matches = []
    if isinstance(tree, Tree):
        if getattr(tree.meta, "line", None) == target_line:
            matches.append(tree)
        for child in tree.children:
            matches.extend(_find_nodes_on_line(child, target_line))
    return matches

def _eval_simple_node(node, env):
    if not isinstance(node, Tree):
        return None, False
    if node.data == "var":
        name = str(node.children[0])
        if name in env:
            return env[name], True
    elif node.data == "number":
        return float(str(node.children[0]).translate(ARABIC_DIGITS)), True
    elif node.data == "string":
        return str(node.children[0]).strip("\"'"), True
    return None, False

def _inspect_index_error(nodes_on_line, env):
    for node in nodes_on_line:
        if node.data == "index_access":
            container_node, index_node = node.children[0], node.children[1]
            container_val, ok_c = _eval_simple_node(container_node, env)
            index_val, ok_i = _eval_simple_node(index_node, env)
            if ok_c and hasattr(container_val, "__len__"):
                length = len(container_val)
                var_label = f"'{container_node.children[0]}'" if container_node.data == "var" else "القائمة"
                if length == 0:
                    return f"{var_label} فارغة تماماً (طولها ٠)، لذلك لا يمكن الوصول إلى أي عنصر بداخلها."
                idx_str = f" رقم {int(index_val)}" if ok_i and isinstance(index_val, (int, float)) else ""
                return (
                    f"{var_label} تحتوي على {length} عناصر فقط (الأرقام المسموحة من ٠ إلى {length - 1})، "
                    f"لكنك طلبت العنصر{idx_str} وهو خارج الحدود."
                )
    return "حاولت الوصول إلى عنصر برقم فهرس خارج حدود القائمة (تذكر أن الترقيم يبدأ من ٠)."

def _inspect_key_error(exc, nodes_on_line, env):
    missing_key = exc.args[0] if exc.args else ""
    for node in nodes_on_line:
        if node.data in ("index_access", "func_call"):
            container_val, ok_c = _eval_simple_node(node.children[0], env)
            if ok_c:
                if hasattr(container_val, "columns"):
                    cols = [str(c) for c in container_val.columns]
                    close = difflib.get_close_matches(str(missing_key), cols, n=1, cutoff=0.5)
                    hint = f" هل تقصد '{close[0]}'؟" if close else ""
                    return f"العمود '{missing_key}' غير موجود في جدول البيانات.{hint}\n   📌 الأعمدة الموجودة: {cols}"
                if isinstance(container_val, dict):
                    keys = [str(k) for k in container_val.keys()]
                    close = difflib.get_close_matches(str(missing_key), keys, n=1, cutoff=0.5)
                    hint = f" هل تقصد '{close[0]}'؟" if close else ""
                    return f"المفتاح '{missing_key}' غير موجود في القاموس.{hint}\n   📌 المفاتيح الموجودة: {keys}"
    return f"العمود أو المفتاح '{missing_key}' غير موجود داخل الجدول أو القاموس."

def _inspect_type_error(nodes_on_line, env):
    for node in nodes_on_line:
        if node.data in OP_NAMES_AR:
            left_val, ok_l = _eval_simple_node(node.children[0], env)
            right_val, ok_r = _eval_simple_node(node.children[-1], env)
            if ok_l and ok_r:
                return (
                    f"لا يمكن تنفيذ عملية {OP_NAMES_AR[node.data]} بين ({ar_type(left_val)}) و ({ar_type(right_val)}). "
                    f"تأكد من أن الطرفين من نفس النوع أو استخدم دالة تحويل مثل عدد_صحيح() أو نص()."
                )
        if node.data == "func_call":
            fn_name = str(node.children[0])
            if fn_name in env and not callable(env[fn_name]):
                val = env[fn_name]
                hint = " هل تقصد استخدام الأقواس المربعة [ ] للوصول إلى عنصر؟" if isinstance(val, (list, dict)) else ""
                return f"المتغير '{fn_name}' هو ({ar_type(val)}) وليس دالة، لذلك لا يمكنك وضع أقواس ( ) بعده.{hint}"
    return "نوع البيانات الذي مررته للدالة أو العملية غير متوافق معها."

def explain_runtime_error(exc, student_line, source_code, parse_tree, live_env):
    lines = source_code.splitlines()
    if type(exc).__name__ == "EduInfiniteLoopError":
        student_line = getattr(exc, "line_no", student_line)

    line_text = lines[student_line - 1].strip() if 0 < student_line <= len(lines) else ""
    nodes_on_line = _find_nodes_on_line(parse_tree, student_line)

    tb_frames = []
    tb = exc.__traceback__
    while tb is not None:
        if tb.tb_frame.f_code.co_filename == "<student_code>":
            tb_frames.append(tb.tb_frame)
        tb = tb.tb_next
    active_env = {**live_env, **(tb_frames[-1].f_locals if tb_frames else {})}

    if type(exc).__name__ == "EduInfiniteLoopError":
        explanation = (
            f"تم إيقاف البرنامج تلقائياً لأن الحلقة في السطر {student_line} تكررت أكثر من الحد المسموح "
            f"({getattr(exc, 'max_steps', 100000)} مرة). تأكد من أن شرط التوقف داخل الحلقة يتحقق!"
        )
    elif isinstance(exc, RecursionError):
        explanation = "استدعت الدالة نفسها بشكل متكرر بلا نهاية. تأكد من وجود شرط توقف (اذا ...) داخل الدالة!"
    elif isinstance(exc, ZeroDivisionError):
        explanation = "قمت بالقسمة على صفر في هذا السطر، وهو غير معرف رياضياً."
    elif isinstance(exc, IndexError):
        explanation = _inspect_index_error(nodes_on_line, active_env)
    elif isinstance(exc, KeyError):
        explanation = _inspect_key_error(exc, nodes_on_line, active_env)
    elif isinstance(exc, NameError):
        raw_name = getattr(exc, "name", "")
        ar_name = REVERSE_NAMES_AR.get(raw_name, raw_name)
        candidates = [k for k in active_env.keys() if not k.startswith("_")]
        close = difflib.get_close_matches(ar_name, candidates, n=1, cutoff=0.6)
        hint = f" هل تقصد '{close[0]}'؟" if close else ""
        explanation = f"المتغير أو الدالة '{ar_name}' غير معرّف.{hint}"
    elif isinstance(exc, AttributeError):
        obj = getattr(exc, "obj", None)
        raw_attr = getattr(exc, "name", "")
        ar_attr = REVERSE_NAMES_AR.get(raw_attr, raw_attr)
        explanation = f"المتغير من نوع ({ar_type(obj)}) لا يمتلك دالة أو خاصية باسم '{ar_attr}'."
    elif isinstance(exc, FileNotFoundError):
        explanation = f"الملف '{exc.filename}' غير موجود. تأكد من كتابة اسم الملف والامتداد (.csv) بشكل صحيح."
    elif isinstance(exc, TypeError):
        explanation = _inspect_type_error(nodes_on_line, active_env)
    elif isinstance(exc, ValueError):
        msg = str(exc)
        if "EMPTY_AVERAGE" in msg:
            explanation = "لا يمكن حساب المتوسط لقائمة فارغة لا تحتوي على أي أرقام."
        elif "EMPTY_CHOICE" in msg:
            explanation = "لا يمكن الاختيار عشوائياً من قائمة فارغة."
        else:
            explanation = "القيمة المدخلة غير صالحة للتحويل."
    else:
        explanation = f"حدث خطأ غير متوقع أثناء تنفيذ هذا السطر ({type(exc).__name__}: {exc})."

    return (
        f"❌ خطأ أثناء التشغيل (السطر {student_line}):\n"
        f"    {line_text}\n"
        f"💡 التشخيص: {explanation}"
    )