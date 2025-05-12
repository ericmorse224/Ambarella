import { defineConfig ***REMOVED*** from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // Optional: for aliasing imports like @/App
    ***REMOVED***,
  ***REMOVED***,
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './frontend/src/setupTests.js', // Optional setup file
    include: ['src/**/*.test.{js,jsx***REMOVED***'], // Ensures Vitest looks in src/
  ***REMOVED***,
***REMOVED***);
