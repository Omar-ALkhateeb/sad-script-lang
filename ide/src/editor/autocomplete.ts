// ide/src/editor/autocomplete.ts
import {
  autocompletion,
  type Completion,
  CompletionContext,
  type CompletionResult,
  snippetCompletion,
} from "@codemirror/autocomplete";
import { type Extension } from "@codemirror/state";

function normalizeAr(str: string): string {
  return str
    .replace(/[أإآ]/g, "ا")
    .replace(/ة/g, "ه")
    .replace(/ى/g, "ي")
    .replace(/ـ/g, "");
}

const KEYWORD_COMPLETIONS: Completion[] = [
  snippetCompletion("اذا ${شرط} {\n\t${}\n}", {
    label: "اذا ... { }",
    detail: "جملة شرطية (if)",
    type: "keyword",
    boost: 9,
  }),
  snippetCompletion("اذا ${شرط} {\n\t${}\n} والا {\n\t\n}", {
    label: "اذا ... والا { }",
    detail: "شرط مع بديل (if/else)",
    type: "keyword",
    boost: 8,
  }),
  snippetCompletion("لكل ${ع} من ${١} الى ${١٠} {\n\t${}\n}", {
    label: "لكل ... من ... الى",
    detail: "حلقة عدّاد رقمي (for range)",
    type: "keyword",
    boost: 9,
  }),
  snippetCompletion("لكل ${عنصر} في ${قائمة} {\n\t${}\n}", {
    label: "لكل ... في ...",
    detail: "حلقة مرور على عناصر (for in)",
    type: "keyword",
    boost: 8,
  }),
  snippetCompletion("كرر ${٣} مرات {\n\t${}\n}", {
    label: "كرر ... مرات { }",
    detail: "تكرار بعدد محدد (repeat)",
    type: "keyword",
    boost: 8,
  }),
  snippetCompletion("طالما ${شرط} {\n\t${}\n}", {
    label: "طالما ... { }",
    detail: "حلقة شرطية (while)",
    type: "keyword",
    boost: 7,
  }),
  snippetCompletion(
    "دالة ${اسم_الدالة}(${المدخلات}) {\n\t${}\n\tارجع ${النتيجة}\n}",
    {
      label: "دالة ... ( ) { }",
      detail: "تعريف دالة جديدة (function)",
      type: "keyword",
      boost: 9,
    },
  ),
  snippetCompletion("حاول {\n\t${}\n} التقط ${خطأ} {\n\tاطبع(${خطأ})\n}", {
    label: "حاول { } التقط { }",
    detail: "معالجة الأخطاء بأمان (try/catch)",
    type: "keyword",
    boost: 6,
  }),
  { label: "ارجع", detail: "إرجاع قيمة من الدالة", type: "keyword" },
  { label: "توقف", detail: "الخروج من الحلقة (break)", type: "keyword" },
  { label: "استمر", detail: "تخطي الدورة الحالية (continue)", type: "keyword" },
  { label: "صحيح", detail: "قيمة منطقية (True)", type: "constant" },
  { label: "خطأ", detail: "قيمة منطقية (False)", type: "constant" },
  { label: "فارغ", detail: "لا شيء (None)", type: "constant" },
];

