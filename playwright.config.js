// playwright.config.js
module.exports = {
  testDir: './e2e',
  timeout: 30000,
  use: {
    headless: true,
    baseURL: 'http://localhost:3000',
    actionTimeout: 0,
  },
  projects: [
    { name: 'chromium' },
    { name: 'firefox' },
    { name: 'webkit' }
  ],
};
