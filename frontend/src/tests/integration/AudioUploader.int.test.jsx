import { render, screen, fireEvent } from '@testing-library/react';
import AudioUploader from '../../components/AudioUploader.jsx';
import fs from 'fs';
import path from 'path';

// Utility function to log messages to file with a timestamp
const logFile = path.resolve(__dirname, 'debug-log.txt');
function logToFile(...args) {
    fs.appendFileSync(
        logFile,
        `[${new Date().toISOString()}] ${args.map(String).join(' ')}\n`
    );
}

describe('AudioUploader (Integration Test)', () => {
    it('uploads a valid audio file and displays transcript or error from backend', async () => {
        logToFile('TEST START');
        render(<AudioUploader />);
        logToFile('Component rendered');
        const input = screen.getByLabelText(/upload audio/i);

        const audioPath = path.resolve(__dirname, '../test_audio/All_Needs.wav');
        const audioData = fs.readFileSync(audioPath);
        const file = new File([audioData], 'All_Needs.wav', { type: 'audio/wav' });
        logToFile('Audio file loaded:', audioPath);

        fireEvent.change(input, { target: { files: [file] } });
        logToFile('File input changed (file selected)');

        fireEvent.click(screen.getByRole('button', { name: /upload|transcribe/i }));
        logToFile('Upload button clicked');

        let transcriptHeader = null, alertMessage = null;

        try {
            transcriptHeader = await screen.findByText(/transcript/i, {}, { timeout: 15000 });
            logToFile('===TRANSCRIPT FOUND===');
        } catch {
            logToFile('Transcript header NOT found');
        }
        try {
            alertMessage = await screen.findByRole('alert', {}, { timeout: 10000 });
            if (alertMessage) {
                logToFile('===ALERT MESSAGE===', alertMessage.textContent);
            }
        } catch {
            logToFile('Alert message NOT found');
        }

        if (transcriptHeader) {
            expect(transcriptHeader).toBeInTheDocument();
            logToFile('TEST PASS: Transcript rendered');
        } else if (alertMessage) {
            expect(alertMessage).toBeInTheDocument();
            logToFile('TEST PASS: Error alert rendered');
        } else {
            logToFile('TEST FAIL: Neither transcript nor error message rendered');
            throw new Error('Neither transcript nor error message rendered');
        }
    }, 60000);
});
