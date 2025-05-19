import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../../App';

describe('App Integration', () => {
    it('uploads audio and schedules action with real backend', async () => {
        render(<App />);
        const file = new File(['test-audio-content'], 'test.wav', { type: 'audio/wav' });
        const input = screen.getByLabelText(/Upload Audio/i);

        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(screen.getByRole('button', { name: /Transcribe|Audio/i }));

        await screen.findByText(/transcript/i, {}, { timeout: 15000 });
        const scheduleBtn = await screen.findByText(/schedule selected/i, {}, { timeout: 10000 });
        fireEvent.click(scheduleBtn);
        const status = await screen.findByRole('status', {}, { timeout: 10000 });
        expect(status).toHaveTextContent(/events scheduled successfully/i);
    }, 20000);
});
