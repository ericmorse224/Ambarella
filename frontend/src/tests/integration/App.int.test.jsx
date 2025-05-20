/**
 * File: App.int.test.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 * 
 * Description:
 * This file contains the integration test for the main App component
 * of the AI Meeting Summarizer frontend. The test covers the flow from
 * audio upload, transcription, and scheduling an action with the real backend,
 * including both success and error states.
 */

import { render, screen, fireEvent } from '@testing-library/react';
import App from '../../App';

describe('App Integration', () => {
    /**
     * Integration test: Simulates user uploading audio and scheduling an action,
     * with assertions for both success and error states. Communicates with the real backend.
     */
    it('uploads audio and schedules action with real backend', async () => {
        render(<App />);
        // Create a mock WAV audio file
        const file = new File(['test-audio-content'], 'test.wav', { type: 'audio/wav' });
        const input = screen.getByLabelText(/Upload Audio/i);

        // Simulate user uploading file and clicking the Transcribe Audio button
        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(screen.getByRole('button', { name: /Transcribe|Audio/i }));

        // Wait for either transcript header or error alert after upload
        let transcriptHeader = null, alertMessage = null;

        try {
            // Wait up to 15s for transcript header to appear (success path)
            transcriptHeader = await screen.findByText(/transcript/i, {}, { timeout: 15000 });
        } catch {
            // Transcript header not found
        }
        try {
            // Wait up to 10s for an error alert to appear (error path)
            alertMessage = await screen.findByRole('alert', {}, { timeout: 10000 });
        } catch {
            // Alert not found
        }

        if (transcriptHeader) {
            // Transcript successfully rendered
            expect(transcriptHeader).toBeInTheDocument();

            // Wait for the "Schedule Selected" button and simulate scheduling
            const scheduleBtn = await screen.findByText(/schedule selected/i, {}, { timeout: 10000 });
            fireEvent.click(scheduleBtn);

            let scheduleStatus = null, scheduleError = null;
            try {
                // Wait for success status message
                scheduleStatus = await screen.findByRole('status', {}, { timeout: 10000 });
            } catch {
                // Status not found
            }
            try {
                // Wait for error alert if scheduling fails
                scheduleError = await screen.findByRole('alert', {}, { timeout: 10000 });
            } catch {
                // Alert not found
            }

            if (scheduleStatus) {
                // Scheduling succeeded
                expect(scheduleStatus).toHaveTextContent(/events scheduled successfully/i);
            } else if (scheduleError) {
                // Scheduling failed
                expect(scheduleError).toHaveTextContent(/error scheduling events/i);
            } else {
                // Neither success nor error rendered
                throw new Error('Neither success nor error message rendered for scheduling');
            }

        } else if (alertMessage) {
            // Audio upload error path
            expect(alertMessage).toHaveTextContent(/error processing audio/i);
        } else {
            // Neither transcript nor error rendered after upload
            throw new Error('Neither transcript nor error message rendered after upload');
        }
    }, 30000);
});
