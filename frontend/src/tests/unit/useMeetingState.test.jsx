/**
 * useMeetingState.test.jsx
 * Author: Eric Morse
 * Date: May 11th 2025
 *
 * Unit tests for the useMeetingState React custom hook.
 * This file tests all public functionality of the hook including:
 *  - Initial state
 *  - Audio upload and error handling
 *  - Transcript processing and error handling
 *  - State reset logic
 * The tests use the React Testing Library's renderHook and act helpers, and axios is mocked for network calls.
 */
import { renderHook, act } from '@testing-library/react';
import useMeetingState from '../../hooks/UseMeetingState';
import axios from 'axios';

vi.mock('axios');

describe('useMeetingState', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });
describe('useMeetingState', () => {
    test('initial state is correct', () => {
        const { result } = renderHook(() => useMeetingState());
        expect(result.current.transcript).toBe('');
        expect(result.current.summary).toEqual([]);
        expect(result.current.actions).toEqual([]);
        expect(result.current.decisions).toEqual([]);
        expect(result.current.isLoading).toBe(false);
        expect(result.current.error).toBe(false);
        expect(result.current.uploadAttempts).toBe(0);
    });

    test('processAudio updates state on success', async () => {
        const file = new File(['audio'], 'audio.wav', { type: 'audio/wav' });
        axios.post.mockResolvedValue({ data: { transcript: 'test transcript' } });

        const { result } = renderHook(() => useMeetingState());

        await act(async () => {
            const success = await result.current.processAudio(file);
            expect(success).toBe(true);
        });

        expect(result.current.transcript).toBe('test transcript');
        expect(result.current.isLoading).toBe(false);
        expect(result.current.error).toBe(false);
        expect(result.current.uploadAttempts).toBe(1);
    });

    test('processAudio handles error', async () => {
        const file = new File(['audio'], 'audio.wav', { type: 'audio/wav' });
        axios.post.mockRejectedValue(new Error('fail'));

        const { result } = renderHook(() => useMeetingState());

        await act(async () => {
            const success = await result.current.processAudio(file);
            expect(success).toBe(false);
        });

        expect(result.current.error).toBe('Error processing audio');
        expect(result.current.isLoading).toBe(false);
        expect(result.current.transcript).toBe('');
        expect(result.current.uploadAttempts).toBe(1);
    });

    test('processTranscript updates summary/actions/decisions on success', async () => {
        axios.post.mockResolvedValue({
            data: {
                summary: ['S'],
                actions: ['A'],
                decisions: ['D']
            }
        });

        const { result } = renderHook(() => useMeetingState());

        // First set a transcript so the function will send it
        act(() => result.current.setTranscript('my transcript'));

        await act(async () => {
            await result.current.processTranscript();
        });

        expect(result.current.summary).toEqual(['S']);
        expect(result.current.actions).toEqual(['A']);
        expect(result.current.decisions).toEqual(['D']);
        expect(result.current.isLoading).toBe(false);
        expect(result.current.error).toBe(false);
    });

    test('processTranscript handles error', async () => {
        axios.post.mockRejectedValue(new Error('fail'));

        const { result } = renderHook(() => useMeetingState());
        act(() => result.current.setTranscript('my transcript'));

        await act(async () => {
            await result.current.processTranscript();
        });

        expect(result.current.error).toBe('Error processing transcript');
        expect(result.current.isLoading).toBe(false);
    });

    test('resetTranscript resets all state', () => {
        const { result } = renderHook(() => useMeetingState());
        act(() => {
            result.current.setTranscript('t');
            result.current.setUploadAttempts(3);
        });

        act(() => {
            result.current.resetTranscript();
        });

        expect(result.current.transcript).toBe('');
        expect(result.current.summary).toEqual([]);
        expect(result.current.actions).toEqual([]);
        expect(result.current.decisions).toEqual([]);
        expect(result.current.uploadAttempts).toBe(0);
        expect(result.current.error).toBe(false);
    });
});
});
