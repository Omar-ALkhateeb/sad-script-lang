// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import path from "path";
import fs from "fs";

// Automatically finds grammar.lark whether ide/ is inside lang/ or next to lang/
const langPath = fs.existsSync(path.resolve(__dirname, "../grammar.lark"))
  ? path.resolve(__dirname, "..")
  : path.resolve(__dirname, "../lang");

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    fs: {
      allow: ["..", "../.."],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@lang": langPath,
    },
  },
  worker: {
    format: "es",
  },
});
