import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: "0.0.0.0",
    proxy: {
      "/api/v1/agents/simple-agent": "http://localhost:8000",
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src")
    }
  },
})
