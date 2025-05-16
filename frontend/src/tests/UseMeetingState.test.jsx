import { renderHook, act } from '@testing-library/react';
import useMeetingState from '../hooks/UseMeetingState';
import axios from 'axios';

vi.mock('axios');

describe('UseMeetingState', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    test('initial state is correct', () => {
        const { result } = renderHook(() => useMeetingState());

        expect(result.current.transcript).toBe('');
        expect(result.current.summary).toEqual([]);
        expect(result.current.actions).toEqual([]);
        expect(result.current.decisions).toEqual([]);
        expect(result.current.isLoading).toBe(false);
        expect(result.current.error).toBe(false);;
        expect(result.current.uploadAttempts).toBe(0);
    });

    test('processAudio sets transcript and updates loading/attempts', async () => {
        axios.post.mockResolvedValue({ data: { transcript: 'Test transcript' } });

        const { result } = renderHook(() => useMeetingState());

        const file = new File(['audio'], 'audio.mp3', { type: 'audio/mpeg' });

        await act(async () => {
            await result.current.processAudio(file);
        });

        expect(result.current.transcript).toBe('Test transcript');
        expect(result.current.isLoading).toBe(false);
        expect(result.current.uploadAttempts).toBe(1);
        expect(result.current.error).toBe(false);
    });

    test('handles error during processAudio', async () => {
        axios.post.mockRejectedValue(new Error('Network Error'));

        const { result } = renderHook(() => useMeetingState());

        const file = new File(['audio'], 'audio.mp3', { type: 'audio/mpeg' });

        await act(async () => {
            await result.current.processAudio(file);
        });

        expect(result.current.transcript).toBe('');
        expect(result.current.isLoading).toBe(false);
        expect(result.current.uploadAttempts).toBe(1);
        expect(result.current.error).toBe('Error processing audio');
    });

    test('processTranscript sets summary/actions/decisions', async () => {
        axios.post.mockResolvedValue({
            data: {
                summary: 'Summary text',
                actions: ['Action 1', 'Action 2'],
                decisions: ['Decision 1'],
            },
        });

        const { result } = renderHook(() => useMeetingState());

        await act(async () => {
            await result.current.processTranscript('Test transcript');
        });

        expect(result.current.summary).toBe('Summary text');
        expect(result.current.actions).toEqual(['Action 1', 'Action 2']);
        expect(result.current.decisions).toEqual(['Decision 1']);
        expect(result.current.isLoading).toBe(false);
        expect(result.current.error).toBe(false);
    });

    test('handles error during processTranscript', async () => {
        axios.post.mockRejectedValue(new Error('LLM Error'));

        const { result } = renderHook(() => useMeetingState());

        await act(async () => {
            await result.current.processTranscript('Test transcript');
        });

        expect(result.current.summary).toEqual([]);
        expect(result.current.actions).toEqual([]);
        expect(result.current.decisions).toEqual([]);
        expect(result.current.isLoading).toBe(false);
        expect(result.current.error).toBe('Error processing transcript');
    });
});
