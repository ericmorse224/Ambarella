const { test, expect } = require('@playwright/test');
const path = require('path');
const fs = require('fs');
const debugLogFile = path.resolve(__dirname, 'pw-debug.txt');

function logToFile(...args) {
  fs.appendFileSync(
    debugLogFile,
    `[${new Date().toISOString()}] ${args.map(String).join(' ')}\n`
  );
}

test('uploads audio and sees transcript or error, and verifies actions', async ({ page }) => {
  await page.goto('http://localhost:3000');
  logToFile('Page loaded');
  const audioFilePath = path.resolve(__dirname, '../frontend/src/tests/test_audio/All_Needs.wav');
  logToFile('Audio file path:', audioFilePath, fs.existsSync(audioFilePath));
  await page.setInputFiles('input[type="file"]', audioFilePath);
  logToFile('File set in input');
  await page.click('button:has-text("Transcribe Audio")');
  logToFile('Clicked transcribe');

  let transcriptAppeared = false;
  let alertAppeared = false;
  let transcriptContent = '';
  let actionsText = '';

  // Wait up to 20 seconds for either transcript or error alert
  try {
    await Promise.any([
      page.locator('text=Transcript').waitFor({ state: 'visible', timeout: 20000 }).then(async () => {
        transcriptAppeared = true;
        logToFile('Transcript appeared!');
        // Now check transcript content
        transcriptContent = await page.locator('pre').innerText();
        logToFile('Transcript content:', transcriptContent);
        // Assert on expected content (edit as needed!)
        expect(transcriptContent).toContain('Bob needs to brush his teeth');
        // Check that at least one action item is visible (adapt selector as needed!)
        actionsText = await page.locator('text=Action').first().innerText();
        logToFile('Action item found:', actionsText);
        // Optionally, assert specific action content
        expect(actionsText.toLowerCase()).toContain('brush his teeth');
      }),
      page.locator('[role=alert]').waitFor({ state: 'visible', timeout: 20000 }).then(async () => {
        alertAppeared = true;
        const alertText = await page.locator('[role=alert]').innerText();
        logToFile('Error alert appeared:', alertText);
        // Optionally, assert on error text
        expect(alertText.toLowerCase()).toContain('error');
      })
    ]);
  } catch (e) {
    logToFile('Neither transcript nor error appeared in DOM within timeout.');
    await page.screenshot({ path: 'playwright-fail.png' });
    logToFile('Screenshot taken at failure');
    logToFile('HTML:', await page.content());
    throw e;
  }

  // Final assert: either transcript or alert must appear!
  if (!transcriptAppeared && !alertAppeared) {
    throw new Error('Neither transcript nor error message rendered');
  }
});
