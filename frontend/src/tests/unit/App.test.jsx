import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../../App';

// Default mock for useMeetingState (most tests)
vi.mock('../../hooks/UseMeetingState', () => ({
    default: () => ({
        transcript: 'Transcript text',
        summary: ['Summary1', 'Summary2'],
        actions: [
            { action: 'Action1', owner: 'Owner1', datetime: '2025-06-01T10:00', included: true },
            { action: 'Action2', owner: 'Owner2', datetime: '2025-06-01T11:00', included: false }
        ],
        decisions: ['Decision1'],
        isLoading: false,
        uploadAttempts: 1,
        processAudio: vi.fn().mockResolvedValue(true),
        processTranscript: vi.fn().mockResolvedValue(true),
        setActions: vi.fn(),
        error: '',
    }),
}));

// Mock fetch for scheduling
global.fetch = vi.fn().mockImplementation((url, opts) => {
    if (url.endsWith('/schedule')) {
        return Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ success: true })
        });
    }
    return Promise.reject(new Error('Unknown endpoint'));
});

// Mock URL.createObjectURL for download tests
global.URL.createObjectURL = vi.fn(() => 'blob:mock');

describe('App', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('renders app header', () => {
        render(<App />);
        expect(screen.getByText(/AI Meeting Summarizer/i)).toBeInTheDocument();
    });

    test('shows file name after selecting a file', () => {
        render(<App />);
        const file = new File(['(test audio)'], 'test.mp3', { type: 'audio/mpeg' });
        const input = screen.getByLabelText(/Upload Audio/i);
        fireEvent.change(input, { target: { files: [file] } });
        expect(screen.getByText('Selected file: test.mp3')).toBeInTheDocument();
    });

    it('alerts for files over 25MB', () => {
        window.alert = vi.fn();
        render(<App />);
        const file = new File(['a'.repeat(26 * 1024 * 1024)], 'big.mp3', { type: 'audio/mpeg' });
        Object.defineProperty(file, 'size', { value: 26 * 1024 * 1024 });
        const input = screen.getByLabelText(/Upload Audio/i);
        fireEvent.change(input, { target: { files: [file] } });
        expect(window.alert).toHaveBeenCalledWith('File size exceeds 25MB limit');
    });

    it('alerts for non-audio file', () => {
        window.alert = vi.fn();
        render(<App />);
        const file = new File(['(not audio)'], 'test.txt', { type: 'text/plain' });
        const input = screen.getByLabelText(/Upload Audio/i);
        fireEvent.change(input, { target: { files: [file] } });
        expect(window.alert).toHaveBeenCalledWith('Unsupported file type! Please upload a valid audio file.');
    });

    it('renders transcript, summary, decisions, and review panel', () => {
        render(<App />);
        expect(screen.getByText('Transcript text')).toBeInTheDocument();
        expect(screen.getByText('Summary1')).toBeInTheDocument();
        expect(screen.getByText('Summary2')).toBeInTheDocument();
        expect(screen.getByText('Decision1')).toBeInTheDocument();
        // Multiple panels with this text, so use getAllByText and check at least one exists
        expect(screen.getAllByText(/Review and Schedule Actions/i).length).toBeGreaterThan(0);
    });

    it('calls schedule endpoint and shows success', async () => {
        render(<App />);
        const scheduleBtn = screen.getByTestId('schedule-actions');
        fireEvent.click(scheduleBtn);
        // Wait for status message to appear
        const status = await screen.findByRole('status');
        expect(status).toHaveTextContent(/events scheduled successfully/i);
    });

    it('shows error message if schedule fails', async () => {
        global.fetch.mockImplementationOnce(() =>
            Promise.resolve({
                ok: false,
                json: () => Promise.resolve({ error: 'Scheduling failed' }),
            })
        );
        render(<App />);
        const scheduleBtns = screen.getAllByText('Schedule Selected');
        fireEvent.click(scheduleBtns[0]);
        // Match the actual rendered error text
        await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent(/error scheduling events/i));
    });

    it('shows generic error if schedule throws', async () => {
        global.fetch.mockImplementationOnce(() => Promise.reject('fail'));
        render(<App />);
        const scheduleBtns = screen.getAllByText('Schedule Selected');
        fireEvent.click(scheduleBtns[0]);
        await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent(/error scheduling events/i));
    });

    it('handles download of transcript and summary', () => {
        render(<App />);
        const createElementSpy = vi.spyOn(document, 'createElement');
        // Try download for transcript
        const transcriptDownload = screen.getByRole('button', { name: /Download Transcript/i });
        fireEvent.click(transcriptDownload);
        expect(createElementSpy).toHaveBeenCalledWith('a');
        // Try download for summary
        const summaryDownload = screen.getByRole('button', { name: /Download Summary/i });
        fireEvent.click(summaryDownload);
        expect(createElementSpy).toHaveBeenCalledWith('a');
        createElementSpy.mockRestore();
    });

    it('opens Nextcloud dashboard on connect button click', () => {
        window.open = vi.fn();
        render(<App />);
        const connectButton = screen.getByRole('button', { name: /Connect to Nextcloud/i });
        fireEvent.click(connectButton);
        expect(window.open).toHaveBeenCalledWith('http://localhost:8080/apps/dashboard/', '_blank');
    });
});

// Clean up global mocks
afterAll(() => {
    global.URL.createObjectURL.mockRestore?.();
});
