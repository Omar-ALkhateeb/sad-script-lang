// ide/src/App.tsx (Update lines 1-35 and the Top Header Bar)
import React, { useState, useEffect, useRef, useCallback } from "react";
import {
  Play,
  Square,
  FileCode,
  FileSpreadsheet,
  X,
  PanelRight,
  PanelLeft,
  Download,
} from "lucide-react";
import { VirtualFile, ExecutionResult, WorkerResponse } from "./types/ide";
import { INITIAL_FILES, CURRICULUM_EXAMPLES } from "./data/examples";
import { HEADER_ASCII_LOGO } from "./data/branding";
import { ArabicEditor } from "./editor/ArabicEditor";
import { FileSidebar } from "./components/FileSidebar";
import { CsvGridEditor } from "./components/CsvGridEditor";
import { OutputWorkbench } from "./components/OutputWorkbench";

const STORAGE_KEY = "sadscript_vfs_v4";

export default function App() {
  const [files, setFiles] = useState<VirtualFile[]>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (!saved) return INITIAL_FILES;

      const parsed: VirtualFile[] = JSON.parse(saved);
      // Always keep custom user files, but sync INITIAL_FILES from examples.ts
      const initialNames = new Set(INITIAL_FILES.map((f) => f.name));
      const customFiles = parsed.filter(
        (f) => !initialNames.has(f.name) && !f.name.endsWith(".edu"),
      );
      return [...INITIAL_FILES, ...customFiles];
    } catch {
      return INITIAL_FILES;
    }
  });

  const [openTabs, setOpenTabs] = useState<string[]>([
    "main.sad",
    "fizzbuzz.sad",
    "students.csv",
  ]);
  const [activeFileName, setActiveFileName] = useState<string>("main.sad");
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(true);
  const [outputOpen, setOutputOpen] = useState<boolean>(true);

  const [sidebarWidth, setSidebarWidth] = useState<number>(210);
  const [outputWidth, setOutputWidth] = useState<number>(460);
  const draggingRef = useRef<"sidebar" | "output" | null>(null);

  const [workerReady, setWorkerReady] = useState<boolean>(false);
  const [statusMessage, setStatusMessage] = useState<string>(
    "جاري تهيئة بايثون...",
  );
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [result, setResult] = useState<ExecutionResult | null>(null);

  const workerRef = useRef<Worker | null>(null);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(files));
    } catch {
      // Ignore storage quota errors
    }
  }, [files]);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!draggingRef.current) return;
      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";

      if (draggingRef.current === "sidebar") {
        const nextWidth = window.innerWidth - e.clientX;
        setSidebarWidth(Math.max(160, Math.min(360, nextWidth)));
      } else if (draggingRef.current === "output") {
        const nextWidth = e.clientX;
        setOutputWidth(
          Math.max(260, Math.min(window.innerWidth - 340, nextWidth)),
        );
      }
    };

    const handleMouseUp = () => {
      if (draggingRef.current) {
        draggingRef.current = null;
        document.body.style.cursor = "";
        document.body.style.userSelect = "";
      }
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, []);

  const spawnWorker = useCallback(() => {
    if (workerRef.current) {
      workerRef.current.terminate();
    }
    setWorkerReady(false);
    const worker = new Worker(
      new URL("./worker/pyodideWorker.ts", import.meta.url),
      {
        type: "module",
      },
    );

    worker.onmessage = (e: MessageEvent<WorkerResponse>) => {
      const msg = e.data;
      if (msg.type === "STATUS") {
        setStatusMessage(msg.message);
        setWorkerReady(msg.ready);
      } else if (msg.type === "INIT_ERROR") {
        setStatusMessage("خطأ في التهيئة");
        setIsRunning(false);
      } else if (msg.type === "RESULT") {
        setIsRunning(false);
        setResult(msg.result);
      }
    };

    worker.postMessage({ type: "INIT" });
    workerRef.current = worker;
  }, []);

  useEffect(() => {
    spawnWorker();
    return () => workerRef.current?.terminate();
  }, [spawnWorker]);

  const activeFile = files.find((f) => f.name === activeFileName) || files[0];

  const handleSelectFile = (name: string) => {
    setActiveFileName(name);
    setOpenTabs((prev) => (prev.includes(name) ? prev : [...prev, name]));
  };

  const handleCloseTab = (e: React.MouseEvent, name: string) => {
    e.stopPropagation();
    if (openTabs.length <= 1) return;
    const nextTabs = openTabs.filter((t) => t !== name);
    setOpenTabs(nextTabs);
    if (activeFileName === name) {
      setActiveFileName(nextTabs[nextTabs.length - 1]);
    }
  };

  const updateActiveFileContent = (newContent: string) => {
    setFiles((prev) =>
      prev.map((f) =>
        f.name === activeFile.name ? { ...f, content: newContent } : f,
      ),
    );
  };

  const handleCreateFile = (
    name: string,
    type: "sad" | "csv",
    content = "",
  ) => {
    setFiles((prev) => {
      const exists = prev.some((f) => f.name === name);
      if (exists) {
        return prev.map((f) => (f.name === name ? { ...f, content } : f));
      }
      return [...prev, { name, type, content }];
    });
    handleSelectFile(name);
  };

  const handleRenameFile = (oldName: string, newName: string) => {
    const isCsv = newName.toLowerCase().endsWith(".csv");
    setFiles((prev) =>
      prev.map((f) =>
        f.name === oldName
          ? { ...f, name: newName, type: isCsv ? "csv" : "sad" }
          : f,
      ),
    );
    setOpenTabs((prev) => prev.map((t) => (t === oldName ? newName : t)));
    if (activeFileName === oldName) setActiveFileName(newName);
  };

  const handleDeleteFile = (name: string) => {
    setFiles((prev) => {
      const remaining = prev.filter((f) => f.name !== name);
      if (activeFileName === name && remaining.length > 0) {
        setActiveFileName(remaining[0].name);
      }
      return remaining;
    });
    setOpenTabs((prev) => prev.filter((t) => t !== name));
  };

  const handleRunCode = useCallback(() => {
    if (!workerRef.current || !workerReady || isRunning) return;

    const targetEduFile =
      activeFile.type === "sad"
        ? activeFile
        : files.find((f) => f.type === "sad") || activeFile;

    const vfsMap: Record<string, string> = {};
    for (const f of files) {
      vfsMap[f.name] = f.content;
    }

    setIsRunning(true);
    setOutputOpen(true);
    workerRef.current.postMessage({
      type: "RUN",
      runId: String(Date.now()),
      code: targetEduFile.content,
      files: vfsMap,
    });
  }, [workerReady, isRunning, activeFile, files]);

  const handleStopExecution = () => {
    setIsRunning(false);
    setStatusMessage("إعادة تشغيل المحرك...");
    spawnWorker();
  };

  const handleLoadExample = (key: string) => {
    const ex = CURRICULUM_EXAMPLES[key];
    if (!ex) return;
    setFiles((prev) =>
      prev.map((f) => (f.name === "main.sad" ? { ...f, content: ex.code } : f)),
    );
    handleSelectFile("main.sad");
    setResult(null);
  };

  return (
    <div
      className="flex flex-col h-screen w-screen bg-[var(--sol-base3)] text-[var(--sol-base00)] overflow-hidden"
      dir="rtl"
    >
      {/* 1. CLEAN TOP BAR */}
      <header className="h-9 bg-[var(--sol-base2)] border-b border-[var(--sol-border)] px-3 flex items-center justify-between gap-3 shrink-0 select-none">
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setSidebarOpen((o) => !o)}
            title="إظهار/إخفاء الملفات"
            className="p-1 rounded hover:bg-[#e1dbcd] text-[var(--sol-base01)] cursor-pointer"
          >
            <PanelRight className="w-4 h-4" />
          </button>
          <span className="font-bold text-xs text-[var(--sol-base01)]">
            عربي كود
          </span>
        </div>

        {/* Center Curriculum Selector */}
        <select
          onChange={(e) => handleLoadExample(e.target.value)}
          defaultValue="pandas_chart"
          className="bg-[var(--sol-base3)] border border-[var(--sol-border)] rounded px-2.5 py-0.5 text-xs text-[var(--sol-base01)] outline-none cursor-pointer"
        >
          {Object.entries(CURRICULUM_EXAMPLES).map(([key, item]) => (
            <option key={key} value={key}>
              {item.title}
            </option>
          ))}
        </select>

        {/* Left: Status + Run + Output Toggle */}
        <div className="flex items-center gap-2">
          <span className="text-[11px] text-[var(--sol-base1)] hidden sm:inline">
            {result?.executionTimeMs
              ? `${result.executionTimeMs} ms`
              : statusMessage}
          </span>

          {!isRunning ? (
            <button
              type="button"
              disabled={!workerReady}
              onClick={handleRunCode}
              className="px-3 py-1 rounded bg-[var(--sol-green)] hover:opacity-90 disabled:opacity-40 text-white font-bold text-xs flex items-center gap-1 cursor-pointer"
            >
              <Play className="w-3 h-3 fill-current" />
              <span>تشغيل</span>
            </button>
          ) : (
            <button
              type="button"
              onClick={handleStopExecution}
              className="px-3 py-1 rounded bg-[var(--sol-red)] text-white font-bold text-xs flex items-center gap-1 cursor-pointer"
            >
              <Square className="w-3 h-3 fill-current" />
              <span>إيقاف</span>
            </button>
          )}

          <button
            type="button"
            onClick={() => setOutputOpen((o) => !o)}
            title="إظهار/إخفاء المخرجات"
            className="p-1 rounded hover:bg-[#e1dbcd] text-[var(--sol-base01)] cursor-pointer"
          >
            <PanelLeft className="w-4 h-4" />
          </button>
        </div>
      </header>

      {/* 2. MAIN WORKSPACE */}
      <div className="flex-1 flex min-h-0 overflow-hidden">
        {sidebarOpen && (
          <>
            <div
              style={{ width: `${sidebarWidth}px` }}
              className="h-full shrink-0"
            >
              <FileSidebar
                files={files}
                activeFileName={activeFile.name}
                onSelectFile={handleSelectFile}
                onCreateFile={handleCreateFile}
                onRenameFile={handleRenameFile}
                onDeleteFile={handleDeleteFile}
              />
            </div>

            <div
              onMouseDown={() => {
                draggingRef.current = "sidebar";
              }}
              className="w-px bg-[var(--sol-border)] relative z-20 shrink-0 cursor-col-resize after:content-[''] after:absolute after:inset-y-0 after:-left-1.5 after:-right-1.5 hover:bg-[var(--sol-blue)] hover:w-0.5 transition-all"
            />
          </>
        )}

        {/* CENTER EDITOR */}
        <main className="flex-1 flex flex-col min-w-65 bg-[var(--sol-base3)]">
          {/* VS Code Tab Bar */}
          <div className="h-8 bg-[var(--sol-base2)] border-b border-[var(--sol-border)] flex items-center overflow-x-auto no-scrollbar shrink-0 select-none">
            {openTabs.map((tabName) => {
              const fileObj = files.find((f) => f.name === tabName);
              if (!fileObj) return null;
              const isTabActive = fileObj.name === activeFile.name;

              return (
                <div
                  key={fileObj.name}
                  onClick={() => setActiveFileName(fileObj.name)}
                  className={`group h-full px-3 flex items-center gap-1.5 text-xs border-l border-[var(--sol-border)] cursor-pointer shrink-0 ${
                    isTabActive
                      ? "bg-[var(--sol-base3)] text-[var(--sol-base01)] border-t-2 border-t-[var(--sol-blue)] font-semibold"
                      : "bg-[var(--sol-base2)] text-[var(--sol-base1)] hover:text-[var(--sol-base01)]"
                  }`}
                >
                  {fileObj.type === "csv" ? (
                    <FileSpreadsheet className="w-3.5 h-3.5 text-[var(--sol-green)] shrink-0" />
                  ) : (
                    <FileCode className="w-3.5 h-3.5 text-[var(--sol-blue)] shrink-0" />
                  )}
                  <span dir="ltr" className="font-mono text-[11px]">
                    {fileObj.name}
                  </span>
                  {openTabs.length > 1 && (
                    <button
                      type="button"
                      onClick={(e) => handleCloseTab(e, fileObj.name)}
                      className="opacity-0 group-hover:opacity-100 hover:bg-[#e1dbcd] rounded p-0.5 text-[var(--sol-base1)] hover:text-[var(--sol-red)] cursor-pointer"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  )}
                </div>
              );
            })}
          </div>

          <div className="flex-1 min-h-0">
            {activeFile.type === "csv" ? (
              <CsvGridEditor
                fileName={activeFile.name}
                content={activeFile.content}
                onChange={updateActiveFileContent}
              />
            ) : (
              <ArabicEditor
                fileName={activeFile.name}
                code={activeFile.content}
                onChange={updateActiveFileContent}
                onRun={handleRunCode}
                errorLine={result && !result.ok ? result.error_line : null}
                errorMessage={result && !result.ok ? result.error : ""}
              />
            )}
          </div>
        </main>

        {/* LEFT OUTPUT WORKBENCH */}
        {outputOpen && (
          <>
            <div
              onMouseDown={() => {
                draggingRef.current = "output";
              }}
              className="w-px bg-[var(--sol-border)] relative z-20 shrink-0 cursor-col-resize after:content-[''] after:absolute after:inset-y-0 after:-left-1.5 after:-right-1.5 hover:bg-[var(--sol-blue)] hover:w-0.5 transition-all"
            />

            <section
              style={{ width: `${outputWidth}px` }}
              className="h-full shrink-0 min-w-65"
            >
              <OutputWorkbench
                result={result}
                onClear={() => setResult(null)}
                onJumpToLine={(line) => {
                  if (activeFile.type !== "sad") {
                    const firstEdu = files.find((f) => f.type === "sad");
                    if (firstEdu) handleSelectFile(firstEdu.name);
                  }
                  setResult((prev) =>
                    prev ? { ...prev, error_line: line } : null,
                  );
                }}
              />
            </section>
          </>
        )}
      </div>
    </div>
  );
}
