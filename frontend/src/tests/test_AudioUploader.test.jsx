
import { render, fireEvent, waitFor } from '@testing-library/react';
import AudioUploader from '../components/AudioUploader.jsx';

describe('AudioUploader', () => {
    beforeEach(() => {
        global.fetch = vi.fn();
        window.alert = vi.fn();
    });

    const setup = () => {
        const utils = render(<AudioUploader />);
        const input = utils.container.querySelector('input[type="file"]');
        return { ...utils, input };
    };

    it('uploads a valid audio file and displays results', async () => {
        const mockTranscript = 'This is a test transcript.';
        const mockJson = {
            summary: ['Summary 1'],
            actions: ['Action 1'],
            decisions: ['Decision 1'],
        };

        fetch
            .mockResolvedValueOnce({ json: () => Promise.resolve({ transcript: mockTranscript }) })
            .mockResolvedValueOnce({ json: () => Promise.resolve(mockJson) });

        const { getByText, input, findByText } = setup();
        const file = new File(['dummy'], 'test.wav', { type: 'audio/wav' });

        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(getByText(/upload & transcribe/i));

        await findByText('Transcript');
        await findByText(mockTranscript);
        await findByText('Summary 1');
        await findByText('Action 1');
        await findByText('Decision 1');
    });

    it('shows alert if no file is selected', async () => {
        const { getByText } = setup();
        fireEvent.click(getByText(/upload & transcribe/i));
        expect(fetch).not.toHaveBeenCalled();
    });

    it('alerts when file is too large (>50MB)', async () => {
        const largeFile = new File([new ArrayBuffer(51 * 1024 * 1024)], 'large.wav', { type: 'audio/wav' });

        const { input, getByText } = setup();
        fireEvent.change(input, { target: { files: [largeFile] } });
        fireEvent.click(getByText(/upload & transcribe/i));

        await waitFor(() => {
            expect(window.alert).toHaveBeenCalledWith(expect.stringMatching(/too large/i));
        });
    });

    it('alerts if transcript is missing from server response', async () => {
        fetch.mockResolvedValueOnce({ json: () => Promise.resolve({}) });

        const { getByText, input } = setup();
        const file = new File(['dummy'], 'test.wav', { type: 'audio/wav' });

        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(getByText(/upload & transcribe/i));

        await waitFor(() => {
            expect(window.alert).toHaveBeenCalledWith(expect.stringMatching(/Transcription failed/i));
        });
    });

    it('alerts on network error during upload', async () => {
        fetch.mockRejectedValueOnce(new Error('Network Error'));

        const { getByText, input } = setup();
        const file = new File(['dummy'], 'test.wav', { type: 'audio/wav' });

        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(getByText(/upload & transcribe/i));

        await waitFor(() => {
            expect(window.alert).toHaveBeenCalledWith(expect.stringMatching(/Upload failed/i));
        });
    });

    it('alerts on summarization failure after successful transcript', async () => {
        fetch
            .mockResolvedValueOnce({ json: () => Promise.resolve({ transcript: 'Transcript here' }) })
            .mockRejectedValueOnce(new Error('LLM error'));

        const { getByText, input } = setup();
        const file = new File(['dummy'], 'test.wav', { type: 'audio/wav' });

        fireEvent.change(input, { target: { files: [file] } });
        fireEvent.click(getByText(/upload & transcribe/i));

        await waitFor(() => {
            expect(window.alert).toHaveBeenCalledWith(expect.stringMatching(/Summarization failed/i));
        });
    });
});
