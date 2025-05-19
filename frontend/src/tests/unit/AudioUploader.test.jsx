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
});
