// ide/src/worker/pyodideWorker.ts
// ide/src/worker/pyodideWorker.ts
import type {
  WorkerRequest,
  WorkerResponse,
  ExecutionResult,
} from "../types/ide";

// Vite bundles the live text of your ../lang/ files directly—zero 404 fetch issues!
import initPy from "@lang/__init__.py?raw";
import grammarLark from "@lang/grammar.lark?raw";
import mappingsPy from "@lang/mappings.py?raw";
import checkerPy from "@lang/checker.py?raw";
import transpilerPy from "@lang/transpiler.py?raw";
import stdlibPy from "@lang/stdlib.py?raw";
import errorsPy from "@lang/errors.py?raw";

const EDU_PACKAGE_FILES: Record<string, string> = {
  "__init__.py": initPy,
  "grammar.lark": grammarLark,
  "mappings.py": mappingsPy,
  "checker.py": checkerPy,
  "transpiler.py": transpilerPy,
  "stdlib.py": stdlibPy,
  "errors.py": errorsPy,
};

let pyodideInstance: any = null;

function post(msg: WorkerResponse) {
  self.postMessage(msg);
}

async function initPyodide() {
  try {
    post({
      type: "STATUS",
      message: "⏳ ١/٣ جاري تشغيل محرك Pyodide...",
      ready: false,
    });

    // Dynamically import Pyodide ESM from CDN inside the Web Worker
    const { loadPyodide } = await import(
      /* @vite-ignore */ "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.mjs"
    );

    pyodideInstance = await loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/",
    });

    post({
      type: "STATUS",
      message: "⏳ ٢/٣ جاري تحميل Pandas و Matplotlib و Lark...",
      ready: false,
    });
    await pyodideInstance.loadPackage(["micropip", "pandas", "matplotlib"]);
    const micropip = pyodideInstance.pyimport("micropip");
    await micropip.install("lark");

    post({
      type: "STATUS",
      message: "⏳ ٣/٣ جاري ربط حزمة اللغة (lang/)...",
      ready: false,
    });
    pyodideInstance.FS.mkdirTree("/home/pyodide/lang");

    for (const [filename, content] of Object.entries(EDU_PACKAGE_FILES)) {
      pyodideInstance.FS.writeFile(`/home/pyodide/lang/${filename}`, content, {
        encoding: "utf8",
      });
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
    if (!pyodideInstance) return;
    const startTime = performance.now();

    try {
      // 1. Write all virtual files (.csv and .sad) into /home/pyodide/
      for (const [filename, content] of Object.entries(data.files)) {
        const fullPath = `/home/pyodide/${filename}`;
        const lastSlash = fullPath.lastIndexOf("/");
        if (lastSlash > 0) {
          pyodideInstance.FS.mkdirTree(fullPath.slice(0, lastSlash));
        }
        pyodideInstance.FS.writeFile(fullPath, content, { encoding: "utf8" });
      }

      // 2. Execute student code
      pyodideInstance.globals.set("_USER_SOURCE_CODE", data.code);
      const pyProxy = await pyodideInstance.runPythonAsync(`
execute_educational_code(_USER_SOURCE_CODE)
      `);

      const rawJsResult = pyProxy.toJs({ dict_converter: Object.fromEntries });
      pyProxy.destroy();

      const elapsed = Math.round(performance.now() - startTime);

      const result: ExecutionResult = {
        ok: Boolean(rawJsResult.ok),
        stdout: String(rawJsResult.stdout || ""),
        error: String(rawJsResult.error || ""),
        error_line: rawJsResult.error_line
          ? Number(rawJsResult.error_line)
          : null,
        python_code: String(rawJsResult.python_code || ""),
        charts: Array.isArray(rawJsResult.charts) ? rawJsResult.charts : [],
        variables: Array.isArray(rawJsResult.variables)
          ? rawJsResult.variables
          : [],
        dataframes: rawJsResult.dataframes || {},
        executionTimeMs: elapsed,
      };

      post({ type: "RESULT", runId: data.runId, result });
    } catch (err: any) {
      post({
        type: "RESULT",
        runId: data.runId,
        result: {
          ok: false,
          stdout: "",
          error: `❌ خطأ داخلي في بيئة التشغيل:\n${err?.message || String(err)}`,
          error_line: null,
          python_code: "",
          charts: [],
          variables: [],
          dataframes: {},
        },
      });
    }
  }
};
