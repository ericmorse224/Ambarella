/**
 * AudioUploadForm.test.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 *
 * Description:
 * ---------------
 * Unit tests for the AudioUploadForm React component, which provides the user interface
 * for uploading audio files to be transcribed in the AI Meeting Summarizer frontend.
 * These tests verify that the file name is displayed correctly after a file is selected,
 * and that the "Transcribe Audio" button is correctly disabled if no file is selected.
 *
 * Test Coverage:
 * ---------------
 * - Verifies the file name is shown after user selects a file.
 * - Ensures the transcribe button is disabled when no file is selected.
 *
 * Usage:
 * ---------------
 * Run these tests using Vitest or Jest in your frontend test suite.
 */
import { render, screen, fireEvent } from '@testing-library/react';
import AudioUploadForm from '../../components/AudioUploadForm';

describe('AudioUploadForm', () => {
    test('shows file name after selecting a file', () => {
        const setFile = vi.fn();
        render(
            <AudioUploadForm
                file={null}
                onFileChange={setFile}
                onSubmit={() => {}}
                isLoading={false}
                uploadAttempts={0}
            />
        );
        const input = screen.getByLabelText(/Upload Audio/i);
        const file = new File(['audio'], 'audio.mp3', { type: 'audio/mpeg' });
        fireEvent.change(input, { target: { files: [file] } });
    });

    test('disable button if no file', () => {
        render(
            <AudioUploadForm
                file={null}
                onFileChange={() => {}}
                onSubmit={() => {}}
                isLoading={false}
                uploadAttempts={0}
            />
        );
        expect(screen.getByRole('button', { name: /transcribe audio/i })).toBeDisabled();
    });
});
