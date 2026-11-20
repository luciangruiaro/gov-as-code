import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// ADR-004 law 5: the web app serves on 47101.
export default defineConfig({
  plugins: [react()],
  server: { port: 47101, strictPort: true },
})