const BUILTIN_COMPLETIONS: Completion[] = [
  snippetCompletion("اطبع(${قيمة})", {
    label: "اطبع",
    detail: "(قيمة) طباعة على الشاشة",
    type: "function",
    boost: 10,
  }),
  snippetCompletion('ادخل("${أدخل قيمة: }")', {
    label: "ادخل",
    detail: "(رسالة) قراءة مدخل من المستخدم",
    type: "function",
  }),
  snippetCompletion('اقرأ_جدول("${students.csv}")', {
    label: "اقرأ_جدول",
    detail: "(ملف) قراءة ملف CSV كجدول باندا",
    type: "function",
    boost: 9,
  }),
  snippetCompletion('احفظ_جدول(${جدول}، "${output.csv}")', {
    label: "احفظ_جدول",
    detail: "(جدول، ملف) حفظ الجدول كملف CSV",
    type: "function",
  }),
  snippetCompletion(
    'ارسم_أعمدة(${الفئات}، ${القيم}، العنوان="${الرسم البياني}")',
    {
      label: "ارسم_أعمدة",
      detail: "(فئات، قيم) رسم بياني بالأعمدة",
      type: "function",
      boost: 8,
    },
  ),
  snippetCompletion('ارسم_خط(${س}، ${ص}، العنوان="${الرسم الخطي}")', {
    label: "ارسم_خط",
    detail: "(س، ص) رسم بياني خطي",
    type: "function",
    boost: 8,
  }),
  snippetCompletion('ارسم_نقاط(${س}، ${ص}، العنوان="${مخطط التبعثر}")', {
    label: "ارسم_نقاط",
    detail: "(س، ص) مخطط تبعثر نقاط",
    type: "function",
  }),
  snippetCompletion('ارسم_دائري(${التسميات}، ${القيم}، العنوان="${النسب}")', {
    label: "ارسم_دائري",
    detail: "(تسميات، قيم) رسم دائري",
    type: "function",
  }),
  snippetCompletion("متوسط(${قائمة})", {
    label: "متوسط",
    detail: "(قائمة/عمود) حساب المعدل الحسابي",
    type: "function",
    boost: 8,
  }),
  snippetCompletion("مجموع(${قائمة})", {
    label: "مجموع",
    detail: "(قائمة) حساب المجموع الكلي",
    type: "function",
  }),
  snippetCompletion("طول(${قائمة})", {
    label: "طول",
    detail: "(قائمة/نص/جدول) عدد العناصر",
    type: "function",
  }),
  snippetCompletion("رتب(${قائمة})", {
    label: "رتب",
    detail: "(قائمة، تصاعدي=صحيح) ترتيب العناصر",
    type: "function",
  }),
  snippetCompletion("بدل(${قائمة}، ${٠}، ${١})", {
    label: "بدل",
    detail: "(قائمة، فهرس١، فهرس٢) تبديل عنصرين",
    type: "function",
  }),
  snippetCompletion("أكبر(${قائمة})", {
    label: "أكبر",
    detail: "(قائمة) القيمة العظمى",
    type: "function",
  }),
  snippetCompletion("أصغر(${قائمة})", {
    label: "أصغر",
    detail: "(قائمة) القيمة الصغرى",
    type: "function",
  }),
  snippetCompletion("قرب(${رقم}، ${٢})", {
    label: "قرب",
    detail: "(رقم، خانات) تقريب الكسور العشرية",
    type: "function",
  }),
  snippetCompletion("عشوائي(${١}، ${١٠٠})", {
    label: "عشوائي",
    detail: "(من، الى) رقم صحيح عشوائي",
    type: "function",
  }),
  snippetCompletion("اختر_عشوائي(${قائمة})", {
    label: "اختر_عشوائي",
    detail: "(قائمة) اختيار عنصر عشوائي",
    type: "function",
  }),
  {
    label: "باندا",
    detail: "مكتبة تحليل البيانات (pandas)",
    type: "namespace",
    boost: 9,
  },
  {
    label: "رياضيات",
    detail: "مكتبة الدوال الرياضية (math)",
    type: "namespace",
  },
];

const DOT_COMPLETIONS: Completion[] = [
  snippetCompletion("جدول_بيانات(${البيانات})", {
    label: "جدول_بيانات",
    detail: "باندا: إنشاء DataFrame جديد",
    type: "method",
    boost: 10,
  }),
  snippetCompletion("أول(${٥})", {
    label: "أول",
    detail: "(عدد) عرض أول صفوف الجدول (head)",
    type: "method",
    boost: 9,
  }),
  snippetCompletion("آخر(${٥})", {
    label: "آخر",
    detail: "(عدد) عرض آخر صفوف الجدول (tail)",
    type: "method",
    boost: 8,
  }),
  snippetCompletion("ملخص()", {
    label: "ملخص",
    detail: "إحصائيات شاملة للجدول (describe)",
    type: "method",
    boost: 9,
  }),
  snippetCompletion("حذف_الفارغ()", {
    label: "حذف_الفارغ",
    detail: "حذف الصفوف الفارغة (dropna)",
    type: "method",
    boost: 9,
  }),
  snippetCompletion("املأ_الفارغ(${٠})", {
    label: "املأ_الفارغ",
    detail: "(قيمة) تعبئة القيم المفقودة (fillna)",
    type: "method",
    boost: 8,
  }),
  snippetCompletion('رتب_قيم(حسب="${العمود}"، تصاعدي=${خطأ})', {
    label: "رتب_قيم",
    detail: "ترتيب الجدول حسب عمود (sort_values)",
    type: "method",
    boost: 9,
  }),
  snippetCompletion('تجميع("${العمود}")', {
    label: "تجميع",
    detail: "تجميع الصفوف حسب عمود (groupby)",
    type: "method",
    boost: 8,
  }),
  snippetCompletion('ارسم_أعمدة("${س}"، "${ص}"، العنوان="${الرسم}")', {
    label: "ارسم_أعمدة",
    detail: "رسم عمودين من الجدول مباشرة",
    type: "method",
    boost: 9,
  }),
  snippetCompletion('ارسم_خط("${س}"، "${ص}"، العنوان="${الرسم}")', {
    label: "ارسم_خط",
    detail: "رسم خطي من الجدول مباشرة",
    type: "method",
    boost: 8,
  }),
  snippetCompletion("متوسط()", {
    label: "متوسط",
    detail: "حساب المتوسط للعمود (mean)",
    type: "method",
    boost: 8,
  }),
  snippetCompletion("مجموع()", {
    label: "مجموع",
    detail: "حساب المجموع للعمود (sum)",
    type: "method",
  }),
  {
    label: "الأعمدة",
    detail: "أسماء أعمدة الجدول (columns)",
    type: "property",
    boost: 9,
  },
  {
    label: "الشكل",
    detail: "(عدد الصفوف، عدد الأعمدة) (shape)",
    type: "property",
    boost: 8,
  },
  { label: "القيم", detail: "مصفوفة القيم الخام (values)", type: "property" },
  snippetCompletion("أضف(${عنصر})", {
    label: "أضف",
    detail: "إضافة عنصر لنهاية القائمة (append)",
    type: "method",
    boost: 7,
  }),
  snippetCompletion("احذف(${عنصر})", {
    label: "احذف",
    detail: "حذف عنصر من القائمة (remove)",
    type: "method",
  }),
  snippetCompletion('استبدل("${القديم}"، "${الجديد}")', {
    label: "استبدل",
    detail: "استبدال نص بنص آخر (replace)",
    type: "method",
  }),
];

