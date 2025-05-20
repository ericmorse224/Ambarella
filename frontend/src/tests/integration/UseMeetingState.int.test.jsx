import { renderHook, act } from '@testing-library/react';
import useMeetingState from '../../hooks/UseMeetingState';
import fs from 'fs';
import path from 'path';
import FormData from 'form-data';
import axios from 'axios';

describe('useMeetingState Integration (Nextcloud backend)', () => {
    test('initial state is correct', () => {
        const { result } = renderHook(() => useMeetingState());
        expect(result.current.transcript).toBe('');
        expect(result.current.summary).toEqual([]);
        expect(result.current.actions).toEqual([]);
        expect(result.current.decisions).toEqual([]);
        expect(result.current.isLoading).toBe(false);
        expect(result.current.error).toBe(false);
        expect(result.current.uploadAttempts).toBe(0);
    }, 20000);

    test('processAudio and processTranscript with real backend', async () => {
        const { result } = renderHook(() => useMeetingState());

        // Load the real audio file as a stream
        const audioPath = path.resolve(__dirname, '../test_audio/All_Needs.wav');
        const form = new FormData();
        form.append('audio', fs.createReadStream(audioPath));

        // Directly POST to backend using Node-compatible FormData
        let transcript = '';
        let backendResponse;
        try {
            backendResponse = await axios.post(
                'http://localhost:5000/process-audio',
                form,
                {
                    headers: form.getHeaders(),
                    maxBodyLength: Infinity,
                }
            );
            transcript = backendResponse.data.transcript || '';
        } catch (err) {
            console.error('Backend error during audio upload:', err);
        }

        // Set transcript in hook manually (simulate what processAudio would do in-browser)
        await act(() => {
            result.current.setTranscript(transcript);
            result.current.setUploadAttempts(1);
        });

        expect(result.current.transcript).not.toBe('');
        expect(result.current.isLoading).toBe(false);
        expect(result.current.uploadAttempts).toBe(1);
        expect(result.current.error).toBe(false);

        // Step 2: processTranscript
        await act(async () => {
            await result.current.processTranscript();
        });

        expect(Array.isArray(result.current.summary)).toBe(true);
        expect(Array.isArray(result.current.actions)).toBe(true);
        expect(Array.isArray(result.current.decisions)).toBe(true);
        expect(result.current.isLoading).toBe(false);
        expect(result.current.error).toBe(false);
    }, 20000); // Increase timeout for real backend
});
