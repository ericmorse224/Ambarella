import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // Optional: for aliasing imports like @/App
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './frontend/src/setupTests.js', // Optional setup file
    include: ['src/**/*.test.{js,jsx}'], // Ensures Vitest looks in src/
  },
});

