// ide/src/editor/arabicLanguage.ts
import {
  StreamLanguage,
  StringStream,
  syntaxHighlighting,
} from "@codemirror/language";
import { EditorView } from "@codemirror/view";
import { tags, tagHighlighter } from "@lezer/highlight";
import type { Extension } from "@codemirror/state";

const KEYWORDS = new Set([
  "اذا",
  "إذ",
  "إذا",
  "والا_اذا",
  "وإلا_إذا",
  "والا_إذا",
  "والا",
  "وإلا",
  "كرر",
  "مرات",
  "مرة",
  "مره",
  "لكل",
  "من",
  "الى",
  "إلى",
  "في",
  "طالما",
  "دالة",
  "داله",
  "ارجع",
  "أرجع",
  "إرجع",
  "توقف",
  "اكسر",
  "إكسر",
  "استمر",
  "إستمر",
  "اكمل",
  "أكمل",
  "حاول",
  "التقط",
  "إلتقط",
  "امسك",
  "أمسك",
  "و",
  "او",
  "أو",
  "ليس",
  "if",
  "elif",
  "else",
  "repeat",
  "times",
  "for",
  "from",
  "to",
  "in",
  "while",
  "function",
  "def",
  "return",
  "break",
  "continue",
  "try",
  "except",
  "and",
  "or",
  "not",
]);

const BUILTINS = new Set([
  "اطبع",
  "إطبع",
  "ادخل",
  "طول",
  "مجموع",
  "أصغر",
  "اصغر",
  "أكبر",
  "اكبر",
  "قرب",
  "مطلق",
  "نص",
  "عدد_صحيح",
  "عدد_عشري",
  "قائمة",
  "نوع",
  "متوسط",
  "رتب",
  "بدل",
  "عشوائي",
  "اختر_عشوائي",
  "اقرأ_جدول",
  "احفظ_جدول",
  "عمود",
  "صف_بيانات",
  "ارسم_أعمدة",
  "ارسم_اعمدة",
  "ارسم_خط",
  "ارسم_نقاط",
  "ارسم_دائري",
  "باندا",
  "رياضيات",
  "رسم",
  "عشوائيات",
  "جدول_بيانات",
  "سلسلة",
  "أول",
  "اول",
  "آخر",
  "اخر",
  "ملخص",
  "معلومات",
  "حذف_الفارغ",
  "املأ_الفارغ",
  "رتب_قيم",
  "تجميع",
  "استعلم",
  "الأعمدة",
  "الشكل",
  "أضف",
  "اضف",
  "احذف",
  "استبدل",
  "قسم",
]);

const ATOMS = new Set([
  "صحيح",
  "صح",
  "خطأ",
  "خطا",
  "فارغ",
  "لا_شيء",
  "true",
  "True",
  "false",
  "False",
  "None",
  "null",
]);

export const arabicStreamLanguage = StreamLanguage.define({
  token(stream: StringStream): string | null {
    if (stream.eatSpace()) return null;

    if (stream.match("//") || stream.match("#")) {
      stream.skipToEnd();
      return "comment";
    }

    if (stream.match(/^"[^"]*"/) || stream.match(/^'[^']*'/)) {
      return "string";
    }

    if (stream.match(/^[0-9٠-٩]+(\.[0-9٠-٩]+)?/)) {
      return "number";
    }

    if (
      stream.match(/^(==|!=|>=|<=|\+=|-=|\*=|\/=|\/\/|\*\*|[=+\-*/%<>!&|])/)
    ) {
      return "operator";
    }

    if (stream.match(/^[()[\]{}:,،;؛.]/)) {
      return "punctuation";
    }

    if (
      stream.match(
        /^[a-zA-Z_\u0621-\u064A\u0671-\u06D3][a-zA-Z0-9_\u0621-\u064A\u0660-\u0669\u0671-\u06D3]*/,
      )
    ) {
      const word = stream.current();
      if (KEYWORDS.has(word)) return "keyword";
      if (ATOMS.has(word)) return "atom";
      if (BUILTINS.has(word)) return "variableName.standard";
      return "variableName";
    }

    stream.next();
    return null;
  },
});

