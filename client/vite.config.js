import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // Explicit development port
    strictPort: true // Prevent fallback to other ports
  },
  preview: {
    port: 4173, // Explicit preview port
    strictPort: true
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: true // Helpful for debugging production
  },
  base: '/', // Set this if deploying to subdirectory (e.g., '/app/')
  define: {
    'process.env': {} // Required for some libraries
  }
});