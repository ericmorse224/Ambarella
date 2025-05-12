import { render, screen, fireEvent, waitFor ***REMOVED*** from '@testing-library/react';
import App from './App';
import axios from 'axios';
import { vi ***REMOVED*** from 'vitest';

vi.mock('axios');

describe('App Component', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    ***REMOVED***);

    test('renders title and file input', () => {
        render(<App />);
        expect(screen.getByText(/AI Meeting Summarizer/i)).toBeInTheDocument();

        const fileInput = screen.getByLabelText(/upload audio/i) || screen.getByRole('textbox');
        expect(fileInput).toBeInTheDocument();
    ***REMOVED***);

    test('alerts on large file upload', () => {
        window.alert = vi.fn(); // Mock window.alert

        render(<App />);
        const file = new File([''], 'big.mp3', { type: 'audio/mp3' ***REMOVED***);
        Object.defineProperty(file, 'size', { value: 30 * 1024 * 1024 ***REMOVED***); // 30MB

        const input = screen.getByLabelText(/upload audio/i);
        fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);

        expect(window.alert).toHaveBeenCalledWith('File too large! Max 25MB allowed.');
    ***REMOVED***);

    test('alerts on unsupported file type', () => {
        window.alert = vi.fn();

        render(<App />);
        const file = new File(['dummy'], 'test.txt', { type: 'text/plain' ***REMOVED***);

        const input = screen.getByLabelText(/upload audio/i);
        fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);

        expect(window.alert).toHaveBeenCalledWith('Unsupported file type! Please upload a valid audio file.');
    ***REMOVED***);

    test('processes audio and shows results', async () => {
        axios.post
            .mockResolvedValueOnce({ data: { transcript: 'Hello world' ***REMOVED*** ***REMOVED***) // /process-audio
            .mockResolvedValueOnce({
                data: {
                    summary: ['Summary 1'],
                    actions: ['Action 1'],
                    decisions: ['Decision 1'],
                ***REMOVED***,
            ***REMOVED***); // /process-json

        render(<App />);
        const file = new File(['dummy'], 'test.wav', { type: 'audio/wav' ***REMOVED***);
        const input = screen.getByLabelText(/upload audio/i);
        fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);

        fireEvent.click(screen.getByText(/Transcribe Audio/i));

        await waitFor(() => {
            expect(screen.getByText(/Summary 1/i)).toBeInTheDocument();
            expect(screen.getByText(/Action 1/i)).toBeInTheDocument();
            expect(screen.getByText(/Decision 1/i)).toBeInTheDocument();
        ***REMOVED***);
    ***REMOVED***);

    test('handles API error and shows error message', async () => {
        axios.post.mockRejectedValueOnce(new Error('Server down'));

        render(<App />);
        const file = new File(['dummy'], 'test.wav', { type: 'audio/wav' ***REMOVED***);
        const input = screen.getByLabelText(/upload audio/i);
        fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);

        fireEvent.click(screen.getByText(/Transcribe Audio/i));

        await waitFor(() => {
            expect(screen.getByText((content, element) =>
                element.tagName.toLowerCase() === 'div' && content.includes('Server down')
            )).toBeInTheDocument();
        ***REMOVED***);
    ***REMOVED***);
***REMOVED***);
