"""Command-line interface for running .edu files."""

import sys
from pathlib import Path
from . import execute_educational_code

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m arabicode.cli <file.edu> [--emit-py]")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"❌ الملف '{input_file}' غير موجود.")
        sys.exit(1)

    source = input_file.read_text(encoding="utf-8")
    res = execute_educational_code(source)

    if "--emit-py" in sys.argv and res["python_code"]:
        out_py = input_file.with_suffix(".py")
        out_py.write_text(res["python_code"], encoding="utf-8")
        print(f"✅ تم حفظ كود بايثون المترجم في: {out_py}")

    if res["stdout"]:
        print(res["stdout"], end="")

    if not res["ok"]:
        print("\n" + res["error"])
        sys.exit(1)
    elif res["charts"]:
        for idx, svg in enumerate(res["charts"], 1):
            chart_path = input_file.with_name(f"{input_file.stem}_chart_{idx}.svg")
            chart_path.write_text(svg, encoding="utf-8")
            print(f"📊 تم حفظ الرسم البياني في: {chart_path}")

if __name__ == "__main__":
    main()