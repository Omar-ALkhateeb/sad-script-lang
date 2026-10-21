// ide/src/components/OutputWorkbench.tsx
import React, { useState } from "react";
import { Terminal, Database, Code, Download, Trash2 } from "lucide-react";
import { ExecutionResult } from "../types/ide";

interface OutputWorkbenchProps {
  result: ExecutionResult | null;
  onClear: () => void;
  onJumpToLine: (line: number) => void;
}

type OutputTab = "console" | "data" | "python";

export const OutputWorkbench: React.FC<OutputWorkbenchProps> = ({
  result,
  onClear,
  onJumpToLine,
}) => {
  const [activeTab, setActiveTab] = useState<OutputTab>("console");

  const dfList = result ? Object.values(result.dataframes) : [];
  const dataCount = result?.variables.length || 0;

  const downloadSvg = (svgStr: string, index: number) => {
    const blob = new Blob([svgStr], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `chart_${index + 1}.svg`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const tabClass = (tab: OutputTab) =>
    `h-full px-3 text-xs flex items-center gap-1.5 border-t-2 whitespace-nowrap shrink-0 transition cursor-pointer ${
      activeTab === tab
        ? "border-[var(--sol-blue)] text-[var(--sol-base01)] font-bold bg-[var(--sol-base3)]"
        : "border-transparent text-[var(--sol-base1)] hover:text-[var(--sol-base01)] bg-[var(--sol-base2)]"
    }`;

  return (
    <div className="flex flex-col h-full bg-[var(--sol-base3)] min-w-0">
      {/* Slim 3-Tab Header */}
      <div className="flex items-center justify-between pl-2 bg-[var(--sol-base2)] border-b border-[var(--sol-border)] h-8 shrink-0 select-none">
        <div className="flex items-center h-full overflow-x-auto no-scrollbar">
          <button
            type="button"
            onClick={() => setActiveTab("console")}
            className={tabClass("console")}
          >
            <Terminal className="w-3.5 h-3.5 text-[var(--sol-green)]" />
            <span>المخرجات</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("data")}
            className={tabClass("data")}
          >
            <Database className="w-3.5 h-3.5 text-[var(--sol-blue)]" />
            <span>البيانات والمتغيرات ({dataCount})</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("python")}
            className={tabClass("python")}
          >
            <Code className="w-3.5 h-3.5 text-[var(--sol-violet)]" />
            <span>بايثون</span>
          </button>
        </div>

        <button
          type="button"
          onClick={onClear}
          className="p-1 text-[var(--sol-base1)] hover:text-[var(--sol-base01)] rounded cursor-pointer"
          title="مسح المخرجات"
        >
          <Trash2 className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* TAB 1: CONSOLE + CHARTS */}
      {activeTab === "console" && (
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-[var(--sol-base3)]">
          {!result ? (
            <div className="text-[var(--sol-base1)] text-xs">
              اضغط على "تشغيل" (أو Ctrl+Enter) لتنفيذ البرنامج...
            </div>
          ) : (
            <>
              {result.stdout && (
                <pre className="whitespace-pre-wrap text-[var(--sol-base01)] leading-relaxed font-mono text-[13px]">
                  {result.stdout}
                </pre>
              )}

              {!result.ok && result.error && (
                <div className="p-3 rounded bg-[var(--sol-base2)] border-r-4 border-[var(--sol-red)] text-[var(--sol-base01)] space-y-2">
                  <pre className="whitespace-pre-wrap text-xs leading-relaxed font-mono text-[var(--sol-red)]">
                    {result.error}
                  </pre>
                  {result.error_line && (
                    <button
                      type="button"
                      onClick={() => onJumpToLine(result.error_line!)}
                      className="px-2.5 py-1 rounded bg-[var(--sol-red)] text-white text-xs font-semibold cursor-pointer"
                    >
                      الانتقال إلى السطر {result.error_line}
                    </button>
                  )}
                </div>
              )}

              {result.charts.length > 0 && (
                <div className="space-y-3 pt-2">
                  {result.charts.map((svg, idx) => (
                    <div
                      key={idx}
                      className="bg-[var(--sol-base3)] border border-[var(--sol-border)] rounded p-3 overflow-x-auto"
                    >
                      <div className="flex items-center justify-between mb-1 text-[11px] font-semibold text-[var(--sol-base1)]">
                        <span>الرسم البياني ({idx + 1})</span>
                        <button
                          type="button"
                          onClick={() => downloadSvg(svg, idx)}
                          className="px-2 py-0.5 rounded bg-[var(--sol-base2)] hover:bg-[#e1dbcd] text-[var(--sol-base01)] flex items-center gap-1 cursor-pointer"
                        >
                          <Download className="w-3 h-3" />
                          <span>SVG</span>
                        </button>
                      </div>
                      <div
                        className="flex justify-center [&>svg]:max-w-full [&>svg]:h-auto"
                        dangerouslySetInnerHTML={{ __html: svg }}
                      />
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      )}

      {/* TAB 2: UNIFIED DATAFRAMES & VARIABLES VIEW */}
      {activeTab === "data" && (
        <div className="flex-1 overflow-y-auto p-4 space-y-5 bg-[var(--sol-base3)] text-xs">
          {/* 1. DataFrames Section */}
          {dfList.length > 0 && (
            <div className="space-y-3">
              <div className="font-bold text-[var(--sol-base01)]">
                جداول البيانات (DataFrames)
              </div>
              {dfList.map((df) => (
                <div
                  key={df.name}
                  className="border border-[var(--sol-border)] rounded overflow-x-auto"
                >
                  <div className="px-3 py-1.5 bg-[var(--sol-base2)] border-b border-[var(--sol-border)] font-bold text-[var(--sol-blue)] flex justify-between">
                    <span>{df.name}</span>
                    <span className="text-[var(--sol-base1)] font-normal">
                      {df.shape[0]} صف × {df.shape[1]} عمود
                    </span>
                  </div>
                  <table className="w-full border-collapse">
                    <thead>
                      <tr className="bg-[var(--sol-base2)]/60 text-[var(--sol-base01)]">
                        {df.columns.map((col) => (
                          <th
                            key={col}
                            className="border-b border-l border-[var(--sol-border)] px-2.5 py-1.5 text-right"
                          >
                            {col}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {df.rows.map((row, rIdx) => (
                        <tr
                          key={rIdx}
                          className="even:bg-[var(--sol-base2)]/30"
                        >
                          {row.map((cell, cIdx) => (
                            <td
                              key={cIdx}
                              className="border-b border-l border-[var(--sol-border)] px-2.5 py-1 font-mono"
                            >
                              {cell}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ))}
            </div>
          )}

          {/* 2. Variables Section */}
          <div className="space-y-2">
            <div className="font-bold text-[var(--sol-base01)]">
              المتغيرات في الذاكرة
            </div>
            {!result || result.variables.length === 0 ? (
              <div className="text-[var(--sol-base1)]">
                لا توجد متغيرات مسجلة بعد.
              </div>
            ) : (
              <table className="w-full border-collapse border border-[var(--sol-border)]">
                <thead>
                  <tr className="bg-[var(--sol-base2)] text-[var(--sol-base01)]">
                    <th className="border border-[var(--sol-border)] px-2.5 py-1.5 text-right">
                      الاسم
                    </th>
                    <th className="border border-[var(--sol-border)] px-2.5 py-1.5 text-right">
                      النوع
                    </th>
                    <th className="border border-[var(--sol-border)] px-2.5 py-1.5 text-right">
                      القيمة
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {result.variables.map((v) => (
                    <tr key={v.name} className="even:bg-[var(--sol-base2)]/30">
                      <td className="border border-[var(--sol-border)] px-2.5 py-1 font-bold text-[var(--sol-blue)] font-mono">
                        {v.name}
                      </td>
                      <td className="border border-[var(--sol-border)] px-2.5 py-1 text-[var(--sol-violet)]">
                        {v.type}
                      </td>
                      <td className="border border-[var(--sol-border)] px-2.5 py-1 font-mono">
                        {v.value}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      )}

      {/* TAB 3: TRANSPILED PYTHON CODE */}
      {activeTab === "python" && (
        <div
          className="flex-1 overflow-auto p-4 bg-[var(--sol-base3)]"
          dir="ltr"
        >
          <pre className="text-xs font-mono text-[var(--sol-base01)] leading-relaxed">
            {result?.python_code ||
              "# سيظهر كود بايثون المترجم هنا بعد تشغيل البرنامج..."}
          </pre>
        </div>
      )}
    </div>
  );
};
