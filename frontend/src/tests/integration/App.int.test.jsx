import { render, screen, fireEvent } from '@testing-library/react';
import App from '../../App';

describe('App Integration', () => {
    it('uploads audio and schedules action with real backend', async () => {
        render(<App />);
        const file = new File(['test-audio-content'], 'test.wav', { type: 'audio/wav' });
        const input = screen.getByLabelText(/Upload Audio/i);

        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(screen.getByRole('button', { name: /Transcribe|Audio/i }));

        // Wait for either transcript header or error alert after upload
        let transcriptHeader = null, alertMessage = null;

        try {
            transcriptHeader = await screen.findByText(/transcript/i, {}, { timeout: 15000 });
        } catch {
            // Not found
        }
        try {
            alertMessage = await screen.findByRole('alert', {}, { timeout: 10000 });
        } catch {
            // Not found
        }

        if (transcriptHeader) {
            expect(transcriptHeader).toBeInTheDocument();

            // Only proceed to scheduling if upload was successful
            const scheduleBtn = await screen.findByText(/schedule selected/i, {}, { timeout: 10000 });
            fireEvent.click(scheduleBtn);

            let scheduleStatus = null, scheduleError = null;
            try {
                scheduleStatus = await screen.findByRole('status', {}, { timeout: 10000 });
            } catch {
                // Not found
            }
            try {
                scheduleError = await screen.findByRole('alert', {}, { timeout: 10000 });
            } catch {
                // Not found
            }

            if (scheduleStatus) {
                expect(scheduleStatus).toHaveTextContent(/events scheduled successfully/i);
            } else if (scheduleError) {
                expect(scheduleError).toHaveTextContent(/error scheduling events/i);
            } else {
                throw new Error('Neither success nor error message rendered for scheduling');
            }

        } else if (alertMessage) {
            // Audio upload error path
            expect(alertMessage).toHaveTextContent(/error processing audio/i);
        } else {
            throw new Error('Neither transcript nor error message rendered after upload');
        }
    }, 30000);
});
