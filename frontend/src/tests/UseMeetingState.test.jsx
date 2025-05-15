import { renderHook, act } from '@testing-library/react'
import useMeetingState from '../hooks/UseMeetingState'
import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'

const mock = new MockAdapter(axios)

describe('UseMeetingState', () => {
    beforeEach(() => {
        mock.reset()
    })

    it('initial state is correct', () => {
        const { result } = renderHook(() => useMeetingState())
        expect(result.current.transcript).toBe('')
        expect(result.current.summary).toEqual([])
        expect(result.current.actions).toEqual([])
        expect(result.current.decisions).toEqual([])
        expect(result.current.loading).toBe(false)
        expect(result.current.error).toBe('')
        expect(result.current.uploadAttempts).toBe(0)
    })

    it('processAudio sets transcript and updates loading/attempts', async () => {
        const dummyFile = new File(['test'], 'audio.mp3', { type: 'audio/mp3' })
        mock.onPost('/api/transcribe').reply(200, { transcript: 'Test transcript' })

        const { result } = renderHook(() => useMeetingState())

        await act(async () => {
            const success = await result.current.processAudio(dummyFile)
            expect(success).toBe(true)
        })

        expect(result.current.transcript).toBe('Test transcript')
        expect(result.current.uploadAttempts).toBe(1)
        expect(result.current.error).toBe('')
    })

    it('processTranscript sets summary/actions/decisions', async () => {
        const { result } = renderHook(() => useMeetingState())

        act(() => {
            result.current.setTranscript('Test transcript')
        })

        mock.onPost('/api/process').reply(200, {
            summary: ['Point 1'],
            actions: ['Action A'],
            decisions: ['Decision X'],
        })

        await act(async () => {
            await result.current.processTranscript()
        })

        expect(result.current.summary).toEqual(['Point 1'])
        expect(result.current.actions).toEqual(['Action A'])
        expect(result.current.decisions).toEqual(['Decision X'])
    })

    it('handles API error gracefully in processAudio', async () => {
        const dummyFile = new File(['test'], 'audio.mp3', { type: 'audio/mp3' })
        mock.onPost('/api/transcribe').networkError()

        const { result } = renderHook(() => useMeetingState())

        await act(async () => {
            const success = await result.current.processAudio(dummyFile)
            expect(success).toBe(false)
        })

        expect(result.current.error).toMatch(/Error processing audio/i)
    })
})

