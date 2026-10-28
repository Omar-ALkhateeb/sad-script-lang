# lang/compiler/sourcemap.py
"""Maps compiled target line numbers back to original .sad source lines."""

import re

LINE_MARKER = "#__LINE__:"


def tag_line(code_line: str, line_no: int) -> str:
    return f"{code_line}  {LINE_MARKER}{line_no}"


def extract_source_line(compiled_lineno: int, compiled_code: str) -> int:
    lines = compiled_code.splitlines()
    if not lines:
        return 1
    idx = min(max(0, compiled_lineno - 1), len(lines) - 1)
    for i in range(idx, -1, -1):
        match = re.search(rf"{LINE_MARKER}(\d+)", lines[i])
        if match:
            return int(match.group(1))
    return 1