// ide/src/editor/autocomplete.ts
import {
  autocompletion,
  CompletionContext,
  Completion,
} from "@codemirror/autocomplete";

// 1. Top-Level Keywords, Control Flow, Types & Global Built-ins
const GLOBAL_COMPLETIONS: Completion[] = [
  // --- Control Flow & Declarations ---
  {
    label: "اذا",
    type: "keyword",
    detail: "جملة شرطية (if)",
    apply: "اذا شرط {\n\t\n}",
    boost: 10,
  },
  {
    label: "والا اذا",
    type: "keyword",
    detail: "شرط بديل (elif)",
    apply: "والا اذا شرط {\n\t\n}",
    boost: 9,
  },
  {
    label: "والا",
    type: "keyword",
    detail: "تنفيذ عند فشل الشروط (else)",
    apply: "والا {\n\t\n}",
    boost: 9,
  },
  {
    label: "لكل من الى",
    type: "keyword",
    detail: "حلقة رقمية شاملة (for range)",
    apply: "لكل ع من ١ الى ١٠ {\n\t\n}",
    boost: 8,
  },
  {
    label: "لكل في",
    type: "keyword",
    detail: "حلقة مرور على عناصر (for each)",
    apply: "لكل عنصر في قائمة {\n\t\n}",
    boost: 8,
  },
  {
    label: "كرر",
    type: "keyword",
    detail: "تكرار عدد محدد من المرات (repeat)",
    apply: "كرر ٣ مرات {\n\t\n}",
    boost: 8,
  },
  {
    label: "طالما",
    type: "keyword",
    detail: "حلقة شرطية مستمرة (while)",
    apply: "طالما شرط {\n\t\n}",
    boost: 7,
  },
  {
    label: "دالة",
    type: "keyword",
    detail: "تعريف دالة جديدة (function)",
    apply: "دالة اسم(مدخل) {\n\tارجع مدخل\n}",
    boost: 9,
  },
  {
    label: "صنف",
    type: "keyword",
    detail: "تعريف صنف كائني (class)",
    apply: "صنف اسم {\n\tدالة انشئ(قيمة) {\n\t\tهذا.قيمة = قيمة\n\t}\n}",
    boost: 8,
  },
  {
    label: "استورد",
    type: "keyword",
    detail: "استيراد مكتبة أو ملف .sad",
    apply: "استورد ",
    boost: 8,
  },
  {
    label: "من استورد",
    type: "keyword",
    detail: "استيراد عناصر محددة من مكتبة أو ملف",
    apply: "من مكتبة استورد عنصر",
    boost: 7,
  },
  {
    label: "حاول",
    type: "keyword",
    detail: "معالجة الأخطاء والاستثناءات (try/catch)",
    apply: "حاول {\n\t\n} التقط خطأ {\n\tاطبع(خطأ)\n}",
    boost: 6,
  },
  {
    label: "ارجع",
    type: "keyword",
    detail: "إرجاع قيمة من الدالة (return)",
    apply: "ارجع ",
  },
  {
    label: "توقف",
    type: "keyword",
    detail: "الخروج من الحلقة (break)",
    apply: "توقف",
  },
  {
    label: "استمر",
    type: "keyword",
    detail: "تخطي الدورة الحالية (continue)",
    apply: "استمر",
  },
  {
    label: "عام",
    type: "keyword",
    detail: "الإشارة لمتغير عام داخل دالة (global)",
    apply: "عام ",
  },
  {
    label: "هذا",
    type: "keyword",
    detail: "الإشارة للكائن الحالي داخل الصنف (self)",
    apply: "هذا.",
  },

  // --- Logical & Atomic Constants ---
  {
    label: "صح",
    type: "constant",
    detail: "قيمة منطقية صحيحة (true)",
    apply: "صح",
  },
  {
    label: "خطأ",
    type: "constant",
    detail: "قيمة منطقية خاطئة (false)",
    apply: "خطأ",
  },
  {
    label: "فارغ",
    type: "constant",
    detail: "قيمة فارغة (null / None)",
    apply: "فارغ",
  },
  {
    label: "عدم",
    type: "constant",
    detail: "قيمة فارغة (null / None)",
    apply: "عدم",
  },
  {
    label: "و",
    type: "keyword",
    detail: "معامل العطف المنطقي (and)",
    apply: "و ",
  },
  {
    label: "او",
    type: "keyword",
    detail: "معامل التخيير المنطقي (or)",
    apply: "او ",
  },
  {
    label: "ليس",
    type: "keyword",
    detail: "معامل النفي المنطقي (not)",
    apply: "ليس ",
  },
  { label: "في", type: "keyword", detail: "فحص الانتماء (in)", apply: "في " },

  // --- Single-Word Core Types ---
  {
    label: "عدد",
    type: "type",
    detail: "تحويل إلى عدد صحيح (int)",
    apply: "عدد()",
  },
  {
    label: "كسر",
    type: "type",
    detail: "تحويل إلى عدد كسري عشري (float)",
    apply: "كسر()",
  },
  { label: "نص", type: "type", detail: "تحويل إلى نص (str)", apply: "نص()" },
  {
    label: "منطق",
    type: "type",
    detail: "تحويل إلى قيمة منطقية (bool)",
    apply: "منطق()",
  },
  {
    label: "قائمة",
    type: "type",
    detail: "إنشاء أو تحويل إلى قائمة (list)",
    apply: "قائمة()",
  },
  {
    label: "قاموس",
    type: "type",
    detail: "إنشاء أو تحويل إلى قاموس (dict)",
    apply: "قاموس()",
  },
  {
    label: "جدول",
    type: "type",
    detail: "إنشاء جدول بيانات (Table)",
    apply: "جدول()",
  },
  {
    label: "عمود",
    type: "type",
    detail: "إنشاء عمود بيانات (Column)",
    apply: "عمود()",
  },
  {
    label: "نوع",
    type: "function",
    detail: "معرفة نوع أي قيمة أو كائن",
    apply: "نوع()",
  },

  // --- Core Built-in Functions ---
  {
    label: "اطبع",
    type: "function",
    detail: "طباعة نص أو جدول للمخرجات",
    apply: 'اطبع("")',
    boost: 10,
  },
  {
    label: "ادخل",
    type: "function",
    detail: "قراءة مدخل نصي من المستخدم",
    apply: 'ادخل("")',
  },
  {
    label: "طول",
    type: "function",
    detail: "عدد عناصر قائمة أو نص أو جدول",
    apply: "طول()",
  },
  {
    label: "مجموع",
    type: "function",
    detail: "مجموع أرقام قائمة أو عمود",
    apply: "مجموع()",
  },
  {
    label: "متوسط",
    type: "function",
    detail: "المتوسط الحسابي لقائمة أو عمود",
    apply: "متوسط()",
  },
  {
    label: "أكبر",
    type: "function",
    detail: "أكبر قيمة في قائمة أو عمود",
    apply: "أكبر()",
  },
  {
    label: "أصغر",
    type: "function",
    detail: "أصغر قيمة في قائمة أو عمود",
    apply: "أصغر()",
  },
  {
    label: "قرب",
    type: "function",
    detail: "تقريب كسر عشري لأقرب خانات",
    apply: "قرب(قيمة، ٢)",
  },
  {
    label: "مطلق",
    type: "function",
    detail: "القيمة المطلقة للعدد",
    apply: "مطلق()",
  },
  {
    label: "رتب",
    type: "function",
    detail: "ترتيب قائمة أو جدول",
    apply: "رتب()",
  },
  {
    label: "بدل",
    type: "function",
    detail: "تبديل عنصرين داخل قائمة",
    apply: "بدل(قائمة، ٠، ١)",
  },
  {
    label: "فهارس",
    type: "function",
    detail: "قائمة فهارس من ٠ إلى الطول-١",
    apply: "فهارس()",
  },
  {
    label: "مدى",
    type: "function",
    detail: "توليد تسلسل أرقام شامل",
    apply: "مدى(١، ١٠)",
  },
  {
    label: "عشوائي",
    type: "function",
    detail: "توليد عدد عشوائي بين حدين",
    apply: "عشوائي(١، ١٠٠)",
  },
  {
    label: "اختر",
    type: "function",
    detail: "اختيار عنصر عشوائي من قائمة",
    apply: "اختر()",
  },

  // --- Data Science & Chart Global Shortcuts ---
  {
    label: "اقرأ",
    type: "function",
    detail: "قراءة ملف CSV إلى جدول بيانات",
    apply: 'اقرأ("students.csv")',
    boost: 9,
  },
  {
    label: "احفظ",
    type: "function",
    detail: "حفظ جدول البيانات في ملف CSV",
    apply: 'احفظ(جدول، "output.csv")',
  },
  {
    label: "أعمدة",
    type: "function",
    detail: "رسم بياني بالأعمدة (Bar Chart)",
    apply: 'أعمدة(س، ص، العنوان="")',
  },
  {
    label: "خط",
    type: "function",
    detail: "رسم بياني خطي (Line Chart)",
    apply: 'خط(س، ص، العنوان="")',
  },
  {
    label: "نقاط",
    type: "function",
    detail: "مخطط تبعثر نقاط (Scatter Plot)",
    apply: 'نقاط(س، ص، العنوان="")',
  },
  {
    label: "دائري",
    type: "function",
    detail: "رسم بياني دائري (Pie Chart)",
    apply: 'دائري(الفئات، القيم، العنوان="")',
  },

  // --- Standard Library Modules ---
  {
    label: "رياضيات",
    type: "namespace",
    detail: "مكتبة الدوال والثوابت الرياضية",
    apply: "رياضيات",
  },
  {
    label: "عشوائيات",
    type: "namespace",
    detail: "مكتبة التوليد والاختيار العشوائي",
    apply: "عشوائيات",
  },
  {
    label: "طلبات",
    type: "namespace",
    detail: "مكتبة الشبكة وطلبات HTTP/JSON",
    apply: "طلبات",
  },
  {
    label: "جداول",
    type: "namespace",
    detail: "مكتبة الجداول وتحليل البيانات",
    apply: "جداول",
  },
  {
    label: "رسوم",
    type: "namespace",
    detail: "مكتبة الرسوم البيانية",
    apply: "رسوم",
  },
];

