// ide/src/types/ide.ts

export type FileType = "sad" | "csv";

export interface VirtualFile {
  name: string;
  type: FileType;
  content: string;
}

export interface RuntimeVariable {
  name: string;
  type: string;
  value: string;
}

export interface SerializedDataFrame {
  name: string;
  shape: [number, number];
  columns: string[];
  dtypes: Record<string, string>;
  rows: string[][];
}

export interface ExecutionResult {
  ok: boolean;
  stdout: string;
  error: string;
  error_line: number | null;
  python_code: string;
  charts: string[];
  variables: RuntimeVariable[];
  dataframes: Record<string, SerializedDataFrame>;
  executionTimeMs?: number;
}

export type WorkerRequest =
  | { type: "INIT" }
  | {
      type: "RUN";
      runId: string;
      code: string;
      files: Record<string, string>;
    };

export type WorkerResponse =
  | { type: "STATUS"; message: string; ready: boolean }
  | { type: "INIT_ERROR"; error: string }
  | { type: "RESULT"; runId: string; result: ExecutionResult };
