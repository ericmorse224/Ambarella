import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';
import React from 'react';

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
        const fileInput = screen.getByLabelText(/Upload Audio/i);
        const file = new File(['dummy'], 'large.mp3', { type: 'audio/mpeg' });
        Object.defineProperty(file, 'size', { value: 11 * 1024 * 1024 });

        fireEvent.change(fileInput, { target: { files: [file] } });
        expect(window.alert).toHaveBeenCalledWith('File size exceeds 10MB limit');
    });

    test('fetches and processes audio correctly', async () => {
        render(<App />);
        const button = screen.getByRole('button', { name: /Transcribe Audio/i });

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
