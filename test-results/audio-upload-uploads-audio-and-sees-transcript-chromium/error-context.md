# Test info

- Name: uploads audio and sees transcript
- Location: C:\Users\bandi\meeting-summary-dashboard\e2e\audio-upload.spec.js:3:1

# Error details

```
Error: expect.toBeVisible: Error: strict mode violation: locator('text=Transcript') resolved to 3 elements:
    1) <p role="alert" class="mt-2 text-sm text-center text-red-600">Error processing transcript</p> aka getByText('Error processing transcript')
    2) <h2 class="text-lg font-bold mt-4">Transcript:</h2> aka getByRole('heading', { name: 'Transcript:' })
    3) <button class="mt-2 bg-gray-700 text-white px-3 py-1 rounded">Download Transcript</button> aka getByRole('button', { name: 'Download Transcript' })

Call log:
  - expect.toBeVisible with timeout 20000ms
  - waiting for locator('text=Transcript')

    at C:\Users\bandi\meeting-summary-dashboard\e2e\audio-upload.spec.js:9:49
```

# Page snapshot

```yaml
- heading "AI Meeting Summarizer (AssemblyAI + OpenAI)" [level=1]
- button "Connect to Nextcloud"
- text: Upload Audio
- button "Upload Audio"
- paragraph: "Selected file: All_Needs.wav"
- button "Transcribe Audio"
- alert: Error processing transcript
- heading "Transcript:" [level=2]
- text: to watch dishes, bar means to brush his teeth, Frank needs to do something interesting.
- button "Download Transcript"
```

# Test source

```ts
   1 | const { test, expect } = require('@playwright/test');
   2 |
   3 | test('uploads audio and sees transcript', async ({ page }) => {
   4 |   await page.goto('http://localhost:3000');
   5 |   await page.setInputFiles('input[type="file"]', 'frontend/src/tests/test_audio/All_Needs.wav');
   6 |   await page.click('button:has-text("Transcribe Audio")');
   7 |
   8 |   // Wait for transcript heading or text to appear
>  9 |   await expect(page.locator('text=Transcript')).toBeVisible({ timeout: 20000 });
     |                                                 ^ Error: expect.toBeVisible: Error: strict mode violation: locator('text=Transcript') resolved to 3 elements:
  10 |
  11 |   // Optionally, assert on transcript content
  12 |   // await expect(page.locator('pre')).toContainText('Bob needs to brush his teeth');
  13 | });
  14 |
```