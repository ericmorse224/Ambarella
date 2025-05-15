import { render, screen, fireEvent, waitFor ***REMOVED*** from '@testing-library/react';
import App from '../App';
import { vi ***REMOVED*** from 'vitest';
import axios from 'axios';

// Mock only external APIs
vi.mock('axios');

describe('App Component', () => {
    beforeEach(() => {
        axios.post.mockReset();
        axios.get.mockReset();
        vi.spyOn(window, 'alert').mockImplementation(() => { ***REMOVED***);
    ***REMOVED***);

    it('alerts on large file upload', () => {
        render(<App />);
        const fileInput = screen.getByLabelText(/upload audio/i);
        const largeFile = new File(['a'.repeat(11 * 1024 * 1024)], 'large.mp3', { type: 'audio/mpeg' ***REMOVED***);

        fireEvent.change(fileInput, { target: { files: [largeFile] ***REMOVED*** ***REMOVED***);
        expect(window.alert).toHaveBeenCalledWith('File size exceeds 10MB limit');
    ***REMOVED***);

    it('fetches and processes audio correctly', async () => {
        axios.post.mockResolvedValueOnce({ data: { transcript: 'Test transcript' ***REMOVED*** ***REMOVED***);
        axios.post.mockResolvedValueOnce({
            data: {
                summary: ['Summary A'],
                actions: ['Action A'],
                decisions: ['Decision A']
            ***REMOVED***
        ***REMOVED***);

        render(<App />);
        const fileInput = screen.getByLabelText(/upload audio/i);
        const file = new File(['audio'], 'audio.mp3', { type: 'audio/mpeg' ***REMOVED***);

        fireEvent.change(fileInput, { target: { files: [file] ***REMOVED*** ***REMOVED***);
        fireEvent.click(screen.getByRole('button', { name: /Transcribe Audio/i ***REMOVED***));

        await waitFor(() => screen.getByText(/Test transcript/i));
        expect(screen.getByText(/Summary A/i)).toBeInTheDocument();
        expect(screen.getByText(/Decision A/i)).toBeInTheDocument();
    ***REMOVED***);

    it('shows error when Zoho token fetch fails', async () => {
        axios.get.mockRejectedValueOnce(new Error('Network Error'));
        render(<App />);

        const connectBtn = screen.getByRole('button', { name: /Connect to Zoho/i ***REMOVED***);
        fireEvent.click(connectBtn);

        await waitFor(() =>
            expect(screen.getByText(/Error fetching Zoho token/i)).toBeInTheDocument()
        );
    ***REMOVED***);

    it('handles audio API failure gracefully', async () => {
        axios.post.mockRejectedValueOnce(new Error('Network Error'));
        render(<App />);

        const fileInput = screen.getByLabelText(/upload audio/i);
        const file = new File(['audio'], 'audio.mp3', { type: 'audio/mpeg' ***REMOVED***);

        fireEvent.change(fileInput, { target: { files: [file] ***REMOVED*** ***REMOVED***);
        fireEvent.click(screen.getByRole('button', { name: /Transcribe Audio/i ***REMOVED***));

        await waitFor(() =>
            expect(screen.getByText(/Error processing audio/i)).toBeInTheDocument()
        );
    ***REMOVED***);

    it('schedules selected actions and shows success message', async () => {
        axios.post
            .mockResolvedValueOnce({ data: { transcript: 'Test transcript' ***REMOVED*** ***REMOVED***)
            .mockResolvedValueOnce({
                data: {
                    summary: ['Point 1'],
                    actions: ['Action A'],
                    decisions: ['Decision X']
                ***REMOVED***
            ***REMOVED***)
            .mockResolvedValueOnce({ status: 200 ***REMOVED***);

        axios.get.mockResolvedValueOnce({ data: { access_token: 'valid_token' ***REMOVED*** ***REMOVED***);

        render(<App />);

        const fileInput = screen.getByLabelText(/upload audio/i);
        const file = new File(['audio'], 'audio.mp3', { type: 'audio/mpeg' ***REMOVED***);

        fireEvent.change(fileInput, { target: { files: [file] ***REMOVED*** ***REMOVED***);
        fireEvent.click(screen.getByRole('button', { name: /Transcribe Audio/i ***REMOVED***));

        await waitFor(() => screen.getByText(/Action A/i));

        const scheduleBtn = screen.getByRole('button', { name: /Schedule Selected/i ***REMOVED***);
        fireEvent.click(scheduleBtn);

        await waitFor(() =>
            expect(screen.getByText(/Events scheduled successfully/i)).toBeInTheDocument()
        );
    ***REMOVED***);

    it('shows error message when scheduling fails', async () => {
        axios.post
            .mockResolvedValueOnce({ data: { transcript: 'Test transcript' ***REMOVED*** ***REMOVED***)
            .mockResolvedValueOnce({
                data: {
                    summary: ['Point 1'],
                    actions: ['Action A'],
                    decisions: ['Decision X']
                ***REMOVED***
            ***REMOVED***)
            .mockRejectedValueOnce(new Error('Error scheduling events'));

        axios.get.mockResolvedValueOnce({ data: { access_token: 'valid_token' ***REMOVED*** ***REMOVED***);

        render(<App />);

        const fileInput = screen.getByLabelText(/upload audio/i);
        const file = new File(['audio'], 'audio.mp3', { type: 'audio/mpeg' ***REMOVED***);

        fireEvent.change(fileInput, { target: { files: [file] ***REMOVED*** ***REMOVED***);
        fireEvent.click(screen.getByRole('button', { name: /Transcribe Audio/i ***REMOVED***));

        await waitFor(() => screen.getByText(/Action A/i));

        const scheduleBtn = screen.getByRole('button', { name: /Schedule Selected/i ***REMOVED***);
        fireEvent.click(scheduleBtn);

        await waitFor(() =>
            expect(screen.getByText(/Error scheduling events/i)).toBeInTheDocument()
        );
    ***REMOVED***);
***REMOVED***);
