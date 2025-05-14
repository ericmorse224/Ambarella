import { render, screen, fireEvent ***REMOVED*** from '@testing-library/react';
import App from './App';
import axios from 'axios';
import { vi ***REMOVED*** from 'vitest';
import React from 'react';

vi.mock('axios');

const originalCreateElement = document.createElement;

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
                return Promise.resolve({
                    data: {
                        summary: ['Summary A'],
                        actions: ['Action A'],
                        decisions: ['Decision A'],
                    ***REMOVED***
                ***REMOVED***);
            ***REMOVED***
        ***REMOVED***);

        render(<App />);

        const file = new File(['dummy'], 'test.wav', { type: 'audio/wav' ***REMOVED***);
        const input = screen.getByLabelText(/Upload Audio/i);
        fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);
        fireEvent.click(screen.getByText(/Transcribe Audio/i));

        const notes = await screen.findAllByText('Meeting notes here.');
        expect(notes.length).toBeGreaterThan(0);

        const summaries = screen.getAllByText('Summary:');
        expect(summaries.length).toBeGreaterThan(0);

        expect(screen.getByText('Decisions:')).toBeInTheDocument();
    ***REMOVED***);

    test('displays transcript when returned', async () => {
        axios.post.mockResolvedValueOnce({ data: { transcript: 'Meeting notes here' ***REMOVED*** ***REMOVED***);
        axios.post.mockResolvedValueOnce({ data: { summary: [], actions: [], decisions: [] ***REMOVED*** ***REMOVED***);

        render(<App />);
        const file = new File(['dummy'], 'sample.wav', { type: 'audio/wav' ***REMOVED***);
        const input = screen.getByLabelText(/Upload Audio/i);
        fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);
        fireEvent.click(screen.getByText(/Transcribe Audio/i));

        const notes = await screen.findAllByText('Meeting notes here');
        expect(notes.length).toBeGreaterThan(0);
    ***REMOVED***);

    describe('Download buttons', () => {
        let clickMock;
        let anchorEl;

        beforeEach(() => {
            clickMock = vi.fn();
            anchorEl = undefined;

            global.Blob = vi.fn((content, options) => ({ content, options ***REMOVED***));
            global.URL.createObjectURL = vi.fn(() => 'blob:test-url');

            global.document.createElement = vi.fn((tagName) => {
                const el = originalCreateElement.call(document, tagName);
                if (tagName === 'a') {
                    el.click = clickMock;
                    anchorEl = el;
                ***REMOVED***
                return el;
            ***REMOVED***);
        ***REMOVED***);

        test('downloads transcript when clicking Download Transcript', async () => {
            axios.post.mockResolvedValueOnce({ data: { transcript: 'Transcript content' ***REMOVED*** ***REMOVED***);
            axios.post.mockResolvedValueOnce({ data: { summary: [], actions: [], decisions: [] ***REMOVED*** ***REMOVED***);

            render(<App />);

            const file = new File(['dummy'], 'sample.wav', { type: 'audio/wav' ***REMOVED***);
            const input = screen.getByLabelText(/Upload Audio/i);
            fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);
            fireEvent.click(screen.getByText(/Transcribe Audio/i));

            const btn = await screen.findByText('Download Transcript');
            fireEvent.click(btn);

            expect(anchorEl.download).toBe('transcript.txt');
            expect(clickMock).toHaveBeenCalled();
        ***REMOVED***);

        test('downloads summary when clicking Download Summary', async () => {
            axios.post.mockResolvedValueOnce({ data: { transcript: 'Dummy transcript' ***REMOVED*** ***REMOVED***);
            axios.post.mockResolvedValueOnce({ data: { summary: ['Summary A'], actions: [], decisions: [] ***REMOVED*** ***REMOVED***);

            render(<App />);

            const file = new File(['dummy'], 'sample.wav', { type: 'audio/wav' ***REMOVED***);
            const input = screen.getByLabelText(/Upload Audio/i);
            fireEvent.change(input, { target: { files: [file] ***REMOVED*** ***REMOVED***);
            fireEvent.click(screen.getByText(/Transcribe Audio/i));

            const btn = await screen.findByText('Download Summary');
            fireEvent.click(btn);

            expect(anchorEl.download).toBe('summary.txt');
            expect(clickMock).toHaveBeenCalled();
        ***REMOVED***);
    ***REMOVED***);
***REMOVED***);