const arabicTagHighlighter = tagHighlighter([
  { tag: tags.keyword, class: "cm-tok-keyword" },
  { tag: tags.standard(tags.variableName), class: "cm-tok-builtin" },
  { tag: tags.string, class: "cm-tok-string" },
  { tag: tags.number, class: "cm-tok-number" },
  { tag: tags.atom, class: "cm-tok-atom" },
  { tag: tags.comment, class: "cm-tok-comment" },
  { tag: tags.operator, class: "cm-tok-operator" },
  { tag: tags.punctuation, class: "cm-tok-punctuation" },
]);

export const arabicRtlTheme = EditorView.theme(
  {
    "&": {
      height: "100%",
      backgroundColor: "var(--sol-base3)",
      color: "var(--sol-base00)",
      fontFamily: "var(--font-mono)",
    },
    ".cm-scroller": {
      fontFamily: "var(--font-mono)",
      lineHeight: "1.85",
    },
    ".cm-content": {
      direction: "rtl",
      textAlign: "right",
      padding: "10px 0",
      caretColor: "var(--sol-base01)",
    },
    ".cm-line": {
      direction: "rtl",
      textAlign: "right",
      padding: "0 16px",
      unicodeBidi: "isolate",
    },
    ".cm-gutters": {
      backgroundColor: "var(--sol-base2)",
      color: "var(--sol-base1)",
      borderLeft: "1px solid var(--sol-border)",
      borderRight: "none",
      padding: "0 8px",
    },
    ".cm-activeLine": {
      backgroundColor: "rgba(238, 232, 213, 0.55)" /* base2 at 55% */,
    },
    ".cm-activeLineGutter": {
      backgroundColor: "var(--sol-base2)",
      color: "var(--sol-base01)",
      fontWeight: "600",
    },
    ".cm-selectionBackground, ::selection": {
      backgroundColor: "var(--sol-base2) !important",
    },
    // Official Solarized Syntax Colors + RTL BiDi Math Fix
    ".cm-tok-operator": {
      color: "var(--sol-magenta)",
      fontWeight: "700",
      unicodeBidi: "isolate",
    },
    ".cm-tok-operator::before, .cm-tok-operator::after": {
      content: '"\\200F"',
    },
    ".cm-tok-punctuation": { color: "var(--sol-base01)", fontWeight: "600" },
    ".cm-tok-keyword": { color: "var(--sol-green)", fontWeight: "700" },
    ".cm-tok-builtin": { color: "var(--sol-violet)", fontWeight: "600" },
    ".cm-tok-string": { color: "var(--sol-yellow)", unicodeBidi: "isolate" },
    ".cm-tok-number": {
      color: "var(--sol-cyan)",
      fontWeight: "600",
      unicodeBidi: "isolate",
    },
    ".cm-tok-atom": { color: "var(--sol-orange)", fontWeight: "700" },
    ".cm-tok-comment": { color: "var(--sol-base1)", fontStyle: "italic" },
    // Solarized Light Autocomplete Tooltip
    ".cm-tooltip.cm-tooltip-autocomplete": {
      direction: "rtl",
      textAlign: "right",
      backgroundColor: "var(--sol-base3)",
      border: "1px solid var(--sol-border)",
      borderRadius: "6px",
      boxShadow: "0 8px 20px rgba(88, 110, 117, 0.15)",
      fontFamily: "var(--font-sans)",
      overflow: "hidden",
    },
    ".cm-tooltip-autocomplete ul li": {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: "12px",
      padding: "5px 10px",
      color: "var(--sol-base00)",
    },
    ".cm-tooltip-autocomplete ul li[aria-selected]": {
      backgroundColor: "var(--sol-base2)",
      color: "var(--sol-base01)",
      fontWeight: "600",
    },
    ".cm-completionDetail": {
      fontStyle: "normal",
      fontSize: "0.75rem",
      color: "var(--sol-base1)",
    },
  },
  { dark: false },
);

export const arabicLanguageSupport: Extension[] = [
  arabicStreamLanguage,
  syntaxHighlighting(arabicTagHighlighter),
  arabicRtlTheme,
];
