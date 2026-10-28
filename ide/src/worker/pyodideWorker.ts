// ide/src/worker/pyodideWorker.ts
import { WorkerRequest, WorkerResponse, ExecutionResult } from "../types/ide";

// Bundle all .py and .lark files in lang/ and its subfolders
const rawLangFiles = import.meta.glob(
  [
    "@lang/**/*.py",
    "@lang/**/*.lark",
    "../../../lang/**/*.py",
    "../../../lang/**/*.lark",
  ],
  { query: "?raw", import: "default", eager: true },
) as Record<string, string>;

let pyodideInstance: any = null;

function post(msg: WorkerResponse) {
  self.postMessage(msg);
}

async function initPyodide() {
  try {
    post({
      type: "STATUS",
      message: "⏳ ١/٣ جاري تشغيل محرك WebAssembly...",
      ready: false,
    });

    const { loadPyodide } = await import(
      /* @vite-ignore */ "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.mjs"
    );

    pyodideInstance = await loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/",
    });

    post({
      type: "STATUS",
      message: "⏳ ٢/٣ جاري تحميل المكتبات القياسية...",
      ready: false,
    });
    await pyodideInstance.loadPackage(["micropip", "pandas", "matplotlib"]);
    const micropip = pyodideInstance.pyimport("micropip");
    await micropip.install("lark==1.2.2");

    post({
      type: "STATUS",
      message: "⏳ ٣/٣ جاري تهيئة مترجم صادسكربت...",
      ready: false,
    });

    for (const [vitePath, content] of Object.entries(rawLangFiles)) {
      const normalized = vitePath.replace(/\\/g, "/");
      const marker = "/lang/";
      const idx = normalized.lastIndexOf(marker);
      const relPath =
        idx !== -1
          ? normalized.slice(idx + marker.length)
          : normalized.replace(/^.*?\//, "");
      const fullDest = `/home/pyodide/lang/${relPath}`;
      const parentDir = fullDest.slice(0, fullDest.lastIndexOf("/"));
      pyodideInstance.FS.mkdirTree(parentDir);
      pyodideInstance.FS.writeFile(fullDest, content, { encoding: "utf8" });
    }

    await pyodideInstance.runPythonAsync(`
import sys
if "/home/pyodide" not in sys.path:
    sys.path.insert(0, "/home/pyodide")
from lang import execute_educational_code
    `);

    post({ type: "STATUS", message: "✅ جاهز للتشغيل", ready: true });
  } catch (err: any) {
    post({ type: "INIT_ERROR", error: err?.message || String(err) });
  }
}

self.onmessage = async (event: MessageEvent<WorkerRequest>) => {
  const data = event.data;

  if (data.type === "INIT") {
    await initPyodide();
    return;
  }

  if (data.type === "RUN") {
    if (!pyodideInstance) {
      post({ type: "INIT_ERROR", error: "لم يتم تهيئة المحرك بعد." });
      return;
    }

    const t0 = performance.now();
    try {
      // Mount all virtual files (.sad, .csv) into /home/pyodide/
      for (const [filename, content] of Object.entries(data.files)) {
        const fullPath = `/home/pyodide/${filename}`;
        const lastSlash = fullPath.lastIndexOf("/");
        if (lastSlash > 0) {
          pyodideInstance.FS.mkdirTree(fullPath.slice(0, lastSlash));
        }
        pyodideInstance.FS.writeFile(fullPath, content, { encoding: "utf8" });
      }

      pyodideInstance.globals.set("_user_code", data.code);

      const jsonStr: string = await pyodideInstance.runPythonAsync(`
import json
from lang import execute_educational_code
_res = execute_educational_code(_user_code)
json.dumps(_res)
      `);

      const parsed: ExecutionResult = JSON.parse(jsonStr);
      parsed.executionTimeMs = Math.round(performance.now() - t0);

      post({ type: "RESULT", runId: data.runId, result: parsed });
    } catch (err: any) {
      post({
        type: "RESULT",
        runId: data.runId,
        result: {
          ok: false,
          stdout: "",
          error: `❌ خطأ في بيئة التشغيل:\n${err?.message || String(err)}`,
          error_line: null,
          python_code: "",
          charts: [],
          variables: [],
          dataframes: {},
          executionTimeMs: Math.round(performance.now() - t0),
        },
      });
    }
  }
};
