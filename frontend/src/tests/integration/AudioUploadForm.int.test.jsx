import { render, screen, fireEvent } from '@testing-library/react';
import AudioUploadForm from '../../components/AudioUploadForm';

describe('AudioUploadForm (Integration)', () => {
    it('uploads a file and calls onSubmit (assumes real backend)', async () => {
        let submitCalled = false;
        render(
            <AudioUploadForm
                file={null}
                onFileChange={() => {}}
                onSubmit={() => { submitCalled = true; }}
                isLoading={false}
                uploadAttempts={0}
            />
        );
        const input = screen.getByLabelText(/Upload Audio/i);
        const file = new File(['test-audio-content'], 'test.wav', { type: 'audio/wav' });
        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(screen.getByRole('button', { name: /transcribe audio/i }));
        expect(submitCalled).toBe(true);
    }, 20000);
});
