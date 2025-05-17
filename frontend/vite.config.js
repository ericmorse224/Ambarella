import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { configDefaults } from 'vitest/config';

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
    setupFiles: './frontend/src/setupTests.js',
    include: ['src/**/*.test.{js,jsx}'],
        coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov', 'json'],
      all: true,
      include: ['src/**/*.{js,jsx}'],
      exclude: [
        'src/**/*.test.{js,jsx}',
        'src/setupTests.js',
        'src/mocks/**',
        'src/index.js', 'src/reportWebVitals.js', 'src/vitest.setup.js',
      ],
    },
  },
});