// 2. Module-Specific Dot Completions (e.g. `رياضيات.`)
const MODULE_MEMBER_COMPLETIONS: Record<string, Completion[]> = {
  رياضيات: [
    { label: "ط", type: "constant", detail: "الثابت ط (Pi = 3.14159...)" },
    { label: "باي", type: "constant", detail: "الثابت باي (Pi = 3.14159...)" },
    {
      label: "هـ",
      type: "constant",
      detail: "العدد النيبيري (e = 2.71828...)",
    },
    {
      label: "جذر",
      type: "function",
      detail: "الجذر التربيعي لعدد",
      apply: "جذر()",
    },
    {
      label: "قوة",
      type: "function",
      detail: "رفع أساس لأس معين",
      apply: "قوة(الأساس، الأس)",
    },
    {
      label: "مطلق",
      type: "function",
      detail: "القيمة المطلقة",
      apply: "مطلق()",
    },
    {
      label: "سقف",
      type: "function",
      detail: "التقريب للأعلى (ceil)",
      apply: "سقف()",
    },
    {
      label: "أرضية",
      type: "function",
      detail: "التقريب للأسفل (floor)",
      apply: "أرضية()",
    },
    {
      label: "جا",
      type: "function",
      detail: "جيب الزاوية بالدرجات (sin)",
      apply: "جا(٩٠)",
    },
    {
      label: "جتا",
      type: "function",
      detail: "جيب تمام الزاوية بالدرجات (cos)",
      apply: "جتا(٠)",
    },
    {
      label: "ظا",
      type: "function",
      detail: "ظل الزاوية بالدرجات (tan)",
      apply: "ظا(٤٥)",
    },
    {
      label: "لوغاريتم",
      type: "function",
      detail: "اللوغاريتم الطبيعي أو لأساس محدد",
      apply: "لوغاريتم()",
    },
  ],
  عشوائيات: [
    {
      label: "عدد",
      type: "function",
      detail: "عدد صحيح عشوائي بين حدين",
      apply: "عدد(١، ١٠٠)",
    },
    {
      label: "كسر",
      type: "function",
      detail: "كسر عشري عشوائي",
      apply: "كسر(٠، ١)",
    },
    {
      label: "اختر",
      type: "function",
      detail: "اختيار عنصر عشوائي من قائمة",
      apply: "اختر(قائمة)",
    },
    {
      label: "اخلط",
      type: "function",
      detail: "خلط عناصر قائمة عشوائياً",
      apply: "اخلط(قائمة)",
    },
    {
      label: "عينة",
      type: "function",
      detail: "سحب عينة عشوائية بحجم ك",
      apply: "عينة(قائمة، ٣)",
    },
  ],
  طلبات: [
    {
      label: "احصل",
      type: "function",
      detail: "إرسال طلب GET وإرجاع كائن استجابة",
      apply: 'احصل("https://...")',
    },
    {
      label: "جلب",
      type: "function",
      detail: "جلب بيانات JSON مباشرة كقاموس أو قائمة",
      apply: 'جلب("https://...")',
    },
  ],
  جداول: [
    {
      label: "اقرأ",
      type: "function",
      detail: "قراءة ملف CSV كجدول بيانات",
      apply: 'اقرأ("students.csv")',
    },
    {
      label: "احفظ",
      type: "function",
      detail: "حفظ جدول في ملف CSV",
      apply: 'احفظ(جدول، "out.csv")',
    },
    {
      label: "أنشئ",
      type: "function",
      detail: "إنشاء جدول من قاموس أو قائمة",
      apply: "أنشئ()",
    },
    {
      label: "عمود",
      type: "function",
      detail: "إنشاء عمود بيانات",
      apply: "عمود([])",
    },
  ],
  رسوم: [
    {
      label: "أعمدة",
      type: "function",
      detail: "رسم بياني بالأعمدة",
      apply: 'أعمدة(س، ص، العنوان="")',
    },
    {
      label: "خط",
      type: "function",
      detail: "رسم بياني خطي",
      apply: 'خط(س، ص، العنوان="")',
    },
    {
      label: "نقاط",
      type: "function",
      detail: "مخطط تبعثر نقاط",
      apply: 'نقاط(س، ص، العنوان="")',
    },
    {
      label: "دائري",
      type: "function",
      detail: "رسم بياني دائري",
      apply: 'دائري(الفئات، القيم، العنوان="")',
    },
  ],
};

