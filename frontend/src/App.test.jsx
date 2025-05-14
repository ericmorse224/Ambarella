import { render, screen, fireEvent ***REMOVED*** from '@testing-library/react';
import App from './App';
import axios from 'axios';
import { vi ***REMOVED*** from 'vitest';

vi.mock('axios');

describe('App Component', () => {
    beforeEach(() => {
        vi.resetAllMocks();
    ***REMOVED***);

    test('renders title and file input', () => {
        render(<App />);
        expect(screen.getByText(/AI Meeting Summarizer/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Upload Audio/i)).toBeInTheDocument();
    ***REMOVED***);

    test('alerts on large file upload', () => {
        window.alert = vi.fn();
        render(<App />);
        const input = screen.getByLabelText(/Upload Audio/i);

        const file = new File(['a'.repeat(26 * 1024 * 1024)], 'large.wav', {
            type: 'audio/wav',
        ***REMOVED***);

        fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);
        expect(window.alert).toHaveBeenCalledWith('File too large! Max 25MB allowed.');
    ***REMOVED***);

    test('alerts on unsupported file type', () => {
        window.alert = vi.fn();
        render(<App />);
        const input = screen.getByLabelText(/Upload Audio/i);

        const file = new File(['hello'], 'file.txt', {
            type: 'text/plain',
        ***REMOVED***);

        fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);
        expect(window.alert).toHaveBeenCalledWith('Unsupported file type! Please upload a valid audio file.');
    ***REMOVED***);

    test('processes audio and shows results', async () => {
        axios.post.mockImplementation((url) => {
            if (url.includes('process-audio')) {
                return Promise.resolve({ data: { transcript: 'Meeting notes here.' ***REMOVED*** ***REMOVED***);
            ***REMOVED***
            if (url.includes('process-json')) {
                return Promise.resolve({ data: { summary: ['Summary A'], actions: ['Action A'], decisions: ['Decision A'] ***REMOVED*** ***REMOVED***);
            ***REMOVED***
        ***REMOVED***);

        render(<App />);

        const file = new File(['dummy'], 'test.wav', { type: 'audio/wav' ***REMOVED***);
        const input = screen.getByLabelText(/Upload Audio/i);
        fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);
        fireEvent.click(screen.getByText(/Transcribe Audio/i));

        await screen.findByText('Transcript:');
        expect(screen.getByText('Transcript:')).toBeInTheDocument();
        expect(screen.getByText('Meeting notes here.')).toBeInTheDocument();
        expect(screen.getByText('Summary:')).toBeInTheDocument();
        expect(screen.getByText('Actions:')).toBeInTheDocument();
        expect(screen.getByText('Decisions:')).toBeInTheDocument();
    ***REMOVED***);

    /*test('handles API error and shows error message', async () => {
        axios.post.mockRejectedValueOnce(new Error('Server down'));

        render(<App />);
        const file = new File(['dummy'], 'test.wav', { type: 'audio/wav' ***REMOVED***);
        const input = screen.getByLabelText(/Upload Audio/i);
        fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);
        fireEvent.click(screen.getByText(/Transcribe Audio/i));

        const alert = await screen.findByRole('alert');
        expect(alert).toHaveTextContent('Error: Server down');
    ***REMOVED***);
    */
    /*test('shows retry message on failure and succeeds on second try', async () => {
        axios.post
            .mockRejectedValueOnce(new Error('Temporary error'))
            .mockResolvedValueOnce({ data: { transcript: 'Hello again' ***REMOVED*** ***REMOVED***)
            .mockResolvedValueOnce({ data: { summary: [], actions: [], decisions: [] ***REMOVED*** ***REMOVED***);

        render(<App />);
        const file = new File(['dummy'], 'test.wav', { type: 'audio/wav' ***REMOVED***);
        const input = screen.getByLabelText(/Upload Audio/i);
        fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);
        fireEvent.click(screen.getByText(/Transcribe Audio/i));

        const alert = await screen.findByRole('alert');
        expect(alert).toHaveTextContent(/Temporary error/);

        const retryButton = screen.getByText('Retry');
        fireEvent.click(retryButton);

        await screen.findByText('Transcript:');
        expect(screen.getByText('Transcript:')).toBeInTheDocument();
        expect(screen.getByText('Hello again')).toBeInTheDocument();
    ***REMOVED***);
    */
    test('displays transcript when returned', async () => {
        axios.post.mockResolvedValueOnce({ data: { transcript: 'Meeting notes here' ***REMOVED*** ***REMOVED***);
        axios.post.mockResolvedValueOnce({ data: { summary: [], actions: [], decisions: [] ***REMOVED*** ***REMOVED***);

        render(<App />);
        const file = new File(['dummy'], 'sample.wav', { type: 'audio/wav' ***REMOVED***);
        const input = screen.getByLabelText(/Upload Audio/i);
        fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);
        fireEvent.click(screen.getByText(/Transcribe Audio/i));

        await screen.findByText('Transcript:');
        expect(screen.getByText('Meeting notes here')).toBeInTheDocument();
    ***REMOVED***);
***REMOVED***);
