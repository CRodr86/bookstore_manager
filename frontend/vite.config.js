import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
    server: {
    // Listen on all interfaces
    host: '0.0.0.0',
    // Use port 5173
    port: 5173,  },
})
