// ide/src/editor/ArabicEditor.tsx
import React, { useEffect, useRef } from "react";
import { EditorState } from "@codemirror/state";
import {
  EditorView,
  keymap,
  lineNumbers,
  highlightActiveLine,
  highlightActiveLineGutter,
} from "@codemirror/view";
import {
  defaultKeymap,
  history,
  historyKeymap,
  indentWithTab,
} from "@codemirror/commands";
import { bracketMatching } from "@codemirror/language";
import { closeBrackets, closeBracketsKeymap } from "@codemirror/autocomplete";
import { ChevronLeft, FileCode } from "lucide-react";

import { arabicLanguageSupport } from "./arabicLanguage";
import { arabicAutocomplete } from "./autocomplete";
import { inlineErrorField, setDiagnosticEffect } from "./errorWidget";

interface ArabicEditorProps {
  fileName?: string;
  code: string;
  onChange: (newCode: string) => void;
  onRun: () => void;
  errorLine: number | null;
  errorMessage: string;
}

export const ArabicEditor: React.FC<ArabicEditorProps> = ({
  fileName = "main.sad",
  code,
  onChange,
  onRun,
  errorLine,
  errorMessage,
}) => {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const viewRef = useRef<EditorView | null>(null);
  const onRunRef = useRef(onRun);
  const onChangeRef = useRef(onChange);
  onRunRef.current = onRun;
  onChangeRef.current = onChange;

  useEffect(() => {
    if (!containerRef.current) return;

    const state = EditorState.create({
      doc: code,
      extensions: [
        lineNumbers(),
        highlightActiveLineGutter(),
        highlightActiveLine(),
        history(),
        bracketMatching(),
        closeBrackets(),
        ...arabicLanguageSupport,
        arabicAutocomplete,
        inlineErrorField,
        EditorView.lineWrapping,
        keymap.of([
          ...closeBracketsKeymap,
          ...defaultKeymap,
          ...historyKeymap,
          indentWithTab,
          {
            key: "Mod-Enter",
            run: () => {
              onRunRef.current();
              return true;
            },
          },
        ]),
        EditorView.updateListener.of((update) => {
          if (update.docChanged) {
            onChangeRef.current(update.state.doc.toString());
          }
        }),
      ],
    });

    const view = new EditorView({
      state,
      parent: containerRef.current,
    });

    viewRef.current = view;
    return () => view.destroy();
  }, []);

  useEffect(() => {
    const view = viewRef.current;
    if (!view) return;
    const currentText = view.state.doc.toString();
    if (code !== currentText) {
      view.dispatch({
        changes: { from: 0, to: currentText.length, insert: code },
        effects: setDiagnosticEffect.of(null),
      });
    }
  }, [code]);

  useEffect(() => {
    const view = viewRef.current;
    if (!view) return;

    if (errorLine && errorMessage) {
      const clampedLine = Math.max(
        1,
        Math.min(Number(errorLine), view.state.doc.lines),
      );
      view.dispatch({
        effects: [
          setDiagnosticEffect.of({
            line: clampedLine,
            message: errorMessage,
            onAutoRun: () => onRunRef.current(),
          }),
          EditorView.scrollIntoView(view.state.doc.line(clampedLine).from, {
            y: "center",
          }),
        ],
      });
    } else {
      view.dispatch({ effects: setDiagnosticEffect.of(null) });
    }
  }, [errorLine, errorMessage]);

  const pathParts = fileName.split("/");

  return (
    <div
      className="flex flex-col h-full w-full bg-[var(--sol-base3)] select-none"
      dir="rtl"
    >
      {/* Slim 24px VS Code Breadcrumb Bar */}
      <div className="h-6 px-3 bg-[var(--sol-base3)] border-b border-[var(--sol-border)] flex items-center gap-1 text-[11px] text-[var(--sol-base1)] shrink-0">
        <span>المشروع</span>
        {pathParts.map((part, i) => (
          <React.Fragment key={i}>
            <ChevronLeft className="w-3 h-3 shrink-0" />
            <span
              dir="ltr"
              className={`font-mono flex items-center gap-1 ${
                i === pathParts.length - 1
                  ? "text-[var(--sol-base01)] font-semibold"
                  : ""
              }`}
            >
              {i === pathParts.length - 1 && (
                <FileCode className="w-3 h-3 text-[var(--sol-blue)] shrink-0" />
              )}
              {part}
            </span>
          </React.Fragment>
        ))}
      </div>

      <div
        ref={containerRef}
        className="flex-1 min-h-0 overflow-auto text-[15px]"
      />
    </div>
  );
};