// 3. General Method & Property Dot Completions (for Table, Column, List, Dict, String)
const METHOD_COMPLETIONS: Completion[] = [
  // Table (`جدول`) Methods
  {
    label: "نظف",
    type: "method",
    detail: "جدول/نص: حذف الصفوف الفارغة أو مسافات الأطراف",
    apply: "نظف()",
  },
  {
    label: "املأ",
    type: "method",
    detail: "جدول: تعويض القيم الفارغة بقيمة افتراضية",
    apply: "املأ(٠)",
  },
  {
    label: "رتب",
    type: "method",
    detail: "جدول/قائمة: ترتيب تصاعدي أو تنازلي",
    apply: 'رتب("المعدل"، تصاعدي=خطأ)',
  },
  {
    label: "صفي",
    type: "method",
    detail: "جدول: تصفية الصفوف بناءً على شرط",
    apply: "صفي()",
  },
  {
    label: "رشح",
    type: "method",
    detail: "جدول: ترشيح الصفوف بناءً على شرط",
    apply: "رشح()",
  },
  {
    label: "تجميع",
    type: "method",
    detail: "جدول: تجميع الصفوف حسب عمود (groupby)",
    apply: 'تجميع("")',
  },
  {
    label: "ملخص",
    type: "method",
    detail: "جدول: ملخص إحصائي شامل للأعمدة",
    apply: "ملخص()",
  },
  {
    label: "أول",
    type: "method",
    detail: "جدول/قائمة: إرجاع أول ن عناصر أو صفوف",
    apply: "أول(٥)",
  },
  {
    label: "آخر",
    type: "method",
    detail: "جدول/قائمة: إرجاع آخر ن عناصر أو صفوف",
    apply: "آخر(٥)",
  },
  {
    label: "صف",
    type: "method",
    detail: "جدول: إرجاع صف محدد كقاموس",
    apply: "صف(٠)",
  },
  {
    label: "احفظ",
    type: "method",
    detail: "جدول: حفظ الجدول في ملف CSV",
    apply: 'احفظ("output.csv")',
  },
  {
    label: "أعمدة",
    type: "method",
    detail: "جدول: رسم بياني بالأعمدة لعمودين",
    apply: 'أعمدة("س"، "ص"، العنوان="")',
  },
  {
    label: "خط",
    type: "method",
    detail: "جدول: رسم بياني خطي لعمودين",
    apply: 'خط("س"، "ص"، العنوان="")',
  },
  {
    label: "نقاط",
    type: "method",
    detail: "جدول: مخطط نقاط لعمودين",
    apply: 'نقاط("س"، "ص")',
  },
  {
    label: "دائري",
    type: "method",
    detail: "جدول: رسم دائري لعمودين",
    apply: 'دائري("الفئات"، "القيم")',
  },
  { label: "الأعمدة", type: "property", detail: "جدول: قائمة بأسماء الأعمدة" },
  {
    label: "الشكل",
    type: "property",
    detail: "جدول: [عدد الصفوف، عدد الأعمدة]",
  },
  { label: "صفوف", type: "property", detail: "جدول: عدد الصفوف" },

  // Column (`عمود`) Statistical Methods
  {
    label: "متوسط",
    type: "method",
    detail: "عمود/تجميع: المتوسط الحسابي",
    apply: "متوسط()",
  },
  {
    label: "مجموع",
    type: "method",
    detail: "عمود/تجميع: مجموع القيم",
    apply: "مجموع()",
  },
  {
    label: "أكبر",
    type: "method",
    detail: "عمود/تجميع: القيمة العظمى",
    apply: "أكبر()",
  },
  {
    label: "أصغر",
    type: "method",
    detail: "عمود/تجميع: القيمة الصغرى",
    apply: "أصغر()",
  },
  {
    label: "وسيط",
    type: "method",
    detail: "عمود: القيمة الوسيطة (median)",
    apply: "وسيط()",
  },
  {
    label: "فريد",
    type: "method",
    detail: "عمود: قائمة القيم الفريدة بدون تكرار",
    apply: "فريد()",
  },
  {
    label: "كقائمة",
    type: "method",
    detail: "عمود: تحويل العمود إلى قائمة",
    apply: "كقائمة()",
  },

  // List (`قائمة`) Methods
  {
    label: "أضف",
    type: "method",
    detail: "قائمة: إضافة عنصر في النهاية",
    apply: "أضف()",
  },
  {
    label: "أدرج",
    type: "method",
    detail: "قائمة: إدراج عنصر في موقع محدد",
    apply: "أدرج(٠، عنصر)",
  },
  {
    label: "احذف",
    type: "method",
    detail: "قائمة/قاموس: حذف عنصر أو مفتاح",
    apply: "احذف()",
  },
  {
    label: "اسحب",
    type: "method",
    detail: "قائمة: سحب وإرجاع عنصر من القائمة",
    apply: "اسحب()",
  },
  {
    label: "امسح",
    type: "method",
    detail: "قائمة: تفريغ جميع العناصر",
    apply: "امسح()",
  },
  {
    label: "اعكس",
    type: "method",
    detail: "قائمة: عكس ترتيب العناصر",
    apply: "اعكس()",
  },
  {
    label: "اربط",
    type: "method",
    detail: "قائمة: دمج العناصر في نص واحد بفاصل",
    apply: 'اربط("، ")',
  },
  {
    label: "عدد",
    type: "method",
    detail: "قائمة/عمود: حساب عدد مرات التكرار",
    apply: "عدد()",
  },

  // Dict (`قاموس`) & HTTP Response Methods
  {
    label: "احصل",
    type: "method",
    detail: "قاموس: جلب قيمة مفتاح مع قيمة افتراضية",
    apply: "احصل(مفتاح، فارغ)",
  },
  {
    label: "مفاتيح",
    type: "method",
    detail: "قاموس: قائمة بجميع المفاتيح",
    apply: "مفاتيح()",
  },
  {
    label: "قيم",
    type: "method",
    detail: "قاموس: قائمة بجميع القيم",
    apply: "قيم()",
  },
  {
    label: "عناصر",
    type: "method",
    detail: "قاموس: قائمة أزواج [المفتاح، القيمة]",
    apply: "عناصر()",
  },
  {
    label: "كقاموس",
    type: "method",
    detail: "استجابة: تحويل JSON إلى قاموس أو قائمة",
    apply: "كقاموس()",
  },

  // String (`نص`) Methods & Shared Properties
  {
    label: "قسم",
    type: "method",
    detail: "نص: تقسيم النص إلى قائمة كلمات",
    apply: 'قسم(" ")',
  },
  {
    label: "استبدل",
    type: "method",
    detail: "نص: استبدال جزء قديم بجديد",
    apply: 'استبدل("قديم"، "جديد")',
  },
  {
    label: "يبدأ",
    type: "method",
    detail: "نص: التحقق من البداية ببادئة",
    apply: 'يبدأ("")',
  },
  {
    label: "ينتهي",
    type: "method",
    detail: "نص: التحقق من النهاية بلاحقة",
    apply: 'ينتهي("")',
  },
  {
    label: "يضم",
    type: "method",
    detail: "نص/قائمة/قاموس: التحقق من وجود عنصر",
    apply: "يضم()",
  },
  {
    label: "موقع",
    type: "method",
    detail: "نص: إرجاع فهرس أول ظهور لجزء نصي",
    apply: 'موقع("")',
  },
  {
    label: "كبير",
    type: "method",
    detail: "نص: تحويل الأحرف اللاتينية لكبيرة",
    apply: "كبير()",
  },
  {
    label: "صغير",
    type: "method",
    detail: "نص: تحويل الأحرف اللاتينية لصغيرة",
    apply: "صغير()",
  },
  {
    label: "حرف",
    type: "method",
    detail: "نص: إرجاع الحرف عند الفهرس المحدد",
    apply: "حرف(٠)",
  },
  {
    label: "طول",
    type: "property",
    detail: "خاصية: عدد العناصر أو الأحرف أو الصفوف",
  },
];

