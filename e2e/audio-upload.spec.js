const { test, expect } = require('@playwright/test');

test('uploads audio and sees transcript', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.setInputFiles('input[type="file"]', 'frontend/src/tests/test_audio/All_Needs.wav');
  await page.click('button:has-text("Transcribe Audio")');

  // Wait for transcript heading or text to appear
  await expect(page.locator('text=Transcript')).toBeVisible({ timeout: 20000 });

  // Optionally, assert on transcript content
  // await expect(page.locator('pre')).toContainText('Bob needs to brush his teeth');
});
