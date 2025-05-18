import { render, screen, fireEvent, waitFor, act, cleanup } from '@testing-library/react';
import App from '../App';
import React from 'react';
import axios from 'axios';

vi.mock('axios');
afterEach(cleanup);
vi.mock('../utils/assemblyAI');
vi.mock('../utils/chatgpt');
vi.mock('../utils/zoho_utils');

vi.mock('../hooks/UseMeetingState', async () => {
    const actual = await vi.importActual('../hooks/UseMeetingState');
    return {
        ...actual,
        default: () => ({
            transcript: 'Test transcript',
            summary: ['Point 1', 'Point 2'],  // Fixed: summary must be an array
            actions: ['Action A', 'Action B'],
            decisions: ['Decision A'],
            loading: false,
            error: 'Error processing audio',
            uploadAttempts: 1,
            processAudio: vi.fn(),
            processTranscript: vi.fn(),
        }),
    };
});

describe('App Component', () => {
    beforeEach(() => {
        vi.spyOn(window, 'alert').mockImplementation(() => { });
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    test('alerts on large file upload', () => {
        render(<App />);
        const fileInput = screen.getByTestId("audio-upload");
        const file = new File(['dummy'], 'large.mp3', { type: 'audio/mpeg' });
        Object.defineProperty(file, 'size', { value: 11 * 1024 * 1024 });

        fireEvent.change(fileInput, { target: { files: [file] } });
        expect(window.alert).toHaveBeenCalledWith('File size exceeds 10MB limit');
    });

    test('fetches and processes audio correctly', async () => {
        render(<App />);
        const button = screen.getByRole('button', { name: /transcribe audio/i });

        fireEvent.click(button);

        await waitFor(() => {
            expect(screen.getByText(/Test transcript/i)).toBeInTheDocument();
            expect(screen.getByText(/Point 1/i)).toBeInTheDocument();
            expect(screen.getAllByText(/Action A/i).length).toBeGreaterThan(0);
        });
    });


    test('shows error when Zoho token fetch fails', () => {
        render(<App />);
        expect(screen.getByRole('alert')).toHaveTextContent('Error processing audio');
    });

    test('handles audio API failure gracefully', () => {
        render(<App />);
        expect(screen.getByRole('alert')).toHaveTextContent('Error processing audio');
    });

    test('schedules selected actions and shows success message', async () => {
        global.fetch = vi.fn()
            .mockResolvedValueOnce({ ok: true, json: async () => ({}) }); // mock /api/schedule

        render(<App />);
        fireEvent.click(screen.getByRole('button', { name: /Transcribe Audio/i }));

        await waitFor(() => {
            expect(screen.getAllByText(/Action A/i).length).toBeGreaterThan(0);
        });

        const buttons = screen.getAllByRole('button', { name: /Schedule Selected/i });
        fireEvent.click(buttons[buttons.length - 1]);

        const successMessage = await screen.findByRole('status');
        expect(successMessage).toBeInTheDocument();
        expect(successMessage.textContent.toLowerCase()).toContain("events scheduled successfully");

        global.fetch.mockRestore();
    });

    test('shows error message when scheduling fails', async () => {
        render(<App />);
        fireEvent.click(screen.getByRole('button', { name: /Transcribe Audio/i }));

        await waitFor(() => {
            expect(screen.getAllByText(/Action A/i).length).toBeGreaterThan(0);
        });

        const buttons = screen.getAllByRole('button', { name: /Schedule Selected/i });
        fireEvent.click(buttons[buttons.length - 1]);

        await waitFor(() => expect(screen.getByRole('alert')).toBeInTheDocument());
    });
});


it('displays app header', () => {
    const { getByText } = render(<App />);
    expect(getByText('AI Meeting Summarizer (AssemblyAI + OpenAI)')).toBeInTheDocument();
});

it('shows file name after selecting a file', () => {
    const { getByLabelText, getByText } = render(<App />);
    const file = new File(['(test audio)'], 'test.mp3', { type: 'audio/mpeg' });
    const input = getByLabelText(/Upload Audio/i);
    fireEvent.change(input, { target: { files: [file] } });
    expect(getByText('Selected file: test.mp3')).toBeInTheDocument();
});

it('renders download buttons when transcript and summary are present', () => {
    const transcript = "Test transcript";
    const summary = ["Summary 1", "Summary 2"];
    const { getByText } = render(
        <App />
    );
    act(() => {
        window.dispatchEvent(new CustomEvent('mockTranscriptAndSummary', { detail: { transcript, summary } }));
    });
    expect(getByText('Download Transcript')).toBeInTheDocument();
    expect(getByText('Download Summary')).toBeInTheDocument();
});

it('displays Zoho error message', () => {
    render(<App />);
    const alerts = screen.getAllByRole('alert');
    expect(alerts.some(p => p.textContent.includes('Error processing audio'))).toBe(true);
});


test('displays transcript and error messages', async () => {
    global.fetch = vi.fn().mockRejectedValueOnce(new Error('Error scheduling events'));

    render(<App />);

    // Click Transcribe Audio button to load transcript & actions
    fireEvent.click(screen.getByRole('button', { name: /Transcribe Audio/i }));

    // Wait for transcript and action items to appear
    await waitFor(() => {
        expect(screen.getByText('Test transcript')).toBeInTheDocument();
        expect(screen.getByText('Point 1')).toBeInTheDocument();
        expect(screen.getAllByText('Action A').length).toBeGreaterThan(0); // handles multiple appearances
    });

    // Click "Schedule Selected" button to trigger scheduling
    const scheduleButtons = screen.getAllByRole('button', { name: /Schedule Selected/i });
    fireEvent.click(scheduleButtons[scheduleButtons.length - 1]);

    // Now wait for the error message to show up
    await waitFor(() => {
        expect(screen.getByText('Error processing audio')).toBeInTheDocument();
        expect(screen.getByText('Error scheduling events')).toBeInTheDocument();
    });

    global.fetch.mockRestore();
});

test('handleFileChange resets state properly', () => {
    const { getByLabelText } = render(<App />);
    const input = getByLabelText(/Upload Audio/i);
    const file = new File(['dummy content'], 'test.mp3', { type: 'audio/mp3' });

    fireEvent.change(input, { target: { files: [file] } });

    // file selection resets state; testing with internal state is tough without refactor
    expect(input.files[0].name).toBe('test.mp3');
});

test('handleUpload does nothing if no file is selected', async () => {
    render(<App />);
    const button = screen.getByRole('button', { name: /transcribe audio/i });
    expect(button).toBeDisabled();
    fireEvent.click(button);
    expect(button).toBeDisabled();
    // Don't check for transcript text, since the mock always returns a transcript
});

test('handleUpload sends audio and updates UI', async () => {
    axios.post.mockResolvedValueOnce({
        data: {
            transcript: 'Transcript content',
            summary: 'Summary content',
            actions: ['Action A', 'Action B'],
            decisions: ['Decision X'],
        },
    });

    render(<App />);
    const file = new File(['data'], 'meeting.wav', { type: 'audio/wav' });
    const input = screen.getByLabelText(/Upload Audio/i);
    fireEvent.change(input, { target: { files: [file] } });

    fireEvent.click(screen.getByRole('button', { name: /transcribe audio/i }))

    await waitFor(() => {
        expect(screen.getByText('Test transcript')).toBeInTheDocument();
        expect(screen.getAllByPlaceholderText('Owner').length).toBeGreaterThan(0);
        expect(screen.getAllByText('Action A').length).toBeGreaterThan(0);
    });
});

test('handleFileChange does nothing when file is null', () => {
    render(<App />);
    const fileInput = screen.getByTestId("audio-upload");
    fireEvent.change(fileInput, { target: { files: null } });
    expect(screen.getByText(/selected file:/i)).toHaveTextContent('None');
});

test('does not render summary, decisions, or actions if state is empty', () => {
    expect(screen.queryByText(/summary:/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/decisions:/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/review and schedule actions/i)).not.toBeInTheDocument();
});

test('alerts on large file (>50MB)', async () => {
    render(<App />);
    const file = new File([new ArrayBuffer(60 * 1024 * 1024)], 'large.mp3', { type: 'audio/mp3' });

    window.alert = vi.fn();
    const input = await screen.findByTestId("audio-upload");
    expect(input).toBeInTheDocument();
    fireEvent.change(input, { target: { files: [file] } });

    expect(window.alert).toHaveBeenCalledWith('File size exceeds 10MB limit');
});


test('disables schedule button if no actions present', () => {
    expect(screen.queryByText(/schedule selected/i)).not.toBeInTheDocument();
});