function extractDocumentSymbols(docText: string): Completion[] {
  const symbols = new Map<string, Completion>();
  const varRegex =
    /^\s*([a-zA-Z_\u0621-\u064A\u0671-\u06D3][a-zA-Z0-9_\u0621-\u064A\u0660-\u0669\u0671-\u06D3]*)\s*=/gm;
  const funcRegex =
    /(?:دالة|داله|function|def)\s+([a-zA-Z_\u0621-\u064A\u0671-\u06D3][a-zA-Z0-9_\u0621-\u064A\u0660-\u0669\u0671-\u06D3]*)\s*\(/g;

  let m: RegExpExecArray | null;
  while ((m = varRegex.exec(docText)) !== null) {
    symbols.set(m[1], {
      label: m[1],
      detail: "متغير في برنامجك",
      type: "variable",
      boost: 5,
    });
  }
  while ((m = funcRegex.exec(docText)) !== null) {
    symbols.set(m[1], {
      label: m[1],
      detail: "دالة في برنامجك",
      type: "function",
      boost: 6,
    });
  }
  return Array.from(symbols.values());
}

function arabicCompletionSource(
  context: CompletionContext,
): CompletionResult | null {
  const dotMatch = context.matchBefore(
    /\.[a-zA-Z0-9_\u0621-\u064A\u0660-\u0669\u0671-\u06D3]*/,
  );
  if (dotMatch) {
    const typedAfterDot = dotMatch.text.slice(1);
    const normQuery = normalizeAr(typedAfterDot);
    const filtered = DOT_COMPLETIONS.filter((item) =>
      normalizeAr(item.label).includes(normQuery),
    );
    return {
      from: dotMatch.from + 1,
      options: filtered,
      filter: false,
    };
  }

  const wordMatch = context.matchBefore(
    /[a-zA-Z_\u0621-\u064A\u0671-\u06D3][a-zA-Z0-9_\u0621-\u064A\u0660-\u0669\u0671-\u06D3]*/,
  );
  if (!wordMatch && !context.explicit) return null;

  const from = wordMatch ? wordMatch.from : context.pos;
  const typedWord = wordMatch ? wordMatch.text : "";
  const normQuery = normalizeAr(typedWord);

  const userSymbols = extractDocumentSymbols(context.state.doc.toString());
  const allOptions = [
    ...KEYWORD_COMPLETIONS,
    ...BUILTIN_COMPLETIONS,
    ...userSymbols,
  ];

  const filtered = allOptions.filter(
    (item) => !typedWord || normalizeAr(item.label).includes(normQuery),
  );

  return {
    from,
    options: filtered,
    filter: false,
  };
}

export const arabicAutocomplete: Extension = autocompletion({
  override: [arabicCompletionSource],
  activateOnTyping: true,
  maxRenderedOptions: 12,
});
