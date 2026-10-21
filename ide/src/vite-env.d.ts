// ide/src/vite-env.d.ts
/// <reference types="vite/client" />

declare module "*.lark?raw" {
  const content: string;
  export default content;
}

declare module "*.py?raw" {
  const content: string;
  export default content;
}

declare module "https://*" {
  export const loadPyodide: (options?: Record<string, unknown>) => Promise<any>;
}