function arabicCompletionSource(context: CompletionContext) {
  // 1. Check if the user is typing after a dot: e.g. `رياضيات.ج` or `جدول.`
  const dotMatch = context.matchBefore(
    /([\u0621-\u064A\u0671-\u06D3a-zA-Z0-9_]+)\.([\u0621-\u064A\u0671-\u06D3a-zA-Z0-9_]*)$/,
  );

  if (dotMatch) {
    const fullText = dotMatch.text;
    const dotIndex = fullText.lastIndexOf(".");
    const receiverName = fullText.slice(0, dotIndex);
    const fromPos = dotMatch.from + dotIndex + 1;

    if (MODULE_MEMBER_COMPLETIONS[receiverName]) {
      return {
        from: fromPos,
        options: MODULE_MEMBER_COMPLETIONS[receiverName],
        validFor: /^[\u0621-\u064A\u0671-\u06D3a-zA-Z0-9_]*$/,
      };
    }

    return {
      from: fromPos,
      options: METHOD_COMPLETIONS,
      validFor: /^[\u0621-\u064A\u0671-\u06D3a-zA-Z0-9_]*$/,
    };
  }

  // 2. Standard top-level identifier completion
  const word = context.matchBefore(/[\u0621-\u064A\u0671-\u06D3a-zA-Z0-9_]+/);
  if (!word && !context.explicit) return null;

  return {
    from: word ? word.from : context.pos,
    options: GLOBAL_COMPLETIONS,
    validFor: /^[\u0621-\u064A\u0671-\u06D3a-zA-Z0-9_]*$/,
  };
}

export const arabicAutocomplete = autocompletion({
  override: [arabicCompletionSource],
  activateOnTyping: true,
});
