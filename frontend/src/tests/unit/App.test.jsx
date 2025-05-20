// File: App.test.jsx
// Author: Eric Morse
// Date: May 11th, 2025
//
// Unit tests for the main App component of the AI Meeting Summarizer frontend.
// This test suite ensures proper rendering, validation, dark mode, error handling,
// download logic, and correct integration with mocked state and handlers.
// Uses Vitest and React Testing Library.
// ----------------------------------------------------------------------------

/**
 * Mock the useMeetingState custom hook.
 * This prevents side effects and allows full control over the app state in tests.
 */
vi.mock('../../hooks/UseMeetingState', () => ({
    __esModule: true,
    default: vi.fn()
}));

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../../App';
import useMeetingState from '../../hooks/UseMeetingState';

// Set up a default mock implementation for useMeetingState for most tests
beforeEach(() => {
    useMeetingState.mockImplementation(() => ({
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
        scheduleError: '',
    }));
});

// Mock URL.createObjectURL globally for download tests
global.URL.createObjectURL = vi.fn(() => 'blob:mock');

/**
 * Main App test suite.
 */
describe('App', () => {
    beforeEach(() => {
        vi.resetModules();
        vi.clearAllMocks();
    });

    it('renders app header', () => {
        render(<App />);
        // Checks that the main page heading is present
        const heading = screen.getByRole('heading', { level: 1, name: /AI Meeting Summarizer/i });
        expect(heading).toBeInTheDocument();
    });

    it('shows file name after selecting a file', () => {
        render(<App />);
        const file = new File(['(test audio)'], 'test.mp3', { type: 'audio/mpeg' });
        const input = screen.getByLabelText(/Upload Audio/i);
        fireEvent.change(input, { target: { files: [file] } });
        expect(screen.getByText((content, node) => node.textContent === 'Selected file: test.mp3')).toBeInTheDocument();
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
    });

    it('handles download of transcript and summary', () => {
        render(<App />);
        const createElementSpy = vi.spyOn(document, 'createElement');
        // Download transcript
        const transcriptDownload = screen.getByRole('button', { name: /Download Transcript/i });
        fireEvent.click(transcriptDownload);
        expect(createElementSpy).toHaveBeenCalledWith('a');
        // Download summary
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

    it('toggles dark mode', () => {
        render(<App />);
        const toggle = screen.getByLabelText(/toggle dark mode/i);
        expect(document.documentElement.classList.contains('dark')).toBe(false);
        fireEvent.click(toggle);
        expect(document.documentElement.classList.contains('dark')).toBe(true);
        fireEvent.click(toggle);
        expect(document.documentElement.classList.contains('dark')).toBe(false);
    });

    it('disables analyze transcript button while loading', () => {
        useMeetingState.mockImplementation(() => ({
            transcript: 'Transcript text',
            summary: [],
            actions: [],
            decisions: [],
            isLoading: true,
            uploadAttempts: 1,
            processAudio: vi.fn(),
            processTranscript: vi.fn(),
            setActions: vi.fn(),
            error: '',
            scheduleError: ''
        }));
        render(<App />);
        expect(screen.getByRole('button', { name: /analyze transcript/i })).toBeDisabled();
    });

    it('renders error alert when error is returned from hook', () => {
        useMeetingState.mockImplementation(() => ({
            transcript: '',
            summary: [],
            actions: [],
            decisions: [],
            isLoading: false,
            uploadAttempts: 1,
            processAudio: vi.fn(),
            processTranscript: vi.fn(),
            setActions: vi.fn(),
            error: 'Critical error!',
            scheduleError: ''
        }));
        render(<App />);
        expect(screen.getByRole('alert')).toHaveTextContent(/critical error/i);
    });

    it('does not render transcript, summary, or decisions if state is empty', () => {
        useMeetingState.mockImplementation(() => ({
            transcript: '',
            summary: [],
            actions: [],
            decisions: [],
            isLoading: false,
            uploadAttempts: 1,
            processAudio: vi.fn(),
            processTranscript: vi.fn(),
            setActions: vi.fn(),
            error: '',
            scheduleError: ''
        }));
        render(<App />);
        expect(screen.queryByText(/transcript:/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/summary:/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/decisions:/i)).not.toBeInTheDocument();
    });
});

// Clean up global mocks after all tests are finished
afterAll(() => {
    global.URL.createObjectURL.mockRestore?.();
});
