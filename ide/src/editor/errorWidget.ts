// ide/src/editor/errorWidget.ts
import { StateField, StateEffect } from "@codemirror/state";
import {
  EditorView,
  Decoration,
  type DecorationSet,
  WidgetType,
} from "@codemirror/view";

export interface DiagnosticPayload {
  line: number;
  message: string;
  onAutoRun?: () => void;
}

export const setDiagnosticEffect =
  StateEffect.define<DiagnosticPayload | null>();

interface QuickFixAction {
  label: string;
  newLineText: string;
}

function parseQuickFix(
  errorText: string,
  lineText: string,
): QuickFixAction | null {
  if (!errorText) return null;

  const didYouMeanMatch = errorText.match(/هل تقصد '([^']+)'؟/);
  if (didYouMeanMatch) {
    const suggested = didYouMeanMatch[1];
    const beforeSuggestion = errorText.split("هل تقصد")[0];
    const wrongTokenMatch = beforeSuggestion.match(/'([^']+)'/);
    if (wrongTokenMatch) {
      const wrongToken = wrongTokenMatch[1];
      if (lineText.includes(wrongToken)) {
        return {
          label: `إصلاح تلقائي: استبدال '${wrongToken}' بـ '${suggested}'`,
          newLineText: lineText.replace(wrongToken, suggested),
        };
      }
    }
  }

  if (errorText.includes("بدلاً من '=='") && lineText.includes("=")) {
    const fixedLine = lineText.replace(/([^=!<>])=([^=])/, "$1==$2");
    if (fixedLine !== lineText) {
      return {
        label: "إصلاح تلقائي: تحويل '=' إلى '=='",
        newLineText: fixedLine,
      };
    }
  }

  if (errorText.includes("نسيت إغلاق القوس الدائري ')'")) {
    return {
      label: "إصلاح تلقائي: إضافة ')' في نهاية السطر",
      newLineText: lineText + ")",
    };
  }

  if (errorText.includes("نسيت فتح قوس المجموعة '{'")) {
    return {
      label: "إصلاح تلقائي: إضافة ' {' في نهاية السطر",
      newLineText: lineText + " {",
    };
  }

  return null;
}

class InlineErrorWidget extends WidgetType {
  lineNo: number;
  message: string;
  onAutoRun?: () => void;

  constructor(lineNo: number, message: string, onAutoRun?: () => void) {
    super();
    this.lineNo = lineNo;
    this.message = message;
    this.onAutoRun = onAutoRun;
  }

  eq(other: InlineErrorWidget): boolean {
    return other.lineNo === this.lineNo && other.message === this.message;
  }

  toDOM(view: EditorView): HTMLElement {
    const container = document.createElement("div");
    container.dir = "rtl";
    container.className =
      "my-1.5 mx-4 p-3 rounded-lg bg-red-950/95 border-r-4 border-red-500 text-red-100 text-sm shadow-lg flex flex-col gap-2 font-sans";

    const parts = this.message.split("💡 التشخيص:");
    const headline = parts[0].split("\n")[0].trim();
    const diagnosis = parts[1] ? parts[1].trim() : this.message;

    const headerRow = document.createElement("div");
    headerRow.className = "font-bold text-red-300";
    headerRow.textContent = headline;
    container.appendChild(headerRow);

    const bodyRow = document.createElement("div");
    bodyRow.className = "text-slate-100 whitespace-pre-wrap leading-relaxed";
    bodyRow.textContent = `💡 ${diagnosis}`;
    container.appendChild(bodyRow);

    if (this.lineNo >= 1 && this.lineNo <= view.state.doc.lines) {
      const lineObj = view.state.doc.line(this.lineNo);
      const fix = parseQuickFix(this.message, lineObj.text);

      if (fix) {
        const actionsRow = document.createElement("div");
        actionsRow.className = "flex items-center gap-2 mt-1";

        const fixBtn = document.createElement("button");
        fixBtn.type = "button";
        fixBtn.className =
          "px-3 py-1.5 rounded-md bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition flex items-center gap-1.5 cursor-pointer shadow";
        fixBtn.textContent = `✨ ${fix.label} وتشغيل`;

        fixBtn.onclick = (e) => {
          e.preventDefault();
          const currentLine = view.state.doc.line(this.lineNo);
          view.dispatch({
            changes: {
              from: currentLine.from,
              to: currentLine.to,
              insert: fix.newLineText,
            },
            effects: setDiagnosticEffect.of(null),
          });
          view.focus();
          if (this.onAutoRun) {
            setTimeout(() => this.onAutoRun?.(), 50);
          }
        };

        actionsRow.appendChild(fixBtn);
        container.appendChild(actionsRow);
      }
    }

    return container;
  }

  ignoreEvent(): boolean {
    return true;
  }
}

export const inlineErrorField = StateField.define<DecorationSet>({
  create() {
    return Decoration.none;
  },
  update(decorations, tr) {
    if (tr.docChanged) {
      return Decoration.none;
    }

    for (const effect of tr.effects) {
      if (effect.is(setDiagnosticEffect)) {
        const payload = effect.value;
        if (
          !payload ||
          !payload.line ||
          payload.line < 1 ||
          payload.line > tr.state.doc.lines
        ) {
          return Decoration.none;
        }

        const lineObj = tr.state.doc.line(payload.line);
        const lineHighlight = Decoration.line({
          attributes: {
            style:
              "background-color: rgba(239, 68, 68, 0.18); border-right: 4px solid #ef4444;",
          },
        }).range(lineObj.from);

        const blockWidget = Decoration.widget({
          widget: new InlineErrorWidget(
            payload.line,
            payload.message,
            payload.onAutoRun,
          ),
          block: true,
          side: 1,
        }).range(lineObj.to);

        return Decoration.set([lineHighlight, blockWidget]);
      }
    }

    return decorations;
  },
  provide: (field) => EditorView.decorations.from(field),
});
