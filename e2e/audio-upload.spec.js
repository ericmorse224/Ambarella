/**
 * File: audio-upload.spec.js
 * Author: Eric Morse
 * Date: May 11th, 2025
 * 
 * Description:
 * --------------
 * This Playwright end-to-end (E2E) test automates the process of uploading an audio file
 * to the AI Meeting Summarizer frontend, verifying the appearance of either the transcript 
 * or an error message, and checks for extracted actions. The test writes debug logs to 
 * pw-debug.txt for easier troubleshooting of failures.
 * 
 * Test Steps:
 * -----------
 * 1. Navigate to the frontend application (localhost:3000).
 * 2. Set the file input to a test WAV audio file.
 * 3. Click the "Transcribe Audio" button to trigger transcription.
 * 4. Wait up to 20 seconds for either a transcript or error alert to appear.
 * 5. If a transcript appears:
 *    - Assert expected content exists in the transcript.
 *    - Assert at least one action item is found and verify its content.
 * 6. If an error alert appears:
 *    - Assert the alert contains an error message.
 * 7. If neither appears, log debug information and fail the test.
 * 
 * Dependencies:
 * -------------
 * - Playwright test runner
 * - Node.js path and fs modules
 * - The test audio file should exist at '../frontend/src/tests/test_audio/All_Needs.wav'
 *
 * Note:
 * -----
 * - Update the file path and assertion content if the test audio or UI changes.
 */
const { test, expect } = require('@playwright/test');
const path = require('path');
const fs = require('fs');
const debugLogFile = path.resolve(__dirname, 'pw-debug.txt');

/**
 * Logs debug messages to the pw-debug.txt file with timestamps.
 * @param  {...any} args - Items to log (will be joined by space).
 */
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
