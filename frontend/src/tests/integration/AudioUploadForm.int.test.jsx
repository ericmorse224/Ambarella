import { render, screen, fireEvent } from '@testing-library/react';
import AudioUploadForm from '../../components/AudioUploadForm';
import React, { useState } from 'react';

function TestWrapper({ onSubmit }) {
    const [file, setFile] = useState(null);
    return (
        <AudioUploadForm
            file={file}
            onFileChange={e => setFile(e.target.files[0])}
            onSubmit={onSubmit}
            isLoading={false}
            uploadAttempts={0}
        />
    );
}

describe('AudioUploadForm (Integration)', () => {
    it('uploads a file and calls onSubmit', async () => {
        let submitCalled = false;
        render(
            <TestWrapper onSubmit={e => { e.preventDefault(); submitCalled = true; }} />
        );
        const input = screen.getByLabelText(/upload audio/i);
        const file = new File(['test-audio-content'], 'test.wav', { type: 'audio/wav' });
        fireEvent.change(input, { target: { files: [file] } });

        // The button should now be enabled
        const button = screen.getByRole('button', { name: /transcribe audio/i });
        fireEvent.click(button);

        expect(submitCalled).toBe(true);
    }, 20000);
});
