import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import AudioUploader from '../../components/AudioUploader.jsx';

describe('AudioUploader (Integration Test)', () => {
    it('uploads a valid audio file and displays real results from backend', async () => {
        render(<AudioUploader />);
        const input = screen.getByLabelText(/upload audio/i);
        const file = new File(['test-audio-content'], 'test.wav', { type: 'audio/wav' });

        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(screen.getByRole('button', { name: /Transcribe|Audio/i }));

        const transcriptHeader = await screen.findByText(/transcript/i, {}, { timeout: 15000 });
        expect(transcriptHeader).toBeInTheDocument();
    }, 20000);
});
