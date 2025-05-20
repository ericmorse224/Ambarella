/**
 * AudioUploadForm.int.test.jsx
 * Integration test for the AudioUploadForm React component.
 * 
 * Author: Eric Morse
 * Date: May 11th 2025
 * 
 * Description:
 * This test file performs an integration test for the AudioUploadForm component.
 * It renders the component in a wrapper that manages file state,
 * simulates a user uploading a file and clicking the submit button,
 * and verifies that the `onSubmit` handler is invoked.
 * 
 * Key Features Tested:
 * - File selection via the file input.
 * - Enabling of the "Transcribe Audio" button after file selection.
 * - Correct invocation of the provided `onSubmit` handler on form submission.
 * 
 * Tech Stack: React, Testing Library
 */
import { render, screen, fireEvent } from '@testing-library/react';
import AudioUploadForm from '../../components/AudioUploadForm';
import React, { useState } from 'react';

// Test wrapper to manage local file state for the form.
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

// Integration test for AudioUploadForm
describe('AudioUploadForm (Integration)', () => {
    it('uploads a file and calls onSubmit', async () => {
        let submitCalled = false;
        render(
            <TestWrapper onSubmit={e => { e.preventDefault(); submitCalled = true; }} />
        );
        const input = screen.getByLabelText(/upload audio/i);
        const file = new File(['test-audio-content'], 'test.wav', { type: 'audio/wav' });
        fireEvent.change(input, { target: { files: [file] } });

        const button = screen.getByRole('button', { name: /transcribe audio/i });
        fireEvent.click(button);

        expect(submitCalled).toBe(true);
    }, 20000);
});
