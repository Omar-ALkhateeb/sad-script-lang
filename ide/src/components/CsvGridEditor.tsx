// ide/src/components/CsvGridEditor.tsx
import React, { useState } from "react";
import { Plus, Table, Code2 } from "lucide-react";

interface CsvGridEditorProps {
  fileName: string;
  content: string;
  onChange: (newContent: string) => void;
}

export const CsvGridEditor: React.FC<CsvGridEditorProps> = ({
  fileName,
  content,
  onChange,
}) => {
  const [rawMode, setRawMode] = useState(false);

  const lines = content.trim().split(/\r?\n/);
  const rows = lines.map((line) => line.split(","));
  const headers = rows[0] || [];
  const bodyRows = rows.slice(1);

  const updateCell = (rowIndex: number, colIndex: number, val: string) => {
    const nextRows = rows.map((r) => [...r]);
    if (!nextRows[rowIndex]) return;
    nextRows[rowIndex][colIndex] = val;
    onChange(nextRows.map((r) => r.join(",")).join("\n"));
  };

  const addRow = () => {
    const emptyRow = headers.map(() => "");
    const nextRows = [...rows, emptyRow];
    onChange(nextRows.map((r) => r.join(",")).join("\n"));
  };

  return (
    <div className="flex flex-col h-full bg-[var(--sol-base3)] text-[var(--sol-base00)]">
      <div className="h-7 px-3 bg-[var(--sol-base2)] border-b border-[var(--sol-border)] flex items-center justify-between text-[11px]">
        <code className="text-[var(--sol-base01)] font-mono" dir="rtl">
          {`جدول = اقرأ_جدول("${fileName}")`}
        </code>

        <div className="flex items-center gap-2">
          {!rawMode && (
            <button
              type="button"
              onClick={addRow}
              className="px-2 py-0.5 rounded bg-[var(--sol-base3)] hover:bg-[#e1dbcd] text-[var(--sol-base01)] border border-[var(--sol-border)] flex items-center gap-1 cursor-pointer"
            >
              <Plus className="w-3 h-3" />
              <span>صف جديد</span>
            </button>
          )}
          <button
            type="button"
            onClick={() => setRawMode(!rawMode)}
            className="px-2 py-0.5 rounded bg-[var(--sol-base3)] hover:bg-[#e1dbcd] text-[var(--sol-base01)] border border-[var(--sol-border)] flex items-center gap-1 cursor-pointer"
          >
            {rawMode ? (
              <Table className="w-3 h-3" />
            ) : (
              <Code2 className="w-3 h-3" />
            )}
            <span>{rawMode ? "جدول" : "نص خام"}</span>
          </button>
        </div>
      </div>

      {rawMode ? (
        <textarea
          value={content}
          onChange={(e) => onChange(e.target.value)}
          className="flex-1 w-full bg-[var(--sol-base3)] text-[var(--sol-base00)] p-4 font-mono text-sm outline-none resize-none"
          dir="rtl"
        />
      ) : (
        <div className="flex-1 overflow-auto p-4">
          <table className="w-full border-collapse text-xs">
            <thead>
              <tr className="bg-[var(--sol-base2)]">
                <th className="border border-[var(--sol-border)] px-2 py-1.5 w-10 text-center text-[var(--sol-base1)]">
                  #
                </th>
                {headers.map((h, colIdx) => (
                  <th
                    key={colIdx}
                    className="border border-[var(--sol-border)] p-0"
                  >
                    <input
                      value={h}
                      onChange={(e) => updateCell(0, colIdx, e.target.value)}
                      className="w-full bg-transparent px-2.5 py-1.5 font-bold text-[var(--sol-base01)] focus:bg-[var(--sol-base3)] outline-none"
                    />
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {bodyRows.map((row, rIdx) => (
                <tr key={rIdx} className="hover:bg-[var(--sol-base2)]/50">
                  <td className="border border-[var(--sol-border)] px-2 py-1 text-center text-[var(--sol-base1)] font-mono">
                    {rIdx + 1}
                  </td>
                  {headers.map((_, cIdx) => (
                    <td
                      key={cIdx}
                      className="border border-[var(--sol-border)] p-0"
                    >
                      <input
                        value={row[cIdx] ?? ""}
                        onChange={(e) =>
                          updateCell(rIdx + 1, cIdx, e.target.value)
                        }
                        className="w-full bg-transparent px-2.5 py-1 text-[var(--sol-base00)] focus:bg-[var(--sol-base2)]/60 outline-none font-mono"
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
