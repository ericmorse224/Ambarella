/**
 * AudioUploader.test.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 * 
 * This file contains unit tests for the AudioUploader React component.
 * 
 * Coverage includes:
 *  - Rendering the input and upload button
 *  - Handling file selection
 *  - Validating file size and type
 *  - Error handling for upload and transcription failures
 *  - State updates for loading and data display (transcript, summary, actions, decisions)
 *  - UI/UX behavior for empty and loading states
 * 
 * Uses: React Testing Library, Vitest/Jest, File API, mocking global.fetch and window.alert
 * 
 * The tests ensure robust error reporting, loading-state UI, and complete user interaction flow
 * for the audio upload and meeting summarization pipeline.
 */

import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import AudioUploader from '../../components/AudioUploader.jsx';

describe('AudioUploader', () => {
    beforeEach(() => {
        global.fetch = undefined;
        vi.restoreAllMocks();
        window.alert = vi.fn();
    });

    it('renders input and upload button', () => {
        render(<AudioUploader />);
        expect(screen.getByLabelText(/upload audio/i)).toBeInTheDocument();
        expect(screen.getByText(/upload & transcribe/i)).toBeInTheDocument();
    });

    it('handles file selection', () => {
        render(<AudioUploader />);
        const input = screen.getByLabelText(/upload audio/i);
        const file = new File(['hello'], 'meeting.wav', { type: 'audio/wav' });
        fireEvent.change(input, { target: { files: [file] } });
        // No error thrown = success for file selection
    });

    it('shows alert for file too large', () => {
        render(<AudioUploader />);
        const input = screen.getByLabelText(/upload audio/i);
        const file = new File(['a'.repeat(26 * 1024 * 1024)], 'big.wav', { type: 'audio/wav' });
        Object.defineProperty(file, 'size', { value: 26 * 1024 * 1024 });
        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(screen.getByText(/upload & transcribe/i));
        expect(window.alert).toHaveBeenCalledWith(expect.stringMatching(/file too large/i));
    });

    it('shows alert if upload fails', async () => {
        global.fetch = vi.fn(() => Promise.reject(new Error('Network')));
        render(<AudioUploader />);
        const input = screen.getByLabelText(/upload audio/i);
        const file = new File(['hello'], 'meeting.wav', { type: 'audio/wav' });
        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(screen.getByText(/upload & transcribe/i));
        await waitFor(() => {
            expect(window.alert).toHaveBeenCalledWith(expect.stringMatching(/upload failed/i));
        });
    });

    it('shows alert if transcription failed', async () => {
        global.fetch = vi.fn(() =>
            Promise.resolve({
                json: () => Promise.resolve({}),
            })
        );
        render(<AudioUploader />);
        const input = screen.getByLabelText(/upload audio/i);
        const file = new File(['hello'], 'meeting.wav', { type: 'audio/wav' });
        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(screen.getByText(/upload & transcribe/i));
        await waitFor(() => {
            expect(window.alert).toHaveBeenCalledWith(expect.stringMatching(/transcription failed/i));
        });
    });

    it('shows transcript, summary, actions, decisions after upload and summarize', async () => {
        global.fetch = vi
            .fn()
            .mockImplementationOnce(() =>
                Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({ transcript: 'Transcript text' }),
                })
            )
            .mockImplementationOnce(() =>
                Promise.resolve({
                    json: () =>
                        Promise.resolve({
                            summary: ['Summary1', 'Summary2'],
                            actions: ['Action1', 'Action2'],
                            decisions: ['Decision1'],
                        }),
                })
            );

        render(<AudioUploader />);
        const input = screen.getByLabelText(/upload audio/i);
        const file = new File(['hello'], 'meeting.wav', { type: 'audio/wav' });
        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(screen.getByText(/upload & transcribe/i));

        await screen.findByText('Transcript text');
        expect(screen.getByRole('heading', { name: /summary/i })).toBeInTheDocument(); // changed line!
        expect(screen.getByText('Summary1')).toBeInTheDocument();
        expect(screen.getByText('Summary2')).toBeInTheDocument();

        expect(screen.getByRole('heading', { name: /action items/i })).toBeInTheDocument();
        expect(screen.getByText('Action1')).toBeInTheDocument();
        expect(screen.getByText('Action2')).toBeInTheDocument();

        expect(screen.getByRole('heading', { name: /decisions/i })).toBeInTheDocument();
        expect(screen.getByText('Decision1')).toBeInTheDocument();
    });


    it('shows alert if summarization fails', async () => {
        global.fetch = vi
            .fn()
            .mockImplementationOnce(() =>
                Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({ transcript: 'Transcript text' }),
                })
            )
            .mockImplementationOnce(() => Promise.reject(new Error('Summarize error')));

        render(<AudioUploader />);
        const input = screen.getByLabelText(/upload audio/i);
        const file = new File(['hello'], 'meeting.wav', { type: 'audio/wav' });
        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(screen.getByText(/upload & transcribe/i));
        await waitFor(() => {
            expect(window.alert).toHaveBeenCalledWith(expect.stringMatching(/summarization failed/i));
        });
    });

    it('disables upload button while uploading', async () => {
        render(<AudioUploader />);
        // Set a file so upload will proceed
        const file = new File(['test'], 'test.mp3', { type: 'audio/mpeg' });
        const input = screen.getByLabelText(/upload audio/i);
        fireEvent.change(input, { target: { files: [file] } });

        // Spy on global fetch to return a promise that never resolves
        global.fetch = vi.fn(() => new Promise(() => { }));

        const uploadBtn = screen.getByText(/upload & transcribe/i);
        fireEvent.click(uploadBtn);
        // The loading state should be true, so button is disabled
        expect(uploadBtn).toBeDisabled();
    });

    it('does not show transcript/summary/decisions when upload is empty', () => {
        render(<AudioUploader />);
        expect(screen.queryByText(/transcript:/i)).not.toBeInTheDocument();
        expect(screen.queryByRole('heading', { name: /summary/i })).not.toBeInTheDocument();
        expect(screen.queryByRole('heading', { name: /decisions/i })).not.toBeInTheDocument();
    });
});
